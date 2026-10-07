#!/usr/bin/env python3
"""Move the LATEST article block to directly after the homepage hero.
DE/FR/IT: hero is <section class="hero"> -> insert after its </section>.
EN: hero is a page-head div -> insert after the trust-row close '</div></div>'.
Idempotent: if the block already sits right after the hero, no-op."""
import re

for f in ["index.html", "en/index.html", "fr/index.html", "it/index.html"]:
    t = open(f, encoding="utf-8").read()
    m = re.search(r"\n?<!-- LATEST:START -->.*?<!-- LATEST:END -->", t, re.S)
    if not m:
        print(f, "NO BLOCK"); continue
    block = m.group(0).lstrip("\n")
    t2 = (t[:m.start()] + t[m.end():]).replace("</section>\n\n", "</section>\n")
    hero = t2.find('<section class="hero">')
    if hero != -1:
        close = t2.find("</section>", hero) + len("</section>")
    else:
        a = re.search(r'<div class="trust-row">.*?</div>\n</div></div>', t2, re.S)
        if not a:
            print(f, "NO HERO ANCHOR - skipped"); continue
        close = a.end()
    t2 = t2[:close] + "\n" + block + t2[close:]
    open(f, "w", encoding="utf-8").write(t2)
    h1 = t2.find("<h1"); lat = t2.find("LATEST:START")
    nxt = t2.find("</section>", lat)
    print(f, "latest@%d after_hero=%s doctype_ok=%s" % (lat, h1 < lat, t2.startswith("<!DOCTYPE html>")))
