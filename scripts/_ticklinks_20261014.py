#!/usr/bin/env python3
"""Add the 5 new articles to ratgeber.html tick lists in all 4 languages."""
import pathlib, re

SLUGS = ["eu-zoll-3-euro-kleinsendungen", "minijobs-lohnschwelle-ahv-pflicht",
         "mwst-ausfuhr-0-prozent-nachweis", "quellensteuer-nov-zusatzabzuege",
         "kapitalsteuer-ag-gmbh"]

def title_of(lang, slug):
    p = pathlib.Path("index.html") if lang == "de" else None
    f = pathlib.Path(f"{slug}.html") if lang == "de" else pathlib.Path(f"{lang}/{slug}.html")
    t = f.read_text()
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", t)
    if m: return m.group(1).strip()
    m = re.search(r'"headline":\s*"([^"]+)"', t)
    return m.group(1)

for lang in ["de", "en", "fr", "it"]:
    rg = pathlib.Path("ratgeber.html") if lang == "de" else pathlib.Path(f"{lang}/ratgeber.html")
    t = rg.read_text()
    m = re.search(r'(<ul class="tick">\n)', t)
    if not m:
        print(lang, "NO TICK LIST"); continue
    items = []
    for s in SLUGS:
        title = title_of(lang, s)
        items.append(f'      <li><a href="{s}.html">{title}</a></li>')
    t = t.replace(m.group(1), m.group(1) + "\n".join(items) + "\n", 1)
    rg.write_text(t)
    print(lang, "added", len(items), "tick links")
