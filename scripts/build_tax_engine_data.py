#!/usr/bin/env python3
"""build_tax_engine_data.py — compile ESTV raw exports into the engine data blob.

Reads  scripts/fixtures/estv_raw_{tarifs,factors,deductions,personnel}_<year>.json
(written by fetch_estv_fixtures.py from the official ESTV Swiss Tax Calculator API)
and emits  scripts/tax_engine_data.js  +  assets/tax_engine_data.js (identical).

The blob drives scripts/tax_engine.js v3, a faithful port of the calculation
semantics of the official ESTV calculator (swisstaxcalculator.estv.admin.ch):
tarif tables (BUND/ZUERICH/FLATTAX/FREIBURG/FORMEL incl. splitting), canton-
capital Steuerfuss factors, income deduction tables (federal + cantonal) and
personnel taxes. Source of the semantics: ESTV API responses + the MIT-licensed
reference implementation github.com/devbrains-com/swisstaxcalculator.

Usage: python3 scripts/build_tax_engine_data.py [year]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")

TABLE_TYPES = {"BUND": 0, "ZUERICH": 1, "FLATTAX": 2, "FREIBURG": 3, "FORMEL": 4}
DED_FORMATS = {"MAXIMUM": 0, "PERCENT": 1, "PERCENT,MINIMUM,MAXIMUM": 2,
               "STANDARDIZED": 3, "PERCENT,MAXIMUM": 4}


def load(name, year):
    path = os.path.join(FIX, f"{name}_{year}.json")
    with open(path) as f:
        return json.load(f)["response"]


def build_tarifs(raw):
    """Income + wealth tarif tables per canton ('CH' = federal BUND target).
    Each table is tagged with its ESTV target: 'k' = KANTON (cantonal simple
    tax), 'g' = GEMEINDE (a separate communal table used by SZ and VS)."""
    out = {}
    for r in raw:
        if r["TaxType"] not in ("EINKOMMENSSTEUER", "VERMOEGENSSTEUER"):
            continue
        if r["Target"] == "BUND":
            kt, target = "CH", "k"
        elif r["Target"] == "KANTON":
            kt, target = r["Location"]["Canton"], "k"
        elif r["Target"] == "GEMEINDE":
            kt, target = r["Location"]["Canton"], "g"
        else:
            continue
        rows = []
        for row in r["Table"]:
            formula = row.get("Formula", "") or ""
            rows.append([row["Amount"], row["Percent"], row["Taxes"],
                         formula if formula else None])
        out.setdefault(kt, []).append({
            "ty": 0 if r["TaxType"] == "EINKOMMENSSTEUER" else 1,
            "g": r["Group"], "s": r["Splitting"], "t": target,
            "tt": TABLE_TYPES[r["TableType"]] if r["TableType"] in TABLE_TYPES else 0,
            "r": rows,
        })
    return out


def build_factors(raw, capitals, overrides):
    """Steuerfuss of each canton capital: [incomeCanton, incomeCity,
    fortuneCanton, fortuneCity] in percent of the simple cantonal tax.
    `overrides` (oracle-calibrated) replace the bulk-export value where the live
    ESTV calculator applies a different factor (e.g. GE/VD cantonal coefficients)."""
    out = {}
    for f in raw:
        kt = f["Location"]["Canton"]
        if kt not in capitals or f["Location"]["BfsID"] != capitals[kt]:
            continue
        vals = [f["IncomeRateCanton"], f["IncomeRateCity"],
                f["FortuneRateCanton"], f["FortuneRateCity"]]
        ov = overrides.get(kt, {})
        for key, idx in (("incomeCanton", 0), ("incomeCity", 1),
                         ("fortuneCanton", 2), ("fortuneCity", 3)):
            if key in ov:
                vals[idx] = ov[key]
        out[kt] = vals
    missing = set(capitals) - set(out)
    if missing:
        raise SystemExit(f"factors missing for capitals: {sorted(missing)}")
    return out


def build_deductions(raw):
    """Income-tax deduction tables: 'CH' = federal, canton keys = cantonal.
    Item: [formatCode, percent, minimum, maximum, amount]."""
    out = {}
    for r in raw:
        if r["TaxType"] != "EINKOMMENSSTEUER":
            continue
        if r["Target"] == "BUND":
            kt = "CH"
        elif r["Target"] == "KANTON":
            kt = r["Location"]["Canton"]
        else:
            continue
        if kt in out:  # BUND table repeats per canton in the raw export
            continue
        items = {}
        for it in r["Table"]:
            fmt = it["Format"]
            if fmt not in DED_FORMATS:
                continue
            items[it["Name"]["ID"]] = [DED_FORMATS[fmt], it["Percent"],
                                       it["Minimum"], it["Maximum"], it["Amount"]]
        out[kt] = items
    return out


def compact_calibration(cells):
    """Raw fetcher rows [[inc, baseC, baseM, taxC, taxCity, credit], ...] ->
    columnar layout {incs: [...], k: {nk: [baseC[], baseM[], taxC[], taxCity[],
    credit[]]}} — same data, ~40% smaller in the generated blob."""
    out = {}
    for kt, groups in cells.items():
        out[kt] = {}
        for group, kids in groups.items():
            ks = sorted(kids.keys(), key=int)
            incs = [row[0] for row in kids[ks[0]]]
            for k in ks:
                if [row[0] for row in kids[k]] != incs:
                    raise SystemExit(f"calibration grid mismatch: {kt} {group} k={k}")
            cell = {"incs": incs, "k": {}}
            for k in ks:
                rows = kids[k]
                cell["k"][k] = [[r[i] for r in rows] for i in range(1, 6)]
            out[kt][group] = cell
    return out


def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
    pers_path = os.path.join(FIX, f"estv_personnel_{year}.json")
    with open(pers_path) as f:
        pers_blob = json.load(f)
    capitals = pers_blob["capitalBfs"]

    ov_path = os.path.join(FIX, f"estv_factor_overrides_{year}.json")
    overrides = json.load(open(ov_path)) if os.path.exists(ov_path) else {}

    cal_path = os.path.join(FIX, f"estv_calibration_{year}.json")
    calibration, child_effects = {}, {}
    if os.path.exists(cal_path):
        cal_blob = json.load(open(cal_path))
        calibration = compact_calibration(cal_blob["cells"])
        child_effects = cal_blob.get("childEffects", {})

    cc_path = os.path.join(FIX, f"estv_child_credits_{year}.json")
    child_credits = json.load(open(cc_path))["credits"] if os.path.exists(cc_path) else {}
    # normalize sign: fetcher stores the raw TaxCredit delta (negative);
    # the engine treats childCredits as positive per-child magnitudes.
    child_credits = {kt: abs(v) for kt, v in child_credits.items()}

    # income quantization probed from the live calculator (100 = floor taxable
    # income to 100 CHF before the tariff; 1 = tax the exact income). Source:
    # fetch_estv_fixtures.py writes it into the parity fixture blob.
    par_path = os.path.join(FIX, f"estv_parity_{year}.json")
    quantum = json.load(open(par_path)).get("quantum", {}) if os.path.exists(par_path) else {}

    blob = {
        "year": year,
        "source": "ESTV swisstaxcalculator API export (tarifs/factors/deductions) "
                  "+ official-calculator probes (personnel, child credit, factor overrides) "
                  "+ oracle-calibrated bases (fetch_estv_calibration.py)",
        "fedChildCredit": pers_blob["fedChildCredit"],
        "tarifs": build_tarifs(load("estv_raw_tarifs", year)),
        "factors": build_factors(load("estv_raw_factors", year), capitals, overrides),
        "deductions": build_deductions(load("estv_raw_deductions", year)),
        "personnel": pers_blob["personnel"],
        "social": pers_blob["social"],
        "calibration": calibration,
        "childEffects": child_effects,
        "childCredits": child_credits,
        # Bagatellgrenze: when the COMBINED simple tax (income + fortune) is
        # below the threshold, no canton/city tax is levied at all. Probed
        # 2026-10-02 across all 26 cantons (income, fortune, and mixed cells):
        #   TG 30 (simple 29 waived / 30 levied), SG 20 (simple 19 waived / 20
        #   levied). Mixed proof: TG inc13k+fort20k (16+22=38) levies BOTH;
        #   SG inc12k+fort10k (16+17=33) levies BOTH; below-threshold combos
        #   waive everything.
        "bagatelle": {"TG": 30, "SG": 20},
        "quantum": quantum,
    }
    data = json.dumps(blob, separators=(",", ":"), sort_keys=True)
    body = (
        "/* tax_engine_data.js — GENERATED FILE, do not edit.\n"
        f" * Swiss tax data {year}, compiled from official ESTV exports by\n"
        " * scripts/build_tax_engine_data.py. Keep scripts/ and assets/ copies identical.\n"
        " * tarif row: [amount, percent, taxes, formula|null]; tableType codes:\n"
        " * 0=BUND 1=ZUERICH 2=FLATTAX 3=FREIBURG 4=FORMEL; ty: 0=income 1=wealth.\n"
        " * factors: [incomeCanton%, incomeCity%, fortuneCanton%, fortuneCity%].\n"
        " * deductions item: [formatCode, percent, minimum, maximum, amount]; formats:\n"
        " * 0=MAXIMUM 1=PERCENT 2=PERCENT,MINIMUM,MAXIMUM 3=STANDARDIZED 4=PERCENT,MAXIMUM.\n"
        " */\n"
        "(function (g) {\n"
        "  \"use strict\";\n"
        f"  var DATA = {data};\n"
        "  if (typeof module !== \"undefined\" && module.exports) module.exports = DATA;\n"
        "  else g.TAX_ENGINE_DATA = DATA;\n"
        "})(typeof window !== \"undefined\" ? window : globalThis);\n"
    )
    for rel in ("scripts/tax_engine_data.js", "assets/tax_engine_data.js"):
        path = os.path.join(HERE, "..", rel)
        with open(path, "w") as f:
            f.write(body)
        print(f"wrote {os.path.normpath(path)} ({len(body)} bytes)")


if __name__ == "__main__":
    main()
