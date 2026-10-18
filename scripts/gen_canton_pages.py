#!/usr/bin/env python3
"""Generate 26 canton hub pages x 4 languages from data/cantons_raw.json.
Path: /kanton/<slug>.html (+ en/ fr/ it/). Requires: python3 scripts/gen_canton_pages.py"""
import json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://steuerberatung.ch"
raw = json.load(open(os.path.join(ROOT, "data/cantons_raw.json"), encoding="utf-8"))
by_canton = {r["canton"]: r for r in raw}

# slug + localized display names (official exonyms)
CANTONS = [
 ("ZH","zuerich","Zürich","Zurich","Zurich","Zurigo"),
 ("BE","bern","Bern","Berne","Bern","Berna"),
 ("LU","luzern","Luzern","Lucerne","Lucerne","Lucerna"),
 ("UR","uri","Uri","Uri","Uri","Uri"),
 ("SZ","schwyz","Schwyz","Schwyz","Schwyz","Svitto"),
 ("OW","obwalden","Obwalden","Obwald","Obwald","Obvaldo"),
 ("NW","nidwalden","Nidwalden","Nidwald","Nidwald","Nidvaldo"),
 ("GL","glarus","Glarus","Glarus","Glaris","Glarona"),
 ("ZG","zug","Zug","Zug","Zoug","Zugo"),
 ("FR","freiburg","Freiburg","Fribourg","Fribourg","Friburgo"),
 ("SO","solothurn","Solothurn","Soleure","Soletta","Soletta"),
 ("BS","basel-stadt","Basel-Stadt","Basel City","Bâle-Ville","Basilea Città"),
 ("BL","basel-landschaft","Basel-Landschaft","Basel Country","Bâle-Campagne","Basilea Campagna"),
 ("SH","schaffhausen","Schaffhausen","Schaffhausen","Schaffhouse","Sciaffusa"),
 ("AR","appenzell-aurrhoden","Appenzell A.Rh.","Appenzell Outer Rhodes","Appenzell Rhodes-Extérieures","Appenzello Esterno"),
 ("AI","appenzell-innerrhoden","Appenzell I.Rh.","Appenzell Inner Rhodes","Appenzell Rhodes-Intérieures","Appenzello Interno"),
 ("SG","st-gallen","St. Gallen","St. Gallen","Saint-Gall","San Gallo"),
 ("GR","graubuenden","Graubünden","Grisons","Grisons","Grigioni"),
 ("AG","aargau","Aargau","Aargau","Argovie","Argovia"),
 ("TG","thurgau","Thurgau","Thurgau","Thurgovie","Turgovia"),
 ("TI","tessin","Tessin","Ticino","Tessin","Ticino"),
 ("VD","waadt","Waadt","Vaud","Vaud","Vaud"),
 ("VS","wallis","Wallis","Valais","Valais","Vallese"),
 ("NE","neuenburg","Neuenburg","Neuchâtel","Neuchâtel","Neuchâtel"),
 ("GE","genf","Genf","Geneva","Genève","Ginevra"),
 ("JU","jura","Jura","Jura","Jura","Giura"),
]

UI = {
"de": dict(ttl="Steuererklärung Kanton {n} {y}: Fristen, Steuerfuss & Online-Tool",
 dsc="Steuererklärung {n} {y}: Abgabefrist, durchschnittlicher Steuerfuss, offizielles Online-Tool ({sw}) und kantonale Besonderheiten für Privatpersonen und Selbstständige.",
 h1="Kanton {n}", sub="Steuererklärung {y}: Fristen, Steuerfuss, offizielles Tool und Besonderheiten – kurz und amtlich belegt.",
 frist="Abgabefrist Steuerperiode {y}", fuss="Durchschnittlicher Steuerfuss (natürliche Personen)",
 tool="Online-Steuererklärung", amt="Kantonales Steueramt", spec="Besonderheiten",
 cmp_h="Steuerfüsse im Vergleich", cmp_intro="Der durchschnittliche Steuerfuss (Kanton + Gemeinden, Ehepaar ohne Kinder, ohne Kirchensteuer, Nettoabgabe) laut ESTV per 1.1.2026:",
 cmp_col1="Kanton", cmp_col2="Steuerfuss", back="Alle Kantone", cta="Steuererklärung im Kanton {n}Professionell machen lassen? Geprüfte Fachperson im Kanton {n} finden",
 more_h="Ratgeber-Artikel", ld_type="Steuererklärung {n}"),
"en": dict(ttl="Tax return canton {n} {y}: deadlines, tax multiplier & online tool",
 dsc="Tax return {n} {y}: filing deadline, average tax multiplier, official online tool ({sw}) and canton-specific facts for individuals and the self-employed.",
 h1="Canton {n}", sub="Tax return {y}: deadlines, tax multiplier, official tool and cantonal specifics – concise and sourced to official pages.",
 frist="Deadline tax period {y}", fuss="Average tax multiplier (natural persons)",
 tool="Online tax return", amt="Cantonal tax administration", spec="Cantonal specifics",
 cmp_h="Tax multipliers compared", cmp_intro="Average tax multiplier (canton + communes, married couple without children, no church tax, net tax) per FTA as of 1 Jan 2026:",
 cmp_col1="Canton", cmp_col2="Multiplier", back="All cantons", cta="Have your {n} tax return done professionally? Find a vetted specialist in {n}",
 more_h="Related guides", ld_type="Tax return {n}"),
"fr": dict(ttl="Déclaration d'impôts canton {n} {y}: délais, multiplicateur & outil en ligne",
 dsc="Déclaration d'impôts {n} {y}: délai de dépôt, multiplicateur d'impôt moyen, outil officiel en ligne ({sw}) et particularités cantonales pour personnes physiques et indépendants.",
 h1="Canton {n}", sub="Déclaration d'impôts {y}: délais, multiplicateur, outil officiel et particularités cantonales – concis et sourcé aux pages officielles.",
 frist="Délai période fiscale {y}", fuss="Multiplicateur moyen (personnes physiques)",
 tool="Déclaration en ligne", amt="Administration fiscale cantonale", spec="Particularités cantonales",
 cmp_h="Multiplicateurs comparés", cmp_intro="Multiplicateur moyen (canton + communes, couple marié sans enfants, sans impôt ecclésiastique, perception nette) selon l'AFC au 1er janvier 2026:",
 cmp_col1="Canton", cmp_col2="Multiplicateur", back="Tous les cantons", cta="Faire établir votre déclaration {n} par un spécialiste vérifié",
 more_h="Guides liés", ld_type="Déclaration d'impôts {n}"),
"it": dict(ttl="Dichiarazione d'imposte canton {n} {y}: termini, moltiplicatore & tool online",
 dsc="Dichiarazione d'imposte {n} {y}: termine di consegna, moltiplicatore medio, tool ufficiale online ({sw}) e particolarità cantonali per persone fisiche e indipendenti.",
 h1="Cantone {n}", sub="Dichiarazione d'imposte {y}: termini, moltiplicatore, tool ufficiale e particolarità cantonali – conciso e con fonti ufficiali.",
 frist="Termine periodo fiscale {y}", fuss="Moltiplicatore medio (persone fisiche)",
 tool="Dichiarazione online", amt="Amministrazione cantonale delle imposte", spec="Particolarità cantonali",
 cmp_h="Moltiplicatori a confronto", cmp_intro="Moltiplicatore medio (cantone + comuni, coppia sposata senza figli, senza imposta ecclesiastica, gettito netto) secondo l'AFC al 1.1.2026:",
 cmp_col1="Cantone", cmp_col2="Moltiplicatore", back="Tutti i cantoni", cta="Far compilare la vostra dichiarazione {n} da uno specialista verificato",
 more_h="Guide correlate", ld_type="Dichiarazione d'imposte {n}"),
}

NAV = {
 "de": [("leistungen.html","Leistungen"),("werbung.html","Werbung"),("ratgeber.html","Ratgeber"),("rechner.html","Rechner"),("suche.html","Suche")],
 "en": [("leistungen.html","Services"),("werbung.html","Advertise"),("ratgeber.html","Guides"),("rechner.html","Calculator"),("search.html","Search")],
 "fr": [("leistungen.html","Prestations"),("werbung.html","Publicité"),("ratgeber.html","Guide fiscal"),("rechner.html","Calculateur"),("recherche.html","Recherche")],
 "it": [("leistungen.html","Prestazioni"),("werbung.html","Pubblicità"),("ratgeber.html","Guida fiscale"),("rechner.html","Calcolatore"),("ricerca.html","Ricerca")],
}
FOOT = {
 "de": dict(about="Ihr unabhängiger Partner für Steuern in der Schweiz. Steuer-Ratgeber, Rechner und Vermittlung geprüfter Fachpersonen – transparent und datenschutzkonform.", services=[("leistungen.html","Steuererklärung"),("leistungen.html","Steuerberatung"),("ratgeber.html","Ratgeber")], legal=[("impressum.html","Impressum"),("datenschutz.html","Datenschutz"),("agb.html","AGB")], contact=[("kontakt.html","Beratung anfragen")], hs="Services", hl="Rechtliches", hc="Kontakt", bottom="© 2026 steuerberatung.ch · Unabhängige Steuer-Information &amp; Vermittlung. steuerberatung.ch erbringt keine individuelle Steuer- oder Rechtsberatung. Die Beratung erfolgt ausschliesslich durch die vermittelten Fachpersonen."),
 "en": dict(about="Your independent partner for taxes in Switzerland. Tax guides, calculators and referral to vetted specialists – transparent and privacy-compliant.", services=[("leistungen.html","Tax return"),("leistungen.html","Tax advice"),("ratgeber.html","Guides")], legal=[("impressum.html","Imprint"),("datenschutz.html","Privacy"),("agb.html","Terms")], contact=[("kontakt.html","Request advice")], hs="Services", hl="Legal", hc="Contact", bottom="© 2026 steuerberatung.ch · Independent tax information &amp; partner mediation. steuerberatung.ch does not provide individual tax or legal advice. Advice is provided exclusively by the referred specialists."),
 "fr": dict(about="Votre partenaire indépendant pour les impôts en Suisse. Guides fiscaux, calculateurs et médiation de spécialistes vérifiés – en toute transparence et dans le respect de la protection des données.", services=[("leistungen.html","Déclaration d'impôts"),("leistungen.html","Conseil fiscal"),("ratgeber.html","Guides")], legal=[("impressum.html","Mentions légales"),("datenschutz.html","Protection des données"),("agb.html","CG")], contact=[("kontakt.html","Demander un conseil")], hs="Prestations", hl="Mentions", hc="Contact", bottom="© 2026 steuerberatung.ch · Information fiscale indépendante &amp; médiation. steuerberatung.ch ne fournit pas de conseil fiscal ou juridique individuel. Le conseil est fourni exclusivement par les spécialistes mandatés."),
 "it": dict(about="Il vostro partner indipendente per le imposte in Svizzera. Guide fiscali, calcolatori e mediazione di specialisti verificati – trasparente e conforme alla protezione dei dati.", services=[("leistungen.html","Dichiarazione d'imposte"),("leistungen.html","Consulenza fiscale"),("ratgeber.html","Guide")], legal=[("impressum.html","Colophon"),("datenschutz.html","Protezione dei dati"),("agb.html","CG")], contact=[("kontakt.html","Richiedere consulenza")], hs="Prestazioni", hl="Note legali", hc="Contatto", bottom="© 2026 steuerberatung.ch · Informazione fiscale indipendente &amp; mediazione. steuerberatung.ch non fornisce consulenza fiscale o giuridica individuale. La consulenza è fornita esclusivamente dagli specialisti incaricati."),
}
HL = {"de":"de-CH","en":"en","fr":"fr-CH","it":"it-CH"}
HTMLEN = {"de":"de","en":"en","fr":"fr-CH","it":"it-CH"}
MORE = {  # related articles per canton type: generic set (links exist in every lang dir)
 "de": [("steuer-checkliste-2026.html","Steuer-Checkliste 2026"),("erwerbsbedingter-umzug-kosten-abzug.html","Umzug wegen Job: Kosten abziehen"),("praemienverbilligung-2027-anmelden.html","Prämienverbilligung 2027 anmelden")],
 "en": [("steuer-checkliste-2026.html","Tax checklist 2026"),("erwerbsbedingter-umzug-kosten-abzug.html","Job-related moving costs"),("praemienverbilligung-2027-anmelden.html","Health insurance subsidy 2027")],
 "fr": [("steuer-checkliste-2026.html","Checklist déclaration 2026"),("erwerbsbedingter-umzug-kosten-abzug.html","Frais de déménagement liés au travail"),("praemienverbilligung-2027-anmelden.html","Réduction de primes 2027")],
 "it": [("steuer-checkliste-2026.html","Checklist dichiarazione 2026"),("erwerbsbedingter-umzug-kosten-abzug.html","Spese di trasloco per motivi di lavoro"),("praemienverbilligung-2027-anmelden.html","Riduzione dei premi 2027")],
}
YEAR = "2026"

def esc(s): return s.replace("&","&amp;").replace("<","&lt;")

def page(lang, code, slug, names, idx):
    r = by_canton.get(code)
    if not r:
        print("NO DATA for", code); return 0
    n = names[idx]  # 1=de 2=en 3=fr 4=it -> idx offset
    u = UI[lang]; up = "" if lang == "de" else "../"
    dpath = f"kanton/{slug}.html" if lang == "de" else f"{lang}/kanton/{slug}.html"
    canon = SITE + ("/kanton/" if lang == "de" else f"/{lang}/kanton/") + slug + ".html"
    alts = "\n".join('<link rel="alternate" hreflang="%s" href="%s/%s%s">' % (HL[l], SITE, "" if l=="de" else l+"/", dpath.split(l+"/",1)[1] if l!="de" else dpath) for l in ["de"])
    alts = "\n".join('<link rel="alternate" hreflang="%s" href="%s/%skanton/%s.html">' % (HL[l], SITE, "" if l=="de" else l+"/", slug) for l in ["de","en","fr","it"]) + '\n<link rel="alternate" hreflang="x-default" href="%s/kanton/%s.html">' % (SITE, slug)
    nav = "\n".join('      <a href="%s%s">%s</a>' % (up, p, t) for p, t in NAV[lang])
    sw = "\n".join('<a href="%s" class="lang%s"%s>%s</a>' % (
        ("index.html" if l=="de" else l+"/index.html") if lang=="de" else ("../index.html" if l=="de" else "../%s/index.html" % l),
        " active" if l==lang else "", ' aria-current="true"' if l==lang else "", l.upper()) for l in ["de","en","fr","it"])
    f = FOOT[lang]
    fs = " ".join('<a href="%s%s">%s</a>' % (up, p, t) for p, t in f["services"])
    fl = " ".join('<a href="%s%s">%s</a>' % (up, p, t) for p, t in f["legal"])
    fc = " ".join('<a href="%s%s">%s</a>' % (up, p, t) for p, t in f["contact"])
    fuss = r.get("steuerfuss_2026") or "–"
    frist = r.get("abgabefrist_2026") or "–"
    sw_name = r.get("e_tax_software") or "–"
    sw_url = r.get("e_tax_url") or r.get("steueramt_url") or "#"
    amt_url = r.get("steueramt_url") or "#"
    bem = r.get("bemerkungen") or ""
    # comparison table (all 26, sorted by multiplier numeric)
    def num(x):
        try: return float(str(x).replace("%","").replace(",",".").strip())
        except Exception: return 999
    rows = sorted(CANTONS, key=lambda c: num(by_canton.get(c[0],{}).get("steuerfuss_2026","999")))
    cmp_rows = "".join(
        '<tr%s><td><a href="%skanton/%s.html">%s</a></td><td>%s</td></tr>' % (
        ' class="cmp-here"' if c[0]==code else "", up, c[1], c[idx], by_canton.get(c[0],{}).get("steuerfuss_2026","–")) for c in rows)
    more = "\n".join('<li><a href="%s%s">%s</a></li>' % (up, s, t) for s, t in MORE[lang])
    cta_lbl = u["cta"].replace("{n}", n)
    ld = json.dumps([
      {"@context":SITE and "https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":{"de":"Start","en":"Home","fr":"Accueil","it":"Home"}[lang],"item":SITE+("/" if lang=="de" else "/%s/"%lang)},
        {"@type":"ListItem","position":2,"name":u["back"],"item":SITE+("/kanton/zh.html" if lang=="de" else "/%s/kanton/zh.html"%lang)},
        {"@type":"ListItem","position":3,"name":n,"item":canon}]},
      {"@context":"https://schema.org","@type":"WebPage","name":u["ld_type"].format(n=n),"description":u["dsc"].format(n=n,y=YEAR,sw=sw_name),"url":canon,"inLanguage":HL[lang]}], ensure_ascii=False)
    html = f"""<!DOCTYPE html>
<html lang="{HTMLEN[lang]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{u['ttl'].format(n=n,y=YEAR)} | steuerberatung.ch</title>
<meta name="description" content="{u['dsc'].format(n=n,y=YEAR,sw=sw_name)}">
<link rel="icon" type="image/png" sizes="32x32" href="{up}assets/favicon-32.png">
<link rel="canonical" href="{canon}">
{alts}
<meta property="og:title" content="{u['ttl'].format(n=n,y=YEAR)}">
<meta property="og:description" content="{u['dsc'].format(n=n,y=YEAR,sw=sw_name)}">
<meta property="og:type" content="article">
<link rel="stylesheet" href="{up}assets/style.css">
<link rel="stylesheet" href="{up}assets/extra.css?v=4">
<link rel="stylesheet" href="{up}assets/redesign.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="index.html"><img class="logo-img" src="{up}assets/logo.svg" alt="" width="32" height="32" aria-hidden="true"><span class="logo-text">steuerberatung<span class="accent">.ch</span></span></a>
    <button class="nav-toggle" type="button" aria-label="Menü" aria-expanded="false" aria-controls="main-nav">☰</button>
    <nav class="main-nav" id="main-nav">
{nav}
{sw}
    </nav>
  </div>
</header>
<main>
<div class="page-head">
  <div class="container">
    <h1>{u['h1'].format(n=n)}</h1>
    <p>{u['sub'].format(y=YEAR)}</p>
  </div>
</div>
<section class="section"><div class="container prose">
<div class="canton-facts">
  <div><h3>{u['frist']}</h3><p>{esc(frist)}</p></div>
  <div><h3>{u['fuss']}</h3><p>{esc(fuss)}</p></div>
  <div><h3>{u['tool']}</h3><p><a href="{sw_url}" rel="noopener">{esc(sw_name)} →</a></p></div>
  <div><h3>{u['amt']}</h3><p><a href="{amt_url}" rel="noopener">{u['amt']} {n} →</a></p></div>
</div>
<h2>{u['spec']}</h2>
<p>{esc(bem)}</p>
<div class="cta-mid"><a href="kontakt.html">{cta_lbl} →</a></div>
<h2 id="cmp">{u['cmp_h']}</h2>
<p>{u['cmp_intro']}</p>
<table><thead><tr><th>{u['cmp_col1']}</th><th>{u['cmp_col2']}</th></tr></thead><tbody>{cmp_rows}</tbody></table>
<p><em>Quelle: <a href="https://www.estv2.admin.ch/stp/ds/e-steuersatz-steuerfuss-de.pdf" rel="noopener">ESTV – Steuersatz und Steuerfuss (PDF, Stand 1.1.2026)</a>. Durchschnittswerte; Ihre Gemeinde weicht ab – konkret rechnet der <a href="{up}rechner.html">Steuerrechner</a>.</em></p>
<h2>{u['more_h']}</h2>
<ul>{more}</ul>
</div></section>
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
</body>
</html>
"""
    outdir = os.path.join(ROOT, "kanton" if lang == "de" else lang + "/kanton")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, slug + ".html"), "w").write(html)
    return len(html)

count = 0
for lang, idx in [("de",1),("en",2),("fr",3),("it",4)]:
    for code, slug, *names in CANTONS:
        if page(lang, code, slug, names, idx): count += 1
print("canton pages written:", count)
