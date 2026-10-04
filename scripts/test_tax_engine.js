// test_tax_engine.js — verification gate for scripts/tax_engine.js (2026).
// Run: node scripts/test_tax_engine.js
//
// Sources of truth:
//  1. Federal: ESTV Form. 58c / DBG Art. 36 tariff 2026 (fedlex, Stand
//     1.1.2026) — every anchor row and selected mid-bracket values EXACT.
//  2. Cantonal+communal+personnel: the OFFICIAL ESTV calculator itself
//     (swisstaxcalculator.estv.admin.ch). scripts/fetch_estv_fixtures.py
//     recorded 832 parity cases (all 26 canton capitals x incomes x
//     single/married x 0/2 children) into scripts/fixtures/estv_parity_2026.json
//     and scripts/fixtures/estv_validation_2026.json (2600 off-grid cases).
//     Every case must reproduce EXACTLY (whole CHF).
//  3. Gross pipeline: ESTV detailed-mode probes (social contributions, BVG
//     default model, standard deduction chain) in scripts/fixtures/.
//
// Maintenance (every January, in this order):
//   python3 scripts/fetch_estv_fixtures.py <year>      # parity + quantum
//   python3 scripts/fetch_estv_calibration.py <year>   # divergent cells (~40min)
//   python3 scripts/build_tax_engine_data.py <year>
//   node scripts/test_tax_engine.js                    # this gate
//   then swap the Form. 58c rows below if the federal tariff changed.
"use strict";
const fs = require("fs");
const path = require("path");
const E = require("./tax_engine.js");

let fails = 0, passes = 0;
function check(name, got, want, tol) {
  const ok = Math.abs(got - want) <= (tol === undefined ? 0.005 : tol);
  if (ok) passes++;
  else { fails++; console.log(`FAIL ${name}: got ${got}, want ${want}`); }
}

// ---- 1. Federal anchors, single (Form. 58c 2026) ---------------------------
const FS = [
  [15200, 0], [18500, 25.41], [19000, 29.26], [20000, 36.96], [30000, 113.96],
  [33200, 138.60], [33100, 137.83], [34000, 145.64], [43400, 228.36], [43500, 229.20],
  [45000, 268.80], [50000, 400.80], [57900, 609.36], [58000, 612.00], [60000, 671.40],
  [61200, 707.04], [61300, 710.01], [65000, 819.90], [70000, 968.40], [76100, 1149.57],
  [76200, 1152.50], [77500, 1229.72], [79000, 1318.82], [79100, 1324.76], [82000, 1497.02],
  [82100, 1502.95], [90000, 2024.35], [100000, 2684.35], [108600, 3251.95], [108700, 3258.55],
  [108900, 3271.75], [110000, 3368.55], [120500, 4292.55], [120600, 4301.35], [125000, 4688.55],
  [130400, 5163.75], [130500, 5172.55], [138300, 5858.95], [138400, 5867.75], [141400, 6131.75],
  [141500, 6140.55], [144200, 6437.55], [144300, 6448.55], [148200, 6877.55], [148300, 6888.55],
  [150300, 7108.55], [150400, 7119.55], [151000, 7185.55], [152300, 7328.55], [152400, 7339.55],
  [155000, 7625.55], [160000, 8175.55], [170000, 9275.55], [185000, 10925.55], [185100, 10936.55],
  [186000, 11055.35], [190000, 11583.35], [200000, 12903.35], [250000, 19503.35], [300000, 26103.35],
  [350000, 32703.35], [400000, 39303.35], [500000, 52503.35], [650000, 72303.35], [700000, 78903.35],
  [793800, 91284.95], [793900, 91298.15], [800000, 92000.00], [941200, 108238.00], [941300, 108249.50],
  [950000, 109250.00]
];
for (const [inc, want] of FS) check(`fed single ${inc}`, E.fedTaxRaw(inc, false, 0), want, 0.005);

// ---- 2. Federal anchors, married -------------------------------------------
const FM = [
  [29700, 0], [33000, 33.00], [33200, 35.00], [53300, 236.00], [53400, 237.00],
  [61200, 393.00], [61300, 395.00], [79000, 926.00], [79100, 929.00], [94800, 1557.00],
  [94900, 1561.00], [108600, 2246.00], [108700, 2251.00], [108800, 2257.00], [108900, 2263.00],
  [110000, 2329.00], [115000, 2629.00], [120500, 2959.00], [120600, 2965.00], [125000, 3273.00],
  [130400, 3651.00], [130500, 3658.00], [135000, 4018.00], [138300, 4282.00], [138400, 4290.00],
  [141400, 4560.00], [141500, 4569.00], [144200, 4812.00], [144300, 4821.00], [148200, 5211.00],
  [148300, 5221.00], [150300, 5441.00], [150400, 5452.00], [151000, 5524.00], [152300, 5680.00],
  [152400, 5692.00], [155000, 6030.00], [160000, 6680.00], [170000, 7980.00], [185000, 9930.00],
  [185100, 9943.00], [186000, 10060.00], [190000, 10580.00], [200000, 11880.00], [250000, 18380.00],
  [300000, 24880.00], [350000, 31380.00], [400000, 37880.00], [500000, 50880.00], [650000, 70380.00],
  [700000, 76880.00], [793800, 89074.00], [793900, 89087.00], [800000, 89880.00], [941200, 108236.00],
  [941300, 108249.00], [950000, 109250.00]
];
for (const [inc, want] of FM) check(`fed married ${inc}`, E.fedTaxRaw(inc, true, 0), want, 0.005);

// ---- 3. Zero band + minimum + child credit ---------------------------------
check("fed single 15000", E.fedTax(15000, false, 0), 0);
check("fed single 15199", E.fedTax(15199, false, 0), 0);
check("fed married 29699", E.fedTax(29699, true, 0), 0);
check("fed <25 not raised", E.fedTax(16000, false, 0), 0);           // 6.16 < 25
check("fed min AFTER credit", E.fedTax(66400, true, 2), 0);           // 548-526=22 < 25
check("fed credit boundary", E.fedTax(66500, true, 2), 25);           // 551-526=25
check("single-parent credit", E.fedTax(70173, false, 2), 133);        // family tariff + credit
check("single-parent credit 2", E.fedTax(100000, false, 2), 1290);
const noKid = E.fedTax(100000, true, 0);
check("child credit 2x263", E.fedTax(100000, true, 2), noKid - 526, 1);

// ---- 4. ESTV parity fixtures (THE gate: exact match to the official tool) ---
function loadFix(name) {
  const p = path.join(__dirname, "fixtures", name);
  return JSON.parse(fs.readFileSync(p, "utf8"));
}
function parityRun(fixName, tolerance) {
  const fix = loadFix(fixName);
  let bad = 0;
  for (const c of fix.cases) {
    const r = E.calcSimple({ canton: c.canton, taxable: c.taxable,
                             married: c.married, children: c.children });
    const fields = [
      ["fed", r.federal, c.fed], ["cant", r.cantonTax, c.cantonTax],
      ["city", r.cityTax, c.cityTax], ["pers", r.personnelTax, c.personnel],
      ["total", r.total, c.total]
    ];
    for (const [fld, got, want] of fields) {
      if (Math.abs(got - want) > tolerance) {
        bad++;
        if (bad <= 10) console.log(`FAIL ${fixName} ${c.canton} ${c.married ? "m" : "s"} k${c.children} ${c.taxable} ${fld}: got ${got}, want ${want}`);
      } else passes++;
    }
  }
  if (bad > 10) console.log(`  ... ${bad - 10} more failures in ${fixName}`);
  fails += bad;
  return { total: fix.cases.length, bad };
}
const p1 = parityRun("estv_parity_2026.json", 0);
const p2 = parityRun("estv_validation_2026.json", 0);
console.log(`parity: ${p1.total} fixture cases + ${p2.total} validation cases`);

// ---- 4b. Bagatellgrenze cells (TG 30 / SG 20 — probed from live ESTV) --------
const BAG = [
  ["TG", 13000, 0, 0, 0, 0, 0], ["TG", 13600, 0, 0, 0, 0, 0],
  ["TG", 13700, 0, 33, 43, 0, 0], ["TG", 0, 20000, 0, 0, 0, 0],
  ["TG", 0, 25000, 0, 0, 0, 0], ["TG", 0, 26000, 0, 0, 0, 0],
  ["TG", 0, 27000, 0, 0, 32, 42], ["TG", 0, 30000, 0, 0, 36, 47],
  ["TG", 13000, 10000, 0, 0, 0, 0], ["TG", 13000, 20000, 17, 23, 24, 31],
  ["TG", 13000, 50000, 17, 23, 60, 78], ["TG", 100000, 0, 6271, 8169, 0, 0],
  ["SG", 11000, 0, 0, 0, 0, 0], ["SG", 12000, 0, 0, 0, 0, 0],
  ["SG", 13000, 0, 59, 77, 0, 0], ["SG", 0, 10000, 0, 0, 0, 0],
  ["SG", 0, 11000, 0, 0, 0, 0], ["SG", 0, 12000, 0, 0, 21, 28],
  ["SG", 0, 15000, 0, 0, 27, 35], ["SG", 11000, 10000, 0, 0, 0, 0],
  ["SG", 12000, 10000, 17, 22, 18, 23], ["SG", 12000, 11000, 17, 22, 20, 26],
  ["SG", 12000, 12000, 17, 22, 21, 28], ["SG", 13000, 10000, 59, 77, 18, 23],
  ["SG", 13000, 20000, 59, 77, 36, 47]
];
for (const [kt, inc, fort, wC, wCity, wFC, wFCity] of BAG) {
  const x = E.calcSimple({ canton: kt, taxable: inc, married: false,
                           children: 0, fortune: fort });
  check(`bag ${kt} ${inc}+${fort} cant`, x.cantonTax, wC, 0);
  check(`bag ${kt} ${inc}+${fort} city`, x.cityTax, wCity, 0);
  check(`bag ${kt} ${inc}+${fort} fortC`, x.fortuneCantonTax, wFC, 0);
  check(`bag ${kt} ${inc}+${fort} fortCity`, x.fortuneCityTax, wFCity, 0);
}

// ---- 5. Monotonicity + ordering sanity --------------------------------------
let prev = -1;
for (let inc = 0; inc <= 1000000; inc += 1000) {
  const t = E.fedTax(inc, false, 0);
  if (t < prev) { fails++; console.log(`FAIL monotonic fed at ${inc}`); break; }
  prev = t;
  passes++;
}
for (const kt of Object.keys(E.DATA.factors)) {
  let pc = -1;
  for (let inc = 0; inc <= 400000; inc += 20000) {
    const r = E.calcSimple({ canton: kt, taxable: inc, married: false, children: 0 });
    if (r.total < pc) { fails++; console.log(`FAIL monotonic total ${kt} at ${inc}`); break; }
    pc = r.total;
    passes++;
  }
}
const zg = E.calcSimple({ canton: "ZG", taxable: 100000, married: false, children: 0 });
const ge = E.calcSimple({ canton: "GE", taxable: 100000, married: false, children: 0 });
if (zg.total >= ge.total) { fails++; console.log("FAIL ZG should be cheaper than GE"); } else passes++;

// ---- 6. Gross pipeline (ESTV detailed-mode probes, recorded 2026-10-02) ------
// social contributions at gross 100k age 35: AHV 5300, ALV 1100, NBU 400, BVG 3538
const s100 = E.socialContributions(100000, 35);
check("gross100k ahv", s100.ahv, 5300, 0);
check("gross100k alv", s100.alv, 1100, 0);
check("gross100k nbu", s100.nbu, 400, 0);
check("gross100k bvg", s100.bvg, 3538, 0);
check("gross100k net", s100.net, 89662, 0);
// ALV/NBU cap at 148200
const s200 = E.socialContributions(200000, 35);
check("gross200k ahv", s200.ahv, 10600, 0);
check("gross200k alv", s200.alv, 1630, 0);
check("gross200k bvg", s200.bvg, 7038, 0);
// BVG age bands + entry threshold (probed)
check("bvg age22 under entry", E.bvgDefault(22680, 22), 0, 0);
check("bvg age25 entry", E.bvgDefault(23000, 25), 132, 0);
check("bvg age35 band", E.bvgDefault(100000, 35), 3538, 0);
check("bvg age45 band", E.bvgDefault(100000, 45), 5144, 0);
check("bvg age55 band", E.bvgDefault(100000, 55), 6108, 0);
check("bvg excess 3.5pct", E.bvgDefault(160000, 35), 5638, 0);
// full gross pipeline ZH single 100k age35 (ESTV detailed: fed 1701, cant 4494, city 5629, pers 24, total 11848)
const g1 = E.calcGross({ canton: "ZH", gross: 100000, married: false, children: 0, age: 35 });
check("gross ZH s100k taxFed", g1.taxableFed, 85173, 0);
check("gross ZH s100k taxCant", g1.taxableCanton, 84073, 0);
check("gross ZH s100k fed", g1.federal, 1701, 0);
check("gross ZH s100k cant", g1.cantonTax, 4494, 0);
check("gross ZH s100k city", g1.cityTax, 5629, 0);
check("gross ZH s100k pers", g1.personnelTax, 24, 0);
check("gross ZH s100k total", g1.total, 11848, 0);
// married 50k+50k 2 kids (ESTV detailed 2026-10-02: taxFed 51246, taxCant 53446,
// fed 0 [credit 526 > raw tax], cant 1473, city 1846, pers 48, total 3367)
const g2 = E.calcGross({ canton: "ZH", married: true, children: 2,
  persons: [{ gross: 50000, age: 35 }, { gross: 50000, age: 35 }] });
check("gross ZH m50+50k2 taxFed", g2.taxableFed, 51246, 0);
check("gross ZH m50+50k2 taxCant", g2.taxableCanton, 53446, 0);
check("gross ZH m50+50k2 fed", g2.federal, 0, 0);
check("gross ZH m50+50k2 cant", g2.cantonTax, 1473, 0);
check("gross ZH m50+50k2 city", g2.cityTax, 1846, 0);
check("gross ZH m50+50k2 pers", g2.personnelTax, 48, 0);
check("gross ZH m50+50k2 total", g2.total, 3367, 0);
// married 50k+50k 0 kids (ESTV detailed: taxFed 66246, taxCant 74846,
// fed 542, cant 2795, city 3501, pers 48, total 6886)
const g2b = E.calcGross({ canton: "ZH", married: true, children: 0,
  persons: [{ gross: 50000, age: 35 }, { gross: 50000, age: 35 }] });
check("gross ZH m50+50k0 taxFed", g2b.taxableFed, 66246, 0);
check("gross ZH m50+50k0 taxCant", g2b.taxableCanton, 74846, 0);
check("gross ZH m50+50k0 fed", g2b.federal, 542, 0);
check("gross ZH m50+50k0 cant", g2b.cantonTax, 2795, 0);
check("gross ZH m50+50k0 city", g2b.cityTax, 3501, 0);
check("gross ZH m50+50k0 total", g2b.total, 6886, 0);
// single parent 100k 2 kids (ESTV: fed 133, cant 1998, city 2503, total 4658)
const g3 = E.calcGross({ canton: "ZH", gross: 100000, married: false, children: 2, age: 35 });
check("gross ZH sp100k2 taxFed", g3.taxableFed, 70173, 0);
check("gross ZH sp100k2 taxCant", g3.taxableCanton, 62673, 0);
check("gross ZH sp100k2 fed", g3.federal, 133, 0);
check("gross ZH sp100k2 cant", g3.cantonTax, 1998, 0);
check("gross ZH sp100k2 city", g3.cityTax, 2503, 0);
check("gross ZH sp100k2 total", g3.total, 4658, 0);

console.log(`\n${passes} passed, ${fails} failed`);
process.exit(fails ? 1 : 0);
