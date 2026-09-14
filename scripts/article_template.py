#!/usr/bin/env python3
"""Build a Ratgeber article page. Usage:
python3 article_template.py <slug> <title> <meta_desc> <h2|body_html>...
Pairs of (h2, body_html) after the first 3 args. Writes <slug>.html.
"""
import sys, os, json, datetime
BASE = "/Users/pino/Code/steuerberatung.ch"
SITE = "https://steuerberatung.ch"
HEADER = """<header class="site-header">
<div class="container header-inner">
<a class="logo" href="index.html"><span class="logo-mark">S</span> steuerberatung<span class="accent">.ch</span></a>
<nav class="main-nav">
<a href="leistungen.html">Leistungen</a>
<a href="preise.html">Preise</a>
<a href="ratgeber.html">Ratgeber</a>
<a href="rechner.html">Rechner</a>
<a href="en/index.html" class="lang">EN</a>
</nav>
<a class="btn btn-primary" href="kontakt.html">Kostenlose Beratung</a>
</div>
</header>
"""
FOOTER = """<footer class="site-footer">
<div class="container footer-grid">
<div>
<div class="logo"><span class="logo-mark">S</span> steuerberatung<span class="accent">.ch</span></div>
<p class="muted">Ihr unabhängiger Partner für Steuern in der Schweiz. Vergleich, Beratung und digitale Services – transparent und datenschutzkonform.</p>
</div>
<div>
<h4>Services</h4>
<a href="leistungen.html">Steuererklärung</a>
<a href="leistungen.html">Steuerberatung</a>
<a href="rechner.html">Steuerrechner</a>
<a href="ratgeber.html">Ratgeber</a>
</div>
<div>
<h4>Rechtliches</h4>
<a href="impressum.html">Impressum</a>
<a href="datenschutz.html">Datenschutz</a>
<a href="agb.html">AGB</a>
</div>
<div>
<h4>Kontakt</h4>
<a href="kontakt.html">Beratung anfragen</a>
<a href="mailto:info@steuerberatung.ch">info@steuerberatung.ch</a>
</div>
</div>
<div class="container footer-bottom">
<p class="muted">© 2026 steuerberatung.ch · Unabhängige Steuer-Information &amp; Vermittlung. Keine Steuerberatung im Sinne des DBG – die eigentliche Beratung erfolgt durch lizenzierte Partner.</p>
</div>
</footer>
"""
CTA = """<section class="section cta-band">
<div class="container">
<h2>Unsicher bei Ihrer Steuererklärung?</h2>
<p class="muted">Kostenlose Erstberatung: Wir prüfen Ihre Situation und vermitteln einen geprüften Partner in Ihrem Kanton.</p>
<a class="btn btn-primary btn-lg" href="kontakt.html">Jetzt kostenlos anfragen</a>
</div>
</section>
"""
def build(slug, title, meta, sections):
    today = datetime.date.today().isoformat()
    toc = "".join(f'<li><a href="#s{i+1}">{h}</a></li>' for i,(h,b) in enumerate(sections))
    body = "".join(f'<section class="section"><div class="container prose"><h2 id="s{i+1}">{h}</h2>{b}</div></section>' for i,(h,b) in enumerate(sections))
    ld = {"@context":"https://schema.org","@type":"Article","headline":title,"datePublished":today,"author":{"@type":"Organization","name":"steuerberatung.ch"},"publisher":{"@type":"Organization","name":"steuerberatung.ch"},"description":meta}
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | steuerberatung.ch</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{SITE}/{slug}.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE}/{slug}.html">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/extra.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{HEADER}
<main>
<div class="page-head"><div class="container">
<h1>{title}</h1>
<p>Veröffentlicht am {today} · Unabhängige Steuer-Information für die Schweiz.</p>
</div></div>
<nav class="toc"><div class="container"><strong>Inhalt:</strong><ol>{toc}</ol></div></nav>
{body}
{CTA}
</main>
{FOOTER}
<script src="assets/endpoint.js"></script>
<script src="assets/track.js"></script>
<script src="assets/app.js"></script>
</body>
</html>
"""
    open(os.path.join(BASE, slug + ".html"), "w").write(html)
    print("wrote", slug + ".html", len(html), "bytes")
if __name__ == "__main__":
    a = sys.argv[1:]
    slug, title, meta = a[0], a[1], a[2]
    secs = [(a[i], a[i+1]) for i in range(3, len(a), 2)]
    build(slug, title, meta, secs)
