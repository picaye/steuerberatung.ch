#!/usr/bin/env python3
"""Add the Suche/Search/Recherche/Ricerca nav link to every page, after the Rechner link."""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINK = {"de": '<a href="suche.html">Suche</a>', "en": '<a href="search.html">Search</a>',
        "fr": '<a href="recherche.html">Recherche</a>', "it": '<a href="ricerca.html">Ricerca</a>'}
ANCHOR = {"de": '<a href="rechner.html">Rechner</a>', "en": '<a href="rechner.html">Calculator</a>',
          "fr": '<a href="rechner.html">Calculateur</a>', "it": '<a href="rechner.html">Calcolatore</a>'}

changed = 0
for lang, pre in [("de", ""), ("en", "en/"), ("fr", "fr/"), ("it", "it/")]:
    for f in (ROOT / pre).glob("*.html"):
        t = f.read_text()
        if LINK[lang] in t:
            continue
        a = ANCHOR[lang]
        if a in t:
            t = t.replace(a, a + "\n      " + LINK[lang], 1)
            f.write_text(t)
            changed += 1
        else:
            print("NO NAV ANCHOR:", pre + f.name)
print("pages updated:", changed)
