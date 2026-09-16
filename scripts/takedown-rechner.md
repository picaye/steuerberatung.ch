# Steuerrechner abgeschaltet (2026-09-16)

## Warum

Der Rechner auf `rechner.html` hat falsche Zahlen geliefert. Falsche
Steuerzahlen sind schlimmer als keine — sie führen zu falschen
Entscheidungen bei echten Steuerrechnungen. Deshalb: offline, bis er
nachweislich korrekt rechnet.

## Was gemacht wurde

- `rechner.html` (+ `en/`, `fr/`, `it/`) → Redirect-Stub mit Erklärung
  (2s), `noindex, follow`, canonical auf den jeweiligen Ratgeber.
  Die URL bleibt gültig, niemand landet auf einer 404.
- 136 Links, die auf den Rechner zeigten, umgebogen auf den Ratgeber
  derselben Sprache.
- 68 Beschriftungen und Klauseln korrigiert, die den Rechner als
  nutzbares Angebot nannten (Fusszeilen, AGB-Gratisklausel,
  Meta-Descriptions, Startseiten-Kacheln, Hero-CTAs, Tipps-Absätze).
- Originale liegen unter `scripts/backup/`:
  `rechner.html`, `en_rechner.html`, `fr_rechner.html`, `it_rechner.html`.

## Wie er zurückkommt

1. Ursache der falschen Werte finden und beheben.
2. Rechnen gegen geprüfte Fälle testen — mindestens:
   - Bundessteuer + Kantonssteuer für 2-3 Kantone mit bekanntem Ergebnis
   - Abzüge: Säule 3a, Berufskosten, Kinderabzug, Doppelverdiener
   - Grenzfälle: tiefes Einkommen, hohes Einkommen, Verheiratete/Alleinstehende
3. Erst wenn die Tests stimmen: Stub durch `scripts/backup/rechner.html`
   ersetzen, Sprache für Sprache.
4. Redirect, `noindex` und canonical entfernen.
5. Links/Beschriftungen wieder auf `rechner.html` zeigen lassen —
   die Änderung oben ist rückwärts zu wiederholen.

Nicht zurückbringen, solange die Testfälle nicht sauber durchlaufen.
