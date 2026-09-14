/* First-party analytics — no cookies beyond our own sid, no third parties. DSG-compliant. */
(function () {
  try {
    var sid = (function () {
      var m = document.cookie.match(/(?:^|; )sid=([^;]+)/);
      if (m) return m[1];
      var id = "s" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
      document.cookie = "sid=" + id + ";path=/;max-age=31536000;samesite=lax";
      return id;
    })();
    var page = location.pathname;
    var ref = document.referrer || "";
    var img = new Image();
    img.src = (window.LEAD_ENDPOINT || "https://pixels-urw-mobility-ladder.trycloudflare.com") +
      "/track?p=" + encodeURIComponent(page) +
      "&r=" + encodeURIComponent(ref) +
      "&sid=" + encodeURIComponent(sid);
    img.referrerPolicy = "no-referrer";
  } catch (e) { /* never break the page */ }
})();
