#!/usr/bin/env python3
"""Round-3: precise windows for the two unresolved claims."""
import json, pathlib

CACHE = pathlib.Path("/Users/pino/.hermes/cache/web")

def win(path, phrase, before, after):
    t = path.read_text()
    i = t.find(phrase)
    if i < 0: raise SystemExit(f"NO MATCH '{phrase}'")
    return t[max(0,i-before):i+after]

S = {}
S["estv_quelle"] = win(CACHE/"www.estv2.admin.ch-d8d31e040f.md", "bis am 31. März des Folgejah", 700, 500)
S["estv_steuerfuss"] = win(CACHE/"www.estv2.admin.ch-ff2a6e5bb9.md", "Gilt nur für Gewinnsteuer (keine Kapitalsteuer beim Kanton)", 900, 300)
json.dump(S, open("data/claim-check/sources-20261014c.json","w"), ensure_ascii=False, indent=1)

C = [
 {"id":"c-qst-frist3","origin":"draft","source":"estv_quelle","file":"quellensteuer-nov-zusatzabzuege.html","claim":"Quellensteuerpflichtige mit Wohnsitz oder Aufenthalt in der Schweiz können bis am 31. März des Folgejahres einen Antrag auf nachträgliche ordentliche Veranlagung einreichen."},
 {"id":"c-ks-ur3","origin":"draft","source":"estv_steuerfuss","file":"kapitalsteuer-ag-gmbh.html","claim":"Im Kanton Uri gilt der Steuerfuss nur für die Gewinnsteuer; eine Kapitalsteuer beim Kanton gibt es nicht."},
 {"id":"c-ks-ur4","origin":"draft","source":"estv_steuerfuss","file":"kapitalsteuer-ag-gmbh.html","claim":"Die Urner Gemeinden erheben Kapitalsteuern mit proportionalen Sätzen zwischen 0,01 Promille und 4,0 Promille."},
]
json.dump(C, open("data/claim-check/claims-20261014c.json","w"), ensure_ascii=False, indent=1)
print("ok", {k: len(v) for k,v in S.items()})
