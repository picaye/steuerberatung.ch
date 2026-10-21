#!/usr/bin/env python3
"""Build the GV-2027 profit/dividend planning article in all 4 languages.

Slug: generalversammlung-2027-gewinn-dividende-steuer
Card: data/content-research.jsonl 2026-10-21 (pin 2027-02-01 — build now,
publish timing owned by the caller).

Sources (all primary; fedlex texts read via rendered DOM, curl status 200):
- OR (SR 220) Art. 698/699/700, 804/805 — fedlex eli/cc/27/317_321_377/de
  * 6-month ordinary GM rule is Art. 699 Abs. 2 OR (AG) and Art. 805 Abs. 2 OR
    (GmbH) in the CURRENT numbering — the card's "Art. 700" is pre-2023 law;
    today Art. 700 OR is the 20-day convocation notice.
- VStG (SR 642.21) Art. 10/11/12/13/14/16/20/29/32 — eli/cc/1966/371_385_384/de
- DBG (SR 642.11) Art. 20 Abs. 1 Bst. c, 1bis, 3, 4; Art. 18b — eli/cc/1991/1184_1184_1184/de
  * Federal partial taxation since STAF: 70 % (NOT the card's outdated 60 %).
- StHG (SR 642.14) Art. 7 Abs. 1 (cantonal floor 50 %), Art. 8 Abs. 2quinquies
- StG (SR 641.10) Art. 6 Abs. 1 Bst. h (CHF 1 mio exemption), Art. 8 Abs. 1 (1 %)
- ESTV: estv.admin.ch/de/verrechnungssteuer, /deklarationspflicht-bei-der-verrechnungssteuer,
  /verrechnungssteuer-bezahlen (declaration 30 days after approval of accounts;
  Meldeverfahren 30 days after due date, Form 102/103/106/108/110; KEB Form 170)
- BGE 9C_532/2025 facts reused from live claim-checked article
  dividenden-ahv-pflicht-bge-9c-532-2025.html
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "generalversammlung-2027-gewinn-dividende-steuer"
RELATED = ["verrechnungssteuer-schweiz-35-prozent.html",
           "dividenden-ahv-pflicht-bge-9c-532-2025.html",
           "kapitalsteuer-ag-gmbh.html"]

SRC_DE = [
 ("https://www.fedlex.admin.ch/eli/cc/27/317_321_377/de", "Obligationenrecht (SR 220), Art. 698–700 und 804–805"),
 ("https://www.fedlex.admin.ch/eli/cc/1966/371_385_384/de", "Verrechnungssteuergesetz VStG (SR 642.21)"),
 ("https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de", "Direkte Bundessteuer DBG (SR 642.11), Art. 18b und 20"),
 ("https://www.fedlex.admin.ch/eli/cc/1991/1256_1256_1256/de", "Steuerharmonisierungsgesetz StHG (SR 642.14), Art. 7 und 8"),
 ("https://www.fedlex.admin.ch/eli/cc/1974/11_11_11/de", "Stempelabgabengesetz StG (SR 641.10), Art. 6 und 8"),
 ("https://www.estv.admin.ch/de/deklarationspflicht-bei-der-verrechnungssteuer", "ESTV: Deklarationspflicht bei der Verrechnungssteuer"),
]
SRC_EN = [
 ("https://www.fedlex.admin.ch/eli/cc/27/317_321_377/de", "Code of Obligations (SR 220), Art. 698–700 and 804–805"),
 ("https://www.fedlex.admin.ch/eli/cc/1966/371_385_384/de", "Withholding Tax Act VStG (SR 642.21)"),
 ("https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de", "Federal Direct Tax Act DBG (SR 642.11), Art. 18b and 20"),
 ("https://www.fedlex.admin.ch/eli/cc/1991/1256_1256_1256/de", "Tax Harmonisation Act StHG (SR 642.14), Art. 7 and 8"),
 ("https://www.fedlex.admin.ch/eli/cc/1974/11_11_11/de", "Stamp Duties Act StG (SR 641.10), Art. 6 and 8"),
 ("https://www.estv.admin.ch/de/deklarationspflicht-bei-der-verrechnungssteuer", "FCSTA: withholding tax declaration duty"),
]
SRC_FR = [
 ("https://www.fedlex.admin.ch/eli/cc/27/317_321_377/de", "Code des obligations (RS 220), art. 698–700 et 804–805"),
 ("https://www.fedlex.admin.ch/eli/cc/1966/371_385_384/de", "Loi sur l'impôt anticipé LIA (RS 642.21)"),
 ("https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de", "Loi sur l'impôt fédéral direct LIFD (RS 642.11), art. 18b et 20"),
 ("https://www.fedlex.admin.ch/eli/cc/1991/1256_1256_1256/de", "Loi sur l'harmonisation fiscale LHID (RS 642.14), art. 7 et 8"),
 ("https://www.fedlex.admin.ch/eli/cc/1974/11_11_11/de", "Loi sur les droits de timbre LT (RS 641.10), art. 6 et 8"),
 ("https://www.estv.admin.ch/de/deklarationspflicht-bei-der-verrechnungssteuer", "AFC : obligation de déclarer l'impôt anticipé"),
]
SRC_IT = [
 ("https://www.fedlex.admin.ch/eli/cc/27/317_321_377/de", "Codice delle obbligazioni (RS 220), art. 698–700 e 804–805"),
 ("https://www.fedlex.admin.ch/eli/cc/1966/371_385_384/de", "Legge sull'imposta preventiva LIP (RS 642.21)"),
 ("https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de", "Legge sull'imposta federale diretta LIFD (RS 642.11), art. 18b e 20"),
 ("https://www.fedlex.admin.ch/eli/cc/1991/1256_1256_1256/de", "Legge sull'armonizzazione fiscale LAID (RS 642.14), art. 7 e 8"),
 ("https://www.fedlex.admin.ch/eli/cc/1974/11_11_11/de", "Legge sulle tasse di bollo LTB (RS 641.10), art. 6 e 8"),
 ("https://www.estv.admin.ch/de/deklarationspflicht-bei-der-verrechnungssteuer", "AFC: obbligo di dichiarazione dell'imposta preventiva"),
]

# ---------------- German ----------------
de_title = "Generalversammlung 2027: Dividende & VST"
de_meta = "GV innert sechs Monaten nach Bilanzschluss: Gewinnverwendung protokollieren, 35 % VST innert 30 Tagen, Kapitalmassnahmen im Blick — Fristen 2027."
de_sections = [
 ("Warum die GV 2027 schon jetzt geplant wird",
  """<p>Die GV-Saison 2027 beginnt lange vor der Einladung. Für Unternehmen mit Kalenderjahr steht per <strong>31. Dezember 2026</strong> der Abschluss des Geschäftsjahres an, und die <strong>ordentliche Generalversammlung muss innerhalb von sechs Monaten nach Abschluss des Geschäftsjahres stattfinden</strong> (Art. 699 Abs. 2 OR) – für das Geschäftsjahr 2026 also spätestens am <strong>30. Juni 2027</strong>.</p>
<p>Für die <strong>GmbH gilt dieselbe Frist</strong>: Seit der Revision des Aktienrechts findet auch die ordentliche Gesellschafterversammlung «alljährlich innerhalb von sechs Monaten nach Schluss des Geschäftsjahres» statt (Art. 805 Abs. 2 OR). Die Einberufung muss bei der AG mindestens 20 Tage vor dem Versammlungstag mitgeteilt werden (Art. 700 Abs. 1 OR); bei der GmbH gilt ebenfalls die 20-Tage-Frist, die Statuten können sie auf bis zu 10 Tage verkürzen (Art. 805 Abs. 3 OR).</p>
<p><strong>Praxistipp:</strong> Planen Sie rückwärts – vom GV-Termin über die Einberufungsfrist bis zur fertigen Jahresrechnung. In der GV-Saison Februar bis Juni sind Treuhand und Revisionsstellen knapp.</p>"""),
 ("Was die Versammlung beschliesst – und was im Protokoll stehen muss",
  """<p>Die Verwendung des Bilanzgewinns ist dem obersten Organ <strong>unübertragbar</strong> vorbehalten: Bei der AG gehören «die Genehmigung der Jahresrechnung sowie die Beschlussfassung über die Verwendung des Bilanzgewinnes, insbesondere die Festsetzung der Dividende und der Tantieme» zu den unübertragbaren Befugnissen der Generalversammlung (Art. 698 Abs. 2 Ziff. 4 OR). Bei der GmbH entscheidet die Gesellschafterversammlung gleichlautend (Art. 804 Abs. 2 Ziff. 5 OR) – und zusätzlich über die Rückzahlung von Kapitalreserven (Ziff. 5bis).</p>
<p>Für die Steuerpraxis entscheidend ist der Protokollinhalt: Beschliessen Sie nicht nur die <strong>Höhe</strong> der Dividende, sondern auch deren <strong>Fälligkeit</strong>. Mit der Fälligkeit entsteht die Verrechnungssteuerforderung (Art. 12 Abs. 1 VStG), und ab diesem Tag laufen die 30-Tage-Fristen für Zahlung, Deklaration und ein allfälliges Meldeverfahren. Ein Beschluss «Dividende von CHF 50'000, fällig am 30. Juni 2027» schafft Klarheit.</p>
<p>Bei Kapitalmassnahmen der GmbH können je nach Beschluss öffentliche Beurkundung und Handelsregistereintragung erforderlich sein – planen Sie dafür Vorlauf ein. Dieser Artikel ist eine Planungshilfe, keine Rechtsberatung.</p>"""),
 ("Der Planungsfahrplan 2027: alle Fristen in einer Tabelle",
  """<p>Der Fahrplan gilt für eine Kapitalgesellschaft mit <strong>Kalenderjahr</strong> (Bilanzstichtag 31.12.2026). Bei abweichendem Geschäftsjahr verschieben sich die Fristen entsprechend.</p>
<table><thead><tr><th>Schritt</th><th>Frist / Termin</th><th>Grundlage</th></tr></thead><tbody>
<tr><td>Bilanzstichtag (Kalenderjahr)</td><td>31.12.2026</td><td>Statuten</td></tr>
<tr><td>Einberufung der Versammlung</td><td>mind. 20 Tage vorher (GmbH: Statuten bis 10 Tage)</td><td>Art. 700 Abs. 1 / Art. 805 Abs. 3 OR</td></tr>
<tr><td>Ordentliche GV: Jahresrechnung genehmigen, Dividende beschliessen</td><td>innerhalb von 6 Monaten nach Geschäftsjahresende, d. h. bis 30.06.2027</td><td>Art. 699 Abs. 2 / Art. 805 Abs. 2 OR</td></tr>
<tr><td>Deklaration bei der ESTV: Jahresrechnung + amtliche Aufstellung</td><td>innert 30 Tagen nach Genehmigung der Jahresrechnung</td><td>VStV / ESTV</td></tr>
<tr><td>Fälligkeit der Dividende</td><td>gemäss Beschluss (z. B. 15.06.2027)</td><td>GV-Protokoll</td></tr>
<tr><td>Verrechnungssteuer (35 %) einzahlen</td><td>30 Tage nach Entstehung der Steuerforderung</td><td>Art. 16 Abs. 1 Bst. c VStG</td></tr>
<tr><td>Meldeverfahren im Konzern: Gesuch statt Zahlung</td><td>innert 30 Tagen nach Fälligkeit der Dividende</td><td>Art. 20 VStG / ESTV</td></tr>
<tr><td>Steuererklärung: Dividende deklarieren</td><td>Steuerjahr 2027</td><td>Art. 20 DBG</td></tr>
<tr><td>VST-Rückerstattungsantrag (falls nicht via Veranlagung)</td><td>frühestens nach dem 31.12.2027, spätestens 31.12.2030</td><td>Art. 29 / Art. 32 Abs. 1 VStG</td></tr>
</tbody></table>
<p><strong>Praxistipp:</strong> Tragen Sie die Fristen direkt nach der GV in die Agenda ein – die 30-Tage-Fristen laufen ab Fälligkeit, nicht ab Überweisung. Was von der Dividende übrig bleibt, zeigt vorab der <a href="rechner.html">Steuerrechner</a>.</p>"""),
 ("Nach dem Dividendenbeschluss: 35 % Verrechnungssteuer innert 30 Tagen",
  """<p>Der Dividendenbeschluss löst die <strong>Verrechnungssteuer (VST)</strong> aus – steuerpflichtig ist die Gesellschaft als Schuldnerin der Leistung (Art. 10 Abs. 1 VStG). Auf Dividenden als Kapitalertrag beträgt die Steuer <strong>35 Prozent der steuerbaren Leistung</strong> (Art. 13 Abs. 1 Bst. a VStG). Die Gesellschaft muss die Leistung bei der Auszahlung um den Steuerbetrag kürzen (Art. 14 Abs. 1 VStG): Beim Aktionär kommen netto 65 Prozent an.</p>
<p>Die Steuerforderung entsteht, sobald die Dividende <strong>fällig</strong> wird (Art. 12 Abs. 1 VStG), und ist <strong>30 Tage danach</strong> zu entrichten (Art. 16 Abs. 1 Bst. c VStG). Die VST ist eine Selbstdeklarationssteuer – Zahlung und Abrechnung erfolgen unaufgefordert, ohne Mahnung oder Aufforderung der ESTV. Bei Verspätung wird ohne Mahnung ein Verzugszins fällig (Art. 16 Abs. 2 VStG); die ESTV erhebt ihn erst ab 100 Franken, der Satz wird jährlich in einer Verordnung des Eidgenössischen Finanzdepartements festgelegt.</p>
<p>Nicht vergessen: Für inländische Kapitalgesellschaften gilt zusätzlich eine <strong>Deklarationspflicht</strong>. Innert <strong>30 Tagen nach Genehmigung der Jahresrechnung</strong> sind der ESTV unaufgefordert der Geschäftsbericht oder eine unterzeichnete Kopie der Jahresrechnung sowie eine Aufstellung nach amtlichem Formular einzureichen – ersichtlich sein müssen Kapitalbestand am Jahresende, Datum der Generalversammlung, beschlossene Gewinnverteilung und deren Fälligkeit. Ausgelöst wird die Pflicht u. a., wenn mit der beschlossenen Gewinnverteilung eine steuerbare Leistung vorliegt oder die Bilanzsumme fünf Millionen Franken übersteigt (VStV, ESTV).</p>
<p><strong>Praxistipp:</strong> Die Liquidität für 35 Prozent der Bruttodividende muss 30 Tage nach Fälligkeit verfügbar sein. Bei Engpässen kann die ESTV auf schriftliches Gesuch Fristverlängerung oder Ratenzahlung gewähren – das Gesuch gehört vor den Termin, nicht danach.</p><div class="cta-mid"><strong>Unklar, was das für Ihre Situation bedeutet?</strong> Eine <a href="partner-pruefung.html">geprüfte Fachperson</a> prüft Ihre Unterlagen und zeigt das konkrete Sparpotenzial – die Erstberatung ist kostenlos: <a href="kontakt.html">unverbindliche Offerte anfragen</a>.</div>"""),
 ("Rückerstattung: Die 35 % kommen zurück – aber nur auf Antrag",
  """<p>Für in der Schweiz steuerpflichtige Aktionäre ist die VST kein definitiver Aufwand – aber auch kein Automatismus. Wer die Dividende in der <strong>Steuererklärung korrekt deklariert</strong>, erhält die abgezogene Steuer im Rahmen der Veranlagung zurück. Wo keine Veranlagung stattfindet, ist der Antrag schriftlich bei der ESTV zu stellen – über das ESTV-Portal oder mit dem elektronischen Formular 25.</p>
<p>Zwei gesetzliche Fristen: Der Antrag kann <strong>frühestens nach Ablauf des Kalenderjahres</strong> gestellt werden, in dem die Leistung fällig wurde (Art. 29 Abs. 2 VStG). Und er <strong>verwirkt nach drei Jahren</strong>: «Der Anspruch auf Rückerstattung erlischt, wenn der Antrag nicht innert drei Jahren nach Ablauf des Kalenderjahres, in dem die steuerbare Leistung fällig geworden ist, gestellt wird» (Art. 32 Abs. 1 VStG). Für eine am 15. Juni 2027 fällige Dividende läuft die Frist also bis zum <strong>31. Dezember 2030</strong> – danach ist das Geld endgültig weg.</p>
<p>Die Gesellschaft muss dem Empfänger die für die Rückerstattung nötigen Angaben machen und auf Verlangen eine Bescheinigung ausstellen (Art. 14 Abs. 2 VStG). Mehr dazu in den Artikeln <a href="verrechnungssteuer-schweiz-35-prozent.html">Verrechnungssteuer 35 % zurückholen</a> und <a href="verrechnungssteuer-rueckerstattungsfrist-ablauf.html">VST-Rückerstattungsfrist im Blick</a>.</p>"""),
 ("Lohn oder Dividende? Die Checkliste für Inhaber-Gesellschafter",
  """<p>Die GV ist der richtige Moment für die Grundsatzfrage <strong>Lohn oder Dividende</strong> – die Steuer- und Abgabefolgen unterscheiden sich deutlich:</p>
<ul>
<li><strong>Lohn</strong> ist bei der Gesellschaft abzugsfähig, unterliegt den AHV/IV/EO- und ALV-Beiträgen und ist beim Empfänger voll steuerbar – er baut aber auch Rentenansprüche auf.</li>
<li><strong>Dividenden</strong> sind beitragsfreier Kapitalertrag und werden nur teilweise besteuert: Auf Bundesebene sind Dividenden aus qualifizierten Beteiligungen (mindestens 10 Prozent des Grund- oder Stammkapitals, Privatvermögen) <strong>zu 70 Prozent steuerbar</strong> (Art. 20 Abs. 1bis DBG); für Beteiligungen im Geschäftsvermögen gilt derselbe Satz (Art. 18b DBG). Die Kantone besteuern solche Dividenden <strong>im Umfang von 50 Prozent</strong>, dürfen aber höher gehen (Art. 7 Abs. 1 StHG) – der konkrete Satz ist kantonal verschieden.</li>
<li><strong>AHV-Risiko:</strong> Ist der Inhaberlohn unangemessen tief und die Dividende offensichtlich überhöht, können Ausgleichskassen Dividenden teilweise als beitragspflichtigen Lohn aufrechnen – das Bundesgericht hat diesen Durchgriff im Urteil <strong>9C_532/2025</strong> sogar durch eine substanzlose Holding bestätigt. Als überhöht gilt eine Dividende nach der Verwaltungspraxis vermutungsweise ab 10 Prozent des Steuerwerts der Beteiligung; Nachforderungen sind bis fünf Jahre rückwirkend möglich. Details im Artikel <a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">Dividenden statt Lohn: das BGE-Urteil</a>.</li>
</ul>
<p><strong>Checkliste vor dem Dividendenbeschluss:</strong></p>
<ol>
<li>Hält der Inhaberlohn dem Branchenvergleich stand (Pensum, Verantwortung, Salarium)?</li>
<li>Bleibt die Dividende unter der kritischen Schwelle von 10 Prozent des Aktien-Steuerwerts?</li>
<li>Wie wirkt die Teilbesteuerung im Wohnsitzkanton? Nachrechnen mit dem <a href="rechner.html">Steuerrechner</a>.</li>
<li>Ist die Liquidität für die VST (35 Prozent) 30 Tage nach Fälligkeit gesichert?</li>
<li>Stehen Höhe, Fälligkeit und Stimmlage sauber im Protokoll?</li>
</ol>"""),
 ("Rechenbeispiel: Ausschüttung einer Inhaber-AG",
  """<div class="cta-mid"><strong>Rechenbeispiel (fiktive Zahlen):</strong> Die Alleinaktionärin hält 100 Prozent der X AG im Privatvermögen; die GV beschliesst am 10. Juni 2027 eine Dividende von <strong>CHF 100'000</strong>, fällig am 15. Juni 2027.<br><br>
<strong>Gesellschaft:</strong> Verrechnungssteuer 35 Prozent = CHF 35'000, fällig 30 Tage nach Entstehung der Steuerforderung (bis 15. Juli 2027); Auszahlung an die Aktionärin netto CHF 65'000. Deklaration (Jahresrechnung + amtliche Aufstellung) innert 30 Tagen nach Genehmigung der Jahresrechnung.<br><br>
<strong>Aktionärin:</strong> Deklaration von CHF 100'000 in der Steuererklärung 2027. Bund: steuerbar sind 70 Prozent = CHF 70'000 (Art. 20 Abs. 1bis DBG). Kanton: 50 Prozent = CHF 50'000 als Untergrenze, je nach Kanton mehr (Art. 7 Abs. 1 StHG). Die VST von CHF 35'000 kommt via Veranlagung zurück – ohne Veranlagung per Antrag an die ESTV, spätestens bis 31.12.2030 (Art. 32 Abs. 1 VStG).<br><br>
<em>Illustratives Beispiel ohne Gewähr; die effektive Belastung hängt von Kanton, Gemeinde und den übrigen Einkünften ab.</em></div>"""),
 ("Parallel-Beschlüsse: Kapitalerhöhung, Kapitaleinlagereserven, Meldeverfahren",
  """<p>Auf der Traktandenliste stehen oft auch Kapitalmassnahmen – mit eigenen Steuerfolgen:</p>
<ul>
<li><strong>Kapitalerhöhung:</strong> Die Emissionsabgabe beträgt <strong>1 Prozent</strong> der der Gesellschaft zufliesenden Gegenleistung, mindestens aber des Nennwerts (Art. 8 Abs. 1 StG). Ausgenommen ist die entgeltliche Ausgabe von Beteiligungsrechten an AG, Kommanditaktiengesellschaften und GmbH, soweit die Leistungen der Gesellschafter gesamthaft <strong>eine Million Franken nicht übersteigen</strong> (Art. 6 Abs. 1 Bst. h StG). Wer eine Erhöhung plant, sollte diesen Freibetrag bewusst ausschöpfen.</li>
<li><strong>Kapitaleinlagereserven (KEB):</strong> Die Rückzahlung von Einlagen, Aufgeldern und Zuschüssen, die nach dem 31.12.1996 geleistet wurden, wird wie die Rückzahlung von Grund- oder Stammkapital behandelt (Art. 20 Abs. 3 DBG) – also ohne Einkommenssteuer und ohne VST. Voraussetzung: Die Reserven sind in der Handelsbilanz auf einem <strong>gesonderten Konto</strong> ausgewiesen, und jede Veränderung ist der ESTV mit <strong>Formular 170</strong> zu melden. Fehlt der Nachweis, wird die Rückzahlung im Zeitpunkt der Auszahlung steuerbar (ESTV-Praxis). Bei kotierten Gesellschaften gelten zusätzliche Ausschüttungsregeln (Art. 20 Abs. 4 DBG).</li>
<li><strong>Meldeverfahren im Konzern:</strong> Bei Dividendenausschüttungen im inländischen und grenzüberschreitenden Konzernverhältnis kann die Steuerpflicht durch <strong>Meldung statt Entrichtung</strong> erfüllt werden (Art. 20 VStG) – die 35 Prozent müssen dann nicht vorfinanziert werden. Das Gesuch ist innert 30 Tagen nach Fälligkeit der Dividende mit den Formularen 106, 108, 102, 103 und 110 samt Jahresrechnung einzureichen; wird die Frist verpasst, wird das Meldeverfahren unter Vorbehalt einer Ordnungsbusse (Art. 64 VStG) dennoch gewährt (ESTV).</li>
</ul>"""),
 ("Kurz gesagt",
  """<ul>
<li>Ordentliche Generalversammlung bzw. Gesellschafterversammlung: innert sechs Monaten nach Geschäftsjahresende – für 2026 also bis 30.06.2027 (Art. 699 Abs. 2 / Art. 805 Abs. 2 OR).</li>
<li>Dividendenbeschluss: Höhe <em>und Fälligkeit</em> ins Protokoll – die Fälligkeit startet alle VST-Fristen.</li>
<li>Verrechnungssteuer: 35 Prozent, zahlbar 30 Tage nach Entstehung der Forderung; Deklaration der Jahresrechnung innert 30 Tagen nach Genehmigung (Art. 13 und 16 VStG; VStV/ESTV).</li>
<li>Rückerstattung an den Aktionär: nur auf Antrag oder via korrekte Deklaration – Verwirkungsfrist drei Jahre (Art. 32 Abs. 1 VStG).</li>
<li>Teilbesteuerung: Bund 70 Prozent ab 10 Prozent Beteiligung (Art. 20 Abs. 1bis DBG), Kantone 50 Prozent als Untergrenze (Art. 7 Abs. 1 StHG).</li>
<li>Vor dem Beschluss Lohn/Dividende im Licht von BGE 9C_532/2025 prüfen – sonst droht die AHV-Nachforderung.</li>
<li>Allgemeine Information, keine individuelle Beratung: Lassen Sie GV-Traktanden und Ausschüttungsplanung von Treuhand oder Steuerberatung prüfen – <a href="kontakt.html">Beratung anfragen</a>.</li>
</ul>"""),
]

# ---------------- English ----------------
en_title = "General Meeting 2027: Dividend & WHT"
en_meta = "Ordinary general meeting within six months of year-end: profit resolution, 35 % withholding tax due in 30 days, refund window of 3 years — 2027 deadlines."
en_sections = [
 ("Why the 2027 general meeting must be planned now",
  """<p>The 2027 meeting season starts long before the invitation goes out. For companies on a calendar year, the financial year closes on <strong>31 December 2026</strong>, and the <strong>ordinary general meeting must be held within six months after the close of the financial year</strong> (Art. 699 para. 2 CO) — for the 2026 financial year, that means <strong>30 June 2027 at the latest</strong>.</p>
<p>The <strong>same deadline applies to the GmbH</strong> (LLC): since the corporate law revision, the ordinary shareholders' meeting also takes place "annually within six months after the close of the financial year" (Art. 805 para. 2 CO). The convocation must be notified at least 20 days before the meeting for an AG (Art. 700 para. 1 CO); for a GmbH the 20-day rule also applies, but the articles may shorten it to as little as 10 days (Art. 805 para. 3 CO).</p>
<p><strong>Practical tip:</strong> plan backwards — from the meeting date over the convocation period to the finished annual accounts. Fiduciaries and auditors are scarce between February and June; booking early gets the accounts done before the meeting.</p>"""),
 ("What the meeting decides — and what the minutes must contain",
  """<p>The appropriation of the balance-sheet profit is a <strong>non-transferable</strong> power of the supreme body: for an AG, "the approval of the annual financial statements and the resolution on the appropriation of the balance-sheet profit, in particular the determination of the dividend" belongs exclusively to the general meeting (Art. 698 para. 2 no. 4 CO). The GmbH shareholders' meeting decides in identical terms (Art. 804 para. 2 no. 5 CO) — plus the repayment of capital reserves (no. 5bis).</p>
<p>What matters for tax practice is the content of the minutes: resolve not only the <strong>amount</strong> of the dividend but also its <strong>due date</strong>. The withholding tax claim arises when the payment falls due (Art. 12 para. 1 WHTA), and the 30-day deadlines for payment, declaration and any notification procedure all run from that day. A resolution reading "dividend of CHF 50'000, due 30 June 2027" creates clarity; without a due date, deadline planning starts in the fog.</p>
<p>For capital measures at a GmbH, public notarisation and commercial register entry may be required depending on the resolution — allow lead time. This article is a planning aid, not legal advice.</p>"""),
 ("The 2027 planning timeline: all deadlines in one table",
  """<p>The timeline assumes a company on a <strong>calendar year</strong> (balance date 31.12.2026). With a different financial year the deadlines shift accordingly.</p>
<table><thead><tr><th>Step</th><th>Deadline</th><th>Basis</th></tr></thead><tbody>
<tr><td>Balance date (calendar year)</td><td>31.12.2026</td><td>Articles</td></tr>
<tr><td>Convocation of the meeting</td><td>at least 20 days before (GmbH: articles may allow 10)</td><td>Art. 700 para. 1 / Art. 805 para. 3 CO</td></tr>
<tr><td>Ordinary meeting: approve accounts, resolve dividend</td><td>within 6 months of year-end, i.e. by 30.06.2027</td><td>Art. 699 para. 2 / Art. 805 para. 2 CO</td></tr>
<tr><td>Declaration to the FTA: annual accounts + official statement</td><td>within 30 days of approval of the accounts</td><td>WHT Ordinance / FTA</td></tr>
<tr><td>Dividend due date</td><td>per resolution (e.g. 15.06.2027)</td><td>Minutes</td></tr>
<tr><td>Pay the 35 % withholding tax</td><td>30 days after the tax claim arises</td><td>Art. 16 para. 1 lit. c WHTA</td></tr>
<tr><td>Group notification procedure: request instead of payment</td><td>within 30 days of the dividend due date</td><td>Art. 20 WHTA / FTA</td></tr>
<tr><td>Tax return: declare the dividend</td><td>2027 tax year</td><td>Art. 20 DBG</td></tr>
<tr><td>WHT refund request (if not via assessment)</td><td>earliest after 31.12.2027, latest 31.12.2030</td><td>Art. 29 / Art. 32 para. 1 WHTA</td></tr>
</tbody></table>
<p><strong>Practical tip:</strong> enter the deadlines in your diary straight after the meeting — the 30-day periods run from the due date, not from the transfer. The <a href="rechner.html">tax calculator</a> shows in advance what is left of the dividend after federal tax, cantonal tax and WHT.</p>"""),
 ("After the dividend resolution: 35 % withholding tax within 30 days",
  """<p>The dividend resolution triggers <strong>Swiss withholding tax (WHT)</strong> — the company, as debtor of the taxable payment, is liable (Art. 10 para. 1 WHTA). On dividends as capital yield the tax is <strong>35 percent of the taxable payment</strong> (Art. 13 para. 1 lit. a WHTA). The company must deduct the tax when paying out (Art. 14 para. 1 WHTA): the shareholder receives a net 65 percent.</p>
<p>The tax claim arises as soon as the dividend <strong>falls due</strong> (Art. 12 para. 1 WHTA) and must be paid <strong>30 days later</strong> (Art. 16 para. 1 lit. c WHTA). WHT is a self-declaration tax — payment and accounting are owed unprompted, without any request from the Federal Tax Administration (FTA). Late payment accrues default interest without reminder (Art. 16 para. 2 WHTA); the FTA only charges it from CHF 100 upwards, and the rate is set annually by ordinance of the Federal Department of Finance.</p>
<p>Do not forget the separate <strong>declaration duty</strong>: within <strong>30 days of the approval of the annual accounts</strong>, domestic companies must submit to the FTA, unprompted, the annual report or a signed copy of the annual accounts plus a statement on the official form — showing the capital at year-end, the date of the general meeting, the profit distribution resolved and its due date. The duty is triggered inter alia where the resolved distribution constitutes a taxable payment or the balance-sheet total exceeds five million francs (WHT Ordinance, FTA).</p>
<p><strong>Practical tip:</strong> liquidity for 35 percent of the gross dividend must be available 30 days after the due date. In a squeeze, the FTA can grant an extension or instalments on written request — file it before the deadline, not after.</p><div class="cta-mid"><strong>Not sure what this means for your situation?</strong> A <a href="partner-pruefung.html">vetted professional</a> reviews your documents and shows your concrete savings potential – first consultation free: <a href="kontakt.html">request a no-obligation quote</a>.</div>"""),
 ("Refund: the 35 % comes back — but only on request",
  """<p>For shareholders taxable in Switzerland, WHT is not a definitive cost — but neither is it automatic. Whoever <strong>declares the dividend correctly in the tax return</strong> gets the deducted tax back through the assessment. Where no assessment takes place, the refund must be requested in writing from the FTA — via the FTA portal or the electronic Form 25.</p>
<p>Two statutory deadlines: the request can be filed <strong>earliest after the end of the calendar year</strong> in which the payment fell due (Art. 29 para. 2 WHTA), and it <strong>forfeits after three years</strong>: the request must be filed within three years after the end of the calendar year in which the taxable payment fell due (Art. 32 para. 1 WHTA). For a dividend due on 15 June 2027 the deadline therefore runs to <strong>31 December 2030</strong> — after that, the money is gone for good.</p>
<p>The company must give the recipient the information needed to claim the refund and issue a certificate on request (Art. 14 para. 2 WHTA). More detail in our articles <a href="verrechnungssteuer-schweiz-35-prozent.html">reclaiming the 35 % withholding tax</a> and <a href="verrechnungssteuer-rueckerstattungsfrist-ablauf.html">the WHT refund deadline</a>.</p>"""),
 ("Salary or dividend? The checklist for owner-managers",
  """<p>The general meeting is the right moment for the fundamental question — <strong>salary or dividend</strong>. The tax and social security consequences differ markedly:</p>
<ul>
<li><strong>Salary</strong> is deductible for the company, subject to AHV/IV/EO and unemployment contributions, and fully taxable for the recipient — but it also builds pension entitlements.</li>
<li><strong>Dividends</strong> are contribution-free capital yield and are only partially taxed: at federal level, dividends from qualifying participations (at least 10 percent of the share capital, private assets) are <strong>taxable at 70 percent</strong> (Art. 20 para. 1bis DBG); the same rate applies to participations held as business assets (Art. 18b DBG). The cantons tax such dividends <strong>at 50 percent</strong> as a floor but may go higher (Art. 7 para. 1 StHG) — the effective rate varies by canton.</li>
<li><strong>AHV risk:</strong> where the owner's salary is unreasonably low and the dividend manifestly excessive, compensation funds may reclassify part of the dividend as contributable salary — the Federal Supreme Court confirmed this look-through even via a substance-less holding in ruling <strong>9C_532/2025</strong>. Under administrative practice a dividend is presumed excessive above 10 percent of the tax value of the shares; back claims reach five years. Details in our article <a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">Dividends instead of salary: the Supreme Court ruling</a>.</li>
</ul>
<p><strong>Checklist before the dividend resolution:</strong></p>
<ol>
<li>Does the owner's salary withstand an industry comparison (workload, responsibility, Salarium)?</li>
<li>Does the dividend stay below the critical threshold of 10 percent of the shares' tax value?</li>
<li>How does partial taxation play out in the canton of residence? Run the numbers in the <a href="rechner.html">tax calculator</a>.</li>
<li>Is liquidity for the WHT (35 percent) secured 30 days after the due date?</li>
<li>Are amount, due date and voting results cleanly recorded in the minutes?</li>
</ol>"""),
 ("Worked example: distribution by an owner-managed AG",
  """<div class="cta-mid"><strong>Worked example (fictitious figures):</strong> the sole shareholder holds 100 percent of X AG in her private assets; the general meeting resolves a dividend of <strong>CHF 100'000</strong> on 10 June 2027, due 15 June 2027.<br><br>
<strong>Company:</strong> withholding tax 35 percent = CHF 35'000, due 30 days after the tax claim arises (by 15 July 2027); net payout to the shareholder CHF 65'000. Declaration (annual accounts + official statement) within 30 days of the approval of the accounts.<br><br>
<strong>Shareholder:</strong> declares CHF 100'000 in the 2027 tax return. Federal: 70 percent taxable = CHF 70'000 (Art. 20 para. 1bis DBG). Canton: 50 percent = CHF 50'000 as the floor, more depending on the canton (Art. 7 para. 1 StHG). The CHF 35'000 WHT comes back via the assessment — or, without one, by request to the FTA at the latest by 31.12.2030 (Art. 32 para. 1 WHTA).<br><br>
<em>Illustrative example, no guarantee; the effective burden depends on canton, municipality and total income.</em></div>"""),
 ("Parallel resolutions: capital increase, capital contribution reserves, notification procedure",
  """<p>Capital measures often share the agenda — with tax consequences of their own:</p>
<ul>
<li><strong>Capital increase:</strong> the issuance stamp duty is <strong>1 percent</strong> of the consideration flowing to the company, at least of the nominal value (Art. 8 para. 1 StG). Exempt is the issuance for consideration of equity rights in AGs, partnerships limited by shares and GmbHs insofar as the shareholders' contributions total no more than <strong>one million francs</strong> (Art. 6 para. 1 lit. h StG). Anyone planning an increase should deliberately use up this allowance.</li>
<li><strong>Capital contribution reserves (KEB):</strong> repayments of contributions, agios and supplements made after 31.12.1996 are treated like the repayment of share capital (Art. 20 para. 3 DBG) — no income tax, no WHT. Condition: the reserves are shown in a <strong>separate account</strong> in the commercial balance sheet and every change is reported to the FTA on <strong>Form 170</strong>. Without that proof there is no KEB and the repayment becomes taxable when paid out (FTA practice). Listed companies face additional distribution rules (Art. 20 para. 4 DBG).</li>
<li><strong>Group notification procedure:</strong> for dividends within domestic and cross-border group relationships the tax may be settled by <strong>notification instead of payment</strong> (Art. 20 WHTA) — no need to pre-finance the 35 percent. The request must be filed within 30 days of the dividend due date with Forms 106, 108, 102, 103 and 110 plus the annual accounts; if the deadline is missed, the procedure is still granted, subject to an administrative fine (Art. 64 WHTA, FTA).</li>
</ul>"""),
 ("In short",
  """<ul>
<li>Ordinary general meeting / shareholders' meeting: within six months of year-end — for 2026, by 30.06.2027 (Art. 699 para. 2 / Art. 805 para. 2 CO).</li>
<li>Dividend resolution: amount <em>and due date</em> into the minutes — the due date starts all WHT deadlines.</li>
<li>Withholding tax: 35 percent, payable 30 days after the claim arises; declaration of the annual accounts within 30 days of approval (Art. 13 and 16 WHTA; WHT Ordinance/FTA).</li>
<li>Refund to the shareholder: only on request or via correct declaration — forfeited after three years (Art. 32 para. 1 WHTA).</li>
<li>Partial taxation: federal 70 percent from a 10 percent participation (Art. 20 para. 1bis DBG); cantonal floor of 50 percent (Art. 7 para. 1 StHG).</li>
<li>Before resolving, review the salary/dividend split in light of ruling 9C_532/2025 — otherwise AHV back claims loom.</li>
<li>General information, not individual advice: have your agenda and distribution planning reviewed by a fiduciary or tax adviser — <a href="kontakt.html">request advice</a>.</li>
</ul>"""),
]

# ---------------- French ----------------
fr_title = "AG 2027 : dividende et impôt anticipé"
fr_meta = "AG dans les six mois après la clôture : répartition du bénéfice, 35 % d'impôt anticipé sous 30 jours, remboursement sous 3 ans — échéances 2027."
fr_sections = [
 ("Pourquoi l'AG 2027 se planifie dès maintenant",
  """<p>La saison des assemblées 2027 commence bien avant la convocation. Pour les entreprises à l'année civile, l'exercice se clôture le <strong>31 décembre 2026</strong> et l'<strong>assemblée générale ordinaire doit se tenir dans les six mois qui suivent la clôture de l'exercice</strong> (art. 699 al. 2 CO) — soit, pour l'exercice 2026, au plus tard le <strong>30 juin 2027</strong>.</p>
<p>Le <strong>même délai vaut pour la Sàrl</strong> : depuis la révision du droit de la société anonyme, l'assemblée ordinaire des associés a lieu « chaque année dans les six mois qui suivent la clôture de l'exercice » (art. 805 al. 2 CO). La convocation doit être communiquée au moins 20 jours avant la séance dans la SA (art. 700 al. 1 CO) ; dans la Sàrl, le délai de 20 jours s'applique aussi, mais les statuts peuvent le réduire jusqu'à 10 jours (art. 805 al. 3 CO).</p>
<p><strong>Conseil pratique :</strong> planifiez à rebours — de la date de l'assemblée au délai de convocation, puis aux comptes annuels. Fiduciaires et organes de révision sont rares entre février et juin ; réserver tôt garantit des comptes prêts avant la séance.</p>"""),
 ("Ce que l'assemblée décide — et ce que le procès-verbal doit contenir",
  """<p>L'emploi du bénéfice reporté est une compétence <strong>inaliénable</strong> de l'organe suprême : dans la SA, « l'approbation des comptes annuels et la décision concernant l'emploi du bénéfice, notamment la fixation du dividende » relèvent exclusivement de l'assemblée générale (art. 698 al. 2 ch. 4 CO). Dans la Sàrl, l'assemblée des associés décide dans les mêmes termes (art. 804 al. 2 ch. 5 CO) — et en plus du remboursement des réserves issues d'apports de capital (ch. 5bis).</p>
<p>Ce qui compte fiscalement, c'est le contenu du procès-verbal : fixez non seulement le <strong>montant</strong> du dividende, mais aussi son <strong>échéance</strong>. La créance d'impôt anticipé naît lorsque la prestation est exigible (art. 12 al. 1 LIA) et les délais de 30 jours — paiement, déclaration, procédure de déclaration — courent dès ce jour. Une décision « dividende de CHF 50'000, exigible le 30 juin 2027 » crée la clarté ; sans échéance, la planification des délais démarre dans le brouillard.</p>
<p>Selon la mesure, les décisions de la Sàrl touchant le capital peuvent requérir un acte authentique et une inscription au registre du commerce — prévoyez du temps. Cet article est une aide à la planification, pas un conseil juridique.</p>"""),
 ("Le calendrier 2027 : tous les délais en un tableau",
  """<p>Ce calendrier suppose une société de capitaux à l'<strong>année civile</strong> (bilan au 31.12.2026). Avec un exercice différent, les échéances se décalent en conséquence.</p>
<table><thead><tr><th>Étape</th><th>Délai</th><th>Base légale</th></tr></thead><tbody>
<tr><td>Clôture du bilan (année civile)</td><td>31.12.2026</td><td>Statuts</td></tr>
<tr><td>Convocation de l'assemblée</td><td>au moins 20 jours avant (Sàrl : statuts jusqu'à 10 jours)</td><td>art. 700 al. 1 / art. 805 al. 3 CO</td></tr>
<tr><td>AG ordinaire : approuver les comptes, décider le dividende</td><td>dans les 6 mois après la clôture, soit jusqu'au 30.06.2027</td><td>art. 699 al. 2 / art. 805 al. 2 CO</td></tr>
<tr><td>Déclaration à l'AFC : comptes annuels + relevé officiel</td><td>dans les 30 jours après l'approbation des comptes</td><td>OIA / AFC</td></tr>
<tr><td>Exigibilité du dividende</td><td>selon la décision (p. ex. 15.06.2027)</td><td>Procès-verbal</td></tr>
<tr><td>Payer l'impôt anticipé (35 %)</td><td>30 jours après la naissance de la créance</td><td>art. 16 al. 1 let. c LIA</td></tr>
<tr><td>Procédure de déclaration dans un groupe : demande au lieu du paiement</td><td>dans les 30 jours après l'échéance du dividende</td><td>art. 20 LIA / AFC</td></tr>
<tr><td>Déclaration fiscale : déclarer le dividende</td><td>année fiscale 2027</td><td>art. 20 LIFD</td></tr>
<tr><td>Demande de remboursement de l'IA (si pas via taxation)</td><td>au plus tôt après le 31.12.2027, au plus tard le 31.12.2030</td><td>art. 29 / art. 32 al. 1 LIA</td></tr>
</tbody></table>
<p><strong>Conseil pratique :</strong> notez les échéances dans l'agenda dès l'assemblée — les délais de 30 jours courent dès l'exigibilité, pas dès le virement. Le <a href="rechner.html">calculateur fiscal</a> montre à l'avance ce qui reste du dividende après impôt fédéral, cantonal et IA.</p>"""),
 ("Après la décision : 35 % d'impôt anticipé sous 30 jours",
  """<p>La décision de distribution déclenche l'<strong>impôt anticipé (IA)</strong> — la société débitrice de la prestation est assujettie (art. 10 al. 1 LIA). Sur les dividendes, revenu de capitaux mobiliers, l'impôt s'élève à <strong>35 pour cent de la prestation imposable</strong> (art. 13 al. 1 let. a LIA). La société doit retrancher l'impôt lors du versement (art. 14 al. 1 LIA) : l'actionnaire reçoit net 65 pour cent.</p>
<p>La créance fiscale naît dès que le dividende est <strong>exigible</strong> (art. 12 al. 1 LIA) et doit être payée <strong>30 jours plus tard</strong> (art. 16 al. 1 let. c LIA). L'IA est un impôt auto-déclaré : paiement et décompte se font spontanément, sans sommation ni demande de l'AFC. En cas de retard, un intérêt moratoire est dû sans rappel (art. 16 al. 2 LIA) ; l'AFC ne le perçoit qu'à partir de 100 francs, le taux étant fixé chaque année par ordonnance du Département fédéral des finances.</p>
<p>Ne pas oublier l'<strong>obligation de déclarer</strong> : dans les <strong>30 jours suivant l'approbation des comptes annuels</strong>, toute société de capitaux suisse doit remettre spontanément à l'AFC le rapport de gestion ou une copie signée des comptes annuels ainsi qu'un relevé sur formulaire officiel — capital à la fin de l'exercice, date de l'assemblée générale, répartition du bénéfice décidée et son échéance. L'obligation est notamment déclenchée lorsque la répartition décidée constitue une prestation imposable ou lorsque le total du bilan dépasse cinq millions de francs (OIA, AFC).</p>
<p><strong>Conseil pratique :</strong> la liquidité pour 35 pour cent du dividende brut doit être disponible 30 jours après l'échéance. En cas de tension, l'AFC peut accorder une prolongation ou des acomptes sur demande écrite — à déposer avant l'échéance, pas après.</p><div class="cta-mid"><strong>Vous ne savez pas ce que cela implique pour votre situation ?</strong> Un <a href="partner-pruefung.html">conseiller vérifié</a> examine vos documents et chiffre votre potentiel d'économie – premier entretien gratuit : <a href="kontakt.html">demandez une offre sans engagement</a>.</div>"""),
 ("Remboursement : les 35 % reviennent — mais seulement sur demande",
  """<p>Pour les actionnaires imposables en Suisse, l'IA n'est pas une charge définitive — mais rien n'est automatique non plus. Qui <strong>déclare correctement le dividende dans sa déclaration fiscale</strong> récupère l'impôt retenu dans le cadre de la taxation. À défaut de taxation, la demande doit être adressée par écrit à l'AFC — via le portail de l'AFC ou le formulaire électronique 25.</p>
<p>Deux délais légaux : la demande peut être déposée <strong>au plus tôt après l'expiration de l'année civile</strong> au cours de laquelle la prestation est devenue exigible (art. 29 al. 2 LIA) ; et elle se <strong>périme après trois ans</strong> : la demande doit être présentée dans les trois ans qui suivent l'expiration de l'année civile au cours de laquelle la prestation imposable est devenue exigible (art. 32 al. 1 LIA). Pour un dividende exigible le 15 juin 2027, le délai court donc jusqu'au <strong>31 décembre 2030</strong> — ensuite, l'argent est définitivement perdu.</p>
<p>La société doit fournir au bénéficiaire les indications nécessaires au remboursement et, sur demande, une attestation (art. 14 al. 2 LIA). Plus de détails dans nos articles <a href="verrechnungssteuer-schweiz-35-prozent.html">récupérer les 35 % d'impôt anticipé</a> et <a href="verrechnungssteuer-rueckerstattungsfrist-ablauf.html">le délai de remboursement de l'IA</a>.</p>"""),
 ("Salaire ou dividende ? La check-list du dirigeant-propriétaire",
  """<p>L'assemblée est le bon moment pour la question de fond : <strong>salaire ou dividende</strong>. Les conséquences fiscales et sociales diffèrent nettement :</p>
<ul>
<li>Le <strong>salaire</strong> est déductible pour la société, soumis aux cotisations AVS/AI/APG et AC, et pleinement imposable pour le bénéficiaire — mais il ouvre des droits à la rente.</li>
<li>Les <strong>dividendes</strong> sont un rendement de la fortune non cotisable et ne sont imposés que partiellement : au niveau fédéral, les dividendes d'une participation qualifiée (au moins 10 pour cent du capital-actions ou social, fortune privée) sont <strong>imposables à raison de 70 pour cent</strong> (art. 20 al. 1bis LIFD) ; le même taux vaut pour les participations de la fortune commerciale (art. 18b LIFD). Les cantons imposent ces dividendes <strong>à raison de 50 pour cent</strong> au minimum et peuvent prévoir davantage (art. 7 al. 1 LHID) — le taux effectif varie selon le canton.</li>
<li><strong>Risque AVS :</strong> si le salaire du dirigeant est anormalement bas et le dividende manifestement excessif, les caisses de compensation peuvent requalifier une partie du dividende en salaire cotisable — le Tribunal fédéral a confirmé ce percement même à travers une holding sans substance dans l'arrêt <strong>9C_532/2025</strong>. Selon la pratique administrative, un dividende est présumé excessif au-delà de 10 pour cent de la valeur fiscale des actions ; les rappels portent sur cinq ans. Détails dans l'article <a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">Dividendes au lieu du salaire : l'arrêt du TF</a>.</li>
</ul>
<p><strong>Check-list avant la décision de distribution :</strong></p>
<ol>
<li>Le salaire du dirigeant résiste-t-il à la comparaison sectorielle (taux d'activité, responsabilité, Salarium) ?</li>
<li>Le dividende reste-t-il sous le seuil critique de 10 pour cent de la valeur fiscale des actions ?</li>
<li>Quel est l'effet de l'imposition partielle dans le canton de domicile ? Vérifiez avec le <a href="rechner.html">calculateur fiscal</a>.</li>
<li>La liquidité pour l'IA (35 pour cent) est-elle assurée 30 jours après l'échéance ?</li>
<li>Montant, échéance et voix figurent-ils proprement au procès-verbal ?</li>
</ol>"""),
 ("Exemple chiffré : distribution d'une SA détenue par son dirigeant",
  """<div class="cta-mid"><strong>Exemple chiffré (valeurs fictives) :</strong> l'actionnaire unique détient 100 pour cent de X SA dans sa fortune privée ; l'AG décide le 10 juin 2027 un dividende de <strong>CHF 100'000</strong>, exigible le 15 juin 2027.<br><br>
<strong>Société :</strong> impôt anticipé 35 pour cent = CHF 35'000, exigible 30 jours après la naissance de la créance (jusqu'au 15 juillet 2027) ; versement net à l'actionnaire CHF 65'000. Déclaration (comptes annuels + relevé officiel) dans les 30 jours après l'approbation des comptes.<br><br>
<strong>Actionnaire :</strong> déclare CHF 100'000 dans la déclaration fiscale 2027. Confédération : 70 pour cent imposables = CHF 70'000 (art. 20 al. 1bis LIFD). Canton : 50 pour cent = CHF 50'000 comme plancher, davantage selon le canton (art. 7 al. 1 LHID). L'IA de CHF 35'000 revient via la taxation — sinon sur demande à l'AFC, au plus tard le 31.12.2030 (art. 32 al. 1 LIA).<br><br>
<em>Exemple illustratif sans garantie ; la charge effective dépend du canton, de la commune et des autres revenus.</em></div>"""),
 ("Décisions parallèles : augmentation de capital, réserves d'apports, procédure de déclaration",
  """<p>L'ordre du jour comporte souvent des mesures de capital — avec leurs propres conséquences fiscales :</p>
<ul>
<li><strong>Augmentation de capital :</strong> le droit de timbre d'émission s'élève à <strong>1 pour cent</strong> de la contre-prestation revenant à la société, mais au moins de la valeur nominale (art. 8 al. 1 LT). Est exceptée l'émission à titre onéreux de droits de participation dans les SA, commandites par actions et Sàrl, pour autant que les apports des associés ne dépassent pas au total <strong>un million de francs</strong> (art. 6 al. 1 let. h LT). Qui planifie une augmentation devrait exploiter délibérément cette franchise.</li>
<li><strong>Réserves issues d'apports de capital (REAC) :</strong> le remboursement d'apports, agios et suppléments versés après le 31.12.1996 est traité comme le remboursement du capital-actions ou social (art. 20 al. 3 LIFD) — sans impôt sur le revenu ni IA. Condition : les réserves figurent dans un <strong>compte séparé</strong> du bilan commercial et chaque modification est annoncée à l'AFC au moyen du <strong>formulaire 170</strong>. Sans cette preuve, il n'y a pas de REAC et le remboursement devient imposable au moment du versement (pratique AFC). Les sociétés cotées connaissent des règles de distribution supplémentaires (art. 20 al. 4 LIFD).</li>
<li><strong>Procédure de déclaration dans un groupe :</strong> pour les dividendes versés dans un rapport de groupe national ou transfrontalier, l'obligation fiscale peut être remplie par <strong>déclaration au lieu du paiement</strong> (art. 20 LIA) — les 35 pour cent ne doivent pas être préfinancés. La demande doit être déposée dans les 30 jours suivant l'échéance du dividende, avec les formulaires 106, 108, 102, 103 et 110 ainsi que les comptes annuels ; si le délai est manqué, la procédure est néanmoins accordée, sous réserve d'une amende d'ordre (art. 64 LIA, AFC).</li>
</ul>"""),
 ("En bref",
  """<ul>
<li>Assemblée générale ordinaire / assemblée des associés : dans les six mois après la clôture — pour 2026, jusqu'au 30.06.2027 (art. 699 al. 2 / art. 805 al. 2 CO).</li>
<li>Décision de distribution : montant <em>et échéance</em> au procès-verbal — l'échéance déclenche tous les délais d'IA.</li>
<li>Impôt anticipé : 35 pour cent, payables 30 jours après la naissance de la créance ; déclaration des comptes dans les 30 jours après approbation (art. 13 et 16 LIA ; OIA/AFC).</li>
<li>Remboursement à l'actionnaire : uniquement sur demande ou via une déclaration correcte — péremption après trois ans (art. 32 al. 1 LIA).</li>
<li>Imposition partielle : Confédération 70 pour cent dès 10 pour cent de participation (art. 20 al. 1bis LIFD), cantons 50 pour cent comme plancher (art. 7 al. 1 LHID).</li>
<li>Avant la décision, examiner le rapport salaire/dividende à la lumière de l'arrêt 9C_532/2025 — sinon un rappel AVS menace.</li>
<li>Information générale, pas de conseil individuel : faites vérifier l'ordre du jour et la planification par une fiduciaire ou un conseiller fiscal — <a href="kontakt.html">demander un conseil</a>.</li>
</ul>"""),
]

# ---------------- Italian ----------------
it_title = "AG 2027: dividendi e imposta preventiva"
it_meta = "Assemblea generale entro sei mesi dalla chiusura: ripartizione dell'utile, imposta preventiva del 35 % entro 30 giorni, rimborso entro 3 anni — scadenze 2027."
it_sections = [
 ("Perché l'assemblea generale 2027 si pianifica già ora",
  """<p>La stagione assembleare 2027 inizia ben prima della convocazione. Per le imprese con anno civile, l'esercizio si chiude il <strong>31 dicembre 2026</strong> e l'<strong>assemblea generale ordinaria deve svolgersi entro sei mesi dalla chiusura dell'esercizio</strong> (art. 699 cpv. 2 CO) — per l'esercizio 2026, dunque al più tardi il <strong>30 giugno 2027</strong>.</p>
<p>Lo <strong>stesso termine vale per le Sagl</strong>: dalla revisione del diritto della società anonima, anche l'assemblea ordinaria dei soci si tiene «ogni anno entro sei mesi dalla chiusura dell'esercizio» (art. 805 cpv. 2 CO). La convocazione va comunicata almeno 20 giorni prima della seduta nella SA (art. 700 cpv. 1 CO); nella Sagl vale parimenti il termine di 20 giorni, che lo statuto può ridurre fino a 10 giorni (art. 805 cpv. 3 CO).</p>
<p><strong>Consiglio pratico:</strong> pianificate a ritroso — dalla data dell'assemblea al termine di convocazione fino ai conti annuali. Fiduciari e uffici di revisione scarseggiano tra febbraio e giugno; chi prenota presto ha i conti pronti prima della seduta.</p>"""),
 ("Che cosa decide l'assemblea — e che cosa deve figurare nel verbale",
  """<p>L'impiego dell'utile di bilancio è una competenza <strong>inalienabile</strong> dell'organo supremo: nella SA «l'approvazione del conto annuale e la deliberazione sull'impiego dell'utile di bilancio, in particolare la fissazione del dividendo» spettano esclusivamente all'assemblea generale (art. 698 cpv. 2 n. 4 CO). Nella Sagl l'assemblea dei soci decide negli stessi termini (art. 804 cpv. 2 n. 5 CO) — e inoltre sulla restituzione delle riserve provenienti da apporti di capitale (n. 5bis).</p>
<p>Per la prassi fiscale è decisivo il contenuto del verbale: deliberate non solo l'<strong>importo</strong> del dividendo, ma anche la sua <strong>scadenza</strong>. Il credito d'imposta preventiva nasce quando la prestazione è esigibile (art. 12 cpv. 1 LIP) e da quel giorno decorrono i termini di 30 giorni per pagamento, dichiarazione ed eventuale procedura di annuncio. Una decisione «dividendo di CHF 50'000, esigibile il 30 giugno 2027» crea chiarezza; senza scadenza, la pianificazione dei termini parte nella nebbia.</p>
<p>A seconda della misura, le decisioni della Sagl sul capitale possono richiedere l'atto pubblico e l'iscrizione a registro di commercio — prevedete tempo a sufficienza. Questo articolo è un aiuto alla pianificazione, non una consulenza legale.</p>"""),
 ("Il calendario 2027: tutte le scadenze in una tabella",
  """<p>Il calendario presuppone una società di capitali con <strong>anno civile</strong> (bilancio al 31.12.2026). Con un esercizio diverso le scadenze slittano di conseguenza.</p>
<table><thead><tr><th>Passo</th><th>Scadenza</th><th>Base legale</th></tr></thead><tbody>
<tr><td>Chiusura del bilancio (anno civile)</td><td>31.12.2026</td><td>Statuto</td></tr>
<tr><td>Convocazione dell'assemblea</td><td>almeno 20 giorni prima (Sagl: statuto fino a 10 giorni)</td><td>art. 700 cpv. 1 / art. 805 cpv. 3 CO</td></tr>
<tr><td>Assemblea ordinaria: approvare i conti, deliberare il dividendo</td><td>entro 6 mesi dalla chiusura, ossia entro il 30.06.2027</td><td>art. 699 cpv. 2 / art. 805 cpv. 2 CO</td></tr>
<tr><td>Dichiarazione all'AFC: conti annuali + distinta ufficiale</td><td>entro 30 giorni dall'approvazione dei conti</td><td>OIP / AFC</td></tr>
<tr><td>Scadenza del dividendo</td><td>secondo la delibera (p. es. 15.06.2027)</td><td>Verbale</td></tr>
<tr><td>Versare l'imposta preventiva (35 %)</td><td>30 giorni dopo la nascita del credito fiscale</td><td>art. 16 cpv. 1 lett. c LIP</td></tr>
<tr><td>Procedura di annuncio nel gruppo: istanza al posto del pagamento</td><td>entro 30 giorni dalla scadenza del dividendo</td><td>art. 20 LIP / AFC</td></tr>
<tr><td>Dichiarazione fiscale: dichiarare il dividendo</td><td>anno fiscale 2027</td><td>art. 20 LIFD</td></tr>
<tr><td>Istanza di rimborso dell'IP (se non via tassazione)</td><td>al più presto dopo il 31.12.2027, al più tardi il 31.12.2030</td><td>art. 29 / art. 32 cpv. 1 LIP</td></tr>
</tbody></table>
<p><strong>Consiglio pratico:</strong> annotate le scadenze in agenda subito dopo l'assemblea — i termini di 30 giorni decorrono dalla scadenza, non dal bonifico. Il <a href="rechner.html">calcolatore fiscale</a> mostra in anticipo quanto resta del dividendo dopo imposta federale, cantonale e IP.</p>"""),
 ("Dopo la delibera: 35 % di imposta preventiva entro 30 giorni",
  """<p>La delibera di distribuzione fa scattare l'<strong>imposta preventiva (IP)</strong> — la società debitrice della prestazione è il soggetto passivo (art. 10 cpv. 1 LIP). Sui dividendi, quali redditi di capitali mobiliari, l'imposta ammonta al <strong>35 per cento della prestazione imponibile</strong> (art. 13 cpv. 1 lett. a LIP). La società deve detrarre l'imposta al momento del pagamento (art. 14 cpv. 1 LIP): all'azionista arriva netto il 65 per cento.</p>
<p>Il credito fiscale nasce quando il dividendo diventa <strong>esigibile</strong> (art. 12 cpv. 1 LIP) e va pagato <strong>30 giorni dopo</strong> (art. 16 cpv. 1 lett. c LIP). L'IP è un'imposta di autodichiarazione: pagamento e rendiconto avvengono d'ufficio, senza solleciti né richieste dell'AFC. In caso di ritardo è dovuto senza diffida un interesse di mora (art. 16 cpv. 2 LIP); l'AFC lo preleva solo a partire da 100 franchi e l'aliquota è fissata ogni anno da un'ordinanza del Dipartimento federale delle finanze.</p>
<p>Da non dimenticare l'<strong>obbligo di dichiarazione</strong>: entro <strong>30 giorni dall'approvazione dei conti annuali</strong>, ogni società di capitali svizzera deve consegnare spontaneamente all'AFC il rapporto di gestione o una copia firmata dei conti annuali nonché una distinta su modulo ufficiale — con il capitale a fine esercizio, la data dell'assemblea generale, la ripartizione dell'utile deliberata e la sua scadenza. L'obbligo scatta in particolare quando la ripartizione deliberata costituisce una prestazione imponibile o quando il totale di bilancio supera i cinque milioni di franchi (OIP, AFC).</p>
<p><strong>Consiglio pratico:</strong> la liquidità per il 35 per cento del dividendo lordo deve essere disponibile 30 giorni dopo la scadenza. In caso di difficoltà, l'AFC può concedere una proroga o rate dietro domanda scritta — da presentare prima della scadenza, non dopo.</p><div class="cta-mid"><strong>Non sapete cosa significa in concreto per la sua situazione?</strong> Un <a href="partner-pruefung.html">consulente verificato</a> esamina i suoi documenti e indica il potenziale di risparmio – primo colloquio gratuito: <a href="kontakt.html">richieda un'offerta senza impegno</a>.</div>"""),
 ("Rimborso: il 35 % torna — ma solo su istanza",
  """<p>Per gli azionisti imponibili in Svizzera l'IP non è un costo definitivo — ma il rimborso non è nemmeno automatico. Chi <strong>dichiara correttamente il dividendo nella dichiarazione fiscale</strong> recupera l'imposta detratta nell'ambito della tassazione. Senza tassazione, l'istanza va presentata per scritto all'AFC — tramite il portale dell'AFC o il modulo elettronico 25.</p>
<p>Due termini legali: l'istanza può essere presentata <strong>al più presto dopo la scadenza dell'anno civile</strong> in cui la prestazione è diventata esigibile (art. 29 cpv. 2 LIP) e <strong>si perime dopo tre anni</strong>: l'istanza va presentata entro tre anni dalla fine dell'anno civile in cui la prestazione imponibile è diventata esigibile (art. 32 cpv. 1 LIP). Per un dividendo esigibile il 15 giugno 2027 il termine scade quindi il <strong>31 dicembre 2030</strong> — dopo, il denaro è definitivamente perso.</p>
<p>La società deve fornire al beneficiario le indicazioni necessarie al rimborso e, su richiesta, un'attestazione (art. 14 cpv. 2 LIP). Approfondimenti nei nostri articoli <a href="verrechnungssteuer-schweiz-35-prozent.html">recuperare il 35 % di imposta preventiva</a> e <a href="verrechnungssteuer-rueckerstattungsfrist-ablauf.html">il termine di rimborso dell'IP</a>.</p>"""),
 ("Salario o dividendi? La check-list del socio-dirigente",
  """<p>L'assemblea è il momento giusto per la domanda di fondo: <strong>salario o dividendi</strong>. Le conseguenze fiscali e contributive differiscono nettamente:</p>
<ul>
<li>Il <strong>salario</strong> è deducibile per la società, sottostà ai contributi AVS/AI/IPG e AD ed è pienamente imponibile per il beneficiario — ma costituisce anche diritti di rendita.</li>
<li>I <strong>dividendi</strong> sono rendimento della sostanza esente da contributi e sono imposti solo parzialmente: a livello federale i dividendi di una partecipazione qualificata (almeno il 10 per cento del capitale azionario o sociale, sostanza privata) sono <strong>imponibili nella misura del 70 per cento</strong> (art. 20 cpv. 1bis LIFD); la stessa aliquota vale per le partecipazioni della sostanza commerciale (art. 18b LIFD). I cantoni impongono tali dividendi <strong>nella misura del 50 per cento</strong> come soglia minima, ma possono prevedere di più (art. 7 cpv. 1 LAID) — l'aliquota effettiva varia da cantone a cantone.</li>
<li><strong>Rischio AVS:</strong> se il salario del dirigente è sproporzionatamente basso e il dividendo manifestamente eccessivo, le casse di compensazione possono riqualificare parte del dividendo come salario soggetto a contributi — il Tribunale federale ha confermato questo superamento persino attraverso una holding senza sostanza nella sentenza <strong>9C_532/2025</strong>. Secondo la prassi amministrativa, un dividendo è presunto eccessivo oltre il 10 per cento del valore fiscale delle azioni; i recuperi coprono cinque anni. Dettagli nell'articolo <a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">Dividendi invece del salario: la sentenza del TF</a>.</li>
</ul>
<p><strong>Check-list prima della delibera di distribuzione:</strong></p>
<ol>
<li>Il salario del dirigente regge il confronto settoriale (grado di occupazione, responsabilità, Salarium)?</li>
<li>Il dividendo resta sotto la soglia critica del 10 per cento del valore fiscale delle azioni?</li>
<li>Quale effetto ha l'imposizione parziale nel cantone di domicilio? Verificate con il <a href="rechner.html">calcolatore fiscale</a>.</li>
<li>La liquidità per l'IP (35 per cento) è assicurata 30 giorni dopo la scadenza?</li>
<li>Importo, scadenza e votazioni figurano correttamente nel verbale?</li>
</ol>"""),
 ("Esempio di calcolo: distribuzione di una SA del proprietario",
  """<div class="cta-mid"><strong>Esempio di calcolo (cifre fittizie):</strong> l'azionista unica detiene il 100 per cento della X SA nella sostanza privata; l'assemblea delibera il 10 giugno 2027 un dividendo di <strong>CHF 100'000</strong>, esigibile il 15 giugno 2027.<br><br>
<strong>Società:</strong> imposta preventiva 35 per cento = CHF 35'000, esigibile 30 giorni dopo la nascita del credito fiscale (entro il 15 luglio 2027); versamento netto all'azionista CHF 65'000. Dichiarazione (conti annuali + distinta ufficiale) entro 30 giorni dall'approvazione dei conti.<br><br>
<strong>Azionista:</strong> dichiara CHF 100'000 nella dichiarazione fiscale 2027. Confederazione: imponibile il 70 per cento = CHF 70'000 (art. 20 cpv. 1bis LIFD). Cantone: 50 per cento = CHF 50'000 come minimo, di più a seconda del cantone (art. 7 cpv. 1 LAID). L'IP di CHF 35'000 torna via tassazione — in mancanza, su istanza all'AFC al più tardi entro il 31.12.2030 (art. 32 cpv. 1 LIP).<br><br>
<em>Esempio illustrativo senza garanzia; il carico effettivo dipende da cantone, comune e altri redditi.</em></div>"""),
 ("Delibere parallele: aumento di capitale, riserve da apporti, procedura di annuncio",
  """<p>All'ordine del giorno figurano spesso misure sul capitale — con proprie conseguenze fiscali:</p>
<ul>
<li><strong>Aumento di capitale:</strong> la tassa d'emissione ammonta all'<strong>1 per cento</strong> della controprestazione che confluisce alla società, ma almeno del valore nominale (art. 8 cpv. 1 LTB). È eccettuata l'emissione a titolo oneroso di diritti di partecipazione in SA, società in accomandita per azioni e Sagl, fintanto che gli apporti dei soci non superano complessivamente <strong>un milione di franchi</strong> (art. 6 cpv. 1 lett. h LTB). Chi pianifica un aumento dovrebbe sfruttare deliberatamente questa franchigia.</li>
<li><strong>Riserve provenienti da apporti di capitale (RAAC):</strong> la restituzione di apporti, agi e supplementi versati dopo il 31.12.1996 è trattata come la restituzione del capitale azionario o sociale (art. 20 cpv. 3 LIFD) — dunque senza imposta sul reddito e senza IP. Condizione: le riserve devono figurare in un <strong>conto separato</strong> del bilancio commerciale e ogni modifica va annunciata all'AFC con il <strong>modulo 170</strong>. Senza questa prova non vi sono RAAC e la restituzione diventa imponibile al momento del versamento (prassi AFC). Per le società quotate valgono regole di distribuzione supplementari (art. 20 cpv. 4 LIFD).</li>
<li><strong>Procedura di annuncio nel gruppo:</strong> per i dividendi in rapporti di gruppo nazionali e transfrontalieri l'obbligo fiscale può essere adempiuto mediante <strong>annuncio invece del versamento</strong> (art. 20 LIP) — il 35 per cento non deve essere prefinanziato. L'istanza va depositata entro 30 giorni dalla scadenza del dividendo con i moduli 106, 108, 102, 103 e 110 nonché i conti annuali; se il termine è mancato, la procedura è comunque concessa, con riserva di una multa d'ordine (art. 64 LIP, AFC).</li>
</ul>"""),
 ("In breve",
  """<ul>
<li>Assemblea generale ordinaria / assemblea dei soci: entro sei mesi dalla chiusura dell'esercizio — per il 2026 dunque entro il 30.06.2027 (art. 699 cpv. 2 / art. 805 cpv. 2 CO).</li>
<li>Delibera sul dividendo: importo <em>e scadenza</em> a verbale — la scadenza fa decorrere tutti i termini dell'IP.</li>
<li>Imposta preventiva: 35 per cento, pagabili 30 giorni dopo la nascita del credito; dichiarazione dei conti entro 30 giorni dall'approvazione (art. 13 e 16 LIP; OIP/AFC).</li>
<li>Rimborso all'azionista: solo su istanza o con dichiarazione corretta — perenzione dopo tre anni (art. 32 cpv. 1 LIP).</li>
<li>Imposizione parziale: Confederazione 70 per cento dal 10 per cento di partecipazione (art. 20 cpv. 1bis LIFD), cantoni 50 per cento come minimo (art. 7 cpv. 1 LAID).</li>
<li>Prima della delibera, verificare il rapporto salario/dividendi alla luce della sentenza 9C_532/2025 — altrimenti incombe un recupero AVS.</li>
<li>Informazione generale, non consulenza individuale: fate verificare ordine del giorno e pianificazione da un fiduciario o consulente fiscale — <a href="kontakt.html">richiedere consulenza</a>.</li>
</ul>"""),
]

for lang, title, meta, sections, src in [("de", de_title, de_meta, de_sections, SRC_DE),
                                          ("en", en_title, en_meta, en_sections, SRC_EN),
                                          ("fr", fr_title, fr_meta, fr_sections, SRC_FR),
                                          ("it", it_title, it_meta, it_sections, SRC_IT)]:
    assert len(title) <= 40, f"{lang} title {len(title)} chars > 40"
    assert len(meta) <= 158, f"{lang} meta {len(meta)} chars > 158"
    assert 8 <= len(sections) <= 10, f"{lang} sections {len(sections)}"
    build(lang, SLUG, title, meta, sections, related=RELATED, sources=src)
print("done")
