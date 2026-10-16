#!/usr/bin/env python3
"""Append 5 research cards (2026-10-15 run) to data/content-research.jsonl.
Queue hygiene per gh#6: every pin carries hold_until == pin date.
Refuses to write if a target slug already exists anywhere in the file."""
import json

Q = "/Users/pino/Code/steuerberatung.ch/data/content-research.jsonl"
TODAY = "2026-10-15"

cards = [
    {
        "date": TODAY,
        "type": "article",
        "slug": "gwg-revision-berater-haendler-sorgfaltspflichten",
        "title": "GwG-Revision seit 1.10.2026: neue Sorgfaltspflichten für Berater, Treuhänder und Händler",
        "meta": "Das revidierte Geldwäschereigesetz gilt seit 1.10.2026. Bestimmte Beratungstätigkeiten sind neu pflichtig, Händler müssen Bargeld-Schwellen prüfen. Wer betroffen ist — und was bis wann zu tun ist.",
        "demand": "high",
        "why": "B2B-Tilt (+1, Basis mittel): harte Compliance-Frist für Treuhänder, Berater, Anwälte/Notare sowie Fahrzeughandel/Kunst/Edelmetall — direkt angrenzend an unser Transparenzregister-Topartikel (gleiches Reformpaket TJPG+GwG, gleiche Zielgruppe, Link-Paarung). Fristfenster SRO-Anschluss (Berater: laut BDO zwei Monate ab Inkrafttreten, also ca. 1.12.2026 — zwingend an der GwV verifizieren) macht November zur aktiven Suchwelle -> pin-2026-11-09. Queue-Scan: transparenzregister-tjpg vorhanden (publiziert), GwG-Pflichten selbst nirgends kardiniert.",
        "facts": [
            "Inkrafttreten: Parlamentsabstimmung 26.9.2025 (revidiertes GwG + TJPG), Bundesratsentscheid 12.6.2026, in Kraft per 1.10.2026 — ausser Amtsnotariats-Bestimmungen (Kantone passen Gesetze an) — an admin.ch-Medienmitteilung verifiziert am 15.10.2026; für den Artikel GwG/GwV-Text (SR 955.0/955.01) belegen",
            "Neu unterstellte Beratungstätigkeiten: u.a. Beratung/Abwicklung von Immobilientransaktionen und Gründung/Führung von Rechtseinheiten ohne eigene Tätigkeit; Grenzwerte der GwV definieren die 'berufsmässige' Tätigkeit; SRO-Anschluss innert Übergangsfrist (BDO-Quelle: spätestens 1.12.2026) — [PFLICHTPRÜFUNG: Übergangsbestimmung im GwV-Wortlaut; das Datum nicht ungeprüft publizieren]",
            "Händlerschwellen Art. 8a GwG: Warenumschlaghandel ab CHF 100'000 Barzahlung; Edelmetalle/Edelsteine neu CHF 15'000; Grundstückshandel neu pflichtig — [alle drei Schwellen gegen die revidierte GwV per 1.10.2026 verifizieren; Sekundärquellen sind teils widersprüchlich; Pflichtenumfang enger als bei Finanzintermediären — Umfang nur mit Verordnungstext belegen]"
        ],
        "status": "pending",
        "priority": "pin-2026-11-09",
        "hold_until": "2026-11-09"
    },
    {
        "date": TODAY,
        "type": "article",
        "slug": "carif-krypto-datenaustausch-ab-2027",
        "title": "Krypto-Datenaustausch CARF: was ab 1.1.2027 für Anleger und Plattformen gilt",
        "meta": "Die Schweiz setzt den OECD-Rahmen CARF frühestens per 1.1.2027 um — Krypto-Guthaben werden steuerlich so transparent wie Bankkonten. Meldepflichtige Anbieter, Zeitplan und was das für die Steuererklärung bedeutet.",
        "demand": "high",
        "why": "B2B-Tilt (+1, Basis mittel): Schweizer Krypto-Anbieter/Börsen werden meldende Institutionen (Registrierungs-/Meldepflicht ESTV) — Compliance-Thema für Treuhänder und Fintechs; Konsumentenseite: CH hat eine der höchsten Krypto-Dichte, Paarung mit publiziertem Krypto-Hub-Artikel + pending-Records (staking, Vererben, 3a). Offizielle SIF-Lage (Stand 18.5.2026): Umsetzung frühestens 1.1.2027, Rechtsgrundlagen 2026 nicht anwendbar — Suchwelle zum Inkrafttreten 1.1.2027 plus Steuererklärungssaison -> pin-2027-01-11.",
        "facts": [
            "OECD CARF verabschiedet Juni 2023; Schweiz: innerstaatliche + völkerrechtliche Grundlagen von Bundesversammlung/Bundesrat genehmigt (AIAV-Änderung 26.11.2025); SIF (18.5.2026): AIA über Kryptowerte frühestens ab 1.1.2027, Rechtsgrundlagen finden 2026 keine Anwendung; parlamentarische Beratungen der Partnerstaaten bis im Verlauf 2026 — an sif.admin.ch verifiziert am 15.10.2026; erstes Austauschjahr (Blogquellen teils widersprüchlich: 2027 vs. 2028 — [gegen SIF-FAQ vom 18.5.2026 belegen, bevor ein Austauschdatum behauptet wird])",
            "Melderadius: Krypto-Dienstleister (Börsen, Verwahrer) melden Kontoinhaber- und Transaktionsdaten — Registrierungspflichten und Meldezeitraum aus der revidierten AIAV (26.11.2025) + ESTV-Vollzugsverordnung verifizieren; Umfang der 'relevanten Krypto-Geschäfte' NICHT aus Blogartikeln ableiten",
            "Für Private ändert sich die Deklarationspflicht nicht (ganzheitliche Deklaration: Bestand per 31.12. zu Steuerwerten, Erträge aus Staking/Lending), aber CARF erhöht das Entdeckungsrisiko bei ausländischen Börsen — Querverweis auf pending-Record aia-auslandskonto-entdeckt-nachsteuer statt Zahlenwiederholung; Rechtsgrundlagen Nachsteuer (DBG Art. 45 ff.) gegen fedlex verifizieren"
        ],
        "status": "pending",
        "priority": "pin-2027-01-11",
        "hold_until": "2027-01-11"
    },
    {
        "date": TODAY,
        "type": "article",
        "slug": "vorsteuer-rueckforderung-eu-schweizer-firmen",
        "title": "Vorsteuer-Rückforderung in der EU: das Drittlandsverfahren für Schweizer Firmen",
        "meta": "Messe, Einkauf oder Geschäftsreise in der EU: Schweizer Firmen holen sich ausländische Umsatzsteuer nicht über das EU-Portal, sondern im Drittlandsverfahren zurück — Fristen, Belege, Mindestbeträge.",
        "demand": "high",
        "why": "B2B-Tilt (+1, Basis mittel): jedes KMU mit EU-Messe-/Beschaffungsaktivität; deutschsprachige Übersicht zum Drittlandsverfahren (ohne EU-Niederlassung) ist rar, Treuhänder-Klientel mit klarem Geldwert; Fristenspitze Jahresmitte (DE/AT-Jahresantrag für Vorjahr bis 30.6., zu verifizieren) -> pin-2027-05-24 für live-vor-Frist. Queue-Scan: Vorsteuer-Records nur Eigenverbrauch/Rechnungsformalien/Methode — Ausland-Rückforderung fehlt.",
        "facts": [
            "Drittlandsunternehmen (Sitz CH, keine EU-Niederlassung) nutzen NICHT das EU-Portalverfahren (13. UStSysRl gilt für EU-Ansässige); Erstattungsantrag geht direkt an den Mitgliedstaat der Belastung (DE: Bundeszentralamt für Steuern; AT: Finanzamt) — [Zuständigkeiten je Ziel-Land vor Publikation prüfen]",
            "DE-Frist für Drittlandsfirmen: Jahresantrag für Vorsteuern 2026 bis 30.6.2027 (sechs Monate nach Ablauf des Erstattungszeitraums — BZSt-Merkblatt/§18 UStG); AT-Frist 30.6. (AT-Fachartikel) — [Länderfristen einzeln mit Primärquelle belegen, keine Pauschalaussage 'alle EU-Länder'; Mindestbeträge (EUR 50 Jahresantrag / 400 bei kürzerem Zeitraum?) verifizieren]",
            "Erstattungsfähigkeit länderspezifisch eingeschränkt: Verpflegung/Restaurant oft ganz oder teilweise ausgeschlossen, Belegpflichten ab Schwellen (DE Kraftstoff ab 250 EUR), Hotel/Messe typisch gut erstattungsfähig — je Land aus BZSt-/BMF-Praxis belegen; in CH ist auf ausländische VAT kein Vorsteuerabzug möglich (ESTV-Praxis; MWSTG-Grundlagen verifizieren)"
        ],
        "status": "pending",
        "priority": "pin-2027-05-24",
        "hold_until": "2027-05-24"
    },
    {
        "date": TODAY,
        "type": "article",
        "slug": "angehoerige-lohn-familienbetrieb-ahv",
        "title": "Lohn an Angehörige im Familienbetrieb: AHV-Pflicht, Fremdüblichkeit, Steuerfolgen",
        "meta": "Ehepartner, Kinder, Eltern im eigenen Betrieb: Ab wann der Lohn fremdüblich sein muss, wer sich AHV/UVG versichern muss und welche Fehler SVA und Steueramt ahnden. Checkliste für KMU.",
        "demand": "high",
        "why": "B2B-Tilt (+1, Basis mittel): KMU-Standardfrage mit Prüfungsrisiko (verdeckte Gewinnausschüttung, Beitragsausfall, AHV-Nachforderung); Treuhänder-Lohnläufe; Suchwelle Jahresend-/Lohndeklaration bis 31.1. (AHV-Jahreslohnabrechnung) -> pin-2027-01-22 live vor der Deadline. Queue-Scan: privathaushalt-putzfrau (fremder Haushalt) und dividenden-oder-lohn (GmbH-Geschäftsführer-Lohnwahl) vorhanden — Angehörigen-Lohn als Eigenstand fehlt.",
        "facts": [
            "Echtes Arbeitsverhältnis = Beitragspflicht AHV/IV/EO + UVG/ALV: Weisungsunterstellung, vertraglicher fremdüblicher Lohn, tatsächliche Arbeit, Abrechnung über die Ausgleichskasse — Abgrenzung an AHVV Art. 5 Abs. 2 (unternehmerisches Risiko => selbstständig erwerbend) + massgebendem Kreisschreiben belegen",
            "Steuerliche Anerkennung: nur fremdüblicher Lohn abzugsfähig, sonst verdeckte Gewinnausschüttung bei AG/GmbH (Aufrechnung + 35 % Verrechnungssteuerfolge) bzw. Abzugsverweigerung/Privatanteil im Einzelunternehmen — Praxisbelege (EFB/ESTV-Kreisschreiben vGA) einholen; keine Pauschalprozente publizieren",
            "Sozialversicherungs-Status von mitarbeitenden Angehörigen mit Kapital-/Mitwirkungsanteil (Ehepartner, Kinder): SVA-Prüfkriterien (Einfluss auf Betriebsführung, Risikobeteiligung) — [keine %-Schwelle ohne Kreisschreiben/Verfügungspraxis belegen]; BVG-Pflicht nur bei unselbstständiger Stellung; Querverweis auf pending-Record Familienzulagen"
        ],
        "status": "pending",
        "priority": "pin-2027-01-22",
        "hold_until": "2027-01-22"
    },
    {
        "date": TODAY,
        "type": "article",
        "slug": "pensionskasse-freiwillig-selbststaendige",
        "title": "Freiwillige Pensionskasse für Selbstständige: die 2. Säule als Steuerhebel",
        "meta": "Selbstständigerwerbende können sich freiwillig einer BVG-Sammelstiftung anschliessen: höhere Beiträge als die Säule 3a, Abzug, Vorsorgeschutz. Statuten, Beiträge, Einkauf und die 3-Jahres-Regel erklärt.",
        "demand": "high",
        "why": "B2B-Tilt (+1, Basis mittel): freiwillige Vorsorge Selbstständiger ist ein Treuhänder-Beratungsthema (Abgrenzung 1. Säule freiwillig / 2. Säule / 3a/3b); Jahresendfenster (Beitritt/Einkauf per 31.12., Budgetentscheid für 2027) + Januar-Planungssuche -> pin-2026-11-20 live vor der 31.12.-Ablösung. Queue-Scan: pensionskassen-einkauf (Arbeitnehmer, publiziert), saeule-2a (Führungskräfte, pending), 3a-Records — Selbstständigen-Freiwilligkeit der 2. Säule fehlt.",
        "facts": [
            "Freiwilliger BVG-Anschluss für Selbstständigerwerbende: nur möglich, wenn die Stiftungsstatuten freiwillige Mitglieder zulassen — nicht jede Sammelstiftung bietet ihn; Versicherungsleistungen (Tod/Invalidität) und Mindestbeiträge nach Stiftungsreglement — [Anbietervergleiche vermeiden; keine gesetzliche Bundes-Obergrenze erfinden; BVG/Statuten-Systematik belegen]",
            "Abzugsmechanik: Beiträge und Einkäufe der Freiwilligen — [verifizieren, ob Abzug als Geschäftskosten (Art. 22 DBG) oder als Vorsorgeabzug läuft, und ob die 3-Jahres-Regel für Einkäufe vor Kapitalbezug (Art. 79b/79c BVG / entsprechende DBG-Norm) hier greift]; Zahlen nur mit Quelle — publizierter pensionskassen-einkauf-Record deckt die Kaufrecht-/Fristlogik bereits ab (nicht duplizieren)",
            "Vorsorge-Paket für Selbstständige als Vergleichstabelle OHNE Zahlen: freiwillige AHV-Beiträge (Verweis auf AHV-Records), 2. Säule freiwillig (dieser Artikel), Säule 3a (Verweis publizierte 3a-Records), Säule 3b (pending 3b-Record) — nur Querverweise; Kapitalbezug vs. Rente ohne Kantonsätze"
        ],
        "status": "pending",
        "priority": "pin-2026-11-20",
        "hold_until": "2026-11-20"
    },
]

with open(Q) as f:
    existing = set()
    for line in f:
        try:
            r = json.loads(line)
        except Exception:
            continue
        if isinstance(r, dict) and r.get("slug"):
            existing.add(r["slug"])

clash = [c["slug"] for c in cards if c["slug"] in existing]
if clash:
    raise SystemExit(f"ABORT — slug already in queue: {clash}")

with open(Q, "a", encoding="utf-8") as f:
    for c in cards:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"appended {len(cards)} records:")
for c in cards:
    print(f"  {c['slug']}  [{c['demand']}]  {c['priority']}")
