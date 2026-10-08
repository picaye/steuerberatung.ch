#!/usr/bin/env python3
"""Säule-3a-Sparrechner: 4 language pages using the existing /api/tax ESTV proxy.
Differential method: tax(taxable) - tax(taxable - 3a) = real saving, official tariffs."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

L = {
"de": dict(
 title="Säule-3a-Rechner 2026: So viel sparen Sie wirklich",
 h1="Säule-3a-Rechner",
 sub="Berechnet mit den offiziellen ESTV-Tarifen Ihrer Gemeinde: Wie viel Steuern spart Ihr 3a-Beitrag – und welcher Beitrag ist für Sie optimal?",
 desc="Säule-3a-Rechner 2026: echte Steuerersparnis Ihres 3a-Beitrags nach den offiziellen ESTV-Tarifen Ihrer Gemeinde. Maximalbeträge, Grenzsteuersatz, Nachzahlung – kostenlos und ohne Anmeldung.",
 loc="Gemeinde oder PLZ", inc="Steuerbares Einkommen (CHF)", fort="Steuerbares Vermögen (CHF)",
 btn="Ersparnis berechnen", with3a="Mit 3a-Beitrag", without="Ohne 3a-Beitrag",
 saved="Ihre Steuerersparnis", rate="Ihr Grenzsteuersatz", contrib="3a-Beitrag",
 maxw="Maximalbetrag mit Pensionskasse: 7'258 Fr.", maxo="ohne Pensionskasse: 36'288 Fr.",
 pk="Mit Pensionskasse (2. Säule)", nopk="Ohne Pensionskasse (Selbstständig)",
 note="Basis: Ihr eingetragenes steuerbares Einkommen. Der 3a-Beitrag reduziert es – die Ersparnis ist die Differenz der ESTV-Totalsteuer. Kirchensteuer und Vermögenssteuer bleiben unverändert.",
 err="Berechnung nicht verfügbar – bitte Gemeinde prüfen.",
 cta="Erst Steuerlast komplett sehen? Zum grossen Steuerrechner →",
 faq=[("Zahlt sich der Maximalbetrag aus?","Bei einem Grenzsteuersatz von 30 % sparen Sie auf 7'258 Fr. Beitrag rund 2'180 Fr. Steuern pro Jahr – über 30 Jahre Anlagezeit plus Zinseszins ist das der wirksamste Sparhebel der Schweiz."),
      ("Was ist der Grenzsteuersatz?","Der Prozentsatz, um den Ihre Gesamtsteuer steigt, wenn Ihr Einkommen um 100 Fr. wächst. Der Rechner ermittelt ihn für Ihre Gemeinde und Ihr Einkommen – er liegt meist zwischen 25 % und 45 %."),
      ("Kann ich nachzahlen?","Ja: Seit 2026 fehlen Beitragsjahre ab 2025 nicht mehr – bis zu 10 Jahre rückwirkend, zusätzlich zum Jahresbetrag. Details: Säule 3a nachzahlen.")],
),
"en": dict(
 title="Pillar 3a calculator 2026: how much you really save",
 h1="Pillar 3a calculator",
 sub="Computed with the official FTA tariffs for your municipality: how much tax does your 3a contribution save – and what is the optimal amount for you?",
 desc="Pillar 3a savings calculator 2026: the real tax saving of your 3a contribution using official FTA tariffs for your municipality. Maximum amounts, marginal tax rate, catch-up contributions – free, no sign-up.",
 loc="Municipality or ZIP", inc="Taxable income (CHF)", fort="Taxable wealth (CHF)",
 btn="Calculate saving", with3a="With 3a contribution", without="Without 3a contribution",
 saved="Your tax saving", rate="Your marginal tax rate", contrib="3a contribution",
 maxw="Maximum with pension fund: CHF 7,258", maxo="without pension fund: CHF 36,288",
 pk="With pension fund (2nd pillar)", nopk="Without pension fund (self-employed)",
 note="Basis: your taxable income. The 3a contribution reduces it – the saving is the difference in total FTA tax. Church and wealth tax stay unchanged.",
 err="Calculation unavailable – please check the municipality.",
 cta="See your full tax load? Go to the main tax calculator →",
 faq=[("Is the maximum amount worth it?","At a 30% marginal rate you save roughly CHF 2,180 per year on a CHF 7,258 contribution – over 30 years of compounding this is Switzerland's most effective savings lever."),
      ("What is the marginal tax rate?","The percentage by which your total tax rises if your income grows by CHF 100. The calculator derives it for your municipality and income – typically 25% to 45%."),
      ("Can I catch up?","Yes: since 2026, missing contribution years from 2025 onwards can be filled retroactively (up to 10 years) on top of the annual amount.")],
),
"fr": dict(
 title="Calculateur pilier 3a 2026 : combien vous économisez vraiment",
 h1="Calculateur pilier 3a",
 sub="Calculé avec les barèmes officiels de l'AFC de votre commune : combien d'impôts votre versement 3a économise-t-il – et quel montant est optimal ?",
 desc="Calculateur d'épargne pilier 3a 2026 : l'économie d'impôt réelle de votre versement 3a selon les barèmes officiels de l'AFC de votre commune. Montants maximaux, taux marginal, rattrapage – gratuit, sans inscription.",
 loc="Commune ou NPA", inc="Revenu imposable (CHF)", fort="Fortune imposable (CHF)",
 btn="Calculer l'économie", with3a="Avec versement 3a", without="Sans versement 3a",
 saved="Votre économie d'impôt", rate="Votre taux marginal", contrib="Versement 3a",
 maxw="Maximum avec caisse de pension : 7 258 fr.", maxo="sans caisse de pension : 36 288 fr.",
 pk="Avec caisse de pension (2e pilier)", nopk="Sans caisse de pension (indépendant)",
 note="Base : votre revenu imposable. Le versement 3a le réduit – l'économie est la différence de l'impôt total AFC. Impôt ecclésiastique et sur la fortune inchangés.",
 err="Calcul indisponible – vérifiez la commune.",
 cta="Voir la charge fiscale complète ? Aller au calculateur d'impôts →",
 faq=[("Le montant maximal vaut-il le coup ?","Avec un taux marginal de 30 %, vous économisez environ 2 180 fr. par an sur un versement de 7 258 fr. – sur 30 ans, c'est le levier d'épargne le plus efficace de Suisse."),
      ("Qu'est-ce que le taux marginal ?","Le pourcentage dont votre impôt total augmente si votre revenu croît de 100 fr. Le calculateur le détermine pour votre commune – généralement entre 25 % et 45 %."),
      ("Puis-je rattraper ?","Oui : depuis 2026, les années manquantes dès 2025 peuvent être comblées rétroactivement (jusqu'à 10 ans) en plus du versement annuel.")],
),
"it": dict(
 title="Calcolatore pilastro 3a 2026: quanto risparmiate davvero",
 h1="Calcolatore pilastro 3a",
 sub="Calcolato con i baremi ufficiali AFC del vostro Comune: quante imposte fa risparmiare il vostro versamento 3a – e qual è l'importo ottimale?",
 desc="Calcolatore di risparmio pilastro 3a 2026: il reale risparmio d'imposta del versamento 3a secondo i baremi ufficiali AFC del vostro Comune. Importi massimi, aliquota marginale, recupero – gratuito, senza registrazione.",
 loc="Comune o CAP", inc="Reddito imponibile (CHF)", fort="Sostanza imponibile (CHF)",
 btn="Calcola il risparmio", with3a="Con versamento 3a", without="Senza versamento 3a",
 saved="Il vostro risparmio d'imposta", rate="La vostra aliquota marginale", contrib="Versamento 3a",
 maxw="Massimo con cassa pensione: 7'258 fr.", maxo="senza cassa pensione: 36'288 fr.",
 pk="Con cassa pensione (2° pilastro)", nopk="Senza cassa pensione (indipendente)",
 note="Base: il vostro reddito imponibile. Il versamento 3a lo riduce – il risparmio è la differenza dell'imposta totale AFC. Imposta ecclesiastica e sulla sostanza invariate.",
 err="Calcolo non disponibile – verificare il Comune.",
 cta="Vedere il carico fiscale completo? Andate al calcolatore d'imposte →",
 faq=[("Conviene l'importo massimo?","Con un'aliquota marginale del 30 % risparmiate circa 2'180 fr. l'anno su un versamento di 7'258 fr. – su 30 anni è la leva di risparmio più efficace della Svizzera."),
      ("Cos'è l'aliquota marginale?","La percentuale di cui l'imposta totale cresce se il reddito aumenta di 100 fr. Il calcolatore la determina per il vostro Comune – di norma tra il 25 % e il 45 %."),
      ("Posso recuperare?","Sì: dal 2026 gli anni mancanti dal 2025 in poi possono essere recuperati retroattivamente (fino a 10 anni) oltre al versamento ordinario.")],
),
}

JS = """
(function(){
  var form=document.getElementById('a3-form'), out=document.getElementById('a3-out');
  var locInput=document.getElementById('a3-loc'), list=document.getElementById('a3-loc-list');
  var sel=null;
  function norm(s){return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');}
  function all(){return window.TAX_LOCATIONS||[];}
  locInput.addEventListener('input',function(){
    var q=norm(locInput.value.trim()); sel=null;
    if(q.length<2){list.hidden=true;return;}
    var hits=all().filter(function(l){return norm(l.city).indexOf(q)>=0||l.zip.indexOf(q.slice(0,4))===0||norm(l.canton||'').indexOf(q)===0;}).slice(0,12);
    list.innerHTML=hits.map(function(l){return '<div class="calc-loc-item" data-id="'+l.id+'" data-name="'+l.city+'">'+l.zip+' '+l.city+' ('+l.canton+')'</div>';}).join('');
    list.hidden=!hits.length;
  });
  list.addEventListener('click',function(e){
    var it=e.target.closest('[data-id]'); if(!it)return;
    sel={id:+it.dataset.id,name:it.dataset.name}; locInput.value=it.dataset.name; list.hidden=true;
  });
  function fmt(n){return (T('frmt'))+n.toLocaleString('de-CH');}
  function T(k){return (window.A3_I18N||{})[k]||k;}
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var loc=sel||all().filter(function(l){return norm(l.city)===norm(locInput.value.trim());})[0];
    if(!loc){out.innerHTML='<p class="a3-err">'+T('err')+'</p>';return;}
    var inc=Math.max(0,parseInt(form.income.value.replace(/[^0-9]/g,''),10)||0);
    var fort=Math.max(0,parseInt(form.fortune.value.replace(/[^0-9]/g,''),10)||0);
    var pk=form.pension.value==='with';
    var max=pk?7258:Math.min(36288,Math.round(inc*0.2));
    var contrib=Math.min(max,Math.max(0,parseInt(form.contrib.value.replace(/[^0-9]/g,''),10)||max));
    var ep=window.LEAD_ENDPOINT||'';
    function call(taxable){return fetch(ep.replace(/\/$/,'')+'/api/tax',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({year:2026,loc:loc.id,rel:1,confession:'NONE',children:[],taxable:taxable,fortune:fort})}).then(function(r){if(!r.ok)throw 0;return r.json();});}
    var base=Math.max(0,inc-contrib);
    Promise.all([call(inc),call(base)]).then(function(rs){
      if(!rs[0].ok||!rs[1].ok)throw 0;
      var t0=rs[0].tax.total,t1=rs[1].tax.total,save=Math.max(0,t0-t1);
      var rate=inc>0?(save/contrib*100):0;
      out.innerHTML='<div class="a3-grid">'
        +'<div class="a3-card"><h3>'+T('without')+'</h3><p class="a3-num">'+fmt(t0)+'</p></div>'
        +'<div class="a3-card"><h3>'+T('with3a')+'</h3><p class="a3-num">'+fmt(t1)+'</p></div>'
        +'<div class="a3-card a3-hi"><h3>'+T('saved')+'</h3><p class="a3-num">'+fmt(save)+'</p><p class="muted">'+T('rate')+': '+rate.toFixed(1)+' %</p></div>'
        +'</div><p class="muted">'+T('note')+'</p>';
    }).catch(function(){out.innerHTML='<p class="a3-err">'+T('err')+'</p>';});
  });
})();
"""

def page(lang, d):
    faq = "\n".join("<h3>%s</h3><p>%s</p>" % (q, a) for q, a in d["faq"])
    dirp = "" if lang == "de" else lang + "/"
    up = "" if lang == "de" else "../"
    alts = "\n".join('<link rel="alternate" hreflang="%s" href="https://steuerberatung.ch/%s3a-rechner.html">' % (l, "" if l == "de" else l + "/") for l in ["de", "en", "fr", "it"]) + '\n<link rel="alternate" hreflang="x-default" href="https://steuerberatung.ch/3a-rechner.html">'
    html = f"""<!DOCTYPE html>
<html lang="{ {'fr':'fr-CH','it':'it-CH'}.get(lang, lang) }">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d['title']} | steuerberatung.ch</title>
<meta name="description" content="{d['desc']}">
<link rel="icon" type="image/png" sizes="32x32" href="{up}assets/favicon-32.png">
<link rel="canonical" href="https://steuerberatung.ch/{dirp}3a-rechner.html">
{alts}
<meta property="og:title" content="{d['title']}">
<meta property="og:description" content="{d['desc']}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="{up}assets/style.css">
<link rel="stylesheet" href="{up}assets/extra.css?v=3">
<link rel="stylesheet" href="{up}assets/redesign.css">
</head>
<body>
<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="index.html"><img class="logo-img" src="{up}assets/logo.svg" alt="" width="32" height="32" aria-hidden="true"><span class="logo-text">steuerberatung<span class="accent">.ch</span></span></a>
    <button class="nav-toggle" type="button" aria-label="Menü" aria-expanded="false" aria-controls="main-nav">☰</button>
    <nav class="main-nav" id="main-nav">
      <a href="leistungen.html">Leistungen</a>
      <a href="werbung.html">Werbung</a>
      <a href="ratgeber.html">Ratgeber</a>
      <a href="rechner.html">Rechner</a>
<a href="index.html" class="lang{' active' if lang=='de' else ''}">DE</a>
<a href="/en/index.html" class="lang{' active' if lang=='en' else ''}">EN</a>
<a href="/fr/index.html" class="lang{' active' if lang=='fr' else ''}">FR</a>
<a href="/it/index.html" class="lang{' active' if lang=='it' else ''}">IT</a>
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
<form id="a3-form" class="calc-form">
<div class="form-row">
<div class="form-field">
<label for="a3-loc">{d['loc']}</label>
<input type="text" id="a3-loc" value="Zürich" autocomplete="off" spellcheck="false" placeholder="z. B. 8400">
<div id="a3-loc-list" class="calc-loc-list" hidden></div>
</div>
<div class="form-field">
<label for="a3-inc">{d['inc']}</label>
<input type="text" id="a3-inc" name="income" value="95000" inputmode="numeric">
</div>
<div class="form-field">
<label for="a3-fort">{d['fort']}</label>
<input type="text" id="a3-fort" name="fortune" value="80000" inputmode="numeric">
</div>
</div>
<div class="form-row">
<div class="form-field">
<label for="a3-pk">2. Säule</label>
<select id="a3-pk" name="pension"><option value="with">{d['pk']}</option><option value="no">{d['nopk']}</option></select>
</div>
<div class="form-field">
<label for="a3-contrib">{d['contrib']}</label>
<input type="text" id="a3-contrib" name="contrib" value="7258" inputmode="numeric">
<p class="muted">{d['maxw']} · {d['maxo']}</p>
</div>
</div>
<button class="btn" type="submit">{d['btn']}</button>
</form>
<div id="a3-out"></div>
<p class="muted"><a href="rechner.html">{d['cta']}</a></p>
</section>
<section class="section">{faq}</section>
</div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <div class="logo"><img class="logo-img" src="{up}assets/logo.svg" alt="" width="32" height="32" aria-hidden="true"><span class="logo-text">steuerberatung<span class="accent">.ch</span></span></div>
    </div>
    <div>
      <h4>Services</h4>
      <a href="leistungen.html">Steuererklärung</a>
      <a href="rechner.html">Steuerrechner</a>
      <a href="3a-rechner.html">3a-Rechner</a>
      <a href="ratgeber.html">Ratgeber</a>
    </div>
  </div>
</footer>
<script>window.A3_I18N={{frmt:"CHF "}};</script>
<script src="{up}assets/locations.js?v=3"></script>
<script src="{up}assets/endpoint.js"></script>
<script>{JS}</script>
</body>
</html>"""
    path = os.path.join(ROOT, dirp, "3a-rechner.html")
    open(path, "w", encoding="utf-8").write(html)
    print("wrote", path, len(html), "bytes")

for lang, d in L.items():
    page(lang, d)
print("done")
