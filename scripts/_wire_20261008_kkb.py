#!/usr/bin/env python3
"""Wire krankenkassenpramien-steuerabzug into 4 ratgeber lists + mark jsonl records."""
import json, os, re

ROOT = "/Users/pino/Code/steuerberatung.ch"
SLUG = "krankenkassenpramien-steuerabzug.html"
LISTS = {
    "de": (os.path.join(ROOT, "ratgeber.html"), "Krankenkassenprämien und Steuern: Was Sie 2026 wirklich abziehen können"),
    "en": (os.path.join(ROOT, "en", "ratgeber.html"), "Health insurance premiums and taxes: what you can actually deduct"),
    "fr": (os.path.join(ROOT, "fr", "ratgeber.html"), "Primes d'assurance-maladie et impôts : ce que vous pouvez réellement déduire"),
    "it": (os.path.join(ROOT, "it", "ratgeber.html"), "Premi dell'assicurazione malattie e imposte: cosa potete davvero dedurre"),
}
ANCHOR_RE = re.compile(r'<li><a href="' + re.escape(SLUG) + r'">')

for lang, (path, title) in LISTS.items():
    txt = open(path, encoding="utf-8").read()
    if ANCHOR_RE.search(txt):
        print(lang, "ratgeber: already wired")
        continue
    lines = txt.split("\n")
    # insert after the last list item in the tick/praxis-tipps list (use the
    # steuern-sparen-tipps li as anchor if present, else saeule-3a-nachzahlen)
    idx = None
    for pat in ('href="steuer-checkliste-2026.html"', 'href="saeule-3a-nachzahlen.html"'):
        for i, l in enumerate(lines):
            if "<li><a href=" in l and pat in l:
                idx = i
                break
        if idx is not None:
            break
    if idx is None:
        raise SystemExit(f"{lang}: anchor not found")
    indent = re.match(r"\s*", lines[idx]).group(0)
    lines.insert(idx + 1, f'{indent}<li><a href="{SLUG}">{title}</a></li>')
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    print(lang, f"ratgeber: inserted after line {idx+1}")

# jsonl updates
recs = []
jl = os.path.join(ROOT, "data", "content-research.jsonl")
with open(jl, encoding="utf-8") as f:
    for line in f:
        s = line.rstrip("\n")
        recs.append(s)

changed = {"kkb": False, "gz": False}
out = []
for s in recs:
    t = s.strip()
    if t:
        try:
            r = json.loads(t)
        except Exception:
            out.append(s); continue
        if r.get("slug") == SLUG[:-5] and r.get("status") != "published":
            r["status"] = "published"
            r["langs"] = ["de", "en", "fr", "it"]
            r["published_at"] = "2026-10-08"
            r["verified_at"] = "2026-10-08"
            r["verified_by"] = ("ESTV Abzuege-Ansaetze-Tarife DBST (Pauschalabzug 1800/2700/3700/5550/700, "
                                "KS 11a 26.5.2026 Selbstbehalt 5 % DB; Kt. SG 2 % Beispiel; "
                                "BAG MM 29.9.2026 Praemie 2027 CHF 412 +5.0 % / 487.60 +4.9 %). "
                                "Kantonale Maximalbetaege Vergleichsportale NICHT verifiziert und nicht publiziert.")
            out.append(json.dumps(r, ensure_ascii=False))
            changed["kkb"] = True
            continue
        if r.get("slug") == "grenzgaenger-homeoffice-telearbeit-regeln" and r.get("status") == "pending":
            r["status"] = "published"
            r["langs"] = ["de", "en", "fr", "it"]
            r["published_at"] = "2026-10-05"
            r["note"] = "status corrected 2026-10-08: file shipped in all 4 langs (de/en/fr/it grenzgaenger-homeoffice-telearbeit-regeln.html live, HTTP 200)"
            out.append(json.dumps(r, ensure_ascii=False))
            changed["gz"] = True
            continue
    out.append(s)
with open(jl, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("jsonl kkb->published:", changed["kkb"], "| grenzgaenger-homeoffice corrected:", changed["gz"])
