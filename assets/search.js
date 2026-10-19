/* steuerberatung.ch article search — client-side over assets/search-index.js.
   Accent-insensitive, token-AND, scored (title > heading > description > body).
   UI strings come from window.SEARCH_UI set inline by each language page. */
(function () {
  var idx = window.SEARCH_INDEX || [];
  var ui = window.SEARCH_UI || { results: "results", nores: "No results", all: "all languages", popular: "Popular topics" };
  var pageLang = document.documentElement.lang.slice(0, 2);

  function norm(s) {
    return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }
  // build normalized haystacks once
  var docs = idx.map(function (e) {
    return { e: e, nt: norm(e.t), nh: norm(e.h.join(" ")), nd: norm(e.d), nb: norm(e.b) };
  });

  var input = document.getElementById("search-q");
  var out = document.getElementById("search-results");
  var count = document.getElementById("search-count");
  var allBox = document.getElementById("search-all");
  var chips = document.getElementById("search-chips");
  var audBar = document.getElementById("search-aud");
  var audSel = null;
  var AUD_KEYS = ["solo", "verheiratet", "konkubinat", "firma"];

  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  function snippet(e, tokens) {
    var low = norm(e.b);
    var pos = -1, hit = "";
    for (var i = 0; i < tokens.length; i++) {
      var p = low.indexOf(tokens[i]);
      if (p >= 0 && (pos < 0 || p < pos)) { pos = p; hit = tokens[i]; }
    }
    if (pos < 0) return esc(e.d.slice(0, 180)) + (e.d.length > 180 ? "…" : "");
    var a = Math.max(0, pos - 70), b = Math.min(e.b.length, pos + 130);
    return (a > 0 ? "…" : "") + esc(e.b.slice(a, b)) + (b < e.b.length ? "…" : "");
  }

  function search(q) {
    var tokens = norm(q).split(/\s+/).filter(Boolean);
    if (!tokens.length && !audSel) { out.innerHTML = ""; count.textContent = ""; return; }
    var onlyLang = !(allBox && allBox.checked);
    var scored = [];
    for (var i = 0; i < docs.length; i++) {
      var d = docs[i];
      if (onlyLang && d.e.l !== pageLang) continue;
      if (audSel && !(d.e.a && d.e.a.indexOf(audSel) >= 0)) continue;
      var score = 0, ok = true;
      for (var j = 0; j < tokens.length; j++) {
        var t = tokens[j], s = 0;
        if (d.nt.indexOf(t) >= 0) s += 6;
        if (d.nh.indexOf(t) >= 0) s += 3;
        if (d.nd.indexOf(t) >= 0) s += 2;
        if (d.nb.indexOf(t) >= 0) s += 1;
        if (!s) { ok = false; break; }
        score += s;
      }
      if (ok) scored.push({ d: d, score: score });
    }
    scored.sort(function (a, b) { return b.score - a.score || (b.d.e.dt > a.d.e.dt ? 1 : -1); });
    var top = scored.slice(0, 15);
    count.textContent = scored.length + " " + (scored.length === 1 ? ui.singular : ui.results);
    out.innerHTML = top.map(function (r) {
      var e = r.d.e;
      var href = (e.l === pageLang) ? e.s : (e.l === "de" ? "../" + e.s : "../" + e.l + "/" + e.s);
      if (pageLang === "de" && e.l !== "de") href = e.l + "/" + e.s;
      var badge = (e.l !== pageLang) ? '<span class="search-lang">' + e.l.toUpperCase() + "</span> " : "";
      var date = e.dt ? '<span class="search-date">' + esc(e.dt) + "</span>" : "";
      return '<li><a href="' + href + '">' + badge + esc(e.t) + "</a> " + date +
             '<p class="search-snip">' + snippet(e, tokens) + "</p></li>";
    }).join("\n") || ("<li class='search-none'>" + esc(ui.nores) + "</li>");
  }

  var timer;
  input.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      var q = input.value.trim();
      try { history.replaceState(null, "", q ? "?q=" + encodeURIComponent(q) : location.pathname); } catch (e) {}
      search(q);
    }, 120);
  });
  if (allBox) allBox.addEventListener("change", function () { search(input.value.trim()); });

  if (chips && ui.topics) {
    chips.innerHTML = "<strong>" + esc(ui.popular) + ":</strong> " + ui.topics.map(function (t) {
      return '<button type="button" class="search-chip">' + esc(t) + "</button>";
    }).join(" ");
    chips.addEventListener("click", function (ev) {
      if (ev.target.classList.contains("search-chip")) {
        input.value = ev.target.textContent;
        input.focus();
        search(input.value);
      }
    });
  }

  if (audBar && ui.aud) {
    audBar.innerHTML = "<strong>" + esc(ui.audH || "") + "</strong> " +
      '<button type="button" class="search-aud-btn on" data-a="">' + esc(ui.audAll || "All") + "</button> " +
      AUD_KEYS.map(function (k) { return '<button type="button" class="search-aud-btn" data-a="' + k + '">' + esc(ui.aud[k] || k) + "</button>"; }).join(" ");
    audBar.addEventListener("click", function (ev) {
      var b = ev.target.closest ? ev.target.closest(".search-aud-btn") : null;
      if (!b) return;
      audSel = b.getAttribute("data-a") || null;
      Array.prototype.forEach.call(audBar.querySelectorAll(".search-aud-btn"), function (x) { x.classList.toggle("on", x === b); });
      search(input.value.trim());
    });
  }

  var pre = new URLSearchParams(location.search).get("q") || "";
  if (pre) { input.value = pre; }
  input.focus();
  if (pre) search(pre);
})();
