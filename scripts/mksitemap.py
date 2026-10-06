#!/usr/bin/env python3
import os, glob, json, datetime, subprocess
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://steuerberatung.ch"
# Guard (t_58b0adf3): only pages tracked in git enter the sitemap — an
# unshipped draft in a dirty working tree must never leak a 404 URL.
try:
    _r = subprocess.run(["git", "-C", BASE, "ls-files", "--cached"],
                        capture_output=True, text=True, timeout=15)
    tracked = set(_r.stdout.split()) if _r.returncode == 0 else None
except Exception:
    tracked = None
files = sorted(glob.glob(BASE + "/*.html"))
for lang in ("en", "fr", "it"):
    files += sorted(glob.glob(BASE + f"/{lang}/*.html"))
if tracked is not None:
    dropped = [f for f in files
               if os.path.relpath(f, BASE) not in tracked]
    for f in dropped:
        print("SKIP (untracked):", os.path.relpath(f, BASE))
    files = [f for f in files if os.path.relpath(f, BASE) in tracked]
# Guard (issue #5 / Foreman): a tracked page whose content-research record is
# still status:pending is staged, not published — keep it out of the sitemap.
def _pending_slugs():
    slugs = set()
    try:
        for line in open(os.path.join(BASE, "data", "content-research.jsonl"), encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("status") == "pending" and r.get("slug"):
                slugs.add(r["slug"])
    except FileNotFoundError:
        pass
    return slugs
_pending = _pending_slugs()
if _pending:
    kept = []
    for f in files:
        stem = os.path.splitext(os.path.basename(f))[0]
        if stem in _pending:
            print("SKIP (status:pending):", os.path.relpath(f, BASE))
        else:
            kept.append(f)
    files = kept
urls = []
for f in files:
    # Staged/draft pages carry <meta name="robots" content="noindex"> — keep them out of the sitemap.
    with open(f, encoding="utf-8", errors="ignore") as fh:
        head = fh.read(4096)
    if 'name="robots"' in head and "noindex" in head:
        continue
    rel = os.path.relpath(f, BASE)
    if rel.endswith("/index.html"):
        path = "/" if rel == "index.html" else "/" + os.path.dirname(rel) + "/"
    else:
        path = "/" + rel
    urls.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>")
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
open(BASE + "/sitemap.xml", "w").write(xml)
print("sitemap:", len(urls), "urls")
