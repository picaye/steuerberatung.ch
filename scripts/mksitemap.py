#!/usr/bin/env python3
import os, glob, datetime
BASE = "/Users/pino/Code/steuerberatung.ch"
SITE = "https://steuerberatung.ch"
files = sorted(glob.glob(BASE + "/*.html"))
for lang in ("en", "fr", "it"):
    files += sorted(glob.glob(BASE + f"/{lang}/*.html"))
urls = []
for f in files:
    rel = os.path.relpath(f, BASE)
    if rel.endswith("/index.html"):
        path = "/" if rel == "index.html" else "/" + os.path.dirname(rel) + "/"
    else:
        path = "/" + rel
    urls.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>")
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
open(BASE + "/sitemap.xml", "w").write(xml)
print("sitemap:", len(urls), "urls")
