#!/usr/bin/env python3
"""Annotate the 2026-10-17 research cards with a calendar-contention note.

Publish calendar v2 (issue #8, Pino-approved 2026-10-16) already assigns one
card to every Friday Nov 6 - Feb 26. The five cards appended by this research
run carry true seasonal peaks that fall inside those weeks, so each gets an
explicit note: on a contested Friday the calendar card goes first, and this
card rolls into the Mar-Apr second pass / re-pin. Rewritten atomically,
read-only otherwise. Run: python3 scripts/_annotate_20261017_calendar.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "content-research.jsonl")

# slug -> (Friday, card that owns that slot in calendar v2)
NOTES = {
    "revisionsstelle-opting-out-handelsregister": ("Fr 2026-11-20", "verrechnungssteuer-meldeverfahren-dividende"),
    "aialg-lohndaten-austausch-2027": ("Fr 2026-12-18", "pauschalspesen-spesenreglement-genehmigt"),
    "mwst-gruppenbesteuerung-art-13": ("Fr 2026-11-27", "bvg-mindestzins-2027"),
    "ahv-arbeitgeberkontrolle-nachzahlung": ("Fr 2027-01-15", "steuererklaerung-fristerstreckung-2027"),
    "mwst-vorsteuerkorrektur-liegenschaft": ("Fr 2026-12-11", "quellensteuer-abrechnung-arbeitgeber-pflichten"),
}
MARK = "Kalender-Notiz (Run 2026-10-17)"

lines = open(QUEUE, encoding="utf-8").read().splitlines()
out, touched = [], []
for raw in lines:
    if not raw.strip():
        out.append(raw)
        continue
    rec = json.loads(raw)
    slug = rec.get("slug")
    if slug in NOTES and rec.get("date") == "2026-10-17" and MARK not in (rec.get("why") or ""):
        friday, owner = NOTES[slug]
        rec["why"] += (
            f" {MARK}: Der Pin liegt in einer Woche, die im freigegebenen "
            f"Publish-Kalender v2 (issue #8) bereits an {owner} geht ({friday}). "
            f"Bei gleichem Demand-Pegel hat die Kalender-Karte den Slot zuerst; "
            f"diese Karte rückt in den Mar-Apr-Second-Pass und wird dort auf das "
            f"nächste Peak-Fenster neu gepinnt, falls das Fenst"
            "er bis dahin durch ist."
        )
        touched.append(slug)
        out.append(json.dumps(rec, ensure_ascii=False))
    else:
        out.append(json.dumps(rec, ensure_ascii=False) if raw.strip() else raw)

tmp = QUEUE + ".tmp-20261017"
with open(tmp, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
os.replace(tmp, QUEUE)
print(f"annotated {len(touched)}: {', '.join(touched)}")
