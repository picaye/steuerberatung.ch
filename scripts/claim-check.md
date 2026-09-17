# Steuerzahlen prüfen, bevor sie publiziert werden

## Warum

Am 16.09.2026 wurde der Steuerrechner abgeschaltet, weil er falsche Zahlen
geliefert hat. Falsche Steuerzahlen sind schlimmer als keine: sie führen zu
falschen Entscheidungen bei echten Steuererklärungen.

`scripts/claim_check.py` prüft jede veröffentlichte Zahl gegen den Wortlaut des
amtlichen Dokuments, auf das sie sich beruft. Der Prüfer hat bei seinem ersten
Einsatz am 17.09.2026 drei echte Fehler in `data/content-research.jsonl`
gefunden, davon zwei in `meta`-Feldern, die direkt publiziert werden.

## Aufbau

Nach dem Muster aus dem TypeSafe-Cookbook „Double-checking citations":

1. **Code sucht die Stelle** — deterministisch, kein Modell. Fällt die Quelle,
   kommt `no_source` heraus, kein Urteil.
2. **Eine Choice-Frage pro Behauptung** — stützt / widerspricht / sagt nichts /
   unbrauchbar. Die Frage beurteilt nur, was in der Quellstelle wirklich steht,
   nicht was allgemein über Schweizer Steuerrecht bekannt ist.
3. **Confidence-Gate bei 0.80** — darüber gilt das Urteil, darunter schaut ein
   Mensch nach. Der Typ garantiert die Schnittstelle, nicht die Wahrheit.

## Aufruf

```bash
python3 -m pip install --user typesafe-sdk   # einmalig
python3 scripts/claim_check.py claims.json sources.json results.json
```

`claims.json`: `[{"id","claim","source","file","origin"}]`
`sources.json`: `{"<source-schlüssel>": "<Quelltext>"}`

Der Schlüssel wird aus `TYPESAFE_API_KEY` gelesen (`~/.hermes/.env`). Modell
`jev-latest`, überschreibbar per `TYPESAFE_DEFAULT_MODEL`.

## Regeln, die sich in der Praxis bestätigt haben

- **Eine Behauptung pro Aussage.** Eine Behauptung mit vier Teilaussagen kam auf
  Confidence 0.66 und wurde zu Recht zur Prüfung markiert. Aufteilen.
- **Quelltext, nicht Erinnerung.** Ohne hinterlegte Quelle gibt es kein Urteil.
- **Gegenkontrollen mitlaufen lassen.** Absichtlich falsche Behauptungen müssen
  als `contradicts` herauskommen — sonst prüft das Werkzeug nichts. Umgekehrt
  muss eine wahre Aussage `supports` ergeben, sonst lehnt es pauschal ab.
- **Nie eine Zahl ohne Quelle freigeben.** Das Gate ist der Mechanismus, nicht
  die Deko.

## Erster Einsatz (17.09.2026)

Geprüft: 21 Behauptungen (Website-Zahlen, Recherche-Fakten, 4 Kontrollen).

Gefundene und behobene Fehler:

| Stelle | Falsch | Richtig |
| --- | --- | --- |
| VSt 35 % | Art. 86 VStG | **Art. 13 VStG** (Steuersätze) |
| Grenzgänger 4,5 % | Art. 86 VStG | **Art. 15a DBA CH-DE** |
| Reduzierter MWST-Satz | 2,5 % | **2,6 %** (seit 1.1.2024) |
| Reduzierter Satz, Branchen | «Baugewerbe, Gastronomie» | Lebensmittel, Medikamente, Bücher; Gastronomie = **Normalsatz** (Art. 25 Abs. 3) |
| Grenzgänger-Frist | 60 Arbeitstage | **60 Nichtrückkehrtage** |

Ohne Beanstandung bestätigt: Säule 3a CHF 7'258 / 36'288, AHV-Mindestbeitrag
CHF 530, MWST-Schwelle CHF 100'000, VSt 35 %, Normalsatz 8,1 %.

## Noch offen

Nicht alle Einträge in `data/content-research.jsonl` sind geprüft. Einträge ohne
`verified_at` tragen ungeprüfte Zahlen. Besonders zu prüfen:

- `hypothek-steuerabzug-schweiz` — Schuldzinsabzug, Liegenschaftsunterhalt
- `verrechnungssteuer-schweiz-35-prozent` — Frist und Formularnummer
  («Formular 110 innert 30 Tagen», «Formular 25») sind noch nicht gegen die
  ESTV-Vorgabe geprüft
- `homeoffice-kosten-abziehen` — trägt den Vermerk
  «[Beträge gegen aktuelles ESTV-Merkblatt 2026 verifizieren]»
