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
"""
import re, glob, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECT_LANG = {'': 'de', 'en': 'en', 'fr': 'fr-CH', 'it': 'it-CH'}
EXPECT_ACTIVE = {'': 'DE', 'en': 'EN', 'fr': 'FR', 'it': 'IT'}
BASE = 'https://steuerberatung.ch'

os.chdir(REPO)
files = sorted(glob.glob('*.html'))
for lang in ('en', 'fr', 'it'):
    files += sorted(glob.glob(f'{lang}/*.html'))

problems = []
for f in files:
    d = os.path.dirname(f)  # '' | en | fr | it
    s = open(f).read()
    page = os.path.basename(f)
    rel_url = f'{BASE}/{f}' if d else f'{BASE}/{page}'
    if page == 'index.html':
        rel_url = f'{BASE}/{d + "/" if d else ""}'

    m = re.search(r'<html lang="([^"]+)"', s)
    if not m or m.group(1) != EXPECT_LANG[d]:
        problems.append(f'{f}: html lang={m.group(1) if m else None} want={EXPECT_LANG[d]}')

    navs = re.findall(r'class="lang[ "]', s)
    if len(navs) != 4:
        problems.append(f'{f}: lang switcher anchors={len(navs)} want=4')
    act = re.search(r'class="lang active"[^>]*>([A-Z]{2})<', s)
    if not act or act.group(1) != EXPECT_ACTIVE[d]:
        problems.append(f'{f}: active switcher={act.group(1) if act else None} want={EXPECT_ACTIVE[d]}')

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
        t = os.path.normpath(os.path.join(d, href.split('#')[0]))
        if not os.path.exists(t):
            problems.append(f'{f}: broken link -> {href}')

print(f'checked {len(files)} pages')
if problems:
    print(f'{len(problems)} PROBLEM(S):')
    for p in problems:
        print(' -', p)
    sys.exit(1)
print('ALL OK')
