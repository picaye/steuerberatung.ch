#!/usr/bin/env python3
"""Build 5 new DE articles from the 2026-10-14 research batch.

Sources (verified 2026-10-14):
- EU-Zoll: zoll.de (Wegfall 150-Euro-Grenze, VO (EU) 2026/382 v. 11.2.2026, 3 EUR je Warenkategorie, IOSS Code 500), bmf.gv.at
- Mini-Jobs: Merkblatt 2.04 via AK Zug/AK OW/SVA SZ/AK SO (2'500-Grenze ab 1.1.2025, vorher 2'300; Schwelle kein Freibetrag), svazurich.ch (Sackgeld 750 bis 25 J.), akso.ch (Kultur/Medien ab 2026), Art. 52 AHVG
- MWST-Ausfuhr: bazg.admin.ch (eVV Export, Form. 11.44, Ausfuhrdokument Reiseverkehr), bern-cci.ch + douana.ch + finesolutions.ch (Passar ab 1.1.2026, e-dec Export ab 31.12.2025 offline, Chartera Output)
- QSt-NOV: ESTV Steuerbegriffe "Besteuerung an der Quelle" (6/2025: 31. März Folgejahr, 120'000 obligatorisch, Art. 137 DBG/Art. 49 StHG), KStV ZH (§ Ende März), FR + TG Steuerämter
- Kapitalsteuer: ESTV Steuerbegriffe "Steuersatz und Steuerfuss" (1/2026: UR keine kantonale KS, LU 0,01‰ Beteiligungen, VD Obergrenze 7‰/30%), StG AG §86 (0,75‰, Anrechnung, §88 Mindeststeuer 500), Kantonsblatt AG
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

# ============ A1: EU 3-Euro-Zoll ============
SLUG1 = "eu-zoll-3-euro-kleinsendungen"
REL1 = ["mwst-ausfuhr-0-prozent-nachweis.html", "mwst-100k-pflicht-schweiz.html", "transparenzregister-tjpg-meldepflicht.html"]
de1_title = "Schweizer Onlineshops in die EU: Seit Juli 2026 Zoll auf Kleinsendungen"
de1_meta = "Die EU hat die 150-Euro-Zollfreigrenze gekippt (Verordnung (EU) 2026/382, seit 1.7.2026): Für Fernverkäufe aus Drittländern – auch aus der Schweiz – gilt pauschal 3 EUR Zoll pro Warenkategorie, Übergangsrecht bis Mitte 2028. Was Schweizer Shops bei IOSS, Checkout und Päckli-Kosten jetzt prüfen müssen."
de1_sections = [
("Was sich am 1. Juli 2026 geändert hat",
 """<p>Wer aus der Schweiz in die EU verkauft, kennt die alte Regel: Päckli mit einem Warenwert bis 150 Euro waren zollfrei. Diese Freigrenze existiert nicht mehr. Der Rat der Europäischen Union hat am 11. Februar 2026 die <strong>Verordnung (EU) 2026/382</strong> erlassen, die die bisherige Zollbefreiungsverordnung (EG) Nr. 1186/2009 ändert – <strong>mit Wirkung zum 1. Juli 2026</strong>.</p>
<p>Seither gilt für Sendungen im Fernverkauf aus Drittländern – also auch aus der Schweiz – ein <strong>pauschaler Zoll von 3 Euro pro Warenkategorie</strong>. «Warenkategorie» bedeutet: je angemeldeter Position der Zollanmeldung. Ein Päckli mit drei verschiedenen Artikelgruppen kostet damit 9 Euro Zoll, nicht 3.</p>
<p>Die deutsche Zollverwaltung (zoll.de) und das österreichische Finanzministerium (bmf.gv.at) bestätigen die Regelung übereinstimmend. Wichtig: Es geht um den <strong>Zoll</strong> – die Einfuhrumsatzsteuer fällt unabhängig davon weiterhin an (die 22-Euro-Freigrenze für Steuern war bereits 2021 entfallen).</p>
<p>Und es kommt noch mehr: Nach jetzigem Stand erhebt die EU <strong>ab dem 1. November 2026</strong> bei Fernabsatzsendungen zusätzlich eine <strong>Abfertigungspauschale («Union Handling Fee») von 2 Euro je Warenkategorie</strong> – unabhängig vom Warenwert, nicht erstattungsfähig und mit der Annahme der Zollanmeldung geschuldet. Die Höhe von 2 Euro basiert auf Entwürfen, die laut zoll.de noch nicht abschliessend beschlossen sind; der Mechanismus selbst ist angekündigt. Für ein Päckli aus drei Warenkategorien summieren sich damit ab November 2026 rasch 9 Euro Zoll plus 6 Euro Abfertigungspauschale.</p>"""),
("IOSS-Sendungen: immer 3 Euro, keine Präferenz",
 """<p>Viele Schweizer Shops wickeln EU-Pakete über das <strong>IOSS-Verfahren</strong> ab (Import One-Stop-Shop): Die Mehrwertsteuer wird bereits im Checkout erhoben und über ein EU-Mitgliedland abgeführt. Für den Zoll ändert IOSS an der Zahlungspflicht nichts – im Gegenteil:</p>
<p>Laut österreichischem BMF ist bei IOSS-Sendungen gemäss Art. 2 lit. a der VO (EU) 2026/382 <strong>generell der 3-Euro-Zoll vorgesehen, eine Zollpräferenz ist ausgeschlossen</strong>. In der Zollanmeldung ist dafür der Präferenzcode «500» zu erklären. Wer also über IOSS verkauft, plant die 3 Euro pro Warenposition besser fest in die Marge ein.</p>
<p>Für nicht-IOSS-Sendungen im Fernverkauf bis 150 Euro gilt der Pauschalzoll ebenfalls – hier kann unter Umständen eine Präferenz (z. B. das Freihandelsabkommen Schweiz–EU) greifen, sofern Ursprungsnachweise vorliegen. Das prüft der Zoll-Dienstleister im Einzelfall.</p>"""),
("Was das für Schweizer Shops konkret bedeutet",
 """<p>Der Pauschalzoll ist klein – die Wirkung ist es nicht immer:</p>
<ul><li><strong>Warenkorb-Grösse:</strong> Bei einem 25-Euro-Produkt sind 3 Euro Zoll plus Abfertigungskosten ein spürbarer Aufschlag – und ein klassischer Abbruch-Grund an der Kasse, wenn der Kunde ihn erst bei der Zustellung sieht.</li>
<li><strong>Positionen zählen:</strong> Mischpakete werden nach Warenkategorien abgerechnet. Sortimentsbündelung (mehr Exemplare derselben Kategorie pro Paket) bleibt zolltechnisch vorteilhaft.</li>
<li><strong>Übergabe vs. DDP:</strong> Wer «Delivered Duty Paid» (Verzollung durch den Shop) anbietet, muss die 3 Euro vorfinanzieren und im Preis einkalkulieren; wer dem Kunden die Zahlung überlässt, riskiert Zustellverweigerungen und Retouren.</li>
<li><strong>Weihnachtsgeschäft:</strong> November und Dezember sind der erste Höhepunkt unter neuem Recht – die erste Bewährungsprobe für Checkout-Logik und Kommunikation.</li></ul>"""),
("Übergangsrecht bis Mitte 2028",
 """<p>Der 3-Euro-Pauschalzoll ist ausdrücklich eine <strong>befristete Übergangslösung</strong>. Die eigentliche EU-Zollreform sieht eine zentrale EU-Zolldatenplattform (Customs Data Hub) vor, über die Einfuhrabgaben künftig vollständig digital erhoben werden sollen – frühestens ab 2028. Bis dahin gilt das Pauschalregime für Kleinsendungen; Details zu Referenzbeträgen und Sicherheitennachweisen regelt die Durchführungsverordnung (EU) 2015/2447 (Art. 155 Abs. 3 lit. c UZK-IA, geändert durch VO (EU) 2026/1200).</p>
<p>Für Schweizer Verkäufer heisst das: Die 3 Euro sind der Anfang, nicht das Ende der Regulierung. Wer seine Daten heute sauber hält (Warennummern, Werte, Ursprung), ist 2028 im Vorteil.</p>"""),
("Checkliste: Diese sechs Punkte jetzt prüfen",
 """<ol><li><strong>IOSS-Registrierung</strong> aktuell? EU-Identifikationsnummer im Checkout sichtbar?</li>
<li><strong>Warennummern (CN-Codes)</strong> pro Artikel gepflegt – damit die Zollanmeldung die Positionen korrekt bündelt?</li>
<li><strong>Preisdarstellung:</strong> zeigt der Checkout «inkl. Zoll» oder «zzgl. Einfuhrabgaben»? Beides ist legal, Irreführung nicht.</li>
<li><strong>Logistikvertrag:</strong> Wer verzollt – Carrier, Zollunternehmen, Shop? Wer trägt die 3 Euro bei DDP?</li>
<li><strong>Kundenkommunikation:</strong> Info-Text auf der Produktseite und in der Sendungsverfolgung.</li>
<li><strong>Marge:</strong> 3 Euro je Warenposition im Sortiment kalkuliert – auch bei Aktionsware?</li>
<li><strong>Ab November 2026:</strong> zusätzlich 2 Euro Union Handling Fee je Kategorie einplanen – Checkout-Preise vor dem Weihnachtsgeschäft anpassen.</li></ol>"""),
("Kurz zusammengefasst",
 """<ul><li>Seit 1.7.2026: keine 150-Euro-Zollfreigrenze mehr in der EU (VO (EU) 2026/382 des Rates vom 11.2.2026).</li>
<li>3 Euro Zoll pro Warenkategorie (je Position der Zollanmeldung) für Fernverkaufssendungen aus Drittländern – auch aus der Schweiz.</li>
<li>Bei IOSS-Sendungen fällt der Pauschalzoll immer an; Zollpräferenz ausgeschlossen (Code 500).</li>
<li>Einfuhrumsatzsteuer bleibt davon unabhängig geschuldet.</li>
<li>Ab 1.11.2026 zusätzlich 2 EUR Abfertigungspauschale (Union Handling Fee) je Warenkategorie angekündigt – Höhe im Entwurf.</li>
<li>Übergangsrecht bis zur EU-Zollplattform (frühestens 2028) – Datenpflege lohnt sich doppelt.</li>
<li>Allgemeine Information, keine Rechtsberatung – für den Einzelfall Zollunternehmen oder Fachanwalt beiziehen.</li></ul>"""),
]

# ============ A2: Mini-Jobs / AHV ============
SLUG2 = "minijobs-lohnschwelle-ahv-pflicht"
REL2 = ["quellensteuer-nov-zusatzabzuege.html", "grenzgaenger-de-fr-it-steuern.html", "ahv-mindestbeitrag-selbststaendige.html"]
de2_title = "Mini-Jobs und Saisonpersonal: Wann Lohnbeiträge und Meldepflichten ausgelöst werden"
de2_meta = "Kurze, unregelmässige Einsätze bis CHF 2'500 Lohn pro Person und Jahr können AHV-frei sein – aber nur, wenn die Grenze pro Arbeitgeber eingehalten wird. Schwellenwert statt Freibetrag, Haushalts-Ausnahme ab dem ersten Franken, Kultur und Medien ab 2026 neu dabei: die Checkliste für Arbeitgeber im Weihnachtsgeschäft."
de2_sections = [
("Die 2'500-Franken-Grenze: geringfügige Löhne",
 """<p>Wer einer Aushilfe pro Kalenderjahr <strong>höchstens CHF 2'500.-</strong> bezahlt, muss grundsätzlich <strong>keine Beiträge an AHV, IV, EO und ALV</strong> abrechnen – es sei denn, die versicherte Person verlangt es ausdrücklich. Das ist die Freigrenze für geringfügige Entgelte (Merkblatt 2.04 der AHV-Ausgleichskassen). Der Betrag wurde per 1. Januar 2025 von CHF 2'300.- auf CHF 2'500.- erhöht.</p>
<p>Entscheidend: Die Grenze gilt <strong>pro Arbeitgeber und Kalenderjahr</strong>. Alle Entgelte, die eine Arbeitgeberin derselben Person im laufenden Jahr ausrichtet – inkl. Nebenbezüge, Trinkgelder und Naturalleistungen –, sind zusammenzählen.</p>"""),
("Schwellenwert, kein Freibetrag – der klassische Fehler",
 """<p>Wird CHF 2'500.- auch nur um einen Franken überschritten, sind <strong>nicht nur derüberschiessende Betrag, sondern der gesamte Lohn beitragspflichtig</strong>. Die Ausgleichskassen sprechen bewusst von einer Grenze, nicht von einem Abzug. Wer im Dezember mit dem dritten Einsatz die Schwelle reissen lässt, zahlt Beiträge auf dem Jahreslohn nach – inklusive Verzugszins.</p>
<p>Die Beiträge richten sich nach dem vollen Satz: 5,3 % AHV/IV/EO plus 1,1 % ALV je Seite (Arbeitgeber halbiert gesamt 12,8 % plus Verwaltungskosten und Familienausgleich nach kantonaler Kasse).</p>"""),
("Ausnahmen: Privathaushalte, Kultur und Medien",
 """<p>Für zwei Bereiche gilt die Freigrenze <strong>nicht</strong> – Beiträge fallen ab dem ersten Franken an:</p>
<ul><li><strong>Privathaushalte</strong> (Hausdienstarbeit: Reinigung, Garten, Kinderbetreuung, Haushaltshilfe): beitragspflichtig in jedem Fall (Merkblatt 2.06). Ausnahme «Sackgeldjobs»: Wer im betreffenden Kalenderjahr höchstens 25 Jahre alt wird, verdient bis CHF 750.- pro Privathaushalt und Jahr beitragsfrei (Stand 2026: Jahrgänge 2001–2008; darüber gilt die Grenze nicht mehr).</li>
<li><strong>Kultur- und Medienschaffende:</strong> Löhne von Tanz- und Theaterproduktionen, Ton- und Bildproduzenten, Radio und Fernsehen sowie künstlerischen Ausbildungsinstitutionen sind immer beitragspflichtig. <strong>Ab 1. Januar 2026</strong> hat der Bundesrat die Beitragspflicht per EEL-Änderung auf weitere Branchen ausgedehnt – neu u. a. Design, Museen, Medien und Chöre (Information der AHV-Ausgleichskasse Solothurn).</li></ul>"""),
("Wer profitiert vom Beitragsverlangen – und wer haftet",
 """<p>Auch unter CHF 2'500.- kann die versicherte Person <strong>Beitragszahlung verlangen</strong>. Das lohnt sich besonders für Studierende und junge Erwerbstätige: Die Beiträge füllen Beitragslücken im individuellen AHV-Konto und können später beim Nichterwerbsbeitrag von Verheirateten angerechnet werden.</p>
<p>Umgekehrt gilt: Akzeptiert die Arbeitnehmerin den Lohn ungekürzt ohne Abzug, kann der Arbeitgeber die Arbeitnehmerbeiträge <strong>nachträglich nicht mehr einfordern</strong>. Und wer Beiträge als Arbeitgeber gar nicht oder zu spät abführt, haftet gemäss <strong>Art. 52 AHVG</strong> für den ganzen Schaden – er trägt dann auch den Arbeitnehmeranteil, ohne Rückgriffsrecht.</p>"""),
("Meldepflichten und Quellensteuer bei Kurzlöhnen",
 """<p>Beitragsfreiheit heisst nicht Anonymität: Auch geringfügig Beschäftigte sind der Ausgleichskasse zu melden, sobald Beiträge geschuldet sind oder verlangt werden. Für <strong>Ausländische ohne Wohnsitz in der Schweiz</strong> (Grenzgänger, Kurzaufenthalter) greift zusätzlich die <strong>Quellensteuer ab dem ersten Franken</strong> – die AHV-Freigrenze schützt davor nicht. Der Lohnausweis ist auch bei Mini-Jobs auszustellen.</p>"""),
("Checkliste für den Saisonstart (November bis Januar)",
 """<ol><li><strong>Jahreslohn pro Person und Arbeitgeber</strong> führen – inkl. aller Nebenbezüge; vor jedem neuen Einsatz die kumulierte Summe prüfen.</li>
<li><strong>Branche checken:</strong> Privathaushalt, Kultur, Design, Medien, Museum, Chor? Dann Beiträge ab dem ersten Franken.</li>
<li><strong>Alter der Aushilfe</strong> notieren (Sackgeldregel bis 25 Jahren in Haushalten).</li>
<li><strong>Beitragsverlangen dokumentieren</strong>, wenn die Person Beiträge wünscht.</li>
<li><strong>Quellensteuer-Pflicht</strong> bei Wohnsitz im Ausland ab erstem Franken einplanen.</li>
<li><strong>Lohnausweis</strong> auch bei Mini-Jobs erstellen und aufbewahren (10 Jahre).</li></ol>"""),
("Kurz zusammengefasst",
 """<ul><li>Bis CHF 2'500.- Lohn pro Person und Arbeitgeber im Kalenderjahr: keine AHV/IV/EO/ALV-Beiträge – ausser die Person verlangt sie (Merkblatt 2.04; Grenze seit 1.1.2025).</li>
<li>Überschreitung = Beiträge auf dem gesamten Lohn (Schwellenwert, kein Freibetrag) – Nachforderung inkl. Verzugszins.</li>
<li>Privathaushalte sowie Kultur-/Medienbereich (ab 2026 erweitert auf Design, Museen, Medien, Chöre): Beiträge ab dem ersten Franken.</li>
<li>Arbeitgeber haftet nach Art. 52 AHVG für nicht abgezogene Arbeitnehmeranteile.</li>
<li>Quellensteuer bei ausländischem Wohnsitz gilt unabhängig von der AHV-Grenze.</li>
<li>Allgemeine Information, keine Einzelfallberatung – Fragen klärt die zuständige Ausgleichskasse.</li></ul>"""),
]

# ============ A3: MWST-Ausfuhrnachweis ============
SLUG3 = "mwst-ausfuhr-0-prozent-nachweis"
REL3 = ["eu-zoll-3-euro-kleinsendungen.html", "mwst-agov-pflicht-oktober-2026.html", "mwst-100k-pflicht-schweiz.html"]
de3_title = "MWST 0 % bei Export: Diese Ausfuhrbelege akzeptiert die ESTV"
de3_meta = "Ins Ausland gelieferte Ware ist MWST-befreit – aber nur mit gültigem Ausfuhrnachweis. Seit 2026 läuft die Ausfuhranmeldung über Passar statt e-dec: Welche Belege (eVV Export, Formular 11.44, Ausfuhrdokument im Reiseverkehr) zählen, und was ohne Nachweis passiert."
de3_sections = [
("0 % Steuer ist eine Beweisfrage",
 """<p>Lieferungen ins Ausland sind von der Mehrwertsteuer befreit bzw. zum Satz von 0 % steuerbar (Art. 6 Abs. 2 Bst. a MWSTG). Aber: Die Steuerbefreiung ist <strong>keine Selbstverständlichkeit, sondern eine Beweisfrage</strong>. Die ESTV hält sich an den Grundsatz, dass der steuerpflichtige Lieferer den Export nachweisen muss. Gelingt der Nachweis nicht, wird die Lieferung im Inland nachversteuert – mit dem Inlandsatz von aktuell 8,1 %, obwohl der ausländische Kunde netto bezahlt hat.</p>
<p>Genau das ist der Klassiker in MWST-Kontrollen: Verkauf verbucht, Steuer deklariert mit 0 %, aber kein gültiger Ausfuhrbeleg in der Ablage. Die Rückforderung geht voll zulasten der Marge.</p>"""),
("Passar hat e-dec Export abgelöst (seit 1.1.2026)",
 """<p>Für den Nachweis hat sich 2026 Grundlegendes geändert: Das BAZG hat das alte System <strong>e-dec Export per 31. Dezember 2025 ausser Betrieb genommen</strong>. Ausfuhranmeldungen laufen seit <strong>1. Januar 2026 ausschliesslich über Passar</strong> (www.passar.admin.ch). Für Exporteure hat das praktische Folgen:</p>
<ul><li>Die <strong>elektronische Veranlagungsverfügung Ausfuhr (eVV Export)</strong> ist der zentrale Ausfuhrnachweis – sie muss aus Passar aktiv abgeholt werden, manuell über das Tool «Chartera Output» oder automatisiert über eine Zollsoftware, und danach elektronisch archiviert werden.</li>
<li>Rechtsgültig ist die Verfügung als PDF nur <strong>mit eingebettetem XML-Teil</strong> – ein Screenshot oder ein reiner Ausdruck genügt nicht.</li>
<li>Für Tabakfabrikate gelten verlängerte Übergangsfristen; das <strong>Formular 11.44</strong> (zollamtlich gestempeltes Doppel der Zollanmeldung für Rohtabak und Tabakfabrikate) bleibt als Belegform bestehen.</li>
<li>e-dec Web kann vorübergehend weiter genutzt werden; die definitive Ablösung wird separat kommuniziert.</li></ul>"""),
("Diese Belege akzeptiert die ESTV",
 """<p>Das BAZG listet die tauglichen Ausfuhrnachweise abschliessend im Grundsatz auf:</p>
<ol><li><strong>Elektronische Ausfuhrveranlagungsverfügung (eVV Export)</strong> mit digitaler Signatur – der Regelfall bei gewerblichen Exporten (seit 2026 aus Passar).</li>
<li><strong>Zollamtlich gestempeltes Doppel der Zollanmeldung für Rohtabak und Tabakfabrikate (Form. 11.44).</strong></li>
<li><strong>Zollamtlich bestätigtes «Ausfuhrdokument im Reiseverkehr»</strong> – der Beleg für Ladengeschäfte, die Ware an Reisende verkaufen (Tax-free-Prozedere; Details bei der ESTV unter «VAT-Refund: Rückerstattung an Unternehmen im Ausland»).</li>
<li><strong>Zollamtliche Dokumente über ordentlich abgeschlossene Verfahren</strong> – z. B. wenn ein Gegenstand nach vorübergehender Verwendung im Inland ausgeführt und im Ausland veranlagt wurde.</li></ol>
<p>Kann die Ausfuhr mit keinem dieser Dokumente nachgewiesen werden, greift die Auffangregel: Die Lieferungen sind im Inland zu versteuern.</p>"""),
("Reiseverkehr: der Beleg am Grenzübergang",
 """<p>Verkauft ein Ladengeschäft an Touristinnen und Touristen, ersetzt das <strong>Ausfuhrdokument im Reiseverkehr</strong> die gewerbliche Zollanmeldung: Die Ware wird bei der Ausreise am Zollamt angemeldet und gestempelt bzw. elektronisch bestätigt (Ausfuhrmeldung). Ohne dieses Dokument gilt die Lieferung als Inlandumsatz – die Rückerstattung der bezahlten Steuer an die Kundschaft scheitert am fehlenden Nachweis. Für Unternehmen mit Kundschaft aus der EU gilt dasselbe Verfahren umgekehrt auch für die Verifizierung von Tax-free-Rückerstattungen.</p>"""),
("Aufbewahrung und Kontrollpraxis",
 """<p>Geschäftsunterlagen – und damit jeder Ausfuhrbeleg – sind <strong>zehn Jahre</strong> aufzubewahren (Art. 49 Abs. 2 MWSTG). Die ESTV prüft bei Kontrollen nicht stichprobenartig «ob exportiert wurde», sondern <strong>ob pro Position ein Beleg existiert</strong>. Die saubere Verknüpfung von Handelsrechnung, Passar-Anmeldung und eVV Export (inkl. XML) ist die halbe MWST-Prüfung.</p>
<p>Praxistipp: Die eVV Export enthält die Veranlagungsbestätigung der Ausfuhr; wer sie «proaktiv abholt und archiviert» (so die Empfehlung des BAZG), statt sie im System liegen zu lassen, vermeidet die häufigste Fallstricke-Konstellation: Ware raus, Beleg nie geholt, Steuer zurückgefordert.</p>"""),
("Checkliste für exportierende Unternehmen",
 """<ol><li><strong>Passar-Onboarding</strong> erledigt? UID in der Zollkundenverwaltung (ZKV) registriert, Rolle «Dokumentenbezug im Warenverkehr» im ePortal aktiviert?</li>
<li><strong>Bezug der eVV Export</strong> organisiert (Chartera Output oder Zollsoftware) – inkl. Archivierung des PDFs mit XML?</li>
<li><strong>Reiseverkehr:</strong> Prozesse für Ausfuhrmeldungen am Grenzübergang definiert?</li>
<li><strong>Tabak:</strong> Übergangsregelungen und Formular 11.44 beachtet?</li>
<li><strong>Rechnungsstellung:</strong> 0 %-Satz mit Hinweis auf Ausfuhrleistung; Referenz auf Zollanmeldungsnummer?</li>
<li><strong>Aufbewahrung:</strong> Belege 10 Jahre revisionssicher gesichert?</li></ol>"""),
("Kurz zusammengefasst",
 """<ul><li>MWST-Befreiung bei Export = Beweislast beim Lieferer; ohne Beleg werden 8,1 % nachversteuert.</li>
<li>Seit 1.1.2026: Ausfuhr nur noch via Passar; e-dec Export ist abgeschaltet. Zentrale Nachweis ist die eVV Export mit digitaler Signatur (PDF nur mit eingebettetem XML gültig).</li>
<li>Weitere taugliche Belege: Formular 11.44 (Tabak), Ausfuhrdokument im Reiseverkehr, zollamtliche Verfahrensdokumente.</li>
<li>Aufbewahrungspflicht: 10 Jahre.</li>
<li>Allgemeine Information, keine Einzelfallberatung – im Zweifel ESTV oder MWST-Experte beiziehen.</li></ul>"""),
]

# ============ A4: Quellensteuer NOV ============
SLUG4 = "quellensteuer-nov-zusatzabzuege"
REL4 = ["grenzgaenger-de-fr-it-steuern.html", "expats-steuern-schweiz.html", "saeule-3a-nachzahlen.html"]
de4_title = "Quellensteuer: Zusatzabzüge nachmelden bis 31. März"
de4_meta = "Krankheitskosten, Weiterbildung, echte Berufskosten, Drittbetreuung: Abzüge, die der Quellensteuertarif nicht enthält, gibt es nur mit nachträglicher ordentlicher Veranlagung (NOV). Antrag bis 31. März des Folgejahres – für Periode 2026 also bis 31.3.2027. Wer muss, wer sollte, was bringt es."
de4_sections = [
("Warum der Quellensteuertarif zu wenig abzieht",
 """<p>Der Quellensteuerabzug ist eine <strong>pauschalierte Endsteuer</strong>: Im Tarif sind Berufskosten, Versicherungsprämien und Abzüge nur pauschal enthalten. Wer höhere tatsächliche Kosten hat – effektive Berufskosten statt Pauschale, Krankheits- und Unfallkosten, Weiterbildungen, Drittbetreuungskosten, Beiträge an die Säule 3a, Unterhaltszahlungen –, sieht davon in der monatlichen Abrechnung nichts.</p>
<p>Diese <strong>Zusatzabzüge</strong> lassen sich nur über die nachträgliche ordentliche Veranlagung (NOV) holen: Die Steuerbehörde veranlagt wie im ordentlichen Verfahren, rechnet die Quellensteuer an und erstattet die Differenz, wenn sie zu hoch ausgefallen ist.</p>"""),
("Die Frist: 31. März des Folgejahres",
 """<p>Der Antrag auf nachträgliche ordentliche Veranlagung ist <strong>an eine harte Frist</strong> gebunden: Er muss bis <strong>Ende März des der Steuerperiode folgenden Jahres</strong> beim kantonalen Steueramt eintreffen (ESTV-Merkblatt «Besteuerung an der Quelle»; ebenso die Quellensteuerverordnung des Kantons Zürich: «bis Ende März des Folgejahres»; bestätigt durch die Steuerämter FR und TG für die Periodepraxis). Für die <strong>Steuerperiode 2026 endet die Frist am 31. März 2027</strong>.</p>
<p>Wer die Frist verpasst, verliert die Abzüge sang- und klanglos: Ohne NOV tritt die Quellensteuer endgültig an die Stelle der Bundes-, Kantons- und Gemeindesteuern auf dem Erwerbseinkommen – zusätzliche Abzüge werden dann keine gewährt.</p>"""),
("Wer muss, wer sollte den Antrag stellen",
 """<p><strong>Obligatorisch</strong> ist die NOV für quellensteuerpflichtige Personen mit Wohnsitz oder Aufenthalt in der Schweiz, wenn das Bruttoeinkommen <strong>CHF 120'000.- pro Jahr</strong> übersteigt (ESTV-Merkblatt). Hier erfolgt die Veranlagung von Amtes wegen – der Antrag erübrigt sich, die Zusatzabzüge sind aber geltend zu machen.</p>
<p><strong>Freiwillig</strong> lohnt sich der Antrag für alle übrigen, deren effektive Abzüge die Tarifpauschalen übersteigen. Typische Kandidaten: Personen mit hohen echten Fahrt- und Verpflegungskosten, Familien mit Drittbetreuung, Personen mit Krankheitskosten über den Abzugsfranchisen, Zahlende von Unterhalt.</p>
<p><strong>Auch Nicht-Ansässige</strong> (Grenzgänger, Personen mit Aufenthalt im Ausland) können die NOV beantragen, um persönliche Abzüge geltend zu machen – für sie ist das Verfahren der einzige Weg zu diesen Abzügen; der Antrag ist ebenfalls bis 31. März des Folgejahres einzureichen.</p>"""),
("Korrektur vs. Zusatzabzüge: zwei verschiedene Anträge",
 """<p>Nicht jede Korrektur braucht eine NOV: Wurde der <strong>Bruttolohn falsch ermittelt, das satzbestimmende Einkommen fehlerhaft berechnet oder ein falscher Tarif angewendet</strong>, genügt der Antrag auf Neuberechnung der Quellensteuer (Art. 137 DBG, Art. 49 Abs. 2–2ter StHG) – ebenfalls bis 31. März des Folgejahres. Die NOV dagegen öffnet die ganze Abzugslogik der ordentlichen Veranlagung inkl. persönlicher Verhältnisse (Zivilstand, Kinder, Vermögen).</p>"""),
("Wie der Antrag funktioniert",
 """<p>Das Formular liegt beim kantonalen Steueramt auf (in vielen Kantonen jedes Jahr vom 1. Januar bis 31. März online verfügbar). Eheleute und eingetragene Partnerschaften müssen den Antrag <strong>gemeinsam unterzeichnen</strong>; er muss die Steuerperiode bezeichnen. Beizulegen sind die üblichen Belege: Lohnausweise, Nachweise über Berufskosten, Krankheitskosten, 3a-Beiträge, Betreuungs- und Unterhaltskosten. Die Veranlagung erfolgt nach ordentlichem Recht; die einbehaltene Quellensteuer wird angerechnet. Die ESTV stellt die Veranlagung in der Regel bis Ende des Antragsjahres zu – danach laufen die ordentlichen Rechtsmittel (Einsprache innert 30 Tagen).</p>"""),
("Rechenbeispiel: Wann sich der Antrag lohnt",
 """<p>Richtwert: Der Quellensteuertarif enthält für Berufskosten eine Pauschale. Liegen die effektiven Kosten (Fahrtkosten, Verpflegung, Weiterbildung, Arbeitszimmer) deutlich darüber, steigt der Abzug um die Differenz. Beispielhaft: Wer CHF 12'000.- echte Berufskosten nachweisen kann statt der tariflichen Pauschale von wenigen Tausend Franken, senkt sein steuerbares Einkommen entsprechend – bei einem Grenztarif von 15–25 % bedeutet das eine Rückerstattung im Bereich von CHF 1'500.–3'000.- pro Jahr. Die genaue Rechnung hängt von Kanton, Gemeinde, Zivilstand und Kindern ab; Steuerämter und Steuersoftware der Kantone erlauben eine Überschlagsrechnung vor dem Antrag.</p>"""),
("Kurz zusammengefasst",
 """<ul><li>Zusatzabzüge (Berufskosten effektiv, Krankheit, Weiterbildung, Drittbetreuung, 3a, Unterhalt) gibt es nur mit nachträglicher ordentlicher Veranlagung (NOV).</li>
<li>Frist: 31. März des Folgejahres – für Periode 2026 bis 31.3.2027. Ohne Antrag verfallen die Abzüge.</li>
<li>Obligatorisch ab Bruttoeinkommen über CHF 120'000.- (Ansässige); freiwillig für alle, auch Grenzgänger.</li>
<li>Falscher Tarif/fehlerhafter Lohn → Neuberechnungsantrag (Art. 137 DBG / Art. 49 StHG), gleiche Frist.</li>
<li>Allgemeine Information, keine Einzelfallberatung – das kantonale Steueramt erteilt Auskunft.</li></ul>"""),
]

# ============ A5: Kapitalsteuer ============
SLUG5 = "kapitalsteuer-ag-gmbh"
REL5 = ["verrechnungssteuer-schweiz-35-prozent.html", "dividenden-ahv-pflicht-bge-9c-532-2025.html", "transparenzregister-tjpg-meldepflicht.html"]
de5_title = "Kapitalsteuer für AG und GmbH: was Firmen auch in Verlustjahren kostet"
de5_meta = "Nicht alle Kantone besteuern Kapital, aber wer es tut, kassiert jährlich – ganz ohne Gewinn. So funktioniert die Kapitalsteuer: Bemessung auf dem Eigenkapital, Anrechnung der Gewinnsteuer, Mindeststeuer, kantonale Sätze zwischen 0 und 7 Promille – und warum Kapitalherabsetzung und Liquidation durchgerechnet gehören."
de5_sections = [
("Was die Kapitalsteuer besteuert",
 """<p>Die Kapitalsteuer ist eine <strong>kantonale Steuer auf dem steuerbaren Eigenkapital</strong> einer Kapitalgesellschaft: Aktiengesellschaften, GmbH und Genossenschaften werden jährlich auf ihrem bilanziellen Eigenkapital (Grundkapital plus gesetzliche und freiwillige Reserven, je nach kantonalem Recht) besteuert – <strong>unabhängig davon, ob die Firma Gewinn macht</strong>. Ein Verlustjahr befreit nicht; die Steuer fällt trotzdem an.</p>
<p>Auf Bundesebene existiert keine Kapitalsteuer – die direkte Bundessteuer kennt nur die Gewinnsteuer (8,5 %). Reine Gewinnsteuer-Kantone gibt es kaum: Die Mehrheit der Kantone erhebt eine Kapitalsteuer, allerdings sehr unterschiedlich ausgestaltet. Der Kanton Uri etwa verzichtet auf kantonaler Ebene ganz darauf (ESTV-Publikation «Steuersatz und Steuerfuss», Stand 1.1.2026), während die Urner Gemeinden proportionale Sätze zwischen 0,01 und 4 Promille erheben.</p>"""),
("Sätze und Steuerfüsse: ein Rundgang",
 """<p>Die gesetzlichen Ansätze bewegen sich im Promillebereich. Beispiel Aargau: <strong>0,75 Promille des steuerbaren Eigenkapitals</strong> (§ 86 Abs. 1 StG AG); bei einem Steuerfuss von 115 % (2026) ergibt das für eine Firma mit CHF 2 Mio. Eigenkapital rund <strong>CHF 1'725.- Kapitalsteuer</strong> pro Jahr. Der Kanton Luzern kennt für den Anteil des Eigenkapitals, der auf Beteiligungen, Patente und vergleichbare Rechte sowie Konzernforderungen entfällt, eine feste Kapitalsteuer von nur 0,01 Promille – die typische Holding-Regelung (ESTV a.a.O.).</p>
<p>Nach oben begrenzt ist die Last nicht überall: Der Kanton Waadt schreibt gesetzlich vor, dass Kantons- und Gemeindesteuern zusammen <strong>7 Promille des steuerbaren Kapitals</strong> (und 30 % des steuerbaren Reingewinns) nicht überschreiten dürfen. Die Mehrheit der Kantone sieht für juristische Personen dagegen <strong>keine Belastungsobergrenze</strong> vor.</p>"""),
("Anrechnung: Die Doppelbelastung hat einen Dämpfer",
 """<p>Viele Kantone mildern die Kombination aus Gewinn- und Kapitalsteuer, indem die <strong>Gewinnsteuer an die Kapitalsteuer angerechnet</strong> wird – so ausdrücklich in Aargau (§ 86 Abs. 4 StG AG). Praktisch heisst das: In profitablen Jahren ist die Kapitalsteuer oft «aufgegangen»; effektiv zusätzlich zahlt die Firma sie vor allem dann, wenn die Kapitalsteuer die Gewinnsteuer übersteigt – also in schwachen und Verlustjahren.</p>
<p>Mindeststeuern bleiben: Kapitalgesellschaften und Genossenschaften entrichten in Aargau eine Mindeststeuer von <strong>CHF 500.-</strong> (einfache 100%ige Kantonssteuer, § 88 StG AG) – auch bei null Gewinn und null Kapitalertrag. Vereine und Stiftungen sind erst ab CHF 50'000.- Eigenkapital kapitalsteuerpflichtig (§ 86 Abs. 3 StG AG).</p>"""),
("Wer spürt die Last wirklich?",
 """<p>Die Kapitalsteuer ist eine <strong>Vermögenssteuer auf Firmengeld</strong>. Drei Konstellationen tun weh:</p>
<ul><li><strong>Cashreiche Ertragszwerge:</strong> Gesparte Reserven erhöhen das Eigenkapital und damit die Steuer, ohne dass Gewinn geflossen ist – die Steuer wird zur reinen Liquiditätslast.</li>
<li><strong>Verlustjahre:</strong> Gewinnsteuer null, Kapitalsteuer voll – die Anrechnung greift ins Leere.</li>
<li><strong>Reorganisationsfälle:</strong> Vor Kapitalherabsetzungen, Umstrukturierungen und Liquidationen gehört die Kapitalsteuer in die Durchrechnung: Bis zur Löschung bleibt die Steuer jährlich geschuldet; eine gestaffelte Kapitalherabsetzung kann sie senken, löst aber je nach Konstruktion Emissionsabgabe-Rückerstattungsfragen oder Verrechnungssteuer aus.</li></ul>"""),
("Kantonaler Standortfaktor – und politischer Dauerbrenner",
 """<p>Die Kapitalsteuer ist ein echtes Standortkriterium: Zwischen «keine kantonale Kapitalsteuer» (Uri) und mehreren Promille inklusive Gemeindeanteil liegen Welten – in der Summe aus Gewinn- und Kapitalsteuer belastet sie kapitalintensive Modelle über Jahre. Einzelne Kantone haben Sätze gesenkt oder Sonderregelungen für Holding-Substanz geschaffen; die politische Debatte um eine gänzliche Abschaffung kehrt auf kantonaler Ebene regelmässig wieder.</p>
<p>Für die Praxis gilt: Wer AG oder GmbH gründet, hält, restrukturiert oder liquidiert, prüft die Kapitalsteuer des Domizilkantons <strong>pro Jahr neu</strong> – Ansätze, Steuerfüsse und Anrechnungsmodelle ändern sich häufiger als die Gewinnsteuer.</p>"""),
("Checkliste für AG/GmbH-Gesellschafter",
 """<ol><li><strong>Standesprotokoll führen:</strong> steuerbares Eigenkapital pro Jahr inkl. Reserveveränderungen.</li>
<li><strong>Kantonsvergleich:</strong> Satz, Steuerfuss, Anrechnungsmodell, Mindeststeuer des Domizilkantons kennen (ESTV «Steuersatz und Steuerfuss» als Ausgangspunkt).</li>
<li><strong>Verlustjahre einplanen:</strong> Kapitalsteuer + Mindeststeuer fliessen unabhängig vom Ergebnis.</li>
<li><strong>Reservepolitik:</strong> Thesaurationsentscheide erhöhen die Kapitalsteuerbasis – Dividende vs. Reserve nach Gesamteffekt rechnen (inkl. Verrechnungssteuer 35 %).</li>
<li><strong>Restrukturierung durchrechnen:</strong> Kapitalherabsetzung, Teilliquidation, Liquidation – Kapitalsteuerersparnis vs. Emissions-/Verrechnungssteuerfolgen.</li>
<li><strong>Jährlich revalidieren:</strong> Steuerfüsse werden oft geändert.</li></ol>"""),
("Kurz zusammengefasst",
 """<ul><li>Kapitalsteuer = kantonale Jahressteuer auf dem Eigenkapital von AG/GmbH/Genossenschaften – auch in Verlustjahren.</li>
<li>Bundessteuer kennt keine Kapitalsteuer; kantonale Sätze liegen im Promillebereich (Beispiel Aargau 0,75 ‰; Uri kantonale: keine; VD Obergrenze 7 ‰).</li>
<li>Gewinnsteuer wird meist angerechnet – effektiv zahlt man Kapitalsteuer vor allem bei schwachen Ergebnissen; Mindeststeuern bleiben (AG: CHF 500.-).</li>
<li>Bei Kapitalherabsetzung und Liquidation gehört sie in die Gesamtdurchrechnung.</li>
<li>Allgemeine Information, keine Einzelfallberatung – Treuhänder oder Steuerexperte beiziehen.</li></ul>"""),
]

for slug, rel, title, meta, sections in [
    (SLUG1, REL1, de1_title, de1_meta, de1_sections),
    (SLUG2, REL2, de2_title, de2_meta, de2_sections),
    (SLUG3, REL3, de3_title, de3_meta, de3_sections),
    (SLUG4, REL4, de4_title, de4_meta, de4_sections),
    (SLUG5, REL5, de5_title, de5_meta, de5_sections),
]:
    build("de", slug, title, meta, sections, related=rel)
    print("built", slug)
print("done")
