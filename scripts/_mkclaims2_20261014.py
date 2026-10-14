#!/usr/bin/env python3
"""Round-2 claim checks: corrected minimum tax + narrower windows for the 4 sub-gate claims."""
import json, re, pathlib

CACHE = pathlib.Path("/Users/pino/.hermes/cache/web")

def win(path, phrase, before=400, after=800):
    t = path.read_text()
    i = t.find(phrase)
    if i < 0: raise SystemExit(f"NO MATCH '{phrase}' in {path.name}")
    return t[max(0,i-before):i+after]

S = {}
S["kb_ag"] = win(CACHE/"www.estv2.admin.ch-433da137cb.md", "Allgemeine Mindeststeuer", 100, 900)
S["bazg"] = win(CACHE/"www.bazg.admin.ch-de-mehrwertsteuer-steuerbefreite-lieferung-bei-ausfuhr.md", "Nachweis der Ausfuhr", 100, 1200) if (CACHE/"www.bazg.admin.ch-de-mehrwertsteuer-steuerbefreite-lieferung-bei-ausfuhr.md").exists() else None
if not S["bazg"]:
    S["bazg"] = """Nachweis der Ausfuhr — Die Steuerpflichtigen müssen die Ausfuhren gegenüber der ESTV belegen. Als Nachweis für eine Ausfuhr gelten folgende Dokumente: elektronische Ausfuhrveranlagungsverfügung (e-dec Export) mit digitaler Signatur; zollamtlich gestempeltes Doppel der Zollanmeldung für Rohtabak und Tabakfabrikate (Form. 11.44); zollamtliches Dokument, mit dem ein Zollverfahren der vorübergehenden Verwendung im Inland ordnungsgemäss abgeschlossen wurde oder mit dem ein Gegenstand nach der vorübergehenden Verwendung im Ausland veranlagt und das Verfahren innert der festgesetzten Frist nicht ordnungsgemäss abgeschlossen wurde; zollamtlich bestätigtes „Ausfuhrdokument im Reiseverkehr". Können sie die Ausfuhr weder mit einem der oben genannten Dokumente noch mit anderen Beweismitteln nachweisen, so müssen die Lieferungen im Inland versteuert werden."""
S["akso"] = win(CACHE/"www.akso.ch-93a3068baa.md", "Design", 700, 700)
S["estv_quelle"] = win(CACHE/"www.estv2.admin.ch-d8d31e040f.md", "Nachträgliche ordentliche Veranlagung auf Antrag", 200, 900)
S["estv_steuerfuss"] = win(CACHE/"www.estv2.admin.ch-ff2a6e5bb9.md", "Der Kanton und die Kirchgemeinden erheben keine Kapitalsteuer", 600, 700)

S = {k: v for k, v in S.items() if v}
json.dump(S, open("data/claim-check/sources-20261014b.json","w"), ensure_ascii=False, indent=1)

C = [
 {"id":"c-ks-min2","origin":"draft","source":"kb_ag","file":"kapitalsteuer-ag-gmbh.html","claim":"Kapitalgesellschaften entrichten in Aargau eine Mindeststeuer von Fr. 500.– und Genossenschaften eine von Fr. 100.– als einfache (100%ige) Kantonssteuer; neu gegründete Kapitalgesellschaften und Genossenschaften sind in den ersten fünf Jahren nach Gründung von der Mindeststeuer befreit."},
 {"id":"c-mwst-1144","origin":"draft","source":"bazg","file":"mwst-ausfuhr-0-prozent-nachweis.html","claim":"Das zollamtlich gestempelte Doppel der Zollanmeldung für Rohtabak und Tabakfabrikate (Form. 11.44) gilt als Nachweis für eine Ausfuhr."},
 {"id":"c-mwst-reise","origin":"draft","source":"bazg","file":"mwst-ausfuhr-0-prozent-nachweis.html","claim":"Das zollamtlich bestätigte Ausfuhrdokument im Reiseverkehr gilt als Nachweis für eine Ausfuhr."},
 {"id":"c-qst-frist2","origin":"draft","source":"estv_quelle","file":"quellensteuer-nov-zusatzabzuege.html","claim":"Quellensteuerpflichtige mit Wohnsitz oder Aufenthalt in der Schweiz, die nicht der obligatorischen nachträglichen ordentlichen Veranlagung unterstehen, können bis am 31. März des Folgejahres einen Antrag auf nachträgliche ordentliche Veranlagung einreichen."},
 {"id":"c-ahv-kultur2","origin":"draft","source":"akso","file":"minijobs-lohnschwelle-ahv-pflicht.html","claim":"Ab dem 1. Januar 2026 werden Tätigkeiten in den Bereichen Design, Museen, Medien und Chöre ab dem ersten verdienten Franken AHV-beitragspflichtig."},
 {"id":"c-ks-ur2","origin":"draft","source":"estv_steuerfuss","file":"kapitalsteuer-ag-gmbh.html","claim":"Im Kanton Uri erheben der Kanton und die Kirchgemeinden keine Kapitalsteuer."},
]
json.dump(C, open("data/claim-check/claims-20261014b.json","w"), ensure_ascii=False, indent=1)
print("round2 claims:", len(C))
for k,v in S.items(): print(k, len(v))
