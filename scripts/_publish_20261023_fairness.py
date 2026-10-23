#!/usr/bin/env python3
"""Build fairness-initiative-ehepaare-2026 in all 4 languages (cron 2026-10-23).

Facts verified 2026-10-23 against official sources:
- ESTV dossier page (curl 200): initiative text (Art. 128 Abs. 3ter BV neu,
  Art. 197 Ziff. 15 Übergangsbestimmung: 3 Jahre Gesetz, sonst Verordnung mit
  alternativer Steuerberechnung nach Ledigentarifen, tieferer Betrag zählt),
  timeline (eingereicht 27.3.2024, 102'051 Unterschriften, 101'382 gültig —
  BK-Verfügung 16.4.2024 BBl 2024 937; Botschaft 7.3.2025; Schlussabstimmung
  19.6.2026NR 102:97 / StR 24:20).
- fedlex BBl 2024 937 (curl 200): 101'382 gültige Unterschriften, Komitee Die Mitte.
- fedlex BBl 2025 1092 (curl 200): Botschaft — Mindereinnahmen Verordnungsweg
  ca. 700 Mio.–1,4 Mrd. CHF/Jahr (Steuerjahr 2025), Verteilung 78,8% Bund /
  21,2% Kantone; kein Gegenentwurf.
- fedlex BBl 2026 1758 (curl 200): Bundesbeschluss (Abstimmungsempfehlung
  Ablehnung, Vorlage 25.018).
- ESTV individualbesteuerung (curl 200): BG Individualbesteuerung am 8.3.2026
  mit 54,23% angenommen.
- 2016-Historie (bk.admin.ch vis404 + ESTV-Timeline): CVP-Initiative am
  28.2.2016 vom Volk mit 50,8% ABGELEHNT (Nur-Mehrheit Kantone), Bundesgericht
  hob Abstimmung 10.4.2019 auf, Komitee zog 2020 zurück. (Research-card
  Behauptung "angenommen, nie umgesetzt" ist falsch — nicht publiziert.)
- Card-Behauptung "Ehegattenabzug am 24.11.2024 verworfen" — nicht belegbar
  (24.11.2024 enthielt keine steuerliche Vorlage gemäss BFS-Jahresliste);
  WEGGELASSEN.
Rechenbeispiele: scripts/tax_engine.js (ESTV-Parität, 18'985 Fixture-Tests ok):
 fed 2026: 160k verh 6'680 vs 2x80k ledig 2'756 (Differenz 3'924);
 110k verh 2'329 vs 2x55k 1'066 (1'263); 90k verh 1'365 vs ledig 2'024 (Bonus 659).
 Kantonsdifferenzen (Kanton+Gemeinde, Richtwert kant. Gemeindesteuerfuss,
 combined 160k vs 2x80k): ZH +2'388, BE +782, LU +324, UR 0, SZ +185, TG ~0,
 VD +1'079, GE ~0, TI +2'415, VS +2'718.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "fairness-initiative-ehepaare-2026"
RELATED = ["individualbesteuerung-erklaert.html",
           "steuern-sparen-tipps.html",
           "steuer-checkliste-2026.html"]

URLS = [
    "https://www.estv.admin.ch/de/eidgenoessische-volksinitiative-ja-zu-fairen-bundessteuern-auch-fuer-ehepaare",
    "https://www.fedlex.admin.ch/eli/fga/2024/937/de",
    "https://www.fedlex.admin.ch/eli/fga/2025/1092/de",
    "https://www.fedlex.admin.ch/eli/fga/2026/1758/de",
    "https://www.estv.admin.ch/de/individualbesteuerung",
]

SOURCES = {"de": list(zip(URLS, [
    "ESTV: Volksinitiative «Ja zu fairen Bundessteuern auch für Ehepaare» (Wortlaut, Verfahren)",
    "BBl 2024 937 – Bundeskanzlei: Zustandekommen der Initiative (101\u202f382 gültige Unterschriften)",
    "BBl 2025 1092 – Botschaft des Bundesrats zur Volksinitiative (25.018)",
    "BBl 2026 1758 – Bundesbeschluss zur Volksinitiative (Abstimmungsempfehlung)",
    "ESTV: Individualbesteuerung (Ja vom 8. März 2026, 54,23 %)"])),
 "en": list(zip(URLS, [
    "FTA: popular initiative “Fair federal taxes for married couples” (text, procedure)",
    "FedLex BBl 2024 937 – initiative validated (101,382 valid signatures)",
    "FedLex BBl 2025 1092 – Federal Council dispatch on the initiative (25.018)",
    "FedLex BBl 2026 1758 – federal decree (voting recommendation)",
    "FTA: individual taxation (accepted 8 March 2026, 54.23%)"])),
 "fr": list(zip(URLS, [
    "AFC : initiative populaire «Pour des impôts fédéraux équitables pour les couples mariés» (texte, procédure)",
    "FedLex BBl 2024 937 – about de l’initiative (101\u202f382 signatures valables)",
    "FedLex BBl 2025 1092 – message du Conseil fédéral (25.018)",
    "FedLex BBl 2026 1758 – arrêté fédéral (recommandation de vote)",
    "AFC : imposition individuelle (oui du 8 mars 2026, 54,23 %)"])),
 "it": list(zip(URLS, [
    "AFC : iniziativa popolare «Sì a imposte federali eque per gli sposi» (testo, procedura)",
    "FedLex BBl 2024 937 – riuscita dell’iniziativa (101\u202f382 firme valide)",
    "FedLex BBl 2025 1092 – messaggio del Consiglio federale (25.018)",
    "FedLex BBl 2026 1758 – decreto federale (raccomandazione di voto)",
    "AFC : imposizione individuale (sì dell’8 marzo 2026, 54,23 %)"])),
}

CTA = {
 "de": '<div class="cta-mid"><strong>Möchten Sie wissen, ob Ihre Ehe steuerlich bestraft wird?</strong> Rechnen Sie Ihre Situation mit dem <a href="rechner.html">kostenlosen Rechner</a> durch – oder lassen Sie sie von einer <a href="partner-pruefung.html">geprüften Fachperson</a> prüfen: <a href="kontakt.html">unverbindliche Offerte anfragen</a>.</div>',
 "en": '<div class="cta-mid"><strong>Want to know whether your marriage is penalised on tax?</strong> Run your numbers through the <a href="rechner.html">free calculator</a> – or have them checked by a <a href="partner-pruefung.html">vetted professional</a>: <a href="kontakt.html">request a no-obligation quote</a>.</div>',
 "fr": '<div class="cta-mid"><strong>Vous voulez savoir si votre mariage est pénalisé fiscalement ?</strong> Calculez votre situation avec le <a href="rechner.html">calculateur gratuit</a> – ou faites-vous conseiller par un <a href="partner-pruefung.html">spécialiste vérifié</a> : <a href="kontakt.html">demandez une offre sans engagement</a>.</div>',
 "it": '<div class="cta-mid"><strong>Vorete sapere se il vostro matrimonio è penalizzato dal fisco?</strong> Calcolate la vostra situazione con il <a href="rechner.html">calcolatore gratuito</a> – o fatela verificare da un <a href="partner-pruefung.html">consulente verificato</a>: <a href="kontakt.html">richiedete un’offerta senza impegno</a>.</div>',
}

TABLE_HEAD = {
 "de": ("<table><tr><th>Kanton</th><th>Verheiratet (Kanton+Gem.)</th>"
        "<th>2× Unverheiratet</th><th>Mehrbelastung</th></tr>"),
 "en": ("<table><tr><th>Canton</th><th>Married (canton+commune)</th>"
        "<th>2× unmarried</th><th>Extra burden</th></tr>"),
 "fr": ("<table><tr><th>Canton</th><th>Mariés (canton+commune)</th>"
        "<th>2× non mariés</th><th>Surcharge</th></tr>"),
 "it": ("<table><tr><th>Cantone</th><th>Sposati (cantone+comune)</th>"
        "<th>2× non sposati</th><th>Peso aggiuntivo</th></tr>"),
}
ROWS = [("ZH","21'092","18'704","+2'388"),("BE","31'556","30'774","+782"),
        ("VD","29'925","28'846","+1'079"),("TI","27'107","24'692","+2'415"),
        ("VS","26'270","23'552","+2'718"),("GE","25'871","25'870","≈ 0"),
        ("UR","22'152","22'152","0"),("TG","21'461","21'462","≈ 0"),
        ("LU","18'644","18'320","+324"),("SZ","14'279","14'094","+185")]
def table(lang):
    return TABLE_HEAD[lang] + "".join(
        f"<tr><td>{c}</td><td>CHF&nbsp;{a}</td><td>CHF&nbsp;{b}</td><td>{d}</td></tr>"
        for c, a, b, d in ROWS) + "</table>"

# ---------------- German ----------------
de_title = "Fairness-Initiative: Ehepaare & Steuern"
de_meta = "Volksinitiative «Ja zu fairen Bundessteuern für Ehepaare» am 29.11.2026: Rechenbeispiel zur Heiratsstrafe, kantonale Unterschiede – was Ja und Nein ändern."
de_sections = [
("Was die Fairness-Initiative am 29. November verlangt",
 """<p>Am <strong>29. November 2026</strong> entscheiden Volk und Stände über die Volksinitiative «Ja zu fairen Bundessteuern auch für Ehepaare – Diskriminierung der Ehe endlich abschaffen!». Die von der Mitte-Partei getragene Initiative wurde am 27. März 2024 mit 102'051 Unterschriften eingereicht; die Bundeskanzlei stellte am 16. April 2024 ihre Gültigkeit mit <strong>101'382 gültigen Unterschriften</strong> fest.</p>
<p>Der Inhalt: Neu soll in Artikel 128 der Bundesverfassung stehen, dass bei der direkten Bundessteuer <strong>das Einkommen eines Ehepaars zusammengerechnet</strong> wird und das Gesetz dafür sorgen muss, dass Ehepaare gegenüber anderen Steuerpflichtigen nicht benachteiligt werden. Die Initiative schreibt das heutige System der gemeinsamen Besteuerung also in der Verfassung fest.</p>
<p>Wichtig zu verstehen: Die Vorlage betrifft <strong>ausschliesslich die direkte Bundessteuer</strong> – Kantone und Gemeinden regelt sie nicht direkt. Bundesrat und Parlament empfehlen Ablehnung (Schlussabstimmung vom 19. Juni 2026: Nationalrat 102:97, Ständerat 24:20); einen Gegenentwurf gibt es nicht. Angenommen wird die Initiative nur mit doppeltem Mehr – Volks- und Ständemehr.</p>
<p><em>Praxis-Tipp:</em> Eine Verfassungsinitiative braucht Volk <em>und</em> die Mehrheit der Kantone. Schon kleine Verschiebungen in bevölkerungsreichen Kantonen wie Zürich oder Bern können den Ausschlag geben – der Abstimmungskampf dürfte daher eng werden.</p>"""),
("Rechenbeispiel: So wirkt die Heiratsstrafe heute",
 """<p>Während der heutigen gemeinsamen Veranlagung werden die Einkommen der Ehegatten addiert und mit dem Ehepaartarif besteuert. Ein Beispiel mit exakten Zahlen aus unserem <a href="rechner.html">Rechner</a> (Steuerjahr 2026, franc-genau am offiziellen ESTV-Rechner verifiziert): <strong>Dora und Emil, verheiratet, kinderlos, je CHF 80'000 steuerbares Einkommen</strong> (zusammen CHF 160'000).</p>
<ul>
<li>Gemeinsame Veranlagung als Ehepaar: <strong>CHF 6'680</strong> direkte Bundessteuer</li>
<li>Zum Vergleich: zwei unverheiratete Steuerpflichtige mit je CHF 80'000: 2 × CHF 1'378 = <strong>CHF 2'756</strong></li>
<li>Mehrbelastung der Ehepaare allein auf Bundesebene: <strong>CHF 3'924 pro Jahr</strong></li>
</ul>
<p>Die gleiche Mechanik wirkt umgekehrt als Heiratsbonus: Ein <strong>Einverdienerpaar mit CHF 90'000 steuerbarem Einkommen</strong> zahlt gemeinsam <strong>CHF 1'365</strong> Bundessteuer, eine ledige Person mit demselben Einkommen <strong>CHF 2'024</strong> – die Ehe spart hier CHF 659. Die ESTV schätzt, dass bei der direkten Bundessteuer je rund <strong>650'000 Ehepaare</strong> einen Heiratsbonus bzw. eine Heiratsstrafe haben.</p>
<p><em>Praxis-Tipp:</em> Die Zahlen oben sind Reineinkommen-Tarifeffekte; Zweiverdiener- und Kinderabzüge mildern die reale Mehrbelastung leicht. Ob Ihre eigene Ehe bestraft oder belohnt wird, hängt von Einkommensverteilung, Kanton und Abzügen ab – rechnen Sie es mit dem <a href="rechner.html">Rechner</a> nach, bevor Sie daraus Konsequenzen ziehen.</p>
""" + CTA["de"]),
("Der Systemwechsel ist bereits beschlossen: Individualbesteuerung",
 """<p>Die Heiratsstrafe ist kein ungeschriebenes Schicksal: Am <strong>8. März 2026</strong> haben die Stimmberechtigten das Bundesgesetz über die <a href="individualbesteuerung-erklaert.html">Individualbesteuerung</a> mit <strong>54,23 %</strong> angenommen. Künftig füllt jede Person – auch Verheiratete – eine eigene Steuererklärung aus, es gilt für alle derselbe Tarif. Umgesetzt wird der Wechsel auf Ebene der direkten Bundessteuer nach dem Zeitplan des Bundesrats <strong>spätestens per 1. Januar 2032</strong>; die Kantone müssen nachziehen.</p>
<p>Genau hier liegt der Konflikt: Die Fairness-Initiative will die gemeinsame Besteuerung der Ehepaare in der Verfassung verankern – sie steht damit im direkten Widerspruch zum bereits gutgeheissenen Systemwechsel. Ein Ja zur Initiative würde den Gesetzgeber zwingen, zur Paarbesteuerung zurückzukehren und die Individualbesteuerung auf Bundesebene zu begraben.</p>
<p><em>Praxis-Tipp:</em> Bis die Individualbesteuerung scharf ist, bleiben verheiratete Paare gemeinsam veranlagt – die Übergangsjahre 2027–2031 laufen steuerlich noch komplett nach den heutigen Regeln. Wer eine Heiratsstrafe vermutet, kann schon heute mit Nachteilen rechnen und sollte Aufschub-Optionen prüfen lassen.</p>"""),
("Was ein Ja ändern würde – Frist, Fallback, Folgen",
 """<p>Die Initiative sagt nicht, <em>wie</em> die gemeinsame Besteuerung auszusehen hat – Splittings, Mehrfachtarife und Abzüge bleiben dem Gesetzgeber überlassen. Die Übergangsbestimmung (Art. 197 Ziff. 15 BV-Entwurf) ist aber konkret: Treten die Ausführungsvorschriften nicht <strong>binnen drei Jahren</strong> nach der Annahme in Kraft, muss der Bundesrat sie auf dem <strong>Verordnungsweg</strong> erlassen – mit einer alternativen Steuerberechnung nach den Tarifen und Abzügen für unverheiratete Personen; massgebend ist der tiefere der beiden berechneten Beträge.</p>
<p>Die Kosten schätzt der Bundesrat im Verordnungsfall auf rund <strong>CHF 700 Millionen bis 1,4 Milliarden pro Jahr</strong> (Steuerjahr 2025, nach heutigen Tarifen); davon würden ca. 78,8 % den Bund und 21,2 % die Kantone treffen. Bei einem Nein an der Urne bleibt es dagegen beim beschlossenen Weg zur Individualbesteuerung – ohne neue Verfassungsnorm.</p>
<p><em>Praxis-Tipp:</em> steuerberatung.ch liefert Sachinformationen, keine Wahlempfehlung. Für Ihre persönliche Planung gilt das in beiden Fällen: Prüfen Sie Ihre aktuelle Belastung im <a href="rechner.html">Rechner</a> – denn was sich ab 2027 ändert, hängt vom Urnenentscheid ab.</p>"""),
("Kantonale Unterschiede: Die Heiratsstrafe je Kanton",
 """<p>Die Initiative ändert nur die Bundessteuer – doch die <em>gesamte</em> Heiratsstrafe variiert stark nach Kanton, weil Kantone und Gemeinden die Paarbesteuerung unterschiedlich ausgestalten (Splitting, Familien- und Ehegattenabzüge, eigene Tarife). Gerechnet mit demselben Fall (Steuerjahr 2026, steuerbares Gesamteinkommen CHF 160'000 bzw. 2 × CHF 80'000, je Kanton mit mittlerem Gemeindesteuerfuss – Richtwerte, der Steuerfuss Ihrer Gemeinde kann abweichen):</p>
""" + table("de") + """
<p>Lesart: In Uri, Thurgau und Genf fällt die kantonale Mehrbelastung praktisch null aus, in Wallis, Tessin und Zürich ist sie am höchsten. Dazu kommt in <em>jedem</em> Kanton die Mehrbelastung der direkten Bundessteuer von CHF 3'924 (Beispiel B).</p>
<p><em>Praxis-Tipp:</em> Ein Wegzug allein wegen der Heiratsstrafe ist selten klug – rechnen Sie Kanton, Gemeinde, Liegenschaftskosten und sämtliche Abzüge zusammen durch, bevor Sie Umzugspläne fassen. Die Individualbesteuerung wird diesen kantonalen Flickenteppich weitgehend vereinheitlichen.</p>"""),
("Was Paare unabhängig vom Abstimmungsresultat jetzt tun",
 """<p>Ob Ja oder Nein: Bis mindestens 2031 werden Ehepaare auf Bundesebene gemeinsam veranlagt. Die Planung bleibt also bei den bewährten Hebeln – und die wirken gegen eine Heiratsstrafe oft stärker als jede Verfassungsnorm: <strong>Säule 3a</strong> beider Ehegatten ausschöpfen (auch nachzahlen, wo möglich: <a href="saeule-3a-nachzahlen.html">Säule 3a nachzahlen</a>, Rechenbasis im <a href="3a-rechner.html">3a-Rechner</a>), Abzüge bündeln, Liegenschaftsunterhalt im richtigen Jahr konzentrieren.</p>
<p>Für die Steuer zählt grundsätzlich der Zivilstand <strong>per Ende der Steuerperiode</strong>: Wer eine Heirat plant, sollte die steuerlichen Folgen fürs gemeinsame erste Steuerjahr vorher durchrechnen – bei ähnlichen Einkommen fällt die Mehrbelastung am grössten aus. Umgekehrt prüfen Paare mit sehr ungleichen Einkommen vor einer Heirat den möglichen Heiratsbonus.</p>
<p><em>Praxis-Tipp:</em> Starten Sie die Planung nicht erst im Abstimmungsfieber: Die <a href="steuer-checkliste-2026.html">Steuer-Checkliste</a> und die <a href="steuern-sparen-tipps.html">Spar-Tipps</a> der Site zeigen die Hebel, die 2026/27 in jedem System funktionieren. Bei komplexeren Konstellationen (Liegenschaften, Selbstständigkeit) lohnt die Abklärung durch eine Fachperson.</p>"""),
]

# ---------------- English ----------------
en_title = "Fairness Vote: Married Couples & Tax"
en_meta = "Popular initiative on fair federal taxes for married couples, 29 Nov 2026: worked marriage-penalty example, cantonal differences, what Yes or No changes."
en_sections = [
("What the fairness initiative on 29 November demands",
 """<p>On <strong>29 November 2026</strong>, Swiss voters and cantons decide on the popular initiative “Yes to fair federal taxes for married couples – end discrimination against marriage!”. Backed by the Die Mitte party, it was filed on 27 March 2024 with 102,051 signatures; the Federal Chancellery declared it valid on 16 April 2024 with <strong>101,382 valid signatures</strong>.</p>
<p>The substance: Article 128 of the Federal Constitution would newly state that for federal direct tax the <strong>income of married couples is aggregated</strong>, and that the law must ensure married couples are not disadvantaged versus other taxpayers – freezing today's joint assessment in the Constitution.</p>
<p>Key point: the initiative covers the <strong>federal direct tax only</strong> – cantons and communes are not directly regulated. The Federal Council and Parliament recommend rejection (final votes 19 June 2026: National Council 102:97, Council of States 24:20); there is no counter-proposal. Adoption requires a double majority – people <em>and</em> cantons.</p>
<p><em>Practical tip:</em> a constitutional initiative needs the canton majority too, so small swings in populous cantons such as Zürich or Bern can decide the outcome – expect a close campaign.</p>"""),
("Worked example: how the marriage penalty works today",
 """<p>Under today's joint assessment, spouses' incomes are added and taxed on the married schedule. Exact numbers from our <a href="rechner.html">calculator</a> (2026 tax year, verified to the franc against the official FTA calculator): <strong>Dora and Emil, married, no children, taxable income CHF 80,000 each</strong> (combined CHF 160,000).</p>
<ul>
<li>Joint assessment as a married couple: <strong>CHF 6,680</strong> federal tax</li>
<li>Comparison – two unmarried taxpayers at CHF 80,000 each: 2 × CHF 1,378 = <strong>CHF 2,756</strong></li>
<li>Federal-level penalty of being married: <strong>CHF 3,924 per year</strong></li>
</ul>
<p>The same mechanics work in reverse as a marriage bonus: a <strong>single-earner couple with CHF 90,000</strong> taxable income pays <strong>CHF 1,365</strong> federal tax jointly, while a single person on the same income pays <strong>CHF 2,024</strong> – marriage saves CHF 659. The FTA estimates roughly <strong>650,000 couples each</strong> benefit from or are penalised by the system at federal level.</p>
<p><em>Practical tip:</em> the figures above isolate the schedule effect on taxable income; dual-earner and child deductions soften the real burden slightly. Whether your own marriage is penalised depends on income split, canton and deductions – run it through the <a href="rechner.html">calculator</a> before drawing conclusions.</p>
""" + CTA["en"]),
("The system change is already approved: individual taxation",
 """<p>The marriage penalty is not a given: on <strong>8 March 2026</strong> voters approved the Federal Act on <a href="individualbesteuerung-erklaert.html">individual taxation</a> with <strong>54.23%</strong>. Eventually every person – including spouses – files an individual return on the same schedule. At federal level the switch takes effect no later than <strong>1 January 2032</strong> under the Federal Council's timetable; cantons must follow.</p>
<p>That is precisely the conflict: the fairness initiative would entrench joint assessment of married couples in the Constitution, directly contradicting the already-approved system change. A Yes would force the legislator back to couple-based taxation and bury individual taxation at federal level.</p>
<p><em>Practical tip:</em> until individual taxation takes effect, married couples remain jointly assessed – the transition years 2027–2031 still run under today's rules. If you suspect a marriage penalty, plan accordingly today instead of waiting for the political transition.</p>"""),
("What a Yes would change – deadline, fallback, consequences",
 """<p>The initiative does not prescribe <em>how</em> joint assessment must look – splitting models, multiple schedules and deductions remain the legislator's choice. But the transitional provision (draft Art. 197 sec. 15 Cst.) is concrete: if implementing law is not in force <strong>within three years</strong> of acceptance, the Federal Council must legislate <strong>by ordinance</strong> – including an alternative assessment calculated on the schedules and deductions for unmarried persons, with the lower of the two amounts levied.</p>
<p>The Federal Council estimates revenue losses of about <strong>CHF 700 million to CHF 1.4 billion per year</strong> in the ordinance scenario (2025 tax year, current schedules); roughly 78.8% would hit the Confederation and 21.2% the cantons. A No, by contrast, leaves the already-decided path to individual taxation untouched – no new constitutional norm.</p>
<p><em>Practical tip:</em> steuerberatung.ch provides facts, not a voting recommendation. Either way, model your current burden now – because what changes in 2027 depends on the ballot.</p>"""),
("Cantonal differences: the marriage penalty by canton",
 """<p>The initiative changes only federal tax – yet the <em>total</em> marriage penalty varies sharply by canton, because cantons and communes design couple taxation differently (splitting, family and spouse deductions, own schedules). Same case, calculated with the site's calculator (2026 tax year, combined taxable CHF 160,000 vs 2 × CHF 80,000, each canton at its average communal multiplier – guide values; your commune's multiplier may differ):</p>
""" + table("en") + """
<p>Reading: in Uri, Thurgau and Geneva the cantonal penalty is virtually nil; in Valais, Ticino and Zürich it is largest. On top, every canton adds the federal penalty of CHF 3,924 (case B).</p>
<p><em>Practical tip:</em> relocating solely because of the marriage penalty is rarely wise – model canton, commune, housing costs and all deductions together first. Individual taxation will largely flatten this cantonal patchwork.</p>"""),
("What couples should do regardless of the vote",
 """<p>Yes or No: until at least 2031, married couples remain jointly assessed at federal level. The proven levers keep working – and usually beat any constitutional clause: exhaust <strong>pillar 3a</strong> contributions for both spouses (including buy-ins where possible: <a href="saeule-3a-nachzahlen.html">pillar 3a buy-in</a>; compute limits in the <a href="3a-rechner.html">3a calculator</a>), bundle deductions, concentrate property maintenance in the right year.</p>
<p>For tax purposes the marital status <strong>as of the end of the tax period</strong> generally applies: couples planning a wedding should model the tax consequences of their first joint year – similar incomes create the largest penalty, while very unequal incomes may gain a bonus.</p>
<p><em>Practical tip:</em> don't wait for the election fever: the site's <a href="steuer-checkliste-2026.html">tax checklist</a> and <a href="steuern-sparen-tipps.html">saving tips</a> show the levers that work in either system in 2026/27. For complex situations (property, self-employment), a professional review pays off.</p>"""),
]

# ---------------- French (Suisse) ----------------
fr_title = "Initiative Fairness : époux et impôts"
fr_meta = "Initiative «Pour des impôts fédéraux équitables pour les couples mariés» du 29.11.2026 : exemple chiffré, différences cantonales, enjeux du vote."
fr_sections = [
("Ce que demande l'initiative Fairness du 29 novembre",
 """<p>Le <strong>29 novembre 2026</strong>, le peuple et les cantons se prononcent sur l'initiative populaire «Pour des impôts fédéraux équitables pour les couples mariés – Mettre fin à la discrimination envers le mariage !». Portée par Le Centre, elle a été déposée le 27 mars 2024 avec 102'051 signatures ; la Chancellerie fédérale a constaté sa validité le 16 avril 2024 avec <strong>101'382 signatures valables</strong>.</p>
<p>Le contenu : l'article 128 de la Constitution disposerait que, pour l'impôt fédéral direct, <strong>le revenu des époux est additionné</strong> et que la loi doit garantir que les couples mariés ne sont pas défavorisés par rapport aux autres contribuables – l'imposition commune actuelle serait gravée dans la Constitution.</p>
<p>À comprendre : l'initiative ne vise que <strong>l'impôt fédéral direct</strong> – cantons et communes ne sont pas réglés directement. Le Conseil fédéral et le Parlement recommandent le rejet (votes finaux du 19 juin 2026 : Conseil national 102:97, Conseil des États 24:20) ; il n'y a pas de contre-projet. L'acceptation exige une double majorité – peuple <em>et</em> cantons.</p>
<p><em>Conseil pratique :</em> une initiative constitutionnelle dépend aussi de la majorité des cantons ; de petits tassements dans les cantons peuplés comme Zurich ou Berne peuvent tout décider – la campagne s'annonce serrée.</p>"""),
("Exemple chiffré : la pénalisation du mariage aujourd'hui",
 """<p>Tant que l'imposition commune s'applique, les revenus des époux sont additionnés et taxés au barème des couples. Chiffres exacts de notre <a href="rechner.html">calculateur</a> (année fiscale 2026, vérifiés au franc près contre le calculateur officiel de l'AFC) : <strong>Dora et Emil, mariés, sans enfants, revenu imposable de CHF 80'000 chacun</strong> (total CHF 160'000).</p>
<ul>
<li>Imposition commune en tant que couple marié : <strong>CHF 6'680</strong> d'impôt fédéral direct</li>
<li>Comparaison – deux concubins imposables chacun à CHF 80'000 : 2 × CHF 1'378 = <strong>CHF 2'756</strong></li>
<li>Surcharge fédérale due au mariage : <strong>CHF 3'924 par an</strong></li>
</ul>
<p>La même mécanique joue en sens inverse comme bonus matrimonial : un <strong>couple à revenu unique de CHF 90'000</strong> imposables paie CHF 1'365 d'impôt fédéral en commun, contre <strong>CHF 2'024</strong> pour une personne seule au même revenu – le mariage fait économiser CHF 659. L'AFC estime qu'environ <strong>650'000 couples chacun</strong> bénéficient d'un bonus ou subissent une pénalisation au niveau fédéral.</p>
<p><em>Conseil pratique :</em> ces chiffres isolent l'effet du barème sur le revenu imposable ; les déductions pour couples biactifs et pour enfants atténuent légèrement la charge réelle. Que votre propre mariage soit pénalisé dépend de la répartition des revenus, du canton et des déductions – passez par le <a href="rechner.html">calculateur</a> avant d'en tirer des conséquences.</p>
""" + CTA["fr"]),
("Le changement de système est déjà accepté : l'imposition individuelle",
 """<p>La pénalisation du mariage n'est pas une fatalité : le <strong>8 mars 2026</strong>, le souverain a accepté la loi fédérale sur <a href="individualbesteuerung-erklaert.html">l'imposition individuelle</a> à <strong>54,23 %</strong>. À terme, chaque personne – y compris les époux – remplira sa propre déclaration au même barème. Au niveau fédéral, la transition s'achève au plus tard le <strong>1er janvier 2032</strong> selon l'échéancier du Conseil fédéral ; les cantons devront suivre.</p>
<p>Tout le conflit est là : l'initiative veut ancrer l'imposition commune des époux dans la Constitution, en contradiction directe avec le changement de système déjà accepté. Un oui forcerait le législateur à revenir à la taxation par couple et enterrerait l'imposition individuelle au niveau fédéral.</p>
<p><em>Conseil pratique :</em> en attendant l'imposition individuelle, les couples mariés restent imposés ensemble – les années de transition 2027–2031 suivent encore pleinement les règles actuelles.</p>"""),
("Ce qu'un oui changerait – délai, solution de repli, conséquences",
 """<p>L'initiative ne dit pas <em>comment</em> l'imposition commune doit être organisée – splittings, barèmes multiples et déductions restent du ressort du législateur. La disposition transitoire (projet d'art. 197 ch. 15 Cst.) est en revanche concrète : si les règles d'exécution ne sont pas en vigueur <strong>trois ans au plus tard</strong> après l'acceptation, le Conseil fédéral doit légiférer <strong>par ordonnance</strong> – avec un calcul alternatif fondé sur les barèmes et déductions des personnes non mariées ; le montant le plus bas des deux calculs est retenu.</p>
<p>Dans le scénario de l'ordonnance, le Conseil fédéral estime les manques à gagner à environ <strong>CHF 700 millions à 1,4 milliard par an</strong> (année fiscale 2025, barèmes actuels) ; environ 78,8 % incomberaient à la Confédération et 21,2 % aux cantons. En cas de non, la route vers l'imposition individuelle décidée par le peuple reste en revanche tracée.</p>
<p><em>Conseil pratique :</em> steuerberatung.ch fournit des informations objectives, pas de consigne de vote. Dans les deux cas, calculez dès maintenant votre charge actuelle – ce qui changera en 2027 dépendra de l'urne.</p>"""),
("Différences cantonales : la pénalisation du mariage selon le canton",
 """<p>L'initiative ne modifie que l'impôt fédéral – mais la pénalisation <em>totale</em> varie fortement selon le canton, car cantons et communes aménagent différemment la fiscalité des couples (splitting, déductions familiales et pour époux, barèmes propres). Même cas (année fiscale 2026, revenu imposable commun CHF 160'000 vs 2 × CHF 80'000, chaque canton avec le multiplier communal moyen – valeurs indicatives, le coefficient de votre commune peut différer) :</p>
""" + table("fr") + """
<p>Lecture : à Uri, Thurgovie et Genève, la surcharge cantonale est pratiquement nulle ; le Valais, le Tessin et Zurich présentent les écarts les plus forts. S'y ajoute, dans <em>chaque</em> canton, la surcharge fédérale de CHF 3'924 (exemple B).</p>
<p><em>Conseil pratique :</em> déménager uniquement pour la pénalisation du mariage est rarement judicieux – calculez d'abord ensemble canton, commune, coûts du logement et toutes les déductions. L'imposition individuelle uniformisera en grande partie ce paysage cantonal.</p>"""),
("Ce que les couples font dès maintenant, quel que soit le résultat",
 """<p>Oui ou non : jusqu'à fin 2031 au moins, les époux restent imposés ensemble au niveau fédéral. Les leviers éprouvés gardent toute leur efficacité – souvent plus qu'une norme constitutionnelle : épuiser les cotisations du <strong>pilier 3a</strong> des deux époux (rachat inclus, quand c'est possible : <a href="saeule-3a-nachzahlen.html">rachat pilier 3a</a>, bases de calcul dans le <a href="3a-rechner.html">calculateur 3a</a>), grouper les déductions, concentrer l'entretien immobilier sur la bonne année.</p>
<p>Fiscalement, l'état civil <strong>à la fin de la période fiscale</strong> est en principe déterminant : un couple qui prévoit de se marier devrait modéliser l'incidence fiscale de sa première année commune – des revenus semblables produisent la plus forte surcharge, des revenus très inégaux peuvent produire un bonus.</p>
<p><em>Conseil pratique :</em> ne pas attendre la fièvre électorale : la <a href="steuer-checkliste-2026.html">check-list fiscale</a> et les <a href="steuern-sparen-tipps.html">conseils d'économie</a> du site listent les leviers valables en 2026/27 dans l'un ou l'autre système. Pour les situations complexes (immobilier, indépendance), un contrôle par un spécialiste s'impose.</p>"""),
]

# ---------------- Italiano ----------------
it_title = "Iniziativa Fairness: fisco e sposi"
it_meta = "Iniziativa «Sì a imposte federali eque per gli sposi» del 29.11.2026: esempio di calcolo, penalizzazione del matrimonio, differenze cantonali, scenari."
it_sections = [
("Che cosa chiede l'iniziativa Fairness del 29 novembre",
 """<p>Il <strong>29 novembre 2026</strong> popolo e Cantoni si pronunciano sull'iniziativa popolare «Sì a imposte federali eque per le coppie sposate – Basta discriminazione del matrimonio!». Sostenuta dal partito Die Mitte, è stata depositata il 27 marzo 2024 con 102'051 firme; la Cancelleria federale ne ha constatata la validità il 16 aprile 2024 con <strong>101'382 firme valide</strong>.</p>
<p>Il contenuto: l'articolo 128 della Costituzione dovrebbe stabilire che per l'imposta federale diretta <strong>il reddito degli sposi è sommato</strong> e che la legge deve impedire svantaggi delle coppie sposate rispetto agli altri contribuenti – imponendo nella Costituzione l'attuale tassazione comune.</p>
<p>Da capire: l'iniziativa riguarda <strong>soltanto l'imposta federale diretta</strong> – Cantoni e Comuni non sono toccati direttamente. Consiglio federale e Parlamento raccomandano il rifiuto (votazioni finali del 19 giugno 2026: Consiglio nazionale 102:97, Consiglio degli Stati 24:20); non esiste controprogetto. Per l'approvazione serve la doppia maggioranza – popolo <em>e</em> Cantoni.</p>
<p><em>Suggerimento pratico:</em> un'iniziativa costituzionale dipende anche dalla maggioranza dei Cantoni; piccoli spostamenti nei Cantoni popolosi come Zurigo o Berna possono decidere il risultato – campagna aperta.</p>"""),
("Esempio di calcolo: la penalizzazione del matrimonio oggi",
 """<p>Finché vige la tassazione comune, i redditi degli sposi vengono sommati e tassati secondo la tariffa per coppie. Numeri esatti del nostro <a href="rechner.html">calcolatore</a> (anno fiscale 2026, verificati al franco rispetto al calcolatore ufficiale dell'AFC): <strong>Dora ed Emil, sposati, senza figli, reddito imponibile di CHF 80'000 ciascuno</strong> (complessivo CHF 160'000).</p>
<ul>
<li>Tassazione comune come coppia sposata: <strong>CHF 6'680</strong> di imposta federale diretta</li>
<li>Confronto – due conviventi non sposati con CHF 80'000 ciascuno: 2 × CHF 1'378 = <strong>CHF 2'756</strong></li>
<li>Maggior onere federale dovuto al matrimonio: <strong>CHF 3'924 all'anno</strong></li>
</ul>
<p>La stessa meccanica opera al rovescio come bonus matrimoniale: una <strong>coppia monoreddito con CHF 90'000</strong> imponibili paga in comune <strong>CHF 1'365</strong> di imposta federale, contro <strong>CHF 2'024</strong> di una persona sola con lo stesso reddito – il matrimonio fa risparmiare CHF 659. L'AFC stima che a livello federale circa <strong>650'000 coppie per parte</strong> godano di un bonus o subiscano una penalizzazione.</p>
<p><em>Suggerimento pratico:</em> questi numeri isolano l'effetto della tariffa sul reddito imponibile; le deduzioni per coppie bi-attive e per figli attenuano leggermente l'onere reale. Che il vostro matrimonio sia penalizzato dipende dalla ripartizione dei redditi, dal Cantone e dalle deduzioni – verificatelo con il <a href="rechner.html">calcolatore</a> prima di trarre conclusioni.</p>
""" + CTA["it"]),
("Il cambio di sistema è già deciso: imposizione individuale",
 """<p>La penalizzazione del matrimonio non è un destino: il <strong>8 marzo 2026</strong> i votanti hanno approvato la legge federale sull'<a href="individualbesteuerung-erklaert.html">imposizione individuale</a> con il <strong>54,23 %</strong>. In futuro ogni persona – sposati compresi – compilerà una propria dichiarazione con la stessa tariffa. A livello federale il passaggio avverrà al più tardi il <strong>1° gennaio 2032</strong> secondo il calendario del Consiglio federale; i Cantoni dovranno adeguarsi.</p>
<p>È qui il conflitto: l'iniziativa vuole ancorare nella Costituzione la tassazione comune degli sposi, in diretta contraddizione con il cambio di sistema già approvato. Un sì costringerebbe il legislatore a tornare alla tassazione di coppia e seppellirebbe l'imposizione individuale a livello federale.</p>
<p><em>Suggerimento pratico:</em> in attesa dell'imposizione individuale, gli sposi restano tassati insieme – gli anni di transizione 2027–2031 seguono ancora pienamente le regole attuali.</p>"""),
("Che cosa cambierebbe un sì – termine, alternativa, conseguenze",
 """<p>L'iniziativa non dice <em>come</em> va organizzata la tassazione comune – splitting, tariffe multiple e deduzioni restano scelta del legislatore. La disposizione transitoria (progetto art. 197 n. 15 Cost.) è però concreta: se le norme di esecuzione non entrano in vigore <strong>entro tre anni</strong> dall'approvazione, il Consiglio federale legifera <strong>per ordinanza</strong> – con un calcolo alternativo basato su tariffe e deduzioni per i non sposati; vale l'importo più basso dei due calcoli.</p>
<p>Nello scenario dell'ordinanza il Consiglio federale stima minori entrate per circa <strong>CHF 700 milioni – 1,4 miliardi all'anno</strong> (anno fiscale 2025, tariffe attuali); ne sarebbero colpiti per il 78,8 % la Confederazione e per il 21,2 % i Cantoni. In caso di no, invece, resta tracciata la strada verso l'imposizione individuale già decisa dal popolo.</p>
<p><em>Suggerimento pratico:</em> steuerberatung.ch offre informazioni oggettive, non raccomandazioni di voto. In entrambi i casi, calcolate subito il vostro onere attuale – ciò che cambierà nel 2027 dipenderà dalle urne.</p>"""),
("Differenze cantonali: la penalizzazione del matrimonio per Cantone",
 """<p>L'iniziativa modifica solo l'imposta federale – ma la penalizzazione <em>complessiva</em> varia molto da Cantone a Cantone, perché Cantoni e Comuni disegnano diversamente la fiscalità di coppia (splitting, deduzioni familiari e per i coniugi, tariffe proprie). Stesso caso (anno fiscale 2026, reddito imponibile complessivo CHF 160'000 vs 2 × CHF 80'000, ogni Cantone con il moltiplicatore comunale medio – valori orientativi, il moltiplicatore del vostro Comune può differire):</p>
""" + table("it") + """
<p>Lettura: a Uri, Turgovia e Ginevra la maggior imposta cantonale è praticamente nulla; Vallese, Ticino e Zurigo mostrano gli scarti maggiori. Si aggiunge, in <em>ogni</em> Cantone, la penalizzazione federale di CHF 3'924 (esempio B).</p>
<p><em>Suggerimento pratico:</em> traslocare solo per la penalizzazione del matrimonio è raramente saggio – calcolate insieme Cantone, Comune, costi dell'alloggio e tutte le deduzioni. L'imposizione individuale omogenerà in gran parte questo mosaico cantonale.</p>"""),
("Che cosa fanno le coppie ora, indipendentemente dal risultato",
 """<p>Sì o no: almeno fino a fine 2031 gli sposi restano tassati insieme a livello federale. Le leve consolidate funzionano ancora – spesso più di qualsiasi norma costituzionale: esaurire i versamenti del <strong>pilastro 3a</strong> di entrambi i coniugi (riscatto incluso, dove possibile: <a href="saeule-3a-nachzahlen.html">riscatto pilastro 3a</a>, basi di calcolo nel <a href="3a-rechner.html">calcolatore 3a</a>), raggruppare le deduzioni, concentrare la manutenzione immobiliare nell'anno giusto.</p>
<p>Fiscalmente vale in linea di principio lo stato civile <strong>a fine periodo d'imposta</strong>: chi pianifica un matrimonio dovrebbe simulare le conseguenze fiscali del primo anno comune – redditi simili producono la penalizzazione maggiore, redditi molto diseguali possono produrre un bonus.</p>
<p><em>Suggerimento pratico:</em> non aspettate la febbre elettorale: la <a href="steuer-checkliste-2026.html">check-list fiscale</a> e i <a href="steuern-sparen-tipps.html">consigli per risparmiare</a> del sito elencano le leve valide nel 2026/27 in entrambi i sistemi. Per situazioni complesse (immobili, attività indipendente) conviene una verifica da parte di un professionista.</p>"""),
]

DATA = [("de", de_title, de_meta, de_sections),
        ("en", en_title, en_meta, en_sections),
        ("fr", fr_title, fr_meta, fr_sections),
        ("it", it_title, it_meta, it_sections)]

for lang, title, meta, sections in DATA:
    assert len(title) <= 40, (lang, "title", len(title))
    assert len(meta) <= 158, (lang, "meta", len(meta))
    assert len(sections) == 6, (lang, "sections", len(sections))
    build(lang, SLUG, title, meta, sections, related=RELATED, sources=SOURCES[lang])
    print(f"{lang}: title {len(title)}, meta {len(meta)}, {len(sections)} sections")
print("done")
