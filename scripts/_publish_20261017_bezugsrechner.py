#!/usr/bin/env python3
"""Kapitalbezugsrechner (3a/PK lump-sum withdrawal tax + staffelung) x4 languages."""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

L = {
"de": dict(title="Kapitalbezugsrechner: 3a & Pensionskasse gestaffelt beziehen", desc="Was kostet der Bezug Ihres 3a- oder PK-Guthabens? Steuer berechnen und die Ersparnis durch gestaffelte Bezüge über mehrere Jahre sehen.", h1="Kapitalbezugsrechner 3a / Pensionskasse", sub="Berechnen Sie die Steuer auf Kapitalleistungen – und was Staffelung über mehrere Jahre bringt.", lbl_amt="Kapitalleistung (CHF)", lbl_n="Anzahl Bezüge", lbl_c="Kanton", btn="Steuer berechnen", res_sep="Getrennte Steuer (Richtwert)", res_per="pro Bezug", res_tot="Gesamt bei Staffelung", res_one="Vergleich: ein einziger Bezug", res_save="Ersparnis durch Staffelung", note="Richtwert nach dem Fünftelungsmodell (Art. 38 DBG) mit dem mittleren Steuerfuss des gewählten Kantons; Kantone mit Sondertarifen (z. B. Zürich, Bern) können abweichen. Verbindliche Zahlen nennt der Steuerrechner oder Ihre Steuerverwaltung.", cta="Säule 3a clever staffeln: So gehen Sie vor →", err="Bitte gültigen Betrag eingeben."),
"en": dict(title="Lump-sum withdrawal calculator: stagger pillar 3a & pension payouts", desc="What does withdrawing your pillar 3a or pension fund capital cost? Estimate the separate tax and see the saving from staggering withdrawals over several years.", h1="Capital withdrawal calculator (3a / pension fund)", sub="Estimate the tax on lump-sum benefits – and what staggering over several years saves you.", lbl_amt="Lump-sum benefit (CHF)", lbl_n="Number of withdrawals", lbl_c="Canton", btn="Calculate tax", res_sep="Separate tax (estimate)", res_per="per withdrawal", res_tot="Total with staggering", res_one="Comparison: single withdrawal", res_save="Saving from staggering", note="Estimate based on the one-fifth model (Art. 38 FATA) at the canton's average tax multiplier; cantons with special tariffs (e.g. Zurich, Bern) may differ. Binding figures come from the tax calculator or your tax administration.", cta="How to stagger pillar 3a withdrawals →", err="Please enter a valid amount."),
"fr": dict(title="Calculateur de prestations en capital : 3e pilier et LPP échelonnées", desc="Que coûte le retrait de votre avoir du 3e pilier ou de la caisse de pension ? Estimez l'impôt séparé et voyez l'économie d'un échelonnement sur plusieurs années.", h1="Calculateur de prestations en capital (3a / LPP)", sub="Estimez l'impôt sur les prestations en capital – et ce que rapporte l'échelonnement sur plusieurs années.", lbl_amt="Prestation en capital (CHF)", lbl_n="Nombre de retraits", lbl_c="Canton", btn="Calculer l'impôt", res_sep="Impôt séparé (estimation)", res_per="par retrait", res_tot="Total avec échelonnement", res_one="Comparaison : un seul retrait", res_save="Économie par échelonnement", note="Estimation selon le modèle du cinquième (art. 38 LIFD) au taux moyen du canton choisi ; les cantons à tarif spécial (p. ex. Zurich, Berne) peuvent s'en écarter. Les chiffres opposables proviennent du calculateur d'impôts ou de votre administration fiscale.", cta="Échelonner ses retraits du 3e pilier : la marche à suivre →", err="Veuillez saisir un montant valide."),
"it": dict(title="Calcolatore prestazioni in capitale: 3° pilastro e cassa pensione scaglionate", desc="Quanto costa il prelievo del vostro avere del 3° pilastro o della cassa pensione? Stimate l'imposta separata e vedete il risparmio dallo scaglionamento su più anni.", h1="Calcolatore delle prestazioni in capitale (3a / LPP)", sub="Stimate l'imposta sulle prestazioni in capitale – e quanto fa risparmiare lo scaglionamento su più anni.", lbl_amt="Prestazione in capitale (CHF)", lbl_n="Numero di prelievi", lbl_c="Cantone", btn="Calcolare l'imposta", res_sep="Imposta separata (stima)", res_per="per prelievo", res_tot="Totale con scaglionamento", res_one="Confronto: un solo prelievo", res_save="Risparmio dallo scaglionamento", note="Stima secondo il modello del quinto (art. 38 LIFD) al moltiplicatore medio del cantone scelto; cantoni con tariffe speciali (p. es. Zurigo, Berna) possono discostarsi. I cifre vincolanti provengono dal calcolatore d'imposte o dall'amministrazione fiscale.", cta="Come scaglionare i prelievi del 3° pilastro →", err="Inserite un importo valido."),
}
NAV = {
 "de": [("leistungen.html","Leistungen"),("werbung.html","Werbung"),("ratgeber.html","Ratgeber"),("rechner.html","Rechner"),("suche.html","Suche")],
 "en": [("leistungen.html","Services"),("werbung.html","Advertise"),("ratgeber.html","Guides"),("rechner.html","Calculator"),("search.html","Search")],
 "fr": [("leistungen.html","Prestations"),("werbung.html","Publicité"),("ratgeber.html","Guide fiscal"),("rechner.html","Calculateur"),("recherche.html","Recherche")],
 "it": [("leistungen.html","Prestazioni"),("werbung.html","Pubblicità"),("ratgeber.html","Guida fiscale"),("rechner.html","Calcolatore"),("ricerca.html","Ricerca")],
}
CANTS = [("ZH","Zürich"),("BE","Bern"),("LU","Luzern"),("UR","Uri"),("SZ","Schwyz"),("OW","Obwalden"),("NW","Nidwalden"),("GL","Glarus"),("ZG","Zug"),("FR","Freiburg"),("SO","Solothurn"),("BS","Basel-Stadt"),("BL","Basel-Landschaft"),("SH","Schaffhausen"),("AR","Appenzell A.Rh."),("AI","Appenzell I.Rh."),("SG","St. Gallen"),("GR","Graubünden"),("AG","Aargau"),("TG","Thurgau"),("TI","Tessin"),("VD","Waadt"),("VS","Wallis"),("NE","Neuenburg"),("GE","Genf"),("JU","Jura")]
FOOT = {
 "de": dict(about="Ihr unabhängiger Partner für Steuern in der Schweiz. Steuer-Ratgeber, Rechner und Vermittlung geprüfter Fachpersonen – transparent und datenschutzkonform.", services=[("leistungen.html","Steuererklärung"),("leistungen.html","Steuerberatung"),("ratgeber.html","Ratgeber")], legal=[("impressum.html","Impressum"),("datenschutz.html","Datenschutz"),("agb.html","AGB")], contact=[("kontakt.html","Beratung anfragen")], hs="Services", hl="Rechtliches", hc="Kontakt", bottom="© 2026 steuerberatung.ch · Unabhängige Steuer-Information &amp; Vermittlung. steuerberatung.ch erbringt keine individuelle Steuer- oder Rechtsberatung. Die Beratung erfolgt ausschliesslich durch die vermittelten Fachpersonen."),
 "en": dict(about="Your independent partner for taxes in Switzerland. Tax guides, calculators and referral to vetted specialists – transparent and privacy-compliant.", services=[("leistungen.html","Tax return"),("leistungen.html","Tax advice"),("ratgeber.html","Guides")], legal=[("impressum.html","Imprint"),("datenschutz.html","Privacy"),("agb.html","Terms")], contact=[("kontakt.html","Request advice")], hs="Services", hl="Legal", hc="Contact", bottom="© 2026 steuerberatung.ch · Independent tax information &amp; partner mediation. steuerberatung.ch does not provide individual tax or legal advice. Advice is provided exclusively by the referred specialists."),
 "fr": dict(about="Votre partenaire indépendant pour les impôts en Suisse. Guides fiscaux, calculateurs et médiation de spécialistes vérifiés – en toute transparence et dans le respect de la protection des données.", services=[("leistungen.html","Déclaration d'impôts"),("leistungen.html","Conseil fiscal"),("ratgeber.html","Guides")], legal=[("impressum.html","Mentions légales"),("datenschutz.html","Protection des données"),("agb.html","CG")], contact=[("kontakt.html","Demander un conseil")], hs="Prestations", hl="Mentions", hc="Contact", bottom="© 2026 steuerberatung.ch · Information fiscale indépendante &amp; médiation. steuerberatung.ch ne fournit pas de conseil fiscal ou juridique individuel. Le conseil est fourni exclusivement par les spécialistes mandatés."),
 "it": dict(about="Il vostro partner indipendente per le imposte in Svizzera. Guide fiscali, calcolatori e mediazione di specialisti verificati – trasparente e conforme alla protezione dei dati.", services=[("leistungen.html","Dichiarazione d'imposte"),("leistungen.html","Consulenza fiscale"),("ratgeber.html","Guide")], legal=[("impressum.html","Colophon"),("datenschutz.html","Protezione dei dati"),("agb.html","CG")], contact=[("kontakt.html","Richiedere consulenza")], hs="Prestazioni", hl="Note legali", hc="Contatto", bottom="© 2026 steuerberatung.ch · Informazione fiscale indipendente &amp; mediazione. steuerberatung.ch non fornisce consulenza fiscale o giuridica individuale. La consulenza è fornita esclusivamente dagli specialisti incaricati."),
}
HL = {"de":"de-CH","en":"en","fr":"fr-CH","it":"it-CH"}
HTMLEN = {"de":"de","en":"en","fr":"fr-CH","it":"it-CH"}

JS = """(function(){
  var form=document.getElementById('br-form'), out=document.getElementById('br-out');
  function fmt(n){return 'CHF '+Math.round(n).toLocaleString('de-CH');}
  function T(k){return (window.BR_I18N||{})[k]||k;}
  function sepTax(amount, canton){
    if(!window.TaxEngine) return null;
    var e = window.TaxEngine;
    var full = e.estimate({taxable: amount, canton: canton, married:false, children:0, taxableFed: amount});
    if(!full) return null;
    return (full.federal + full.cantonalCommunal) / 5;
  }
  form.addEventListener('submit', function(ev){
    ev.preventDefault();
    var amt = parseInt(form.amount.value.replace(/[^0-9]/g,''),10)||0;
    var n = parseInt(form.n.value,10)||1;
    var cant = form.canton.value;
    if(amt < 1000){ out.innerHTML='<p class="a3-err">'+T('err')+'</p>'; return; }
    var per = amt / n;
    var one = sepTax(amt, cant);
    var each = sepTax(per, cant);
    if(one===null||each===null){ out.innerHTML='<p class="a3-err">Engine offline</p>'; return; }
    var tot = each * n;
    var save = one - tot;
    out.innerHTML = '<div class="br-res">'
      + '<div><h3>'+T('res_sep')+'</h3><p class="br-big">'+fmt(tot)+'</p><p>'+T('res_per')+': '+fmt(each)+' × '+n+'</p></div>'
      + '<div><h3>'+T('res_one')+'</h3><p>'+fmt(one)+'</p></div>'
      + '<div><h3>'+T('res_save')+'</h3><p class="br-save">'+fmt(save)+'</p></div>'
      + '</div>';
  });
})();"""

def page(lang):
    d = L[lang]; up = "" if lang == "de" else "../"
    alts = "\n".join('<link rel="alternate" hreflang="%s" href="https://steuerberatung.ch/%s%s">' % (HL[l], "" if l=="de" else l+"/", "bezugsrechner.html" if l=="de" else {"de":"bezugsrechner.html","en":"bezugsrechner.html","fr":"bezugsrechner.html","it":"bezugsrechner.html"}[l]) for l in ["de","en","fr","it"])
    alts = "\n".join('<link rel="alternate" hreflang="%s" href="https://steuerberatung.ch/%sbezugsrechner.html">' % (HL[l], "" if l=="de" else l+"/") for l in ["de","en","fr","it"]) + '\n<link rel="alternate" hreflang="x-default" href="https://steuerberatung.ch/bezugsrechner.html">'
    nav = "\n".join('      <a href="%s">%s</a>' % (p, t) for p, t in NAV[lang])
    sw = "\n".join('<a href="%s" class="lang%s"%s>%s</a>' % (
        ("index.html" if l=="de" else l+"/index.html") if lang=="de" else ("../index.html" if l=="de" else "../%s/index.html" % l),
        " active" if l==lang else "", ' aria-current="true"' if l==lang else "", l.upper()) for l in ["de","en","fr","it"])
    f = FOOT[lang]
    fs = " ".join('<a href="%s">%s</a>' % (p, t) for p, t in f["services"])
    fl = " ".join('<a href="%s">%s</a>' % (p, t) for p, t in f["legal"])
    fc = " ".join('<a href="%s">%s</a>' % (p, t) for p, t in f["contact"])
    opts = "".join('<option value="%s"%s>%s</option>' % (c, " selected" if c=="ZH" else "", nm) for c, nm in CANTS)
    html = f"""<!DOCTYPE html>
<html lang="{HTMLEN[lang]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d['title']} | steuerberatung.ch</title>
<meta name="description" content="{d['desc']}">
<link rel="icon" type="image/png" sizes="32x32" href="{up}assets/favicon-32.png">
<link rel="canonical" href="https://steuerberatung.ch/{'bezugsrechner.html' if lang=='de' else lang+'/bezugsrechner.html'}">
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
<div class="container">
<section class="section">
  <form id="br-form" class="calc-form">
    <label>{d['lbl_amt']}<input type="text" name="amount" inputmode="numeric" placeholder="200000" required></label>
    <label>{d['lbl_n']}<select name="n"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option></select></label>
    <label>{d['lbl_c']}<select name="canton">{opts}</select></label>
    <button type="submit" class="btn">{d['btn']}</button>
  </form>
  <div id="br-out" role="status" aria-live="polite"></div>
  <p class="calc-note">{d['note']}</p>
  <p class="latest-more"><a href="saeule-3a-bezug-staffeln.html">{d['cta']}</a></p>
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
<script>window.BR_I18N={json.dumps({k:d[k] for k in ('res_sep','res_per','res_tot','res_one','res_save','err')}, ensure_ascii=False)};</script>
<script src="{up}assets/tax_engine_data.js?v=3"></script>
<script src="{up}assets/tax_engine.js?v=3"></script>
<script>{JS}</script>
</body>
</html>
"""
    path = os.path.join(ROOT, "bezugsrechner.html" if lang=="de" else lang+"/bezugsrechner.html")
    open(path, "w").write(html)
    print("wrote", path)

for lang in ["de","en","fr","it"]:
    page(lang)
