#!/usr/bin/env python3
"""v2: reschedule pins onto a Wed+Fri publishing calendar (2/wk peak, min 1/wk guaranteed)."""
import json, datetime, pathlib, sys

ROOT = pathlib.Path("/Users/pino/Code/steuerberatung.ch")
JL = ROOT / "data/content-research.jsonl"

slots = []
d = datetime.date(2026, 10, 28)
while d <= datetime.date(2028, 6, 30):
    if d.weekday() in (2, 4) and not (d.month == 12 and d.day == 23) and not (d.month == 12 and d.day == 30) and not (d.month == 1 and d.day == 1) and not (d.month == 1 and d.day == 5):
        slots.append(d)
    d += datetime.timedelta(days=1)

cards = [json.loads(l) for l in open(JL)]
art = [c for c in cards if c.get("status") == "pending" and c.get("type") in (None, "article") and c.get("hold_until")]

FIXED = {
    "ahv2030-reform-beitraege-fruehrente": "2026-11-13",
    "lohnabrechnung-2027-ahv-iv-eo-neue-werte": "2026-12-04",
    "kassabuch-twint-aufzeichnung-pflicht-jahresende": "2026-12-16",
    "ubs-cs-migration-steuererklaerung-2026": "2027-01-06",
    "generalversammlung-2027-gewinn-dividende-steuer": "2027-02-03",
}
DEADLINE = {
    "mwst-erhoehung-2027-ahv-armee": "2026-11-27",
    "fairness-initiative-ehepaare-2026": "2026-11-27",
    "saeule-3a-jahresende-einzahlung-2026": "2026-12-16",
    "mwst-option-wechsel-frist-31-dezember": "2026-12-11",
    "stille-reserven-eigenkapitalaufbau-jahresende": "2026-12-09",
    "mwst-vorsteuer-eigenverbrauch-jahresende": "2026-12-16",
    "mwst-abmeldung-unter-100000-jahresende": "2026-12-16",
    "pauschalspesen-spesenreglement-genehmigt": "2027-01-27",
    "sachzuwendungen-mitarbeitende-600-freigrenze": "2027-01-08",
    "w-8ben-us-quellensteuer-erneuern": "2027-02-05",
    "bvg-mindestzins-2027": "2026-12-09",
    "quellensteuer-abrechnung-arbeitgeber-pflichten": "2027-01-29",
    "verrechnungssteuer-meldeverfahren-dividende": "2026-12-16",
    "ferien-auszahlen-steuern-ahv": "2027-01-08",
    "aialg-lohndaten-austausch-2027": "2027-02-26",
    "ahv-quartalsbeitraege-selbststaendige-jahresausgleich": "2027-01-27",
    "pauschale-rueckstellungen-grossreparaturen-2026": "2026-12-09",
    "arbeitgeber-3a-beitrag-lohnausweis": "2026-12-09",
    "carif-krypto-datenaustausch-ab-2027": "2027-01-06",
    "ahv-lohnabrechnung-annualisieren-frist-31-januar": "2027-01-27",
    "steuererklaerung-fristerstreckung-2027": "2027-03-19",
    "saeule-3a-beguenstigte-neu-2027": "2026-12-16",
}
D = {"high": 0, "medium": 1, "low": 2}
for c in art:
    c["_rel"] = datetime.date.fromisoformat(c["hold_until"]) - datetime.timedelta(days=21)  # prep pieces may lead their nominal date by up to 3 weeks
    c["_dl"] = datetime.date.fromisoformat(DEADLINE[c["slug"]]) if c.get("slug") in DEADLINE else None

plan, free = {}, list(slots)
for slug, when in FIXED.items():
    f = datetime.date.fromisoformat(when)
    assert f in free, f"{when} not in slot grid"
    plan[f] = slug
    free.remove(f)

open_cards = [c for c in art if c["slug"] not in FIXED]
for slot in slots:
    if slot in plan:
        continue
    elig = [c for c in open_cards if c["_rel"] <= slot and (c["_dl"] is None or c["_dl"] >= slot)]
    if not elig:
        continue
    elig.sort(key=lambda c: (c["_dl"] or datetime.date(2099, 1, 1), c["_rel"], D.get(c.get("demand"), 3), c["slug"]))
    pick = elig[0]
    plan[slot] = pick["slug"]
    open_cards.remove(pick)

print("planned:", len(plan), "| slots:", len(slots), "| unplaced:", sorted(c["slug"] for c in open_cards))
for c in art:
    if c["_dl"]:
        got = next((s for s, sl in plan.items() if sl == c["slug"]), None)
        if got and got > c["_dl"]:
            print("!! LATE:", c["slug"], got, ">", c["_dl"])

if len(sys.argv) > 1 and sys.argv[1] == "--apply":
    byslug = {c["slug"]: c for c in cards if "slug" in c}
    for s, slug in plan.items():
        card = byslug[slug]
        card["hold_until"] = str(s)
        card["priority"] = "pin-" + str(s)
    with open(JL, "w") as f:
        for c in cards:
            clean = {k: v for k, v in c.items() if not k.startswith("_")}
            f.write(json.dumps(clean, ensure_ascii=False) + "\n")
    print("APPLIED", len(plan), "pins")
    # print human calendar
    for s in sorted(plan):
        print(s.strftime("%Y-%m-%d %a"), "->", plan[s])
