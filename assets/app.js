/* steuerberatung.ch — app.js (i18n: de/en/fr/it) */
(function () {
  "use strict";

  /* ---------- i18n ---------- */
  var I18N = {
    de: {
      errRequired: "Bitte Name und E-Mail-Adresse angeben.",
      sending: "Wird gesendet …",
      ok: "Vielen Dank! Wir melden uns innert 24 Stunden bei Ihnen.",
      errSend: "Die Anfrage konnte nicht gesendet werden. Bitte schreiben Sie uns an info@steuerberatung.ch.",
      calcNoIncome: "Bitte ein Einkommen eingeben.",
      calcRate: "geschätzter effektiver Steuersatz (Bund + Kanton + Gemeinde)",
      calcTaxable: "Steuernbares Einkommen",
      calcCantRate: "Kantonaler + kommunaler Satz",
      calcFed: "Bundessteuer",
      calcTotal: "Geschätzte Gesamtsteuer",
      calcDisclaimer: "Vereinfachte Schätzung zu Informationszwecken. Keine Steuerberatung. " +
        "Der tatsächliche Satz hängt von Gemeinde, Familienstand, Abzügen und kantonalen Regeln ab. " +
        "Für eine verbindliche Einschätzung wenden Sie sich an einen unserer geprüften Partner."
    },
    en: {
      errRequired: "Please enter your name and e-mail address.",
      sending: "Sending …",
      ok: "Thank you! We will get back to you within 24 hours.",
      errSend: "Your request could not be sent. Please write to info@steuerberatung.ch.",
      calcNoIncome: "Please enter an income.",
      calcRate: "estimated effective tax rate (federal + cantonal + municipal)",
      calcTaxable: "Taxable income",
      calcCantRate: "Cantonal + municipal rate",
      calcFed: "Federal tax",
      calcTotal: "Estimated total tax",
      calcDisclaimer: "Simplified estimate for information purposes only. Not tax advice. " +
        "The actual rate depends on municipality, marital status, deductions and cantonal rules. " +
        "For a binding assessment, please contact one of our vetted partners."
    },
    fr: {
      errRequired: "Veuillez indiquer votre nom et votre adresse e-mail.",
      sending: "Envoi en cours …",
      ok: "Merci ! Nous vous répondons dans les 24 heures.",
      errSend: "La demande n'a pas pu être envoyée. Veuillez écrire à info@steuerberatung.ch.",
      calcNoIncome: "Veuillez saisir un revenu.",
      calcRate: "taux d'imposition effectif estimé (Confédération + canton + commune)",
      calcTaxable: "Revenu imposable",
      calcCantRate: "Taux cantonal + communal",
      calcFed: "Impôt fédéral",
      calcTotal: "Impôt total estimé",
      calcDisclaimer: "Estimation simplifiée à titre d'information. Ceci ne constitue pas un conseil fiscal. " +
        "Le taux réel dépend de la commune, de l'état civil, des déductions et des règles cantonales. " +
        "Pour une évaluation contraignante, contactez l'un de nos partenaires vérifiés."
    },
    it: {
      errRequired: "Inserisca nome e indirizzo e-mail.",
      sending: "Invio in corso …",
      ok: "Grazie! Rispondiamo entro 24 ore.",
      errSend: "La richiesta non è stata inviata. Scriva a info@steuerberatung.ch.",
      calcNoIncome: "Inserisca un reddito.",
      calcRate: "aliquota d'imposta effettiva stimata (Confederazione + cantone + comune)",
      calcTaxable: "Reddito imponibile",
      calcCantRate: "Aliquota cantonale + comunale",
      calcFed: "Imposta federale",
      calcTotal: "Imposta totale stimata",
      calcDisclaimer: "Stima semplificata a scopo informativo. Non costituisce consulenza fiscale. " +
        "L'aliquota effettiva dipende da comune, stato civile, deduzioni e regole cantonali. " +
        "Per una valutazione vincolante contatti uno dei nostri partner verificati."
    }
  };
  var docLang = (document.documentElement.lang || "de").slice(0, 2).toLowerCase();
  var T = I18N[docLang] || I18N.de;

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
        message: form.querySelector("[name=message]").value.trim(),
        lang: docLang
      };
      if (!data.name || !data.email) {
        if (status) { status.className = "form-status err"; status.textContent = T.errRequired; }
        return;
      }
      var btn = form.querySelector("button[type=submit]");
      var btnLabel = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = T.sending; }
      fetch((window.LEAD_ENDPOINT || "https://pixels-urw-mobility-ladder.trycloudflare.com") + "/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          if (status) { status.className = "form-status ok"; status.textContent = T.ok; }
          form.reset();
        })
        .catch(function () {
          if (status) { status.className = "form-status err"; status.textContent = T.errSend; }
        })
        .finally(function () {
          if (btn) { btn.disabled = false; btn.textContent = btnLabel; }
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
        out.innerHTML = "<p class='muted'>" + T.calcNoIncome + "</p>";
        return;
      }
      var r = effectiveRate(income, canton, deductions);
      var tax = r.taxable * r.total;
      out.innerHTML =
        "<div class='big'>" + (r.total * 100).toFixed(1) + " %</div>" +
        "<p class='muted'>" + T.calcRate + "</p>" +
        "<table>" +
        "<tr><td>" + T.calcTaxable + "</td><td>" + fmt(r.taxable) + "</td></tr>" +
        "<tr><td>" + T.calcCantRate + "</td><td>" + (r.cantRate * 100).toFixed(1) + " %</td></tr>" +
        "<tr><td>" + T.calcFed + "</td><td>" + (FEDERAL * 100).toFixed(1) + " %</td></tr>" +
        "<tr><td>" + T.calcTotal + "</td><td>" + fmt(tax) + "</td></tr>" +
        "</table>" +
        "<div class='disclaimer'>" + T.calcDisclaimer + "</div>";
    }

    calc.addEventListener("submit", function (e) { e.preventDefault(); runCalc(); });
    calc.addEventListener("input", runCalc);
    runCalc();
  }
})();
