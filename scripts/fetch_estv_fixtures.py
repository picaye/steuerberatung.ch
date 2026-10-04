#!/usr/bin/env python3
"""Fetch parity fixtures from the official ESTV Swiss Tax Calculator API.

Source: https://swisstaxcalculator.estv.admin.ch (Eidg. Steuerverwaltung).
Endpoint: API_calculateSimpleTaxes — the same one the official web UI calls
(payload shape reverse-engineered from the app bundle on 2026-10-02;
Children entries are {"Age": n} objects, Relationship 1=SINGLE 2=MARRIED).

Writes scripts/fixtures/estv_parity_<year>.json — the offline test fixture for
test_tax_engine.js. Re-run each January when the new tax year is published,
then re-run the test gate.

Usage: python3 scripts/fetch_estv_fixtures.py [year] [--out FILE]
"""
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

API = ("https://swisstaxcalculator.estv.admin.ch/delegate/ost-integration/v1/"
       "lg-proxy/operation/c3b67379_ESTV")
UA = "steuerberatung.ch-parity-fixture/1.0"

# TaxLocationID of each canton capital (via API_searchLocation, 2026-10-02).
CAPITALS = {
    "ZH": 800000000, "BE": 300000000, "LU": 600000000, "UR": 646000000,
    "SZ": 643000000, "OW": 606000000, "NW": 637000000, "GL": 875000000,
    "ZG": 630000000, "FR": 170000001, "SO": 450000000, "BS": 400000000,
    "BL": 441000000, "SH": 820000000, "AR": 910000000, "AI": 905000000,
    "SG": 900000000, "GR": 700000000, "AG": 500000000, "TG": 850000000,
    "TI": 650000000, "VD": 100000000, "VS": 195000000, "NE": 200000000,
    "GE": 120000001, "JU": 290000000,
}

GRID_INCOMES = [0, 15200, 15300, 29700, 30000, 50000, 75000, 100000,
                150000, 200000, 300000, 794000, 1000000]
CHILD_INCOMES = [50000, 100000, 200000]


def call(op, body, retries=3):
    req = urllib.request.Request(
        API + "/" + op, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 "User-Agent": UA}, method="POST")
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())["response"]
        except Exception as e:  # noqa: BLE001 - transient gateway errors
            if attempt == retries - 1:
                raise RuntimeError(f"{op} failed: {e}") from e
            time.sleep(2 * (attempt + 1))


def simple(year, loc, rel, kids, income):
    return call("API_calculateSimpleTaxes", {
        "TaxYear": year, "TaxLocationID": loc, "Relationship": rel,
        "Confession1": "NONE", "Confession2": 0,
        "Children": [{"Age": a} for a in kids],
        "TaxableIncomeCanton": income, "TaxableIncomeFed": income,
        "TaxableFortune": 0,
    })


def probe_quantum(year, loc, rel):
    """100 if the canton floors taxable income to 100 CHF before the tariff
    (base(X) == base(floor100(X))), 1 if it taxes the exact income.
    Robust version: probes SEVERAL odd incomes high enough that tariffs are
    active everywhere; returns 1 if ANY odd income differs from its floor twin.
    (The old single-probe version misread BL married as 100: at low incomes
    the exact and floored curves coincidentally agree.)"""
    for x in (234567, 456789, 88888):
        b = simple(year, loc, rel, [], x)["IncomeSimpleTaxCanton"]
        b_floor = simple(year, loc, rel, [], (x // 100) * 100)["IncomeSimpleTaxCanton"]
        if b != b_floor:
            return 1
    return 100


def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2026
    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    if out is None:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "fixtures", f"estv_parity_{year}.json")

    jobs = []
    for kt, loc in CAPITALS.items():
        for inc in GRID_INCOMES:
            for rel, marr in ((1, False), (2, True)):
                jobs.append((kt, loc, rel, marr, [], inc))
        for inc in CHILD_INCOMES:
            jobs.append((kt, loc, 1, False, [10, 12], inc))   # single parent
            jobs.append((kt, loc, 2, True, [10, 12], inc))    # married

    def run(job):
        kt, loc, rel, marr, kids, inc = job
        r = simple(year, loc, rel, kids, inc)
        if not isinstance(r, dict):
            raise RuntimeError(f"unexpected ESTV response for {kt} {inc}: {r!r:.100}")
        return {
            "canton": kt, "married": marr, "children": len(kids), "taxable": inc,
            "fed": r["IncomeTaxFed"], "cantonTax": r["IncomeTaxCanton"],
            "cityTax": r["IncomeTaxCity"], "personnel": r["PersonalTax"],
            "total": r["TotalNetTax"],
        }

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=4) as ex:
        fixtures = list(ex.map(run, jobs))

    # income quantization probe (per canton x status)
    quantum = {}
    qjobs = [(kt, loc, rel) for kt, loc in CAPITALS.items() for rel in (1, 2)]
    with ThreadPoolExecutor(max_workers=4) as ex:
        qvals = list(ex.map(lambda j: probe_quantum(year, j[1], j[2]), qjobs))
    for (kt, _, rel), q in zip(qjobs, qvals):
        quantum.setdefault(kt, {})["married" if rel == 2 else "single"] = q
    os.makedirs(os.path.dirname(out), exist_ok=True)
    blob = {"year": year, "source": "ESTV API_calculateSimpleTaxes (official calculator)",
            "fetched": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "cases": fixtures,
            "quantum": quantum}
    with open(out, "w") as f:
        json.dump(blob, f, separators=(",", ":"))
    print(f"wrote {len(fixtures)} fixtures to {out} in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
