#!/usr/bin/env python3
"""Partner-vetting page (4 languages) — makes 'geprüfte Partner' concrete."""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = "partner-pruefung.html"

L = {
"de": dict(
 title="So prüfen wir unsere Partner | steuerberatung.ch",
 desc="Klare Kriterien für geprüfte Steuerpartner: eidg. Diplom oder anerkannte Qualifikation, Mitgliedschaft bei Treuhand Suisse/EXPERTsuisse, Berufshaftpflicht, Sitz in der Schweiz und laufende Kontrolle.",
 h1="So prüfen wir unsere Partner",
 sub="„Geprüft“ ist bei uns kein Marketingwort. Jede vermittelte Fachperson erfüllt diese Kriterien und wird laufend kontrolliert.",
 crit_h="Pflichtkriterien",
 crit=[
  ("<strong>Anerkannte Qualifikation:</strong> Eidgenössischer Fachausweis (Steuerexperte/-expertin, Treuhänder/-in) oder gleichwertige Qualifikation; Mitgliedschaft bei Treuhand Suisse oder EXPERTsuisse bevorzugt.",),
  ("<strong>Berufshaftpflicht:</strong> gültige Vermögensschadenhaftpflicht in angemessener Deckungshöhe.",),
  ("<strong>Sitz und Datenhaltung in der Schweiz:</strong> Geschäftssitz im Kanton der Vermittlung; Client-Daten werden in der Schweiz bearbeitet.",),
  ("<strong>Praxis in der natürlichen Person:</strong> nachweisbare Erfahrung mit Privatsteuererklärungen im zuständigen Kanton.",),
  ("<strong>Unabhängigkeit:</strong> keine provisionsgetriebenen Produktverkäufe im Namen des Portals; Ranglisten sind nicht käuflich.",),
 ],
 proc_h="So läuft die Prüfung ab",
 proc=["Bewerbung oder Anfrage über das Kontaktformular.",
       "Prüfung der Nachweise: Diplom, Versicherung, Eintrag im Handelsregister (SHAB-Nummer).",
       "Erstvermittlung an ausgewählte Mandate mit anschliessendem Feedback.",
       "Laufende Kontrolle: Bei Beschwerden oder fehlenden Nachweisen wird die Partnerschaft pausiert oder beendet."],
 note_h="Transparenz",
 note="Bezahlte Platzierungen (Sponsored Posts, Banner) sind auf werbung.html als Werbung gekennzeichnet und haben keinen Einfluss auf die Partnerprüfung. Ein öffentliches Verzeichnis aller Partner bauen wir derzeit auf; bis dahin nennen wir Ihnen bei der Vermittlung die Qualifikation des jeweiligen Partners.",
 cta="Partner werden oder Mandat anfragen →",
),
"en": dict(
 title="How we vet our partners | steuerberatung.ch",
 desc="Clear criteria for vetted tax partners: federal diploma or equivalent qualification, Treuhand Suisse/EXPERTsuisse membership, professional indemnity insurance, Swiss seat and ongoing checks.",
 h1="How we vet our partners",
 sub="“Vetted” is not a marketing word here. Every specialist we refer meets these criteria and is checked on an ongoing basis.",
 crit_h="Mandatory criteria",
 crit=[
  ("<strong>Recognised qualification:</strong> Federal certificate of proficiency (tax expert, fiduciary) or equivalent; membership of Treuhand Suisse or EXPERTsuisse preferred.",),
  ("<strong>Professional indemnity insurance:</strong> valid financial-loss liability cover with adequate sum insured.",),
  ("<strong>Swiss seat and data handling:</strong> business address in the canton of referral; client data processed in Switzerland.",),
  ("<strong>Practice with individuals:</strong> demonstrable experience with private tax returns in the relevant canton.",),
  ("<strong>Independence:</strong> no commission-driven product sales in the portal's name; rankings cannot be bought.",),
 ],
 proc_h="The vetting process",
 proc=["Application or enquiry via the contact form.",
       "Verification of documents: diploma, insurance, commercial register entry (SHAB number).",
       "First referrals to selected mandates with follow-up feedback.",
       "Ongoing checks: complaints or missing evidence suspend or end the partnership."],
 note_h="Transparency",
 note="Paid placements (sponsored posts, banners) are labelled as advertising on werbung.html and have no influence on partner vetting. A public partner directory is being built; until then, we disclose the qualification of each referred specialist at the time of referral.",
 cta="Become a partner or request a mandate →",
),
"fr": dict(
 title="Comment nous vérifions nos partenaires | steuerberatung.ch",
 desc="Critères clairs pour les partenaires fiscaux vérifiés : brevet fédéral ou qualification équivalente, appartenance à Treuhand Suisse/EXPERTsuisse, assurance RC professionnelle, siège suisse et contrôles continus.",
 h1="Comment nous vérifions nos partenaires",
 sub="« Vérifié » n'est pas un mot marketing chez nous. Chaque spécialiste mandaté remplit ces critères et fait l'objet de contrôles continus.",
 crit_h="Critères obligatoires",
 crit=[
  ("<strong>Qualification reconnue :</strong> brevet fédéral (expert fiscal, fiduciaire) ou équivalent ; appartenance à Treuhand Suisse ou EXPERTsuisse appréciée.",),
  ("<strong>Assurance RC professionnelle :</strong> couverture valide des dommages purement financiers, à hauteur adéquate.",),
  ("<strong>Siège et traitement des données en Suisse :</strong> domicile professionnel dans le canton de mandat ; données clients traitées en Suisse.",),
  ("<strong>Pratique pour les personnes physiques :</strong> expérience démontrable des déclarations d'impôt privées dans le canton concerné.",),
  ("<strong>Indépendance :</strong> pas de ventes de produits motivées par des commissions au nom du portail ; les classements ne sont pas achetables.",),
 ],
 proc_h="Le déroulement de la vérification",
 proc=["Candidature ou demande via le formulaire de contact.",
       "Vérification des justificatifs : diplôme, assurance, inscription au registre du commerce (numéro FOSC).",
       "Premiers mandats confiés avec retour d'expérience.",
       "Contrôle continu : en cas de plaintes ou de justificatifs manquants, le partenariat est suspendu ou résilié."],
 note_h="Transparence",
 note="Les emplacements payants (sponsored posts, bannières) sont signalés comme publicité sur werbung.html et n'influencent pas la vérification des partenaires. Un annuaire public des partenaires est en cours de construction ; d'ici là, nous indiquons la qualification de chaque spécialiste mandaté.",
 cta="Devenir partenaire ou demander un mandat →",
),
"it": dict(
 title="Come verifichiamo i nostri partner | steuerberatung.ch",
 desc="Criteri chiari per partner fiscali verificati: attestato professionale federale o qualifica equivalente, appartenenza a Treuhand Suisse/EXPERTsuisse, assicurazione RC professionale, sede svizzera e controlli continui.",
 h1="Come verifichiamo i nostri partner",
 sub="«Verificato» non è una parola di marketing. Ogni specialista incaricato soddisfa questi criteri ed è sottoposto a controlli continui.",
 crit_h="Criteri obbligatori",
 crit=[
  ("<strong>Qualifica riconosciuta:</strong> attestato professionale federale (esperto fiscale, fiduciario) o equivalente; appartenenza a Treuhand Suisse o EXPERTsuisse preferibile.",),
  ("<strong>Assicurazione RC professionale:</strong> copertura valida per danni puramente finanziari, con somma adeguata.",),
  ("<strong>Sede e trattamento dati in Svizzera:</strong> domicilio professionale nel cantone dell'incarico; dati dei clienti trattati in Svizzera.",),
  ("<strong>Esperienza con persone fisiche:</strong> esperienza dimostrabile nelle dichiarazioni d'imposte private nel cantone competente.",),
  ("<strong>Indipendenza:</strong> nessuna vendita di prodotti guidata da provvigioni a nome del portale; le classifiche non sono acquistabili.",),
 ],
 proc_h="Come si svolge la verifica",
 proc=["Candidatura o richiesta tramite il modulo di contatto.",
       "Controllo delle prove: diploma, assicurazione, iscrizione al registro di commercio (numero FOSC).",
       "Primi incarichi selezionati con riscontro successivo.",
       "Controllo continuo: in caso di reclami o prove mancanti la partnership viene sospesa o risolta."],
 note_h="Trasparenza",
 note="Gli spazi a pagamento (sponsored post, banner) sono contrassegnati come pubblicità su werbung.html e non influenzano la verifica dei partner. Un registro pubblico dei partner è in preparazione; fino ad allora comunichiamo la qualifica di ogni specialista incaricato al momento della mediazione.",
 cta="Diventare partner o richiedere un incarico →",
),
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

def page(lang):
    d = L[lang]; up = "" if lang == "de" else "../"
    alts = "\n".join('<link rel="alternate" hreflang="%s" href="https://steuerberatung.ch/%s%s">' % (HL[l], "" if l=="de" else l+"/", SLUG) for l in ["de","en","fr","it"]) + '\n<link rel="alternate" hreflang="x-default" href="https://steuerberatung.ch/%s">' % SLUG
    nav = "\n".join('      <a href="%s">%s</a>' % (p, t) for p, t in NAV[lang])
    sw = "\n".join('<a href="%s" class="lang%s"%s>%s</a>' % (
        ("index.html" if l=="de" else l+"/index.html") if lang=="de" else ("../index.html" if l=="de" else "../%s/index.html" % l),
        " active" if l==lang else "", ' aria-current="true"' if l==lang else "", l.upper()) for l in ["de","en","fr","it"])
    f = FOOT[lang]
    fs = " ".join('<a href="%s">%s</a>' % (p, t) for p, t in f["services"])
    fl = " ".join('<a href="%s">%s</a>' % (p, t) for p, t in f["legal"])
    fc = " ".join('<a href="%s">%s</a>' % (p, t) for p, t in f["contact"])
    crit = "\n".join("<li>%s</li>" % c[0] for c in d["crit"])
    proc = "\n".join("<li>%s</li>" % p for p in d["proc"])
    ld = json.dumps({"@context":"https://schema.org","@type":"WebPage","name":d["h1"],"description":d["desc"],"url":"https://steuerberatung.ch/%s" % (SLUG if lang=="de" else lang+"/"+SLUG),"inLanguage":HL[lang]}, ensure_ascii=False)
    html = f"""<!DOCTYPE html>
<html lang="{HTMLEN[lang]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d['title']}</title>
<meta name="description" content="{d['desc']}">
<link rel="icon" type="image/png" sizes="32x32" href="{up}assets/favicon-32.png">
<link rel="canonical" href="https://steuerberatung.ch/{SLUG if lang=='de' else lang+'/'+SLUG}">
{alts}
<meta property="og:title" content="{d['h1']}">
<meta property="og:description" content="{d['desc']}">
<meta property="og:type" content="website">
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
    <h1>{d['h1']}</h1>
    <p>{d['sub']}</p>
  </div>
</div>
<section class="section"><div class="container prose">
<h2>{d['crit_h']}</h2>
<ul>{crit}</ul>
<h2>{d['proc_h']}</h2>
<ol>{proc}</ol>
<h2>{d['note_h']}</h2>
<p>{d['note']}</p>
<p><a class="btn" href="kontakt.html">{d['cta']}</a></p>
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
    path = os.path.join(ROOT, SLUG if lang == "de" else lang + "/" + SLUG)
    open(path, "w").write(html)
    print("wrote", path)

for lang in ["de","en","fr","it"]:
    page(lang)
