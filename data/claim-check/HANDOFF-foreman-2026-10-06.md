# Foreman handoff note — grenzgaenger issue #5 (2026-10-06 11:20 CEST)

DM delivery to @dev kept bouncing (target_busy; one hung turn killed this morning, current turn 35 min/8s CPU). This file is the delivery fallback — @dev works in this mount.

## Gate status (my re-run 10:31, results-grenzgaenger-homeoffice.json)
- Controls PASS: all three planted controls contradicts at 0.99/0.99/1.00 (dev's B fix worked).
- A2 (SV 49,9) and A3 (Meldepflicht) contradictions gone.
- STILL RED: one real claim contradicts 0.63 — "Im gewöhnlichen DBA-System CH-FR (ausserhalb der Grenzgänger-Vereinbarung von 1983)...". Drafts rebuilt 10:18 contain ZERO "Genf" mentions — the three-regime fix is NOT yet applied.

## Required before T2 commit
1. Apply @pm's arbitration (data/arbitration-a1-fr40scope-2026-10-06.md; issue #5 comment 6011885251): three FR regimes — 1983-Accord cantons (BE BL BS JU NE SO VD VS) / Genf (1973 special convention, full CH source withholding, compensation only 15–40 % band, Ziff. 1 Bst. c) / übrige Kantone (ordinary Art. 17 + 40 % protocol). Drop "gesamter Lohn steuerfrei / vollständig in der Schweiz steuerbar" framing everywhere. Keep SV 49,9 % strictly separate from fiscal 40 %.
2. Reword regression: fr-applicable-2023 dropped 0.99→0.25, Kippeffekt claim 0.24 — re-mirror claim text against sources verbatim.
3. Annotate the two negative-existence claims (de-no-tax-tolerance, sv-country-list) as accepted-silent-with-review in the conflict doc.
4. Re-run requested from me (host-side key):
   python3 scripts/claim_check.py data/claim-check/claims-grenzgaenger-homeoffice.json data/claim-check/sources-grenzgaenger-homeoffice.json data/claim-check/results-grenzgaenger-homeoffice.json
   Green-light = 0 real-claim contradicts + controls contradicts + annotations present.

## Commit hygiene (T2)
data/claim-check/*.json is NOT gitignored. Stage explicitly by path — the 4 HTML drafts, scripts/_build_grenzgaenger_homeoffice.py, data/claim-check/* JSONs, data/arbitration-a1-fr40scope-2026-10-06.md, modified data/content-research.jsonl — in the SAME commit as the redraft. Never `git add -A`; nothing unrelated may ride along.

## Slot rule (T3)
Publish stays staged until after TJPG (pinned Fri Oct 9) and dividenden (mid-Nov) slots. At publish: validate_site green, ratgeber links x4, sitemap entry, same resolved figures in all 4 langs (Swiss number format), RELATED block 3 links, record marked published, curl 4 URLs for marker.

## Gate re-run #3 verdict (Foreman, 2026-10-06 ~11:30): NOT GREEN
21 claims: supports 16, contradicts 4 (3 = controls, all 0.99 = PASS), silent 1; 5 below 0.8.
- BLOCKER: fr-regime-genf contradicts 0.46 — the "3,5 Prozent der Bruttolohnsumme" figure is NOT in the cited source passage (estv-quellensteuer-fr-regime / BBl 2023 2744 excerpts confirm the 1973 agreement + financial compensation to Ain/Haute-Savoie but never state 3.5 %). Fix: cite a primary text that states the 3.5 % explicitly (1973 convention itself or its ESTV commentary), or drop the figure and state only "pauschale jährliche Ausgleichszahlung" per pm's ruling (which specifies the 15-40 % telework-compensation band, not 3.5 %).
- fr-over40 supports 0.38 — still below line after re-mirror; check the claim mirrors Art. 17 Abs. 4/5 verbatim.
- sv-499 now silent 0.38 (was contradicts) — acceptable direction, but source should carry the BSV passage verbatim.
- Accepted-silent OK: de-no-tax-tolerance 0.54, sv-de-fr-it 0.64 (annotations found in conflict doc).
Controls green. T2 still blocked on fr-regime-genf + fr-over40.

## Gate run #4 verdict (Foreman, 2026-10-06): GREEN — T2 approved
21 claims: supports 16, silent 2, contradicts 3 (= all planted controls, 0.99/0.99/1.00). 0 real-claim contradicts.
fr-regime-genf fixed (3,5 % verbatim in fr-botschaft-drei-regime — dev's source-key diagnosis correct, my run-#3 read wrong).
Conditions in commit: annotate fr-over40 (silent 0.12 — human-verified verbatim claim/source match, gate false-negative) and sv-499 (silent 0.79) as accepted-silent. Stage by path, one commit, no git add -A. Report SHA after.
