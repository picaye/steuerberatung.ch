#!/usr/bin/env python3
"""Build a Ratgeber article page in one of 4 languages.

Usage:
  python3 article_template.py <lang> <slug> <title> <meta_desc> <h2|body_html>...

  lang: de | en | fr | it   (de writes to repo root, others to <lang>/ subdir)
  Pairs of (h2, body_html) after the first 4 args. Writes <slug>.html.

Emits: 4-way lang switcher, 5 hreflang alternates, localized chrome
(header/nav/footer/CTA/date label), correct canonical + og:url.
"""
import sys, os, json, datetime, html as htmllib

BASE = "/Users/pino/Code/steuerberatung.ch"
SITE = "https://steuerberatung.ch"

LANGS = ["de", "en", "fr", "it"]
HTML_LANG = {"de": "de", "en": "en", "fr": "fr-CH", "it": "it-CH"}
HREFLANG = {"de": "de-CH", "en": "en", "fr": "fr-CH", "it": "it-CH"}

L = {
    "de": dict(
        nav=[("leistungen.html", "Leistungen"), ("werbung.html", "Werbung"),
             ("ratgeber.html", "Ratgeber")],
        cta_btn="Kostenlose Beratung", menu="Menü",
        foot_about="Ihr unabhängiger Partner für Steuern in der Schweiz. Vergleich, Beratung und digitale Services – transparent und datenschutzkonform.",
        foot_services=[("leistungen.html", "Steuererklärung"), ("leistungen.html", "Steuerberatung"),
                       ("ratgeber.html", "Ratgeber")],
        foot_legal=[("impressum.html", "Impressum"), ("datenschutz.html", "Datenschutz"), ("agb.html", "AGB")],
        foot_contact=[("kontakt.html", "Beratung anfragen")],
        h_services="Services", h_legal="Rechtliches", h_contact="Kontakt",
        foot_bottom="© 2026 steuerberatung.ch · Unabhängige Steuer-Information &amp; Vermittlung. Keine Steuerberatung im Sinne des DBG – die eigentliche Beratung erfolgt durch lizenzierte Partner.",
        cta_h="Unsicher bei Ihrer Steuererklärung?",
        cta_p="Kostenlose Erstberatung: Wir prüfen Ihre Situation und vermitteln einen geprüften Partner in Ihrem Kanton.",
        cta_btn2="Jetzt kostenlos anfragen",
        published="Veröffentlicht am {date} · Unabhängige Steuer-Information für die Schweiz.",
        toc="Inhalt:",
    ),
    "en": dict(
        nav=[("leistungen.html", "Services"), ("werbung.html", "Advertise"),
             ("ratgeber.html", "Guides")],
        cta_btn="Free advice", menu="Menu",
        foot_about="Your independent partner for taxes in Switzerland. Comparison, advice and digital services – transparent and privacy-compliant.",
        foot_services=[("leistungen.html", "Tax return"), ("leistungen.html", "Tax advice"),
                       ("ratgeber.html", "Guides")],
        foot_legal=[("impressum.html", "Imprint"), ("datenschutz.html", "Privacy"), ("agb.html", "Terms")],
        foot_contact=[("kontakt.html", "Request advice")],
        h_services="Services", h_legal="Legal", h_contact="Contact",
        foot_bottom="© 2026 steuerberatung.ch · Independent tax information &amp; partner mediation. No tax advice within the meaning of the Swiss Federal Direct Tax Act (FATA) – advice is provided exclusively by licensed partners.",
        cta_h="Not sure about your tax return?",
        cta_p="Free initial consultation: we review your situation and match you with a vetted partner in your canton.",
        cta_btn2="Request free advice",
        published="Published on {date} · Independent tax information for Switzerland.",
        toc="Contents:",
    ),
    "fr": dict(
        nav=[("leistungen.html", "Prestations"), ("werbung.html", "Publicité"),
             ("ratgeber.html", "Guide fiscal")],
        cta_btn="Conseil gratuit", menu="Menu",
        foot_about="Votre partenaire indépendant pour les impôts en Suisse. Comparaison, conseil et services numériques – transparent et conforme à la protection des données.",
        foot_services=[("leistungen.html", "Déclaration d'impôt"), ("leistungen.html", "Conseil fiscal"),
                       ("ratgeber.html", "Guide fiscal")],
        foot_legal=[("impressum.html", "Mentions légales"), ("datenschutz.html", "Protection des données"), ("agb.html", "CGV")],
        foot_contact=[("kontakt.html", "Demander un conseil")],
        h_services="Services", h_legal="Mentions légales", h_contact="Contact",
        foot_bottom="© 2026 steuerberatung.ch · Information fiscale indépendante &amp; mise en relation. Aucun conseil fiscal au sens de la LIFD – le conseil est fourni exclusivement par des partenaires agréés.",
        cta_h="Incertain pour votre déclaration d'impôt ?",
        cta_p="Premier conseil gratuit : nous examinons votre situation et vous mettons en relation avec un partenaire vérifié dans votre canton.",
        cta_btn2="Demander un conseil gratuit",
        published="Publié le {date} · Information fiscale indépendante pour la Suisse.",
        toc="Sommaire :",
    ),
    "it": dict(
        nav=[("leistungen.html", "Servizi"), ("werbung.html", "Pubblicità"),
             ("ratgeber.html", "Guida fiscale")],
        cta_btn="Consulenza gratuita", menu="Menu",
        foot_about="Il vostro partner indipendente per le imposte in Svizzera. Confronto, consulenza e servizi digitali – trasparente e conforme alla protezione dei dati.",
        foot_services=[("leistungen.html", "Dichiarazione d'imposte"), ("leistungen.html", "Consulenza fiscale"),
                       ("ratgeber.html", "Guida fiscale")],
        foot_legal=[("impressum.html", "Impressum"), ("datenschutz.html", "Protezione dei dati"), ("agb.html", "CGV")],
        foot_contact=[("kontakt.html", "Richiedere consulenza")],
        h_services="Servizi", h_legal="Note legali", h_contact="Contatto",
        foot_bottom="© 2026 steuerberatung.ch · Informazione fiscale indipendente &amp; messa in relazione. Nessuna consulenza fiscale ai sensi della LIFD – la consulenza è fornita esclusivamente da partner autorizzati.",
        cta_h="Incerti sulla vostra dichiarazione d'imposte?",
        cta_p="Prima consulenza gratuita: esaminiamo la vostra situazione e vi mettiamo in contatto con un partner verificato nel vostro cantone.",
        cta_btn2="Richiedi consulenza gratuita",
        published="Pubblicato il {date} · Informazione fiscale indipendente per la Svizzera.",
        toc="Indice:",
    ),
}


def build(lang, slug, title, meta, sections):
    assert lang in LANGS, f"lang must be one of {LANGS}"
    t = L[lang]
    today = datetime.date.today().isoformat()
    pre = "" if lang == "de" else "../"          # asset/link prefix inside lang dir
    url_tail = f"{slug}.html"
    page_url = lambda l: (f"{SITE}/{url_tail}" if l == "de" else f"{SITE}/{l}/{url_tail}")

    # language switcher: same-dir index for current lang; DE root index is ../index.html
    sw = []
    for l in LANGS:
        if l == lang:
            href = "index.html"
        elif lang == "de":
            href = f"{l}/index.html"
        elif l == "de":
            href = "../index.html"
        else:
            href = f"../{l}/index.html"
        cls = 'class="lang active" aria-current="true"' if l == lang else 'class="lang"'
        sw.append(f'<a href="{href}" {cls}>{l.upper()}</a>')
    switcher = "\n".join(sw)

    nav_links = "\n".join(f'<a href="{pre if False else ""}{p}">{label}</a>' for p, label in t["nav"])
    # nav sibling links stay same-dir (articles live next to their language's pages)
    nav_links = "\n".join(f'<a href="{p}">{label}</a>' for p, label in t["nav"])

    header = f"""<header class="site-header">
<div class="container header-inner">
<a class="logo" href="{pre}index.html"><img class="logo-img" src="{pre}assets/logo.svg" alt="" width="32" height="32" aria-hidden="true"><span class="logo-text">steuerberatung<span class="accent">.ch</span></span></a>
<button class="nav-toggle" type="button" aria-label="{t['menu']}" aria-expanded="false" aria-controls="main-nav">☰</button>
<nav class="main-nav" id="main-nav">
{nav_links}
{switcher}
</nav>
</div>
</header>
"""
    footer = f"""<footer class="site-footer">
<div class="container footer-grid">
<div>
<div class="logo"><img class="logo-img" src="{pre}assets/logo.svg" alt="" width="32" height="32" aria-hidden="true"><span class="logo-text">steuerberatung<span class="accent">.ch</span></span></div>
<p class="muted">{t['foot_about']}</p>
</div>
<div>
<h4>{t['h_services']}</h4>
{chr(10).join(f'<a href="{p}">{label}</a>' for p, label in t['foot_services'])}
</div>
<div>
<h4>{t['h_legal']}</h4>
{chr(10).join(f'<a href="{p}">{label}</a>' for p, label in t['foot_legal'])}
</div>
<div>
<h4>{t['h_contact']}</h4>
{chr(10).join(f'<a href="{p}">{label}</a>' for p, label in t['foot_contact'])}
<a href="mailto:info@steuerberatung.ch">info@steuerberatung.ch</a>
</div>
</div>
<div class="container footer-bottom">
<p class="muted">{t['foot_bottom']}</p>
</div>
</footer>
"""
    cta = f"""<section class="section cta-band">
<div class="container">
<h2>{t['cta_h']}</h2>
<p class="muted">{t['cta_p']}</p>
<a class="btn btn-primary btn-lg" href="kontakt.html">{t['cta_btn2']}</a>
</div>
</section>
"""
    toc = "".join(f'<li><a href="#s{i+1}">{h}</a></li>' for i, (h, b) in enumerate(sections))
    body = "".join(
        f'<section class="section"><div class="container prose"><h2 id="s{i+1}">{h}</h2>{b}</div></section>'
        for i, (h, b) in enumerate(sections))

    ld = {"@context": "https://***", "@type": "Article", "headline": title,
          "datePublished": today,
          "author": {"@type": "Organization", "name": "steuerberatung.ch"},
          "publisher": {"@type": "Organization", "name": "steuerberatung.ch"},
          "description": meta,
          "inLanguage": HTML_LANG[lang]}
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{page_url(l)}">' for l in LANGS)
    alternates += f'\n<link rel="alternate" hreflang="x-default" href="{page_url("de")}">'

    canon = page_url(lang)
    html_doc = f"""<!DOCTYPE html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | steuerberatung.ch</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{canon}">
{alternates}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="steuerberatung.ch">
<link rel="icon" type="image/png" sizes="32x32" href="{pre}assets/favicon-32.png">
<link rel="apple-touch-icon" href="{pre}assets/logo-180.png">
<link rel="stylesheet" href="{pre}assets/style.css">
<link rel="stylesheet" href="{pre}assets/extra.css">
<link rel="stylesheet" href="{pre}assets/redesign.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{header}
<main>
<div class="page-head"><div class="container">
<h1>{title}</h1>
<p>{t['published'].format(date=today)}</p>
</div></div>
<nav class="toc"><div class="container"><strong>{t['toc']}</strong><ol>{toc}</ol></div></nav>
{body}
</main>
{footer}
<script src="{pre}assets/endpoint.js"></script>
<script src="{pre}assets/track.js"></script>
<script src="{pre}assets/app.js"></script>
</body>
</html>
"""
    outdir = BASE if lang == "de" else os.path.join(BASE, lang)
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, slug + ".html")
    open(outpath, "w").write(html_doc)
    print("wrote", os.path.relpath(outpath, BASE), len(html_doc), "bytes")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 4:
        print(__doc__)
        sys.exit(1)
    lang, slug, title, meta = a[0], a[1], a[2], a[3]
    secs = [(a[i], a[i + 1]) for i in range(4, len(a), 2)]
    build(lang, slug, title, meta, secs)
