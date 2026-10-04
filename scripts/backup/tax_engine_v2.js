// tax_engine.js — steuerberatung.ch tax calculation engine (2026).
// Federal part: exact DBG Art. 36 tariff 2026 (SR 642.11, fedlex, Stand 1.1.2026),
// piecewise linear per CHF 100 bracket. Cantonal+communal part: published
// effective combined rates at canton capitals excl. church tax
// (taxbooks.ch "Einkommenssteuerbelastung in den Kantonen", Version 1.1/2026,
// based on Dr.Tax; cross-checked vs KPMG Clarity on Swiss Taxes 2026 marginals).
// Methodology note: cantonal/communal effective rate is interpolated on the
// cantonal share (anchor minus exact federal at that anchor) and applied to the
// same taxable income as the federal tax — the same simplification the source
// table states. Estimates are for the canton CAPITAL unless a municipality
// multiplier is given.
(function (global) {
  "use strict";

  // ---- Federal tariff 2026 (DBG Art. 36) --------------------------------
  // anchors: [income, tax, per100 for the NEXT bracket]
  var FED_SINGLE = [
    [0, 0, 0],             // bis 15'200 Franken Einkommen: 0.00
    [15200, 0, 0.77],
    [33200, 138.60, 0.88],
    [43500, 229.20, 2.64],
    [58000, 612.00, 2.97],
    [76200, 1152.50, 5.94],
    [82100, 1502.95, 6.60],
    [108900, 3271.75, 8.80],
    [141500, 6140.55, 11.00],
    [185100, 10936.55, 13.20],
    [793900, 91298.15, 13.20],
    [794000, 91310.00, 11.50]
  ];
  var FED_MARRIED = [
    [0, 0, 0],             // bis 29'700 Franken Einkommen: 0.00
    [29700, 0, 1.00],
    [53400, 237.00, 2.00],
    [61300, 395.00, 3.00],
    [79100, 929.00, 4.00],
    [94900, 1561.00, 5.00],
    [108700, 2251.00, 6.00],
    [120600, 2965.00, 7.00],
    [130500, 3658.00, 8.00],
    [138400, 4290.00, 9.00],
    [144300, 4821.00, 10.00],
    [148300, 5221.00, 11.00],
    [150400, 5452.00, 12.00],
    [152400, 5692.00, 13.00],
    [941300, 108249.00, 13.00],
    [941400, 108261.00, 11.50]
  ];

  function fedTax(taxable, married) {
    var A = married ? FED_MARRIED : FED_SINGLE;
    if (taxable <= 0) return 0;
    // find the anchor row whose income <= taxable
    var i = 0;
    while (i + 1 < A.length && A[i + 1][0] <= taxable) i++;
    var base = A[i][1], per100 = A[i][2];
    // Row semantics: [anchorIncome, taxAtAnchor, per100 above anchor].
    // Above the cap anchor the statute applies a flat 11.5% ("Für höhere
    // steuerbare Einkünfte beträgt die Jahressteuer einheitlich 11.5 %").
    var tax;
    // integer-cent arithmetic: per100 rates are exact to 2 decimals
    var steps = Math.floor((taxable - A[i][0]) / 100);
    tax = (Math.round(base * 100) + steps * Math.round(per100 * 100)) / 100;
    // DBG Art. 36: Restbeträge unter 100 Franken fallen ausser Betracht —
    // handled by floor above. The table values are exact formula outputs;
    // the "auf die nächsten 5 Rp abgerundet" rounding applies at assessment,
    // not in Form. 58c, so we reproduce the table exactly.
    if (tax < 25) tax = 0; // Steuerbeträge unter 25 Franken werden nicht erhoben
    return tax;
  }

  // ---- Federal standard deductions 2026 (ESTV Form. 58c era figures) -----
  // Berufskosten: 4% min 2'400 max 4'400; Versicherungsprämien/Zinsen:
  // 1'800 (mit 2. Säule) / 2'800 (ohne); Ehepaarabzug 2'800; Kinder 6'800.
  function fedStandardDeductions(gross, married, children, hasPension) {
    var d = Math.min(4400, Math.max(2400, gross * 0.04));
    d += hasPension ? 1800 : 2800;
    if (married) d += 2800;
    d += 6800 * children;
    return d;
  }

  // ---- Cantonal+communal effective rates (canton capitals, excl. church) --
  // [single, married] at taxable 75'000 / 150'000 / 300'000, COMBINED incl.
  // federal (taxbooks 1.1/2026). Cantonal share is derived by subtracting the
  // exact federal effective rate at each anchor, then interpolated linearly
  // (flat extrapolation outside the anchors).
  var CANTONS = {
    AG: [[14.3, 9.1], [21.3, 16.4], [27.8, 24.8]],
    AI: [[11.7, 8.7], [16.6, 13.8], [20.9, 20.2]],
    AR: [[15.9, 11.9], [22.3, 19.0], [27.9, 26.7]],
    BE: [[20.5, 17.1], [26.9, 23.0], [33.7, 31.3]],
    BL: [[17.3, 9.3], [26.6, 19.4], [34.5, 30.2]],
    BS: [[22.5, 22.1], [25.7, 24.6], [31.6, 29.3]],
    FR: [[18.8, 13.2], [26.5, 20.9], [32.5, 30.0]],
    GE: [[17.2, 10.0], [25.3, 20.4], [32.8, 29.2]],
    GL: [[14.1, 10.7], [20.1, 16.9], [26.7, 24.3]],
    GR: [[14.6, 9.1], [21.3, 17.1], [27.3, 25.1]],
    JU: [[18.3, 13.9], [26.0, 21.0], [32.9, 29.8]],
    LU: [[13.6, 10.2], [18.7, 15.8], [24.5, 23.3]],
    NE: [[20.1, 14.6], [27.9, 22.5], [33.8, 31.7]],
    NW: [[12.9, 9.5], [18.4, 15.3], [22.5, 22.1]],
    OW: [[14.3, 13.9], [17.5, 16.4], [21.5, 21.1]],
    SG: [[16.8, 11.1], [23.7, 18.9], [29.4, 27.3]],
    SH: [[13.1, 8.9], [19.7, 15.5], [25.1, 23.5]],
    SO: [[17.7, 12.4], [24.7, 20.2], [30.8, 28.5]],
    SZ: [[10.6, 8.5], [14.9, 12.8], [20.2, 18.5]],
    TG: [[14.7, 9.8], [20.7, 16.8], [26.8, 24.3]],
    TI: [[16.5, 10.6], [24.4, 20.1], [31.6, 29.9]],
    UR: [[15.4, 15.0], [18.6, 17.5], [22.6, 22.2]],
    VD: [[19.2, 15.5], [27.4, 22.0], [36.2, 31.7]],
    VS: [[15.9, 10.4], [26.4, 18.8], [33.0, 29.3]],
    ZG: [[7.8, 5.8], [14.0, 9.9], [18.7, 17.5]],
    ZH: [[13.0, 9.8], [20.9, 16.7], [29.8, 26.0]]
  };
  var ANCHORS = [75000, 150000, 300000];

  function cantCommRate(taxable, canton, married) {
    var row = CANTONS[canton] || CANTONS.ZH;
    var m = married ? 1 : 0;
    var shares = ANCHORS.map(function (a) {
      return row[ANCHORS.indexOf(a)][m] / 100 - fedTax(a, married) / a;
    });
    // piecewise linear on cantonal share, flat outside
    var share;
    if (taxable <= ANCHORS[0]) share = shares[0];
    else if (taxable >= ANCHORS[2]) share = shares[2];
    else if (taxable <= ANCHORS[1])
      share = shares[0] + (shares[1] - shares[0]) * (taxable - ANCHORS[0]) / (ANCHORS[1] - ANCHORS[0]);
    else
      share = shares[1] + (shares[2] - shares[1]) * (taxable - ANCHORS[1]) / (ANCHORS[2] - ANCHORS[1]);
    return Math.max(0, share);
  }

  // ---- Main estimate ------------------------------------------------------
  // input: { gross, canton, married, children, hasPension, deductions (null=standard), municipalityFactor (null=1) }
  function estimate(inp) {
    var gross = Math.max(0, inp.gross || 0);
    var married = !!inp.married;
    var children = Math.max(0, inp.children || 0);
    var ded = (inp.deductions === null || inp.deductions === undefined)
      ? fedStandardDeductions(gross, married, children, inp.hasPension !== false)
      : Math.max(0, inp.deductions);
    var taxable = Math.max(0, gross - ded);
    var fed = fedTax(taxable, married);
    var childCredit = married ? 263 * children : 0; // Art. 36 Abs. 2bis DBG
    if (childCredit > fed) childCredit = fed;
    fed -= childCredit;
    var cc = cantCommRate(taxable, inp.canton || "ZH", married) * taxable * (inp.municipalityFactor || 1);
    var total = fed + cc;
    return {
      taxable: taxable,
      federal: Math.round(fed),
      cantonalCommunal: Math.round(cc),
      total: Math.round(total),
      effective: gross > 0 ? total / gross : 0
    };
  }

  var api = { fedTax: fedTax, fedStandardDeductions: fedStandardDeductions, cantCommRate: cantCommRate, estimate: estimate, CANTONS: CANTONS };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else global.TaxEngine = api;
})(typeof window !== "undefined" ? window : globalThis);
