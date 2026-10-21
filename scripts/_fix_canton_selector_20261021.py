#!/usr/bin/env python3
"""Replace homepage canton <select> form with an elegant card grid (so.ch-inspired)."""
import json, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CANTONS = json.load(open("/tmp/cantons.json"))  # [code, slug, [de,en,fr,it]]

INTRO = {
 0: ("Steuern nach Kanton", "Alle 26 Kantone im Überblick: Steueramt, eTax-Portal, aktueller Steuerfuss und Fristen.", "Kantone", "Nach Kanton springen"),
 1: ("Taxes by canton", "All 26 cantons at a glance: tax office, e-tax portal, current multiplier and deadlines.", "Cantons", "Jump to a canton"),
 2: ("Impôts par canton", "Les 26 cantons en un coup d’œil: administration fiscale, portail eTax, multiplicateur communal et délais.", "Cantons", "Aller à un canton"),
 3: ("Imposte per cantone", "Tutti i 26 cantoni in una panoramica: amministrazione fiscale, portale eTax, moltiplicatore e scadenze.", "Cantoni", "Vai a un cantone"),
}
FILES = {0: "index.html", 1: "en/index.html", 2: "fr/index.html", 3: "it/index.html"}

pat = re.compile(r'<section class="section"><div class="container"><form class="canton-select".*?</form></div></section>', re.S)

for li, path in FILES.items():
    t = open(path, encoding="utf-8").read()
    if not pat.search(t):
        print("!! no form in", path); continue
    h2, sub, aria, _ = INTRO[li]
    tiles = "".join(
        f'<a href="kanton/{c[1]}.html"><b>{c[0]}</b><span>{c[2][li]}</span></a>' for c in CANTONS)
    new = (f'<section class="section canton-sec"><div class="container">'
           f'<h2>{h2}</h2><p class="muted">{sub}</p>'
           f'<nav class="canton-grid" aria-label="{aria}">{tiles}</nav>'
           f'</div></section>')
    t = pat.sub(lambda m: new, t, count=1)
    open(path, "w", encoding="utf-8").write(t)
    print("rewrote", path)

# CSS: replace .canton-select rules with the grid design
css = open("assets/extra.css", encoding="utf-8").read()
old_rules = ".canton-select{margin:18px 0}\n.canton-select select{padding:10px 14px;font-size:1rem;border:2px solid #d7e0d8;border-radius:10px;background:#fff;min-width:220px}"
if old_rules not in css:
    print("!! css anchor not found"); sys.exit(1)
grid_css = """.canton-sec .muted{margin:-2px 0 14px}
.canton-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(138px,1fr));gap:9px}
.canton-grid a{display:flex;align-items:center;gap:9px;padding:10px 12px;border:1px solid #d7e0d8;border-radius:11px;background:#fff;text-decoration:none;color:#223;transition:border-color .15s,box-shadow .15s,transform .15s}
.canton-grid a:hover{border-color:#2e7d4f;box-shadow:0 3px 10px rgba(46,125,79,.13);transform:translateY(-1px)}
.canton-grid a b{flex:0 0 auto;font-size:.8rem;font-weight:700;color:#2e7d4f;background:#eaf4ee;border-radius:7px;padding:3px 7px;letter-spacing:.02em}
.canton-grid a span{font-size:.92rem}
@media(max-width:640px){.canton-grid{grid-template-columns:repeat(auto-fill,minmax(102px,1fr));gap:7px}.canton-grid a{padding:8px 9px;gap:7px}.canton-grid a span{font-size:.84rem}}"""
css = css.replace(old_rules, grid_css, 1)
open("assets/extra.css", "w", encoding="utf-8").write(css)
print("css updated")

# cache bump on the 4 homepages
for path in FILES.values():
    t = open(path, encoding="utf-8").read()
    t2 = t.replace("extra.css?v=7", "extra.css?v=8")
    if t != t2:
        open(path, "w", encoding="utf-8").write(t2); print("bumped", path)
