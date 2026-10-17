#!/usr/bin/env python3
"""Append the 2026-10-17 research batch (5 topics) to the publish queue.

Schema follows the last records of data/content-research.jsonl:
  date, type, slug, title, meta, demand, why, facts, status, priority, hold_until
Every pinned card gets hold_until == pin date (gh#6 rule, enforced by
scripts/validate_queue.py). Run: python3 scripts/_append_20261017_research.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "content-research.jsonl")
DATE = "2026-10-17"

RECORDS = [
    {
        "date": DATE,
        "type": "article",
        "slug": "revisionsstelle-opting-out-handelsregister",
        "title": "Revisionsstelle sparen: Den Opting-out müssen Sie vor dem 31. Dezember anmelden",
        "meta": "AG und GmbH mit höchstens 10 Vollzeitstellen im Jahresdurchschnitt können auf die eingeschränkte Revision verzichten (Art. 727a Abs. 2 OR). Der einstimmige Beschluss muss vor Beginn des Geschäftsjahres beim Handelsregisteramt sein — sonst gilt die Prüfpflicht 2027.",
        "demand": "high",
        "why": "B2B-Tilt (+1, Basis mittel): betrifft jede der über 100'000 kleinen AG/GmbH und spart direkt Honorar (eingeschränkte Revision ist ein wiederkehrender Posten); die Mechanik ist eine lautlose Frist (Anmeldung muss vor dem neuen Geschäftsjahr eingetragen sein) — genau das Muster, das auf dieser Site bereits funktioniert (transparenzregister-tjpg = Gesellschafter-Meldepflicht mit Frist, einziger belegter organischer Bing-Treffer). Zielgruppe Inhaber/Geschäftsführer/Treuhänder; deutschsprachige Erklärstücke stammen von Kanzleien (Caminada, nexova, kmu.admin.ch) und sind für Laien nicht lesbar. Peak-Fenster: GV-/Jahresendplanung November–Dezember für das Geschäftsjahr 2027 -> pin-2026-11-20, live sechs Wochen vor der 31.12.-Grenze. Queue-Scan: 'revision' trifft nur gwg-revision-berater-haendler-sorgfaltspflichten (GwG-Sorgfaltspflichten der Prüfer, nicht Revisionspflicht der Gesellschaft); handelsregister-pflicht-einzelfirma-100000 ist die Eintragungspflicht von Einzelunternehmen — andere Norm, andere Rechtsgrundlage. Kein Duplikat.",
        "facts": [
            "Schwellenwerte: ordentliche Revision, wenn die Gesellschaft an zwei aufeinanderfolgenden Geschäftsjahren zwei dieser drei Grössen überschreitet — Bilanzsumme CHF 20 Mio., Umsatzerlös CHF 40 Mio., 250 Vollzeitstellen im Jahresdurchschnitt (Art. 727 OR; zusätzlich Publikumsgesellschaften und konzernrevisionspflichtige Gesellschaften). Darunter eingeschränkte Revision, wenn zwei der kleineren Grössen überschritten werden (Bilanzsumme CHF 10 Mio., Umsatz CHF 20 Mio., 50 Vollzeitstellen — Art. 727a Abs. 1 OR) [beide Satze exakt an fedlex OR 727/727a in der geltenden Fassung belegen; der weka-Fachartikel nennt 10/20/50 teils als Ordentlich-Revision — widersprüchliche Sekundärquelle, nicht übernehmen]",
            "Opting-out: Gesellschaften mit höchstens 10 Vollzeitstellen im Jahresdurchschnitt können durch einstimmigen Beschluss aller Gesellschafter bzw. Aktionäre auf die eingeschränkte Revision verzichten (Art. 727a Abs. 2 OR); der Verzicht ist dem Handelsregisteramt einzureichen und wirkt erst für ein Geschäftsjahr, das nach der Eintragung beginnt — Caminada-Fallbeispiel: bis Ende Jahr eingereicht, gilt ab dem Folgejahr [Anmeldeweg (HR2-Portal/zHAB) und Stichtagslogik gegen Praxis eines Handelsregisteramts belegen; Frist 'vor Beginn des Geschäftsjahres' nur mit Quelle behaupten]",
            "Gegenrechte und Folgen: Ein Gesellschafter kann eine eingeschränkte Revision verlangen, selbst wenn die Gesellschaft optiert hat — nexova nennt 'mindestens 10 Tage vor der Generalversammlung' [Artikelnummer (Art. 727a Abs. 3/4 OR) und Frist an fedlex verifizieren]; keine Revisionspflicht besteht für Einzelunternehmen und Personengesellschaften; fehlt die Revisionsstelle trotz Pflicht, sind Jahresrechnung/Entlastung nicht gültig abzunehmen und der Vermerk 'geprüft' ist unzulässig [keine Bussen- oder Kostensätze erfinden — wenn Busse, dann mit OR/HRV-Norm belegen]",
        ],
        "status": "pending",
        "priority": "pin-2026-11-20",
        "hold_until": "2026-11-20",
    },
    {
        "date": DATE,
        "type": "article",
        "slug": "aialg-lohndaten-austausch-2027",
        "title": "AIALG ab 2027: Lohndaten von Grenzgängern und Telearbeitenden elektronisch melden",
        "meta": "Der Bundesrat setzt das Lohndaten-Austauschgesetz (AIALG) per 1.1.2027 in Kraft. Arbeitgebende melden Lohn- und Quellensteuerdaten von Mitarbeitenden aus Italien und Frankreich der kantonalen Steuerverwaltung — Fristen, Datenfelder, Aufbewahrung, Bussen.",
        "demand": "high",
        "why": "B2B-Tilt (+1, Basis mittel): Gesetz mit amtlichem Inkrafttretensdatum (1.1.2027), das die Lohnabrechnung aller Betriebe mit ausländischem Personal umstellt — Kernzielgruppe Treuhänder/HR/Payroll, genau der Kanal, über den transparenzregister-tjpg funktioniert hat; frischer Amts-Hook: TREX (Treuhand|SUISSE-Fachzeitschrift) meldet den Bundesratsentscheid in Ausgabe 5/26 vom 1.10.2026, also mitten in der Vorbereitungsphase. Betroffenheitsradius asymmetrisch: das Frankreich-Abkommen erfasst alle Schweizer Arbeitgebenden, das Italien-Abkommen v.a. TI/VS/GR — deshalb auch für die Deutschschweiz relevant. Queue-Scan: grenzgaenger-de-fr-it-steuern (publiziert, materiell-steuerliche Regeln für Grenzgänger), grenzgaenger-homeoffice-telearbeit-regeln (publiziert, Telearbeit-Schwellen), quellensteuer-abrechnung-arbeitgeber-pflichten (pending, Quellensteuer-Abrechnung) — die Meldepflicht nach AIALG als Eigenstand fehlt. Peak: Inkrafttreten 1.1.2027 + erste Melde- und Informationsrunden 2027 (IT 20. März, FR 30. November, Mitarbeitenden-Info bis 28. Februar) -> pin-2026-12-18, live unmittelbar vor dem 1.1.",
        "facts": [
            "In-Kraft-Treten: Bundesgesetz über den internationalen automatischen Informationsaustausch betreffend Lohndaten (AIALG) gilt ab 1.1.2027 (TREX 5/26 vom 1.10.2026: 'Der Bundesrat hat beschlossen, das AIALG per 1. Januar 2027 in Kraft zu setzen'; Botschaft BBl 2025 1656; PwC und OBT bestätigen dasselbe Datum) [SR-Nummer und Inkrafttretens-Verfügung via fedlex/admin.ch-Medienmitteilung belegen; für das Lohnjahr 2026 nicht als 'bereits geltend' formulieren]",
            "Fristen und Umfang je Abkommen: Italien (Grenzgängerabkommen, seit 1.1.2024, erster Austausch März 2025 fürs Steuerjahr 2024) — Meldung bis 20. März des Folgejahres; Frankreich (ständiges Zusatzabkommen zur Telearbeit, anwendbar ab 1.1.2026, erster Austausch geplant Herbst 2027 fürs Steuerjahr 2026) — Meldung bis 30. November des Folgejahres; gemeldete Felder umfassen u.a. Identifikation, Wohnadresse, Steuernummer des Ansässigkeitsstaats, Brutto-Lohnsumme, obligatorische Sozialabgaben (AHV/IV/EO, ALV, BVG), Quellensteuerbetrag, Arbeitgeberdaten; Telearbeitsanteil max. 40 % [alle Fristen/Felder gegen die Abkommenstexte (fedlex AS) und das ESTV-/Kantonale Vollzugsmerkblatt prüfen — OBT/PwC sind Sekundärquellen; Format und Übermittlungsweg legen die Kantone fest]",
            "Arbeitgeber-Pflichten und Sanktionen: jährliche elektronische Übermittlung an die kantonale Steuerbehörde, Informationspflicht gegenüber den betroffenen Mitarbeitenden bis spätestens 28. Februar des Jahres der ersten Übermittlung, zehnjährige Aufbewahrung der Unterlagen (Art. 958f OR), DSG-Rechte der Mitarbeitenden (Auskunft Art. 25, Berichtigung Art. 27, Löschung/Sperrung Art. 28, Einschränkung Art. 29, Beschwerde Art. 38 DSG); Bussen laut OBT bis CHF 1'000 bei leichter/erster und bis CHF 10'000 bei schwerer/wiederholter Pflichtverletzung [Bussbeträge, Adressat und Tatbestand im AIALG-Wortlaut verifizieren — nicht als 'pro Mitarbeiter' darstellen; 40-%-Schwelle nur mit Abkommenstext belegen]",
        ],
        "status": "pending",
        "priority": "pin-2026-12-18",
        "hold_until": "2026-12-18",
    },
    {
        "date": DATE,
        "type": "article",
        "slug": "mwst-gruppenbesteuerung-art-13",
        "title": "MWST-Gruppe: Wann sich der Zusammenschluss von Firmen lohnt — und was die Mithaftung kostet",
        "meta": "Rechtsträger unter einheitlicher Leitung können sich auf Antrag zu einem einzigen MWST-Subjekt zusammenschliessen (Art. 13 MWSTG). Innenleistungen fallen dann aus der Steuer — dafür haften alle Mitglieder solidarisch. Antrag, Voraussetzungen, Bindungsdauer.",
        "demand": "high",
        "why": "B2B-Tilt (+1, Basis mittel): Strukturthema mit echtem Geldwert — Holding-/Betriebsgruppen (Management Fees, IT-, Immobilien- und Dienstleistungsgesellschaften unter einer Mutter) versteuern heute Innenleistungen, die wirtschaftlich Nullbewegungen sind; die ESTV hat die MWST-Info 03 Gruppenbesteuerung am 27.5.2026 neu herausgegeben (Praxisüberprüfung mit Publikationsdatum 20.9.2024 zur zeitlichen Wirkung), also frischer Rechtsstand, aber auf Deutsch nur in Kanzlei-Newslettern erklärt; Treuhänder-Klientel. Entscheidungslogik: Der Zusammenschluss wirkt nur auf Beginn einer Steuerperiode (= Kalenderjahr) und muss mindestens eine Periode gehalten werden -> Entscheidungsfenster November–Dezember für 2027 -> pin-2026-11-27. Queue-Scan: 14 MWST-Records decken Registrierung (100k/AGOV), Methoden (Saldosteuersatz), Option, Rechnungen, Eigenverbrauch, Kontrolle, EU-Rückforderung ab — Gruppenbesteuerung kommt in keinem Record vor.",
        "facts": [
            "Voraussetzung 'einheitliche Leitung' (Art. 13 Abs. 1 MWSTG): Indiz ist eine stimmenmässige Beteiligung von mehr als 50 % zwischen den Rechtsträgern; fehlt sie — etwa bei natürlichen Personen oder Stiftungen — muss der ESTV im Einzelnen belegt werden, warum trotzdem von einheitlicher Leitung auszugehen ist (Statuten, Verträge) (MWST-Info 03, Fassung 27.5.2026); alle Mitglieder müssen im Inland domiziliert und MWST-pflichtig bzw. von der Pflicht befreit sein [Mitglieds-Voraussetzungen + Schwellenlogik an MWST-Info 03 (swissvat.ch/MI_03_27.05.2026.pdf) und Art. 13/MWSTV belegen; Einverständniserklärung zur Gruppenbesteuerung und Mithaftung = Formular Nr. 664]",
            "Zeitliche Wirkung und Bindung: Der Zusammenschluss kann auf den Beginn jeder Steuerperiode gewählt werden (Art. 13 Abs. 2 MWSTG); die Gruppenbesteuerung muss während mindestens einer Steuerperiode beibehalten werden und endet auf Antrag per Ende der laufenden Steuerperiode (weka-Fachartikel); Antrag wird von der ESTV genehmigt, solange noch keiner der betroffenen Rechtsträger für die betreffende Abrechnungsperiode abgerechnet hat (MWST-Info 03, sinngemäss) [Praxisänderung mit Publikationsdatum 20.9.2024 zur zeitlichen Wirkung gegen MWST-Info 20 verifizieren, bevor Rückwirkung/Optik 'ab Gesuchseingang' behauptet wird]",
            "Wirtschaftliche Wirkung und Risiko: Lieferungen und Dienstleistungen innerhalb der Gruppe sind nicht steuerbar, die Vorsteuern der Gruppenmitglieder werden zentral geltend gemacht — im Gegenzug haften die Mitglieder für die MWST-Schulden der Gruppe (Mithaftung nach Formular 664), und Vorsteuerkorrekturen bei Nutzungsänderungen bzw. beim Ausscheiden eines Mitglieds sind zu prüfen; Vorsorgeeinrichtungen nach BVG können nur Mitglied sein, wenn sie die einheitliche Leitung innehaben oder unter der einheitlichen Leitung einer anderen BVG-Vorsorgeeinrichtung stehen [Mithaftungs-Norm (MWSTG/MWSTV-Artikel) und Exit-Mechanik an der Primärquelle belegen; keine 'Ersparnis in %' oder Sample-Rechnung ohne eigene, nachvollziehbare Berechnung]",
        ],
        "status": "pending",
        "priority": "pin-2026-11-27",
        "hold_until": "2026-11-27",
    },
    {
        "date": DATE,
        "type": "article",
        "slug": "ahv-arbeitgeberkontrolle-nachzahlung",
        "title": "AHV-Arbeitgeberkontrolle: Was die Ausgleichskasse prüft und was Fehler zurückwirkend kosten",
        "meta": "Ausgleichskassen müssen jeden Arbeitgeber periodisch kontrollieren (Art. 63 AHVG). Welche Lohnbestandteile beitragspflichtig sind, wie weit die Kasse zurückblickt, wer den Arbeitnehmeranteil trägt und wie Sie sich auf die Kontrolle vorbereiten.",
        "demand": "high",
        "why": "B2B-Tilt (+1, Basis mittel): jeder Betrieb mit Angestellten steckt im Kontrollzyklus 'seiner' Ausgleichskasse, und der Arbeitgeber haftet für beide Beitragsanteile — hohe Nachforderung plus Verzugszins, also dieselbe Geldgefahr-Intention wie der publizierte MWST-Kontrolle-Artikel, nur bei einer anderen Behörde und mit grösserem Personenkreis; Suchende sind Lohnbuchhaltung/HR/Geschäftsführung plus Treuhänder (Komplement zu pending quellensteuer-abrechnung-arbeitgeber-pflichten und ahv-lohnabrechnung-annualisieren-frist-31-januar, die beide andere Pflichten erklären). Peak: Lohnabrechnungssaison Januar (Jahresdeklaration) + Kontrolleankündigungen -> pin-2027-01-15 (bewusst nicht der Slot 2027-01-04, in dem bereits 14 pending-Karten liegen).",
        "facts": [
            "Kontrollpflicht und Rückblick: Die Ausgleichskassen kontrollieren ihre angeschlossenen Arbeitgebenden periodisch auf die Einhaltung der gesetzlichen Bestimmungen (Art. 63 Abs. 1 AHVG; sva-sz.ch, rsa.ch, handelskammer-d.ch bestätigen); in der Praxis prüfen viele Kassen etwa alle fünf Jahre, weil Beitragsforderungen fünf Jahre nach Ablauf des Kalenderjahres, in dem sie hätten bezahlt werden müssen, verjähren (Art. 16 AHVG; Wegleitung über den Bezug der Beiträge WBB, Rz zu Festsetzungsverjährung, Stand 1.1.2025) ['alle fünf Jahre' ist Kassenpraxis, keine eidgenössische Frist — mit Kassenquelle formulieren; WBB-Randziffer via koordination.ch belegen]",
            "Prüfgegenstand massgebender Lohn: Barlöhne, Naturallöhne, Lohnzulagen, Gratifikationen und ähnliche Leistungen (inkl. 13. Monatslohn), Prämien für besondere Leistungen, Versicherungs- und ähnliche Leistungen sowie Unkostenentschädigungen ohne genehmigte Regelung — das Suva-Factsheet 'AHV- und Suva-pflichtige Löhne' (Publikation 1313.d, Ausgabe 4.2.2026) führt die Positionen alphabetisch auf und enthält die AHV/IV/EO- und ALV-Übersicht [mit 1313.d und der ESTV-Wegleitung zum Lohnausweis abgleichen; die CHF-600-Freigrenze bei Naturalgeschenken und die Spesenreglement-Systemik (Ziff. 13.2/15) sind auf der Site bereits in sachzuwendungen-mitarbeitende-600-freigrenze und pauschalspesen-spesenreglement-genehmigt behandelt — dorthin verlinken, nicht neu aufrollen]",
            "Folgen bei Nachforderung: Der Arbeitgeber ist Beitragsschuldner und trägt nach rsa.ch-Praxis sowohl den Arbeitgeber- als auch den Arbeitnehmeranteil, wenn er den Abzug beim Lohn unterlassen hat [Rückgriff des Arbeitgebers auf den Arbeitnehmeranteil und dessen Frist an Art. 52 AHVG / Wegleitung AHVB belegen — nicht als 'immer' darstellen]; dazu Verzugszins — BDO nennt 'fünf Prozent' für nachträglich deklarierte Löhne [Satz seit der letzten Änderung der AHVV prüfen (4.25 % vs. 5 %), Zahl nur mit BSV-/AHVV-Beleg]; Bussatbestände bei Nichtabrechnung (Art. 79 AHVG) mit Betrag am Gesetzestext verifizieren, keinen Prozentsatz oder Beispiel-Nachforderung ohne Beleg publizieren",
        ],
        "status": "pending",
        "priority": "pin-2027-01-15",
        "hold_until": "2027-01-15",
    },
    {
        "date": DATE,
        "type": "article",
        "slug": "mwst-vorsteuerkorrektur-liegenschaft",
        "title": "Vorsteuerkorrektur bei Liegenschaften: Die 20-Jahres-Regel, die beim Umbau zum teuren Fehler wird",
        "meta": "Wer eine Geschäftsliegenschaft neu nutzt oder verkauft, muss die damals abgezogenen Vorsteuern berichtigen — über 20 Jahre zu 5 % pro Jahr (Art. 32 MWSTG). So ermitteln Sie die Korrektur, was Option und Nutzungsänderung damit zu tun haben.",
        "demand": "high",
        "why": "B2B-Tilt (+1, Basis mittel): betrifft Immobilien-Gesellschaften, Liegenschaftsverwaltungen, Gewerbevermieter und jede KMU, die ihr eigenes Gebäude von 'Büro/Laden' auf 'Wohnen ohne Option' oder auf einen nicht abzugsberechtigenden Zweck umstellt — die Korrektur ist ein Buchungs- und Jahresend-Thema mit klarer Geldwirkung, und die ESTV verlangt sie grundsätzlich effektiv ermittelt statt pauschal (TREX-Fachartikel 'Die (neue) Handhabung der MWST im Bereich der Immobilien'); dazu hat die ESTV die MWST-Info 09 Vorsteuerabzug total überarbeitet (BDO-Review) — Rechtsstand 2026/27, auf Deutsch kaum laienfähig erklärt. Queue-Scan/Abgrenzung: pending mwst-option-wechsel-frist-31-dezember behandelt die FRIST und den Optionswechsel; pending mwst-vorsteuer-eigenverbrauch-jahresende behandelt Eigenverbrauch und Jahresend-Abstimmung — die 20-jährige Vorsteuerberichtigung bei Nutzungsänderung als eigenes Instrument fehlt. Peak: Jahresendabrechnung + Um-/Ausbauplanung Nov–Dez -> pin-2026-12-11, live vor dem Jahresabschluss.",
        "facts": [
            "Mechanik: Ändert sich die Verwendung einer Leistung nachträglich (von abzugsberechtigender zu nicht abzugsberechtigender Verwendung oder umgekehrt), ist der Vorsteuerabzug zu korrigieren; bei Liegenschaften und Liegenschaftsteilen wird über 20 Jahre berichtigt — jedes abgelaufene Jahr mindert den korrigierbaren Betrag um 5 %, nach 20 Jahren entfällt die Korrektur (Art. 32 MWSTG i.V.m. MWSTV; weka-Fachartikel 'Nutzungsänderung MWST'; MWST-Info 10 Vorsteuerberichtigungen, Fassung 20.3.2026) [Artikel und Berichtigungszeitraum exakt an fedlex SR 641.20/MWSTV + Ziffern der MWST-Praxispublikationen belegen; Rechenbeispiel nur mit selbst nachvollziehbarer Rechnung, keine Zahlen aus DE-Quellen (§ 15a UStG) übernehmen]",
            "Auslösung und Nachweis: Jede vollumfängliche Nutzungsänderung ist abzurechnen und die Korrektur ist im Liegenschaftsbereich grundsätzlich effektiv zu ermitteln, nicht geschätzt; die revidierte MWST-Info 09 verlangt umfangreichere Nachweise bei Nutzungsänderungen und zusammen mit Subventionen (BDO-Übersicht), neu sind auch Einlageentsteuerung und Marge/Beleglogik kombiniert geregelt [Publikationsdatum/Umsetzungsjahr der geänderten Praxis + Übergangsregel gegen swissvat.ch-Praxispublikation und MWST-Info 20 (zeitliche Wirkung von Praxisfestlegungen) verifizieren, bevor 'seit 1.1.2026' behauptet wird]",
            "Wechselwirkung mit Option, Verkauf und Bezug: Optiert ein Vermieter für die Vermietung (Art. 22 MWSTG), wird die Miete steuerbar und die Vorsteuern aus Bau/Unterhalt sind abzugsfähig — beim Übergang zu reiner Wohnvermietung ohne Option schlägt die 20-jährige Korrektur zu; umgekehrt erlaubt die Einlageentsteuerung den nachträglichen Abzug (Art. 32 MWSTG); beim Verkauf einer Liegenschaft kann steuerbare Lieferung oder Ausnahmen-/Optionslogik entscheiden [Formular-/ePortal-Weg für die Deklaration der Korrektur und die Marge bei Liegenschaftsverkäufen an ESTV-Praxis belegen; Content-Zuschnitt auf pending-Records abstimmen (mwst-option-wechsel-frist-31-dezember = Frist, dieser Artikel = Korrekturmechanik)]",
        ],
        "status": "pending",
        "priority": "pin-2026-12-11",
        "hold_until": "2026-12-11",
    },
]


def main():
    existing_slugs = set()
    with open(QUEUE, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("slug"):
                existing_slugs.add(rec["slug"])
            if rec.get("published_slug"):
                existing_slugs.add(rec["published_slug"])

    for rec in RECORDS:
        if rec["slug"] in existing_slugs:
            raise SystemExit(f"ABORT: slug already in queue: {rec['slug']}")
        if rec["priority"].replace("pin-", "") != rec["hold_until"]:
            raise SystemExit(f"ABORT: pin/hold_until mismatch: {rec['slug']}")

    with open(QUEUE, "a", encoding="utf-8") as fh:
        for rec in RECORDS:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"appended {len(RECORDS)} records: " + ", ".join(r["slug"] for r in RECORDS))


if __name__ == "__main__":
    main()
