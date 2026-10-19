#!/usr/bin/env python3
"""Whole-site validator for steuerberatung.ch (4-language static site).

Run from anywhere:  python3 <repo>/scripts/validate_site.py
Exit 0 = all checks pass; exit 1 with a report otherwise.

Checks per page (root DE + en/ fr/ it/):
  1. html lang attribute matches directory (de/en/fr-CH/it-CH)
  2. exactly 4 lang-switcher anchors; the current language one active+aria-current
  3. exactly 5 hreflang alternates (de-CH/en/fr-CH/it-CH/x-default)
  4. canonical present and pointing at this language's URL
  5. assets referenced with the right prefix (../assets/ in lang dirs, assets/ at root)
  6. every internal href resolves to an existing file
  7. no cross-language leakage: lang-dir pages must not link ../<page>.html
     when <page>.html exists in their own dir
  8. RELATED block (where present): exactly 3 internal links, no self-link,
     all resolving inside the page's own language dir, no cross-language hrefs
"""
import re, glob, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECT_LANG = {'': 'de', 'kanton': 'de', 'en': 'en', 'fr': 'fr-CH', 'it': 'it-CH'}
EXPECT_ACTIVE = {'kanton': 'DE', '': 'DE', 'en': 'EN', 'fr': 'FR', 'it': 'IT'}
BASE = 'https://steuerberatung.ch'

os.chdir(REPO)
files = sorted(glob.glob('*.html')) + sorted(glob.glob('kanton/*.html'))
for lang in ('en', 'fr', 'it'):
    files += sorted(glob.glob(f'{lang}/*.html'))
    files += sorted(glob.glob(f'{lang}/kanton/*.html'))

files = [f for f in files if 'yandex_' not in f]
problems = []
for f in files:
    d = os.path.dirname(f)  # '' | en | fr | it
    s = open(f).read()
    page = os.path.basename(f)
    rel_url = f'{BASE}/{f}' if d else f'{BASE}/{page}'
    if page == 'index.html':
        rel_url = f'{BASE}/{d + "/" if d else ""}'

    m = re.search(r'<html lang="([^"]+)"', s)
    if not m or m.group(1) != EXPECT_LANG[d.split('/')[0]]:
        problems.append(f'{f}: html lang={m.group(1) if m else None} want={EXPECT_LANG[d.split('/')[0]]}')

    # noindex stub pages (e.g. rechner.html takedown) carry no switcher/hreflang
    if 'content="noindex' in s:
        continue

    navs = re.findall(r'class="lang[ "]', s)
    if len(navs) != 4:
        problems.append(f'{f}: lang switcher anchors={len(navs)} want=4')
    act = re.search(r'class="lang active"[^>]*>([A-Z]{2})<', s)
    if not act or act.group(1) != EXPECT_ACTIVE[d.split('/')[0]]:
        problems.append(f'{f}: active switcher={act.group(1) if act else None} want={EXPECT_ACTIVE[d.split('/')[0]]}')

    hl = s.count('hreflang=')
    if hl != 5:
        problems.append(f'{f}: hreflang count={hl} want=5')

    canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if not canon:
        problems.append(f'{f}: missing canonical')
    elif canon.group(1) != rel_url:
        problems.append(f'{f}: canonical={canon.group(1)} want={rel_url}')

    if d:
        if 'href="../assets/' not in s and '../assets/' not in s:
            problems.append(f'{f}: assets not rebased to ../assets/')
        # cross-language leakage: ../<page>.html where <page>.html exists in own dir
        for href in set(re.findall(r'href="\.\./([a-z0-9-]+\.html)"', s)):
            if href != 'index.html' and os.path.exists(f'{d}/{href}'):
                problems.append(f'{f}: leaks to ../{href} (exists as {d}/{href})')
    else:
        if '../assets/' in s:
            problems.append(f'{f}: root page must not use ../assets/')

# link resolution across the whole site
for f in files:
    d = os.path.dirname(f)
    for href in re.findall(r'href="([^"]+)"', open(f).read()):
        if href.startswith(('http', 'mailto:', '#', 'tel:')):
            continue
        path = href.split('#')[0].split('?')[0]
        if not path:
            continue
        if path.startswith('/'):
            # site-absolute URL -> resolve against repo root
            t = os.path.normpath(os.path.join('.', path.lstrip('/')))
        else:
            t = os.path.normpath(os.path.join(d, path))
        if not os.path.exists(t):
            problems.append(f'{f}: broken link -> {href}')

# 8. RELATED block well-formedness (t_b74df8d0, CTO 2026-10-16):
#    multilingual related blocks are the site rule — every page that carries
#    a RELATED block must have exactly 3 internal links, no self-link, all
#    resolving inside its own language dir, and no cross-language hrefs.
rel_pages = 0
for f in files:
    s = open(f, encoding='utf-8').read()
    if 'RELATED:START' not in s:
        continue
    rel_pages += 1
    d = os.path.dirname(f)
    page = os.path.basename(f)
    m = re.search(r'RELATED:START(.*?)RELATED:END', s, re.S)
    if not m:
        problems.append(f'{f}: RELATED:START without matching RELATED:END')
        continue
    hrefs = re.findall(r'href="([^"]+)"', m.group(1))
    if len(hrefs) != 3:
        problems.append(f'{f}: RELATED links={len(hrefs)} want=3')
    for href in hrefs:
        if href.startswith(('http', 'mailto:', 'tel:', '#')):
            problems.append(f'{f}: RELATED link not internal: {href}')
            continue
        path = href.split('#')[0].split('?')[0]
        if not path or path.startswith('/') or path.startswith('../') \
                or re.match(r'(en|fr|it)/', path):
            problems.append(f'{f}: RELATED cross-language/absolute href: {href}')
            continue
        if path == page:
            problems.append(f'{f}: RELATED self-link: {href}')
        if not os.path.exists(os.path.normpath(os.path.join(d, path))):
            problems.append(f'{f}: RELATED broken link -> {href}')
print(f'RELATED gate: {rel_pages} pages with block checked')

# 8. inline JS must parse (node --check) — catches string/regex bugs before push
#    (t_47f77cb2: broken 3a-rechner JS passed CI 3x because nothing ever
#    parsed the inline <script> blocks shipped inside HTML pages.)
#    Match <script> with optional attributes but skip non-JS types (ld+json).
import subprocess, tempfile
inline_checked = 0
inline_files = []
for f in files:
    s = open(f, encoding='utf-8').read()
    hit = 0
    for i, m in enumerate(re.finditer(r'<script((?![^>]*type="application/ld\+json")[^>]*)>(.*?)</script>', s, re.S)):
        attrs, js = m.group(1), m.group(2)
        if 'src=' in attrs:
            continue  # external script — not inline
        if len(js.strip()) < 10:
            continue  # skip empty/placeholder blocks
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as tf:
            tf.write(js); tmp = tf.name
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        inline_checked += 1; hit += 1
        if r.returncode != 0:
            # node's stderr ends with a version banner; surface the SyntaxError line
            err = next((ln for ln in r.stderr.splitlines() if 'Error' in ln),
                       r.stderr.strip().splitlines()[-1] if r.stderr.strip() else '?')
            problems.append(f'{f}: inline script #{i} syntax error: {err.strip()}')
        os.unlink(tmp)
    if hit:
        inline_files.append(f'{f} ({hit})')
print(f'inline JS gate: {inline_checked} inline scripts parsed with node --check')
print('inline JS gate files: ' + ', '.join(inline_files))

print(f'checked {len(files)} pages')
if problems:
    print(f'{len(problems)} PROBLEM(S):')
    for p in problems:
        print(' -', p)
    sys.exit(1)
print('ALL OK')
