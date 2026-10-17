#!/usr/bin/env python3
"""Generate assets/search-index.js — client-side search index over ALL articles (4 languages).

Detection: pages carrying a JSON-LD Article node (article_template.py emits headline/
description/datePublished) — core/tool pages are excluded automatically.
Run after every publish (the content pipeline already runs gen_latest + mksitemap).
"""
import json, re, pathlib, sys, html as H

ROOT = pathlib.Path(__file__).resolve().parent.parent
LANGS = {"de": "", "en": "en/", "fr": "fr/", "it": "it/"}

def strip_tags(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = H.unescape(s)
    return re.sub(r"\s+", " ", s).strip()

def ld_field(t, key):
    m = re.search(r'"%s":\s*"((?:[^"\\]|\\.)*)"' % key, t)
    return json.loads('"%s"' % m.group(1)) if m else ""

entries = []
for lang, pre in LANGS.items():
    base = ROOT / pre
    for f in sorted(base.glob("*.html")):
        t = f.read_text()
        if '"@type": "Article"' not in t and '"@type":"Article"' not in t:
            continue
        title = ld_field(t, "headline") or (re.search(r"<h1[^>]*>([^<]+)</h1>", t) or [None, ""])[1]
        desc = ld_field(t, "description")
        date = ld_field(t, "datePublished")[:10]
        m = re.search(r"<main[^>]*>(.*?)</main>", t, flags=re.S) or re.search(r'(<section class="section".*?)(<!-- RELATED|<footer)', t, flags=re.S)
        body = strip_tags(m.group(1) if m else "")[:4000]
        headings = [strip_tags(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", t, flags=re.S)]
        slug = f.name
        if not title:
            print("WARN no title:", pre + slug, file=sys.stderr)
            continue
        entries.append({"l": lang, "s": slug, "t": title, "d": desc, "dt": date, "h": headings, "b": body})

out = "window.SEARCH_INDEX=" + json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + ";"
(ROOT / "assets/search-index.js").write_text(out)
per = {}
for e in entries: per[e["l"]] = per.get(e["l"], 0) + 1
print(f"indexed {len(entries)} pages {per} -> assets/search-index.js ({len(out)} bytes)")
