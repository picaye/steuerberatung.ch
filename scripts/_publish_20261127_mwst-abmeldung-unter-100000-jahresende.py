#!/usr/bin/env python3
# Build mwst-abmeldung-unter-100000-jahresende in de/en/fr/it via article_template
# (cron 2026-11-27; picker pick; worked Vorsteuer-repayment numbers computed
#  with node against the 8.1% normal rate valid for 2026).
import sys, os
REPO = "/Users/pino/Code/steuerberatung.ch"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import article_template as at

SLUG = "mwst-abmeldung-unter-100000-jahresende"

FEDLEX   = "https://www.fedlex.admin.ch/eli/cc/2010/632/de"
P_ABML   = "https://www.estv.admin.ch/de/mwst-abmelden"
P_PFLEGT = "https://www.estv.admin.ch/de/mwst-steuerpflicht"
P_UEBER  = "https://www.estv.admin.ch/de/mehrwertsteuer"
MI02     = "https://www.swissvat.ch/fileadmin/user_upload/MI02_06.02.2025.pdf"

SRC = {
 "de": [(FEDLEX,   "MWSTG (SR 641.20) – Bundesgesetz über die Mehrwertsteuer, konsolidierte Fassung (Art. 10, 11, 14, 31)"),
        (P_ABML,   "ESTV: Mehrwertsteuer abmelden – Wegfall der obligatorischen Steuerpflicht"),
        (P_PFLEGT, "ESTV: MWST-Steuerpflicht – Befreiung, Verzicht, Unterstellung"),
        (P_UEBER,  "ESTV: Mehrwertsteuer – Übersicht, An- und Abmeldung, Fristen"),
        (MI02,     "ESTV: MWST-Info 02 Steuerpflicht (Ende der Steuerpflicht)")]
,
 "en": [(FEDLEX,   "VAT Act (MWSTG, SR 641.20) – consolidated text (Art. 10, 11, 14, 31)"),
        (P_ABML,   "ESTV: De-registering from VAT – where compulsory liability ceases"),
        (P_PFLEGT, "ESTV: VAT liability – exemption, waiver, voluntary registration"),
        (P_UEBER,  "ESTV: Value added tax – overview, registration and de-registration, deadlines"),
        (MI02,     "ESTV: MWST-Info 02 Tax liability (end of tax liability)")]
,
 "fr": [(FEDLEX,   "LTVA (RS 641.20) – texte consolidé (art. 10, 11, 14, 31)"),
        (P_ABML,   "AFC : se désinscrire de la TVA – fin de l’assujettissement obligatoire"),
        (P_PFLEGT, "AFC : assujettissement à la TVA – exemption, renonciation, imposition volontaire"),
        (P_UEBER,  "AFC : taxe sur la valeur ajoutée – vue d’ensemble, annonce et désinscription, délais"),
        (MI02,     "AFC : TVA-Info 02 Assujettissement (fin de l’assujettissement)")]
,
 "it": [(FEDLEX,   "LIVA (RS 641.20) – testo consolidato (art. 10, 11, 14, 31)"),
        (P_ABML,   "AFC: disdetta dell’IVA – venir meno dell’obbligo contributivo"),
        (P_PFLEGT, "AFC: IVA – esenzione, rinuncia, assoggettamento volontario"),
        (P_UEBER,  "AFC: imposta sul valore aggiunto – panoramica, annuncio e disdetta, termini"),
        (MI02,     "AFC: IVA-Info 02 Contribuente (fine dell’obbligo contributivo)")]
}

TITLE = {
 "de": "Umsatz unter CHF 100’000 gefallen: MWST-Abmeldung vor dem Periodenende 31.12. prüfen",
 "en": "Turnover below CHF 100,000: check VAT de-registration before the 31.12. period end",
 "fr": "Chiffre d’affaires passé sous CHF 100’000 : pensez à la désinscription TVA avant le 31.12.",
 "it": "Fatturato sotto CHF 100’000: verificate la disdetta IVA prima della fine del periodo il 31.12.",
}
META = {
 "de": "Wer mit dem massgebenden Umsatz dauerhaft unter 100’000 Franken rutscht, kann sich per Periodenende aus dem MWST-Register löschen lassen. Wer die Abmeldung verpasst, verzichtet automatisch auf die Befreiung – und bleibt gebunden. Fristen, Verzichtsfolge und die Vorsteuerkorrektur bei der Schlussabrechnung im Überblick.",
 "en": "Anyone whose relevant turnover falls permanently below CHF 100,000 can have the company deleted from the VAT register at the end of the period. Miss the deadline and you automatically waive the exemption – and stay bound. Deadlines, the deemed-waiver trap and the input-tax correction on the final settlement at a glance.",
 "fr": "Celui dont le chiffre d’affaires déterminant passe durablement sous CHF 100’000 peut demander sa radiation du registre TVA en fin de période. Manquer le délai équivaut à renoncer automatiquement à l’exemption – et à rester lié. Délais, effet du renoncement tacite et régularisation de l’impôt préalable au décompte final.",
 "it": "Chi scende in modo duraturo sotto CHF 100’000 di fatturato determinante può farsi cancellare dal registro IVA a fine periodo. Chi perde il termine rinuncia automaticamente all’esenzione – e resta vincolato. Termini, conseguenze della rinuncia tacita e rettifica dell’imposta precedente nel conteggio finale.",
}

# ---- DEUTSCH ----
DE = [
("Wann die Abmeldung möglich ist – und warum die Schwelle allein nicht reicht",
 """<p>Eine Löschung aus dem MWST-Register verlangt zwei Prüfungen, nicht eine. Erstens darf der <strong>massgebende Umsatz</strong> aus steuerbaren Leistungen im In- und Ausland die Grenze von <strong>CHF 100’000</strong> nicht mehr erreichen; für nicht gewinnstrebige, ehrenamtlich geführte Sport- und Kulturvereine sowie gemeinnützige Institutionen gilt die höhere Grenze von CHF 250’000 (Art. 10 Abs. 2 MWSTG). Zweitens muss <strong>zu erwarten sein, dass die Grenze auch in der folgenden Steuerperiode nicht erreicht wird</strong>. Nur wenn beides zutrifft, besteht überhaupt ein Anrecht auf die Befreiung (ESTV, MWST-Steuerpflicht; MWST-Info 02).</p>
<p>Rechenbeispiel: Eine Grafikerin (Einzelfirma, effektive Methode) erzielte 2025 noch CHF 128’000 steuerbaren Umsatz und war deshalb MWST-pflichtig. 2026 sinkt der massgebende Umsatz auf <strong>CHF 92’000 netto</strong>, und wegen eines weggefallenen Grossauftrags ist auch 2027 nicht mit einem Wiederanstieg zu rechnen. Damit ist die Löschung frühestens auf das <strong>Ende der Steuerperiode</strong> möglich, in der die Grenze erstmals unterschritten wurde – bei kalenderjahriger Periode also auf den <strong>31. Dezember 2026</strong>.</p>
<p>Die Abmeldung ist rechtzeitig eingereicht, wenn sie der ESTV <strong>innert 60 Tagen nach Ende der Steuerperiode</strong> vorliegt (Art. 14 Abs. 5 MWSTG). Für das Periodenende 31.12.2026 heisst der Stichtag damit <strong>1. März 2027</strong>. Strategisch getroffen wird der Entscheid aber schon jetzt im November/Dezember – denn er hängt davon ab, wie sich der letzte Quartalsumsatz und die Auftragslage ins neue Jahr fortsetzen.</p>
<p><strong>Praxistipp:</strong> Prüfen Sie die Schwelle bereits auf Basis von Januar bis September, wenn der Dezember erfahrungsgemäss nicht die grösste Umsatzphase ist. So gewinnen Sie Wochen für die Schlussabrechnung – statt im Januar unter Zeitdruck zu entscheiden.</p>"""),

("Warum Nichtstun zur freiwilligen Steuerpflicht wird – die Verzichts-Falle",
 """<p>Der wichtigste Satz des Artikels steht in Art. 14 Abs. 5 MWSTG: <strong>«Eine Nichtabmeldung gilt als Verzicht auf die Befreiung von der Steuerpflicht.»</strong> Wer also unter die Grenze rutscht, sich aber nicht aktiv abmeldet, entscheidet sich rechtlich dafür, steuerpflichtig zu bleiben. Die freiwillige Steuerpflicht wirkt ab Beginn der folgenden Steuerperiode – die Firma bleibt eingetragen, muss weiterhin MWST auf den Rechnungen ausweisen und periodisch abrechnen.</p>
<p>Nicht ignorieren lässt sich die <strong>Bindungswirkung</strong>: Ein Verzicht auf die Befreiung ist gemäss Art. 11 Abs. 2 MWSTG <strong>während mindestens einer Steuerperiode</strong> beizubehalten. Wer den Fehler bemerkt, kann die Löschung also nicht sofort rückgängig machen oder einen mittendrin erklärten Verzicht widerrufen – er bleibt bis zum Ablauf der Periode gebunden.</p>
<p>Für B2C-Kunden ist das doppelt schmerzhaft: Ausgewiesene MWST verteuert die Preise gegenüber Endkonsumentinnen und -konsumenten um den Satz, ohne dass deren eigene Rechnung etwas bringt – im Unterschied zu Firmenkunden, die den Vorsteuerabzug nutzen. Die Verzichts-Falle ist damit weniger ein juristisches Detail als eine direkte Preis- und Administrationsfrage.</p>
<p><strong>Praxistipp:</strong> Notieren Sie sich den Abmeldetermin (bei Kalenderperiode: 1. März des Folgejahres) bereits jetzt im Kalender – nicht erst im neuen Jahr, wenn die Frist zu laufen begonnen hat.</p>"""),

("Was die Löschung kostet: Vorsteuerkorrektur und Eigenverbrauch in der Schlussabrechnung",
 """<p>Die Abmeldung ist nicht gratis. Solange die Firma steuerpflichtig war, hat sie bei ihren Einkäufen die Vorsteuer abgezogen – auf Fahrzeugen, Maschinen, Werkzeug, EDV und dem Lager. <strong>Fällt die Steuerpflicht weg, fällt rückwirkend die Voraussetzung für diesen Abzug</strong>: Was sich bei Wegfall noch in Ihrer Verfügungsmacht befindet, gilt als Eigenverbrauch (Art. 31 Abs. 2 Bst. d MWSTG) und die früher abgezogene Vorsteuer ist zurückzuzahlen.</p>
<p>Bewegliche Gegenstände werden dabei <strong>pro abgelaufenem Jahr um einen Fünftel</strong> abgeschrieben (Korrektur über 5 Jahre), unbewegliche um einen Zwanzigstel (20 Jahre); <strong>ungebrauchtes Lagermaterial</strong> ist dagegen voll zu korrigieren. Die Korrektur gehört in die Abrechnung der <strong>letzten Steuerperiode</strong>.</p>""" + """<table><thead><tr><th>Wirtschaftsgut</th><th>Einkauf netto</th><th>Abgezogene Vorsteuer</th><th>Abgelaufene Jahre</th><th>Zurückzuzahlen</th></tr></thead><tbody>""" + \
"<tr><td>Kamera (2024, beweglich)</td><td>CHF 5’000</td><td>CHF 405.00</td><td>2 (Rest 3/5)</td><td><strong>CHF 243.00</strong></td></tr>" + \
"<tr><td>Laptop (2025, beweglich)</td><td>CHF 2’400</td><td>CHF 194.40</td><td>1 (Rest 4/5)</td><td><strong>CHF 155.52</strong></td></tr>" + \
"<tr><td>Lagermaterial (ungebraucht)</td><td>CHF 1’200</td><td>CHF 97.20</td><td>– (voll)</td><td><strong>CHF 97.20</strong></td></tr>" + \
"<tr><td><strong>Total Schlussabrechnung</strong></td><td></td><td></td><td></td><td><strong>CHF 495.72</strong></td></tr>" + \
"""</tbody></table><p class="muted">Normalsatz 8,1 % (Stand 2026/2027); Zeitwerte gerundet. Beispielrechnung mit dem Satz von 2026.</p>
<p>Wer nach <strong>Saldosteuersatz</strong> abrechnet, von dieser Korrektur weitgehend verschont: Der Eigenverbrauch ist im Pauschalsatz bereits berücksichtigt, abzurechnen sind nur die Umsätze und angefangenen Arbeiten bis zum Löschungszeitpunkt mit dem eigenen Satz. Wer effektiv abrechnet, deklariert die Rückzahlung in der letzten ordentlichen Abrechnung.</p>
<div class="cta-mid"><strong>Lohnt sich der Schritt für Ihren Fall?</strong> Der Steuerrechner zeigt, was die Änderung Ihrer Buchführung für Ihre Steuerrechnung bedeutet; bei Liegenschaften oder einem grösseren Anlagenbestand prüft eine geprüfte Fachperson die Schlussabrechnung sauber: <a href="rechner.html">zum Steuerrechner</a> · <a href="kontakt.html">unverbindliche Beratung anfragen</a>.</div>
<p><strong>Praxistipp:</strong> Stellen Sie die Anlage mit abgezogener Vorsteuer (Kaufdatum, Preis, Vorsteuer) bereits zusammen, bevor Sie den Antrag auslösen – so vermeiden Sie eine Berichtigungsabrechnung, auf der zusätzlich Verzugszins laufen kann.</p>"""),

("Rechnen statt raten: abmelden oder freiwillig steuerpflichtig bleiben?",
 """<p>Unter der Grenze ist die Befreiung ein Recht, keine Pflicht. Genau deshalb lohnt der Entscheid eine Rechnung. Der Trade-off entscheidet sich an zwei Fragen: Wie hoch ist Ihr Vorsteueranteil aus eigenen Einkauf (den Sie mit der Löschung verlieren), und wer sind Ihre Kunden (denen MWST auf der Rechnung nützt oder schadet)?</p>""" + """<table><thead><tr><th>Situation</th><th>Lohnender Weg</th><th>Grund</th></tr></thead>""" + \
"<tbody>" + \
"<tr><td>Überwiegend B2C, tiefe eigene Einkaufe</td><td>Abmelden</td><td>Kein Preisnachteil, weniger Administration</td></tr>" + \
"<tr><td>Überwiegend B2B (Firmenkunden)</td><td>Freiwillig bleiben</td><td>Kunden wollen den Vorsteuerabzug</td></tr>" + \
"<tr><td>Grosse Investitionen geplant</td><td>Freiwillig bleiben</td><td>Vorsteuer auf Anlagen abziehbar</td></tr>" + \
"<tr><td>Stabile tiefe Margin ohne Anlagen</td><td>Abmelden</td><td>Verzicht auf quartalsweise Abrechnung</td></tr>" + \
"</tbody></table>" + """<p>Beispielrechnung zur Orientierung: Bleibt die Grafikerin steuerpflichtig, stellt sie auf CHF 92’000 Ausgangsleistung MWST von <strong>CHF 7’452</strong> den Kunden in Rechnung, macht auf eigenen Einkaufen von CHF 8’000 Vorsteuer von <strong>CHF 648</strong> geltend – der Saldo fliesst an die ESTV. Meldet sie sich ab, entfällt beides: kein Vorsteuerabzug, aber auch kein MWST-Ausweis mehr. Für ein reines Endkundengeschäft ist das Abmelden meist klar vorteilhaft.</p>
<p><strong>Praxistipp:</strong> Prüfen Sie bei der Abwägung auch die Radio- und TV-Abgabe ( Serafe), deren Höhe am Gesamtumsatz hängt, sowie allfällige Vertragsklauseln, die einen MWST-Ausweis voraussetzen.</p>"""),

("Ablauf: Abmeldung im neuen ESTV-Portal – und was danach zu tun ist",
 """<p>Seit dem <strong>9. November 2026</strong> läuft die MWST-Abmeldung über das neue ESTV-Portal. Der Antrag steht dort unter «<strong>Neue Geschäfte</strong>»; die Abmeldung über die alte Website steht nicht mehr zur Verfügung. Halten Sie MWST-Nummer, die Umsatzberechnung und das gewünschte Löschungsdatum bereit und sichern Sie die Eingangsbestätigung sowie den späteren Entscheid mit dem Löschungsdatum.</p>
<p>Drei Dinge sind nach der Löschung zwingend anzupassen. Erstens dürfen Sie auf <strong>neuen Rechnungen keine MWST mehr ausweisen</strong> – stellen Sie Vorlagen und wiederkehrende Rechnungen um, die UID als Firmen-ID bleibt erhalten, aber ohne fortbestehende MWST-Registrierung. Zweitens erledigt die MWST-Abmeldung <strong>nicht</strong> die Abmeldung bei Handelsregister oder Ausgleichskasse. Drittens bleibt die <strong>Bezugsteuer</strong> bestehen: Wer im Ausland Dienstleistungen (SaaS, Beratung, Werbung) über CHF 10’000 pro Jahr bezieht, schuldet die Steuer auch ohne MWST-Registrierung (Art. 45 Abs. 2 Bst. b MWSTG).</p>
<p><strong>Praxistipp:</strong> Trennen Sie in der letzten Abrechnung sauber zwischen Umsätzen der Periode und der Eigenverbrauchskorrektur – und rechnen Sie die Schlussabrechnung bis zur Frist 1. März, auch wenn die Löschung selbst erst später rechtskräftig wird.</p>"""),

("Kurz-Checkliste: MWST-Abmeldung fristgerecht einreichen",
 """<ul>
<li><strong>Schwelle prüfen:</strong> Liegt der massgebende Umsatz (netto, In- und Ausland, steuerbare Leistungen) unter CHF 100’000 – und wird er das laut Erwartung auch in der Folgeperiode?</li>
<li><strong>Entscheid fällen:</strong> Befreiung nutzen und abmelden – oder freiwillig steuerpflichtig bleiben (z. B. bei B2B-Kunden oder geplanten Investitionen).</li>
<li><strong>Frist halten:</strong> Abmeldung innert 60 Tagen nach Periodenende einreichen – für den 31.12.2026 bis am 1. März 2027. Nichtabmeldung gilt als Verzicht.</li>
<li><strong>Schlussabrechnung:</strong> Eigenverbrauchskorrektur auf behaltenen Anlagen und Lager deklarieren (Restwert-Methode).</li>
<li><strong>Nachlauf erledigen:</strong> Rechnungsvorlagen ohne MWST, Bezugsteuer für Importleistungen, Handelsregister und Ausgleichskasse separat prüfen.</li>
</ul>
<p>Ob Einzelunternehmen, Start-up mit Schwundjahr oder KMU, das einen Bereich ausgliedert – die Abmeldung ist ein einmaliger, aber folgenreicher Schritt im Jahresabschluss. Prüfen Sie Frist und Schlussabrechnung vor dem 31. Dezember; bei Anlagen, Liegenschaften oder Unsicherheit über die Verzichtsbindung lohnt sich eine vorgängige Nachfrage bei einer <a href="kontakt.html">geprüften Fachperson</a>.</p>"""),
]

# ---- ENGLISH ----
EN = [
("When de-registration is possible – and why the threshold alone is not enough",
 """<p>Deletion from the VAT register requires two tests, not one. First, the <strong>relevant turnover</strong> from taxable supplies in Switzerland and abroad may no longer reach <strong>CHF 100,000</strong>; non-profit, voluntarily run sports and cultural clubs and charitable institutions have the higher threshold of CHF 250,000 (Art. 10 para. 2 VAT Act). Second, it must be <strong>expected that the threshold will also not be reached in the following tax period</strong>. Only when both apply is there a right to the exemption (ESTV, VAT liability; MWST-Info 02).</p>
<p>Worked example: a graphic designer (sole proprietorship, effective method) still generated CHF 128,000 of taxable turnover in 2025 and was therefore VAT-liable. In 2026 the relevant turnover drops to <strong>CHF 92,000 net</strong>, and because a major contract has been lost no recovery is expected in 2027 either. Deletion is therefore possible at the earliest <strong>at the end of the tax period</strong> in which the threshold was first missed – for a calendar-year period, i.e. <strong>31 December 2026</strong>.</p>
<p>The de-registration is filed in time if it reaches the ESTV <strong>within 60 days after the end of the tax period</strong> (Art. 14 para. 5 VAT Act). For the 31.12.2026 period end that makes the deadline <strong>1 March 2027</strong>. Strategically, though, the decision is made now in November/December – because it depends on how the final quarter and the order backlog carry into the new year.</p>
<p><strong>Practical tip:</strong> Test the threshold already on the basis of January to September when December is traditionally not your biggest phase. That buys you weeks for the final settlement – instead of a rushed decision in January.</p>"""),

("Why doing nothing turns into voluntary tax liability – the waiver trap",
 """<p>The single most important sentence is in Art. 14 para. 5 VAT Act: <strong>«Failure to de-register is deemed a waiver of the exemption from tax liability.»</strong> Anyone who drops below the threshold but does not actively de-register thus legally decides to remain taxable. The voluntary liability takes effect from the start of the following tax period – the company stays registered, must keep showing VAT on invoices and filing settlements periodically.</p>
<p>The <strong>binding effect</strong> must not be ignored: a waiver of the exemption must be maintained for <strong>at least one tax period</strong> (Art. 11 para. 2 VAT Act). Someone who notices the mistake can neither reverse the deletion immediately nor revoke a waiver declared in the middle of a period – they are bound until the period expires.</p>
<p>For B2C customers this is doubly painful: showing VAT makes prices higher for end consumers without any benefit on their side – unlike corporate customers, who use the input-tax deduction. The waiver trap is therefore less a legal footnote than a direct question of pricing and administration.</p>
<p><strong>Practical tip:</strong> Put the de-registration date (for a calendar period: 1 March of the following year) in your calendar now – not only in the new year once the deadline is already running.</p>"""),

("What de-registration costs: input-tax correction and self-consumption on the final settlement",
 """<p>De-registration is not free. While the company was taxable it deducted input tax on purchases – vehicles, machines, tools, IT and stock. <strong>When tax liability lapses, the prerequisite for that deduction lapses retroactively</strong>: anything still within your disposal when the liability ends is treated as self-consumption (Art. 31 para. 2 lit. d VAT Act) and the input tax previously deducted must be repaid.</p>
<p>Movable assets are written down <strong>by one fifth per elapsed year</strong> (a correction over 5 years), immovable assets by one twentieth (20 years); <strong>unused stock</strong>, however, is corrected in full. The correction belongs in the settlement of the <strong>last tax period</strong>.</p>""" + """<table><thead><tr><th>Asset</th><th>Purchase net</th><th>Input tax deducted</th><th>Years elapsed</th><th>Repayable</th></tr></thead><tbody>""" + \
"<tr><td>Camera (2024, movable)</td><td>CHF 5,000</td><td>CHF 405.00</td><td>2 (3/5 left)</td><td><strong>CHF 243.00</strong></td></tr>" + \
"<tr><td>Laptop (2025, movable)</td><td>CHF 2,400</td><td>CHF 194.40</td><td>1 (4/5 left)</td><td><strong>CHF 155.52</strong></td></tr>" + \
"<tr><td>Stock material (unused)</td><td>CHF 1,200</td><td>CHF 97.20</td><td>– (full)</td><td><strong>CHF 97.20</strong></td></tr>" + \
"<tr><td><strong>Total final settlement</strong></td><td></td><td></td><td></td><td><strong>CHF 495.72</strong></td></tr>" + \
"""</tbody></table><p class="muted">Standard rate 8.1% (as of 2026/2027); residual values rounded. Example uses the 2026 rate.</p>
<p>Anyone settling at a <strong>flat rate</strong> (Saldosteuersatz) is largely spared this correction: self-consumption is already accounted for in the flat rate, so only turnover and work in progress up to the deletion date are settled at your own rate. Effective-method taxpayers declare the repayment in the last ordinary settlement.</p>
<div class="cta-mid"><strong>Is the step worth it in your case?</strong> The tax calculator shows what the change to your bookkeeping means for your tax bill; for real estate or a larger asset base a verified professional can review the final settlement properly: <a href="rechner.html">open the tax calculator</a> · <a href="kontakt.html">request non-binding advice</a>.</div>
<p><strong>Practical tip:</strong> Compile the schedule of assets with deducted input tax (purchase date, price, VAT) before you trigger the application – this avoids a corrective settlement that can additionally trigger default interest.</p>"""),

("Do the math: de-register or stay voluntarily taxable?",
 """<p>Below the threshold, exemption is a right, not a duty. That is exactly why the decision deserves a calculation. The trade-off turns on two questions: how large is your input tax on your own purchases (which you lose on deletion), and who are your customers (for whom VAT on an invoice helps or hurts)?</p>""" + """<table><thead><tr><th>Situation</th><th>Worthwhile path</th><th>Reason</th></tr></thead>""" + \
"<tbody>" + \
"<tr><td>Predominantly B2C, low own purchases</td><td>De-register</td><td>No price disadvantage, less administration</td></tr>" + \
"<tr><td>Predominantly B2B (corporate clients)</td><td>Stay voluntary</td><td>Clients want the input-tax deduction</td></tr>" + \
"<tr><td>Large investments planned</td><td>Stay voluntary</td><td>Input tax on assets is deductible</td></tr>" + \
"<tr><td>Stable low margin, no assets</td><td>De-register</td><td>Waives quarterly settlements</td></tr>" + \
"</tbody></table>" + """<p>Guiding calculation: if the graphic designer stays taxable, she charges clients VAT of <strong>CHF 7,452</strong> on CHF 92,000 of output and claims input tax of <strong>CHF 648</strong> on her own purchases of CHF 8,000 – the balance flows to the ESTV. If she de-registers, both disappear: no input-tax deduction, but no more VAT on invoices either. For a pure end-customer business, de-registering is usually the clear advantage.</p>
<p><strong>Practical tip:</strong> When weighing it up, also consider the radio/TV reception fee (Serafe), which is based on total turnover, and any contract clauses that presuppose showing VAT.</p>"""),

("Procedure: de-registration in the new ESTV portal – and what to do afterwards",
 """<p>Since <strong>9 November 2026</strong>, VAT de-registration runs through the new ESTV portal. The application is under «<strong>Neue Geschäfte</strong>» (new transactions); the old website form is no longer available. Keep your VAT number, the turnover calculation and the desired deletion date ready, and save both the submission confirmation and the later decision with the deletion date.</p>
<p>Three things must be adjusted after deletion. First, <strong>new invoices may no longer show VAT</strong> – update templates and recurring invoices; the UID remains as company ID but without continuing VAT registration. Second, VAT de-registration does <strong>not</strong> cancel the commercial register or the compensation fund. Third, <strong>purchaser tax</strong> (Bezugsteuer) remains: anyone importing services from abroad (SaaS, consulting, advertising) above CHF 10,000 a year owes the tax even without VAT registration (Art. 45 para. 2 lit. b VAT Act).</p>
<p><strong>Practical tip:</strong> Keep period turnover and the self-consumption correction separate in the last settlement – and submit the final settlement by the 1 March deadline even if the deletion itself only becomes legally effective later.</p>"""),

("Quick checklist: file the VAT de-registration on time",
 """<ul>
<li><strong>Test the threshold:</strong> Is the relevant turnover (net, in and abroad, taxable supplies) below CHF 100,000 – and expected to stay so in the following period?</li>
<li><strong>Make the decision:</strong> Use the exemption and de-register – or stay voluntarily taxable (e.g. for B2B clients or planned investments).</li>
<li><strong>Keep the deadline:</strong> File the de-registration within 60 days after the period end – for 31.12.2026 by 1 March 2027. Non-de-registration counts as a waiver.</li>
<li><strong>Final settlement:</strong> Declare the self-consumption correction on retained assets and stock (residual-value method).</li>
<li><strong>Follow-up:</strong> Invoice templates without VAT, purchaser tax on imported services, commercial register and compensation fund checked separately.</li>
</ul>
<p>Whether sole proprietorship, start-up in a down year or SME carving out a unit – de-registration is a one-off but consequential step in the year-end close. Check the deadline and the final settlement before 31 December; for assets, real estate or uncertainty about the waiver binding, ask a <a href="kontakt.html">verified professional</a> first.</p>"""),
]

# ---- FRANÇAIS ----
FR = [
("Quand la désinscription est possible – et pourquoi le seuil ne suffit pas",
 """<p>La radiation du registre TVA exige deux vérifications, pas une. Premièrement, le <strong>chiffre d’affaires déterminant</strong> des prestations imposables en Suisse et à l’étranger ne doit plus atteindre <strong>CHF 100’000</strong> ; les clubs sportifs et culturels sans but lucratif gérés bénévolement ainsi que les institutions d’utilité publique bénéficient du seuil supérieur de CHF 250’000 (art. 10 al. 2 LTVA). Deuxièmement, il faut <strong>pouvoir s’attendre à ce que le seuil ne soit pas non plus atteint durant la période fiscale suivante</strong>. Ce n’est que si les deux conditions sont réunies que le droit à l’exemption existe (AFC, assujettissement TVA ; TVA-Info 02).</p>
<p>Exemple chiffré : une graphiste (raison individuelle, méthode effective) réalisait encore CHF 128’000 de chiffre d’affaires imposable en 2025 et était donc assujettie. En 2026, le chiffre d’affaires déterminant tombe à <strong>CHF 92’000 net</strong>, et, vu un grand mandat perdu, aucun redressement n’est attendu en 2027. La radiation est donc possible au plus tôt <strong>à la fin de la période fiscale</strong> durant laquelle le seuil n’a plus été atteint – pour une période calendaire, soit le <strong>31 décembre 2026</strong>.</p>
<p>La désinscription est déposée en temps utile si elle parvient à l’AFC <strong>dans les 60 jours après la fin de la période fiscale</strong> (art. 14 al. 5 LTVA). Pour la fin de période du 31.12.2026, l’échéance est donc le <strong>1<sup>er</sup> mars 2027</strong>. Stratégiquement, la décision se prend dès maintenant, en novembre/décembre – car elle dépend de la façon dont le dernier trimestre et le carnet de commandes se prolongent dans la nouvelle année.</p>
<p><strong>Conseil pratique :</strong> testez déjà le seuil sur la base de janvier à septembre lorsque décembre n’est pas votre plus grosse phase. Vous gagnez ainsi des semaines pour le décompte final – au lieu d’une décision dans l’urgence en janvier.</p>"""),

("Pourquoi ne rien faire revient à une imposition volontaire – le piège du renoncement",
 """<p>La phrase la plus importante figure à l’art. 14 al. 5 LTVA : <strong>« Une absence de désinscription vaut renoncement à l’exemption de l’assujettissement. »</strong> Celui qui passe sous le seuil sans se désinscrire activement opte donc juridiquement pour le maintien de l’assujettissement. L’imposition volontaire prend effet dès le début de la période fiscale suivante – l’entreprise reste inscrite, doit continuer à faire figurer la TVA sur ses factures et à déposer des décomptes périodiques.</p>
<p>L’<strong>effet contraignant</strong> est à ne pas négliger : le renoncement à l’exemption doit être maintenu <strong>pendant au moins une période fiscale</strong> (art. 11 al. 2 LTVA). Celui qui remarque l’erreur ne peut donc pas annuler la radiation ni révoquer un renoncement déclaré en cours de période – il reste lié jusqu’à l’échéance de celle-ci.</p>
<p>Pour la clientèle B2C, c’est doublement pénible : faire figurer la TVA renchérit les prix auprès des consommateurs finaux sans aucun avantage pour eux – contrairement aux clients entreprises, qui profitent de la déduction de l’impôt préalable. Le piège du renoncement est donc moins un détail juridique qu’une question directe de prix et d’administration.</p>
<p><strong>Conseil pratique :</strong> inscrivez d’ores et déjà la date de désinscription (pour une période calendaire : le 1<sup>er</sup> mars de l’année suivante) à votre agenda – pas seulement en janvier, lorsque le délai aura déjà commencé à courir.</p>"""),

("Ce que coûte la radiation : régularisation de l’impôt préalable et consommation propre au décompte final",
 """<p>La désinscription n’est pas gratuite. Tant que l’entreprise était assujettie, elle a déduit l’impôt préalable sur ses achats – véhicules, machines, outillage, informatique et stock. <strong>Si l’assujettissement tombe, la condition de cette déduction tombe rétroactivement</strong> : ce qui se trouve encore dans votre sphère de disposition à la fin de l’assujettissement est traité comme consommation propre (art. 31 al. 2 let. d LTVA) et l’impôt préalablement déduit doit être remboursé.</p>
<p>Les biens meubles sont amortis <strong>d’un cinquième par année écoulée</strong> (régularisation sur 5 ans), les immeubles d’un vingtième (20 ans) ; le <strong>matériel de stock non utilisé</strong>, en revanche, est corrigé intégralement. La régularisation figure dans le décompte de la <strong>dernière période fiscale</strong>.</p>""" + """<table><thead><tr><th>Bien</th><th>Achat net</th><th>Impôt préalable déduit</th><th>Années écoulées</th><th>À rembourser</th></tr></thead><tbody>""" + \
"<tr><td>Appareil photo (2024, meuble)</td><td>CHF 5’000</td><td>CHF 405.00</td><td>2 (3/5 restants)</td><td><strong>CHF 243.00</strong></td></tr>" + \
"<tr><td>Ordinateur portable (2025, meuble)</td><td>CHF 2’400</td><td>CHF 194.40</td><td>1 (4/5 restants)</td><td><strong>CHF 155.52</strong></td></tr>" + \
"<tr><td>Matériel de stock (non utilisé)</td><td>CHF 1’200</td><td>CHF 97.20</td><td>– (intégral)</td><td><strong>CHF 97.20</strong></td></tr>" + \
"<tr><td><strong>Total du décompte final</strong></td><td></td><td></td><td></td><td><strong>CHF 495.72</strong></td></tr>" + \
"""</tbody></table><p class="muted">Taux normal 8,1 % (état 2026/2027) ; valeurs résiduelles arrondies. Exemple avec le taux 2026.</p>
<p>Celui qui décompte au <strong>taux forfaitaire</strong> (impôt préalable déduit du taux) est largement épargné : la consommation propre est déjà comprise dans le forfait, et seuls le chiffre d’affaires et les travaux en cours jusqu’à la radiation sont décomptés à votre propre taux. En méthode effective, le remboursement se déclare dans le dernier décompte ordinaire.</p>
<div class="cta-mid"><strong>Le pas en vaut-il la peine pour votre cas ?</strong> Le calculateur d’impôts montre ce que le changement de comptabilité implique pour votre facture fiscale ; pour l’immobilier ou un parc d’actifs important, une personne qualifiée vérifiée examine le décompte final proprement : <a href="rechner.html">ouvrir le calculateur</a> · <a href="kontakt.html">demander un conseil sans engagement</a>.</div>
<p><strong>Conseil pratique :</strong> dressez la liste des actifs avec impôt préalable déduit (date d’achat, prix, TVA) avant de déposer la demande – vous éviterez ainsi un décompte rectificatif pouvant en plus déclencher des intérêts moratoires.</p>"""),

("Calculer plutôt que deviner : se désinscrire ou rester volontairement assujetti ?",
 """<p>Sous le seuil, l’exemption est un droit, pas une obligation. C’est précisément pourquoi la décision mérite un calcul. L’arbitrage tient à deux questions : quelle est l’ampleur de l’impôt préalable sur vos propres achats (perdu à la radiation), et qui sont vos clients (pour qui la TVA sur la facture est un atout ou un handicap) ?</p>""" + """<table><thead><tr><th>Situation</th><th>Voie pertinente</th><th>Motif</th></tr></thead>""" + \
"<tbody>" + \
"<tr><td>Surtout B2C, achats propres faibles</td><td>Se désinscrire</td><td>Aucun désavantage de prix, moins d’administration</td></tr>" + \
"<tr><td>Surtout B2B (clients entreprises)</td><td>Rester volontaire</td><td>Les clients veulent la déduction de l’impôt préalable</td></tr>" + \
"<tr><td>Investissements importants prévus</td><td>Rester volontaire</td><td>Impôt préalable sur les actifs déductible</td></tr>" + \
"<tr><td>Marge basse stable, sans actifs</td><td>Se désinscrire</td><td>S’épargne les décomptes trimestriels</td></tr>" + \
"</tbody></table>" + """<p>Calcul d’orientation : si la graphiste reste assujettie, elle facture CHF 7’452 de TVA à ses clients sur CHF 92’000 de prestations et déduit CHF 648 d’impôt préalable sur ses achats propres de CHF 8’000 – le solde revient à l’AFC. Si elle se désinscrit, les deux disparaissent : plus de déduction d’impôt préalable, mais plus de TVA sur les factures. Pour un pur commerce de détail final, la désinscription est généralement le net avantage.</p>
<p><strong>Conseil pratique :</strong> dans la pesée, tenez aussi compte de la redevance radio-TV (Serafe), dont le montant dépend du chiffre d’affaires total, ainsi que d’éventuelles clauses contractuelles présupposant l’indication de la TVA.</p>"""),

("Déroulement : la désinscription dans le nouveau portail AFC – et ce qu’il faut faire ensuite",
 """<p>Depuis le <strong>9 novembre 2026</strong>, la désinscription TVA passe par le nouveau portail AFC. La demande s’y trouve sous « <strong>Neue Geschäfte</strong> » (nouvelles opérations) ; le formulaire de l’ancien site n’est plus disponible. Ayez sous la main votre numéro TVA, le calcul du chiffre d’affaires et la date de radiation souhaitée, et conservez l’accusé de réception comme la décision ultérieure portant la date de radiation.</p>
<p>Trois ajustements s’imposent après la radiation. Premièrement, <strong>les nouvelles factures ne peuvent plus porter la TVA</strong> – modifiez modèles et factures récurrentes ; l’UID demeure comme identifiant d’entreprise mais sans assujettissement TVA subsistant. Deuxièmement, la désinscription TVA ne résilie <strong>pas</strong> l’inscription au registre du commerce ni à la caisse de compensation. Troisièmement, l’<strong>impôt sur les prestations reçues</strong> (Bezugsteuer) demeure : celui qui reçoit de l’étranger des prestations (SaaS, conseil, publicité) pour plus de CHF 10’000 par an doit la taxe même sans inscription TVA (art. 45 al. 2 let. b LTVA).</p>
<p><strong>Conseil pratique :</strong> distinguez, dans le dernier décompte, les prestations de la période et la régularisation de consommation propre – et déposez le décompte final avant l’échéance du 1<sup>er</sup> mars, même si la radiation ne produit effet que plus tard.</p>"""),

("Check-list rapide : déposer la désinscription TVA dans les délais",
 """<ul>
<li><strong>Tester le seuil :</strong> le chiffre d’affaires déterminant (net, Suisse et étranger, prestations imposables) est-il sous CHF 100’000 – et attendu comme tel aussi la période suivante ?</li>
<li><strong>Prendre la décision :</strong> user de l’exemption et se désinscrire – ou rester volontairement assujetti (p. ex. clientèle B2B, investissements prévus).</li>
<li><strong>Tenir le délai :</strong> déposer la désinscription dans les 60 jours après la fin de période – pour le 31.12.2026, jusqu’au 1<sup>er</sup> mars 2027. L’absence de désinscription vaut renoncement.</li>
<li><strong>Décompte final :</strong> déclarer la régularisation de consommation propre sur les actifs et stocks conservés (méthode de la valeur résiduelle).</li>
<li><strong>Suivi :</strong> modèles de facture sans TVA, impôt sur les prestations reçues pour les services importés, registre du commerce et caisse de compensation vérifiés séparément.</li>
</ul>
<p>Raison individuelle, start-up en année creuse ou PME détachant une activité – la désinscription est un pas ponctuel mais lourd de conséquences dans la clôture de l’exercice. Vérifiez délai et décompte final avant le 31 décembre ; pour les actifs, l’immobilier ou en cas de doute sur la contrainte du renoncement, consultez au préalable une <a href="kontakt.html">personne qualifiée vérifiée</a>.</p>"""),
]

# ---- ITALIANO ----
IT = [
("Quando la disdetta è possibile – e perché la soglia da sola non basta",
 """<p>La cancellazione dal registro IVA richiede due verifiche, non una. In primo luogo, il <strong>fatturato determinante</strong> delle prestazioni imponibili in Svizzera e all’estero non deve più raggiungere <strong>CHF 100’000</strong>; per le società sportive e culturali senza scopo di lucro gestite a titolo onorifico e per le istituzioni di utilità pubblica vale la soglia superiore di CHF 250’000 (art. 10 cpv. 2 LIVA). In secondo luogo, occorre <strong>poter prevedere che la soglia non venga raggiunta nemmeno nel periodo fiscale successivo</strong>. Solo se entrambe le condizioni sono adempite esiste il diritto all’esenzione (AFC, contribuente IVA; IVA-Info 02).</p>
<p>Esempio di calcolo: una grafica (ditta individuale, metodo effettivo) conseguiva ancora CHF 128’000 di fatturato imponibile nel 2025 ed era quindi contribuente. Nel 2026 il fatturato determinante scende a <strong>CHF 92’000 netti</strong> e, venuto meno un grande mandato, non ci si attende un recupero nemmeno nel 2027. La cancellazione è pertanto possibile al più presto <strong>alla fine del periodo fiscale</strong> in cui la soglia non è più stata raggiunta – per un periodo coincidente con l’anno civile, il <strong>31 dicembre 2026</strong>.</p>
<p>La disdetta è presentata in tempo se perviene all’AFC <strong>entro 60 giorni dalla fine del periodo fiscale</strong> (art. 14 cpv. 5 LIVA). Per la fine del periodo il 31.12.2026 la scadenza è dunque il <strong>1<sup>o</sup> marzo 2027</strong>. Strategicamente, però, la decisione va presa già ora, a novembre/dicembre, perché dipende dall’andamento dell’ultimo trimestre e del portafoglio ordini nel nuovo anno.</p>
<p><strong>Suggerimento pratico:</strong> verifichi la soglia già sui dati da gennaio a settembre, se dicembre non è la sua fase di maggior fatturato. Guadagna così settimane per il conteggio finale, anziché decidere in gennaio sotto pressione.</p>"""),

("Perché non fare nulla diventa assoggettamento volontario – la trappola della rinuncia",
 """<p>La frase più importante è nell’art. 14 cpv. 5 LIVA: <strong>«La mancata disdetta vale come rinuncia all’esenzione dall’obbligo contributivo.»</strong> Chi scende sotto la soglia senza disdire attivamente decide giuridicamente di restare contribuente. L’assoggettamento volontario produce effetti dall’inizio del periodo fiscale successivo: l’azienda resta iscritta, deve ancora indicare l’IVA in fattura e depositare conteggi periodici.</p>
<p>L’<strong>effetto vincolante</strong> non va ignorato: la rinuncia all’esenzione deve essere mantenuta <strong>per almeno un periodo fiscale</strong> (art. 11 cpv. 2 LIVA). Chi si accorge dell’errore non può quindi annullare la cancellazione né revocare una rinuncia dichiarata nel corso del periodo – resta vincolato fino alla scadenza del periodo.</p>
<p>Per i clienti B2C è doppiamente penalizzante: indicare l’IVA rincara i prezzi verso i consumatori finali senza alcun vantaggio per loro – a differenza dei clienti imprese, che utilizzano la deduzione dell’imposta precedente. La trappola della rinuncia è dunque meno un dettaglio giuridico che una questione diretta di prezzi e di amministrazione.</p>
<p><strong>Suggerimento pratico:</strong> annoti già ora la data della disdetta (per un periodo civile: il 1<sup>o</sup> marzo dell’anno seguente) in agenda – non soltanto a gennaio, quando il termine avrà già cominciato a decorrere.</p>"""),

("Quanto costa la cancellazione: rettifica dell’imposta precedente e consumo proprio nel conteggio finale",
 """<p>La disdetta non è gratuita. Finché l’azienda era contribuente ha detratto l’imposta precedente sugli acquisti – veicoli, macchine, utensili, informatica e magazzino. <strong>Venendo meno l’obbligo contributivo, cade retroattivamente anche la presupposizione della deduzione</strong>: ciò che si trova ancora nella sua sfera di disponibilità alla fine dell’assoggettamento è trattato come consumo proprio (art. 31 cpv. 2 lett. d LIVA) e l’imposta precedente detratta va rimborsata.</p>
<p>I beni mobili sono ammortizzati <strong>di un quinto per ogni anno trascorso</strong> (rettifica su 5 anni), gli immobili di un ventesimo (20 anni); il <strong>materiale di magazzino non utilizzato</strong> è invece rettificato integralmente. La rettifica appartiene al conteggio dell’<strong>ultimo periodo fiscale</strong>.</p>""" + """<table><thead><tr><th>Bene</th><th>Acquisto netto</th><th>Imposta precedente detratta</th><th>Anni trascorsi</th><th>Da rimborsare</th></tr></thead><tbody>""" + \
"<tr><td>Fotocamera (2024, mobile)</td><td>CHF 5’000</td><td>CHF 405.00</td><td>2 (3/5 residui)</td><td><strong>CHF 243.00</strong></td></tr>" + \
"<tr><td>Portatile (2025, mobile)</td><td>CHF 2’400</td><td>CHF 194.40</td><td>1 (4/5 residui)</td><td><strong>CHF 155.52</strong></td></tr>" + \
"<tr><td>Materiale di magazzino (non usato)</td><td>CHF 1’200</td><td>CHF 97.20</td><td>– (integrale)</td><td><strong>CHF 97.20</strong></td></tr>" + \
"<tr><td><strong>Totale conteggio finale</strong></td><td></td><td></td><td></td><td><strong>CHF 495.72</strong></td></tr>" + \
"""</tbody></table><p class="muted">Aliquota normale 8,1 % (stato 2026/2027); valori residui arrotondati. Esempio con l’aliquota 2026.</p>
<p>Chi conteggia a <strong>aliquota forfettaria</strong> (imposta precedente compensata nel tasso) è in gran parte risparmiato: il consumo proprio è già considerato nella forfetta e vanno conteggiati solo i fatturati e i lavori in corso fino alla cancellazione con la propria aliquota. Nel metodo effettivo il rimborso si dichiara nell’ultimo conteggio ordinario.</p>
<div class="cta-mid"><strong>Il passo conviene nel suo caso?</strong> Il calcolatore d’imposta mostra cosa comporta la modifica della contabilità sulla sua fattura fiscale; per gli immobili o un patrimonio aziendale rilevante, una persona qualificata verificata esamina il conteggio finale in modo accurato: <a href="rechner.html">aprire il calcolatore</a> · <a href="kontakt.html">richiedere una consulenza senza impegno</a>.</div>
<p><strong>Suggerimento pratico:</strong> prepari l’elenco dei cespiti con imposta precedente detratta (data d’acquisto, prezzo, IVA) prima di presentare la richiesta – eviterà così un conteggio rettificativo su cui possono inoltre maturare interessi moratori.</p>"""),

("Calcolare anziché indovinare: disdire o restare volontariamente contribuenti?",
 """<p>Sotto la soglia l’esenzione è un diritto, non un obbligo. È proprio per questo che la decisione merita un calcolo. La scelta si gioca su due domande: quanto è alta l’imposta precedente sui suoi acquisti propri (che perde con la cancellazione) e chi sono i suoi clienti (per i quali l’IVA in fattura è un vantaggio o un handicap)?</p>""" + """<table><thead><tr><th>Situazione</th><th>Via conveniente</th><th>Motivo</th></tr></thead>""" + \
"<tbody>" + \
"<tr><td>Prevalentemente B2C, acquisti bassi</td><td>Disdire</td><td>Nessuno svantaggio di prezzo, meno amministrazione</td></tr>" + \
"<tr><td>Prevalentemente B2B (clienti imprese)</td><td>Restare volontario</td><td>I clienti vogliono la deduzione dell’imposta precedente</td></tr>" + \
"<tr><td>Investimenti importanti in programma</td><td>Restare volontario</td><td>Imposta precedente sui cespiti deducibile</td></tr>" + \
"<tr><td>Margine basso stabile, senza cespiti</td><td>Disdire</td><td>Si evitano i conteggi trimestrali</td></tr>" + \
"</tbody></table>" + """<p>Calcolo orientativo: se la grafica resta contribuente fattura CHF 7’452 di IVA ai clienti su CHF 92’000 di prestazioni e deduce CHF 648 di imposta precedente sui suoi acquisti di CHF 8’000 – il saldo va all’AFC. Se disdice, entrambi vengono meno: nessuna deduzione dell’imposta precedente, ma nemmeno più IVA in fattura. Per un’attività rivolta solo a consumatori finali, la disdetta è di solito il chiaro vantaggio.</p>
<p><strong>Suggerimento pratico:</strong> nella valutazione consideri anche il canone radio-TV (Serafe), il cui ammontare dipende dal fatturato complessivo, ed eventuali clausole contrattuali che presuppongono l’indicazione dell’IVA.</p>"""),

("Svolgimento: la disdetta nel nuovo portale AFC – e cosa fare dopo",
 """<p>Dal <strong>9 novembre 2026</strong> la disdetta IVA avviene tramite il nuovo portale AFC. La richiesta si trova alla voce «<strong>Neue Geschäfte</strong>» (nuove operazioni); il modulo del vecchio sito non è più disponibile. Tenga a portata di mano il numero IVA, il calcolo del fatturato e la data di cancellazione desiderata e conservi sia la conferma di ricezione sia la successiva decisione con la data di cancellazione.</p>
<p>Tre adeguamenti sono obbligatori dopo la cancellazione. Primo, <strong>le nuove fatture non possono più indicare l’IVA</strong> – modifichi modelli e fatture ricorrenti; l’UID resta come identificativo dell’azienda ma senza un assoggettamento IVA persistente. Secondo, la disdetta IVA non cancella <strong>né</strong> il registro di commercio <strong>né</strong> la cassa di compensazione. Terzo, resta dovuta l’imposta per le prestazioni ricevute dall’estero (reverse charge, art. 45 cpv. 2 lett. b LIVA): chi ottiene da fornitori esteri prestazioni (SaaS, consulenza, pubblicità) per oltre CHF 10’000 l’anno deve l’imposta anche senza iscrizione IVA.</p>
<p><strong>Suggerimento pratico:</strong> distingua, nell’ultimo conteggio, tra le prestazioni del periodo e la rettifica di consumo proprio – e deponga il conteggio finale entro la scadenza del 1<sup>o</sup> marzo, anche se la cancellazione produce effetti giuridici solo più tardi.</p>"""),

("Check-list rapida: presentare la disdetta IVA nei termini",
 """<ul>
<li><strong>Verificare la soglia:</strong> il fatturato determinante (netto, Svizzera ed estero, prestazioni imponibili) è sotto CHF 100’000 – e si prevede tale anche nel periodo successivo?</li>
<li><strong>Prendere la decisione:</strong> sfruttare l’esenzione e disdire – oppure restare volontariamente contribuenti (ad es. clienti B2B, investimenti in programma).</li>
<li><strong>Rispettare il termine:</strong> presentare la disdetta entro 60 giorni dalla fine del periodo – per il 31.12.2026 entro il 1<sup>o</sup> marzo 2027. La mancata disdetta vale come rinuncia.</li>
<li><strong>Conteggio finale:</strong> dichiarare la rettifica di consumo proprio sui cespiti e sul magazzino conservati (metodo del valore residuo).</li>
<li><strong>Seguito:</strong> modelli di fattura senza IVA, imposta in conto per le prestazioni importate, registro di commercio e cassa di compensazione verificati separatamente.</li>
</ul>
<p>Ditta individuale, start-up in anno fiacco o PMI che scorpora un’attività – la disdetta è un passo singolo ma dalle conseguenze rilevanti nella chiusura d’esercizio. Verifichi termine e conteggio finale prima del 31 dicembre; per cespiti, immobili o dubbi sul vincolo della rinuncia, consulti preventivamente una <a href="kontakt.html">persona qualificata verificata</a>.</p>"""),
]

CONTENT = {"de": DE, "en": EN, "fr": FR, "it": IT}
REL = ["mwst-100k-pflicht-schweiz.html", "mwst-vorsteuer-eigenverbrauch-jahresende.html", "mwst-abrechnung-fristen.html"]

os.chdir(REPO)
for lang in ("de", "en", "fr", "it"):
    at.build(lang, SLUG, TITLE[lang], META[lang], CONTENT[lang], related=REL, sources=SRC[lang])
print("build complete:", SLUG)
