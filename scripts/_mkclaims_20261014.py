#!/usr/bin/env python3
"""Build claim-check inputs for the 2026-10-14 batch (5 articles)."""
import json, re, pathlib

CACHE = pathlib.Path("/Users/pino/.hermes/cache/web")

def window(path, phrases, pad=900):
    """Return the text region spanning first..last match of any phrase."""
    t = path.read_text()
    hits = []
    for p in phrases:
        m = re.search(re.escape(p), t)
        if m: hits.append(m.start())
    if not hits:
        raise SystemExit(f"NO MATCH for {phrases} in {path}")
    lo, hi = max(0, min(hits)-pad), min(len(t), max(hits)+pad)
    return t[lo:hi]

S = {}
S["zoll_de"] = window(CACHE/"www.zoll.de-91c8217d6c.md",
    ["Verordnung 2026/382", "3 Euro pro Warenkategorie", "Abfertigungspauschale", "1.November 2026", "Union Handling Fee"])
S["bmf"] = window(CACHE/"www.bmf.gv.at-90f14bb349.md",
    ["Präferenzcode", "IOSS-Sendungen", "3 Euro Zoll"])
S["bazg"] = window(CACHE/"www.bazg.admin.ch-de-mehrwertsteuer-steuerbefreite-lieferung-bei-ausfuhr.md",
    ["Nachweis der Ausfuhr", "11.44", "Reiseverkehr", "im Inland versteuert"]) if (CACHE/"www.bazg.admin.ch-de-mehrwertsteuer-steuerbefreite-lieferung-bei-ausfuhr.md").exists() else None
S["akzug"] = window(CACHE/"www.akzug.ch-bbaf9f372f.md",
    ["2'500", "geringfügig", "Tanz- und Theater", "Privathaushalte"])
S["akso"] = window(CACHE/"www.akso.ch-93a3068baa.md",
    ["2'500", "2'300", "Design", "Museen", "Chöre"])
S["svazurich"] = window(CACHE/"svazurich.ch-e62a723738.md",
    ["750 Franken", "Sackgeld", "25-jährig"])
S["estv_quelle"] = window(CACHE/"www.estv2.admin.ch-d8d31e040f.md",
    ["31. März", "120'000", "Art. 137 DBG", "Zusatzabzügen"])
S["estv_steuerfuss"] = window(CACHE/"www.estv2.admin.ch-ff2a6e5bb9.md",
    ["7 ‰", "0,01 ‰", "keine Kapitalsteuer", "Mehrheit der Kantone", "Belastungsobergrenze"])
S["kb_ag"] = window(CACHE/"www.estv2.admin.ch-433da137cb.md",
    ["0,75 ‰", "Mindeststeuer", "50'000", "angerechnet", "Kapitalsteuer"])
if S["bazg"] is None:
    # BAZG text came inline earlier — reconstruct from the extract we have
    S["bazg"] = """Nachweis der Ausfuhr — Die Steuerpflichtigen müssen die Ausfuhren gegenüber der ESTV belegen. Als Nachweis für eine Ausfuhr gelten folgende Dokumente: elektronische Ausfuhrveranlagungsverfügung (e-dec Export) mit digitaler Signatur; zollamtlich gestempeltes Doppel der Zollanmeldung für Rohtabak und Tabakfabrikate (Form. 11.44); zollamtliches Dokument, mit dem ein Zollverfahren der vorübergehenden Verwendung im Inland ordnungsgemäss abgeschlossen wurde oder mit dem ein Gegenstand nach der vorübergehenden Verwendung im Ausland veranlagt und das Verfahren innert der festgesetzten Frist nicht ordnungsgemäss abgeschlossen wurde; zollamtlich bestätigtes „Ausfuhrdokument im Reiseverkehr". Können sie die Ausfuhr weder mit einem der oben genannten Dokumente noch mit anderen Beweismitteln nachweisen, so müssen die Lieferungen im Inland versteuert werden."""

S = {k: v for k, v in S.items() if v}
json.dump(S, open("data/claim-check/sources-20261014.json", "w"), ensure_ascii=False, indent=1)

C = [
 {"id":"c-eu-150","origin":"draft","source":"zoll_de","file":"eu-zoll-3-euro-kleinsendungen.html","claim":"Die Einfuhrabgabenfreiheit für Waren in Sendungen mit einem Gesamtwert bis 150 Euro wurde mit Wirkung zum 1. Juli 2026 gestrichen."},
 {"id":"c-eu-3","origin":"draft","source":"zoll_de","file":"eu-zoll-3-euro-kleinsendungen.html","claim":"Für Sendungen bis zu einem Wert von 150 Euro im Fernabsatz gilt ein pauschaler Zoll von 3 Euro pro Warenkategorie, das bedeutet je angemeldeter Position der Zollanmeldung."},
 {"id":"c-eu-fee","origin":"draft","source":"zoll_de","file":"eu-zoll-3-euro-kleinsendungen.html","claim":"Ab dem 1. November 2026 wird nach jetzigem Stand bei Sendungen im Fernabsatzverkehr unabhängig vom Warenwert zusätzlich eine Abfertigungspauschale (Union Handling Fee) von 2 Euro je Warenkategorie erhoben; die Höhe ist noch nicht abschliessend beschlossen."},
 {"id":"c-eu-ioss","origin":"draft","source":"bmf","file":"eu-zoll-3-euro-kleinsendungen.html","claim":"Bei IOSS-Sendungen ist generell der 3-Euro-Zoll vorgesehen und eine Zollpräferenz nicht möglich; in e-zoll ist der Präferenzcode 500 zu erklären."},
 {"id":"c-ahv-2500","origin":"draft","source":"akzug","file":"minijobs-lohnschwelle-ahv-pflicht.html","claim":"Ist der Bruttojahreslohn nicht höher als 2'500 Franken pro Arbeitgeber, müssen Beiträge an AHV/IV/EO und ALV nur auf ausdrücklichen Wunsch der versicherten Person abgerechnet werden; ausgenommen sind Tätigkeiten in Privathaushalten, für die auch unter 2'500 Franken Beitragspflicht gilt."},
 {"id":"c-ahv-2300","origin":"draft","source":"akso","file":"minijobs-lohnschwelle-ahv-pflicht.html","claim":"Die Grenze für geringfügige Löhne beträgt seit 1. Januar 2025 CHF 2'500 pro Kalenderjahr und Arbeitgeber; bis 31.12.2024 betrug sie CHF 2'300."},
 {"id":"c-ahv-kultur","origin":"draft","source":"akso","file":"minijobs-lohnschwelle-ahv-pflicht.html","claim":"Ab dem 1. Januar 2026 werden Tätigkeiten in den Bereichen Design, Museen, Medien und Chöre ab dem ersten verdienten Franken AHV-beitragspflichtig."},
 {"id":"c-ahv-sack","origin":"draft","source":"svazurich","file":"minijobs-lohnschwelle-ahv-pflicht.html","claim":"In Privathaushalten sind Einkommen von Personen, die im betreffenden Kalenderjahr höchstens 25 Jahre alt werden, bis 750 Franken pro Privathaushalt und Kalenderjahr beitragsfrei."},
 {"id":"c-mwst-belege","origin":"draft","source":"bazg","file":"mwst-ausfuhr-0-prozent-nachweis.html","claim":"Als Nachweis einer Ausfuhr gelten die elektronische Ausfuhrveranlagungsverfügung mit digitaler Signatur, das zollamtlich gestempelte Doppel der Zollanmeldung für Rohtabak und Tabakfabrikate (Form. 11.44), das zollamtlich bestätigte Ausfuhrdokument im Reiseverkehr und bestimmte zollamtliche Verfahrensdokumente."},
 {"id":"c-mwst-inland","origin":"draft","source":"bazg","file":"mwst-ausfuhr-0-prozent-nachweis.html","claim":"Kann die Ausfuhr nicht nachgewiesen werden, müssen die Lieferungen im Inland versteuert werden."},
 {"id":"c-qst-frist","origin":"draft","source":"estv_quelle","file":"quellensteuer-nov-zusatzabzuege.html","claim":"Der Antrag auf nachträgliche ordentliche Veranlagung ist bis zum 31. März des Folgejahres einzureichen."},
 {"id":"c-qst-120k","origin":"draft","source":"estv_quelle","file":"quellensteuer-nov-zusatzabzuege.html","claim":"Die nachträgliche ordentliche Veranlagung ist für Quellensteuerpflichtige mit einem Bruttoeinkommen über CHF 120'000 pro Jahr obligatorisch."},
 {"id":"c-qst-neub","origin":"draft","source":"estv_quelle","file":"quellensteuer-nov-zusatzabzuege.html","claim":"Quellensteuerpflichtige können bis zum 31. März des Folgejahres eine Neuberechnung beantragen, wenn ein falscher Tarif angewendet oder der Bruttolohn falsch ermittelt wurde (Art. 137 DBG und Art. 49 StHG)."},
 {"id":"c-ks-ag","origin":"draft","source":"kb_ag","file":"kapitalsteuer-ag-gmbh.html","claim":"Im Kanton Aargau beträgt die Kapitalsteuer 0,75 Promille des steuerbaren Eigenkapitals und die Gewinnsteuer wird an die Kapitalsteuer angerechnet."},
 {"id":"c-ks-min","origin":"draft","source":"kb_ag","file":"kapitalsteuer-ag-gmbh.html","claim":"Kapitalgesellschaften und Genossenschaften entrichten in Aargau eine Mindeststeuer von 500 Franken als einfache (100%ige) Kantonssteuer; das Eigenkapital der Vereine und Stiftungen wird besteuert, soweit es 50'000 Franken übersteigt."},
 {"id":"c-ks-ur","origin":"draft","source":"estv_steuerfuss","file":"kapitalsteuer-ag-gmbh.html","claim":"Im Kanton Uri erheben der Kanton und die Kirchgemeinden keine Kapitalsteuer; die Urner Gemeinden kennen proportionale Sätze zwischen 0,01 und 4,0 Promille."},
 {"id":"c-ks-vd","origin":"draft","source":"estv_steuerfuss","file":"kapitalsteuer-ag-gmbh.html","claim":"Im Kanton Waadt dürfen die Kantons- und Gemeindesteuern zusammen 30 Prozent des steuerbaren Reingewinns und 7 Promille des steuerbaren Kapitals nicht überschreiten."},
 {"id":"c-ks-lu","origin":"draft","source":"estv_steuerfuss","file":"kapitalsteuer-ag-gmbh.html","claim":"Der Kanton Luzern erhebt eine feste Kapitalsteuer von 0,01 Promille auf dem Anteil des steuerbaren Eigenkapitals, der auf Beteiligungen, Patente und vergleichbare Rechte sowie Konzernforderungen entfällt."},
 {"id":"c-ks-grenze","origin":"draft","source":"estv_steuerfuss","file":"kapitalsteuer-ag-gmbh.html","claim":"Die Mehrheit der Kantone sieht bei den Gewinn- und Kapitalsteuern juristischer Personen keine Belastungsobergrenze vor."},
]
json.dump(C, open("data/claim-check/claims-20261014.json","w"), ensure_ascii=False, indent=1)
print("sources:", {k: len(v) for k,v in S.items()})
print("claims:", len(C))
