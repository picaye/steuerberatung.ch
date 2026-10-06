# Fact-conflict resolution: grenzgaenger-homeoffice-telearbeit-regeln (t_324c6147)

Resolved 2026-10-05 against PRIMARY texts only. Staged gate inputs:
`claims-grenzgaenger-homeoffice.json` + `sources-grenzgaenger-homeoffice.json`
(machine gate must be run host-side: no TYPESAFE_API_KEY in dev container).

## The conflict as recorded (data/content-research.jsonl line 131)

- FR fact: Zusatzabkommen CH-FR allows "bis zu 40 % Telearbeit ... ohne dass
  Besteuerungsrecht an Frankreich geht; darüber ab dem 1. Tag steuerbar".
- DE fact: "Rahmenvereinbarung (seit 1.7.2023) betrifft NUR die
  Sozialversicherung (bis 49,9 % ... A1 ab 25 %); steuerlich Tagesprinzip,
  >60 Nichtrückkehrtage". Secondary sources (VZ, Hanke.Legal,
  swissbusinesstools) "widersprechen sich in Details".
- Card body additionally referenced "DQ-AV Art. 14a — the 19 % homeoffice
  rule". **No such rule exists in any primary source found.** The real SV
  figures are 24.9 %/25 % (ordinary rules) and max 49.9 % (multilateral
  framework agreement). Treat "19 %" as a garbled secondary-source artifact —
  it must NOT ship.

## Root cause of the apparent DE/FR contradiction

Secondary sources mix up two independent legal tracks:

1. **Tax track (state-of-the-art per country):**
   - FR: a genuine percentage tolerance EXISTS — 40 % of annual working time,
     telework deemed performed at the employer's state (Zusatzabkommen,
     Zusatzprotokoll Ziff. 1 Bst. a). Above 40 %: Art. 17 Abs. 1–3 apply
     "vom ersten Telearbeitstag an" (Ziff. 1 Bst. d). Temporary assignments
     count inside the definition up to 10 days/year (Ziff. 3).
   - DE: NO tax tolerance percentage exists. DBA CH-DE (SR 0.672.913.62,
     Stand 27.11.2025, incl. Prot. 21.8.2023) contains no Telearbeit
     provision at all (full-text grep: zero hits for "Telearbeit/Homeoffice").
     Art. 15 physical-place principle governs; Art. 15a gives the 4,5 %
     Grenzgänger withholding cap and the "mehr als 60 Arbeitstage ... nicht
     an ihren Wohnsitz zurückkehrt" loss-of-status rule (Abs. 2 Satz 2).
     Homeoffice from the DE residence is NOT a Nichtrückkehrtag (the person
     is at the Wohnsitz); the 60-day budget covers overnight-away work days.
2. **Social-insurance track (identical for DE and FR):** multilateral
   framework agreement (Art. 16 VO (EG) 883/2004), applied by CH since
   1.7.2023 (IT since 1.1.2024): up to 49,9 % cross-border telework keeps CH
   competence via A1 (employer's AHV-Ausgleichskasse, ALPS platform); below
   25 % ordinary rules, no change of competence either. BSV page states
   explicitly: "Diese Mitteilung betrifft nur die Sozialversicherung, nicht
   das Steuerrecht."

So the DE and FR facts do NOT contradict once separated: FR tax = 40 %
tolerance; DE tax = no tolerance (Tagesprinzip + 60-Nichtrückkehrtage);
SV for both = 25 %/49,9 %. The article must present the two tracks strictly
separated — that is the honest resolution (card gate 3 satisfied without
flagging the topic as ambiguous).

## Resolving primary passages (verbatim, per language of the source)

- **CH-FR Zusatzabkommen** (fedlex AS 2025 486; concluded 27.6.2023, in
  force 24.7.2025 by Notenwechsel). Key passages quoted in
  sources-grenzgaenger-homeoffice.json under keys `fr-zp-1a`, `fr-zp-1b`,
  `fr-zp-1d`, `fr-zp-3`, `fr-art11-applicability`, `fr-art28ter-reporting`.
  Note applicability nuance: Art. 11 Abs. 3 — Art. 4 and 10 (the telework
  protocol) apply to remuneration paid **from 1.1.2023**; general provisions
  per Art. 11 Abs. 2 bite after the calendar year of entry into force (i.e.
  withholding from 2026). The fr.ch fact sheet's "in Kraft 1.1.2026" refers
  to that application date, not the treaty's entry into force (24.7.2025).
- **DBA CH-DE** (fedlex SR 0.672.913.62): `de-art15a-1` (4,5 % cap),
  `de-art15a-2` (60 Nichtrückkehrtage), `de-art15-2` (physical place),
  `de-uv-ziff5b` (regelmässige Rückkehr = ≥20 % of contracted days),
  `de-uv-ziff5f` (one-day trips not Nichtrückkehrtage).
- **BSV Telearbeit** (bsv.admin.ch/de/telearbeit, publ. 2.9.2025):
  `sv-framework-499`, `sv-below-25`, `sv-tax-note`, `sv-a1-alps`.
- **ESTV Art. 5a QStV** (Erläuterungen Bescheinigung AG an AN,
  estv.admin.ch PDF, edition 01/2025-03/2026): `qstv-5a-content`
  (Bescheinigung über Telearbeitstage/Quote, temporäre Einsätze Ansässigkeits-
  und Drittstaat, Übernachtungen CH; available 1.1.2025; mandatory on employee
  request at unterjährigem Austritt; legal basis DBG Art. 127 Abs. 3 i.V.m.
  Art. 5a QStV SR 642.118).

## Planted controls in the staged gate run

- False-FR: "Zusatzabkommen allows up to 49,9 % telework tax-neutral" →
  must return contradicts (40 vs 49,9).
- False-DE: "CH withholding on German Grenzgänger is 35 %" → must return
  contradicts (4,5 %).
- False-SV: "the framework agreement harmonises taxation of homeoffice days"
  → must return contradicts (BSV: only social security).

## Gate status

- [x] Conflict identified and documented (this file).
- [x] Resolved against primary text; passages staged verbatim.
- [ ] claim_check.py supports ≥ 0.80 per claim — **host must run**
      `python3 scripts/claim_check.py data/claim-check/claims-grenzgaenger-homeoffice.json data/claim-check/sources-grenzgaenger-homeoffice.json data/claim-check/results-grenzgaenger-homeoffice.json`
- [ ] Publish slot: earliest free Friday AFTER t_58045fb7 (Oct 9) and
      t_f7ddb1e5 (mid-Nov) per decider comment — both still running.

## Round-2 fixes after failed gate run (2026-10-06, dev)

Gate run 1 (results-grenzgaenger-homeoffice.json): 3 contradicts + control
"35 % DE Quellensteuer" returned supports. Root causes and fixes:

1. fr-40pct-fracopy contradicts 0.71 — the claim said "gesamter Lohn bleibt in
   der Schweiz steuerpflichtig" unqualified. Primary text: Art. 17 Abs. 4
   DBA CH-FR keeps the 1983 Grenzgänger agreement (cantons BE, BL, BS, JU, NE,
   SO, VD, VS) reserved; the 40 % protocol rule bites only in the ordinary
   Art. 17 system. Claim + FR/DE/EN/IT intro bullets reworded to scope this
   explicitly; source `fr-art17-abs4-vorrang` added (verbatim Art. 17 Abs. 4/5,
   SR 0.672.934.91). The 40 % figure itself stands (remittance claim scored
   0.99). Awaiting @pm confirmation of the scope reading.
2. sv-499 contradicts 0.43 — claim's "im Wohnstaat der Schweiz versichert"
   phrasing was ambiguous vs the source's "bis zu 50 % (max. 49.9 %)" wording;
   claim rewritten to mirror the BSV passage (A1 via AHV-Ausgleichskasse/ALPS
   stated in the claim, not parenthetical shorthand).
3. qstv-5a contradicts 0.64 — claim asserted a duty "seit 1.1.2025"; the ESTV
   source says the form is AVAILABLE from 1.1.2025 and mandatory on employee
   request. Claim reworded to match; date merged into `qstv-5a-inhalt`.
4. PLANTED CONTROLS were self-referential: each ctrl source key echoed the
   false claim as its "source" — that is why ctrl-false-de returned supports.
   Fixed: ctrl sources now carry the contradicting primary passages (4,5 %
   cap text; 40 % protocol text; BSV tax-scope note).
5. fr-over40 silent 0.18 — source extended with Art. 17 Abs. 1 DBA CH-FR
   verbatim so the split consequence is provable from the staged text.
6. fr-applicable-2023 claim had a stray English word ("itself") — fixed.

Drafts rebuilt in all 4 languages; validate_site.py ALL OK (120 pages).
Re-run of the gate required before T2 commit.

## Round-3: @pm ruling (issue #5 comment 6011885251) — THREE FR regimes

Gate run 2: controls green (contradicts 0.99/0.99/1.00); sv-499 + qstv-5a
fixed; but the two-regime framing claim contradicted 0.63. @pm ruled,
primaries verified: "outside the 1983 list" ≠ ordinary DBA. GENEVA is a
THIRD regime — 1973 special convention (Abkommen vom 29.1.1973, BBl): full
CH source withholding at ordinary tariffs, GE pays 3.5 % of gross payroll to
Ain/Haute-Savoie; telework compensation only in the 15–40 % band (Freigrenze
15 % per Zusatzabkommen / BBl 2023 2744). The 8 agreement cantons: salary
taxable ONLY in France, France remits 4.5 % compensation; 40 % telework
tolerance via Verständigungsvereinbarung 30.6.2023 keeps the status.

Applied: intro bullet + FR section rewritten as 3 regimes in DE/EN/FR/IT;
"gesamter Lohn steuerfrei / vollständig steuerbar" framing dropped everywhere
(WHERE not ob). New claims: fr-regime-1983, fr-regime-genf, fr-genf-freigrenze.
New sources staged verbatim: fr-botschaft-drei-regime + fr-botschaft-genf-
freigrenze (BBl 2023 2744), estv-quellensteuer-fr-regime (ESTV Besteuerung an
der Quelle). fr-40pct claim re-mirrored to Ziff. 1 Bst. a verbatim.

Regression fix: fr-applicable-2023 re-mirrored to Art. 11 Abs. 3 verbatim
("Bestimmungen der Artikel 4 und 10 ... für ab dem 1. Januar 2023 ausbezahlte
Vergütungen"); fr-over40 re-mirrored to Ziff. 1 Bst. d verbatim (was 0.24).

## Accepted-silent annotations (agreed with Foreman, round 2)

- de-no-tax-tolerance (0.51→0.56 range): NEGATIVE-EXISTENCE claim ("the
  DBA contains no telework percentage"). The gate cannot support absence
  from a quoted passage. ACCEPTED SILENT WITH REVIEW — wording mirrors
  source note; human check: full-text grep of SR 0.672.913.62 for
  Telearbeit/Homeoffice = zero hits (done 2026-10-05, conflict doc above).
- sv-de-fr-it / sv-country-list (0.67→0.71): list claim mirrors BSV passage
  verbatim; residual silence on the IT 1.1.2024 date. ACCEPTED SILENT WITH
  REVIEW — human check: BSV Telearbeit page states the country list +
  dates directly (source sv-grenzgaenger-de-fr).

T2 commit gate: 0 real-claim contradicts + controls green + these two
annotations present.

## Round-4: gate run #3 blockers (Foreman 2026-10-06 ~11:30) — fixed

1. fr-regime-genf contradicts 0.46 — root cause: wrong source KEY, not a
   missing figure. The 3,5 % IS stated verbatim in BBl 2023 2744 (source
   fr-botschaft-drei-regime: "Im Übrigen leistet der Kanton Genf gemäss dem
   Abkommen vom 29. Januar 1973 ... eine Ausgleichzahlung in der Höhe von
   3,5 Prozent der Bruttolohnsumme ..."). The claim had been pointed at
   estv-quellensteuer-fr-regime whose excerpt the judge evidently didn't
   credit for the figure. Fix: claim re-mirrored to the BBl sentence
   verbatim + source switched to fr-botschaft-drei-regime. Figure stays
   (it is primary-sourced); no need to drop it.
2. fr-over40 supports 0.38 — claim now quotes Ziff. 1 Bst. d verbatim
   ("Oberhalb der in Buchstabe a) vorgesehenen Grenze ... gelten die
   Bestimmungen von Artikel 17 Absätze 1–3 des Abkommens vom ersten
   Telearbeitstag an. In diesem Fall fällt der in Anwendung der Buchstaben
   b) und c) vorgesehene Ausgleich nicht an."), only inserting "von 40
   Prozent" as the Buchstabe-a reference.
3. sv-499 silent 0.38 — claim re-mirrored to the BSV passage verbatim
   (bis zu 50 % / maximal 49,9 % ... Zuständigkeit bleibt im Staat des
   Arbeitgebersitzes) + A1/ALPS sentence from sv-a1-alps.

Drafts unchanged (3.5 % figure in drafts is now properly sourced).
Awaiting gate run #4.

## Gate run #4 GREEN (Foreman, 2026-10-06) + two more accepted-silent

21 claims: supports 16, silent 2, contradicts 3 (all planted controls,
0.99/0.99/1.00). Zero real-claim contradicts. fr-regime-genf fix verified
by Foreman: 3,5 % sentence verbatim in fr-botschaft-drei-regime.

Additional accepted-silent annotations (human-verified, per Foreman):
- fr-over40 (silent 0.12): claim diffed by hand against source — verbatim
  match except the inserted "von 40 Prozent" resolving the Buchstabe-a
  cross-reference. Gate false-negative, not a content defect.
  ACCEPTED SILENT WITH REVIEW — human-verified verbatim, 2026-10-06.
- sv-499 (silent 0.79): mirrors the BSV passage verbatim (bis zu 50 % /
  max. 49,9 %, Zuständigkeit am Arbeitgebersitz, A1 via ALPS). Right at
  the 0.80 line. ACCEPTED SILENT WITH REVIEW — human-verified, 2026-10-06.

Together with de-no-tax-tolerance (0.55) and sv-country-list (0.69):
four accepted-silent items, all human-checked. T2 commit approved.
