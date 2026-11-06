#!/usr/bin/env python3
"""Build stille-reserven-eigenkapitalaufbau-jahresende in 4 languages (cron, 2026-11-06).

Pinned card: pin-2026-11-06, demand high. Angle: Selbstständige + kleine KMU
(private-person lens per audience-focus rule — Einzelunternehmen benefit from
progression-arithmetic savings; AG/GmbH only mentioned for limits).

Every tax figure computed 2026-11-06 with the site's own ESTV-calibrated engine
(scripts/tax_engine.js, calcSimple, single taxpayer, default average communal
factors, church tax excluded):
  ZH Stadt 140k -> 115k taxable: total 27'575 -> 20'025 = save 7'550 (30.2%)
    federal part 6'009 -> 3'809 = 2'200; canton+city 21'566 -> 16'216 = 5'350
  Canton savings on CHF 25'000 (marginal): ZH 7'550/30.2, BE 8'689/34.8,
    LU 6'006/24.0, GL 7'028/28.1, ZG 5'191/20.8, SG 7'911/31.6,
    GR 7'240/29.0, TI 8'511/34.0, GE 8'637/34.5
  Realization year (ZH, profit 40k, +25k hidden reserves): t(65k)-t(40k)=4'377
    = 17.5% -> progression-arithmetic gain vs 30.2% = ~CHF 3'170
Legal facts checked 2026-11-06 against official documents (curl 200 each):
  - ESTV Kreisschreiben Nr. 28 (03.11.2010) verbatim quotes Art. 37b DBG:
    definitive cessation after 55th birthday or IV-invalidity; sum of hidden
    reserves realized in last 2 business years taxed separately; BVG-style
    buy-ins (Art. 33 Abs. 1 Bst. d DBG) deductible first against ordinary
    income; remainder at one-fifth of the Art. 36 tariff, minimum 2%;
    death: heirs/legatees if they do not continue the business, settlement at
    the latest 5 calendar years after the year of death; one-time use; minor
    subsequent self-employment without staff/premises allowed (below BVG
    entry threshold).
  - Art. 58 DBG commercial-assessment standard for Abschreibungen/
    Wertberichtigungen/Rückstellungen; non-justified ones added back
    (LU KG A-10/130 v. 20.10.2011; ZH Wegleitung Kapitalgesellschaften:
    "aus nicht versteuertem Gewinn gebildete stillen Reserven" taxed with
    last-year profit on cessation; "entsteuerte" reserves deducted on
    realization to avoid double taxation; Form. 530 listing).
  - BL Steuerbuch 24.18: cessation via sale or transfer to private assets.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "stille-reserven-eigenkapitalaufbau-jahresende"
RELATED3 = ["pensionskassen-einkauf-steuern-sparen.html",
            "saeule-3a-nachzahlen.html",
            "kapitalsteuer-ag-gmbh.html"]

URLS_DE = [
 ("https://www.fedlex.admin.ch/eli/cc/1990/426/de",
  "FedLex: Bundesgesetz über die direkte Bundessteuer (DBG, SR 642.1)"),
 ("https://www.estv.admin.ch/dam/de/sd-web/geU4pmmZRFPX/dbst-ks-2010-1-028-d-de.pdf",
  "ESTV: Kreisschreiben Nr. 28 – Besteuerung der Liquidationsgewinne (PDF)"),
 ("https://www.estv.admin.ch/de/kreisschreiben-direkten-bundessteuer",
  "ESTV: Kreisschreiben zur direkten Bundessteuer (Übersicht)"),
 ("https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/steuern-finanzen/steuern/juristischepersonen/2023/gewinnsteuer_wegleitung/505%20Wegl%20Kapitalges%20ZH%202023%20DEF.pdf",
  "Kanton Zürich: Wegleitung Gewinnsteuer Kapitalgesellschaften (PDF)"),
 ("https://kanton.baselland.ch/finanz-und-kirchendirektion/steuerverwaltung-steuerbuch/band-2/unternehmen/downloads-1/band2_024_18.pdf",
  "Finanzdepartement BL: Steuerbuch 24.18 – Liquidationsgewinn (PDF)"),
]
URLS_OTHER = [
 ("https://www.fedlex.admin.ch/eli/cc/1990/426/{l}", None),
 ("https://www.estv.admin.ch/dam/de/sd-web/geU4pmmZRFPX/dbst-ks-2010-1-028-d-de.pdf", "DE"),
 ("https://www.estv.admin.ch/de/kreisschreiben-direkten-bundessteuer", "DE"),
 ("https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/steuern-finanzen/steuern/juristischepersonen/2023/gewinnsteuer_wegleitung/505%20Wegl%20Kapitalges%20ZH%202023%20DEF.pdf", "DE"),
 ("https://kanton.baselland.ch/finanz-und-kirchendirektion/steuerverwaltung-steuerbuch/band-2/unternehmen/downloads-1/band2_024_18.pdf", "DE"),
]
LAB = {
 "en": ["FedLex: Federal Act on Direct Federal Tax (DBG, SR 642.1)",
        "FTA: Circular No. 28 – taxation of liquidation gains (PDF, German)",
        "FTA: Circulars on direct federal tax (overview, German)",
        "Canton Zurich: instructions for corporate profit tax (PDF, German)",
        "Canton Basel-Landschaft: tax handbook 24.18 – liquidation gain (PDF, German)"],
 "fr": ["FedLex : loi fédérale sur l’impôt fédéral direct (LIFD, RS 642.1)",
        "AFC : circulaire n° 28 – imposition des gains en liquidation (PDF, all.)",
        "AFC : circulaires sur l’impôt fédéral direct (aperçu, all.)",
        "Canton de Zurich : guide de l’impôt sur le bénéfice des personnes morales (PDF, all.)",
        "Canton de Bâle-Campagne :手册 replaced below"],
 "it": ["FedLex: legge federale sull’imposta federale diretta (LIFD, RS 642.1)",
        "AFC: circolare n. 28 – imposizione degli utili di liquidazione (PDF, ted.)",
        "AFC: circolari sull’imposta federale diretta (panoramica, ted.)",
        "Cantone Zurigo: istruzioni per l’imposta sull’utile delle persone giuridiche (PDF, ted.)",
        "Cantone Basilea Campagna: manuale fiscale 24.18 – utile di liquidazione (PDF, ted.)"],
}
LAB["fr"][4] = "Canton de Bâle-Campagne : manuel fiscal 24.18 – gain en liquidation (PDF, all.)"

def sources(lang):
    if lang == "de":
        return URLS_DE
    return [(u.replace("{l}", lang), LAB[lang][i]) for i, (u, _) in enumerate(URLS_OTHER)]

CTA = {
 "de": '<div class="cta-mid"><strong>Simulieren Sie Ihren Fall:</strong> Mit dem <a href="rechner.html">Steuerrechner</a> prüfen Sie in einer Minute, wie stark sich CHF 10\'000 – 50\'000 weniger Gewinn in Ihrem Kanton auf die Steuer auswirkt. Für die Bewertung Ihrer konkreten Positionen lohnt sich eine <a href="partner-pruefung.html">geprüfte Fachperson</a>: <a href="kontakt.html">unverbindliche Offerte anfragen</a>.</div>',
 "en": '<div class="cta-mid"><strong>Model your own case:</strong> the <a href="rechner.html">tax calculator</a> shows in one minute how much a reduction of CHF 10,000–50,000 in profit saves you in your canton. For valuing your specific balance-sheet items, a <a href="partner-pruefung.html">vetted professional</a> is worth it: <a href="kontakt.html">request a no-obligation quote</a>.</div>',
 "fr": '<div class="cta-mid"><strong>Calculez votre cas :</strong> le <a href="rechner.html">calculateur d’impôts</a> montre en une minute ce qu’économise une réduction du bénéfice de CHF 10\'000 à 50\'000 dans votre canton. Pour évaluer vos postes concrets, une <a href="partner-pruefung.html">personne vérifiée</a> vous y aide : <a href="kontakt.html">demandez une offre sans engagement</a>.</div>',
 "it": '<div class="cta-mid"><strong>Simulate your case:</strong> il <a href="rechner.html">calcolatore d’imposta</a> mostra in un minuto quanto fa risparmiare una riduzione dell’utile di CHF 10\'000–50\'000 nel vostro cantone. Per valutare le singole posizioni del bilancio, una <a href="partner-pruefung.html">persona verificata</a> è d’aiuto: <a href="kontakt.html">richiedete un’offerta non vincolante</a>.</div>',
}

# ---------------- DE ----------------
de_sections = [
 ("Was stille Reserven sind – und wem sie wirklich nutzen",
  """<p>Eine stille Reserve entsteht, wenn ein Betrieb Vermögen tiefer in den Büchern führt, als es wirklich da ist: Maschinen voll abgeschrieben, Lager zu tief bewertet, Forderungen mit Erfahrungszuschlägen entwertet, erkennbare Risiken als Rückstellung verbucht. Der Unterschied zwischen Buchwert und tatsächlichem Wert ist steuerlich <em>noch nicht versteuert</em> – und genau das ist der Hebel. Aufgedeckt oder realisiert, wird die Reserve später ganz normal als Ertrag besteuert.</p>
<p>Der doppelte Vorteil für Selbstständige und Inhaber von Einzelunternehmen: Erstens wirkt die <strong>progressionsarithmetische Arithmetik</strong> – die Bildung mindert das Ergebnis im Gewinnjahr zum <em>marginellen</em> Steuersatz, die spätere Realisierung wird oft in einem schwächeren Jahr zum <em>durchschnittlichen</em>, tieferen Satz taxed. Zweitens bleibt das Geld im Betrieb: Eine gebildete Rückstellung ist liquide, keine Ausgabe. Bei AG und GmbH ist der Effekt deutlich kleiner, weil deren Gewinn nahezu linear besteuert wird; der Eigenkapitalaufbau lohnt sich dort vor allem aus Risikogründen.</p>
<p><em>Praxis-Tipp:</em> Stille Reserven sind kein Jahresend-Trick, sondern Bilanzpolitik mit Substanz. Wer das ganze Jahr über Belege für Lager- und Debitorenrisiken sammelt, kann per 31.12.2026 sauber begründet buchen statt raten.</p>"""),
 ("Was Sie per 31. Dezember bilden dürfen – und was die Steuerbehörden aufrechnen",
  """<p>Massgebend ist die kaufmännische Beurteilung: Abschreibungen, Wertberichtigungen, Rückstellungen und Verluste sind abzugsfähig, soweit sie nach kaufmännischer Betrachtung erforderlich bzw. hinreichend bemessen sind (Art. 58 DBG; die Praxis der Kantone und des Bundesgerichts handhabt diesen Massstab bei Selbstständigen sinngemäss gleich). Erlaubt ist damit per Jahresende insbesondere:</p>
<ul>
<li><strong>Abschreibungen</strong> auf bewegliches Geschäftsvermögen bis gegen null, wenn Zustand und Nutzungsdauer es tragen;</li>
<li><strong>Wertberichtigungen</strong> auf Lager und Debitoren nach dokumentierten Erfahrungssätzen oder einzelnen erkennbaren Risiken;</li>
<li><strong>Rückstellungen</strong> für konkrete, dem Grunde nach feststehende Risiken – Garantieleistungen, hängende Prozesse, drohende Aufträge unter Selbstkosten;</li>
<li><strong>Passivische Rechnungsabgrenzungen</strong> für Vorauszahlungen und Anzahlungen, die erst 2027 verdient sind.</li>
</ul>
<p>Nicht anerkannt und im Veranlagungsverfahren aufgerechnet (mit Nachsteuerrisiko bei arglistigem Vorgehen) werden dagegen Pauschalreserven «ins Blaue» ohne greifbaren Anlass, Privataufwand, der als Geschäftsausgabe verbucht wird, und willkürliche Gewinnglättung über mehrere Jahre. Bei Geschäftsliegenschaften gilt eine Besonderheit: Buchwerte dürfen tief gehalten werden; wird die Liegenschaft ins Privatvermögen überführt, taxierbar sind grundsätzlich die «wieder eingebrachten Abschreibungen», während der Wertzuwachs bis zur Veräusserung aufgeschoben bleibt (ESTV-Kreisschreiben Nr. 28).</p>
<p><em>Praxis-Tipp:</em> Führen Sie zu jeder Position eine einseitige Begründung (Erfahrungswerte der letzten Jahre, Auftragsliste, Prozessverfügung). Kantonale Formulare wie die «Aufstellung über Rückstellungen/Wertberichtigungen» verlangen diese Einzelnachweise ohnehin – sauber dokumentierte Reserven überstehen jede Veranlagung.</p>"""),
 ("Rechenbeispiel: CHF 25'000 weniger Gewinn – was das in Zürich bringt",
  """<p>Ein selbstständiger Informatiker in der Stadt Zürich, ledig, kinderlos, erzielt 2026 einen Gewinn von CHF 140'000. Per 31.12. bildet er eine Rückstellung für ein hängendes Leistungsverweigerungsrecht (CHF 9'000), berichtigt Debitoren pauschal nach Erfahrungssatz (CHF 6'000) und schreibt eine Maschine vollständig ab (CHF 10'000). Total: <strong>CHF 25'000</strong> weniger steuerbarer Gewinn – der Buchgewinn 2026 sinkt auf CHF 115'000.</p>
<p>Die Rechnung mit den Tarifen 2026 (Kanton, Gemeinde mit durchschnitlichem Steuerfuss, direkte Bundessteuer; ohne Kirchensteuer):</p>
<table><thead><tr><th>Abgabe</th><th>Bei CHF 140'000 Gewinn</th><th>Bei CHF 115'000 Gewinn</th><th>Ersparnis</th></tr></thead><tbody>
<tr><td>Direkte Bundessteuer</td><td>CHF 6'009</td><td>CHF 3'809</td><td>CHF 2'200</td></tr>
<tr><td>Kantons- und Gemeindesteuern ZH</td><td>CHF 21'566</td><td>CHF 16'216</td><td>CHF 5'350</td></tr>
<tr><td><strong>Total</strong></td><td><strong>CHF 27'575</strong></td><td><strong>CHF 20'025</strong></td><td><strong>CHF 7'550</strong></td></tr>
</tbody></table>
<p>Die Ersparnis von CHF 7'550 entspricht einer Grenzbelastung von <strong>30,2 %</strong>. Wird die Reserve später in einem schwachen Geschäftsjahr realisiert, fallen darauf nur noch rund CHF 4'377 Steuer an (Unterrechnung im Abschnitt «Realisierung») – netto bleibt ein Gewinn von etwa CHF 3'170.<br><em>Illustratives Beispiel, gerundete Beträge; steuerbarer Gewinn vereinfacht = Gewinn vor Massnahme.</em></p>""" + CTA["de"]),
 ("Kantonstabelle: Bei CHF 25'000 Reserve schwankt die Ersparnis von CHF 5'200 bis CHF 8'700",
  """<p>Weil die Steuertarife kantonal stark abweichen, hängt der Wert einer Reserve am Grenzsteuersatz. Selbstständige in Bern oder Genf sparen pro Franken Reserve rund zwei Drittel mehr als solche im Kanton Zug:</p>
<table><thead><tr><th>Kanton (Hauptort, avg. Gemeinde)</th><th>Steuern bei CHF 140'000</th><th>Steuern bei CHF 115'000</th><th>Ersparnis auf CHF 25'000</th><th>Grenzbelastung</th></tr></thead><tbody>
<tr><td>Bern</td><td>CHF 36'577</td><td>CHF 27'888</td><td>CHF 8'689</td><td>34,8 %</td></tr>
<tr><td>Genf</td><td>CHF 34'168</td><td>CHF 25'531</td><td>CHF 8'637</td><td>34,5 %</td></tr>
<tr><td>Tessin</td><td>CHF 32'928</td><td>CHF 24'417</td><td>CHF 8'511</td><td>34,0 %</td></tr>
<tr><td>St. Gallen</td><td>CHF 32'213</td><td>CHF 24'302</td><td>CHF 7'911</td><td>31,6 %</td></tr>
<tr><td>Zürich (Stadt)</td><td>CHF 27'575</td><td>CHF 20'025</td><td>CHF 7'550</td><td>30,2 %</td></tr>
<tr><td>Graubünden</td><td>CHF 28'355</td><td>CHF 21'115</td><td>CHF 7'240</td><td>29,0 %</td></tr>
<tr><td>Glarus</td><td>CHF 28'068</td><td>CHF 21'040</td><td>CHF 7'028</td><td>28,1 %</td></tr>
<tr><td>Luzern</td><td>CHF 24'135</td><td>CHF 18'129</td><td>CHF 6'006</td><td>24,0 %</td></tr>
<tr><td>Zug</td><td>CHF 18'275</td><td>CHF 13'084</td><td>CHF 5'191</td><td>20,8 %</td></tr>
</tbody></table>
<p>Rechenbasis: ledige Person ohne Kinder, gleiche Kantons- und Gemeindesteuerfüsse und gleiche direkte Bundessteuer in allen Zeilen (ESTV-Tarifdaten 2026; ohne Kirchensteuer, ohne individuelle Abzüge). Wer in einem tiefen Kanton wohnt und später in einem hohen Kanton realisiert (oder umgekehrt), verschiebt den Effekt zusätzlich – ein Argument, die <a href="rechner.html">Simulation</a> mit dem eigenen Standort zu wiederholen.</p>"""),
 ("Realisierung: ordinär, im tiefen Jahr – oder privilegiert nach Art. 37b DBG",
  """<p>Ohne besonderen Antritt wird die aufgelöste Reserve im Realisierungsjahr <strong>ordinär besteuert</strong>. Wer klug plant, legt die Auflösung in ein schwaches Geschäftsjahr: Im Zürcher Beispiel erzielt der Informatiker 2028 nur CHF 40'000 Gewinn; kommen die CHF 25'000 Reserve hinzu, steigt die Steuer um CHF 4'377 – eine Belastung von nur <strong>17,5 %</strong> statt 30,2 %. Gegenüber der Bildung ergibt das einen Gewinn von rund CHF 3'170 plus den Zinsvorteil des Aufschubs.</p>
<p>Deutlich stärker wirkt der privilegierte Zugang: Wer seine selbstständige Erwerbstätigkeit <strong>nach dem vollendeten 55. Altersjahr oder wegen Invalidität definitiv aufgibt</strong>, versteuert die Summe der in den letzten zwei Geschäftsjahren realisierten stillen Reserven getrennt vom übrigen Einkommen – zu einem <strong>Fünftel des ordentlichen Tarifs</strong>, jedoch mit einem Mindeststeuersatz von 2 % (Art. 37b DBG; Einzelheiten regelt die Liquidationsgewinnverordnung LGBV). Freiwillige BVG-Einkäufe im Liquidationsjahr und Vorjahr werden zuerst vom ordentlichen Einkommen abgezogen und reduzieren sonst den privilegierten Gewinn. Im Todesfall können Erben und Vermächtnisnehmer, die den Betrieb nicht weiterführen, dieselbe Begünstigung verlangen – die Abrechnung muss spätestens fünf Kalenderjahre nach dem Todesjahr erfolgen.</p>
<p>Zwei Fallstricke: Der Vorzug wird nur <em>einmal</em> gewährt – wer danach erneut selbstständig erwerbstätig ist, profitiert bei der nächsten Aufgabe nicht mehr. Und eine «geringfügige» Weiterbeschäftigung ohne Personal und Räumlichkeiten ist erlaubt, bleibt aber an die BVG-Eintrittsschwelle gebunden.</p>"""),
 ("Stille Reserven, Säule 3a, Pensionskasse: das Jahresende-Trio im Vergleich",
  """<p>Für Selbstständige konkurrieren Ende 2026 drei Instrumente um dieselbe Ersparnis. Die Maximalbeträge sind gesetzlich fix, die stillen Reserven sind es nicht:</p>
<table><thead><tr><th>Instrument</th><th>Maximal 2026</th><th>Wirkung</th><th>Nachteil</th></tr></thead><tbody>
<tr><td>Säule 3a</td><td>CHF 7'258 mit / CHF 36'288 ohne 2. Säule</td><td>Sofortabzug, gesperrtes Vorsorgegeld</td><td>Blockiert bis Vorsorgealter, Bezug versteuert</td></tr>
<tr><td>Freiwilliger 2.-Säulen-Einkauf</td><td>Bis zum maximal möglichen Einkauf (Altersgitter)</td><td>Wie 3a, oft höhere Beträge</td><td>Teilweise 3-Jahres-Sperrfrist bei Bezug</td></tr>
<tr><td>Stille Reserven</td><td>Kein Limit – kaufmännisch begründet</td><td>Aufschub + Progressionsvorteil, Kapital bleibt frei</td><td>Besteuerung nur aufgeschoben; ohne 37b-Voraussetzungen ordinär</td></tr>
</tbody></table>
<p>Die sinnvolle Reihenfolge: Zuerst die vollen Vorsorge-Abzüge, denn sie sind steuerlich «sicher» und endgültig. Restliches Sparpotenzial gehört in sauber begründete Reserven – am besten im eigenen <a href="rechner.html">Steuerrechner</a> durchgespielt; die 3a-Alternative prüft der <a href="3a-rechner.html">Säule-3a-Rechner</a>.</p>""" + CTA["de"]),
 ("Kurz gesagt",
  """<ul>
<li>Stille Reserven = Vermögen tiefer buchen als es ist; Bildung mindert den Gewinn 2026, Realisierung besteuert ihn später.</li>
<li>Erlaubt: Abschreibungen, Wertberichtigungen und Rückstellungen nach kaufmännischer Beurteilung (Art. 58 DBG) – alles «ins Blaue» wird aufgerechnet.</li>
<li>Beispiel Zürich: CHF 25'000 Reserve spart CHF 7'550 Steuern (30,2 %); in Zug sind es CHF 5'191, in Bern CHF 8'689.</li>
<li>Auflösung ins schwache Jahr legen; bei definitiver Aufgabe ab 55 oder wegen IV: Separate Besteuerung zu 1/5 des Tarifs, min. 2 % (Art. 37b DBG).</li>
<li>Reihenfolge: Säule 3a (CHF 7'258) und BVG-Einkauf zuerst, dann stille Reserven – <a href="rechner.html">rechnerisch prüfen</a>.</li>
<li>Allgemeine Information, keine individuelle Beratung – geprüfte Fachpersonen finden Sie <a href="partner-pruefung.html">hier</a>, Offerte auf <a href="kontakt.html">kontakt.html</a>.</li>
</ul>"""),
]

# ---------------- EN ----------------
en_sections = [
 ("What hidden reserves are — and who really benefits",
  """<p>A hidden reserve exists whenever a business carries assets lower than their true value: machinery written down to zero, inventory held at a discount, receivables reduced by documented loss rates, identifiable risks booked as provisions. The gap between book value and real value has <em>not yet been taxed</em> — and that is exactly the lever. Once revealed or realised, the reserve is taxed as ordinary income later on.</p>
<p>Self-employed individuals and sole-proprietor owners enjoy a double benefit. First, <strong>progressive-rate arbitrage</strong>: forming the reserve reduces profit in a strong year at the <em>marginal</em> rate, while the later realisation is often taxed in a weaker year at a lower <em>average</em> rate. Second, the money stays in the business — a booked provision is liquidity, not an expense. For AG and GmbH companies the effect is far smaller, because corporate profit is taxed almost proportionally; there, building equity pays mainly for risk reasons.</p>
<p><em>Practical tip:</em> hidden reserves are not an end-of-year trick but balance-sheet management with substance. Collect evidence on inventory and debtor risks all year and you can book well-founded entries on 31.12.2026 instead of guessing.</p>"""),
 ("What you may form on 31 December — and what tax authorities add back",
  """<p>The benchmark is prudent commercial judgement: depreciations, write-downs, provisions and losses are deductible insofar as they are required or sufficiently sized under commercial assessment (Art. 58 of the Direct Federal Tax Act; cantons and the Federal Supreme Court apply the same standard to the self-employed in substance). What year-end legitimately allows:</p>
<ul>
<li><strong>Depreciation</strong> of movable business assets down to near zero where condition and useful life support it;</li>
<li><strong>Write-downs</strong> on inventory and receivables based on documented experience rates or specific identifiable risks;</li>
<li><strong>Provisions</strong> for concrete risks — warranty obligations, pending litigation, contracts expected below cost;</li>
<li><strong>Deferred income</strong> for advance payments and deposits not yet earned in 2027.</li>
</ul>
<p>Not recognised — and added back at assessment, with reassessment risk in cases of concealment — are flat-risk reserves without a tangible trigger, private spending booked as a business expense, and arbitrary profit smoothing across years. Business real estate has a special regime: book values may be kept low; when the property is transferred to private wealth, what is generally taxed are the "reintroduced depreciation" amounts, while the appreciation gain stays deferred until sale (FTA Circular No. 28).</p>
<p><em>Practical tip:</em> keep a one-page justification per item (multi-year experience rates, order list, court order). Cantonal schedules such as the "statement of provisions and write-downs" demand exactly that — and well-documented reserves survive any assessment.</p>"""),
 ("Worked example: CHF 25,000 less profit — what it saves in Zurich",
  """<p>A self-employed IT specialist in the city of Zurich, single, no children, books a 2026 profit of CHF 140,000. On 31.12. he forms a provision for a pending performance dispute (CHF 9,000), writes down receivables by a documented experience rate (CHF 6,000) and fully depreciates a machine (CHF 10,000). Total: <strong>CHF 25,000</strong> less taxable profit — the 2026 book result falls to CHF 115,000.</p>
<p>The bill under 2026 tariffs (canton, commune at average multiplier, direct federal tax; church tax excluded):</p>
<table><thead><tr><th>Levy</th><th>At CHF 140,000 profit</th><th>At CHF 115,000 profit</th><th>Saving</th></tr></thead><tbody>
<tr><td>Direct federal tax</td><td>CHF 6,009</td><td>CHF 3,809</td><td>CHF 2,200</td></tr>
<tr><td>Cantonal and communal tax ZH</td><td>CHF 21,566</td><td>CHF 16,216</td><td>CHF 5,350</td></tr>
<tr><td><strong>Total</strong></td><td><strong>CHF 27,575</strong></td><td><strong>CHF 20,025</strong></td><td><strong>CHF 7,550</strong></td></tr>
</tbody></table>
<p>The CHF 7,550 saving equals a marginal burden of <strong>30.2%</strong>. If the reserve is revealed later in a weak business year, the CHF 25,000 attracts only about CHF 4,377 of tax (computation in the realisation section below) — a net gain of roughly CHF 3,170 compared with never having built the reserve, plus the interest benefit of deferral.<br><em>Illustrative example, rounded; taxable income simplified = profit before the measure.</em></p>""" + CTA["en"]),
 ("Cantonal table: the saving on a CHF 25,000 reserve ranges from CHF 5,191 to CHF 8,689",
  """<p>Because tax scales differ sharply between cantons, the value of a reserve follows the marginal rate. Self-employed people in Bern or Geneva save roughly two-thirds more per reserved franc than those in Zug:</p>
<table><thead><tr><th>Canton (capital, average commune)</th><th>Tax at CHF 140,000</th><th>Tax at CHF 115,000</th><th>Saving on CHF 25,000</th><th>Marginal burden</th></tr></thead><tbody>
<tr><td>Bern</td><td>CHF 36,577</td><td>CHF 27,888</td><td>CHF 8,689</td><td>34.8%</td></tr>
<tr><td>Geneva</td><td>CHF 34,168</td><td>CHF 25,531</td><td>CHF 8,637</td><td>34.5%</td></tr>
<tr><td>Ticino</td><td>CHF 32,928</td><td>CHF 24,417</td><td>CHF 8,511</td><td>34.0%</td></tr>
<tr><td>St. Gallen</td><td>CHF 32,213</td><td>CHF 24,302</td><td>CHF 7,911</td><td>31.6%</td></tr>
<tr><td>Zurich (city)</td><td>CHF 27,575</td><td>CHF 20,025</td><td>CHF 7,550</td><td>30.2%</td></tr>
<tr><td>Grisons</td><td>CHF 28,355</td><td>CHF 21,115</td><td>CHF 7,240</td><td>29.0%</td></tr>
<tr><td>Glarus</td><td>CHF 28,068</td><td>CHF 21,040</td><td>CHF 7,028</td><td>28.1%</td></tr>
<tr><td>Lucerne</td><td>CHF 24,135</td><td>CHF 18,129</td><td>CHF 6,006</td><td>24.0%</td></tr>
<tr><td>Zug</td><td>CHF 18,275</td><td>CHF 13,084</td><td>CHF 5,191</td><td>20.8%</td></tr>
</tbody></table>
<p>Basis: single taxpayer without children, identical federal tax and average communal multipliers in every row (FTA 2026 tariff data; church tax and individual deductions excluded). Residing in a low-tax canton and revealing the reserve in a high-tax one (or vice versa) shifts the effect again — one more reason to rerun the <a href="rechner.html">simulation</a> for your own location.</p>"""),
 ("Realisation: ordinary in a weak year — or privileged under Art. 37b",
  """<p>Absent a special trigger, a revealed reserve is taxed <strong>ordinarily</strong> in the year of realisation. Plan the release into a weak business year: in the Zurich example the specialist earns only CHF 40,000 in 2028; adding the CHF 25,000 reserve raises the bill by CHF 4,377 — a burden of just <strong>17.5%</strong> instead of 30.2%. Compared with the original deduction that is a net gain of roughly CHF 3,170, plus the interest benefit of deferral.</p>
<p>The privileged route is far stronger: whoever <strong>definitively ceases self-employment after the age of 55 or due to disability</strong> taxes the hidden reserves realised in the last two business years separately from all other income — at <strong>one-fifth of the ordinary tariff</strong>, subject to a minimum rate of 2% (Art. 37b DBG; details in the liquidation-gain ordinance LGBV). Voluntary pension-fund buy-ins in the liquidation year and the year before are first deducted from ordinary income and otherwise reduce the privileged gain. In the event of death, heirs and legatees who do not continue the business may claim the same relief — the assessment must happen at the latest five calendar years after the year of death.</p>
<p>Two traps: the privilege is granted <em>once</em> — a later return to self-employment enjoys it no more. And only a "minor" continuing activity without staff or premises is permitted, capped at the occupational-pension entry threshold.</p>"""),
 ("Hidden reserves vs. pillar 3a vs. pension fund: the year-end trio compared",
  """<p>At the end of 2026 three instruments compete for the same saving. The contribution caps are fixed by law; hidden reserves are not:</p>
<table><thead><tr><th>Instrument</th><th>2026 maximum</th><th>Effect</th><th>Trade-off</th></tr></thead><tbody>
<tr><td>Pillar 3a</td><td>CHF 7,258 with / CHF 36,288 without 2nd pillar</td><td>Immediate deduction, locked retirement capital</td><td>Blocked until retirement; withdrawal taxed</td></tr>
<tr><td>Voluntary 2nd-pillar buy-in</td><td>Up to the age-grid maximum</td><td>Like 3a, often larger amounts</td><td>Withdrawal sometimes blocked for 3 years</td></tr>
<tr><td>Hidden reserves</td><td>No limit — as far as commercially justified</td><td>Deferral plus progressive-rate gain, capital stays free</td><td>Tax only postponed; ordinary unless Art. 37b applies</td></tr>
</tbody></table>
<p>The sensible order of battle: use up the secure retirement deductions first, since they are final. Remaining headroom belongs in well-founded reserves — best rehearsed in your own <a href="rechner.html">tax calculator</a>; the <a href="3a-rechner.html">pillar 3a calculator</a> checks the alternative.</p>""" + CTA["en"]),
 ("In short",
  """<ul>
<li>Hidden reserves = carrying assets below real value; forming them cuts 2026 profit, realising them taxes it later.</li>
<li>Allowed: depreciation, write-downs and provisions under prudent commercial judgement (Art. 58 DBG) — anything arbitrary is added back.</li>
<li>Zurich example: a CHF 25,000 reserve saves CHF 7,550 (30.2%); in Zug CHF 5,191, in Bern CHF 8,689.</li>
<li>Release in a weak year; on definitive cessation after 55 or due to disability: separate tax at 1/5 of the tariff, minimum 2% (Art. 37b DBG).</li>
<li>Sequence: pillar 3a (CHF 7,258) and pension buy-ins first, hidden reserves after — <a href="rechner.html">run the numbers</a>.</li>
<li>General information, not individual advice — find vetted professionals <a href="partner-pruefung.html">here</a> or request a quote at <a href="kontakt.html">kontakt.html</a>.</li>
</ul>"""),
]

# ---------------- FR ----------------
fr_sections = [
 ("Ce que sont les réserves latentes — et qui en profite vraiment",
  """<p>Une réserve latente existe dès qu’une entreprise inscrit des actifs en dessous de leur valeur réelle : machines amorties à zéro, stocks sous-évalués, créances corrigées par des taux d’expérience, risques identifiables provisionnés. L’écart entre la valeur comptable et la valeur effective n’est <em>pas encore imposé</em> — c’est précisément le levier. Lors de sa révélation ou de sa réalisation, la réserve est imposée plus tard comme revenu ordinaire.</p>
<p>Les indépendants et les propriétaires de raison individuelle bénéficient d’un double avantage. D’abord l’<strong>arbitrage progressif</strong> : la constitution réduit le bénéfice d’une année forte au taux <em>marginal</em>, tandis que la réalisation ultérieure est souvent imposée lors d’une année plus faible, à un taux moyen inférieur. Ensuite, l’argent reste dans l’entreprise — une provision est de la liquidité, pas une dépense. Pour les SA et Sàrl, l’effet est nettement plus faible, leur bénéfice étant imposé de manière quasi proportionnelle ; chez elles, constituer des fonds propres sert avant tout la maîtrise des risques.</p>
<p><em>Conseil pratique :</em> les réserves latentes ne sont pas un truc de fin d’année mais une politique de bilan crédible. Documentez toute l’année vos risques sur les stocks et les débiteurs pour passer des écritures solides au 31.12.2026.</p>"""),
 ("Ce que vous pouvez constituer au 31 décembre — et ce que les autorités réintègrent",
  """<p>La référence est le jugement commercial prudent : amortissements, dépréciations, provisions et pertes sont déductibles dans la mesure où ils sont nécessaires ou suffisamment dimensionnés selon l’appréciation commerciale (art. 58 LIFD ; les cantons et le Tribunal fédéral appliquent en substance le même standard aux indépendants). En fin d’exercice, sont légitimes notamment :</p>
<ul>
<li>les <strong>amortissements</strong> d’actifs mobiliers commerciaux jusqu’à près de zéro, si l’état et la durée d’utilisation le justifient ;</li>
<li>les <strong>dépréciations</strong> sur stocks et créances fondées sur des taux d’expérience documentés ou des risques spécifiques ;</li>
<li>les <strong>provisions</strong> pour des risques concrets — garanties, litiges en cours, commandes attendues à perte ;</li>
<li>les <strong>produits constatés d’avance</strong> pour acomptes et arrhes non encore gagnés en 2027.</li>
</ul>
<p>Ne sont pas admises — et sont réintégrées à taxation, avec risque de rappel en cas de dissimulation — les réserves forfaitaires « au doigt mouillé » sans déclencheur tangible, les dépenses privées passées en charges et les lissages arbitraires de bénéfices. Les immeubles commerciaux obéissent à un régime spécial : les valeurs comptables peuvent rester basses ; en cas de transfert dans la fortune privée, sont en principe imposables les amortissements « réintroduits », le gain d’estimation restant différé jusqu’à la vente (circulaire AFC n° 28).</p>
<p><em>Conseil pratique :</em> joignez à chaque poste une justification d’une page (séries d’expérience, liste de commandes, ordonnance). Les états cantonaux des provisions l’exigent de toute façon — une réserve bien documentée survit à toute taxation.</p>"""),
 ("Exemple chiffré : CHF 25'000 de bénéfice en moins — ce que ça rapporte à Zurich",
  """<p>Un informaticien indépendant en ville de Zurich, célibataire sans enfant, réalise un bénéfice 2026 de CHF 140'000. Au 31.12., il constitue une provision pour un litige d’exécution en cours (CHF 9'000), corrige ses créances selon un taux d’expérience (CHF 6'000) et amortit totalement une machine (CHF 10'000). Total : <strong>CHF 25'000</strong> de bénéfice imposable en moins — le résultat 2026 tombe à CHF 115'000.</p>
<p>La facture selon les tarifs 2026 (canton, commune au coefficient moyen, impôt fédéral direct ; hors impôt ecclésiastique) :</p>
<table><thead><tr><th>Prélèvement</th><th>Sur bénéfice de CHF 140'000</th><th>Sur bénéfice de CHF 115'000</th><th>Économie</th></tr></thead><tbody>
<tr><td>Impôt fédéral direct</td><td>CHF 6'009</td><td>CHF 3'809</td><td>CHF 2'200</td></tr>
<tr><td>Impôts cantonal et communal ZH</td><td>CHF 21'566</td><td>CHF 16'216</td><td>CHF 5'350</td></tr>
<tr><td><strong>Total</strong></td><td><strong>CHF 27'575</strong></td><td><strong>CHF 20'025</strong></td><td><strong>CHF 7'550</strong></td></tr>
</tbody></table>
<p>L’économie de CHF 7'550 correspond à une charge marginale de <strong>30,2 %</strong>. Si la réserve est révélée plus tard dans un exercice creux, les CHF 25'000 ne supportent alors qu’environ CHF 4'377 d’impôt (détail plus bas) — soit un gain net d’environ CHF 3'170 par rapport à une absence de réserve, avantage d’intérêt du report compris.<br><em>Exemple illustratif, montants arrondis ; revenu imposable simplifié = bénéfice avant mesure.</em></p>""" + CTA["fr"]),
 ("Tableau cantonal : de CHF 5'191 à CHF 8'689 d’économie pour une réserve de CHF 25'000",
  """<p>Les barèmes variant fortement d’un canton à l’autre, la valeur d’une réserve suit le taux marginal. Un indépendant bernois ou genevois économise environ deux tiers de plus par franc réservé qu’un collègue zougois :</p>
<table><thead><tr><th>Canton (chef-lieu, commune moyenne)</th><th>Impôt à CHF 140'000</th><th>Impôt à CHF 115'000</th><th>Économie sur CHF 25'000</th><th>Charge marginale</th></tr></thead><tbody>
<tr><td>Berne</td><td>CHF 36'577</td><td>CHF 27'888</td><td>CHF 8'689</td><td>34,8 %</td></tr>
<tr><td>Genève</td><td>CHF 34'168</td><td>CHF 25'531</td><td>CHF 8'637</td><td>34,5 %</td></tr>
<tr><td>Tessin</td><td>CHF 32'928</td><td>CHF 24'417</td><td>CHF 8'511</td><td>34,0 %</td></tr>
<tr><td>Saint-Gall</td><td>CHF 32'213</td><td>CHF 24'302</td><td>CHF 7'911</td><td>31,6 %</td></tr>
<tr><td>Zurich (ville)</td><td>CHF 27'575</td><td>CHF 20'025</td><td>CHF 7'550</td><td>30,2 %</td></tr>
<tr><td>Grisons</td><td>CHF 28'355</td><td>CHF 21'115</td><td>CHF 7'240</td><td>29,0 %</td></tr>
<tr><td>Glaris</td><td>CHF 28'068</td><td>CHF 21'040</td><td>CHF 7'028</td><td>28,1 %</td></tr>
<tr><td>Lucerne</td><td>CHF 24'135</td><td>CHF 18'129</td><td>CHF 6'006</td><td>24,0 %</td></tr>
<tr><td>Zoug</td><td>CHF 18'275</td><td>CHF 13'084</td><td>CHF 5'191</td><td>20,8 %</td></tr>
</tbody></table>
<p>Base : personne seule sans enfants, impôt fédéral et coefficient communal moyen identiques sur chaque ligne (données tarifaires AFC 2026 ; hors impôt ecclésiastique et déductions individuelles). Habiter un canton peu chargé et réaliser la réserve dans un canton plus fort (ou l’inverse) décale encore l’effet — une raison de plus de rejouer la <a href="rechner.html">simulation</a> avec votre propre situation.</p>"""),
 ("Réalisation : ordinaire en année faible — ou privilégiée selon l’art. 37b LIFD",
  """<p>Sans événement particulier, la réserve révélée est imposée <strong>normalement</strong> l’année de sa réalisation. Placez la reprise sur un exercice creux : dans l’exemple zurichois, l’informaticien ne réalise que CHF 40'000 de bénéfice en 2028 ; l’ajout des CHF 25'000 de réserve n’augmente la facture que de CHF 4'377 — une charge de <strong>17,5 %</strong> au lieu de 30,2 %. Par rapport à la déduction initiale, le gain net atteint environ CHF 3'170, sans compter l’avantage d’intérêt du report.</p>
<p>La voie privilégiée est bien plus forte : celui qui <strong>cesse définitivement son activité indépendante après 55 ans révolus ou pour cause d’invalidité</strong> impose les réserves latentes réalisées lors des deux derniers exercices séparément du reste du revenu — au <strong>cinquième du barème ordinaire</strong>, avec un taux minimal de 2 % (art. 37b LIFD ; détails dans l’ordonnance sur les gains en liquidation, OGL). Les rachats volontaires de 2e pilier faits l’année de la liquidation et l’année précédente s’imputent d’abord sur le revenu ordinaire, sinon ils réduisent le gain privilégié. En cas de décès, les héritiers et légataires qui ne poursuivent pas l’entreprise peuvent exiger le même traitement — le décompte doit intervenir au plus tard cinq années civiles après l’année du décès.</p>
<p>Deux pièges : le privilège n’est accordé qu’<em>une fois</em> — un retour ultérieur à l’indépendance n’en bénéficie plus. Et seule une activité résiduelle « mineure », sans personnel ni locaux, reste admise, plafonnée au seuil d’entrée du 2e pilier.</p>"""),
 ("Réserves latentes, pilier 3a, caisse de pension : le trio de fin d’année",
  """<p>Fin 2026, trois instruments se disputent la même économie. Les plafonds de cotisation sont légaux ; les réserves latentes ne le sont pas :</p>
<table><thead><tr><th>Instrument</th><th>Maximum 2026</th><th>Effet</th><th>Contrepartie</th></tr></thead><tbody>
<tr><td>Pilier 3a</td><td>CHF 7'258 avec / CHF 36'288 sans 2e pilier</td><td>Déduction immédiate, capital de prévoyance bloqué</td><td>Bloqué jusqu’à la retraite ; prestataire imposable</td></tr>
<tr><td>Rachat volontaire 2e pilier</td><td>Jusqu’au maximum lié à l’âge</td><td>Comme le 3a, souvent des montants supérieurs</td><td>Blocage de 3 ans pour la prestation en capital</td></tr>
<tr><td>Réserves latentes</td><td>Aucune limite — dans les bornes du jugement commercial</td><td>Report + arbitrage progressif, capital restant libre</td><td>Impôt seulement différé ; ordinaire sauf art. 37b</td></tr>
</tbody></table>
<p>Le bon ordre : épuiser d’abord les déductions de prévoyance, sûres et définitives. Le reliquat de capacité d’épargne va dans des réserves bien fondées — à rejouer dans votre propre <a href="rechner.html">calculateur d’impôts</a> ; le <a href="3a-rechner.html">calculateur du pilier 3a</a> vérifie l’alternative.</p>""" + CTA["fr"]),
 ("En bref",
  """<ul>
<li>Réserve latente = actifs inscrits sous leur valeur réelle ; la constitution allège le bénéfice 2026, la réalisation l’impose plus tard.</li>
<li>Admis : amortissements, dépréciations et provisions selon le jugement commercial (art. 58 LIFD) — tout ce qui est arbitraire est réintégré.</li>
<li>Exemple Zurich : une réserve de CHF 25'000 économise CHF 7'550 (30,2 %) ; à Zoug CHF 5'191, à Berne CHF 8'689.</li>
<li>Reprise en année faible ; cessation définitive après 55 ans ou pour invalidité : imposition séparée au cinquième du barème, min. 2 % (art. 37b LIFD).</li>
<li>Ordre : pilier 3a (CHF 7'258) et rachats LPP d’abord, réserves ensuite — <a href="rechner.html">calculez</a>.</li>
<li>Information générale, pas un conseil individuel — trouvez un <a href="partner-pruefung.html">spécialiste vérifié</a> ou demandez une offre sur <a href="kontakt.html">kontakt.html</a>.</li>
</ul>"""),
]

# ---------------- IT ----------------
it_sections = [
 ("Cosa sono le riserve latenti — e chi ne trae davvero vantaggio",
  """<p>Una riserva latente esiste quando un’azienda iscrive il patrimonio a valori inferiori a quelli reali: macchinari ammortizzati a zero, magazzino sottovalutato, crediti rettificati con aliquote di esperienza, rischi riconoscibili accantonati a fondo. La differenza tra valore contabile e valore effettivo <em>non è ancora stata tassata</em> — ed è esattamente questa la leva. Quando viene rivelata o realizzata, la riserva è tassata più tardi come ricavo ordinario.</p>
<p>I lavoratori indipendenti e i titolari di ditte individuali godono di un doppio vantaggio. Primo, l’<strong>arbitraggio progressivo</strong>: la costituzione riduce l’utile di un anno forte all’aliquota <em>marginale</em>, mentre la realizzazione successiva spesso ricade in un anno debole, a un’aliquota media inferiore. Secondo, il denaro resta in azienda: un fondo è liquidità, non una spesa. Per SA e Sagl l’effetto è nettamente più piccolo, poiché l’utile è tassato quasi in proporzione; lì il rafforzamento dei mezzi propri conviene soprattutto per ragioni di rischio.</p>
<p><em>Suggerimento pratico:</em> le riserve latenti non sono un trucco di fine anno, ma una politica di bilancio con sostanza. Raccogliete durante tutto l’anno le prove sui rischi di magazzino e dei debitori per poter scrivere partite ben motivate il 31.12.2026.</p>"""),
 ("Cosa potete costituire al 31 dicembre — e cosa le autorità riaddebitano",
  """<p>Il parametro è la prudente valutazione commerciale: ammortamenti, rettifiche di valore, fondi e perdite sono deducibili nella misura in cui risultano necessari o adeguatamente dimensionati secondo il giudizio commerciale (art. 58 LIFD; cantoni e Tribunale federale applicano in sostanza lo stesso criterio agli indipendenti). A fine esercizio sono legittimi in particolare:</p>
<ul>
<li>gli <strong>ammortamenti</strong> di cespiti mobili commerciali fino a quasi zero, se lo giustificano stato e vita utile;</li>
<li>le <strong>rettifiche di valore</strong> su magazzino e crediti basate su aliquote di esperienza documentate o su rischi singoli;</li>
<li>i <strong>fondi</strong> per rischi concreti — garanzie, cause in corso, commesse in perdita attesa;</li>
<li>i <strong>ratei e risconti passivi</strong> per acconti non ancora guadagnati nel 2027.</li>
</ul>
<p>Non sono ammessi — e vengono riaddebitati in tassazione, con rischio di suppletoria in caso di occultamento — i fondi forfettari «a naso» senza un fatto scatenante concreto, le spese private iscritte a costi e il livellamento arbitrario degli utili. Gli immobili commerciali seguono un regime speciale: i valori contabili possono restare bassi; in caso di trasferimento nel patrimonio privato sono in linea di principio tassabili gli ammortamenti «reintegrati», mentre la plusvalore resta differita fino alla vendita (circolare AFC n. 28).</p>
<p><em>Suggerimento pratico:</em> allegate a ogni voce una motivazione di una pagina (serie storiche, lista ordini, provvedimento giudiziale). I formulari cantonali sui fondi lo esigono comunque — una riserva ben documentata supera qualsiasi tassazione.</p>"""),
 ("Esempio di calcolo: CHF 25'000 di utile in meno — quanto si risparmia a Zurigo",
  """<p>Un informatico indipendente in città di Zurigo, celibe, senza figli, realizza nel 2026 un utile di CHF 140'000. Al 31.12. constitui un fondo per una controversia in essere (CHF 9'000), rettifica i crediti con un’aliquota di esperienza (CHF 6'000) e ammortizza integralmente una macchina (CHF 10'000). Totale: <strong>CHF 25'000</strong> di utile imponibile in meno — l’utile contabile 2026 scende a CHF 115'000.</p>
<p>Il conto secondo le aliquote 2026 (cantone, Comune con moltiplicatore medio, imposta federale diretta; senza imposta ecclesiastica):</p>
<table><thead><tr><th>Prelievo</th><th>Su utile di CHF 140'000</th><th>Su utile di CHF 115'000</th><th>Risparmio</th></tr></thead><tbody>
<tr><td>Imposta federale diretta</td><td>CHF 6'009</td><td>CHF 3'809</td><td>CHF 2'200</td></tr>
<tr><td>Imposte cantonali e comunali ZH</td><td>CHF 21'566</td><td>CHF 16'216</td><td>CHF 5'350</td></tr>
<tr><td><strong>Totale</strong></td><td><strong>CHF 27'575</strong></td><td><strong>CHF 20'025</strong></td><td><strong>CHF 7'550</strong></td></tr>
</tbody></table>
<p>Il risparmio di CHF 7'550 corrisponde a un onere marginale del <strong>30,2 %</strong>. Se la riserva viene rivelata più tardi in un esercizio fiacco, i CHF 25'000 supportano allora solo circa CHF 4'377 di imposta (dettaglio più sotto) — con un guadagno netto di circa CHF 3'170 rispetto alla rinuncia all’accantonamento, oltre al vantaggio d’interesse del rinvio.<br><em>Esempio indicativo, importi arrotondati; reddito imponibile semplificato = utile prima della misura.</em></p>""" + CTA["it"]),
 ("Tabella cantonale: da CHF 5'191 a CHF 8'689 di risparmio per una riserva di CHF 25'000",
  """<p>Poiché le scale di imposizione variano molto da cantone a cantone, il valore di una riserva segue l’aliquota marginale. Un indipendente bernese o ginevrino risparmia circa due terzi in più per franco accantonato rispetto a un collega zughese:</p>
<table><thead><tr><th>Cantone (capoluogo, Comune medio)</th><th>Imposte su CHF 140'000</th><th>Imposte su CHF 115'000</th><th>Risparmio su CHF 25'000</th><th>Onere marginale</th></tr></thead><tbody>
<tr><td>Berna</td><td>CHF 36'577</td><td>CHF 27'888</td><td>CHF 8'689</td><td>34,8 %</td></tr>
<tr><td>Ginevra</td><td>CHF 34'168</td><td>CHF 25'531</td><td>CHF 8'637</td><td>34,5 %</td></tr>
<tr><td>Ticino</td><td>CHF 32'928</td><td>CHF 24'417</td><td>CHF 8'511</td><td>34,0 %</td></tr>
<tr><td>Sancogallo</td><td>CHF 32'213</td><td>CHF 24'302</td><td>CHF 7'911</td><td>31,6 %</td></tr>
<tr><td>Zurigo (città)</td><td>CHF 27'575</td><td>CHF 20'025</td><td>CHF 7'550</td><td>30,2 %</td></tr>
<tr><td>Grigioni</td><td>CHF 28'355</td><td>CHF 21'115</td><td>CHF 7'240</td><td>29,0 %</td></tr>
<tr><td>Glarona</td><td>CHF 28'068</td><td>CHF 21'040</td><td>CHF 7'028</td><td>28,1 %</td></tr>
<tr><td>Lucerna</td><td>CHF 24'135</td><td>CHF 18'129</td><td>CHF 6'006</td><td>24,0 %</td></tr>
<tr><td>Zugo</td><td>CHF 18'275</td><td>CHF 13'084</td><td>CHF 5'191</td><td>20,8 %</td></tr>
</tbody></table>
<p>Base: persona single senza figli, imposta federale e moltiplicatore comunale medi identici su ogni riga (dati tariffali AFC 2026; senza imposta ecclesiastica e deduzioni individuali). Abitare in un cantone leggero e rivelare la riserva in uno pesante (o viceversa) sposta ulteriormente l’effetto — un buon motivo per ripetere la <a href="rechner.html">simulazione</a> con la propria situazione.</p>"""),
 ("Realizzazione: ordinaria nell’anno debole — o privilegiata secondo l’art. 37b LIFD",
  """<p>In assenza di un evento specifico, la riserva rivelata è tassata <strong>normalmente</strong> nell’anno di realizzazione. Pianificate la ripresa in un esercizio fiacco: nell’esempio zurighese l’informatico realizza nel 2028 solo CHF 40'000 di utile; aggiungendo i CHF 25'000 di riserva il conto cresce di CHF 4'377 — un onere del <strong>17,5 %</strong> invece del 30,2 %. Rispetto alla deduzione iniziale ne risulta un guadagno di circa CHF 3'170, più il vantaggio d’interesse del rinvio.</p>
<p>La via privilegiata è molto più forte: chi <strong>cessa definitivamente l’attività indipendente dopo il compimento del 55° anno di età o per invalidità</strong> tassa le riserve latenti realizzate negli ultimi due esercizi separatamente dal resto del reddito — a un <strong>quinto della tariffa ordinaria</strong>, con un’aliquota minima del 2 % (art. 37b LIFD; dettagli nell’ordinanza sugli utili di liquidazione, OUL). I versamenti volontari nel 2° pilastro fatti nell’anno di liquidazione e in quello precedente sono dedotti prima dal reddito ordinario, altrimenti riducono l’utile privilegiato. In caso di successione, gli eredi e i legatari che non proseguono l’azienda possono esigere lo stesso trattamento — il conteggio va effettuato al più tardi cinque anni civili dopo l’anno del decesso.</p>
<p>Due trappole: il privilegio è concesso <em>una sola volta</em> — chi riprende in seguito un’attività indipendente non ne beneficia più. Ed è ammessa solo un’attività residua «modesta», senza personale né locali, entro la soglia d’entrata del 2° pilastro.</p>"""),
 ("Riserve latenti, pilastro 3a, cassa pensione: il trio di fine anno",
  """<p>A fine 2026 tre strumenti si contendono lo stesso risparmio. I massimali contributivi sono fissati per legge; le riserve latenti no:</p>
<table><thead><tr><th>Strumento</th><th>Massimale 2026</th><th>Effetto</th><th>Contropartita</th></tr></thead><tbody>
<tr><td>Pilastro 3a</td><td>CHF 7'258 con / CHF 36'288 senza 2° pilastro</td><td>Deduzione immediata, capitale previdenziale vincolato</td><td>Bloccato fino alla pensione; prestazione imponibile</td></tr>
<tr><td>Versamento volontario 2° pilastro</td><td>Fino al massimo legato all’età</td><td>Come il 3a, spesso importi maggiori</td><td>Blocco di 3 anni sulla prestazione in capitale</td></tr>
<tr><td>Riserve latenti</td><td>Nessun limite — nei confini della valutazione commerciale</td><td>Rinvio + arbitraggio progressivo, capitale resta libero</td><td>Imposta solo rinviata; ordinaria fuorché art. 37b</td></tr>
</tbody></table>
<p>L’ordine sensato: esaurire prima le deduzioni previdenziali, sicure e definitive. La capacità di risparmio residua va in riserve ben motivate — meglio se simulate nel proprio <a href="rechner.html">calcolatore d’imposta</a>; il <a href="3a-rechner.html">calcolatore del pilastro 3a</a> verifica l’alternativa.</p>""" + CTA["it"]),
 ("In sintesi",
  """<ul>
<li>Riserva latente = patrimonio iscritto sotto il valore reale; la costituzione alleggerisce l’utile 2026, la realizzazione lo tassa più tardi.</li>
<li>Ammessi: ammortamenti, rettifiche e fondi secondo la valutazione commerciale (art. 58 LIFD) — tutto ciò che è arbitrario viene riaddebitato.</li>
<li>Esempio Zurigo: una riserva di CHF 25'000 fa risparmiare CHF 7'550 (30,2 %); a Zugo CHF 5'191, a Berna CHF 8'689.</li>
<li>Ripresa nell’anno debole; cessazione definitiva dopo i 55 anni o per invalidità: imposizione separata a 1/5 della tariffa, min. 2 % (art. 37b LIFD).</li>
<li>Sequenza: prima pilastro 3a (CHF 7'258) e versamenti LPP, poi le riserve — <a href="rechner.html">fate i conti</a>.</li>
<li>Informazione generale, non consulenza individuale — trovate un <a href="partner-pruefung.html">consulente verificato</a> o chiedete un’offerta su <a href="kontakt.html">kontakt.html</a>.</li>
</ul>"""),
]

def main():
    jobs = [
        ("de", "Stille Reserven 2026: Eigenkapitalaufbau für KMU richtig nutzen",
         "Stille Reserven per 31.12.2026: was Selbstständige und kleine KMU bei Rückstellungen und Abschreibungen steuerlich nutzen – Rechenbeispiel, Kantonstabelle, Art. 37b DBG."),
        ("en", "Hidden Reserves 2026: Year-End Equity Building for the Self-Employed",
         "Build hidden reserves by 31.12.2026: what the self-employed and small firms may book, what gets added back – worked Zurich example, cantonal table, Art. 37b relief on liquidation."),
        ("fr", "Réserves latentes 2026 : constituer des fonds propres en fin d’année",
         "Réserves latentes au 31.12.2026 : ce que les indépendants et les petites entreprises peuvent constituer – exemple chiffré à Zurich, tableau cantonal, privilège de l’art. 37b LIFD."),
        ("it", "Riserve latenti 2026: rafforzare i mezzi propri a fine anno",
         "Riserve latenti al 31.12.2026: cosa gli indipendenti e le piccole aziende possono accantonare – esempio zurighese, tabella cantonale, privilegio dell’art. 37b LIFD."),
    ]
    sec = {"de": de_sections, "en": en_sections, "fr": fr_sections, "it": it_sections}
    for lang, title, meta in jobs:
        path = build(lang, SLUG, title, meta, sec[lang], related=RELATED3, sources=sources(lang))
        print("built:", path)

if __name__ == "__main__":
    main()
