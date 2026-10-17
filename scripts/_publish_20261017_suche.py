#!/usr/bin/env python3
"""Article search pages (4 languages) over assets/search-index.js + assets/search.js."""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SLUG = {"de": "suche.html", "en": "search.html", "fr": "recherche.html", "it": "ricerca.html"}

L = {
"de": dict(
 title="Artikel-Suche: alle Steuer-Ratgeber auf einen Schlag",
 desc="Suche über alle Steuer-Artikel von steuerberatung.ch: Fristen, Abzüge, MWST, AHV, 3a, Quellensteuer und mehr – kostenlos, schnell, auf Deutsch, Französisch, Italienisch und Englisch.",
 h1="Artikel-Suche", sub="Alle Ratgeber-Artikel durchsuchen – Fristen, Abzüge, neue Gesetzesänderungen. Geben Sie ein Stichwort ein, die Ergebnisse erscheinen sofort.",
 ph="Stichwort eingeben, z. B. 3a, Frist, Quellensteuer…", results="Ergebnisse", singular="Ergebnis", nores="Keine Treffer – versuchen Sie ein kürzeres Stichwort oder alle Sprachen.",
 all="auch in anderen Sprachen", popular="Beliebte Themen",
 topics=["3a","Eigenmietwert","Quellensteuer","MWST","AHV","Fristen","Verrechnungssteuer"],
),
"en": dict(
 title="Article search: every tax guide on steuerberatung.ch",
 desc="Search all tax articles on steuerberatung.ch: deadlines, deductions, VAT, AHV, pillar 3a, withholding tax and more – free, fast, in German, French, Italian and English.",
 h1="Article search", sub="Search every guide – deadlines, deductions, new law changes. Type a keyword, results appear instantly.",
 ph="Type a keyword, e.g. 3a, deadline, withholding…", results="results", singular="result", nores="No matches – try a shorter keyword or search all languages.",
 all="also in other languages", popular="Popular topics",
 topics=["pillar 3a","imputed rent","withholding tax","VAT","AHV","deadlines","stamp duty"],
),
"fr": dict(
 title="Recherche d'articles : tous les guides fiscaux",
 desc="Recherchez tous les articles fiscaux de steuerberatung.ch : délais, déductions, TVA, AVS, pilier 3a, impôt à la source – gratuit, rapide, en allemand, français, italien et anglais.",
 h1="Recherche d'articles", sub="Recherchez tous les guides – délais, déductions, nouvelles modifications légales. Saisissez un mot-clé, les résultats s'affichent immédiatement.",
 ph="Mot-clé, p. ex. 3a, délai, impôt à la source…", results="résultats", singular="résultat", nores="Aucun résultat – essayez un mot-clé plus court ou toutes les langues.",
 all="aussi dans les autres langues", popular="Sujets populaires",
 topics=["pilier 3a","valeur locative","impôt à la source","TVA","AVS","délais","impôt anticipé"],
),
"it": dict(
 title="Ricerca articoli: tutte le guide fiscali",
 desc="Cercate in tutti gli articoli fiscali di steuerberatung.ch: termini, deduzioni, IVA, AVS, pilastro 3a, imposta alla fonte – gratuito, rapido, in tedesco, francese, italiano e inglese.",
 h1="Ricerca articoli", sub="Cercate in tutte le guide – termini, deduzioni, nuove modifiche legislative. Inserite una parola chiave, i risultati appaiono subito.",
 ph="Parola chiave, ad es. 3a, termine, imposta alla fonte…", results="risultati", singular="risultato", nores="Nessun risultato – provate una parola chiave più corta o tutte le lingue.",
 all="anche in altre lingue", popular="Temi popolari",
 topics=["pilastro 3a","valore locativo","imposta alla fonte","IVA","AVS","termini","imposta preventiva"],
),
}

NAV = {
 "de": [("leistungen.html","Leistungen"),("werbung.html","Werbung"),("ratgeber.html","Ratgeber"),("rechner.html","Rechner"),("suche.html","Suche")],
 "en": [("leistungen.html","Services"),("werbung.html","Advertise"),("ratgeber.html","Guides"),("rechner.html","Calculator"),("search.html","Search")],
 "fr": [("leistungen.html","Prestations"),("werbung.html","Publicité"),("ratgeber.html","Guides"),("rechner.html","Calculateur"),("recherche.html","Recherche")],
 "it": [("leistungen.html","Prestazioni"),("werbung.html","Pubblicità"),("ratgeber.html","Guide"),("rechner.html","Calcolatore"),("ricerca.html","Ricerca")],
}
FOOT = {
 "de": dict(about="Ihr unabhängiger Partner für Steuern in der Schweiz. Vergleich, Beratung und digitale Services – transparent und datenschutzkonform.", services=[("leistungen.html","Steuererklärung"),("leistungen.html","Steuerberatung"),("ratgeber.html","Ratgeber")], legal=[("impressum.html","Impressum"),("datenschutz.html","Datenschutz"),("agb.html","AGB")], contact=[("kontakt.html","Beratung anfragen")], hs="Services", hl="Rechtliches", hc="Kontakt", bottom="© 2026 steuerberatung.ch · Unabhängige Steuer-Information &amp; Vermittlung. Keine Steuerberatung im Sinne des DBG – die eigentliche Beratung erfolgt durch lizenzierte Partner."),
 "en": dict(about="Your independent partner for taxes in Switzerland. Comparison, advice and digital services – transparent and privacy-compliant.", services=[("leistungen.html","Tax return"),("leistungen.html","Tax advice"),("ratgeber.html","Guides")], legal=[("impressum.html","Imprint"),("datenschutz.html","Privacy"),("agb.html","Terms")], contact=[("kontakt.html","Request advice")], hs="Services", hl="Legal", hc="Contact", bottom="© 2026 steuerberatung.ch · Independent tax information &amp; partner mediation. No tax advice within the meaning of the Swiss Federal Direct Tax Act (FATA) – advice is provided exclusively by licensed partners."),
 "fr": dict(about="Votre partenaire indépendant pour les impôts en Suisse. Comparaison, conseil et services numériques – transparent et conforme à la protection des données.", services=[("leistungen.html","Déclaration d'impôts"),("leistungen.html","Conseil fiscal"),("ratgeber.html","Guides")], legal=[("impressum.html","Mentions légales"),("datenschutz.html","Protection des données"),("agb.html","CG")], contact=[("kontakt.html","Demander un conseil")], hs="Prestations", hl="Mentions", hc="Contact", bottom="© 2026 steuerberatung.ch · Information fiscale indépendante &amp; médiation. Aucun conseil fiscal au sens de la LIFD – le conseil est fourni exclusivement par des partenaires agréés."),
 "it": dict(about="Il vostro partner indipendente per le imposte in Svizzera. Confronto, consulenza e servizi digitali – trasparente e conforme alla protezione dei dati.", services=[("leistungen.html","Dichiarazione d'imposte"),("leistungen.html","Consulenza fiscale"),("ratgeber.html","Guide")], legal=[("impressum.html","Colophon"),("datenschutz.html","Protezione dei dati"),("agb.html","CG")], contact=[("kontakt.html","Richiedere consulenza")], hs="Prestazioni", hl="Note legali", hc="Contatto", bottom="© 2026 steuerberatung.ch · Informazione fiscale indipendente &amp; mediazione. Nessuna consulenza fiscale ai sensi della LIFD – la consulenza è fornita esclusivamente da partner autorizzati."),
}
HL = {"de":"de-CH","en":"en","fr":"fr-CH","it":"it-CH"}
HTMLEN = {"de":"de","en":"en","fr":"fr-CH","it":"it-CH"}

def page(lang):
    d = L[lang]; up = "" if lang == "de" else "../"
    alts = "\n".join('<link rel="alternate" hreflang="%s" href="https://steuerberatung.ch/%s">' % (HL[l], SLUG[l] if l=="de" else l+"/"+SLUG[l]) for l in ["de","en","fr","it"]) + '\n<link rel="alternate" hreflang="x-default" href="https://steuerberatung.ch/suche.html">'
    nav = "\n".join('      <a href="%s">%s</a>' % (p, t) for p, t in NAV[lang])
    sw = "\n".join('<a href="%sindex.html" class="lang%s"%s>%s</a>' % (
        ("" if l=="de" else ("../" if lang!="de" else "")) if l=="de" else ("../%s/" % l if lang!="de" else "%s/" % l),
        " active" if l==lang else "", ' aria-current="true"' if l==lang else "", l.upper()) for l in ["de","en","fr","it"])
    f = FOOT[lang]
    fs = " ".join('<a href="%s">%s</a>' % (p, t) for p, t in f["services"])
    fl = " ".join('<a href="%s">%s</a>' % (p, t) for p, t in f["legal"])
    fc = " ".join('<a href="%s">%s</a>' % (p, t) for p, t in f["contact"])
    ui = dict(results=d["results"], singular=d["singular"], nores=d["nores"], popular=d["popular"], topics=d["topics"])
    html = f"""<!DOCTYPE html>
<html lang="{HTMLEN[lang]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d['title']} | steuerberatung.ch</title>
<meta name="description" content="{d['desc']}">
<link rel="icon" type="image/png" sizes="32x32" href="{up}assets/favicon-32.png">
<link rel="canonical" href="https://steuerberatung.ch/{SLUG[lang] if lang=='de' else lang+'/'+SLUG[lang]}">
{alts}
<meta property="og:title" content="{d['title']}">
<meta property="og:description" content="{d['desc']}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="{up}assets/style.css">
<link rel="stylesheet" href="{up}assets/extra.css?v=4">
<link rel="stylesheet" href="{up}assets/redesign.css">
</head>
<body>
<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="index.html"><img class="logo-img" src="{up}assets/logo.svg" alt="" width="32" height="32" aria-hidden="true"><span class="logo-text">steuerberatung<span class="accent">.ch</span></span></a>
    <button class="nav-toggle" type="button" aria-label="{d['h1']}" aria-expanded="false" aria-controls="main-nav">☰</button>
    <nav class="main-nav" id="main-nav">
{nav}
{sw}
    </nav>
  </div>
</header>
<main>
<div class="page-head">
  <div class="container">
    <h1>{d['h1']}</h1>
    <p>{d['sub']}</p>
  </div>
</div>
<div class="container">
<section class="section">
  <div class="search-box">
    <input type="search" id="search-q" placeholder="{d['ph']}" autocomplete="off" aria-label="{d['h1']}">
    <label class="search-all"><input type="checkbox" id="search-all"> {d['all']}</label>
  </div>
  <p id="search-count" class="search-count" role="status" aria-live="polite"></p>
  <div id="search-chips" class="search-chips"></div>
  <ul id="search-results" class="search-results"></ul>
</section>
</div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div><img class="logo-img" src="{up}assets/logo.svg" alt="" width="28" height="28"><p>{f['about']}</p></div>
    <div><h3>{f['hs']}</h3><p>{fs}</p></div>
    <div><h3>{f['hl']}</h3><p>{fl}</p></div>
    <div><h3>{f['hc']}</h3><p>{fc}</p></div>
  </div>
  <div class="container footer-bottom"><p>{f['bottom']}</p></div>
</footer>
<script>window.SEARCH_UI={json.dumps(ui, ensure_ascii=False)};</script>
<script src="{up}assets/search-index.js?v=1" defer></script>
<script src="{up}assets/search.js?v=1" defer></script>
</body>
</html>
"""
    path = os.path.join(ROOT, SLUG[lang] if lang == "de" else lang + "/" + SLUG[lang])
    open(path, "w").write(html)
    print("wrote", path, len(html))

for lang in ["de", "en", "fr", "it"]:
    page(lang)
