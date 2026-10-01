# Steuerrechner: Takedown (2026-09-16) und Neuaufbau (2026-10-01)

## Status: WIEDER ONLINE (2026-10-01), neu aufgebaut und getestet

Der alte Rechner (linearer Rate-Satz, `CANTONS base/top/threshold` in app.js)
lieferte falsche Zahlen und wurde am 2026-09-16 offline genommen
(Takedown: commit 9f6a625).

## Was jetzt anders ist

- **Bundessteuer: exakter Gesetzestarif 2026** (Art. 36 DBG, SR 642.11,
  Stand 1.1.2026 via fedlex; gegen ESTV Form. 58c 2026 tabellarisch abgeglichen —
  PDF-Kopie: ur.ch/_docn/439286). Stufenweise pro 100-Franken-Schritt,
  Integer-Cent-Arithmetik, Freibeträge (15'200/29'700), Minimum 25 Fr.,
  11.5 %-Deckel, Kinder-Credit 263 Fr. (Abs. 2bis).
- **Kanton+Gemeinde: publizierte Durchschnittssteuersätze 2026** je
  Kantonshauptort (taxbooks.ch "Einkommenssteuerbelastung in den Kantonen"
  V1.1/2026, Dr.-Tax-Basis; ohne Kirchensteuer; gegen KPMG Clarity 2026
  Grenzsätze geordnet plausibilisiert). Kantonsanteil = Tabellenwert minus
  exakter Bundesanteil an den Ankern 75k/150k/300k, linear interpoliert.
- **Engine:** `scripts/tax_engine.js` (= `assets/tax_engine.js`, identisch).
- **Test-Gate:** `node scripts/test_tax_engine.js` — 290 Assertions
  (alle 132 Form-58c-Zeilen beider Tarife, Anker-Nullband, 26 Kantone ×
  3 Anker × ledig/verheiratet ±0.05 pp, Monotonie, ZG<GE, Kinder-Credit).
  Stand 2026-10-01: **290 passed, 0 failed.**

## Grenzen (im Disclaimer genannt)

- Schätzung gilt für den Kantonshauptort; Gemeinden abweichen deutlich.
- Pauschalabzüge nach DBG-Sozialabzügen (Berufskosten 4%/2'400–4'400,
  Versicherung 1'800/2'800, Ehe 2'800, Kinder 6'800); kantonale Abzüge
  unterscheiden sich — darum "Schätzung", nie "Steuerberatung".
- Kinder-Credit nur auf der Bundessteuer; kirchliche Steuer nicht enthalten.

## Links

Nav + Footer "Rechner" wurden auf allen Seiten wiederhergestellt
(Takedown-Schritt 5 rückgängig). rechner.html ist wieder indexierbar
(kein noindex mehr).

## Rückfall-Procedure

Falls Zahlen beanstandet werden: `node scripts/test_tax_engine.js` zuerst —
grün heisst: Tarif-Treue gegeben, Problem ist Datenaktualität (neue
Kantons-tabellen jeden Januar: taxbooks 127 / ESTV Form. 58c).
