#!/usr/bin/env python3
"""Build the 5 pending DE Ratgeber articles (todo 2026-09-17) via article_template.
All figures pre-verified with scripts/claim_check.py (rounds 2-4, 2026-09-17):
- VSt 35 % Art. 13 VStG (0.92); refund route Art. 30 (0.98); 3-year bar Art. 32 Abs. 1 (0.95)
- private debt interest cap = income + 50k, Art. 33 Abs. 1 Bst. a DBG (0.98)
- MWST 100k Art. 10 (0.84/0.87); 30-day registration Art. 66 Abs. 1 (0.99); rates 8.1/2.6 (0.93/0.98)
- Grenzgänger 4.5 % Art. 15a DBA CH-DE (0.99); Gre-1/Gre-3/60 days zh.ch (0.98/0.89); DE Frist 31.07.2026 (0.98)
- AHV self-employed 8.1+1.4+0.5=10.0 % (0.86); scale < 60'500 (0.99); minimum 530 (0.97)
WRONG facts deliberately NOT used: Formular 110 as refund form, Formular 25 as MWST form,
Formulare 130/140/150 bei AHV, 2.5 % reduced VAT, 5 % mortgage deduction, Art. 86 VStG.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import article_template as at


def P(s):
    return f'<p>{s}</p>'

def UL(items):
    return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def OL(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


articles = []

# ---------------------------------------------------------------- A1: VSt
articles.append((
 "verrechnungssteuer-schweiz-35-prozent",
 "Verrechnungssteuer 35 %: Dividenden und Zinsen zurückholen",
 "Verrechnungssteuer Schweiz: 35 % auf Dividenden und Zinsen (Art. 13 VStG). So holst du sie über die Steuererklärung zurück – Frist 3 Jahre (Art. 32 VStG), ohne Formular-110-Chaos.",
 [
  ("Was die Verrechnungssteuer ist",
   P("Die Verrechnungssteuer ist eine Bundessteuer auf Kapitalerträgen: Auf Dividenden, Zinsen und Gewinnen aus Geldspielen werden <strong>35 Prozent</strong> abgezogen (Art. 13 Abs. 1 Bst. a VStG). Leibrenten und Pensionen sind mit 15 Prozent betroffen, sonstige Versicherungsleistungen mit 8 Prozent.")
   + P("Den Abzug nimmt nicht der Staat vor, sondern die zahlende Stelle: Deine Bank oder die Aktiengesellschaft behält die Steuer beim Fälligkeitsdatum ein und liefert sie der Eidgenössischen Steuerverwaltung (ESTV) ab. Sie soll Steuerhinterziehung auf Kapitaleinkommen erschweren – deshalb liegt der Satz absichtlich über der normalen Steuerbelastung.")),
  ("Die Steuer ist kein Verlust – sie ist vorausbezahlt",
   P("Für in der Schweiz unbeschränkt steuerpflichtige natürliche Personen ist die Verrechnungssteuer keine Endsteuer, sondern eine Sicherungssteuer: Du kannst sie zurückfordern, sofern du die Erträge korrekt deklarierst. Wer sie nicht geltend macht, verschenkt Geld – bei einem Depot mit 2'000 Franken Dividenden und Zinsen sind das allein 700 Franken pro Jahr.")),
  ("Der einfache Weg: die Steuererklärung",
   P("Hast du eine Steuererklärung ausgefüllt, gilt deren Einreichung in der Praxis als Rückerstattungsgesuch: Zuständig ist die Steuerbehörde des Kantons, in dem du am Ende des Fälligkeitsjahres Wohnsitz hattest (Art. 30 VStG). Der Wertschriftenausweis der Steuererklärung wirkt dabei als Gesuch – die Kantone erstatten die Steuer in der Regel bis zur Höhe deiner kantonalen und kommunalen Steuer (Art. 31 VStG).")
   + P("Wichtig für Depot-Inhaber: Trage alle Dividenden und Zinsen vollständig in den Wertschriftenausweis ein – auch kleine Beträge. Fehlt eine Position, fehlt bei der Erstattung genau dieser Betrag.")),
  ("Ohne Steuererklärung: Formular 25",
   P("Wer keine Steuererklärung einreicht (zum Beispiel weil der Wohnsitzkanton keine verlangt), beantragt die Rückerstattung mit <strong>Formular 25</strong> über das ESTV-Portal. Achtung, häufige Verwechslung: <strong>Formular 110 ist nichts für dich</strong> – damit deklariert die zahlende Gesellschaft ihre Abrechnung (innert 30 Tagen nach der Generalversammlung). Als Privatperson holst du damit nada zurück.")),
  ("Frist: drei Jahre nach dem Fälligkeitsjahr",
   P("Der Anspruch erlischt, wenn du ihn nicht <strong>innert drei Jahren nach Ablauf des Kalenderjahrs</strong> geltend machst, in dem die Leistung fällig wurde (Art. 32 Abs. 1 VStG). Beispiel: Dividende am 15. Mai 2023 → Fristablauf am 31. Dezember 2026. Verpasste Fristen sind endgültig verloren, auch bei guten Gründen.")),
  ("Häufige Irrtümer auf einen Blick",
   UL([
    "<strong>«Rückerstattung innert 30 Tagen»</strong> – falsch. Die 30-Tage-Frist betrifft die Deklaration der zahlenden Gesellschaft (Formular 110), nicht dein Gesuch.",
    "<strong>«Die Steuer ist weg, wenn ich nichts tue»</strong> – sie ist weg, wenn du innert drei Jahren nichts tust. Sonst bekommst du sie zurück.",
    "<strong>«Ausländische Quellensteuer zahlt die Schweiz zurück»</strong> – nein, dafür gilt das jeweilige Doppelbesteuerungsabkommen; die CH-Verrechnungssteuer ist unabhängig davon."])),
  ("Kurz gesagt",
   OL([
    "35 % auf Dividenden/Zinsen, 15 % auf Leibrenten/Pensionen, 8 % auf sonstige Versicherungsleistungen (Art. 13 VStG).",
    "Mit der Steuererklärung gilt die vollständige Deklaration als Rückerstattungsgesuch beim Wohnsitzkanton (Art. 30 VStG).",
    "Ohne Steuererklärung: Formular 25 via ESTV-Portal.",
    "Frist: 3 Jahre nach Ablauf des Fälligkeitsjahres (Art. 32 Abs. 1 VStG) – nicht 30 Tage."])
   + P("Unsicher, ob dein Wertschriftenausweis vollständig ist? Über die <a href=\"kontakt.html\">Kontaktseite</a> vermitteln wir dir einen geprüften Partner in deinem Kanton – das erste Offert zeigt transparent, was die Prüfung kostet.")),
 ]))

# ---------------------------------------------------------------- A2: Grenzgänger
articles.append((
 "grenzgaenger-de-fr-it-steuern",
 "Grenzgänger DE/FR/IT: Quellensteuer 4,5 % und Formulare richtig einreichen",
 "Grenzgänger Schweiz-Deutschland: 4,5 % Quellensteuer (Art. 15a DBA CH-DE), Formular Gre-1, 60 Nichtrückkehrtage, deutsche Frist 31. Juli. Für FR/IT gelten andere Regeln – die Übersicht 2026.",
 [
  ("Wer steuerlich als Grenzgänger gilt",
   P("Grenzgänger bist du nach Steuerrecht nur, wenn alle Bedingungen erfüllt sind: Wohnsitz im Ausland (DE, FR oder IT), Arbeitgeber und Arbeitsort in der Schweiz, <strong>tägliche Rückkehr</strong> an den Wohnsitz – und diese Rückkehr muss zumutbar sein. Zumutbar heisst in der Praxis der Kantone: höchstens 100 Kilometer Fahrstrecke mit dem Auto oder höchstens 1,5 Stunden mit dem öffentlichen Verkehr.")
   + P("Achtung: Die Grenzgängerbewilligung (Ausweis G) ist etwas anderes – sie begründet keinen steuerlichen Grenzgängerstatus. Wer nicht täglich zurückkehrt, ist internationaler Wochenaufenthalter und wird nach den ordentlichen Schweizer Tarifen quellenbesteuert.")),
  ("Deutschland: 4,5 % Quellensteuer – aber nur mit Gre-1",
   P("Echte deutsche Grenzgänger besteuert die Schweiz pauschal mit <strong>4,5 Prozent des Bruttolohns</strong> (Art. 15a DBA CH-DE). Das gilt aber nicht automatisch: Du musst dem Arbeitgeber die <strong>Ansässigkeitsbescheinigung Formular Gre-1</strong> abgeben, die dein deutsches Finanzamt ausstellt. Ohne Gre-1 rechnet der Arbeitgeber nach dem ordentlichen Tarif ab – das ist oft deutlich mehr.")
   + P("Gre-1 gilt jeweils für ein Kalenderjahr und muss dem Arbeitgeber jedes Jahr neu abgegeben werden; nach dem ersten Jahr stellt das Finanzamt es in der Regel automatisch aus. Pro Arbeitgeber brauchst du ein eigenes Formular.")),
  ("Die 60-Nichtrückkehrtage-Grenze",
   P("Kehrst du aus beruflichen Gründen (Geschäftsreisen, Pikettdienst, Weiterbildung) an <strong>mehr als 60 Tagen</strong> im Kalenderjahr nicht nach Hause zurück, verlierst du den Grenzgängertarif. Dein Schweizer Einkommen wird nach den ordentlichen Tarifen neu berechnet und nachveranlagt. Die beruflich bedingten Nichtrückkehrtage muss der Arbeitgeber mit <strong>Formular Gre-3</strong> bescheinigen – im Kanton Zürich etwa schriftlich, pro Arbeitgeber separat und bis spätestens <strong>31. März des Folgejahres</strong> beim kantonalen Steueramt (die Frist ist kantonal unterschiedlich). Privat begründete Übernachtungen zählen nicht.")),
  ("Deutschland: Steuererklärung bis 31. Juli",
   P("Auch wenn die Schweiz 4,5 % erhoben hat: In Deutschland bist du mit deinem Welteinkommen steuerpflichtig und musst die Grenzgängereinkünfte in der Einkommensteuererklärung deklarieren. Die allgemeine Abgabefrist für die deutsche Einkommensteuererklärung 2025 endet am <strong>31. Juli 2026</strong>; mit Steuervertretung (Lohnsteuerhilfeverein, Steuerberaterin) später. Die Schweizer Quellensteuer wird in Deutschland angerechnet, damit keine Doppelbesteuerung hängen bleibt.")),
  ("Frankreich und Italien: völlig andere Regeln",
   P("<strong>Frankreich:</strong> Das Grenzgängerabkommen von 1983 gilt nur für Arbeitsorte in den Kantonen BE, BL, BS, JU, NE, SO, VD und VS. Ausserhalb dieser Zone – zum Beispiel Genf – greift das reguläre DBA mit ordentlichem Schweizer Quellensteuertarif und Besteuerung in Frankreich mit Anrechnung; die Details hängen vom Tätigkeitskanton ab.")
   + P("<strong>Italien:</strong> Seit dem revidierten Abkommen (in Kraft 17. Juli 2023, anwendbar ab 2024) dürfen «neue» Grenzgänger – Arbeitsbeginn nach dem 17. Juli 2023 – in der Schweiz mit bis zu 80 Prozent des ordentlichen Quellensteuerbetrags besteuert werden; Italien rechnet diese Steuer an. Für vor dem Stichtag angestellte Grenzgänger gilt eine Übergangsregelung bis Ende 2033. Homeoffice ist bis zu 25 Prozent der Arbeitszeit möglich, ohne den Status zu gefährden.")),
  ("Die häufigsten Fehler",
   UL([
    "<strong>G-Bewilligung gleich Steuerstatus?</strong> Nein – entscheidend sind tägliche Rückkehr und Zumutbarkeit.",
    "<strong>Gre-1 vergessen</strong> → ordentlicher Tarif statt 4,5 %, mühsame Korrektur.",
    "<strong>Nichtrückkehrtage falsch dokumentiert</strong> → Gre-3 nicht fristgerecht eingereicht, Nachveranlagung nach ordentlichem Tarif.",
    "<strong>«Formulare 130/140/150 bei der AHV»?</strong> Gibt es nicht – die AHV ist für die Quellensteuer nie zuständig; die Bescheinigungen laufen über Arbeitgeber und kantonale Steuerämter."])),
  ("Kurz gesagt",
   OL([
    "4,5 % CH-Quellensteuer für echte deutsche Grenzgänger – nur mit Formular Gre-1 beim Arbeitgeber.",
    "Über 60 berufliche Nichtrückkehrtage (Gre-3) → ordentlicher Tarif, Nachveranlagung.",
    "Deutsche Seite: Anlage N-GRE, Abgabefrist 2025er-Erklärung am 31. Juli 2026.",
    "FR: Abkommen 1983 nur in 8 Grenzkantonen; IT: neues Regime ab 2024 (bis 80 % CH-Quellensteuer, Anrechnung, Übergang bis 2033)."])
   + P("Du hattest ein Homeoffice-Jahr mit vielen Reisetagen? Genau da wird es kompliziert. Über die <a href=\"kontakt.html\">Kontaktseite</a> vermitteln wir dir einen geprüften Partner – mit transparentem Offert vor jedem Mandat.")),
 ]))

# ---------------------------------------------------------------- A3: Hypothek
articles.append((
 "hypothek-steuerabzug-schweiz",
 "Hypothek und Steuern: Zinsen, Abzug und Grenzen richtig verstehen",
 "Hypothekarzinsen abziehen 2026: private Schuldzinsen bis zum Vermögensertrag plus CHF 50'000 (Art. 33 Abs. 1 Bst. a DBG). So deklarierst du sie richtig – und was du NICHT abziehen kannst.",
 [
  ("Das Prinzip: Eigenmietwert gegen Abzüge",
   P("Wer im eigenen Eigentum wohnt, versteuert den <strong>Eigenmietwert</strong> – einen fiktiven Mietzins, der zum Einkommen addiert wird. Dafür darfst du die Kosten der Liegenschaft abziehen: vor allem die Hypothekarzinsen, den Unterhalt und die Beiträge an Energiespar- und Schutzmassnahmen. Das System soll vermietetes und selbst bewohntes Eigentum steuerlich ähnlich stellen – es ist kein Geschenk.")),
  ("Hypothekarzinsen: Abzug, aber mit Deckel",
   P("Hypothekarzinsen für selbst genutztes Wohneigentum sind <strong>private Schuldzinsen</strong>. Bei der direkten Bundessteuer sind private Schuldzinsen abzugsfähig – aber nicht grenzenlos: nur im Umfang der <strong>steuerbaren Vermögenserträge plus weitere CHF 50'000</strong> (Art. 33 Abs. 1 Bst. a DBG). Hast du wenig Erträge aus Vermögen (Zinsen, Dividenden, Mietzinsen), greift der Deckel: Nicht alles, was die Bank dir im Jahr verrechnet, kommt in die Steuerrechnung. Die Kantone handhaben private Schuldzinsen teils anders – für die eigene Steuererklärung zählt das jeweilige kantonale Recht.")),
  ("Richtig deklarieren: Schuldenverzeichnis Formular 14",
   P("Alle Hypotheken und Darlehen trägst du ins <strong>Schuldenverzeichnis (Formular 14)</strong> ein: Gläubiger, Restschuld per Jahresende, Zinsbetrag. Beleg ist der <strong>Zinsausweis deiner Bank</strong> – ohne ihn erkennt die Steuerbehörde den Abzug nicht an. Die Schuld selbst mindert zudem dein steuerbares Vermögen; die Vermögenssteuer sinkt.")),
  ("Was du NICHT abziehen kannst",
   UL([
    "<strong>Baukreditzinsen während der Bauphase:</strong> Sie sind Anlagekosten des Gebäudes, kein Einkommensabzug – später über die Abschreibung der Baukosten holbar.",
    "<strong>Luxusaufwand:</strong> Einbausachen mit luxuriösem Charakter (Whirlpool, Wellness-Sondereinbauten) akzeptieren Steuerbehörden regelmässig nicht als Unterhalt.",
    "<strong>Erfundene Regeln:</strong> Ein «5 %-Zinsabzug auf das Darlehen» existiert ebenso wenig wie Formulare «bei der AHV» – die AHV ist für Hypotheken nie zuständig."])),
  ("Strategie: amortisieren oder abzahlen?",
   P("Höhere Hypothekarzinsen machen das Amortisieren attraktiv: Jede getilgte Stufe spart künftige Zinsen – senkt aber auch deinen Abzug und erhöht netto dein steuerbares Einkommen. Wer nahe am Deckel der privaten Schuldzinsen liegt, fährt mit der Amortisation oft besser als mit dem (blockierten) Zinsabzug. Der Eigenmietwert-Abzugsvergleich ist Kantons- und Einzelfallsache – hier rechnet sich eine individuelle Beratung eher als irgendwo sonst.")),
  ("Kurz gesagt",
   OL([
    "Hypothekarzinsen sind abzugsfähig – private Schuldzinsen aber gedeckelt auf Vermögensertrag + CHF 50'000 auf Bundesebene (Art. 33 Abs. 1 Bst. a DBG).",
    "Deklaration im Schuldenverzeichnis Formular 14, Beleg = Zinsausweis der Bank.",
    "Bauphasen-Zinsen sind Anlagekosten, keine Einkommensabzüge.",
    "Kantonale Unterschiede prüfen – besonders bei Amortisation und Eigenmietwert."])
   + P("Unsicher, ob deine Abzüge an den Deckel stossen? Über die <a href=\"kontakt.html\">Kontaktseite</a> finden wir einen geprüften Partner in deiner Region – Offert vor jedem Mandat.")),
 ]))

# ---------------------------------------------------------------- A4: MWST
articles.append((
 "mwst-100k-pflicht-schweiz",
 "MWST ab CHF 100'000: Wann du mehrwertsteuerpflichtig wirst",
 "Mehrwertsteuer-Pflicht Schweiz: ab 100'000 CHF Weltumsatz (Art. 10 MwStG), Anmeldung innert 30 Tagen via ESTV-Onlineformular, Sätze 8,1 % / 2,6 %. Schwellen, Fristen und Ausnahmen 2026.",
 [
  ("Die Schwelle: 100'000 Franken – weltweit",
   P("Mehrwertsteuerpflichtig wirst du, wenn dein Unternehmen jährlich <strong>CHF 100'000 oder mehr</strong> mit nicht von der Steuer ausgenommenen Leistungen erzielst (Art. 10 Abs. 2 MwStG). Wichtig: Gezählt wird der Umsatz <strong>im In- und Ausland</strong>, nicht nur der Schweizer Umsatz. Ausgenommene Leistungen (zum Beispiel Vermietung von Wohnraum, Versicherungs- und Bankengeschäfte, bestimmte Bildungsleistungen) zählen nicht mit.")
   + P("Wer jährlich unter der Grenze bleibt, ist von der Steuerpflicht befreit – Ausnahme für Vereine: Nicht gewinnstrebige, ehrenamtlich geführte Sport- und Kulturvereine sowie gemeinnützige Organisationen haben eine erhöhte Grenze von <strong>CHF 250'000</strong> (Art. 10 Abs. 2 Bst. c MwStG). Massgebend ist jeweils ein Jahr; wer absehen kann, dass er die Grenze in den nächsten zwölf Monaten überschreitet, wird bereits vorher steuerpflichtig.")),
  ("Anmeldung: unaufgefordert, innert 30 Tagen",
   P("Sobald du die Grenze überschreitest (oder absehbar überschreitest), musst du dich <strong>unaufgefordert innert 30 Tagen</strong> nach Beginn der Steuerpflicht schriftlich bei der ESTV anmelden (Art. 66 Abs. 1 MwStG). Niemand schreibt dich an. Die Anmeldung läuft über den <strong>Online-Fragebogen der ESTV</strong>; du erhältst eine nicht übertragbare MWST-Nummer. Verwechslungsgefahr: Das «Formular 25» betrifft die Rückerstattung der Verrechnungssteuer – für die MWST ist das Onlineformular der ESTV zuständig.")
   + P("Umgekehrt: Wer unter der Grenze bleibt, kann freiwillig auf die Befreiung verzichten und sich anmelden (Art. 11/14 MwStG) – das lohnt sich wegen des Vorsteuerabzugs vor allem bei hohen Investitionen. Achtung: Wer MwSt auf der Rechnung ausweist, ohne berechtigt zu sein, schuldet den Betrag trotzdem (Art. 27 MwStG).")),
  ("Die Sätze 2026",
   P("Es gelten: <strong>Normalsatz 8,1 Prozent</strong>, <strong>reduzierter Satz 2,6 Prozent</strong> (Art. 25 MwStG). Der reduzierte Satz gilt unter anderem für Lebensmittel nach dem Lebensmittelgesetz (ohne Alkoholgetränke), Wasser in Leitungen, Medikamente, Bücher und Presseerzeugnisse. Achtung, verbreiteter Irrtum: <strong>Für gastgewerbliche Leistungen gilt der Normalsatz</strong> – Restaurantbetrieb und Verzehr vor Ort sind nicht reduziert, auch wenn die Lebensmittel an sich es wären. Wer «Gastronomie zu 2,6 %» rechnet, hat falsch gelernt.")),
  ("Abrechnung: quartalsweise, halbjährlich oder nach Saldosteuersatz",
   P("Regel ist die <strong>vierteljährliche Abrechnung</strong> über das MWST-Portal der ESTV. Kleine Betriebe (wenig Steuerbetrag pro Jahr) dürfen halbjährlich oder jährlich abrechnen; viele KMU nutzen die <strong>Saldosteuersätze</strong> – pauschale Branchensätze, die den Buchhaltungsaufwand senken, weil die Vorsteuer nicht einzeln belegt werden muss.")),
  ("Nebenjob, Verein, Plattform: wann du trotzdem «Unternehmen» bist",
   P("Unternehmen ist, wer eine auf nachhaltige Einnahmeerzielung gerichtete Tätigkeit selbstständig ausübt (Art. 10 Abs. 1bis MwStG) – auch neben dem Hauptjob und auch mit 20-Prozent-Pensum auf einer Plattform. Laufende Consulting-Aufträge, Shop-Umsätze oder Vermietung mit Infrastruktur können Steuerpflicht auslösen, bevor du es merkst. Geringfügige Entgelte und echte Gelegenheitsgeschäfte tun das nicht.")),
  ("Kurz gesagt",
   OL([
    "Pflicht ab CHF 100'000 Weltumsatz aus nicht ausgenommenen Leistungen (Art. 10 Abs. 2 MwStG); Sport-/Kulturvereine und gemeinnützige Institutionen: CHF 250'000.",
    "Anmeldung: innert 30 Tagen, unaufgefordert, Onlinefragebogen ESTV – nicht Formular 25.",
    "Sätze 2026: 8,1 % Normal, 2,6 % reduziert; Gastronomie = Normalsatz.",
    "Freiwillige Anmeldung bringt Vorsteuerabzug; ausgewiesene MwSt ohne Berechtigung wird geschuldet (Art. 27)."])
   + P("Du hast die 100'000 gerade (bald) überschritten und willst sauber starten? Über die <a href=\"kontakt.html\">Kontaktseite</a> vermitteln wir dir einen geprüften Partner für die MWST-Erstanmeldung – mit Offert vor dem Mandat.")),
 ]))

# ---------------------------------------------------------------- A5: AHV
articles.append((
 "ahv-mindestbeitrag-selbststaendige",
 "AHV 2026: Mindestbeitrag CHF 530 und die Beitragsskala für Selbstständige",
 "AHV/IV/EO für Selbstständige 2026: 10 % total (AHV 8,1, IV 1,4, EO 0,5), sinkende Skala unter CHF 60'500, Mindestbeitrag CHF 530. Dazu Renten min/max und die 13. Rente ab Dezember 2026.",
 [
  ("Was Selbstständige zahlen",
   P("Selbständigerwerbende zahlen die Beiträge an AHV, IV und EO <strong>komplett selbst</strong> – es gibt keinen Arbeitgeber, der die Hälfte übernimmt. Der Satz 2026: AHV 8,1 % + IV 1,4 % + EO 0,5 % = <strong>total 10,0 Prozent</strong> des Nettoeinkommens aus selbstständiger Erwerbstätigkeit. Zur Einordnung: Angestellte und Arbeitgeber teilen sich zusammen 10,6 % zu je 5,3 %.")),
  ("Die sinkende Skala: tieferes Einkommen, tieferer Satz",
   P("Für Jahreseinkommen <strong>unter CHF 60'500</strong> gilt ein tieferer Beitragssatz – die «sinkende Skala» (Merkblatt AHV 2.02). Sie startet bei <strong>5,371 Prozent</strong> für Einkommen ab CHF 10'100 und steigt in Stufen auf volle 10,0 Prozent ab CHF 60'500. Beispiel: Bei CHF 40'500 Einkommen zahlst du 6,728 % ≈ CHF 2'725 statt der vollen 4'050 Franken. Massgebend ist das Nettoeinkommen, das deine Ausgleichskasse per Veranlagungsverfügung feststellt.")),
  ("Mindestbeitrag CHF 530",
   P("Erzielst du weniger als CHF 10'100 Jahreseinkommen, zahlst du den <strong>Mindestbeitrag von CHF 530 pro Jahr</strong> (er entspricht einem Jahreslohn von CHF 5'000). Auch Nichterwerbstätige zahlen mindestens 530 Franken, höchstens 26'500. Wer auf einem Lohn bereits den Mindestbeitrag geleistet hat, kann verlangen, dass die Selbstständigungs-Beiträge nur zum tiefsten Skalasatz (5,371 %) erhoben werden.")
   + P("Nebenberuflich: Übst du die selbstständige Tätigkeit nur nebenberuflich aus und beträgt das Jahreseinkommen daraus maximal CHF 2'500, werden Beiträge nur auf deinen Wunsch erhoben (Merkblatt 2.02).").replace("nur auf deinen Wunsch erhoben","nur auf dein ausdrückliches Verlangen erhoben")),
  ("AHV-Renten 2026",
   P("Die Vollrente (bei vollständiger Beitragsdauer) liegt 2026 zwischen <strong>CHF 1'260 und CHF 2'520 pro Monat</strong> – das sind <strong>15'120 bis 30'240 Franken pro Jahr</strong> (BSV). Ehepaare erhalten zwei Individualrenten, zusammen begrenzt auf 150 Prozent der Maximalrente: höchstens <strong>CHF 3'780 pro Monat</strong> (45'360 pro Jahr). Die Höhe hängt von Beitragsdauer und durchschnittlichem Erwerbseinkommen ab.")),
  ("Die 13. AHV-Rente kommt – erstmals Dezember 2026",
   P("Das Volk hat die 13. Altersrente angenommen. Ausbezahlt wird sie <strong>erstmals zusammen mit der Dezemberrente 2026</strong> als Zuschlag: ein Zwölftel (8,333 Prozent) aller von Januar bis Dezember 2026 bezogenen Monatsrenten. Wer im Dezember 2026 eine Altersrente bezieht, erhält den Zuschlag automatisch von der AHV-Ausgleichskasse – eine Anmeldung braucht es nicht.")),
  ("Häufige Fehler",
   UL([
    "<strong>Beitragsbasis verwechseln:</strong> Massgebend ist der Reingewinn der selbstständigen Tätigkeit laut Veranlagung, nicht ein «Salär».",
    "<strong>Verzugszins 5 %:</strong> zahlst du die Jahresrechnung mehr als 30 Tage nach Rechnungsdatum, wird es teuer.",
    "<strong>Mindestbeitrag doppelt gezahlt</strong> trotz Anrechnung vom Lohn – mit Beleg korrigierbar.",
    "<strong>Familienausgleichskasse vergessen:</strong> Je nach Kanton kommt ein Beitrag an die Familienzulagen zu den 10 % dazu."])),
  ("Kurz gesagt",
   OL([
    "Selbstständige: 10,0 % AHV/IV/EO (8,1 + 1,4 + 0,5), voller Satz ab CHF 60'500.",
    "Darunter sinkende Skala ab 5,371 % (ab CHF 10'100); darunter: Mindestbeitrag CHF 530.",
    "Renten 2026: 1'260–2'520 Fr./Monat (15'120–30'240 Fr./Jahr), Ehepaar-Max 3'780 Fr./Monat.",
    "13. AHV-Rente: erster Zuschlag mit der Dezemberrente 2026, automatisch."])
   + P("Willst du wissen, wie sich deine Beiträge optimieren lassen und was Beitragslücken kosten? Über die <a href=\"kontakt.html\">Kontaktseite</a> vermitteln wir dir einen geprüften Partner – erstes Offert transparent, vor jedem Mandat.")),
 ]))

for slug, title, meta, sections in articles:
    at.build('de', slug, title, meta, sections)
print("DE built:", [s[0] for s in articles])
