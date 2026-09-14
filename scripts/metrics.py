#!/usr/bin/env python3
"""Site metrics: per-page views, unique sessions, top referrers, conversions.
Reads data/analytics.jsonl + leads.jsonl + orders.jsonl. Prints a compact report.
--json for machine output.
"""
import json, os, sys, collections, datetime
BASE = "/Users/pino/Code/steuerberatung.ch/data"
def load(name):
    p = os.path.join(BASE, name)
    if not os.path.exists(p): return []
    out = []
    for line in open(p):
        line = line.strip()
        if line:
            try: out.append(json.loads(line))
            except Exception: pass
    return out
an = load("analytics.jsonl")
leads = load("leads.jsonl")
orders = load("orders.jsonl")
pages = collections.Counter()
sessions = collections.defaultdict(set)
refs = collections.Counter()
for r in an:
    pg = r.get("page") or "/"
    pages[pg] += 1
    if r.get("sid"): sessions[pg].add(r["sid"])
    ref = r.get("ref") or ""
    if ref and "steuerberatung.ch" not in ref:
        host = ref.split("/")[2] if ref.count("/") >= 2 else ref
        refs[host] += 1
report = {
    "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "total_views": len(an),
    "total_leads": len(leads),
    "total_orders": len(orders),
    "pages": {p: {"views": pages[p], "sessions": len(sessions[p])} for p in pages},
    "top_referrers": refs.most_common(10),
}
if "--json" in sys.argv:
    print(json.dumps(report, ensure_ascii=False))
else:
    print(f"Views: {len(an)} | Leads: {len(leads)} | Orders: {len(orders)}")
    print("Top pages:")
    for p, c in pages.most_common(12):
        print(f"  {p}: {c} views, {len(sessions[p])} sessions")
    if refs:
        print("Top referrers:", ", ".join(f"{h}({c})" for h, c in refs.most_common(5)))
