# AGENTS.md — steuerberatung.ch

Static multilingual site (DE root, `en/`, `fr/`, `it/`) on GitHub Pages via
Actions, edge on Cloudflare. Lead-gen calculator + articles. Workers: dev,
qa, decider.

## Layout
- 18+ DE articles at root; translations mirrored under `en/ fr/ it/`.
- `rechner.html` (+ locale copies) = tax calculator v3: official ESTV engine
  proxied through `lead.steuerberatung.ch/api/tax`; offline fallback
  `scripts/tax_engine.js` + `assets/tax_engine_data.js`, always labeled with a
  mode badge.
- `scripts/lead_server.py` (VERSION 3) runs under launchd on this Mac,
  supervised tunnel to `lead.steuerberatung.ch`. Leads append to
  `data/leads.jsonl`.
- `assets/locations.js` is GENERATED — edit `scripts/gen_locations.py`, never
  the output.

## Gates (run before pushing; all must be green)
- `python3 scripts/validate_site.py` — broken links, cross-language leakage.
- `node scripts/test_tax_engine.js` — 290-assertion engine test.
- `python3 scripts/claim_check.py` — every published tax figure checked
  against the official source text (TypeSafe). No figure ships unchecked.

## Conventions
- New DE article: use `scripts/article_template.py` — it auto-injects the
  RELATED block from `scripts/related_map.json` (DE only; FR/IT/EN stay None).
- After publishing: `python3 scripts/indexnow_ping.py` (non-fatal by design).
- Sitemap: regenerate with `scripts/mksitemap.py`.
- ESTV fixtures refresh each January: `scripts/fetch_estv_fixtures.py 2027`
  then regenerate locations.
- Cache busting: bump `?v=N` on app.js/locations.js/extra.css in all four
  rechner pages — the deploy's Cloudflare purge step is skipped (token lacks
  Cache Purge grant) until Pino fixes it.

## Never
- Never call the ESTV API from the browser; go through `/api/tax`.
- Never `git add -A` — `data/` and `.hermes-patches/` are deliberately
  untracked; stage targeted paths only.
- Never edit another locale's article from a DE-only task; FR/IT/EN mirror
  changes go through their own translation pass.
- Never claim "live" without curling https://steuerberatung.ch/<page> after
  the Actions deploy finishes.
