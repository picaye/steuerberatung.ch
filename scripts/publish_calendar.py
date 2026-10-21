#!/usr/bin/env python3
"""Publish calendar helper: which Wed/Fri slots are taken, which are free.
Usage: publish_calendar.py [--free]  (default: full calendar)"""
import json, datetime, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
cards = [json.loads(l) for l in open(ROOT / "data/content-research.jsonl")]
taken = {}
for c in cards:
    if c.get("status") == "pending" and c.get("hold_until"):
        taken.setdefault(c["hold_until"], []).append(c.get("slug", "?"))
d, slots = datetime.date(2026, 10, 28), []
while d <= datetime.date(2028, 6, 30):
    if d.weekday() in (2, 4) and d not in (datetime.date(2026,12,23), datetime.date(2026,12,30), datetime.date(2027,1,1), datetime.date(2027,1,5)):
        slots.append(d)
    d += datetime.timedelta(days=1)
if "--free" in sys.argv:
    for s in slots:
        if str(s) not in taken:
            print(s)
    print("# taken count:", len(taken), "| free count:", sum(1 for s in slots if str(s) not in taken))
else:
    for s in slots:
        if str(s) in taken:
            print(s, "->", ", ".join(taken[str(s)]))
