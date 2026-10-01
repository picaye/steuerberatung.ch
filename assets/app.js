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
      errNoEndpoint: "Das Formular ist derzeit nicht verfügbar. Bitte schreiben Sie uns direkt an info@steuerberatung.ch.",
      mailFallback: "Ihr E-Mail-Programm öffnet sich mit der fertigen Anfrage – bitte nur noch senden.",
      calcNoIncome: "Bitte ein Einkommen eingeben.",
      calcRate: "geschätzter effektiver Steuersatz (Bund + Kanton + Gemeinde)",
      calcTaxable: "Steuernbares Einkommen",
      calcCantRate: "Kantons- und Gemeindesteuer",
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
      errNoEndpoint: "The form is currently unavailable. Please write to us directly at info@steuerberatung.ch.",
      mailFallback: "Your email client is opening with the enquiry ready — just press send.",
      calcNoIncome: "Please enter an income.",
      calcRate: "estimated effective tax rate (federal + cantonal + municipal)",
      calcTaxable: "Taxable income",
      calcCantRate: "Cantonal + municipal tax",
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
      errNoEndpoint: "Le formulaire est actuellement indisponible. Écrivez-nous directement à info@steuerberatung.ch.",
      mailFallback: "Votre logiciel de messagerie s'ouvre avec la demande prête — il ne reste qu'à envoyer.",
      calcNoIncome: "Veuillez saisir un revenu.",
      calcRate: "taux d'imposition effectif estimé (Confédération + canton + commune)",
      calcTaxable: "Revenu imposable",
      calcCantRate: "Impôt cantonal + communal",
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
      errNoEndpoint: "Il modulo non è attualmente disponibile. Ci scriva direttamente a info@steuerberatung.ch.",
      mailFallback: "Si apre il Suo programma di posta con la richiesta pronta — basta inviarla.",
      calcNoIncome: "Inserisca un reddito.",
      calcRate: "aliquota d'imposta effettiva stimata (Confederazione + cantone + comune)",
      calcTaxable: "Reddito imponibile",
      calcCantRate: "Imposta cantonale + comunale",
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
    /* Pre-fill from query params (e.g. the rechner.html CTA link). */
    try {
      var qs = new URLSearchParams(window.location.search);
      ["message", "situation"].forEach(function (k) {
        var v = qs.get(k);
        if (!v) return;
        var el = form.querySelector("[name=" + k + "]");
        if (el && !el.value) el.value = v;
      });
    } catch (e) { /* URLSearchParams unsupported: skip prefill */ }
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
      var endpoint = window.LEAD_ENDPOINT;
      var mailFallback = function () {
        // No usable endpoint: hand the enquiry to mail instead of losing it.
        // The visitor gets a working path, and nothing is silently dropped.
        var to = "info@steuerberatung.ch";
        var subject = "Werbeanfrage steuerberatung.ch: " + data.name;
        var body = [
          "Firma / Name: " + data.name,
          "E-Mail: " + data.email,
          "Kanton / Region: " + data.canton,
          "Interesse an: " + data.situation,
          "",
          data.message
        ].join("\n");
        window.location.href = "mailto:" + to +
          "?subject=" + encodeURIComponent(subject) +
          "&body=" + encodeURIComponent(body);
        if (status) {
          status.className = "form-status ok";
          status.textContent = (T.mailFallback || T.ok);
        }
        if (btn) { btn.disabled = false; btn.textContent = btnLabel; }
      };
      if (!endpoint) {
        mailFallback();
        return;
      }
      fetch(endpoint.replace(/\/$/, "") + "/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          return res.json();
        })
        .then(function (out) {
          // Only claim success if the server actually recorded the lead.
          if (!out || out.ok !== true) throw new Error("server did not store lead");
          if (status) { status.className = "form-status ok"; status.textContent = T.ok; }
          form.reset();
        })
        .catch(function () {
          // Endpoint unreachable (tunnel down, quota, network): fall back to
          // mail rather than telling the visitor their enquiry failed.
          mailFallback();
        });
    });
  }

  /* ---------- Tax calculator (engine: scripts/tax_engine.js, tested) ---------- */
  var calc = document.getElementById("tax-calc");
  if (calc && window.TaxEngine) {
    function fmt(n) {
      return "CHF " + Math.round(n).toLocaleString("de-CH");
    }
    function runCalc() {
      var income = parseFloat(calc.querySelector("[name=income]").value) || 0;
      var canton = calc.querySelector("[name=canton]").value;
      var married = calc.querySelector("[name=status]").value === "married";
      var children = parseInt(calc.querySelector("[name=children]").value, 10) || 0;
      var dedRaw = calc.querySelector("[name=deductions]").value;
      var deductions = dedRaw === "" ? null : Math.max(0, parseFloat(dedRaw) || 0);
      var out = document.getElementById("calc-result");
      if (!out) return;
      if (income <= 0) {
        out.innerHTML = "<p class='muted'>" + T.calcNoIncome + "</p>";
        return;
      }
      var r = window.TaxEngine.estimate({
        gross: income, canton: canton, married: married, children: children,
        hasPension: true, deductions: deductions
      });
      out.innerHTML =
        "<div class='big'>" + (r.effective * 100).toFixed(1) + " %</div>" +
        "<p class='muted'>" + T.calcRate + "</p>" +
        "<table>" +
        "<tr><td>" + T.calcTaxable + "</td><td>" + fmt(r.taxable) + "</td></tr>" +
        "<tr><td>" + T.calcFed + "</td><td>" + fmt(r.federal) + "</td></tr>" +
        "<tr><td>" + T.calcCantRate + "</td><td>" + fmt(r.cantonalCommunal) + "</td></tr>" +
        "<tr><td>" + T.calcTotal + "</td><td>" + fmt(r.total) + "</td></tr>" +
        "</table>" +
        "<div class='disclaimer'>" + T.calcDisclaimer + "</div>";
    }
    calc.addEventListener("submit", function (e) { e.preventDefault(); runCalc(); });
    calc.addEventListener("input", runCalc);
    runCalc();
  }
})();
