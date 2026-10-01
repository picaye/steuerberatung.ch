// test_tax_engine.js — verification gate for scripts/tax_engine.js (2026).
// Run: node scripts/test_tax_engine.js
// Sources of truth:
//  - Federal: ESTV Form. 58c / DBG Art. 36 tariff 2026 (fedlex, Stand 1.1.2026).
//    Every anchor row and selected mid-bracket values must match EXACTLY.
//  - Cantonal+communal: taxbooks.ch "Einkommenssteuerbelastung in den Kantonen"
//    1.1/2026 (canton capitals, excl. church tax, combined incl. federal).
//    At the three anchors (75k/150k/300k) the engine must reproduce the table
//    within 0.05 percentage points.
"use strict";
const E = require("./tax_engine.js");

let fails = 0, passes = 0;
function check(name, got, want, tol) {
  const ok = Math.abs(got - want) <= (tol === undefined ? 0.005 : tol);
  if (ok) passes++;
  else { fails++; console.log(`FAIL ${name}: got ${got}, want ${want}`); }
}

// ---- 1. Federal anchors, single (Form. 58c 2026) -------------------------
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
for (const [inc, want] of FS) check(`fed single ${inc}`, E.fedTax(inc, false), want, 0.005);

// ---- 2. Federal anchors, married -----------------------------------------
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
for (const [inc, want] of FM) check(`fed married ${inc}`, E.fedTax(inc, true), want, 0.005);

// ---- 3. Zero band + minimum ----------------------------------------------
check("fed single 15000", E.fedTax(15000, false), 0);
check("fed single 15199", E.fedTax(15199, false), 0);
check("fed married 29699", E.fedTax(29699, true), 0);
check("fed <25 not raised", E.fedTax(16000, false), 0); // 6.16 < 25

// ---- 4. Cantonal table reproduction at anchors (all 26 cantons) ----------
// estimate() with deductions=0 and taxable at the anchor must reproduce the
// published COMBINED effective % (incl. federal) within 0.05pp.
const TB = E.CANTONS;
for (const [kt, rows] of Object.entries(TB)) {
  for (let a = 0; a < 3; a++) {
    const inc = [75000, 150000, 300000][a];
    for (const m of [false, true]) {
      const r = E.estimate({ gross: inc, canton: kt, married: m, children: 0, hasPension: true, deductions: 0 });
      const gotPct = (r.total / inc) * 100;
      const wantPct = rows[a][m ? 1 : 0];
      check(`${kt} ${m ? "married" : "single"} @${inc}`, gotPct, wantPct, 0.05);
    }
  }
}

// ---- 5. Monotonicity + ordering sanity -----------------------------------
let prev = -1;
for (let inc = 0; inc <= 1000000; inc += 1000) {
  const t = E.fedTax(inc, false);
  if (t < prev) { fails++; console.log(`FAIL monotonic fed at ${inc}`); break; }
  prev = t;
}
const zg = E.estimate({ gross: 100000, canton: "ZG", deductions: 0 });
const ge = E.estimate({ gross: 100000, canton: "GE", deductions: 0 });
if (zg.total >= ge.total) { fails++; console.log("FAIL ZG should be cheaper than GE"); } else passes++;

// ---- 6. Child credit (Art. 36 Abs. 2bis): married, 2 children ------------
const noKid = E.fedTax(100000, true);
const r2 = E.estimate({ gross: 100000, canton: "ZH", married: true, children: 2, deductions: 0 });
check("child credit 2x263", r2.federal, Math.round(noKid - 526), 1);

console.log(`\n${passes} passed, ${fails} failed`);
process.exit(fails ? 1 : 0);
