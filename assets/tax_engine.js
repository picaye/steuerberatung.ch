// tax_engine.js — steuerberatung.ch Swiss tax engine v3 (2026).
//
// Faithful port of the calculation semantics of the OFFICIAL ESTV calculator
// (swisstaxcalculator.estv.admin.ch), verified to the franc against its live
// API (see scripts/fetch_estv_fixtures.py + scripts/test_tax_engine.js).
// Data: tax_engine_data.js (generated from ESTV's own yearly exports by
// scripts/build_tax_engine_data.py — tarif tables, Steuerfuss factors,
// deduction tables, personnel taxes).
//
// Two input modes, mirroring the official calculator:
//   calcSimple — taxable income in, tax out (exact parity with ESTV simple mode)
//   calcGross  — brutto employment income in; the standard deduction pipeline
//                (AHV/IV/EO, ALV, NBU, BVG, professional expenses, insurance
//                premiums, social/child deductions, dual-earner deduction) is
//                applied first, with the same defaults ESTV's detailed mode uses.
//
// Rounding conventions (empirically verified against the ESTV API):
//   social contributions — half-up to whole CHF
//   deduction amounts    — floor to whole CHF, then the table's min/max clamps
//   tax components       — half-up to whole CHF; federal minimum: raw tax
//                          (after the child credit) below 25 CHF is not levied
//   taxable income       — floored to 100 CHF before the tariff (FORMEL
//                          cantons excepted, matching ESTV behaviour)
(function (global) {
  "use strict";

  var DATA = (typeof module !== "undefined" && module.exports && typeof require === "function")
    ? require("./tax_engine_data.js")
    : global.TAX_ENGINE_DATA;
  if (!DATA) throw new Error("tax_engine_data.js must be loaded before tax_engine.js");

  // ---------- numeric helpers (all amounts are positive here) ----------
  // Tax components round HALF-EVEN (banker's rounding) — the official
  // calculator's money library (dinero.js transformScale halfEven) does, and
  // parity fixtures confirm it on .5 tie cases.
  function roundHalfEven(x) {
    var f = Math.floor(x);
    var d = x - f;
    if (Math.abs(d - 0.5) < 1e-9) return (f % 2 === 0) ? f : f + 1;
    return Math.round(x);
  }
  function roundHalfUp(x) { return Math.floor(x + 0.5); }
  function floor(x) { return Math.floor(x); }
  function clamp(x, lo, hi) { return Math.min(hi, Math.max(lo, x)); }
  function pct(x, p) { return (x * p) / 100; }
  function floor100(x) { return Math.floor(x / 100) * 100; }

  // ---------- formula parser for FORMEL cantons (e.g. BL) ----------
  // expr := term (('+'|'-') term)* ; term := unary (('*'|'/') unary)* ;
  // unary := '-' unary | primary ; primary := number | 'log' primary
  //          | '(' expr ')' | $wert$
  function evalFormula(formula, wert) {
    if (!formula) return 0;
    var tokens = [];
    var i = 0, s = formula;
    while (i < s.length) {
      var ch = s[i];
      if (ch === " " || ch === "\t") { i++; continue; }
      if (ch === "$") {
        var end = s.indexOf("$", i + 1);
        if (end === -1) throw new Error("bad formula variable: " + formula);
        tokens.push(String(wert));
        i = end + 1;
        continue;
      }
      if (s.substr(i, 3) === "log") { tokens.push("log"); i += 3; continue; }
      if ("+-*/()".indexOf(ch) >= 0) { tokens.push(ch); i++; continue; }
      if (/[0-9.]/.test(ch)) {
        var num = "";
        while (i < s.length && /[0-9.]/.test(s[i])) { num += s[i]; i++; }
        tokens.push(num);
        continue;
      }
      throw new Error("bad formula char '" + ch + "' in: " + formula);
    }
    var ctx = { pos: 0 };
    function expr() {
      var left = term();
      while (ctx.pos < tokens.length && (tokens[ctx.pos] === "+" || tokens[ctx.pos] === "-")) {
        var op = tokens[ctx.pos++];
        var right = term();
        left = op === "+" ? left + right : left - right;
      }
      return left;
    }
    function term() {
      var left = unary();
      while (ctx.pos < tokens.length && (tokens[ctx.pos] === "*" || tokens[ctx.pos] === "/")) {
        var op = tokens[ctx.pos++];
        var right = unary();
        left = op === "*" ? left * right : left / right;
      }
      return left;
    }
    function unary() {
      if (tokens[ctx.pos] === "-") { ctx.pos++; return -unary(); }
      return primary();
    }
    function primary() {
      var t = tokens[ctx.pos];
      if (t === "log") { ctx.pos++; return Math.log(primary()); }
      if (t === "(") {
        ctx.pos++;
        var v = expr();
        if (tokens[ctx.pos] !== ")") throw new Error("missing ) in: " + formula);
        ctx.pos++;
        return v;
      }
      var n = parseFloat(t);
      if (isNaN(n)) throw new Error("expected number, got '" + t + "' in: " + formula);
      ctx.pos++;
      return n;
    }
    var result = expr();
    if (ctx.pos !== tokens.length) throw new Error("trailing tokens in: " + formula);
    return result;
  }

  // ---------- tarif tables ----------
  // Group preference (ESTV fallback semantics):
  //   married     -> VERHEIRATET
  //   single+kids -> LEDIG_MIT_KINDER, then LEDIG_ALLEINE
  //   single      -> LEDIG_ALLEINE
  // A table matches when its group list is "ALLE" or contains the group name.
  // Splitting applies only when the matched group itself is VERHEIRATET or
  // LEDIG_MIT_KINDER (an "ALLE" table with splitting>0 still splits — ESTV
  // data pairs splitting with those groups; verified by parity tests).
  function groupChain(married, children) {
    if (married) return ["VERHEIRATET"];
    if (children > 0) return ["LEDIG_MIT_KINDER", "LEDIG_ALLEINE"];
    return ["LEDIG_ALLEINE"];
  }

  function pickTarif(canton, ty, married, children) {
    return pickTarifTarget(canton, ty, married, children, "k");
  }
  // SZ and VS publish a separate GEMEINDE (communal) tarif table; the communal
  // tax comes from that table rather than factor x cantonal tax.
  function pickGemeinde(canton, ty, married, children) {
    var all = DATA.tarifs[canton] || [];
    var has = all.some(function (t) { return t.t === "g" && t.ty === ty; });
    if (!has) return null;
    return pickTarifTarget(canton, ty, married, children, "g");
  }
  function pickTarifTarget(canton, ty, married, children, target) {
    var all = DATA.tarifs[canton] || DATA.tarifs.ZH;
    var chain = groupChain(married, children);
    for (var gi = 0; gi < chain.length; gi++) {
      for (var i = 0; i < all.length; i++) {
        var t = all[i];
        if (t.ty !== ty) continue;
        if ((t.t || "k") !== target) continue;
        if (t.g === "ALLE" || t.g.indexOf(chain[gi]) >= 0) {
          return { tarif: t, usedGroup: chain[gi] };
        }
      }
    }
    throw new Error("no " + target + " tarif for " + canton + " ty=" + ty + " married=" + married);
  }

  // BUND rows: [threshold, percentAbove, taxAtThreshold, null]
  function bundTax(table, x) {
    var row = table[0];
    for (var i = 0; i < table.length; i++) {
      if (table[i][0] <= x) row = table[i];
      else break;
    }
    return row[2] + pct(x - row[0], row[1]);
  }

  // ZUERICH rows: [bandWidth, percent, 0, null] — consume bands in order
  function zurichTax(table, x) {
    var tax = 0, remaining = x;
    for (var i = 0; i < table.length && remaining > 0; i++) {
      var usable = Math.min(remaining, table[i][0]);
      tax += pct(usable, table[i][1]);
      remaining -= usable;
    }
    return tax;
  }

  // FREIBURG: continuous effective-rate table. The FIRST row whose threshold
  // is >= x closes the segment; the effective rate is interpolated linearly
  // between the previous row and the closing row and applied to the whole
  // income. Above the table top the last rate applies.
  // (Verified against ESTV: FR city 30k/50k/100k all exact.)
  function freiburgTax(table, x) {
    var prev = null;
    for (var i = 0; i < table.length; i++) {
      var row = table[i];
      if (row[0] >= x) {
        if (!prev || prev[0] === 0) return 0;
        var rate = prev[1] + ((row[1] - prev[1]) / (row[0] - prev[0])) * (x - prev[0]);
        return pct(x, rate);
      }
      prev = row;
    }
    return pct(x, prev[1]);
  }

  function flattaxTax(table, x) { return pct(x, table[0][1]); }

  function formelTax(table, x) {
    var row = table[0];
    for (var i = 0; i < table.length; i++) {
      if (table[i][0] <= x) row = table[i];
      else break;
    }
    if (!row[3]) return 0;
    return Math.max(0, evalFormula(row[3], x));
  }

  function splittingEligible(usedGroup) {
    return usedGroup === "VERHEIRATET" || usedGroup === "LEDIG_MIT_KINDER";
  }

  // Tax for one tarif table, incl. splitting and ESTV's 100-CHF flooring.
  // usedGroup is the REQUESTED group (VERHEIRATET / LEDIG_MIT_KINDER /
  // LEDIG_ALLEINE), not the table's group string — a single "ALLE" table serves
  // every group, but only couples/single-parents may apply its splitting.
  // Flooring order (verified against ESTV, AG married 15'350 -> 67): the TOTAL
  // taxable income is floored to 100 FIRST, then split; the split share is
  // NOT re-floored.
  // quantum: 100 = floor taxable income to 100 CHF before the tariff (most
  // cantons), 1 = tax the exact income (BL single/GE/GR/SO/UR — probed from
  // the live calculator, stored in DATA.quantum). FORMEL tables are always
  // exact. Federal is always floor-100 (DBG Art. 36 per-100 steps).
  function tarifTax(tarif, usedGroup, taxable, quantum) {
    var x = Math.max(0, taxable);
    var split = (tarif.s > 0 && splittingEligible(usedGroup)) ? tarif.s : 1;
    // Some cantons ship BUND-style rows under tableType ZUERICH; detect via a
    // non-zero "tax at threshold" column (same workaround ESTV's data needs).
    var type = tarif.tt;
    if (type === 1) {
      for (var i = 0; i < tarif.r.length; i++) if (tarif.r[i][2] > 0) { type = 0; break; }
    }
    if (type !== 4 && quantum !== 1) x = floor100(x);
    if (split !== 1) x = x / split;
    var raw;
    switch (type) {
      case 0: raw = bundTax(tarif.r, x); break;
      case 1: raw = zurichTax(tarif.r, x); break;
      case 2: raw = flattaxTax(tarif.r, x); break;
      case 3: raw = freiburgTax(tarif.r, x); break;
      case 4: raw = formelTax(tarif.r, x); break;
      default: throw new Error("unknown table type " + type);
    }
    if (split !== 1) raw = raw * split;
    return raw;
  }

  // ---------- federal tax (DBG Art. 36, 2026) ----------
  // Married couples AND single parents use the family tariff; the tax is
  // reduced by 263 CHF per child (Art. 36 Abs. 2bis). Amounts below 25 CHF
  // are not levied (Abs. 2ter) — the minimum test applies AFTER the credit.
  function fedTaxRaw(taxable, married, children) {
    var picked = pickTarif("CH", 0, married, children);
    var raw = tarifTax(picked.tarif, picked.usedGroup, taxable);
    var credit = children > 0 ? DATA.fedChildCredit * children : 0;
    if (credit > raw) credit = raw;
    return raw - credit;
  }
  function fedTax(taxable, married, children) {
    var raw = fedTaxRaw(taxable, married, children || 0);
    if (raw < 25) return 0;
    return roundHalfUp(raw);
  }

  // ---------- personnel tax (flat per-head cantonal tax) ----------
  // DATA.personnel[kt] = [amountSingle, doublesForMarried]
  function personnelTax(canton, married) {
    var p = DATA.personnel[canton];
    if (!p) return 0;
    return p[0] * (married && p[1] ? 2 : 1);
  }

  // ---------- oracle-calibrated curves ----------
  // DATA.calibration[kt][group] = { incs: [...], k: { "0": [cbase[], mbase[],
  // ctax[], citytax[], credit[]], "1": [...], ... } } — sampled from the live
  // ESTV calculator for cells whose live backend diverges from the public
  // export (see fetch_estv_calibration.py). Linear interpolation between
  // income nodes on every column; beyond the last node, extrapolate with the
  // final segment's slope. For child counts above the highest sampled k, the
  // per-extra-child delta (k_max - k_max-1) is applied, taxes clamped at 0.
  // Resolve the curve columns for a child count:
  //  - exact k available -> use it
  //  - cell has a flat per-child rebate (DATA.childEffects[canton], VS/NE) ->
  //    take the sampled curve and subtract rebate*(kids - kSampled)
  //  - multi-k cell (VD/BL) above kmax -> extrapolate with the (kmax - kmax-1)
  //    delta per income node
  function calibColumns(canton, cell, kids) {
    var keys = Object.keys(cell.k).map(Number).sort(function (a, b) { return a - b; });
    var kmax = keys[keys.length - 1];
    if (kids <= kmax) {
      if (cell.k[String(kids)]) return cell.k[String(kids)];
      // gap in sampled kids (never happens with complete fixtures): use the
      // largest sampled k below, then the flat-rebate/delta rules adjust it
      var below = keys.filter(function (k) { return k < kids; });
      var use = below.length ? below[below.length - 1] : keys[0];
      kids = use; // fall through to rebate/delta extrapolation below
      kmax = use;
    }
    var eff = (DATA.childEffects && DATA.childEffects[canton]) || null;
    if (eff) {
      // flat rebate (VS/NE): curve sampled at kmax, subtract rebate per extra child
      var base = cell.k[String(kmax)];
      var extra = kids - kmax;
      return base.map(function (col, ci) {
        if (ci === 2) return col.map(function (v) { return Math.max(0, v - eff.cant * extra); });
        if (ci === 3) return col.map(function (v) { return Math.max(0, v - eff.city * extra); });
        return col;
      });
    }
    var top = cell.k[String(kmax)];
    if (keys.length < 2) {
      // single-k cell (staircase cantons, SZ): children do NOT change the
      // cantonal/city tax — verified by probe for AI/GL/GR/NW/SG/SH/SO/TG/SZ
      // (only the flat SH/TG TaxCredit scales, added separately in calcSimple).
      return top;
    }
    // delta extrapolation (VD/BL multi-k cells): taxes clamp at 0, credits may grow
    var prev = cell.k[String(kmax - 1)];
    return top.map(function (col, ci) {
      return col.map(function (v, i) {
        var d = v - prev[ci][i];
        var out = v + d * (kids - kmax);
        return ci === 4 ? out : Math.max(0, out);
      });
    });
  }
  function interpCalib(canton, cell, kids, x) {
    var cols = calibColumns(canton, cell, kids);
    var incs = cell.incs, n = incs.length;
    var out = cols.map(function () { return 0; });
    var i, j;
    if (x <= incs[0]) {
      for (j = 0; j < cols.length; j++) out[j] = cols[j][0];
      return out;
    }
    for (i = 1; i < n; i++) {
      if (incs[i] >= x) {
        var w = incs[i] === incs[i - 1] ? 0 : (x - incs[i - 1]) / (incs[i] - incs[i - 1]);
        for (j = 0; j < cols.length; j++)
          out[j] = cols[j][i - 1] + (cols[j][i] - cols[j][i - 1]) * w;
        return out;
      }
    }
    for (j = 0; j < cols.length; j++) {
      var slope = (cols[j][n - 1] - cols[j][n - 2]) / (incs[n - 1] - incs[n - 2]);
      out[j] = cols[j][n - 1] + slope * (x - incs[n - 1]);
    }
    return out;
  }

  // ---------- simple mode: taxable income (+ optional fortune) -> tax ----------
  // DATA.factors[kt] = [incomeCanton%, incomeCity%, fortuneCanton%, fortuneCity%]
  function calcSimple(inp) {
    var canton = DATA.factors[inp.canton] ? inp.canton : "ZH";
    var f = DATA.factors[canton];
    var married = !!inp.married;
    var children = Math.max(0, inp.children || 0);
    var taxableCant = Math.max(0, inp.taxableCanton !== undefined ? inp.taxableCanton : (inp.taxable || 0));
    var taxableFed = Math.max(0, inp.taxableFed !== undefined ? inp.taxableFed : taxableCant);
    var fortune = Math.max(0, inp.fortune || 0);

    var fed = fedTax(taxableFed, married, children);

    // ESTV keeps full precision on the simple cantonal tax and rounds only the
    // final components (verified across cantons: rounding the base first loses
    // on ~50% of cases).
    var incPicked = pickTarif(canton, 0, married, children);
    var cityFactor = (inp.cityFactor !== undefined && inp.cityFactor !== null) ? inp.cityFactor : f[1];

    // Oracle-calibrated cells: for a few (canton, group) pairs the live ESTV
    // calculator uses internal tariff data its public export omits (fractional
    // splitting rounding, VS/VD coefficients, per-child cantonal rebates).
    // scripts/fetch_estv_calibration.py samples the oracle; interpolate it.
    var cell = (DATA.calibration && DATA.calibration[canton] &&
                DATA.calibration[canton][incPicked.usedGroup]) || null;

    // Fortune first: TG's Bagatellgrenze waiver of income tax depends on the
    // computed fortune tax being zero (probed 2026-10-02).
    var fortuneCantonTax = 0, fortuneCityTax = 0, simpleFortune = 0;
    if (fortune > 0) {
      var wPicked = pickTarif(canton, 1, married, children);
      simpleFortune = tarifTax(wPicked.tarif, wPicked.usedGroup, fortune);
      fortuneCantonTax = roundHalfUp(pct(simpleFortune, f[2]));
      fortuneCityTax = roundHalfUp(pct(simpleFortune, f[3]));
      var gFort = pickGemeinde(canton, 1, married, children);
      if (gFort) {
        fortuneCityTax = roundHalfUp(pct(tarifTax(gFort.tarif, gFort.usedGroup, fortune), f[3]));
      }
    }

    var cantonTax, cityTax, childCredit = 0;
    if (cell) {
      // [cantonalBase, communalBase, cantonalTax, cityTax, taxCredit]
      // All calibrated cantons quantize income to 100 (probed); flooring first
      // makes interpolation EXACT at every node and piecewise-linear between.
      var qCell = 100;
      if (DATA.quantum && DATA.quantum[canton]) {
        qCell = DATA.quantum[canton][married ? "married" : "single"] || 100;
      }
      var xCalib = qCell === 1 ? taxableCant : floor100(taxableCant);
      var cb = interpCalib(canton, cell, children, xCalib);
      cantonTax = roundHalfUp(cb[2]);
      cityTax = inp.cityFactor !== undefined && inp.cityFactor !== null
        ? roundHalfUp(pct(cb[1], cityFactor))   // user-overridden communal factor
        : roundHalfUp(cb[3]);
      childCredit = Math.max(0, -cb[4]);        // taxCredit arrives negative
      // flat per-child credit beyond the sampled kmax (SH 320 / TG 100):
      var kmaxCell = Math.max.apply(null, Object.keys(cell.k).map(Number));
      if (children > kmaxCell && DATA.childCredits && DATA.childCredits[canton]) {
        childCredit += DATA.childCredits[canton] * (children - kmaxCell);
      }
    } else {
      var q = 100;
      if (DATA.quantum && DATA.quantum[canton]) {
        q = DATA.quantum[canton][married ? "married" : "single"] || 100;
      }
      var simpleInc = tarifTax(incPicked.tarif, incPicked.usedGroup, taxableCant, q);
      // Bagatellgrenze (TG 2026, probed exactly): when the COMBINED simple tax
      // (income + fortune) is below the threshold, no canton/city tax is levied
      // at all — verified: inc13k+fort10k (16+11=27<30) -> 0; inc13k+fort20k
      // (16+22=38>=30) -> both levied; fort25k alone (28<30) -> 0; fort27k
      // (30>=30) -> levied. Data-driven via DATA.bagatelle.
      var bag = DATA.bagatelle && DATA.bagatelle[canton];
      // Threshold compares the ROUNDED combined simple tax (TG fortune 27k:
      // raw 29.7 displays as 30 -> levied, and levied amounts still compute
      // from the raw 29.7: fortCant round(29.7*1.09)=32 = ESTV).
      if (bag && roundHalfUp(simpleInc + simpleFortune) < bag) {
        cantonTax = 0; cityTax = 0;
        fortuneCantonTax = 0; fortuneCityTax = 0;
      } else {
      cantonTax = roundHalfUp(pct(simpleInc, f[0]));
      cityTax = roundHalfUp(pct(simpleInc, cityFactor));
      // SZ and VS publish a separate GEMEINDE tarif: the communal tax is its
      // own table's result (times the communal Steuerfuss), not factor x canton.
      var gInc = pickGemeinde(canton, 0, married, children);
      if (gInc) {
        cityTax = roundHalfUp(pct(tarifTax(gInc.tarif, gInc.usedGroup, taxableCant, q), cityFactor));
      }
      }
      // Cantonal per-child tax credits (SH 320, TG 100 in 2026 — probed).
      if (children > 0 && DATA.childCredits && DATA.childCredits[canton]) {
        childCredit = DATA.childCredits[canton] * children;
      }
    }


    var pers = personnelTax(canton, married);
    // child credits reduce the total but never below zero (no refunds —
    // verified: SH low-income k2 total is 0, not negative)
    var total = Math.max(0, fed + cantonTax + cityTax + fortuneCantonTax + fortuneCityTax + pers - childCredit);
    return {
      federal: fed,
      cantonTax: cantonTax,
      cityTax: cityTax,
      fortuneCantonTax: fortuneCantonTax,
      fortuneCityTax: fortuneCityTax,
      personnelTax: pers,
      childCredit: childCredit,
      churchTax: 0,
      total: total,
      taxableCanton: taxableCant,
      taxableFed: taxableFed
    };
  }

  // ---------- gross -> net salary pipeline (ESTV detailed-mode defaults) ----------
  var S = DATA.social;
  // Default 2nd-pillar employee contribution (fitted exactly to ESTV probes):
  // entry threshold 22'680; coordinated salary = gross - 26'460, clamped to
  // [3'780, 64'260]; age bands 0/3.5/5/7.5/9%; excess above 90'720 at 3.5%.
  function bvgDefault(gross, age) {
    var b = S.bvg;
    if (gross <= b.entryThreshold) return 0;
    var rate = 0;
    for (var i = 0; i < b.bands.length; i++) if (age >= b.bands[i][0]) rate = b.bands[i][1];
    var coordinated = clamp(gross - b.coordination, b.minInsured,
                            b.maxPensionableSalary - b.coordination);
    var excess = Math.max(0, gross - b.maxPensionableSalary);
    return roundHalfUp(pct(coordinated, rate) + pct(excess, b.excessPct));
  }
  function socialContributions(gross, age) {
    var g = Math.max(0, gross);
    var ahv = roundHalfUp(pct(g, S.ahvIvEoPct));
    var capped = Math.min(g, S.maxSalaryAlvNbu);
    var alv = roundHalfUp(pct(capped, S.alvPct));
    var nbu = roundHalfUp(pct(capped, S.nbuPct));
    var bvg = bvgDefault(g, age);
    return { ahv: ahv, alv: alv, nbu: nbu, bvg: bvg, net: g - ahv - alv - nbu - bvg };
  }

  // ---------- deduction tables ----------
  // item: [formatCode, percent, minimum, maximum, amount]
  // formats: 0 MAXIMUM | 1 PERCENT | 2 PERCENT,MIN,MAX | 3 STANDARDIZED
  //          4 PERCENT,MAXIMUM
  function dedTable(scope) { return DATA.deductions[scope] || {}; }
  function applyFormat(item, base) {
    if (!item) return 0;
    switch (item[0]) {
      case 0: return Math.min(base, item[3]);
      case 1: return pct(base, item[1]);
      case 2: return clamp(pct(base, item[1]), item[2], item[3]);
      case 3: return item[4];
      case 4: return Math.min(pct(base, item[1]), item[3]);
      default: return 0;
    }
  }
  function dedFloor(scope, id, base) {
    return floor(applyFormat(dedTable(scope)[id], base === undefined ? 0 : base));
  }

  // Insurance-premium deduction family. Cantons use one of two id families;
  // both are capped maximums fed by ESTV's default premium assumption
  // (4'560 per adult, 1'400 per child). The with/without-2nd-pillar variant is
  // selected by whether any earner has BVG contributions.
  var KK_ADULT = 4560, KK_CHILD = 1400;
  function kkDeduction(scope, married, children, hasBvg) {
    var t = dedTable(scope);
    var total = 0;
    if (t.KKSparLedigMitBVGS3a_EK || t.KKSparLedigOhneBVGS3a_EK) {
      var idAdult = married
        ? (hasBvg ? "KKSparzVerhMitBVGS3a_EK" : "KKSparVerhOhneBVGS3a_EK")
        : (hasBvg ? "KKSparLedigMitBVGS3a_EK" : "KKSparLedigOhneBVGS3a_EK");
      total += applyFormat(t[idAdult], KK_ADULT * (married ? 2 : 1));
      if (children > 0 && t.KKSparProKind_EK)
        total += applyFormat(t.KKSparProKind_EK, KK_CHILD) * children;
    } else {
      var idP = married ? "KKPrivVersVerheiratet_EK" : "KKPrivVersLedig_EK";
      if (t[idP]) total += applyFormat(t[idP], KK_ADULT * (married ? 2 : 1));
      if (children > 0 && t.KKPrivVersProKind_EK)
        total += applyFormat(t.KKPrivVersProKind_EK, KK_CHILD) * children;
      if (children > 0 && t.KKProMinderjKind_EK)
        total += applyFormat(t.KKProMinderjKind_EK, KK_CHILD) * children;
    }
    return floor(total);
  }

  // ---------- gross mode: full default deduction pipeline ----------
  function calcGross(inp) {
    var canton = DATA.factors[inp.canton] ? inp.canton : "ZH";
    var married = !!inp.married;
    var children = Math.max(0, inp.children || 0);
    var defaultAge = inp.age || 35;
    var persons = (inp.persons && inp.persons.length)
      ? inp.persons
      : [{ gross: Math.max(0, inp.gross || 0), age: defaultAge }];
    if (married && persons.length < 2) persons = [persons[0], { gross: 0, age: defaultAge }];
    if (!married && persons.length > 1) persons = [persons[0]];

    var details = persons.map(function (p) {
      var age = p.age === undefined ? defaultAge : p.age;
      var s = socialContributions(p.gross, age);
      return { gross: Math.max(0, p.gross), age: age, ahv: s.ahv, alv: s.alv,
               nbu: s.nbu, bvg: s.bvg, net: s.net };
    });
    var hasBvg = details.some(function (d) { return d.bvg > 0; });
    var netTotal = details.reduce(function (a, d) { return a + d.net; }, 0);

    // per-person professional-expenses flat rate (HauptErw_EK)
    var profFed = details.map(function (d) {
      return d.net > 0 ? dedFloor("CH", "HauptErw_EK", d.net) : 0;
    });
    var profCant = details.map(function (d) {
      return d.net > 0 ? dedFloor(canton, "HauptErw_EK", d.net) : 0;
    });

    function build(scope, prof) {
      var t = dedTable(scope);
      var ded = 0;
      for (var i = 0; i < details.length; i++) ded += prof[i];
      ded += kkDeduction(scope, married, children, hasBvg);
      if (married) {
        if (t.SozVerheiratet_EK) ded += applyFormat(t.SozVerheiratet_EK, 0);
      } else {
        if (t.SozLedig_EK) ded += applyFormat(t.SozLedig_EK, 0);
        if (children > 0) {
          if (t.SozAlleinerzieher_EK) ded += applyFormat(t.SozAlleinerzieher_EK, 0);
          if (t.SozKindAlleinerzieher_EK) ded += applyFormat(t.SozKindAlleinerzieher_EK, 0);
          if (t.SozAlleinEigenemHaushalt_EK) ded += applyFormat(t.SozAlleinEigenemHaushalt_EK, 0);
        }
      }
      if (children > 0) {
        if (t.SozKind_EK) ded += floor(applyFormat(t.SozKind_EK, 0)) * children;
        if (t.EigenBetr_EK) ded += floor(applyFormat(t.EigenBetr_EK, 0)) * children;
      }
      // dual-earner deduction: only when both partners have income
      if (married && details[0].net > 0 && details[1].net > 0 && t.ZweitVerdiener_EK) {
        var bases = details.map(function (d, i) {
          return Math.max(0, d.net - prof[i]);
        }).sort(function (a, b) { return a - b; });
        var item = t.ZweitVerdiener_EK;
        // ESTV federal rule: 50% of the lower earner's net-after-professional,
        // floored, clamped to the table's [min,max]; MAXIMUM-only tables (ZH
        // style) cap the lower earner's basis directly.
        ded += item[0] === 2
          ? floor(clamp(pct(bases[0], item[1]), item[2], item[3]))
          : Math.min(bases[0], item[3]);
      }
      return Math.min(ded, netTotal);
    }

    var dedFed = build("CH", profFed);
    var dedCant = build(canton, profCant);
    var taxableFed = Math.max(0, floor(netTotal - dedFed));
    var taxableCant = Math.max(0, floor(netTotal - dedCant));

    var simple = calcSimple({
      canton: canton, married: married, children: children,
      taxableCanton: taxableCant, taxableFed: taxableFed,
      fortune: inp.fortune || 0, cityFactor: inp.cityFactor
    });
    simple.persons = details;
    simple.deductionsFed = dedFed;
    simple.deductionsCant = dedCant;
    simple.grossTotal = details.reduce(function (a, d) { return a + d.gross; }, 0);
    simple.netTotal = netTotal;
    return simple;
  }

  // ---------- public estimate() — website entry point ----------
  // input: { gross, canton, married, children, age, fortune, cityFactor,
  //          persons, taxable (override: skip the gross pipeline) }
  function estimate(inp) {
    var r = (inp.taxable !== undefined && inp.taxable !== null)
      ? calcSimple({
          canton: inp.canton, married: inp.married, children: inp.children,
          taxableCanton: inp.taxable,
          taxableFed: inp.taxableFed !== undefined ? inp.taxableFed : inp.taxable,
          fortune: inp.fortune, cityFactor: inp.cityFactor
        })
      : calcGross(inp);
    var grossForRate = r.grossTotal !== undefined ? r.grossTotal : Math.max(0, inp.gross || 0);
    return {
      taxable: r.taxableCant,
      taxableFed: r.taxableFed,
      federal: r.federal,
      cantonalCommunal: r.cantonTax + r.cityTax + r.fortuneCantonTax + r.fortuneCityTax + r.personnelTax,
      cantonTax: r.cantonTax,
      cityTax: r.cityTax,
      fortuneTax: r.fortuneCantonTax + r.fortuneCityTax,
      personnelTax: r.personnelTax,
      total: r.total,
      effective: grossForRate > 0 ? r.total / grossForRate : 0,
      persons: r.persons,
      deductionsFed: r.deductionsFed,
      deductionsCant: r.deductionsCant,
      netTotal: r.netTotal
    };
  }

  var api = {
    version: 3,
    year: DATA.year,
    estimate: estimate,
    calcSimple: calcSimple,
    calcGross: calcGross,
    fedTax: fedTax,
    fedTaxRaw: fedTaxRaw,
    tarifTax: tarifTax,
    pickTarif: pickTarif,
    personnelTax: personnelTax,
    socialContributions: socialContributions,
    bvgDefault: bvgDefault,
    evalFormula: evalFormula,
    DATA: DATA
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else global.TaxEngine = api;
})(typeof window !== "undefined" ? window : globalThis);
