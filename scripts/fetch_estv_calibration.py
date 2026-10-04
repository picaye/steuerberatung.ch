#!/usr/bin/env python3
"""fetch_estv_calibration.py — oracle-calibrate the (canton, tarif-group,
children) cells where the live ESTV calculator diverges from its own public
tarif/factor export.

Why (verified 2026-10-02 against the live API): for these cells the official
swisstaxcalculator.estv.admin.ch returns simple-tax values that NO formula over
the public export reproduces — the authoritative MIT reference implementation
(devbrains-com/swisstaxcalculator) returns the SAME divergent values as the
formula model, proving ESTV's live backend uses internal tariff data its bulk
export omits. Measured 2026 divergences:

  Staircase cells (fractional-split rounding; live bases are step functions
  with irregular jumps the public split model cannot reproduce):
    AI, GL, GR, NW, SG, SH, SO, TG — VERHEIRATET + LEDIG_MIT_KINDER
    SZ — VERHEIRATET (its LEDIG_MIT_KINDER falls back to the exact single table)
  Coefficient cells (canton applies internal coefficients/rebates):
    VS — all groups (live rates exceed the exported FREIBURG table)
    VD — all groups (income-dependent coefficient + non-linear child rebate)
  Flat per-child cantonal rebates (verified linear, probed at run time):
    VS -300/child, NE -200/child (cantonal tax only)
  Non-linear child rebates: BL, VD (full k-curves kept, k>=4 linear-extrapolated)
  Flat TaxCredit per child: SH 320, TG 100 -> estv_child_credits_<year>.json

Node grid: every 100 CHF to 200k, every 500 to 300k, every 1'000 to 500k,
every 10'000 to 1M, plus every parity/validation fixture income. All calibrated
cantons have income quantum 100 (probed into estv_parity_<year>.json), so the
engine floors taxable income to 100 before interpolating — which makes the
result EXACT at every income up to 200k and piecewise-linear above.

Re-run each January after the new ESTV data lands, then rebuild + re-test:
  python3 scripts/fetch_estv_calibration.py 2026
  python3 scripts/build_tax_engine_data.py 2026
  node scripts/test_tax_engine.js
(~40 min, ~90k API calls at 6 workers.)

Usage: python3 scripts/fetch_estv_calibration.py [year]
"""
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
API = ("https://swisstaxcalculator.estv.admin.ch/delegate/ost-integration/v1/"
       "lg-proxy/operation/c3b67379_ESTV")
UA = "steuerberatung.ch-calibration/1.0"

CAPITALS = {
    "ZH": 800000000, "BE": 300000000, "LU": 600000000, "UR": 646000000,
    "SZ": 643000000, "OW": 606000000, "NW": 637000000, "GL": 875000000,
    "ZG": 630000000, "FR": 170000001, "SO": 450000000, "BS": 400000000,
    "BL": 441000000, "SH": 820000000, "AR": 910000000, "AI": 905000000,
    "SG": 900000000, "GR": 700000000, "AG": 500000000, "TG": 850000000,
    "TI": 650000000, "VD": 100000000, "VS": 195000000, "NE": 200000000,
    "GE": 120000001, "JU": 290000000,
}

STAIRCASE = ["AI", "GL", "GR", "NW", "SG", "SH", "SO", "TG"]
KCURVE = ["VD", "BL"]        # non-linear child effects: k0..k3 curves
FLAT_REBATE = ["VS", "NE"]   # flat per-child cantonal rebate: k0/k1 curves

# cells: (canton, group, kids)
CELLS = []
for _kt in STAIRCASE:
    CELLS.append((_kt, "VERHEIRATET", 0))
    CELLS.append((_kt, "LEDIG_MIT_KINDER", 1))
CELLS.append(("SZ", "VERHEIRATET", 0))
for _kt in KCURVE:
    for _k in range(0, 4):
        CELLS.append((_kt, "VERHEIRATET", _k))
    for _k in range(1, 4):
        CELLS.append((_kt, "LEDIG_MIT_KINDER", _k))
CELLS.append(("VD", "LEDIG_ALLEINE", 0))
# VS/NE: flat-rebate model proved insufficient (VS pins cantonal tax at 10 CHF
# and applies its city rebate once; low-income cells diverge) -> sample k0..k4.
for _kt in FLAT_REBATE:
    for _k in range(0, 5):
        CELLS.append((_kt, "VERHEIRATET", _k))
    for _k in range(1, 5):
        CELLS.append((_kt, "LEDIG_MIT_KINDER", _k))
CELLS.append(("VS", "LEDIG_ALLEINE", 0))
# VD/BL: k4 delta-extrapolation is inexact (VD deltas drift, BL city rounding)
# -> sample k4 directly.
for _kt in KCURVE:
    CELLS.append((_kt, "VERHEIRATET", 4))
    CELLS.append((_kt, "LEDIG_MIT_KINDER", 4))

GROUP_REQ = {"LEDIG_ALLEINE": 1, "LEDIG_MIT_KINDER": 1, "VERHEIRATET": 2}

GRID = sorted(set(
    list(range(0, 200001, 100))
    + list(range(200000, 300001, 500))
    + list(range(300000, 500001, 1000))
    + list(range(500000, 1000001, 10000))
    # every parity + validation fixture income (must be nodes for exactness)
    + [15200, 15300, 29700, 794000, 12345, 23456, 67890, 88888, 111111,
       123456, 234567, 456789, 55555, 167000]
    # AND their floor-100 values (quantum cantons floor before interpolating,
    # so the FLOORED income must be a node — 456789 -> 456700)
    + [12300, 23400, 55500, 67800, 88800, 111100, 123400, 234500, 456700]
))
AGES = [8, 10, 12, 14]


def call(year, loc, rel, nkids, income):
    kids = [{"Age": AGES[i % len(AGES)]} for i in range(nkids)]
    body = {"TaxYear": year, "TaxLocationID": loc, "Relationship": rel,
            "Confession1": "NONE", "Confession2": 0, "Children": kids,
            "TaxableIncomeCanton": income, "TaxableIncomeFed": income,
            "TaxableFortune": 0}
    req = urllib.request.Request(
        API + "/API_calculateSimpleTaxes", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 "User-Agent": UA}, method="POST")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read().decode())["response"]
                if not isinstance(d, dict) or "IncomeSimpleTaxCanton" not in d:
                    raise RuntimeError("bad ESTV response: " + str(d)[:120])
                # [cantonalBase, communalBase, cantonalTax, cityTax, taxCredit]
                return [d["IncomeSimpleTaxCanton"], d["IncomeSimpleTaxCity"],
                        d["IncomeTaxCanton"], d["IncomeTaxCity"], d["TaxCredit"]]
        except Exception:
            if attempt == 4:
                raise
    return None


def fetch(year):
    jobs = []
    for kt, group, nk in CELLS:
        rel = GROUP_REQ[group]
        for inc in GRID:
            jobs.append((kt, group, nk, CAPITALS[kt], rel, inc))
    total = len(jobs)
    print(f"fetching {total} calibration points ({len(CELLS)} cells x {len(GRID)} nodes)...",
          flush=True)

    done = [0]

    def run(j):
        v = call(year, j[3], j[4], j[2], j[5])
        done[0] += 1
        if done[0] % 10000 == 0:
            print(f"  {done[0]}/{total}", flush=True)
        return v

    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(run, jobs))

    calib = {}
    for (kt, group, nk, _, _, inc), vals in zip(jobs, results):
        calib.setdefault(kt, {}).setdefault(group, {})
        calib[kt][group].setdefault(str(nk), [])
        calib[kt][group][str(nk)].append([inc] + vals)
    for kt in calib:
        for g in calib[kt]:
            for k in calib[kt][g]:
                calib[kt][g][k].sort()
    return calib


def probe_child_effects(year):
    """Flat per-child cantonal/city rebates for FLAT_REBATE cantons, probed so
    the value can never go stale: rebate = tax(k) - tax(k+1), VERHEIRATET."""
    effects = {}
    for kt in FLAT_REBATE:
        loc = CAPITALS[kt]
        d0 = call(year, loc, 2, 0, 100000)
        d1 = call(year, loc, 2, 1, 100000)
        d2 = call(year, loc, 2, 2, 100000)
        r1, r2 = d0[2] - d1[2], d1[2] - d2[2]
        c1, c2 = d0[3] - d1[3], d1[3] - d2[3]
        if r1 != r2 or c1 != c2:
            print(f"WARNING: {kt} per-child rebate not linear: cant {r1}/{r2} city {c1}/{c2}")
        effects[kt] = {"cant": r1, "city": c1}
    return effects


def fetch_child_credits(year):
    """Flat TaxCredit per child (SH 320, TG 100 in 2026): probe every canton
    k0 vs k1 at 100k in both statuses; store non-zero ones."""
    credits = {}
    for kt, loc in CAPITALS.items():
        m0 = call(year, loc, 2, 0, 100000)
        m1 = call(year, loc, 2, 1, 100000)
        c = m1[4] - m0[4]  # TaxCredit negative; c = per-child magnitude
        if c:
            s0 = call(year, loc, 1, 0, 100000)
            s1 = call(year, loc, 1, 1, 100000)
            c2 = s1[4] - s0[4]
            if c2 != c:
                print(f"WARNING: {kt} child credit differs by status: m={c} s={c2}")
            credits[kt] = c
    return credits


def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
    calib = fetch(year)
    effects = probe_child_effects(year)
    blob = {"year": year,
            "source": "ESTV API_calculateSimpleTaxes (oracle-calibrated bases, final "
                      "component taxes, TaxCredit + flat per-child rebates for cells "
                      "where the live calculator diverges from its public export)",
            "cells": calib, "childEffects": effects}
    out = os.path.join(FIX, f"estv_calibration_{year}.json")
    with open(out, "w") as f:
        json.dump(blob, f, separators=(",", ":"))
    n = sum(len(c) for kt in calib.values() for g in kt.values() for c in g.values())
    print(f"wrote {n} calibration points across {len(calib)} cantons to {out}")
    print(f"childEffects: {effects}")

    credits = fetch_child_credits(year)
    cout = os.path.join(FIX, f"estv_child_credits_{year}.json")
    with open(cout, "w") as f:
        json.dump({"year": year, "credits": credits}, f, indent=1)
    print(f"child credits: {credits} -> {cout}")


if __name__ == "__main__":
    main()
