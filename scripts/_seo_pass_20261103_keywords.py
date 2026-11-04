#!/usr/bin/env python3
"""On-page SEO pass for Pino's keyword task (todo 4701), 2026-11-03.
Evergreen titles, keyword-exact forms; datePublished/dateModified and visible
'Zuletzt aktualisiert' lines NOT touched (Pino rule: no date tricks).
Targets: verrechnungssteuer rückerstattung | 3a abzug rechner | liegenschaftskosten steuerabzug.
"""
import os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

misses = []
def patch_file(path, subs):
    p = os.path.join(BASE, path)
    s = open(p, encoding="utf-8").read()
    for old, new in subs:
        if old not in s:
            misses.append((path, old[:70]))
            continue
        s = s.replace(old, new, 1)
    open(p, "w", encoding="utf-8").write(s)
    print("patched:", path)

# ---- 1) Verrechnungssteuer 35% — exact keyword Rückerstattung / Refund / restitution / rimborso ----
patch_file("verrechnungssteuer-schweiz-35-prozent.html", [
 ('<title>Verrechnungssteuer 35 %: zurückholen | steuerberatung.ch</title>',
  '<title>Verrechnungssteuer 35 %: Rückerstattung | steuerberatung.ch</title>'),
 ('og:title" content="Verrechnungssteuer 35 %: zurückholen | steuerberatung.ch"',
  'og:title" content="Verrechnungssteuer 35 %: Rückerstattung | steuerberatung.ch"'),
 ('"headline": "Verrechnungssteuer 35 %: zurückholen"',
  '"headline": "Verrechnungssteuer 35 %: Rückerstattung"'),
 ('Rückholung via Steuererklärung – Frist 3 Jahre',
  'Rückerstattung via Steuererklärung – Frist 3 Jahre'),
 ('<h1>Verrechnungssteuer 35 %: Dividenden und Zinsen zurückholen</h1>',
  '<h1>Verrechnungssteuer 35 %: Rückerstattung von Dividenden und Zinsen</h1>'),
 ('<h2 id="s5">Frist: drei Jahre nach dem Fälligkeitsjahr</h2>',
  '<h2 id="s5">Rückerstattung: Frist drei Jahre nach dem Fälligkeitsjahr</h2>'),
 ('<a href="#s5">Frist: drei Jahre nach dem Fälligkeitsjahr</a>',
  '<a href="#s5">Rückerstattung: Frist drei Jahre nach dem Fälligkeitsjahr</a>'),
])
patch_file("en/verrechnungssteuer-schweiz-35-prozent.html", [
 ('<title>Withholding Tax 35 %: Reclaim | steuerberatung.ch</title>',
  '<title>Withholding Tax 35 %: Refund Guide | steuerberatung.ch</title>'),
 ('og:title" content="Withholding Tax 35 %: Reclaim | steuerberatung.ch"',
  'og:title" content="Withholding Tax 35 %: Refund Guide | steuerberatung.ch"'),
 ('"headline": "Withholding Tax 35 %: Reclaim"',
  '"headline": "Withholding Tax 35 %: Refund Guide"'),
 ('<h1>Withholding tax 35 %: Reclaiming your dividends and interest</h1>',
  '<h1>Withholding tax 35 %: refund of dividends and interest explained</h1>'),
])
patch_file("fr/verrechnungssteuer-schweiz-35-prozent.html", [
 ('<title>Impôt anticipé de 35 % : récupérer | steuerberatung.ch</title>',
  '<title>Impôt anticipé de 35 % : restitution | steuerberatung.ch</title>'),
 ('og:title" content="Impôt anticipé de 35 % : récupérer | steuerberatung.ch"',
  'og:title" content="Impôt anticipé de 35 % : restitution | steuerberatung.ch"'),
 ('"headline": "Impôt anticipé de 35 % : récupérer"',
  '"headline": "Impôt anticipé de 35 % : restitution"'),
 ('<h1>Impôt anticipé de 35 % : récupérer vos dividendes et intérêts</h1>',
  '<h1>Impôt anticipé de 35 % : la restitution de vos dividendes et intérêts</h1>'),
])
patch_file("it/verrechnungssteuer-schweiz-35-prozent.html", [
 ('<title>Imposta preventiva 35 %: recuperare | steuerberatung.ch</title>',
  '<title>Imposta preventiva 35 %: rimborso | steuerberatung.ch</title>'),
 ('og:title" content="Imposta preventiva 35 %: recuperare | steuerberatung.ch"',
  'og:title" content="Imposta preventiva 35 %: rimborso | steuerberatung.ch"'),
 ('"headline": "Imposta preventiva 35 %: recuperare"',
  '"headline": "Imposta preventiva 35 %: rimborso"'),
 ('<h1>Imposta preventiva del 35 %: recuperare dividendi e interessi</h1>',
  '<h1>Imposta preventiva del 35 %: il rimborso di dividendi e interessi</h1>'),
])

# ---- 2) 3a-rechner — evergreen title + Abzug/Deduction keyword (year stays in body only) ----
patch_file("3a-rechner.html", [
 ('<title>Säule-3a-Rechner 2026 | steuerberatung.ch</title>',
  '<title>Säule-3a-Rechner: 3a-Abzug berechnen | steuerberatung.ch</title>'),
 ('og:title" content="Säule-3a-Rechner 2026 | steuerberatung.ch"',
  'og:title" content="Säule-3a-Rechner: 3a-Abzug berechnen | steuerberatung.ch"'),
 ('content="Säule-3a-Rechner 2026: echte Steuerersparnis Ihres 3a-Beitrags',
  'content="Säule-3a-Rechner: den 3a-Abzug und die echte Steuerersparnis Ihres Beitrags'),
])
patch_file("en/3a-rechner.html", [
 ('<title>Pillar 3a Calculator 2026 | steuerberatung.ch</title>',
  '<title>Pillar 3a Calculator: Deduction &amp; Saving | steuerberatung.ch</title>'),
 ('og:title" content="Pillar 3a Calculator 2026 | steuerberatung.ch"',
  'og:title" content="Pillar 3a Calculator: Deduction & Saving | steuerberatung.ch"'),
 ('content="Pillar 3a savings calculator 2026: the real tax saving',
  content_marker := 'content="Pillar 3a deduction calculator: the real tax saving'),
])
patch_file("fr/3a-rechner.html", [
 ('<title>Calculateur pilier 3a 2026 | steuerberatung.ch</title>',
  '<title>Calculateur pilier 3a : déduction | steuerberatung.ch</title>'),
 ('og:title" content="Calculateur pilier 3a 2026 | steuerberatung.ch"',
  'og:title" content="Calculateur pilier 3a : déduction | steuerberatung.ch"'),
 ("content=\"Calculateur d'épargne pilier 3a 2026 : l'économie d'impôt réelle",
  "content=\"Calculateur de déduction pilier 3a : l'économie d'impôt réelle"),
])
patch_file("it/3a-rechner.html", [
 ('<title>Calcolatore pilastro 3a 2026 | steuerberatung.ch</title>',
  '<title>Calcolatore pilastro 3a: detrazione | steuerberatung.ch</title>'),
 ('og:title" content="Calcolatore pilastro 3a 2026 | steuerberatung.ch"',
  'og:title" content="Calcolatore pilastro 3a: detrazione | steuerberatung.ch"'),
 ('content="Calcolatore di risparmio pilastro 3a 2026: il reale risparmio',
  'content="Calcolatore di detrazione pilastro 3a: il reale risparmio'),
])

# ---- 3) hypothek — Liegenschaftskosten keyword (DBG Art. 9 Bst. c Unterhaltskosten) ----
patch_file("hypothek-steuerabzug-schweiz.html", [
 ('<title>Hypothek und Steuern: Zinsen abziehen | steuerberatung.ch</title>',
  '<title>Hypothek und Liegenschaftskosten: Abzüge | steuerberatung.ch</title>'),
 ('og:title" content="Hypothek und Steuern: Zinsen abziehen | steuerberatung.ch"',
  'og:title" content="Hypothek und Liegenschaftskosten: Abzüge | steuerberatung.ch"'),
 ('"headline": "Hypothek und Steuern: Zinsen abziehen"',
  '"headline": "Hypothek und Liegenschaftskosten: Abzüge"'),
 ('<h1>Hypothek und Steuern: Zinsen, Abzug und Grenzen richtig verstehen</h1>',
  '<h1>Hypothek und Liegenschaftskosten: Zinsen, Unterhalt und Grenzen verstehen</h1>'),
 ('vor allem die Hypothekarzinsen, den Unterhalt und die Beiträge an Energiespar- und Schutzmassnahmen',
  'vor allem die Hypothekarzinsen sowie die weiteren abziehbaren Liegenschaftskosten: Unterhalt und Beiträge an Energiespar- und Schutzmassnahmen'),
])
patch_file("en/hypothek-steuerabzug-schweiz.html", [
 ('<title>Mortgage and Taxes: Interest Deductions | steuerberatung.ch</title>',
  '<title>Mortgage and Property Costs: Deductions | steuerberatung.ch</title>'),
 ('og:title" content="Mortgage and Taxes: Interest Deductions | steuerberatung.ch"',
  'og:title" content="Mortgage and Property Costs: Deductions | steuerberatung.ch"'),
 ('"headline": "Mortgage and Taxes: Interest Deductions"',
  '"headline": "Mortgage and Property Costs: Deductions"'),
 ('<h1>Mortgage and taxes: interest, deductions and limits explained</h1>',
  '<h1>Mortgage and property costs: interest, deductions and limits explained</h1>'),
 ('above all mortgage interest, maintenance, and contributions to energy-saving and protective measures',
  'above all mortgage interest and further deductible property costs: maintenance and contributions to energy-saving and protective measures'),
])
patch_file("fr/hypothek-steuerabzug-schweiz.html", [
 ('<title>Hypothèque et impôts : intérêts | steuerberatung.ch</title>',
  '<title>Hypothèque et frais immobiliers : déductions | steuerberatung.ch</title>'),
 ('og:title" content="Hypothèque et impôts : intérêts | steuerberatung.ch"',
  'og:title" content="Hypothèque et frais immobiliers : déductions | steuerberatung.ch"'),
 ('"headline": "Hypothèque et impôts : intérêts"',
  '"headline": "Hypothèque et frais immobiliers : déductions"'),
 ('<h1>Hypothèque et impôts : intérêts, déduction et limites</h1>',
  '<h1>Hypothèque et frais immobiliers : intérêts, déduction et limites</h1>'),
 ("avant tout les intérêts hypothécaires, l'entretien et les contributions aux économies d'énergie et de protection",
  "avant tout les intérêts hypothécaires et les autres frais immobiliers déductibles : entretien et contributions aux économies d'énergie et de protection"),
])
patch_file("it/hypothek-steuerabzug-schweiz.html", [
 ('<title>Mutuo e imposte: interessi | steuerberatung.ch</title>',
  '<title>Mutuo e spese della proprietà: deduzioni | steuerberatung.ch</title>'),
 ('og:title" content="Mutuo e imposte: interessi | steuerberatung.ch"',
  'og:title" content="Mutuo e spese della proprietà: deduzioni | steuerberatung.ch"'),
 ('"headline": "Mutuo e imposte: interessi"',
  '"headline": "Mutuo e spese della proprietà: deduzioni"'),
 ('<h1>Mutuo e imposte: interessi, deduzioni e limiti</h1>',
  '<h1>Mutuo e spese della proprietà: interessi, deduzioni e limiti</h1>'),
 ('soprattutto gli interessi ipotecari, la manutenzione e i contributi per risparmio energetico e protezione',
  "soprattutto gli interessi ipotecari e le ulteriori spese della proprietà deducibili: manutenzione e contributi per il risparmio energetico e la protezione"),
])

print("MISSES:", len(misses))
for m in misses: print("  ", m)
sys.exit(1 if misses else 0)
