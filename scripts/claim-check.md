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

## Zweiter Einsatz: die fünf Artikel (17.09.2026)

18 Behauptungen aus den fünf neuen Artikeln gegen die amtlichen Normen geprüft.
Ergebnis: **14 von 14 inhaltlichen Aussagen `supports`** (0.79–1.00), keine
Faktenfehler in den Artikeln. Die drei mitlaufenden falschen Kontrollen kamen
alle als `contradicts` (0.97–1.00) heraus.

Geprüft wurden unter anderem: VSt-Sätze 35/15/8 % (Art. 13 VStG), VSt-Frist
3 Jahre (Art. 32 VStG), Grenzgänger 4,5 % und Gre-1 (Art. 15a DBA), 60
Nichtrückkehrtage, MWST-Schwelle 100'000 (Art. 10), 30-Tage-Anmeldung
(Art. 66), Sätze 8,1/2,6 % (Art. 25), Vereinsgrenze 250'000, AHV-Satz 10,0 %,
sinkende Skala 5,371 % ab CHF 10'100, Mindestbeitrag CHF 530, Schuldzinsenabzug
Art. 33 DBG (Vermögenserträge + CHF 50'000), Säule 3a 7'258/36'288.

### Grenze des Verfahrens: verneinende Aussagen

Eine Aussage der Form «X existiert nicht» lässt sich durch Zitat **nicht**
bestätigen. Die Behauptung «ein pauschaler 5 %-Zinsabzug existiert nicht»
kam folgerichtig als `silent` mit Confidence 0.370 zurück — Art. 33 DBG regelt,
was abziehbar ist, und sagt über erfundene Regeln nichts.

Solche Widerlegungen sind die riskanteste Klasse im Bestand: sie sind weder
durch Zitat zu belegen noch zu widerlegen, also auch nicht maschinell zu
sichern. Sie brauchen eine menschliche Entscheidung. Wer sie publiziert,
sollte die Quelle der Legende kennen — nicht nur wissen, dass die Regel fehlt.

### Weitere Beobachtung

Eine Behauptung mit vier Teilaussagen kam erneut auf 0.790 und rutschte knapp
unter das Gate. Das bestätigt die Regel: eine Aussage pro Behauptung.

## Quellenregel: nur amtliches Schweizer Recht

Für die Prüfung zählen ausschliesslich amtliche Schweizer Quellen:

- **fedlex.admin.ch** — Bundesrecht (SR-Nummern). Die `?print=true`-Variante
  liefert den Text serverseitig gerendert; ohne diesen Parameter kommt bei
  einigen Erlassen nur die JavaScript-Hülle zurück.
- **Amtliche Publikationen des Bundes**: ahv-iv.ch (Informationsstelle AHV/IV,
  herausgegeben mit dem BSV), ch.ch, estv.admin.ch.

Nicht als Quelle verwendet werden: kommerzielle Gesetzesportale, Anwalts- und
Beratungsartikel, ausländische Behörden (z. B. deutsche Finanzämter) sowie
deutsche Steuerliteratur.

**Völkerrechtliche Verträge sind Schweizer Recht.** Das DBA Schweiz-Deutschland
(SR 0.672.913.62) ist in der amtlichen Sammlung publiziert und damit zitierfähig
— für die Grenzgängerregelung des Art. 15a ist es die einzige massgebende Quelle.
Deutsches Steuerrecht (EStG) oder deutsche Behördenangaben sind es nicht.

### Warum diese Regel praktisch zählt

Der Grenzgänger-Artikel stützte sich zuerst auf einen Beratungsartikel, der von
«Nichtrückkehrtagen» sprach. Der amtliche Vertragstext sagt «an mehr als
60 Arbeitstagen». Beide Formulierungen passieren die Prüfung (0.98 bzw. 0.92),
aber nur die erste steht im Gesetz. Eine Korrektur, die den Gesetzeswortlaut
durch einen Praxisbegriff ersetzt, ist keine Verbesserung — sie entfernt die
Belegbarkeit.

## Noch offen

Nicht alle Einträge in `data/content-research.jsonl` sind geprüft. Einträge ohne
`verified_at` tragen ungeprüfte Zahlen. Besonders zu prüfen:

- `hypothek-steuerabzug-schweiz` — Schuldzinsabzug, Liegenschaftsunterhalt
- `verrechnungssteuer-schweiz-35-prozent` — Frist und Formularnummer
  («Formular 110 innert 30 Tagen», «Formular 25») sind noch nicht gegen die
  ESTV-Vorgabe geprüft
- `homeoffice-kosten-abziehen` — trägt den Vermerk
  «[Beträge gegen aktuelles ESTV-Merkblatt 2026 verifizieren]»
