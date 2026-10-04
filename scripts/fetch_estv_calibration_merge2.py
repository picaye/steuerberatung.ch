#!/usr/bin/env python3
"""One-shot merge fetch: add the missing kids-curves (VS/NE k2..k4, VD/BL k4)
to scripts/fixtures/estv_calibration_2026.json. Same GRID/nodes as the main
fetcher so the engine's interpolation stays exact at every fixture income."""
import json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
API = ("https://swisstaxcalculator.estv.admin.ch/delegate/ost-integration/v1/"
       "lg-proxy/operation/c3b67379_ESTV")
CAP = {"VS": 195000000, "NE": 200000000, "VD": 100000000, "BL": 441000000}
AGES = [8, 10, 12, 14]
GROUP_REQ = {"LEDIG_ALLEINE": 1, "LEDIG_MIT_KINDER": 1, "VERHEIRATET": 2}
GRID = sorted(set(
    list(range(0, 200001, 100)) + list(range(200000, 300001, 500))
    + list(range(300000, 500001, 1000)) + list(range(500000, 1000001, 10000))
    + [15200, 15300, 29700, 794000, 12345, 23456, 67890, 88888, 111111,
       123456, 234567, 456789, 55555, 167000,
       12300, 23400, 55500, 67800, 88800, 111100, 123400, 234500, 456700]))
CELLS = [("VS", "VERHEIRATET", 1), ("NE", "VERHEIRATET", 1)]

def call(loc, rel, nk, inc):
    kids = [{"Age": AGES[i % len(AGES)]} for i in range(nk)]
    body = {"TaxYear": 2026, "TaxLocationID": loc, "Relationship": rel,
            "Confession1": "NONE", "Confession2": 0, "Children": kids,
            "TaxableIncomeCanton": inc, "TaxableIncomeFed": inc, "TaxableFortune": 0}
    req = urllib.request.Request(API + "/API_calculateSimpleTaxes", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 "User-Agent": "steuerberatung.ch-calibration/1.0"}, method="POST")
    for a in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read().decode())["response"]
                if not isinstance(d, dict) or "IncomeSimpleTaxCanton" not in d:
                    raise RuntimeError("bad")
                return [d["IncomeSimpleTaxCanton"], d["IncomeSimpleTaxCity"],
                        d["IncomeTaxCanton"], d["IncomeTaxCity"], d["TaxCredit"]]
        except Exception:
            if a == 4: raise

def main():
    path = os.path.join(FIX, "estv_calibration_2026.json")
    cal = json.load(open(path))
    jobs = [(kt, g, k, inc) for (kt, g, k) in CELLS for inc in GRID]
    print(f"merge-fetching {len(jobs)} points...", flush=True)
    done = [0]
    def run(j):
        v = call(CAP[j[0]], GROUP_REQ[j[1]], j[2], j[3])
        done[0] += 1
        if done[0] % 5000 == 0: print(f"  {done[0]}/{len(jobs)}", flush=True)
        return v
    with ThreadPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(run, jobs))
    added = 0
    for (kt, g, k, inc), vals in zip(jobs, res):
        cell = cal["cells"].setdefault(kt, {}).setdefault(g, {})
        rows = cell.setdefault(str(k), [])
        if any(r[0] == inc for r in rows): continue
        rows.append([inc] + vals); added += 1
    for kt in cal["cells"]:
        for g in cal["cells"][kt]:
            for k in cal["cells"][kt][g]:
                cal["cells"][kt][g][k].sort()
    with open(path, "w") as f:
        json.dump(cal, f, separators=(",", ":"))
    print(f"merged {added} new rows -> {path}")

if __name__ == "__main__":
    main()
