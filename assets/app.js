/* steuerberatung.ch — app.js */
(function () {
  "use strict";

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", nav.classList.contains("open") ? "true" : "false");
    });
  }

  /* ---------- Lead form (POST /api/lead) ---------- */
  var form = document.getElementById("lead-form");
  if (form) {
    var status = document.getElementById("form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (status) { status.className = "form-status"; status.textContent = ""; }
      var data = {
        name: form.querySelector("[name=name]").value.trim(),
        email: form.querySelector("[name=email]").value.trim(),
        canton: form.querySelector("[name=canton]").value,
        situation: form.querySelector("[name=situation]").value,
        message: form.querySelector("[name=message]").value.trim()
      };
      if (!data.name || !data.email) {
        if (status) { status.className = "form-status err"; status.textContent = "Bitte Name und E-Mail-Adresse angeben."; }
        return;
      }
      var btn = form.querySelector("button[type=submit]");
      if (btn) { btn.disabled = true; btn.textContent = "Wird gesendet …"; }
      fetch((window.LEAD_ENDPOINT || "https://pixels-urw-mobility-ladder.trycloudflare.com") + "/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          if (status) { status.className = "form-status ok"; status.textContent = "Vielen Dank! Wir melden uns innert 24 Stunden bei Ihnen."; }
          form.reset();
        })
        .catch(function () {
          if (status) { status.className = "form-status err"; status.textContent = "Die Anfrage konnte nicht gesendet werden. Bitte schreiben Sie uns an info@steuerberatung.ch."; }
        })
        .finally(function () {
          if (btn) { btn.disabled = false; btn.textContent = "Anfrage senden"; }
        });
    });
  }

  /* ---------- Tax calculator ---------- */
  var calc = document.getElementById("tax-calc");
  if (calc) {
    var CANTONS = {
      "AG": { base: 0.21, top: 0.36, threshold: 120000 },
      "AR": { base: 0.18, top: 0.32, threshold: 110000 },
      "AI": { base: 0.15, top: 0.28, threshold: 130000 },
      "BL": { base: 0.20, top: 0.34, threshold: 120000 },
      "BS": { base: 0.20, top: 0.33, threshold: 120000 },
      "BE": { base: 0.19, top: 0.33, threshold: 125000 },
      "FR": { base: 0.18, top: 0.32, threshold: 120000 },
      "GE": { base: 0.22, top: 0.38, threshold: 115000 },
      "GL": { base: 0.17, top: 0.31, threshold: 125000 },
      "GR": { base: 0.16, top: 0.30, threshold: 130000 },
      "JU": { base: 0.17, top: 0.31, threshold: 125000 },
      "LU": { base: 0.18, top: 0.32, threshold: 125000 },
      "NE": { base: 0.19, top: 0.33, threshold: 120000 },
      "NW": { base: 0.16, top: 0.30, threshold: 130000 },
      "OW": { base: 0.16, top: 0.30, threshold: 130000 },
      "SG": { base: 0.15, top: 0.29, threshold: 135000 },
      "SH": { base: 0.17, top: 0.31, threshold: 125000 },
      "SZ": { base: 0.17, top: 0.31, threshold: 125000 },
      "SO": { base: 0.18, top: 0.32, threshold: 125000 },
      "TG": { base: 0.18, top: 0.32, threshold: 125000 },
      "TI": { base: 0.17, top: 0.31, threshold: 125000 },
      "UR": { base: 0.15, top: 0.29, threshold: 135000 },
      "VD": { base: 0.20, top: 0.34, threshold: 120000 },
      "VS": { base: 0.16, top: 0.30, threshold: 130000 },
      "ZG": { base: 0.18, top: 0.32, threshold: 125000 },
      "ZH": { base: 0.19, top: 0.33, threshold: 125000 }
    };
    var FEDERAL = 0.0773;

    function effectiveRate(income, canton, deductions) {
      var c = CANTONS[canton] || CANTONS["ZH"];
      var taxable = Math.max(0, income - deductions);
      var t = Math.min(1, taxable / c.threshold);
      var cantRate = c.base + (c.top - c.base) * t;
      return { taxable: taxable, cantRate: cantRate, total: cantRate + FEDERAL };
    }

    function fmt(n) {
      return "CHF " + Math.round(n).toLocaleString("de-CH");
    }

    function runCalc() {
      var income = parseFloat(calc.querySelector("[name=income]").value) || 0;
      var deductions = parseFloat(calc.querySelector("[name=deductions]").value) || 0;
      var canton = calc.querySelector("[name=canton]").value;
      var out = document.getElementById("calc-result");
      if (!out) return;
      if (income <= 0) {
        out.innerHTML = "<p class='muted'>Bitte ein Einkommen eingeben.</p>";
        return;
      }
      var r = effectiveRate(income, canton, deductions);
      var tax = r.taxable * r.total;
      out.innerHTML =
        "<div class='big'>" + (r.total * 100).toFixed(1) + " %</div>" +
        "<p class='muted'>geschätzter effektiver Steuersatz (Bund + Kanton + Gemeinde)</p>" +
        "<table>" +
        "<tr><td>Steuernbares Einkommen</td><td>" + fmt(r.taxable) + "</td></tr>" +
        "<tr><td>Kantonaler + kommunaler Satz</td><td>" + (r.cantRate * 100).toFixed(1) + " %</td></tr>" +
        "<tr><td>Bundessteuer</td><td>" + (FEDERAL * 100).toFixed(1) + " %</td></tr>" +
        "<tr><td>Geschätzte Gesamtsteuer</td><td>" + fmt(tax) + "</td></tr>" +
        "</table>" +
        "<div class='disclaimer'>Vereinfachte Schätzung zu Informationszwecken. Keine Steuerberatung. " +
        "Der tatsächliche Satz hängt von Gemeinde, Familienstand, Abzügen und kantonalen Regeln ab. " +
        "Für eine verbindliche Einschätzung wenden Sie sich an einen unserer geprüften Partner.</div>";
    }

    calc.addEventListener("submit", function (e) { e.preventDefault(); runCalc(); });
    calc.addEventListener("input", runCalc);
    runCalc();
  }

  /* ---------- Order form (POST /api/order) ---------- */
  var oform = document.getElementById("order-form");
  if (oform) {
    var ostatus = document.getElementById("order-status");
    oform.addEventListener("submit", function (e) {
      e.preventDefault();
      if (ostatus) { ostatus.className = "form-status"; ostatus.textContent = ""; }
      var data = {
        name: oform.querySelector("[name=name]").value.trim(),
        email: oform.querySelector("[name=email]").value.trim(),
        canton: oform.querySelector("[name=canton]").value,
        package: oform.querySelector("[name=package]").value,
        price: oform.querySelector("[name=package]").selectedOptions[0] ? oform.querySelector("[name=package]").selectedOptions[0].text : "",
        note: oform.querySelector("[name=note]").value.trim()
      };
      if (!data.name || !data.email || !data.package) {
        if (ostatus) { ostatus.className = "form-status err"; ostatus.textContent = "Bitte Name, E-Mail und Paket angeben."; }
        return;
      }
      var obtn = oform.querySelector("button[type=submit]");
      if (obtn) { obtn.disabled = true; obtn.textContent = "Wird gesendet …"; }
      fetch((window.LEAD_ENDPOINT || "https://pixels-urw-mobility-ladder.trycloudflare.com") + "/api/order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          if (ostatus) { ostatus.className = "form-status ok"; ostatus.textContent = "Vielen Dank! Ihre Bestellung ist eingegangen. Zahlung per PayPal an picaye@gmail.com – die Zugangsdaten erhalten Sie nach Zahlungseingang."; }
          oform.reset();
        })
        .catch(function () {
          if (ostatus) { ostatus.className = "form-status err"; ostatus.textContent = "Die Bestellung konnte nicht gesendet werden. Bitte schreiben Sie uns an info@steuerberatung.ch."; }
        })
        .finally(function () {
          if (obtn) { obtn.disabled = false; obtn.textContent = "Bestellung senden"; }
        });
    });
  }
})();
