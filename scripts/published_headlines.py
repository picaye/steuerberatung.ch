#!/usr/bin/env python3
"""Print one line per published article: <slug>\t<JSON-LD headline>.

Scans *.html in the repo root (DE) plus en/ fr/ it/ mirrors and reads the
headline from each page's JSON-LD Article node. Used by the publish cron for
topic-level dedupe (slug-based dedupe alone misses articles that shipped
under a different slug than their research record).
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def headlines_for(path):
    try:
        html = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    out = []
    for m in re.finditer(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        html, re.S,
    ):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        nodes = data if isinstance(data, list) else [data]
        for n in nodes:
            if isinstance(n, dict) and n.get("@type") == "Article":
                h = n.get("headline")
                if h:
                    out.append(h)
    return out

def main():
    paths = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    for lang in ("en", "fr", "it"):
        paths += sorted(glob.glob(os.path.join(ROOT, lang, "*.html")))
    seen = set()
    for p in paths:
        rel = os.path.relpath(p, ROOT)
        slug = os.path.basename(p)[:-5]
        for h in headlines_for(p):
            key = (slug, h)
            if key in seen:
                continue
            seen.add(key)
            print(f"{slug}\t{h}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
