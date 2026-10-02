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
        "Für eine verbindliche Einschätzung wenden Sie sich an einen unserer geprüften Partner.",
      calcKidAge: "Kind {n}, Alter",
      calcRateLive: "effektiver Steuersatz auf dem steuerbaren Einkommen (offizieller ESTV-Tarif)",
      calcChurch: "Kirchensteuer",
      calcFortune: "Vermögenssteuer",
      calcPersonal: "Persönlicher Abzug/Steuer (kantonal)",
      calcModeLive: "Berechnet nach den offiziellen ESTV-Tarifen für Ihre Gemeinde.",
      calcModeEstimate: "Offline-Schätzung mit Kantonsdurchschnitt – die Live-Anbindung ist derzeit nicht erreichbar."
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
        "For a binding assessment, please contact one of our vetted partners.",
      calcKidAge: "Child {n}, age",
      calcRateLive: "effective tax rate on taxable income (official ESTV tariff)",
      calcChurch: "Church tax",
      calcFortune: "Wealth tax",
      calcPersonal: "Personal tax/credit (cantonal)",
      calcModeLive: "Calculated with the official ESTV tariffs for your municipality.",
      calcModeEstimate: "Offline estimate using canton averages — the live connection is currently unavailable."
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
        "Pour une évaluation contraignante, contactez l'un de nos partenaires vérifiés.",
      calcKidAge: "Enfant {n}, âge",
      calcRateLive: "taux d'imposition effectif sur le revenu imposable (tarif officiel AFC)",
      calcChurch: "Impôt ecclésiastique",
      calcFortune: "Impôt sur la fortune",
      calcPersonal: "Taxe personnelle/crédit (cantonal)",
      calcModeLive: "Calculé selon les tarifs officiels de l'AFC pour votre commune.",
      calcModeEstimate: "Estimation hors ligne avec les moyennes cantonales – la connexion live est actuellement indisponible."
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
        "Per una valutazione vincolante contatti uno dei nostri partner verificati.",
      calcKidAge: "Figlio {n}, età",
      calcRateLive: "aliquota effettiva sul reddito imponibile (tariffa ufficiale AFC)",
      calcChurch: "Imposta ecclesiastica",
      calcFortune: "Imposta sulla sostanza",
      calcPersonal: "Imposta personale/credito (cantonale)",
      calcModeLive: "Calcolato con le tariffe ufficiali AFC per il Suo comune.",
      calcModeEstimate: "Stima offline con medie cantonali – la connessione live non è attualmente disponibile."
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

  /* ---------- Tax calculator ----------
     Primary: official ESTV engine via our proxy (/api/tax on the lead
     endpoint — same supervised tunnel). Fallback: scripts/tax_engine.js
     (tested, canton-average estimate) when the proxy is unreachable.
     The result block always labels which mode produced the numbers. */
  var calc = document.getElementById("tax-calc");
  if (calc && window.TaxEngine) {
    function fmt(n) {
      return "CHF " + Math.round(n).toLocaleString("de-CH");
    }
    var locInput = calc.querySelector("[name=location]");
    var locList = document.getElementById("calc-loc-list");
    var kidAgesBox = document.getElementById("calc-kid-ages");
    var sel = { id: 800000000, city: "Zürich", canton: "ZH" };  // default
    var pending = null, timer = null;

    /* --- municipality autocomplete over the static ESTV location list --- */
    function allLocations() { return window.TAX_LOCATIONS || []; }
    function norm(s) {
      return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    }
    function matchLocations(q) {
      q = norm(q.trim());
      if (!q) return [];
      var out = [];
      var list = allLocations();
      for (var i = 0; i < list.length && out.length < 12; i++) {
        var L = list[i];
        if ((L.zip && L.zip.indexOf(q) === 0) ||
            norm(L.city).indexOf(q) !== -1) out.push(L);
      }
      return out;
    }
    function renderLocList(items) {
      if (!locList) return;
      if (!items.length) { locList.hidden = true; locList.innerHTML = ""; return; }
      locList.innerHTML = items.map(function (L, i) {
        return "<button type='button' data-i='" + i + "'>" +
          (L.zip ? L.zip + " " : "") + L.city +
          " <span class='muted'>" + L.canton + "</span></button>";
      }).join("");
      locList.hidden = false;
      locList._items = items;
    }
    if (locInput && locList) {
      locInput.addEventListener("input", function () {
        sel = null;  // text no longer matches a confirmed location
        renderLocList(matchLocations(locInput.value));
        scheduleCalc();
      });
      locInput.addEventListener("focus", function () {
        renderLocList(matchLocations(locInput.value));
      });
      locList.addEventListener("click", function (e) {
        var b = e.target.closest("button[data-i]");
        if (!b || !locList._items) return;
        var L = locList._items[+b.getAttribute("data-i")];
        sel = L;
        locInput.value = (L.zip ? L.zip + " " : "") + L.city;
        locList.hidden = true;
        runCalc();
      });
      document.addEventListener("click", function (e) {
        if (!e.target.closest(".form-field")) locList.hidden = true;
      });
    }

    /* --- child age inputs (the official tariff credits depend on ages) --- */
    function kidCount() {
      return Math.max(0, Math.min(10, parseInt(calc.querySelector("[name=children]").value, 10) || 0));
    }
    function renderKidAges() {
      if (!kidAgesBox) return;
      var n = kidCount(), html = "";
      for (var i = 0; i < n; i++) {
        var have = kidAgesBox.querySelectorAll("input")[i];
        var v = have ? have.value : "10";
        html += "<label class='kid-age'>" + T.calcKidAge.replace("{n}", i + 1) +
          "<input type='number' min='0' max='25' step='1' value='" + v + "'></label>";
      }
      kidAgesBox.innerHTML = html;
    }

    function readForm() {
      var taxable = Math.max(0, parseInt(calc.querySelector("[name=income]").value, 10) || 0);
      var fortuneRaw = calc.querySelector("[name=fortune]");
      var fortune = fortuneRaw ? Math.max(0, parseInt(fortuneRaw.value, 10) || 0) : 0;
      var married = calc.querySelector("[name=status]").value === "married";
      var confSel = calc.querySelector("[name=confession]");
      var confession = confSel ? confSel.value : "NONE";
      var yearSel = calc.querySelector("[name=year]");
      var year = yearSel ? parseInt(yearSel.value, 10) : 2026;
      var ages = [];
      if (kidAgesBox) kidAgesBox.querySelectorAll("input").forEach(function (inp) {
        ages.push(Math.max(0, Math.min(25, parseInt(inp.value, 10) || 10)));
      });
      while (ages.length < kidCount()) ages.push(10);
      return { taxable: taxable, fortune: fortune, married: married,
               confession: confession, year: year, ages: ages };
    }

    function resultRow(label, val) {
      return "<tr><td>" + label + "</td><td>" + fmt(val) + "</td></tr>";
    }

    function renderLive(f, tax) {
      var out = document.getElementById("calc-result");
      var incomeTotal = tax.fed + tax.canton + tax.city + tax.church + tax.personal;
      var eff = f.taxable > 0 ? incomeTotal / f.taxable : 0;
      var rows = resultRow(T.calcFed, tax.fed) +
        resultRow(T.calcCantRate, tax.canton + tax.city);
      if (tax.church) rows += resultRow(T.calcChurch, tax.church);
      if (tax.fortune) rows += resultRow(T.calcFortune, tax.fortune);
      if (tax.personal) rows += resultRow(T.calcPersonal, tax.personal);
      out.innerHTML =
        "<div class='big'>" + (eff * 100).toFixed(1) + " %</div>" +
        "<p class='muted'>" + T.calcRateLive + " · " + tax.location + " " + f.year + "</p>" +
        "<table>" + rows +
        resultRow(T.calcTotal, tax.total) + "</table>" +
        "<div class='calc-mode live'>" + T.calcModeLive + "</div>" +
        "<div class='disclaimer'>" + T.calcDisclaimer + "</div>";
    }

    function renderFallback(f) {
      // Offline estimate: tested local engine, canton of the typed location.
      var canton = (sel && sel.canton) || guessCanton(locInput ? locInput.value : "");
      var r = window.TaxEngine.estimate({
        gross: f.taxable, canton: canton, married: f.married,
        children: f.ages.length, hasPension: true, deductions: 0
      });
      var out = document.getElementById("calc-result");
      out.innerHTML =
        "<div class='big'>" + (r.effective * 100).toFixed(1) + " %</div>" +
        "<p class='muted'>" + T.calcRate + " · " + canton + "</p>" +
        "<table>" +
        resultRow(T.calcFed, r.federal) +
        resultRow(T.calcCantRate, r.cantonalCommunal) +
        resultRow(T.calcTotal, r.total) + "</table>" +
        "<div class='calc-mode est'>" + T.calcModeEstimate + "</div>" +
        "<div class='disclaimer'>" + T.calcDisclaimer + "</div>";
    }

    var CANTON_WORDS = { zürich:"ZH", zurich:"ZH", bern:"BE", luzern:"LU", basel:"BS",
      genf:"GE", geneve:"GE", geneva:"GE", lausanne:"VD", chur:"GR", thurgau:"TG", aargau:"AG",
      tessin:"TI", ticino:"TI", wallis:"VS", waadt:"VD", solothurn:"SO", "st.gallen":"SG", zug:"ZG",
      schaffhausen:"SH", fribourg:"FR", freiburg:"FR", neuchâtel:"NE", appenzell:"AI", graubünden:"GR" };
    function guessCanton(text) {
      var t = (text || "").trim().toLowerCase();
      for (var k in CANTON_WORDS) if (t.indexOf(k) !== -1) return CANTON_WORDS[k];
      return "ZH";
    }

    function runCalc() {
      var out = document.getElementById("calc-result");
      if (!out) return;
      var f = readForm();
      if (f.taxable <= 0) {
        out.innerHTML = "<p class='muted'>" + T.calcNoIncome + "</p>";
        return;
      }
      var endpoint = window.LEAD_ENDPOINT;
      if (!endpoint || !sel) { renderFallback(f); return; }
      var payload = { year: f.year, loc: sel.id, rel: f.married ? 2 : 1,
                      confession: f.confession, children: f.ages.map(function (a) { return { age: a }; }),
                      taxable: f.taxable, fortune: f.fortune };
      if (pending) pending.abort();
      pending = new AbortController();
      fetch(endpoint.replace(/\/$/, "") + "/api/tax", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: pending.signal
      })
        .then(function (res) { if (!res.ok) throw new Error("HTTP " + res.status); return res.json(); })
        .then(function (out2) {
          if (!out2 || out2.ok !== true || !out2.tax) throw new Error("bad payload");
          renderLive(f, out2.tax);
        })
        .catch(function (err) {
          if (err && err.name === "AbortError") return;
          renderFallback(f);
        });
    }

    function scheduleCalc() {
      if (timer) clearTimeout(timer);
      timer = setTimeout(runCalc, 450);
    }

    calc.addEventListener("submit", function (e) { e.preventDefault(); runCalc(); });
    calc.addEventListener("input", function (e) {
      if (e.target.closest("#children")) renderKidAges();
      scheduleCalc();
    });
    calc.addEventListener("change", runCalc);
    renderKidAges();
    runCalc();
  }
})();
