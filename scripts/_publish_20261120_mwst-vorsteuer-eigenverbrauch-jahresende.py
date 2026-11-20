#!/usr/bin/env python3
# Build mwst-vorsteuer-eigenverbrauch-jahresende in de/en/fr/it via article_template
# (cron 2026-11-20; picker pick; worked examples + canton table computed with
#  scripts/tax_engine.js — see mwst_calc_20261120.js output)
import sys, os
REPO = "/Users/pino/Code/steuerberatung.ch"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import article_template as at

SLUG = "mwst-vorsteuer-eigenverbrauch-jahresende"

FEDLEX = "https://www.fedlex.admin.ch/eli/cc/2010/632/de"
PDF_LAW = "https://www.estv.admin.ch/dam/de/sd-web/sc4WgPZIIElS/21019-mwstg-mit-aenderungen-de.pdf"
PDF_LOHNA = "https://www.estv.admin.ch/dam/de/sd-web/afP1GDFr8gE3/dbst-form-lohna-wegleitung-2026-de.pdf"
P_MITTEIL = "https://www.estv.admin.ch/de/mitteilungen-mehrwertsteuer"
P_JAHRES = "https://www.estv.admin.ch/de/mwst-jahresabstimmung"

TABLE_ROWS = [("SZ", "10’183", "11’034", "851", "17,5 %", "17.5%"),
              ("LU", "12’684", "13’697", "1’013", "20,8 %", "20.8%"),
              ("ZH", "13’326", "14’567", "1’241", "25,5 %", "25.5%"),
              ("TI", "16’629", "18’075", "1’446", "29,8 %", "29.8%"),
              ("BE", "19’769", "21’300", "1’531", "31,5 %", "31.5%"),
              ("VD", "18’931", "20’521", "1’590", "32,7 %", "32.7%")]

def table(headers, idx_pct):
    rows = "".join(
        f"<tr><td>{c}</td><td>CHF {a}</td><td>CHF {b}</td><td><strong>+CHF {d}</strong></td><td>{p}</td></tr>"
        for c, a, b, d, *_ in TABLE_ROWS for p in (row_pct(c, idx_pct),))
    def row_pct(c, i):  # helper inline (never called standalone)
        return [r[4] if i == 0 else r[5] for r in TABLE_ROWS if r[0] == c][0]
    return ('<table><thead><tr>' + "".join(f"<th>{h}</th>" for h in headers) +
            '</tr></thead><tbody>' + rows + '</tbody></table>')

SRC = {
 "de": [(FEDLEX, "MWSTG (SR 641.20) – Bundesgesetz über die Mehrwertsteuer, konsolidierte Fassung"),
        (PDF_LAW, "ESTV: MWSTG mit Änderungen (PDF; Art. 22, 31–33, 42, 71–72, 79, 86–88)"),
        (PDF_LOHNA, "ESTV: Wegleitung 2026 zum Lohnausweis (Privatanteil Geschäftsfahrzeug)"),
        (P_MITTEIL, "ESTV: Mitteilungen Mehrwertsteuer (Pauschale 0,9 % ab 1.1.2022)"),
        (P_JAHRES, "ESTV: MWST-Jahresabstimmung und Berichtigungsabrechnung (240 Tage)")],
 "en": [(FEDLEX, "VAT Act (MWSTG, SR 641.20) – consolidated text"),
        (PDF_LAW, "ESTV: VAT Act with amendments (PDF; Art. 22, 31–33, 42, 71–72, 79, 86–88)"),
        (PDF_LOHNA, "ESTV: Instructions 2026 for the salary certificate (private-use component of business vehicles)"),
        (P_MITTEIL, "ESTV: VAT circulars (0.9% flat rate from 1 Jan 2022)"),
        (P_JAHRES, "ESTV: VAT annual reconciliation and corrective settlement (240 days)")],
 "fr": [(FEDLEX, "LTVA (MWSTG, RS 641.20) – texte consolidé"),
        (PDF_LAW, "AFC : LTVA avec modifications (PDF ; art. 22, 31–33, 42, 71–72, 79, 86–88)"),
        (PDF_LOHNA, "AFC : instructions 2026 pour le certificat de salaire (part privée des véhicules de fonction)"),
        (P_MITTEIL, "AFC : communications TVA (forfait de 0,9 % dès le 1.1.2022)"),
        (P_JAHRES, "AFC : révision annuelle TVA et décompte rectificatif (240 jours)")],
 "it": [(FEDLEX, "LIVA (MWSTG, RS 641.20) – testo consolidato"),
        (PDF_LAW, "AFC: LIVA con modifiche (PDF; art. 22, 31–33, 42, 71–72, 79, 86–88)"),
        (PDF_LOHNA, "AFC: istruzioni 2026 per il certificato di salario (quota privata dei veicoli aziendali)"),
        (P_MITTEIL, "AFC: comunicazioni IVA (forfait dello 0,9 % dal 1.1.2022)"),
        (P_JAHRES, "AFC: revisione annuale IVA e conteggio rettificativo (240 giorni)")],
}

TITLE = {
 "de": "MWST-Korrekturen per Jahresende: Eigenverbrauch, private Nutzung und Vorsteueranpassung",
 "en": "Year-End VAT Corrections: Self-Consumption, Private Use and Input Tax Adjustments",
 "fr": "Corrections TVA de fin d’année : consommation propre, usage privé et régularisation de l’impôt préalable",
 "it": "Correzioni IVA di fine anno: consumo proprio, uso privato e rettifica dell’imposta precedente",
}
META = {
 "de": "Firmenwagen privat genutzt, Kundengeschenke, teils vermietete Geschäftsliegenschaft: Wo Unternehmen 2026 die Vorsteuer korrigieren und den Eigenverbrauch abrechnen müssen — Pauschalen, Grenzen, Fristen via ePortal.",
 "en": "Business cars used privately, customer gifts, partly rented business premises: where companies must correct input tax and settle self-consumption in 2026 — flat rates, thresholds and deadlines via the ePortal.",
 "fr": "Véhicules de société utilisés à titre privé, cadeaux aux clients, immeubles commerciaux à usage mixte : où les entreprises doivent régulariser l’impôt préalable et déclarer la consommation propre en 2026 — forfaits, limites et délais via le portail ePortal.",
 "it": "Auto aziendali usate anche privatamente, regali ai clienti, immobili commerciali ad uso misto: dove le aziende nel 2026 devono rettificare l’imposta precedente e conteggiare il consumo proprio — forfette, soglie e termini tramite ePortal.",
}

CONTENT = {
"de": [
("Warum sich die MWST-Jahresabstimmung jetzt lohnt",
 """<p>Jede quartalsweise abrechnende MWST-pflichtige Person muss den Abrechnungsblock für das <strong>3. Quartal 2026 (Juli bis September)</strong> innert 60 Tagen einreichen und die Steuer in derselben Frist zahlen – <strong>Stichtag ist der 30. November 2026</strong> (Art. 71 Abs. 1 und Art. 86 Abs. 1 MWSTG). Wer nachträglich vergessene Korrekturen entdeckt – etwa nicht gemeldeten Eigenverbrauch –, berichtigt sie in dieser Abrechnung. Die ESTV mahnt nicht vorher; die 60-Tage-Regel gilt automatisch für jede Periode (Details: <a href="mwst-abrechnung-fristen.html">MWST-Abrechnung: Fristen pro Periode</a>).</p>
<p>Zur Jahresabstimmung gehört der Abgleich der MWST-Abrechnungen mit dem Jahresabschluss: Erkannte Mängel sind spätestens in jener Abrechnung zu korrigieren, in die der <strong>180. Tag nach Ende des Geschäftsjahres</strong> fällt (Art. 72 MWSTG) – bei Geschäftsjahren nach Kalenderjahr also bis Ende Juni des Folgejahres.</p>
<p>Die ESTV ihrerseits schliesst ab: Bleibt eine Berichtigungsabrechnung <strong>binnen 240 Tagen nach Geschäftsjahresende</strong> aus, geht sie davon aus, dass die Abrechnungen vollständig und korrekt sind, und finalisiert die Steuerperiode. Nachträgliche Korrekturen zugunsten des Unternehmens werden dann deutlich aufwendiger.</p>
<p><strong>Praxistipp:</strong> Legen Sie den Abschluss-Termin mit der Buchhaltung auf Ende November. Korrekturen aus Eigenverbrauch, Geschenken und Nutzungsänderungen landen so in der 30.11.-Abrechnung – statt in einer Berichtigungsabrechnung des Folgejahres, auf der zudem Verzugszins laufen kann.</p>"""),

("Geschäftsfahrzeuge: 0,9 % pro Monat als Pauschale für die private Nutzung",
 """<p>Darf ein Arbeitnehmer das Geschäftsfahrzeug auch privat benutzen, liegt aus MWST-Sicht eine Entnahme vor: Die private Nutzung ist <strong>Eigenverbrauch nach Art. 31 Abs. 2 MWSTG</strong> und zum Normalsatz (seit 2024: 8,1 %) abzurechnen. Anerkannt ist die mit dem Lohnausweis abgestimmte Pauschale: <strong>0,9 % des Kaufpreises pro Monat</strong> – inklusive Sonderausstattungen, exklusive MWST –, wie die ESTV seit dem 1. Januar 2022 anwendet (zuvor 0,8 %). Bei Fahrzeugen mit einem Kaufpreis unter CHF 16’667 gilt ein Mindestansatz von CHF 150 pro Monat.</p>
<p>Rechenbeispiel: Ein Neuwagen kostet CHF 45’000 ohne MWST. Der Privatanteil beträgt 0,9 % × CHF 45’000 = CHF 405 pro Monat, also <strong>CHF 4’860 pro Jahr</strong>. Pro Quartal (Bemessungsgrundlage CHF 1’215) schuldet das Unternehmen 8,1 % = <strong>CHF 98,42</strong>, aufs Jahr <strong>CHF 393,66</strong> – deklariert in jeder ordentlichen Abrechnung. Wer weniger private Nutzung hat, kann tiefer abrechnen, muss sie dann aber sauber belegen (Fahrtenbuch).</p>
<p><strong>Praxistipp:</strong> Die Pauschale hat eine Doppelwirkung – derselbe Privatanteil steht als Lohnbestandteil in Ziffer 2.2 des Lohnausweises (mit AHV-/IV/EO-/ALV-Pflicht) und als Eigenverbrauch in der MWST-Abrechnung. Prüfen Sie per Jahresende beide Stellen: Oft wird der Lohnausweis aktualisiert, die MWST-Seite aber vergessen.</p>"""),

("Der Privatanteil wirkt auch in der Einkommensteuer – mit grossen kantonalen Unterschieden",
 """<p>Für die angesetzte Person ist der Privatanteil steuerbares Gehalt. Wie stark er die Rechnung erhöht, hängt vom Wohnort ab. Die Tabelle zeigt die Zusatzsteuer auf einem Beispiel von <strong>CHF 4’860 Privatanteil</strong> zu einem steuerbaren Einkommen von CHF 90’000 (ledig, keine Kinder; berechnet mit dem hauseigenen Steuerrechner, Stand 2026, Bund/Kanton/Gemeinde, ohne Sozialversicherungsbeiträge).</p>""" +
 """<table><thead><tr><th>Kanton</th><th>Steuer ohne Privatanteil</th><th>Steuer mit Privatanteil</th><th>Zusatzsteuer</th><th>Grenzsatz</th></tr></thead><tbody><tr><td>SZ</td><td>CHF 10’183</td><td>CHF 11’034</td><td><strong>+CHF 851</strong></td><td>17,5 %</td></tr><tr><td>LU</td><td>CHF 12’684</td><td>CHF 13’697</td><td><strong>+CHF 1’013</strong></td><td>20,8 %</td></tr><tr><td>ZH</td><td>CHF 13’326</td><td>CHF 14’567</td><td><strong>+CHF 1’241</strong></td><td>25,5 %</td></tr><tr><td>TI</td><td>CHF 16’629</td><td>CHF 18’075</td><td><strong>+CHF 1’446</strong></td><td>29,8 %</td></tr><tr><td>BE</td><td>CHF 19’769</td><td>CHF 21’300</td><td><strong>+CHF 1’531</strong></td><td>31,5 %</td></tr><tr><td>VD</td><td>CHF 18’931</td><td>CHF 20’521</td><td><strong>+CHF 1’590</strong></td><td>32,7 %</td></tr></tbody></table>
<p>Beim identischen Lohnausweis kostet der Privatanteil in Schwyz knapp CHF 850, im Waadtland rund CHF 1’590 – fast das Doppelte. Für Mitarbeitende mit Firmenwagen lohnt sich die Frage, ob das Fahrzeug ganz oder nur teilweise privat freigegeben wird; für Arbeitgebende ist der Grenzsatz Teil der Verhandlung über Naturallohn versus Barlohn.</p>
<div class="cta-mid"><strong>Simulieren Sie Ihren Fall:</strong> Mit dem <a href="rechner.html">Steuerrechner</a> prüfen Sie in einer Minute, was ein Zusatzbetrag von CHF 4’860 in Ihrer Gemeinde kostet. Für die saubere Aufteilung von Naturallohn und Spesen lohnt sich eine <a href="partner-pruefung.html">geprüfte Fachperson</a>: <a href="kontakt.html">unverbindliche Offerte anfragen</a>.</div>
<p><strong>Praxistipp:</strong> Geben Sie Fahrzeug-Privatanteile immer mit dem Monatswert im laufenden Lohnausweis an – retroaktive Korrekturen im Dezember verändern die AHV-Lohnsummenmeldung und die Quellensteuer nachträglich.</p>"""),

("Kundengeschenke: Freigrenze CHF 500 pro Person und Jahr",
 """<p>Präsentkorb, Wein, Give-aways: Unentgeltliche Abgaben aus dem Unternehmen gelten grundsätzlich als Eigenverbrauch – <strong>Ausnahme gemäss Art. 31 Abs. 2 Bst. c MWSTG</strong>: Bei Geschenken bis <strong>CHF 500 pro Person und Kalenderjahr</strong> (Wert ohne MWST) wird der unternehmerische Grund ohne Weiteres angenommen; es fällt keine MWST an. Gleiches gilt für Werbegeschenke und Warenmuster zur Erzielung steuerbarer Umsätze.</p>
<p>Wer die Grenze überschreitet, versteuert den <strong>vollen Betrag</strong> im Eigenverbrauch – nicht nur den überschiessenden Teil. Beispiel: Ein Kundengeschenk im Einkaufswert von CHF 600 kostet bei 8,1 % rund CHF 48,60 MWST. Identisch hoch ist die Grenze im Gewinnsteuerrecht: Auch dort sind Kundengeschenke nur bis CHF 500 pro Empfänger und Jahr abzugsfähig.</p>
<p><strong>Praxistipp:</strong> Führen Sie zu Weihnachten eine Geschenkeliste nach Empfänger und addieren Sie alle Zuwendungen des Kalenderjahres. Die Grenze gilt „pro Person und Jahr“ – zwei Geschenke à CHF 300 an dieselbe Person sind bereits voll steuerbar.</p>"""),

("Nutzungsänderung bei Geschäftsliegenschaften: die Korrektur über 20 Jahre",
 """<p>Auch bei Liegenschaften entscheidet die tatsächliche Nutzung über den Vorsteuerabzug: Fallen die Voraussetzungen nachträglich weg – etwa weil ein bisher steuerbar genutztes Büro künftig zu Wohnzwecken steuerbefreit und ohne Option vermietet wird –, ist die abgezogene Vorsteuer zeitwertig zurückzuzahlen (Art. 31 Abs. 1 und 3 MWSTG). Die ESTV kürzt pro abgelaufenem Jahr linear um <strong>einen Zwanzigstel bei Liegenschaften</strong> (Korrektur über 20 Jahre zu je 5 %) und um <strong>einen Fünftel bei beweglichen Gegenständen und Dienstleistungen</strong> (5 Jahre). Die buchmässige Behandlung ist nicht massgebend.</p>
<p>Rechenbeispiel: Ein Unternehmen erstellt 2019 ein Bürogebäude; Baukosten CHF 2 Mio. ohne MWST, abzogene Vorsteuer CHF 154’000 (Satz von 2019: 7,7 %). Per 1. Januar 2026 werden 40 % der Fläche steuerbefreit an Private vermietet. Bemessung: 40 % von CHF 154’000 = CHF 61’600; 7 abgelaufene Jahre (2019–2025) kürzen um 35 %, es bleiben 65 % → zurückzuzahlen sind <strong>CHF 40’040</strong> – zu korrigieren in der Abrechnung jener Periode, in der die Nutzungsänderung eintritt.</p>
<p>In die Gegenrichtung wirkt die <strong>Einlageentsteuerung</strong> (Art. 32 MWSTG): Tritt die Abzugsberechtigung erst später ein, kann die Vorsteuer nach demselben Zeitwert-Mechanismus nachträglich geltend gemacht werden. Und wer eine steuerbefreite Vermietung doch im MWST-System behalten will, kann die Leistung optional steuerbar erklären (Art. 22 MWSTG) – dann bleibt der Abzug bestehen. <strong>Praxistipp:</strong> Belege zur Nutzung von Geschäftsliegenschaften mindestens 20 Jahre aufbewahren – die übliche zehnjährige Aufbewahrungsfrist genügt für diese Korrekturen nicht.</p>"""),

("Jahresend-Checkliste: MWST-Korrekturen fristgerecht und zinsfrei erledigen",
 """<ul>
<li><strong>Bis 30. November 2026:</strong> Q3-Abrechnung einreichen und zahlen – nachträgliche Eigenverbrauchskorrekturen (Fahrzeuge, Geschenke, Mischkosten) gehören in diese Abrechnung.</li>
<li><strong>Jahresabstimmung:</strong> MWST-Abrechnungen mit dem Jahresabschluss abgleichen; erkannte Mängel spätestens in der Abrechnung mit dem 180. Tag nach Geschäftsjahresende korrigieren (Art. 72 MWSTG).</li>
<li><strong>240-Tage-Praxis der ESTV</strong> im Blick: Danach gilt die Periode als finalisiert – Korrekturen zu Ihren Gunsten sind dann nur noch mit Aufwand möglich.</li>
<li><strong>Verzug kostet:</strong> Verzugszins ohne Mahnung (Art. 87 MWSTG), eine Einschätzung der Steuerforderung mangels Aufzeichnungen (Art. 79 MWSTG) und Bussen nach den Strafbestimmungen (Art. 96 ff. MWSTG). Das Recht, Steuerforderungen festzusetzen, verjährt übrigens erst nach fünf Jahren (Art. 42 MWSTG) – Wegschauen hilft nicht.</li>
<li><strong>Zugänge prüfen:</strong> Seit 31. Oktober 2026 läuft die MWST-Abrechnung obligatorisch über AGOV (<a href="mwst-agov-pflicht-oktober-2026.html">AGOV-Pflicht: so melden Sie sich an</a>).</li>
<li><strong>Satzwechsel planen:</strong> Zur AHV-Finanzierung soll der Normalsatz auf 8,5 % steigen – was das für Ihre Abrechnungen bedeutet, zeigt <a href="mwst-erhoehung-2027-ahv-armee.html">dieser Beitrag</a>.</li>
</ul>
<p>Ob Firmenwagen, Weihnachtspräsent oder Umnutzung der Ladenfläche – die Jahresendkorrekturen sind Kleinarbeit mit grosser Hebelwirkung, weil sich Fehler sofort in barer MWST-Zahlung bemerkbar machen. Prüfen Sie die drei Klassiker dieses Artikels (Fahrzeugpauschale, Geschenkeliste, Nutzungsänderungen) vor dem 30. November; bei Liegenschaftsfällen lohnt sich vorgängig eine <a href="kontakt.html">Nachfrage bei einer geprüften Fachperson</a>.</p>"""),
],

"en": [
("Why the year-end VAT reconciliation is due now",
 """<p>Every VAT-liable person filing quarterly must submit the settlement block for the <strong>third quarter of 2026 (July–September)</strong> within 60 days and pay the tax within the same period – <strong>the deadline is 30 November 2026</strong> (Art. 71 para. 1 and Art. 86 para. 1 VAT Act). Corrections discovered late – e.g. undeclared self-consumption – are simply reported in this settlement. The ESTV does not send reminders; the 60-day rule applies automatically to every period (details: <a href="mwst-abrechnung-fristen.html">VAT settlements: deadlines per period</a>).</p>
<p>Year-end reconciliation means comparing your VAT settlements with the annual financial statements: deficiencies identified must be corrected no later than in the settlement covering the <strong>180th day after the end of the business year</strong> (Art. 72 VAT Act) – i.e. by the end of June the following year for calendar business years.</p>
<p>The ESTV closes the book as well: if no corrective settlement arrives <strong>within 240 days after the end of the business year</strong>, it assumes the settlements were complete and correct and finalises the tax period. Later corrections in the company's favour then become considerably more laborious.</p>
<p><strong>Practical tip:</strong> Set the closing date with your bookkeeping team at the end of November. Corrections for self-consumption, gifts and change of use then land in the 30.11. settlement – rather than in a corrective settlement the following year, which can also trigger default interest.</p>"""),

("Business vehicles: the 0.9% per month flat rate for private use",
 """<p>If an employee may use a business vehicle privately, this constitutes a withdrawal from the business in VAT terms: the private use is <strong>self-consumption under Art. 31 para. 2 VAT Act</strong>, taxable at the standard rate (8.1% since 2024). Accepted is the flat rate aligned with the salary certificate: <strong>0.9% of the purchase price per month</strong> – including special equipment, excluding VAT – as applied by the ESTV since 1 January 2022 (previously 0.8%). For vehicles with a purchase price below CHF 16,667, a minimum of CHF 150 per month applies.</p>
<p>Worked example: a new car costs CHF 45’000 net of VAT. The private-use component is 0.9% × CHF 45’000 = CHF 405 per month, i.e. <strong>CHF 4’860 per year</strong>. Per quarter (tax base CHF 1,215) the company owes 8.1% = <strong>CHF 98.42</strong>, or <strong>CHF 393.66</strong> per year – reported in each ordinary settlement. Anyone with less private use may declare a lower amount but must document it properly (mileage log).</p>
<p><strong>Practical tip:</strong> The flat rate has a double effect – the same private-use component appears as salary item 2.2 on the salary certificate (subject to AHV/IV/EO/ALV contributions) and as self-consumption in the VAT settlement. Check both positions at year-end: in practice the salary certificate gets updated and the VAT side is forgotten.</p>"""),

("The private-use component also affects income tax – with large cantonal differences",
 """<p>For the employee, the private-use component is taxable salary. How much it adds to the bill depends on the canton of residence. The table shows the additional tax on a sample <strong>CHF 4’860 private-use component</strong> added to a taxable income of CHF 90,000 (single, no children; calculated with this website's own tax calculator, 2026 status, federal/cantonal/municipal, excluding social security contributions).</p>""" +
 """<table><thead><tr><th>Canton</th><th>Tax without component</th><th>Tax with component</th><th>Additional tax</th><th>Marginal rate</th></tr></thead><tbody><tr><td>SZ</td><td>CHF 10,183</td><td>CHF 11,034</td><td><strong>+CHF 851</strong></td><td>17.5%</td></tr><tr><td>LU</td><td>CHF 12,684</td><td>CHF 13,697</td><td><strong>+CHF 1,013</strong></td><td>20.8%</td></tr><tr><td>ZH</td><td>CHF 13,326</td><td>CHF 14,567</td><td><strong>+CHF 1,241</strong></td><td>25.5%</td></tr><tr><td>TI</td><td>CHF 16,629</td><td>CHF 18,075</td><td><strong>+CHF 1,446</strong></td><td>29.8%</td></tr><tr><td>BE</td><td>CHF 19,769</td><td>CHF 21,300</td><td><strong>+CHF 1,531</strong></td><td>31.5%</td></tr><tr><td>VD</td><td>CHF 18,931</td><td>CHF 20,521</td><td><strong>+CHF 1,590</strong></td><td>32.7%</td></tr></tbody></table>
<p>With an identical salary certificate, the private-use component costs just under CHF 850 in Schwyz and about CHF 1,590 in Vaud – nearly double. For employees with a company car, it is worth asking whether the vehicle should be released for full or only partial private use; for employers, the marginal rate is part of the negotiation between fringe benefit and cash salary.</p>
<div class="cta-mid"><strong>Run your own numbers:</strong> the <a href="rechner.html">tax calculator</a> shows in one minute what an extra CHF 4,860 costs in your municipality. For a clean split between fringe benefits and expenses, a <a href="partner-pruefung.html">verified professional</a> is worth it: <a href="kontakt.html">request a non-binding quote</a>.</div>
<p><strong>Practical tip:</strong> Always report vehicle private-use components as the monthly value in the ongoing payroll – retroactive December corrections change the annual AHV salary statement and source tax afterwards.</p>"""),

("Customer gifts: the CHF 500 allowance per person per year",
 """<p>Gift baskets, wine, giveaways: gratuitous transfers from the business are in principle self-consumption – <strong>exception under Art. 31 para. 2 lit. c VAT Act</strong>: for gifts up to <strong>CHF 500 per person per calendar year</strong> (value net of VAT) the business reason is presumed without further ado and no VAT is due. The same applies to advertising gifts and samples used to generate taxable turnover.</p>
<p>Anyone exceeding the threshold taxes the <strong>full amount</strong> as self-consumption – not just the excess. Example: a customer gift with a purchase value of CHF 600 costs about CHF 48.60 in VAT at 8.1%. The profit-tax rules use the same ceiling: customer gifts are deductible only up to CHF 500 per recipient per year.</p>
<p><strong>Practical tip:</strong> At Christmas, keep a gift list per recipient and add up all transfers during the calendar year. The allowance is “per person and year” – two gifts of CHF 300 to the same person are already fully taxable.</p>"""),

("Change of use of business property: the 20-year correction",
 """<p>For real estate too, actual use decides on the input tax deduction: if the requirements lapse afterwards – e.g. because an office previously used for taxable purposes is rented out for private residential use without option, i.e. tax-exempt – the input tax deducted must be repaid at its value in time (Art. 31 paras. 1 and 3 VAT Act). The deduction is reduced linearly by <strong>one twentieth per elapsed year for real estate</strong> (a correction over 20 years, 5% each) and <strong>one fifth for movable assets and services</strong> (5 years). Accounting treatment is irrelevant.</p>
<p>Worked example: a company builds an office in 2019; construction costs CHF 2 million net of VAT, input tax of CHF 154’000 deducted (2019 rate: 7.7%). From 1 January 2026, 40% of the floor space is rented tax-exemptly to private tenants. Calculation: 40% of CHF 154,000 = CHF 61,600; 7 elapsed years (2019–2025) cut 35%, leaving 65% → <strong>CHF 40,040</strong> repayable – corrected in the settlement of the period in which the change of use occurs.</p>
<p>The reverse mechanism is the <strong>tax removal on private assets brought in</strong> (Einlageentsteuerung, Art. 32 VAT Act): if entitlement to the deduction arises only later, input tax can be reclaimed using the same value-in-time mechanism. And a landlord who wants to keep tax-exempt rentals inside the VAT system can opt to declare them taxable (Art. 22 VAT Act) – the deduction then remains intact. <strong>Practical tip:</strong> keep documentation on the use of business property for at least 20 years – the usual ten-year retention period is not enough for these corrections.</p>"""),

("Year-end checklist: VAT corrections on time and interest-free",
 """<ul>
<li><strong>By 30 November 2026:</strong> file and pay the Q3 settlement – late self-consumption corrections (vehicles, gifts, mixed costs) belong in this settlement.</li>
<li><strong>Year-end reconciliation:</strong> compare VAT settlements with the financial statements; correct deficiencies no later than in the settlement containing the 180th day after the end of the business year (Art. 72 VAT Act).</li>
<li><strong>Keep the ESTV's 240-day practice</strong> in view: after that the period counts as finalised – corrections in your favour then require considerably more effort.</li>
<li><strong>Delay costs money:</strong> default interest without reminder (Art. 87 VAT Act), an assessed tax claim where records are missing (Art. 79 VAT Act) and fines under the criminal provisions (Art. 96 et seq. VAT Act). The right to assess tax claims only becomes time-barred after five years (Art. 42 VAT Act) – ignoring the issue does not help.</li>
<li><strong>Check access:</strong> since 31 October 2026, VAT settlements run mandatorily via AGOV (<a href="mwst-agov-pflicht-oktober-2026.html">AGOV requirement: how to log in</a>).</li>
<li><strong>Plan for the rate change:</strong> to finance the AHV, the standard rate is set to rise to 8.5% – <a href="mwst-erhoehung-2027-ahv-armee.html">this article</a> shows what it means for your settlements.</li>
</ul>
<p>Whether company car, Christmas present or the conversion of shop space – year-end corrections are small-scale work with big leverage, because mistakes turn into cash VAT payments immediately. Check the three classics in this article (vehicle flat rate, gift list, change of use) before 30 November; for real-estate cases, consult a <a href="kontakt.html">verified professional</a> beforehand.</p>"""),
],

"fr": [
("Pourquoi la régularisation TVA de fin d’année tombe maintenant",
 """<p>Toute personne assujettie qui décompte par trimestre doit déposer le décompte du <strong>3<sup>e</sup> trimestre 2026 (juillet à septembre)</strong> dans les 60 jours et payer la taxe dans le même délai – <strong>date limite : le 30 novembre 2026</strong> (art. 71 al. 1 et art. 86 al. 1 LTVA). Les corrections oubliées découvertes après coup – par exemple une consommation propre non déclarée – sont régularisées dans ce décompte. L’AFC ne rappelle pas avant l’échéance ; la règle des 60 jours s’applique automatiquement à chaque période (détails : <a href="mwst-abrechnung-fristen.html">Décomptes TVA : délais par période</a>).</p>
<p>La révision annuelle consiste à comparer les décomptes TVA avec les comptes annuels : les défauts constatés doivent être corrigés au plus tard dans le décompte couvrant le <strong>180<sup>e</sup> jour suivant la fin de l’exercice</strong> (art. 72 LTVA), soit fin juin de l’année suivante pour un exercice coïncidant avec l’année civile.</p>
<p>L’AFC clôture de son côté : si aucun décompte rectificatif ne parvient <strong>dans les 240 jours après la fin de l’exercice</strong>, elle présume les décomptes complets et exacts et finalise la période fiscale. Des corrections ultérieures en faveur de l’entreprise deviennent alors nettement plus fastidieuses.</p>
<p><strong>Conseil pratique :</strong> fixez la date de clôture avec la comptabilité à fin novembre. Les corrections de consommation propre, de cadeaux et de changement d’affectation arrivent ainsi dans le décompte du 30.11. – au lieu d’un décompte rectificatif de l’année suivante, qui peut en plus entraîner des intérêts moratoires.</p>"""),

("Véhicules de fonction : le forfait de 0,9 % par mois pour l’usage privé",
 """<p>Si un employé peut utiliser le véhicule de fonction à titre privé, il y a prélèvement du patrimoine de l’entreprise : l’usage privé constitue une <strong>consommation propre au sens de l’art. 31 al. 2 LTVA</strong>, à décompter au taux normal (8,1 % depuis 2024). Reconnu est le forfait aligné sur le certificat de salaire : <strong>0,9 % du prix d’achat par mois</strong> – équipements spéciaux inclus, TVA non comprise –, appliqué par l’AFC depuis le 1<sup>er</sup> janvier 2022 (0,8 % auparavant). Pour les véhicules dont le prix d’achat est inférieur à CHF 16’667, un minimum de CHF 150 par mois s’applique.</p>
<p>Exemple chiffré : une voiture neuve coûte CHF 45’000 hors TVA. La part privée représente 0,9 % × CHF 45’000 = CHF 405 par mois, soit <strong>CHF 4’860 par an</strong>. Par trimestre (base d’imposition CHF 1’215), l’entreprise doit 8,1 % = <strong>CHF 98,42</strong>, et <strong>CHF 393,66</strong> sur l’année – à déclarer dans chaque décompte ordinaire. Celui qui démontre un usage privé moindre peut retenir un montant plus bas, à condition de le documenter proprement (journal de bord).</p>
<p><strong>Conseil pratique :</strong> le forfait a un double effet – la même part privée figure comme élément du salaire au chiffre 2.2 du certificat de salaire (soumis aux cotisations AVS/AI/APG/AC) et comme consommation propre dans le décompte TVA. Vérifiez les deux volets en fin d’année : en pratique, on actualise le certificat de salaire et on oublie le volet TVA.</p>"""),

("La part privée pèse aussi sur l’impôt sur le revenu – avec de fortes différences cantonales",
 """<p>Pour la personne imposée, la part privée est un salaire imposable. Son coût dépend du canton de domicile. Le tableau ci-dessous montre l’impôt additionnel sur un exemple de <strong>CHF 4’860 de part privée</strong> ajouté à un revenu imposable de CHF 90’000 (célibataire, sans enfants ; calculé avec le calculateur d’impôts de ce site, état 2026, Confédération/canton/commune, cotisations sociales non comprises).</p>""" +
 """<table><thead><tr><th>Canton</th><th>Impôt sans part privée</th><th>Impôt avec part privée</th><th>Impôt additionnel</th><th>Taux marginal</th></tr></thead><tbody><tr><td>SZ</td><td>CHF 10’183</td><td>CHF 11’034</td><td><strong>+CHF 851</strong></td><td>17,5 %</td></tr><tr><td>LU</td><td>CHF 12’684</td><td>CHF 13’697</td><td><strong>+CHF 1’013</strong></td><td>20,8 %</td></tr><tr><td>ZH</td><td>CHF 13’326</td><td>CHF 14’567</td><td><strong>+CHF 1’241</strong></td><td>25,5 %</td></tr><tr><td>TI</td><td>CHF 16’629</td><td>CHF 18’075</td><td><strong>+CHF 1’446</strong></td><td>29,8 %</td></tr><tr><td>BE</td><td>CHF 19’769</td><td>CHF 21’300</td><td><strong>+CHF 1’531</strong></td><td>31,5 %</td></tr><tr><td>VD</td><td>CHF 18’931</td><td>CHF 20’521</td><td><strong>+CHF 1’590</strong></td><td>32,7 %</td></tr></tbody></table>
<p>À certificat de salaire identique, la part privée coûte un peu moins de CHF 850 à Schwyz et environ CHF 1’590 dans le canton de Vaud – presque le double. Pour les collaborateurs disposant d’une voiture de fonction, la question d’un usage privé total ou partiel vaut d’être posée ; pour l’employeur, le taux marginal fait partie de la négociation entre salaire en nature et salaire en espèces.</p>
<div class="cta-mid"><strong>Calculez votre cas :</strong> le <a href="rechner.html">calculateur d’impôts</a> montre en une minute ce que coûte un supplément de CHF 4’860 dans votre commune. Pour une répartition propre entre salaire en nature et frais, une <a href="partner-pruefung.html">personne qualifiée vérifiée</a> vaut son prix : <a href="kontakt.html">demander une offre sans engagement</a>.</div>
<p><strong>Conseil pratique :</strong> indiquez toujours la part privée des véhicules à la valeur mensuelle dans les certificats de salaire courants – des corrections rétroactives en décembre modifient après coup la déclaration annuelle des salaires AVS et l’impôt à la source.</p>"""),

("Cadeaux aux clients : une franchise de CHF 500 par personne et par an",
 """<p>Panier-cadeau, vin, goodies : les attributions gratuites provenant de l’entreprise valent en principe consommation propre – <strong>exception selon l’art. 31 al. 2 let. c LTVA</strong> : pour les cadeaux jusqu’à <strong>CHF 500 par personne et par année civile</strong> (valeur hors TVA), le motif d’entreprise est admis sans autre ; aucune TVA n’est due. Il en va de même pour les cadeaux publicitaires et les échantillons servant à générer du chiffre d’affaires imposable.</p>
<p>Qui dépasse la limite taxe le <strong>montant intégral</strong> en consommation propre – et non pas seulement l’excédent. Exemple : un cadeau clients d’une valeur d’achat de CHF 600 coûte environ CHF 48,60 de TVA à 8,1 %.</p>
<p><strong>Conseil pratique :</strong> tenez à Noël une liste des cadeaux par destinataire et additionnez toutes les attributions de l’année civile. La limite vaut « par personne et par année » – deux cadeaux de CHF 300 à la même personne sont déjà entièrement imposables.</p>"""),

("Changement d’affectation d’un immeuble commercial : la régularisation sur 20 ans",
 """<p>Pour les immeubles aussi, l’affectation réelle décide du droit à déduction de l’impôt préalable : si les conditions tombent ultérieurement – par exemple parce qu’un bureau jusqu’ici utilisé à des fins imposables est loué sans option à des fins d’habitation, donc exclu du droit à déduction –, l’impôt préalable déduit doit être remboursé selon la valeur résiduelle dans le temps (art. 31 al. 1 et 3 LTVA). La déduction est réduite linéairement de <strong>vingtième par année écoulée pour les immeubles</strong> (régularisation sur 20 ans, 5 % l’an) et de <strong>cinquième pour les biens meubles et les prestations de services</strong> (5 ans). Le traitement comptable n’est pas déterminant.</p>
<p>Exemple chiffré : une entreprise construit un bureau en 2019 ; coûts de construction CHF 2 millions hors TVA, impôt préalable déduit de CHF 154’000 (taux 2019 : 7,7 %). Dès le 1<sup>er</sup> janvier 2026, 40 % des surfaces sont loués à bail d’habitation, sans option. Calcul : 40 % de CHF 154’000 = CHF 61’600 ; 7 années écoulées (2019–2025) réduisent de 35 %, il reste 65 % → <strong>CHF 40’040</strong> à rembourser – à régulariser dans le décompte de la période où le changement d’affectation intervient.</p>
<p>En sens inverse joue la <strong>sortie de régime</strong> sur biens privés (Einlageentsteuerung, art. 32 LTVA) : si le droit à déduction ne naît que plus tard, l’impôt préalable peut être récupéré selon le même mécanisme de valeur résiduelle. Et le bailleur qui veut garder une location exclue dans le système TVA peut l’imposer par option (art. 22 LTVA) – la déduction reste alors acquise. <strong>Conseil pratique :</strong> conservez les justificatifs sur l’affectation des immeubles commerciaux pendant au moins 20 ans – le délai de conservation usuel de dix ans ne suffit pas pour ces régularisations.</p>"""),

("Check-list de fin d’année : corriger la TVA dans les délais et sans intérêts",
 """<ul>
<li><strong>D’ici au 30 novembre 2026 :</strong> déposer et payer le décompte du 3<sup>e</sup> trimestre – les corrections ultérieures de consommation propre (véhicules, cadeaux, coûts mixtes) y figurent.</li>
<li><strong>Révision annuelle :</strong> comparer les décomptes TVA avec les comptes annuels ; corriger les défauts au plus tard dans le décompte couvrant le 180<sup>e</sup> jour après la fin de l’exercice (art. 72 LTVA).</li>
<li><strong>Garder en vue la pratique des 240 jours de l’AFC :</strong> après quoi la période est réputée finalisée – les corrections en votre faveur exigent alors des efforts conséquents.</li>
<li><strong>Le retard coûte :</strong> intérêts moratoires sans rappel (art. 87 LTVA), imposition d’office à défaut de pièces (art. 79 LTVA) et amendes prévues par les dispositions pénales (art. 96 ss LTVA). Du reste, le droit de fixer une créance fiscale ne se prescrit qu’après cinq ans (art. 42 LTVA) – ne rien faire n’y change rien.</li>
<li><strong>Vérifier les accès :</strong> depuis le 31 octobre 2026, les décomptes TVA passent obligatoirement par AGOV (<a href="mwst-agov-pflicht-oktober-2026.html">Obligation AGOV : comment se connecter</a>).</li>
<li><strong>Anticiper le changement de taux :</strong> le taux normal doit passer à 8,5 % pour financer l’AVS – <a href="mwst-erhoehung-2027-ahv-armee.html">cet article</a> explique ce que cela change pour vos décomptes.</li>
</ul>
<p>Qu’il s’agisse de la voiture de société, du cadeau de Noël ou de la transformation d’une surface de vente – les corrections de fin d’année sont un travail de minutie au fort effet de levier, car les erreurs se traduisent immédiatement en TVA à payer. Vérifiez les trois classiques de cet article (forfait véhicule, liste des cadeaux, changements d’affectation) avant le 30 novembre ; pour les cas immobiliers, consultez au préalable une <a href="kontakt.html">personne qualifiée vérifiée</a>.</p>"""),
],

"it": [
("Perché la revisione IVA di fine anno va fatta adesso",
 """<p>Chi versa l’IVA con conteggi trimestrali deve depositare il conteggio del <strong>3<sup>o</sup> trimestre 2026 (luglio–settembre)</strong> entro 60 giorni e pagare l’imposta nello stesso termine – <strong>scadenza il 30 novembre 2026</strong> (art. 71 cpv. 1 e art. 86 cpv. 1 LIVA). Le correzioni scoperte in ritardo – ad esempio un consumo proprio non dichiarato – vanno regolate in questo conteggio. L’AFC non invia solleciti: la regola dei 60 giorni si applica automaticamente a ogni periodo (dettagli: <a href="mwst-abrechnung-fristen.html">Conteggi IVA: termini per periodo</a>).</p>
<p>La revisione annuale consiste nel confrontare i conteggi IVA con il conto annuale: gli errori riscontrati vanno corretti al più tardi nel conteggio che copre il <strong>180<sup>o</sup> giorno dopo la fine dell’esercizio</strong> (art. 72 LIVA), quindi entro fine giugno dell’anno seguente per gli esercizi coincidenti con l’anno civile.</p>
<p>Anche l’AFC chiude: se entro <strong>240 giorni dalla fine dell’esercizio</strong> non perviene alcun conteggio rettificativo, presume che i conteggi siano completi ed esatti e finalizza il periodo fiscale. Correzioni successive a favore dell’azienda diventano allora decisamente più laboriose.</p>
<p><strong>Suggerimento pratico:</strong> fissi la data di chiusura con la contabilità a fine novembre. Le correzioni di consumo proprio, regali e cambi di destinazione confluiscono così nel conteggio del 30.11. – invece che in un conteggio rettificativo dell’anno seguente, su cui possono inoltre maturare interessi moratori.</p>"""),

("Veicoli aziendali: la forfetta dell’0,9 % al mese per l’uso privato",
 """<p>Se un dipendente può usare il veicolo aziendale anche privatamente, dal profilo IVA si ha un prelievo dall’azienda: l’uso privato è <strong>consumo proprio secondo l’art. 31 cpv. 2 LIVA</strong>, da conteggiare all’aliquota normale (8,1 % dal 2024). È riconosciuta la forfetta coordinata con il certificato di salario: <strong>0,9 % del prezzo d’acquisto al mese</strong> – accessori esclusi IVA – applicata dall’AFC dal 1<sup>o</sup> gennaio 2022 (prima 0,8 %). Per veicoli con prezzo d’acquisto inferiore a CHF 16’667 vale un importo minimo di CHF 150 al mese.</p>
<p>Esempio di calcolo: un’auto nuova costa CHF 45’000 IVA esclusa. La quota privata è 0,9 % × CHF 45’000 = CHF 405 al mese, cioè <strong>CHF 4’860 all’anno</strong>. Per trimestre (base d’imposta CHF 1’215) l’azienda deve versare 8,1 % = <strong>CHF 98,42</strong>, su base annua <strong>CHF 393,66</strong> – da dichiarare in ogni conteggio ordinario. Chi documenta un uso privato inferiore (registro di bordo) può dichiarare meno.</p>
<p><strong>Suggerimento pratico:</strong> la forfetta ha un doppio effetto – la stessa quota privata figura come componente del salario al numero 2.2 del certificato di salario (soggetta ai contributi AVS/AI/IPG/AD) e come consumo proprio nel conteggio IVA. A fine anno verifichi entrambi i fronti: in pratica si aggiorna il certificato di salario e si dimentica il lato IVA.</p>"""),

("La quota privata pesa anche sull’imposta sul reddito – con forti differenze cantonali",
 """<p>Per il contribuente la quota privata è salario imponibile. Quanto incide dipende dal cantone di domicilio. La tabella mostra l’imposta aggiuntiva su un esempio di <strong>quota privata di CHF 4’860</strong> aggiunta a un reddito imponibile di CHF 90’000 (non sposato/a, senza figli; calcolata con il calcolatore d’imposta di questo sito, stato 2026, Confederazione/Cantone/Comune, contributi sociali esclusi).</p>""" +
 """<table><thead><tr><th>Cantone</th><th>Imposta senza quota</th><th>Imposta con quota</th><th>Aggiunta</th><th>Aliquota marginale</th></tr></thead><tbody><tr><td>SZ</td><td>CHF 10’183</td><td>CHF 11’034</td><td><strong>+CHF 851</strong></td><td>17,5 %</td></tr><tr><td>LU</td><td>CHF 12’684</td><td>CHF 13’697</td><td><strong>+CHF 1’013</strong></td><td>20,8 %</td></tr><tr><td>ZH</td><td>CHF 13’326</td><td>CHF 14’567</td><td><strong>+CHF 1’241</strong></td><td>25,5 %</td></tr><tr><td>TI</td><td>CHF 16’629</td><td>CHF 18’075</td><td><strong>+CHF 1’446</strong></td><td>29,8 %</td></tr><tr><td>BE</td><td>CHF 19’769</td><td>CHF 21’300</td><td><strong>+CHF 1’531</strong></td><td>31,5 %</td></tr><tr><td>VD</td><td>CHF 18’931</td><td>CHF 20’521</td><td><strong>+CHF 1’590</strong></td><td>32,7 %</td></tr></tbody></table>
<p>A parità di certificato di salario, la quota privata costa poco meno di CHF 850 in Svitto e circa CHF 1’590 nel canton Vaud – quasi il doppio. Per i collaboratori con auto aziendale vale la pena esaminare se il veicolo sia liberato per un uso privato totale o parziale; per il datore di lavoro l’aliquota marginale è parte della trattativa tra retribuzione in natura e salario in denaro.</p>
<div class="cta-mid"><strong>Simuli il suo caso:</strong> il <a href="rechner.html">calcolatore d’imposta</a> mostra in un minuto quanto costa un supplemento di CHF 4’860 nel suo Comune. Per ripartire correttamente retribuzioni in natura e spese accessorie, una <a href="partner-pruefung.html">persona qualificata verificata</a> vale la spesa: <a href="kontakt.html">richieda un’offerta senza impegno</a>.</div>
<p><strong>Suggerimento pratico:</strong> indichi le quote private dei veicoli sempre con il valore mensile nei certificati di salario correnti – correzioni retroattive a dicembre modificano a posteriori la denuncia annuale dei salari AVS e l’imposta alla fonte.</p>"""),

("Regali ai clienti: franchigia di CHF 500 per persona e anno",
 """<p>Cesto natalizio, vino, gadget: le attribuzioni gratuite dall’azienda valgono in principio consumo proprio – <strong>eccezione secondo l’art. 31 cpv. 2 lett. c LIVA</strong>: per regali fino a <strong>CHF 500 per persona e anno civile</strong> (valore IVA esclusa) il motivo aziendale è ammesso senz’altro e non è dovuta alcuna IVA. Lo stesso vale per regali pubblicitari e campioni d’uso volti a generare cifre d’affari imponibili.</p>
<p>Chi supera la soglia tassa l’<strong>importo integrale</strong> come consumo proprio – e non solo l’eccedenza. Esempio: un regalo ai clienti del valore d’acquisto di CHF 600 costa circa CHF 48,60 di IVA all’8,1 %. Il diritto fiscale prevede lo stesso limite per la tassa sull’utile: i regali ai clienti sono deducibili solo fino a CHF 500 per destinatario e anno.</p>
<p><strong>Suggerimento pratico:</strong> a Natale tenga un elenco dei regali per destinatario e sommi tutte le attribuzioni dell’anno civile. La franchigia vale «per persona e anno» – due regali da CHF 300 alla stessa persona sono già interamente imponibili.</p>"""),

("Cambio di destinazione di immobili commerciali: la rettifica su 20 anni",
 """<p>Anche per gli immobili la destinazione effettiva decide il diritto alla deduzione dell’imposta precedente: se i presupposti vengono meno successivamente – ad esempio perché un ufficio finora usato per scopi imponibili è d’ora innanzi locato a scopo abitativo senza opzione, quindi escluso dalla deduzione – l’imposta precedente detratta va rimborsata secondo il valore residuo nel tempo (art. 31 cpv. 1 e 3 LIVA). La deduzione è ridotta linearmente di <strong>un ventesimo per ogni anno trascorso per gli immobili</strong> (rettifica su 20 anni, 5 % l’anno) e di <strong>un quinto per beni mobili e prestazioni di servizi</strong> (5 anni). Il trattamento contabile non è determinante.</p>
<p>Esempio di calcolo: un’azienda costruisce un ufficio nel 2019; costi di costruzione CHF 2 milioni IVA esclusa, imposta precedente detratta CHF 154’000 (aliquota 2019: 7,7 %). Dal 1<sup>o</sup> gennaio 2026 il 40 % delle superfici è locato a scopo abitativo senza opzione. Calcolo: 40 % di CHF 154’000 = CHF 61’600; 7 anni trascorsi (2019–2025) riducono del 35 %, restano il 65 % → rimborsare <strong>CHF 40’040</strong> – da rettificare nel conteggio del periodo in cui avviene il cambio di destinazione.</p>
<p>In direzione opposta agisce la <strong>deimposizione per prestazioni aziendali private</strong> (Einlageentsteuerung, art. 32 LIVA): se il diritto alla deduzione sorge solo più tardi, l’imposta precedente può essere recuperata con lo stesso meccanismo del valore residuo. E chi vuole mantenere nel sistema IVA una locazione esclusa può dichiararla imponibile in via di opzione (art. 22 LIVA) – la deduzione resta così acquisita. <strong>Suggerimento pratico:</strong> conservi le giustificazioni sulla destinazione degli immobili commerciali per almeno 20 anni – l’ordinario termine di conservazione di dieci anni non basta per queste rettifiche.</p>"""),

("Check-list di fine anno: correggere l’IVA nei termini e senza interessi",
 """<ul>
<li><strong>Entro il 30 novembre 2026:</strong> depositare e pagare il conteggio del 3<sup>o</sup> trimestre – le rettifiche successive di consumo proprio (veicoli, regali, costi misti) appartengono a questo conteggio.</li>
<li><strong>Revisione annuale:</strong> confrontare i conteggi IVA con il conto annuale; correggere gli errori al più tardi nel conteggio che copre il 180<sup>o</sup> giorno dopo la fine dell’esercizio (art. 72 LIVA).</li>
<li><strong>Tenga presente la prassi dei 240 giorni dell’AFC:</strong> dopo tale termine il periodo si considera finalizzato – correzioni a suo favore esigono allora sforzi notevoli.</li>
<li><strong>Il ritardo costa:</strong> interessi moratori senza sollecito (art. 87 LIVA), tassazione secondo il potere d’apprezzamento in assenza di contabilità (art. 79 LIVA) e multe secondo le norme penali (art. 96 segg. LIVA). Peraltro il diritto di fissare un credito d’imposta si prescrive solo dopo cinque anni (art. 42 LIVA) – non fare nulla non aiuta.</li>
<li><strong>Verifichi gli accessi:</strong> dal 31 ottobre 2026 i conteggi IVA passano obbligatoriamente per AGOV (<a href="mwst-agov-pflicht-oktober-2026.html">Obbligo AGOV: come registrarsi</a>).</li>
<li><strong>Piani il cambio d’aliquota:</strong> per finanziare l’AVS l’aliquota normale dovrebbe salire all’8,5 % – <a href="mwst-erhoehung-2027-ahv-armee.html">questo contributo</a> mostra cosa cambia per i suoi conteggi.</li>
</ul>
<p>Si tratti dell’auto aziendale, del regalo di Natale o della riconversione di una superficie commerciale – le rettifiche di fine anno sono un lavoro di fino con un grande effetto leva, perché gli errori si trasformano subito in IVA da versare in contanti. Verifichi i tre classici di questo articolo (forfetta veicoli, elenco regali, cambi di destinazione) prima del 30 novembre; per i casi immobiliari consulti preventivamente una <a href="kontakt.html">persona qualificata verificata</a>.</p>"""),
],
}

REL = ["mwst-abrechnung-fristen.html", "mwst-agov-pflicht-oktober-2026.html", "mwst-100k-pflicht-schweiz.html"]

os.chdir(REPO)
for lang in ("de", "en", "fr", "it"):
    secs = CONTENT[lang]
    at.build(lang, SLUG, TITLE[lang], META[lang], secs, related=REL, sources=SRC[lang])
print("build complete:", SLUG)
