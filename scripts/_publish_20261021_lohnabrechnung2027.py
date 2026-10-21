#!/usr/bin/env python3
"""Lohnabrechnung 2027: neue AHV/IV/EO-Beitragswerte (Arbeitgeber-/Payroll-Seite). DE/EN/FR/IT.

Slug: lohnabrechnung-2027-ahv-iv-eo-neue-werte
Card: data/content-research.jsonl, run 2026-10-21 (pin-2026-11-30, high demand).
Angle: employer/payroll side of the 1.1.2027 adjustment — distinct intent from the live
ahv-rentenerhoehung-2027-neue-betraege (pensioner side, cross-linked, not duplicated).

Sources (all primary, curl-200 verified 2026-10-21):
- Fedlex AS 2026 542: Verordnung vom 2.10.2026 über Anpassungen an die Lohn- und
  Preisentwicklung bei der AHV/IV/EO ab 2027 (Mindestbeitrag 541 = 444+71+26, Skala
  10'300–61'500, Minimalrente 1'280, EO-Kappen 275/220 unverändert, Inkrafttreten 1.1.2027)
- BSV Medienmitteilung 2.10.2026 «AHV/IV-Minimalrente steigt um 20 Franken» (+1,59 %,
  BVG-Grenzbeträge 23'040/26'880, 3a 7'373/36'864)
- Fedlex AS 2026 547: BVV-2-Änderung vom 2.10.2026 (22'680→23'040, 26'460→26'880,
  90'720→92'160, 3'780→3'840)
- BSV Beitragstabellen SE/NE 318.114 v14, gültig ab 1.1.2027 (publ. 7.10.2026):
  Mindestbeitrag 541/45.10, Maximalbeitrag NE 27'050, Vermögensgrenzen 360'000/9'160'000,
  tiefster Skalasatz 5.371 %, Freibetrag Referenzalter 16'800
- BSV Dok. 6141 «Berechnung der Beiträge und Einträge ins IK», gültig ab 1.1.2027
  (Änderungen 2026→2027: 10'100→10'300, 60'500→61'500, 530→541, 1'010→1'030,
  Vermögensgrenzen 350'000→360'000, 1'750'000→1'760'000, 8'950'000→9'160'000)
- BSV Synoptische Tabelle Beitrags- und Prämiensätze, Stand 1.1.2026 (Sätze 4,35/0,7/0,25
  je Seite = 5,3 %; ALV 1,1 % bis 148'200; FamZ-Arbeitgeber 1,025–2,75 %)
- BSV «Beiträge im Überblick» (Total AHV/IV/EO 5,3 % + 5,3 %)
- Merkblatt 2.04 der AHV-Ausgleichskassen (Bagatellgrenze 2'500 pro Arbeitgeber/Kalenderjahr)

NOT yet official at time of writing (labelled «offen/Stand heute» in the text):
- 2027er Beitragstabellen für Arbeitnehmende/Arbeitgebende (318.110) — publiziert i.d.R. Q4
- ALV-Beitragssätze 2027 (separate Verordnung; Stand heute 1,1 % / 148'200 unverändert)
- Deckel massgebendes Jahreseinkommen 307'200 = abgeleitet (AHVG Art. 23: Tabellengrenze
  30'720 = 12 × Maximalrente 2'560; 1/10-Regel darüber; Rückerstattung über 10×)
"""
import sys, os, json, re, html as htmllib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from article_template import build

BASE = os.path.dirname(HERE)
SLUG = "lohnabrechnung-2027-ahv-iv-eo-neue-werte"
RELATED = ["ahv-rentenerhoehung-2027-neue-betraege.html",
           "minijobs-lohnschwelle-ahv-pflicht.html",
           "ahv-mindestbeitrag-selbststaendige.html"]

SRC = {
    "fedlex542": "https://www.fedlex.admin.ch/eli/oc/2026/542/de",
    "fedlex547": "https://www.fedlex.admin.ch/eli/oc/2026/547/de",
    "bsvmm":     "https://www.bsv.admin.ch/de/newnsb/BqB41FVYi5FB",
    "tab2027":   "https://sozialversicherungen.admin.ch/de/d/6139/download",
    "berech":    "https://sozialversicherungen.admin.ch/de/d/6141/download",
    "synop":     "https://sozialversicherungen.admin.ch/de/d/6877/download",
    "ueberblick":"https://www.bsv.admin.ch/de/beitraege-im-ueberblick",
    "mb204":     "https://www.ahv-iv.ch/p/2.04.d",
}
SOURCES = {
 "de": [(SRC["fedlex542"], "Fedlex AS 2026 542: Verordnung vom 2.10.2026 über Anpassungen an die Lohn- und Preisentwicklung bei der AHV/IV/EO ab 2027"),
        (SRC["bsvmm"], "BSV-Medienmitteilung vom 2.10.2026: «AHV/IV-Minimalrente steigt um 20 Franken»"),
        (SRC["fedlex547"], "Fedlex AS 2026 547: Änderung der BVV 2 vom 2.10.2026 (Grenzbeträge der beruflichen Vorsorge)"),
        (SRC["tab2027"], "BSV: Beitragstabellen Selbständigerwerbende und Nichterwerbstätige AHV/IV/EO, gültig ab 1.1.2027 (318.114, Version 14)"),
        (SRC["berech"], "BSV: Berechnung der Beiträge und Einträge in das individuelle Konto (IK), gültig ab 1.1.2027"),
        (SRC["synop"], "BSV: Synoptische Tabelle der anwendbaren Beitrags- und Prämiensätze, Stand 1.1.2026"),
        (SRC["ueberblick"], "BSV: Beiträge an die Sozialversicherungen im Überblick"),
        (SRC["mb204"], "Merkblatt 2.04 der AHV-Ausgleichskassen: Geringfügiger Verdienst")],
 "en": [(SRC["fedlex542"], "Fedlex AS 2026 542: Ordinance of 2 Oct 2026 on wage/price adjustments to AHV/IV/EO from 2027 (German)"),
        (SRC["bsvmm"], "FSIO media release of 2 Oct 2026: «AHV/IV minimum pension rises by 20 francs» (German)"),
        (SRC["fedlex547"], "Fedlex AS 2026 547: BVV 2 amendment of 2 Oct 2026 (occupational pension thresholds, German)"),
        (SRC["tab2027"], "FSIO: contribution tables for self-employed and non-employed, valid from 1 Jan 2027 (318.114, v14, DE/FR/IT PDF)"),
        (SRC["berech"], "FSIO: calculation of contributions and individual-account entries, valid from 1 Jan 2027 (German)"),
        (SRC["synop"], "FSIO: synoptic table of applicable contribution and premium rates, as of 1 Jan 2026 (German)"),
        (SRC["ueberblick"], "FSIO: social security contributions at a glance (German)"),
        (SRC["mb204"], "AHV/IV info sheet 2.04: minor earnings (German)")],
 "fr": [(SRC["fedlex542"], "Fedlex RS 2026 542 : ordonnance du 2.10.2026 sur l'adaptation des rentes et cotisations AVS/AI/APG dès 2027 (allemand)"),
        (SRC["bsvmm"], "Communiqué de l'OFAS du 2.10.2026 : « La rente minimale AVS/AI augmente de 20 francs » (allemand)"),
        (SRC["fedlex547"], "Fedlex RS 2026 547 : modification de l'OPP 2 du 2.10.2026 (montants limites LPP, allemand)"),
        (SRC["tab2027"], "OFAS : tables des cotisations AVS/AI/APG pour indépendants et personnes sans activité lucrative, valables dès le 1.1.2027 (318.114, v14)"),
        (SRC["berech"], "OFAS : calcul des cotisations et inscriptions au compte individuel (CI), valable dès le 1.1.2027 (allemand)"),
        (SRC["synop"], "OFAS : tableau synoptique des taux de cotisation et de prime, état au 1.1.2026 (allemand)"),
        (SRC["ueberblick"], "OFAS : les cotisations aux assurances sociales en bref (allemand)"),
        (SRC["mb204"], "Mémento 2.04 des caisses de compensation AVS : salaire minime (allemand)")],
 "it": [(SRC["fedlex542"], "Fedlex RU 2026 542: ordinanza del 2.10.2026 sull'adattamento di rendite e contributi AVS/AI/IPG dal 2027 (tedesco)"),
        (SRC["bsvmm"], "Comunicato UFAS del 2.10.2026: «La rendita minima AVS/AI aumenta di 20 franchi» (tedesco)"),
        (SRC["fedlex547"], "Fedlex RU 2026 547: modifica dell'OPP 2 del 2.10.2026 (importi limite LPP, tedesco)"),
        (SRC["tab2027"], "UFAS: tabelle dei contributi AVS/AI/IPG per indipendenti e persone senza attività lucrativa, valide dal 1.1.2027 (318.114, v14)"),
        (SRC["berech"], "UFAS: calcolo dei contributi e iscrizioni nel conto individuale (CI), valido dal 1.1.2027 (tedesco)"),
        (SRC["synop"], "UFAS: tabella sinottica delle aliquote di contribuzione e dei premi, stato 1.1.2026 (tedesco)"),
        (SRC["ueberblick"], "UFAS: i contributi alle assicurazioni sociali in sintesi (tedesco)"),
        (SRC["mb204"], "Promemoria 2.04 delle casse di compensazione AVS: salario di poca entità (tedesco)")],
}

CTA_MID = {
 "de": """<div class="cta-mid"><strong>Unklar, was das für Ihre Situation bedeutet?</strong> Eine <a href="partner-pruefung.html">geprüfte Fachperson</a> prüft Ihre Unterlagen und zeigt das konkrete Sparpotenzial – die Erstberatung ist kostenlos: <a href="kontakt.html">unverbindliche Offerte anfragen</a>.</div>""",
 "en": """<div class="cta-mid"><strong>Not sure what this means for your situation?</strong> A <a href="partner-pruefung.html">vetted professional</a> reviews your documents and shows your concrete savings potential – first consultation free: <a href="kontakt.html">request a no-obligation quote</a>.</div>""",
 "fr": """<div class="cta-mid"><strong>Vous ne savez pas ce que cela implique pour votre situation ?</strong> Un <a href="partner-pruefung.html">conseiller vérifié</a> examine vos documents et chiffre votre potentiel d’économie – premier entretien gratuit : <a href="kontakt.html">demandez une offre sans engagement</a>.</div>""",
 "it": """<div class="cta-mid"><strong>Non sapete cosa significa in concreto per la sua situazione?</strong> Un <a href="partner-pruefung.html">consulente verificato</a> esamina i suoi documenti e indica il potenziale di risparmio – primo colloquio gratuito: <a href="kontakt.html">richieda un’offerta senza impegno</a>.</div>""",
}

# =================================================================== German ===
de_title = "Lohnabrechnung 2027: AHV/IV/EO-Werte"
de_meta = "Renten +1,59 %, Minimalrente 1'280, neue Beitragswerte per 1.1.2027: was Arbeitgeber und Treuhänder nach dem Bundesrats-Entscheid umstellen müssen."
de_sections = [
 ("Was der Bundesrat am 2. Oktober 2026 beschlossen hat",
  """<p>An seiner Sitzung vom <strong>2. Oktober 2026</strong> hat der Bundesrat die AHV/IV-Renten per <strong>1. Januar 2027</strong> um rund <strong>1,59 Prozent</strong> erhöht (Mischindex; exakter Anpassungsfaktor 1,587 %, neuer Rentenindex 232,7 Punkte). Die Minimalrente steigt von 1'260 auf <strong>1'280 Franken</strong>, die Maximalrente von 2'520 auf <strong>2'560 Franken</strong> pro Monat.</p>
<p>Für die Rentenbezüger ist damit die Sache erledigt – die Erhöhung kommt automatisch (Details in unserem Artikel <a href="ahv-rentenerhoehung-2027-neue-betraege.html">AHV-Renten 2027</a>). Für <strong>Arbeitgeber, Lohnbüros und Treuhänderinnen</strong> ist der Entscheid vom 2. Oktober aber erst der Anfang: Dieselbe Anpassungsverordnung (<strong>AS 2026 542</strong>, publiziert am 14.10.2026, in Kraft am 1.1.2027) hebt zugleich die Beitragswerte an – Mindestbeiträge, die sinkende Beitragsskala für Selbstständigerwerbende und die Vermögensgrenzen der Nichterwerbstätigen. Parallel hat der Bundesrat die Grenzbeträge der beruflichen Vorsorge angepasst (<strong>AS 2026 547</strong>: Eintrittsschwelle 23'040 Fr., Koordinationsabzug 26'880 Fr., oberer Grenzwert 92'160 Fr.).</p>
<p>Die Beitragssätze selbst (AHV/IV/EO total 10,6 % des AHV-Lohns, je hälftig Arbeitgeber und Arbeitnehmende) bleiben unverändert – geändert haben sich die <strong>Rahmenwerte</strong>. Diese Zahlen müssen vor der Januar-Lohnabrechnung 2027 in der Lohnsoftware sitzen; wer den Dezember-Lochnachlauf fährt, braucht sie bereits im laufenden Betrieb.</p>"""),
 ("Beitragswerte 2027 im Überblick: 2026 vs. 2027",
  """<p>Die vollständige Gegenüberstellung – Stand 21. Oktober 2026. «Beschlossen» heisst: Der Wert steht in der amtlichen Sammlung (Fedlex) und ist per 1.1.2027 verbindlich. «Offen» heisst: Hier entscheidet der Bundesrat bzw. publizieren die Ausgleichskassen erst später.</p>
<table><thead><tr><th>Kennwert</th><th>2026</th><th>2027</th><th>Status</th></tr></thead><tbody>
<tr><td>Minimale Vollrente AHV/IV (Fr./Monat)</td><td>1'260</td><td>1'280</td><td>beschlossen</td></tr>
<tr><td>Maximale Vollrente AHV/IV (Fr./Monat)</td><td>2'520</td><td>2'560</td><td>beschlossen</td></tr>
<tr><td>Beitragssatz AHV/IV/EO Arbeitnehmende + Arbeitgeber (je)</td><td>5,3 %</td><td>5,3 %</td><td>gesetzlich, unverändert</td></tr>
<tr><td>Deckel massgebendes Jahreseinkommen (Fr./Jahr)</td><td>302'400</td><td>307'200</td><td>abgeleitet (AHVG Art. 23)</td></tr>
<tr><td>Mindestbeitrag AHV/IV/EO Selbstständige + Nichterwerbstätige (Fr./Jahr)</td><td>530</td><td>541</td><td>beschlossen</td></tr>
<tr><td>– davon AHV / IV / EO (Fr.)</td><td>435 / 70 / 25</td><td>444 / 71 / 26</td><td>beschlossen</td></tr>
<tr><td>Mindestbeitrag freiwillige AHV/IV (Fr./Jahr)</td><td>1'010</td><td>1'030</td><td>beschlossen</td></tr>
<tr><td>Sinkende Beitragsskala Selbstständige: untere/obere Grenze (Fr.)</td><td>10'100 / 60'500</td><td>10'300 / 61'500</td><td>beschlossen</td></tr>
<tr><td>Höchstbeitrag Nichterwerbstätige (50× Mindestbeitrag, Fr./Jahr)</td><td>26'500</td><td>27'050</td><td>beschlossen</td></tr>
<tr><td>Vermögensgrenzen Nichterwerbstätige: Mindest-/Höchstbeitrag (Fr.)</td><td>350'000 / 8'950'000</td><td>360'000 / 9'160'000</td><td>beschlossen</td></tr>
<tr><td>Freibetrag im Referenzalter für Selbstständige (Fr./Jahr)</td><td>16'800</td><td>16'800</td><td>unverändert</td></tr>
<tr><td>Bagatellgrenze geringfügiger Lohn (Fr. pro Arbeitgeber und Jahr)</td><td>2'500</td><td>2'500</td><td>unverändert</td></tr>
<tr><td>ALV-Beitrag (je Seite) / max. versicherter Verdienst</td><td>1,1 % / 148'200</td><td>Stand heute: unverändert</td><td>offen (separate Regelung)</td></tr>
<tr><td>EO-Tagesentschädigung: Höchstbeträge gesamt / Adoption (Fr./Tag)</td><td>275 / 220</td><td>275 / 220</td><td>beschlossen (unverändert)</td></tr>
<tr><td>BVG: Eintrittsschwelle / Koordinationsabzug / oberer Grenzwert (Fr.)</td><td>22'680 / 26'460 / 90'720</td><td>23'040 / 26'880 / 92'160</td><td>beschlossen (AS 2026 547)</td></tr>
</tbody></table>
<p><strong>Wichtig für die Praxis:</strong> Die Tabellen für <em>Arbeitnehmende und Arbeitgebende</em> (monatliche Beitragstabellen der Ausgleichskassen) erscheinen traditionsgemäss erst im <strong>November/Dezember</strong> – die Werte hier sind aber durch die Verordnung bzw. das Gesetz bereits fix, die Softwarehäuser liefern die Parameter im Q4-Update nach.</p>"""),
 ("Lohnabrechnung ab Januar 2027: Die Sätze bleiben, die Deckel verschieben sich",
  """<p>Die gute Nachricht für die Lohnbuchhaltung: An den Prozentsätzen ändert sich nichts. Arbeitgeber und Arbeitnehmende tragen weiterhin je <strong>5,3 Prozent</strong> AHV/IV/EO (AHV 4,35 % + IV 0,7 % + EO 0,25 %) vom AHV-Lohn – zusammen 10,6 Prozent. Auch die ALV bleibt Stand heute bei 1,1 Prozent je Seite bis zum versicherten Verdienst von 148'200 Franken (Solidaritätsbeitrag gibt es seit 2023 nicht mehr); eine allfällige Änderung der ALV-Sätze wäre ein separater Bundesratsentscheid, der üblicherweise im Spätherbst fällt.</p>
<p>Verschieben tut sich der <strong>Deckel</strong>: Beiträge auf Löhnen über der obersten Tabellenklasse werden als Zehntel des massgebenden Einkommens erhoben (Art. 23 Abs. 1 AHVG), bis zum Zehnfachen der Tabellengrenze – also bis <strong>307'200 Franken</strong> Jahreseinkommen (2026: 302'400 Fr.); was darüberliegt, wird zurückerstattet (Art. 23 Abs. 2 AHVG). Konkret:</p>
<ul><li>Wer 2027 genau am Deckel verdient, zahlt je Seite 5,3 % von 307'200 Fr. = <strong>16'281.60 Fr.</strong> pro Jahr (2026: 16'027.20 Fr.) – ein Plus von 254.40 Fr. pro Seite bzw. 508.80 Fr. insgesamt.</li>
<li>Löhne zwischen 302'400 und 307'200 Franken werden 2027 erstmals voll beitragspflichtig – hier lohnt sich ein Blick in die Lohnsummenplanung.</li></ul>
<p>Bei der EO bleiben auch die Tagesentschädigungen unverändert: Höchstbetrag der Gesamtentschädigung 275 Franken pro Tag, Adoptionsentschädigung 220 Franken pro Tag (Art. 7 der Anpassungsverordnung).</p>
<p><strong>Praxistipp:</strong> Spielen Sie Lohnkosten-Szenarien 2027 vor der Budgetierung mit unserem <a href="rechner.html">Rechner</a> durch – gerade bei Löhnen nahe dem Deckel und bei Teilzeit-Mehrfachbeschäftigungen (jede Stelle hat ihren eigenen ALV-Deckel).</p>"""),
 ("Beispielrechnung: Arbeitgeberkosten bei 7'000 Franken Monatslohn",
  """<p>Ein durchgerechnetes Beispiel für die Januar-Abrechnung 2027 – Monatslohn <strong>7'000 Franken</strong> (84'000 Fr. pro Jahr, unter allen Deckeln), angestellte Person ohne Sonderfälle:</p>
<table><thead><tr><th>Beitrag (1. Säule)</th><th>Satz</th><th>Arbeitgeber/Monat</th><th>Abzug Arbeitnehmende/Monat</th></tr></thead><tbody>
<tr><td>AHV/IV/EO</td><td>je 5,3 %</td><td>371.00 Fr.</td><td>371.00 Fr.</td></tr>
<tr><td>ALV (bis 148'200 Fr.)</td><td>je 1,1 %</td><td>77.00 Fr.</td><td>77.00 Fr.</td></tr>
<tr><td><strong>Total</strong></td><td><strong>je 6,4 %</strong></td><td><strong>448.00 Fr.</strong></td><td><strong>448.00 Fr.</strong></td></tr>
</tbody></table>
<p>Die Gesamtbelastung der ersten Säule beträgt damit <strong>896 Franken pro Monat</strong> (12,8 % des Bruttolohns). Nicht enthalten sind: die Beiträge an die Pensionskasse (je nach Reglement), die Familienzulagen (kantonal unterschiedlich, Arbeitgebende ca. 1,0–2,8 % des Lohns, im Kanton Wallis zahlen auch Arbeitnehmende 0,42 %), die Berufsunfallversicherung BUV (Arbeitgeber) und die Nichtberufsunfallversicherung NBUV (Arbeitnehmende).</p>
<p>Da sich die Sätze 2027 nicht ändern, gilt diese Rechnung für 2026 und 2027 identisch – der Unterschied liegt ausschliesslich in den Deckeln und Mindestbeiträgen (siehe Tabelle oben). Genau deshalb ist die Januar-Umstellung für Standardlöhne unspektakulär: Wer die Software-Parameter rechtzeitig einspielt, rechnet ohne Handarbeit weiter.</p>""" + CTA_MID["de"]),
 ("Selbstständigerwerbende und Verwaltungsräte: neuer Mindestbeitrag, neue Skala",
  """<p>Für Inhaber-AGs, Einzelunternehmen und Mandatsträger im eigenen Betrieb ändern sich die fixen Werte:</p>
<ul><li>Der <strong>Mindestbeitrag</strong> AHV/IV/EO für Selbstständigerwerbende und Nichterwerbstätige steigt von 530 auf <strong>541 Franken</strong> pro Jahr (AHV 444 + IV 71 + EO 26); monatlich entspricht das 45.10 Franken.</li>
<li>Die <strong>sinkende Beitragsskala</strong> gilt neu für Einkommen zwischen <strong>10'300 und 61'500 Franken</strong> (bisher 10'100–60'500); der tiefste Skalensatz liegt bei 5,371 %, ab 61'500 Franken gilt der Maximalsatz von 10 Prozent.</li>
<li>Der <strong>Freibetrag im Referenzalter</strong> (Beiträge nur auf dem Einkommen über 16'800 Fr.) bleibt unverändert.</li>
<li>Der Mindestbeitrag der <strong>freiwilligen AHV/IV</strong> (Auslandschweizer) steigt von 1'010 auf 1'030 Franken.</li></ul>
<p>Die neuen Beitragstabellen für Selbstständigerwerbende und Nichterwerbstätige (Dok. 318.114, Version 14) hat das BSV bereits am <strong>7. Oktober 2026</strong> publiziert – sie sind gültig ab 1.1.2027. Hintergrund und Rechenbeispiele für Inhaber: <a href="ahv-mindestbeitrag-selbststaendige.html">AHV-Mindestbeitrag für Selbstständige</a>.</p>
<p><strong>Verwaltungsratshonorare</strong> bleiben unselbstständiges Einkommen: Die Gesellschaft rechnet darauf die normalen 5,3 % + 5,3 % AHV/IV/EO (plus ALV) ab – unabhängig von der Höhe. Wer Honorar und Dividende kombiniert, sollte die Angemessenheit der Gesamtentlöhnung im Blick behalten; zur aktuellen Rechtsprechung siehe unseren Artikel zum <a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">BGE 9C_532/2025 (Dividenden statt Lohn)</a>.</p>"""),
 ("Mini-Jobs und Aushilfen: die 2'500-Franken-Grenze bleibt",
  """<p>Die Freigrenze für geringfügige Entlöhne wird von der Anpassungsverordnung <strong>nicht</strong> erfasst: Wer einer Aushilfe pro Kalenderjahr und Arbeitgeber höchstens <strong>2'500 Franken</strong> bezahlt, rechnet darauf grundsätzlich keine AHV/IV/EO/ALV-Beiträge ab – es sei denn, die versicherte Person verlangt es ausdrücklich (vereinfachtes Abrechnungsverfahren; Merkblatt 2.04). Der Betrag war erst per 1.1.2025 von 2'300 auf 2'500 Franken erhöht worden und bleibt 2027 unverändert.</p>
<p>Achtung, gerade im Dezember und Januar mit Saison- und Aushilfspersonal: Die 2'500 Franken sind eine <strong>Schwelle, kein Freibetrag</strong>. Wird sie um einen Franken gerissen, ist der gesamte Lohn beitragspflichtig – alle Entgelte desselben Arbeitgebers im Kalenderjahr zählen zusammen, inklusive Nebenbezüge und Naturalleistungen. Details: <a href="minijobs-lohnschwelle-ahv-pflicht.html">Mini-Jobs und die AHV-Lohnschwelle</a>.</p>"""),
 ("Nichterwerbstätige: neue Grenzen für Mindest- und Höchstbeitrag",
  """<p>Auch die Beitragspflicht der Nichterwerbstätigen (Bemessung nach Vermögen plus dem 20-fachen jährlichen Renteneinkommen) wird per 1.1.2027 nachgeführt:</p>
<ul><li>Mindestbeitrag: <strong>541 Franken</strong> pro Jahr (bisher 530) – geschuldet, wenn Vermögen + 20 × Renteneinkommen unter <strong>360'000 Franken</strong> liegen (bisher 350'000).</li>
<li>Höchstbeitrag: <strong>27'050 Franken</strong> pro Jahr (50 × Mindestbeitrag; bisher 26'500) – erreicht ab <strong>9'160'000 Franken</strong> (bisher 8'950'000); die mittlere Grenzstufe steigt von 1'750'000 auf 1'760'000 Franken.</li>
<li>Bei Ehepaaren werden Vermögen und Renteneinkommen beider Ehegatten zusammengezählt und halbiert.</li></ul>
<p>Für Arbeitgeber ist das relevant bei <strong>unbezahltem Urlaub, Frühpensionierungen und mitreisenden Partnern</strong> von Auslandentsandten: Wer aus der Erwerbstätigkeit ausscheidet oder weniger als die Hälfte des üblichen Pensums leistet, kann als nichterwerbstätig beitragspflichtig werden – die Ausgleichskasse meldet sich typischerweise im Folgejahr. Die neuen Tabellen (S. 25–30 des Dok. 318.114) gelten ab 1.1.2027.</p>"""),
 ("Zeitplan für die Lohnbuchhaltung: vom Dezember-Lochnachlauf bis zum 31. Januar",
  """<p>Die Umstellung ist Pflichtprogramm, aber planbar. Der Fahrplan bis Ende Januar 2027:</p>
<ol><li><strong>November/Dezember 2026:</strong> Q4-Update der Lohnsoftware einspielen (AHV/IV/EO-Parameter 2027, neue Deckel) und die neuen Tabellen der Ausgleichskasse für Arbeitnehmende abwarten bzw. importieren – sie erscheinen üblicherweise im November/Dezember.</li>
<li><strong>Dezember-Abrechnung:</strong> Dezember-Löhne laufen noch auf den 2026er Werten; die 2027er Parameter greifen mit dem ersten Januar-Lohn. Wer im Dezember bereits Vorschusszahlungen für Januar abrechnet, braucht die neuen Werte jetzt.</li>
<li><strong>Q1 2027:</strong> Akontobeiträge an die Ausgleichskasse werden auf Basis der neuen Lohnsumme neu veranlagt – nach grösseren Lohnrunden oder Personalabbau die Akontohöhe aktiv prüfen lassen.</li>
<li><strong>Pensionskasse:</strong> Eintrittsschwelle 23'040 Fr., Koordinationsabzug 26'880 Fr., oberer Grenzwert 92'160 Fr. (AS 2026 547). Prüfen Sie, ob Teilzeit-Mitarbeitende 2027 neu unter die Eintrittsschwelle fallen oder darüber rutschen, und ob das Reglement Ihrer Kasse die Werte per 1.1.2027 übernimmt.</li>
<li><strong>Bis Ende Januar 2027:</strong> Die jährliche Lohnsummen-Deklaration (Meldung der massgebenden Löhne 2026) an die Ausgleichskasse – noch auf den alten Werten. Frist verpassen ist teuer: Die Kasse veranlagt nach Ermessen.</li>
<li><strong>Kantonal separat prüfen:</strong> Familienzulagen-Sätze (FAK) und Quellensteuertarife 2027 – beides ändert unabhängig von der AHV-Indexierung.</li>
<li><strong>Mitarbeitende informieren:</strong> Höhere Rentenansprüche entstehen nur aus lückenlosen Beiträgen. Ein IK-Auszug deckt Lücken auf: <a href="ahv-beitragsluecken-pruefen-nachzahlen.html">AHV-Beitragslücken prüfen und nachzahlen</a>.</li></ol>
<p><strong>Stand der Dinge (21.10.2026):</strong> Alle oben als «beschlossen» gekennzeichneten Werte sind in der Amtlichen Sammlung publiziert und damit fix. Offen sind lediglich die Ausführungs-Tabellen der Ausgleichskassen für Arbeitnehmende und allfällige separate Entscheide zu den ALV-Sätzen 2027 – beides üblicherweise bis Anfang Dezember bekannt.</p>"""),
 ("Kurz gesagt",
  """<ul><li>Bundesrat 2.10.2026: AHV/IV-Renten +1,59 % per 1.1.2027; Minimalrente 1'280 Fr., Maximalrente 2'560 Fr. pro Monat (AS 2026 542).</li>
<li>Die Beitragssätze für Arbeitnehmende und Arbeitgeber bleiben bei je 5,3 % AHV/IV/EO (plus ALV 1,1 % bis 148'200 Fr.) – der Deckel des massgebenden Jahreseinkommens steigt auf 307'200 Fr.</li>
<li>Mindestbeitrag Selbstständige/Nichterwerbstätige: 530 → 541 Fr.; Skala neu 10'300–61'500 Fr.; Höchstbeitrag Nichterwerbstätige 27'050 Fr. (Vermögensgrenzen 360'000/9'160'000 Fr.).</li>
<li>BVG per 1.1.2027: Eintrittsschwelle 23'040 Fr., Koordinationsabzug 26'880 Fr., oberer Grenzwert 92'160 Fr. (AS 2026 547).</li>
<li>Unverändert: Bagatellgrenze 2'500 Fr., EO-Tagesentschädigungen (275/220 Fr.), Freibetrag im Referenzalter 16'800 Fr.; ALV-Sätze 2027 separat (Stand heute unverändert).</li>
<li>Lohnsoftware-Update im Dezember, erste betroffene Abrechnung: Januar 2027; Jahresdeklaration 2026 bis Ende Januar 2027.</li>
<li>Dies ist allgemeine Information, keine individuelle Beratung – lassen Sie Ihre Lohnabrechnung 2027 von einer Fachperson gegenprüfen.</li></ul>"""),
]

# ================================================================== English ===
en_title = "Payroll 2027: new AHV/IV/EO values"
en_meta = "Federal Council decision of 2 Oct 2026: AHV/IV/EO values change on 1 Jan 2027. New contribution figures, income caps and payroll deadlines for employers."
en_sections = [
 ("What the Federal Council decided on 2 October 2026",
  """<p>At its meeting of <strong>2 October 2026</strong>, the Federal Council raised AHV/IV pensions by approximately <strong>1.59 per cent</strong> with effect from <strong>1 January 2027</strong> (mixed price/wage index; exact adjustment factor 1.587 %, new pension index 232.7 points). The minimum pension rises from CHF 1,260 to <strong>CHF 1,280</strong>, the maximum pension from CHF 2,520 to <strong>CHF 2,560</strong> per month.</p>
<p>For pensioners that is the end of the story — the increase is automatic (details in our article <a href="ahv-rentenerhoehung-2027-neue-betraege.html">AHV pensions 2027</a>). For <strong>employers, payroll offices and fiduciaries</strong>, however, the 2 October decision is only the starting point: the same adjustment ordinance (<strong>AS 2026 542</strong>, published 14 Oct 2026, in force 1 Jan 2027) also raises the contribution-side values — minimum contributions, the degressive scale for the self-employed and the wealth thresholds for non-employed persons. In parallel, the Federal Council adjusted the occupational pension thresholds (<strong>AS 2026 547</strong>: entry threshold CHF 23,040, coordination deduction CHF 26,880, upper limit CHF 92,160).</p>
<p>The contribution rates themselves (AHV/IV/EO total 10.6 % of AHV salary, split evenly between employer and employee) remain unchanged — what changes are the <strong>framework values</strong>. They must be loaded into payroll software before the January 2027 payroll run; anyone processing the December run in advance already needs them.</p>"""),
 ("Contribution values 2027 at a glance: 2026 vs 2027",
  """<p>The full comparison — status as of 21 October 2026. "Decided" means the value has been published in the Official Compilation (Fedlex) and is binding from 1 Jan 2027. "Pending" means the Federal Council or the compensation funds will decide or publish later.</p>
<table><thead><tr><th>Key value</th><th>2026</th><th>2027</th><th>Status</th></tr></thead><tbody>
<tr><td>Minimum full AHV/IV pension (CHF/month)</td><td>1,260</td><td>1,280</td><td>decided</td></tr>
<tr><td>Maximum full AHV/IV pension (CHF/month)</td><td>2,520</td><td>2,560</td><td>decided</td></tr>
<tr><td>AHV/IV/EO rate, employee + employer (each)</td><td>5.3 %</td><td>5.3 %</td><td>statutory, unchanged</td></tr>
<tr><td>Cap on contribution-relevant annual income (CHF/year)</td><td>302,400</td><td>307,200</td><td>derived (AHVG Art. 23)</td></tr>
<tr><td>Minimum AHV/IV/EO contribution, self-employed + non-employed (CHF/year)</td><td>530</td><td>541</td><td>decided</td></tr>
<tr><td>– of which AHV / IV / EO (CHF)</td><td>435 / 70 / 25</td><td>444 / 71 / 26</td><td>decided</td></tr>
<tr><td>Minimum contribution, voluntary AHV/IV (CHF/year)</td><td>1,010</td><td>1,030</td><td>decided</td></tr>
<tr><td>Degressive scale, self-employed: lower/upper limit (CHF)</td><td>10,100 / 60,500</td><td>10,300 / 61,500</td><td>decided</td></tr>
<tr><td>Maximum contribution, non-employed (50× minimum, CHF/year)</td><td>26,500</td><td>27,050</td><td>decided</td></tr>
<tr><td>Wealth thresholds, non-employed: minimum/maximum contribution (CHF)</td><td>350,000 / 8,950,000</td><td>360,000 / 9,160,000</td><td>decided</td></tr>
<tr><td>Tax-free allowance at reference age, self-employed (CHF/year)</td><td>16,800</td><td>16,800</td><td>unchanged</td></tr>
<tr><td>Bagatelle threshold for minor earnings (CHF per employer and year)</td><td>2,500</td><td>2,500</td><td>unchanged</td></tr>
<tr><td>ALV rate (each side) / maximum insured earnings</td><td>1.1 % / 148,200</td><td>as of today: unchanged</td><td>pending (separate rules)</td></tr>
<tr><td>EO daily allowance: total cap / adoption (CHF/day)</td><td>275 / 220</td><td>275 / 220</td><td>decided (unchanged)</td></tr>
<tr><td>BVG: entry threshold / coordination deduction / upper limit (CHF)</td><td>22,680 / 26,460 / 90,720</td><td>23,040 / 26,880 / 92,160</td><td>decided (AS 2026 547)</td></tr>
</tbody></table>
<p><strong>Practice note:</strong> the monthly contribution tables for <em>employees and employers</em> (compensation-fund tables) are traditionally published only in <strong>November/December</strong> — but the values above are already fixed by ordinance or statute, and payroll software vendors ship the parameters with their Q4 update.</p>"""),
 ("Payroll from January 2027: rates stay, caps move",
  """<p>The good news for payroll: nothing changes in the percentages. Employers and employees continue to pay <strong>5.3 per cent each</strong> in AHV/IV/EO (AHV 4.35 % + IV 0.7 % + EO 0.25 %) of AHV salary — 10.6 per cent in total. As of today the ALV also stays at 1.1 per cent per side up to insured earnings of CHF 148,200 (the solidarity surcharge has been abolished since 2023); any change to ALV rates would be a separate Federal Council decision, usually taken in late autumn.</p>
<p>What moves is the <strong>cap</strong>: contributions on salaries above the top table bracket are levied as one tenth of the relevant income (Art. 23 para. 1 AHVG), up to ten times the table limit — i.e. up to <strong>CHF 307,200</strong> of annual income (2026: CHF 302,400); amounts above that are refunded (Art. 23 para. 2 AHVG). Specifically:</p>
<ul><li>Anyone earning exactly at the cap in 2027 pays 5.3 % of CHF 307,200 = <strong>CHF 16,281.60</strong> per year per side (2026: CHF 16,027.20) — an increase of CHF 254.40 per side, CHF 508.80 in total.</li>
<li>Salaries between CHF 302,400 and CHF 307,200 become fully contribution-liable for the first time in 2027 — worth a look in your salary budgeting.</li></ul>
<p>For the EO the daily-allowance ceilings also stay put: maximum total allowance CHF 275 per day, adoption allowance CHF 220 per day (Art. 7 of the adjustment ordinance).</p>
<p><strong>Practical tip:</strong> run your 2027 labour-cost scenarios through our <a href="rechner.html">calculator</a> before budgeting — especially for salaries near the cap and for part-time employees with several jobs (each employment relationship has its own ALV cap).</p>"""),
 ("Worked example: employer cost on a CHF 7,000 monthly salary",
  """<p>A fully calculated example for the January 2027 payroll — monthly salary <strong>CHF 7,000</strong> (CHF 84,000 per year, below all caps), standard employment without special cases:</p>
<table><thead><tr><th>Contribution (1st pillar)</th><th>Rate</th><th>Employer/month</th><th>Employee deduction/month</th></tr></thead><tbody>
<tr><td>AHV/IV/EO</td><td>5.3 % each</td><td>CHF 371.00</td><td>CHF 371.00</td></tr>
<tr><td>ALV (up to CHF 148,200)</td><td>1.1 % each</td><td>CHF 77.00</td><td>CHF 77.00</td></tr>
<tr><td><strong>Total</strong></td><td><strong>6.4 % each</strong></td><td><strong>CHF 448.00</strong></td><td><strong>CHF 448.00</strong></td></tr>
</tbody></table>
<p>Total first-pillar burden: <strong>CHF 896 per month</strong> (12.8 % of gross salary). Not included: pension fund contributions (per fund rules), family allowances (cantonal, employer roughly 1.0–2.8 % of salary; in canton Valais employees also pay 0.42 %), occupational accident insurance BUV (employer) and non-occupational accident insurance NBUV (employee).</p>
<p>Since the rates do not change in 2027, this calculation is identical for 2026 and 2027 — the differences lie exclusively in the caps and minimum contributions (see table above). That is why the January switch-over is uneventful for standard salaries: load the software parameters in time and payroll continues without manual work.</p>""" + CTA_MID["en"]),
 ("Self-employed persons and board members: new minimum contribution, new scale",
  """<p>For owner-managed companies, sole proprietorships and officers paid by their own business, the fixed values change:</p>
<ul><li>The <strong>minimum contribution</strong> for self-employed and non-employed persons rises from CHF 530 to <strong>CHF 541</strong> per year (AHV 444 + IV 71 + EO 26), i.e. CHF 45.10 per month.</li>
<li>The <strong>degressive contribution scale</strong> now applies to income between <strong>CHF 10,300 and CHF 61,500</strong> (previously 10,100–60,500); the lowest scale rate is 5.371 %, and the maximum rate of 10 per cent applies from CHF 61,500.</li>
<li>The <strong>allowance at reference age</strong> (contributions only on income above CHF 16,800) remains unchanged.</li>
<li>The minimum contribution for <strong>voluntary AHV/IV</strong> (Swiss nationals abroad) rises from CHF 1,010 to CHF 1,030.</li></ul>
<p>The new contribution tables for self-employed and non-employed persons (doc. 318.114, version 14) were already published by the FSIO on <strong>7 October 2026</strong>, valid from 1 Jan 2027. Background and calculation examples for owner-managers: <a href="ahv-mindestbeitrag-selbststaendige.html">AHV minimum contribution for the self-employed</a>.</p>
<p><strong>Board fees</strong> remain employment income: the company deducts the standard 5.3 % + 5.3 % AHV/IV/EO (plus ALV) regardless of amount. If you combine fees and dividends, keep the overall remuneration at arm's length — on current case law see our article on <a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">Federal Supreme Court ruling 9C_532/2025 (dividends instead of salary)</a>.</p>"""),
 ("Mini-jobs and casual staff: the CHF 2,500 threshold stays",
  """<p>The threshold for minor earnings is <strong>not</strong> touched by the adjustment ordinance: if you pay a casual worker no more than <strong>CHF 2,500</strong> per calendar year and employer, you generally account for no AHV/IV/EO/ALV contributions on it — unless the insured person expressly requests it (simplified settlement procedure; info sheet 2.04). The amount had only been raised from CHF 2,300 to CHF 2,500 with effect from 1 Jan 2025 and stays unchanged for 2027.</p>
<p>Take care in December and January with seasonal and casual staff: the CHF 2,500 is a <strong>threshold, not an allowance</strong>. Exceed it by one franc and the entire salary becomes contribution-liable — all payments from the same employer within the calendar year count together, including ancillary benefits and benefits in kind. Details: <a href="minijobs-lohnschwelle-ahv-pflicht.html">mini-jobs and the AHV salary threshold</a>.</p>"""),
 ("Non-employed persons: new limits for the minimum and maximum contribution",
  """<p>The contribution duty of non-employed persons (assessed on wealth plus 20 times annual pension income) is also updated as of 1 Jan 2027:</p>
<ul><li>Minimum contribution: <strong>CHF 541</strong> per year (previously 530) — due where wealth + 20 × pension income is below <strong>CHF 360,000</strong> (previously 350,000).</li>
<li>Maximum contribution: <strong>CHF 27,050</strong> per year (50 × minimum; previously 26,500) — reached at <strong>CHF 9,160,000</strong> or more (previously 8,950,000); the middle threshold rises from CHF 1,750,000 to CHF 1,760,000.</li>
<li>For married couples, the wealth and pension income of both spouses is added together and then halved.</li></ul>
<p>This matters to employers in cases of <strong>unpaid leave, early retirement and accompanying partners</strong> of expatriate staff: anyone who leaves gainful employment — or works less than half the usual workload — may become contribution-liable as a non-employed person, and the compensation fund typically follows up the next year. The new tables (pp. 25–30 of doc. 318.114) apply from 1 Jan 2027.</p>"""),
 ("Payroll timetable: from the December run to 31 January",
  """<p>The switch-over is mandatory but plannable. The schedule until end of January 2027:</p>
<ol><li><strong>November/December 2026:</strong> install the Q4 payroll software update (AHV/IV/EO parameters 2027, new caps) and import the compensation funds' new tables for employees as soon as they appear — usually in November/December.</li>
<li><strong>December payroll:</strong> December salaries still run on the 2026 values; the 2027 parameters take effect with the first January salary. If you already process January advance payments in December, you need the new values now.</li>
<li><strong>Q1 2027:</strong> instalment payments (Akontobeiträge) to the compensation fund are reassessed on the new salary total — after major salary rounds or headcount cuts, have the instalment level reviewed proactively.</li>
<li><strong>Pension fund:</strong> entry threshold CHF 23,040, coordination deduction CHF 26,880, upper limit CHF 92,160 (AS 2026 547). Check whether part-time staff fall below or above the new entry threshold in 2027 and whether your fund's regulations adopt the values as of 1 Jan 2027.</li>
<li><strong>By end of January 2027:</strong> the annual salary declaration (report of 2026 contribution-relevant salaries) to the compensation fund — still on the old values. Missing the deadline is costly: the fund then assesses at its discretion.</li>
<li><strong>Check separately (cantonal):</strong> family allowance rates (FAK) and 2027 withholding tax tariffs — both change independently of the AHV indexation.</li>
<li><strong>Inform employees:</strong> higher pension entitlements only arise from uninterrupted contributions. An individual account statement reveals gaps: <a href="ahv-beitragsluecken-pruefen-nachzahlen.html">checking and closing AHV contribution gaps</a>.</li></ol>
<p><strong>Status (21 Oct 2026):</strong> all values marked "decided" above are published in the Official Compilation and therefore final. Only the compensation funds' implementing tables for employees and any separate decision on 2027 ALV rates remain open — both usually known by early December.</p>"""),
 ("In short",
  """<ul><li>Federal Council, 2 Oct 2026: AHV/IV pensions +1.59 % from 1 Jan 2027; minimum pension CHF 1,280, maximum CHF 2,560 per month (AS 2026 542).</li>
<li>Contribution rates for employees and employers stay at 5.3 % each for AHV/IV/EO (plus ALV 1.1 % up to CHF 148,200) — the cap on contribution-relevant annual income rises to CHF 307,200.</li>
<li>Minimum contribution self-employed/non-employed: CHF 530 → 541; scale now CHF 10,300–61,500; maximum contribution non-employed CHF 27,050 (wealth thresholds CHF 360,000/9,160,000).</li>
<li>BVG from 1 Jan 2027: entry threshold CHF 23,040, coordination deduction CHF 26,880, upper limit CHF 92,160 (AS 2026 547).</li>
<li>Unchanged: CHF 2,500 bagatelle threshold, EO daily allowances (CHF 275/220), reference-age allowance CHF 16,800; 2027 ALV rates decided separately (unchanged as of today).</li>
<li>Payroll software update in December; first affected run: January 2027; 2026 annual declaration due by end of January 2027.</li>
<li>General information, not individual advice — have your 2027 payroll reviewed by a licensed professional.</li></ul>"""),
]

# =================================================================== French ===
fr_title = "Salaires 2027 : valeurs AVS/AI/APG"
fr_meta = "Décision du Conseil fédéral du 2.10.2026 : nouvelles valeurs AVS/AI/APG au 1.1.2027. Cotisations, plafonds et échéances salariales pour les employeurs."
fr_sections = [
 ("Ce que le Conseil fédéral a décidé le 2 octobre 2026",
  """<p>Lors de sa séance du <strong>2 octobre 2026</strong>, le Conseil fédéral a relevé les rentes AVS/AI d'environ <strong>1,59 %</strong> au <strong>1er janvier 2027</strong> (indice mixte prix/salaires ; facteur exact 1,587 %, nouvel indice des rentes 232,7 points). La rente minimale passe de 1 260 à <strong>1 280 francs</strong>, la rente maximale de 2 520 à <strong>2 560 francs</strong> par mois.</p>
<p>Pour les retraités, l'affaire est réglée — l'adaptation est automatique (détails dans notre article <a href="ahv-rentenerhoehung-2027-neue-betraege.html">Rentes AVS 2027</a>). Pour les <strong>employeurs, bureaux de salaires et fiduciaires</strong>, la décision du 2 octobre n'est toutefois que le début : la même ordonnance d'adaptation (<strong>RS 2026 542</strong>, publiée le 14.10.2026, en vigueur le 1.1.2027) relève aussi les valeurs cotisatives — cotisations minimales, barème dégressif des indépendants et seuils de fortune des personnes sans activité lucrative. En parallèle, le Conseil fédéral a adapté les montants limites de la prévoyance professionnelle (<strong>RS 2026 547</strong> : seuil d'entrée 23 040 fr., déduction de coordination 26 880 fr., plafond 92 160 fr.).</p>
<p>Les taux de cotisation eux-mêmes (AVS/AI/APG : 10,6 % du salaire AVS, à parts égales entre employeur et salarié) restent inchangés — ce sont les <strong>valeurs-cadres</strong> qui bougent. Elles doivent être intégrées au logiciel de paie avant le décompte de janvier 2027 ; quiconque prépare le bouclement de décembre en a déjà besoin.</p>"""),
 ("Valeurs de cotisation 2027 en un coup d'œil : 2026 vs 2027",
  """<p>La comparaison complète — état au 21 octobre 2026. « Décidé » signifie que la valeur figure au Recueil officiel (Fedlex) et s'impose dès le 1.1.2027. « Ouvert » signifie que le Conseil fédéral ou les caisses de compensation décideront ou publieront plus tard.</p>
<table><thead><tr><th>Valeur-clé</th><th>2026</th><th>2027</th><th>Statut</th></tr></thead><tbody>
<tr><td>Rente minimale complète AVS/AI (fr./mois)</td><td>1 260</td><td>1 280</td><td>décidé</td></tr>
<tr><td>Rente maximale complète AVS/AI (fr./mois)</td><td>2 520</td><td>2 560</td><td>décidé</td></tr>
<tr><td>Taux AVS/AI/APG salarié + employeur (chacun)</td><td>5,3 %</td><td>5,3 %</td><td>légal, inchangé</td></tr>
<tr><td>Plafond du revenu annuel déterminant (fr./an)</td><td>302 400</td><td>307 200</td><td>dérivé (art. 23 LAVS)</td></tr>
<tr><td>Cotisation minimale AVS/AI/APG indépendants + sans activité lucrative (fr./an)</td><td>530</td><td>541</td><td>décidé</td></tr>
<tr><td>– dont AVS / AI / APG (fr.)</td><td>435 / 70 / 25</td><td>444 / 71 / 26</td><td>décidé</td></tr>
<tr><td>Cotisation minimale AVS/AI facultative (fr./an)</td><td>1 010</td><td>1 030</td><td>décidé</td></tr>
<tr><td>Barème dégressif indépendants : limite inférieure/supérieure (fr.)</td><td>10 100 / 60 500</td><td>10 300 / 61 500</td><td>décidé</td></tr>
<tr><td>Cotisation maximale personnes sans activité lucrative (50× minimale, fr./an)</td><td>26 500</td><td>27 050</td><td>décidé</td></tr>
<tr><td>Seuils de fortune sans activité lucrative : cotisation min./max. (fr.)</td><td>350 000 / 8 950 000</td><td>360 000 / 9 160 000</td><td>décidé</td></tr>
<tr><td>Franchise à l'âge de référence, indépendants (fr./an)</td><td>16 800</td><td>16 800</td><td>inchangé</td></tr>
<tr><td>Seuil bagatelle salaire minime (fr. par employeur et année)</td><td>2 500</td><td>2 500</td><td>inchangé</td></tr>
<tr><td>Taux AC (chaque partie) / gain maximal assuré</td><td>1,1 % / 148 200</td><td>à ce jour : inchangé</td><td>ouvert (règle séparée)</td></tr>
<tr><td>Indemnités APG : plafonds total / adoption (fr./jour)</td><td>275 / 220</td><td>275 / 220</td><td>décidé (inchangé)</td></tr>
<tr><td>LPP : seuil d'entrée / déduction de coordination / plafond (fr.)</td><td>22 680 / 26 460 / 90 720</td><td>23 040 / 26 880 / 92 160</td><td>décidé (RS 2026 547)</td></tr>
</tbody></table>
<p><strong>À retenir :</strong> les tables de cotisation mensuelles pour <em>salariés et employeurs</em> (tables des caisses de compensation) ne paraissent traditionnellement qu'en <strong>novembre/décembre</strong> — mais les valeurs ci-dessus sont déjà fixées par ordonnance ou par la loi, et les éditeurs de logiciels de paie livrent les paramètres avec la mise à jour du 4e trimestre.</p>"""),
 ("Décompte de salaire dès janvier 2027 : les taux restent, les plafonds bougent",
  """<p>Bonne nouvelle pour la paie : rien ne change dans les pourcentages. Employeur et salarié continuent de payer <strong>5,3 % chacun</strong> de AVS/AI/APG (AVS 4,35 % + AI 0,7 % + APG 0,25 %) du salaire AVS — soit 10,6 % au total. À ce jour, l'AC reste aussi à 1,1 % par partie jusqu'à un gain assuré de 148 200 francs (la cotisation de solidarité a disparu depuis 2023) ; une éventuelle modification des taux AC ferait l'objet d'une décision séparée du Conseil fédéral, en général à la fin de l'automne.</p>
<p>C'est le <strong>plafond</strong> qui bouge : les cotisations sur les salaires dépassant la dernière classe de la table sont perçues au dixième du revenu déterminant (art. 23 al. 1 LAVS), jusqu'à dix fois la limite de la table — soit <strong>307 200 francs</strong> de revenu annuel (2026 : 302 400 fr.) ; le surplus est restitué (art. 23 al. 2 LAVS). Concrètement :</p>
<ul><li>Quiconque gagne exactement le plafond en 2027 paie 5,3 % de 307 200 fr. = <strong>16 281.60 fr.</strong> par an et par partie (2026 : 16 027.20 fr.), soit +254.40 fr. par partie ou +508.80 fr. au total.</li>
<li>Les salaires entre 302 400 et 307 200 francs deviennent pleinement cotisables en 2027 — un point à vérifier dans la planification de la masse salariale.</li></ul>
<p>Pour les APG, les plafonds journaliers restent également inchangés : indemnité totale maximale 275 francs par jour, allocation d'adoption 220 francs par jour (art. 7 de l'ordonnance d'adaptation).</p>
<p><strong>Conseil pratique :</strong> testez vos scénarios de coûts salariaux 2027 avec notre <a href="rechner.html">calculateur</a> avant le budget — notamment pour les salaires proches du plafond et les temps partiels multiples (chaque emploi a son propre plafond AC).</p>"""),
 ("Exemple chiffré : coûts employeur pour un salaire de 7 000 francs par mois",
  """<p>Un exemple entièrement calculé pour le décompte de janvier 2027 — salaire mensuel de <strong>7 000 francs</strong> (84 000 fr. par an, sous tous les plafonds), emploi standard sans particularités :</p>
<table><thead><tr><th>Cotisation (1er pilier)</th><th>Taux</th><th>Employeur/mois</th><th>Déduction salarié/mois</th></tr></thead><tbody>
<tr><td>AVS/AI/APG</td><td>5,3 % chacun</td><td>371.00 fr.</td><td>371.00 fr.</td></tr>
<tr><td>AC (jusqu'à 148 200 fr.)</td><td>1,1 % chacun</td><td>77.00 fr.</td><td>77.00 fr.</td></tr>
<tr><td><strong>Total</strong></td><td><strong>6,4 % chacun</strong></td><td><strong>448.00 fr.</strong></td><td><strong>448.00 fr.</strong></td></tr>
</tbody></table>
<p>La charge totale du premier pilier s'élève donc à <strong>896 francs par mois</strong> (12,8 % du salaire brut). Ne sont pas compris : les cotisations à la caisse de pension (selon règlement), les allocations familiales (variables selon le canton, employeur env. 1,0–2,8 % du salaire ; en Valais les salariés paient aussi 0,42 %), l'assurance-accidents professionnelle LAA (employeur) et non professionnelle (salarié).</p>
<p>Comme les taux ne changent pas en 2027, ce calcul est identique pour 2026 et 2027 — la différence porte exclusivement sur les plafonds et les cotisations minimales (voir tableau ci-dessus). C'est pourquoi le passage à janvier est sans histoire pour les salaires standard : chargez les paramètres du logiciel à temps et la paie continue sans travail manuel.</p>""" + CTA_MID["fr"]),
 ("Indépendants et administrateurs : nouvelle cotisation minimale, nouveau barème",
  """<p>Pour les SA détenues par leur dirigeant, les raisons individuelles et les mandataires payés par leur propre entreprise, les valeurs fixes changent :</p>
<ul><li>La <strong>cotisation minimale</strong> AVS/AI/APG des indépendants et des personnes sans activité lucrative passe de 530 à <strong>541 francs</strong> par an (AVS 444 + AI 71 + APG 26), soit 45.10 francs par mois.</li>
<li>Le <strong>barème dégressif</strong> s'applique désormais aux revenus entre <strong>10 300 et 61 500 francs</strong> (auparavant 10 100–60 500) ; le taux le plus bas du barème est de 5,371 %, le taux maximal de 10 % s'applique dès 61 500 francs.</li>
<li>La <strong>franchise à l'âge de référence</strong> (cotisations uniquement sur le revenu dépassant 16 800 fr.) reste inchangée.</li>
<li>La cotisation minimale de l'<strong>AVS/AI facultative</strong> (Suisses de l'étranger) passe de 1 010 à 1 030 francs.</li></ul>
<p>Les nouvelles tables de cotisation pour indépendants et personnes sans activité lucrative (doc. 318.114, version 14) ont déjà été publiées par l'OFAS le <strong>7 octobre 2026</strong> — valables dès le 1.1.2027. Contexte et exemples de calcul pour propriétaires : <a href="ahv-mindestbeitrag-selbststaendige.html">cotisation minimale AVS des indépendants</a>.</p>
<p>Les <strong>honoraires d'administrateur</strong> restent un revenu salarié : la société prélève les 5,3 % + 5,3 % AVS/AI/APG usuels (plus AC), quel que soit le montant. Qui combine honoraires et dividendes doit garder une rémunération d'ensemble conforme au marché — sur la jurisprudence actuelle, voir notre article sur l'<a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">ATF 9C_532/2025 (dividendes au lieu du salaire)</a>.</p>"""),
 ("Mini-jobs et auxiliaires : le seuil de 2 500 francs reste",
  """<p>L'ordonnance d'adaptation ne touche <strong>pas</strong> la franchise pour salaire minime : quiconque paie à un auxiliaire au plus <strong>2 500 francs</strong> par année civile et par employeur ne décompte en principe aucune cotisation AVS/AI/APG/AC dessus — sauf demande expresse de la personne assurée (procédure simplifiée ; mémento 2.04). Le montant venait d'être relevé de 2 300 à 2 500 francs au 1.1.2025 et reste inchangé pour 2027.</p>
<p>Attention en décembre et janvier avec le personnel saisonnier et les auxiliaires : les 2 500 francs sont un <strong>seuil, pas une franchise</strong>. Dépassé d'un franc, l'entier du salaire devient cotisable — toutes les rémunérations versées par le même employeur dans l'année civile comptent ensemble, accessoires et avantages en nature compris. Détails : <a href="minijobs-lohnschwelle-ahv-pflicht.html">mini-jobs et seuil de salaire AVS</a>.</p>"""),
 ("Personnes sans activité lucrative : nouveaux seuils de cotisation",
  """<p>L'obligation de cotiser des personnes sans activité lucrative (calculée sur la fortune plus 20 fois le revenu annuel acquis sous forme de rente) est également actualisée au 1.1.2027 :</p>
<ul><li>Cotisation minimale : <strong>541 francs</strong> par an (auparavant 530) — due lorsque fortune + 20 × revenu de rente restent inférieurs à <strong>360 000 francs</strong> (auparavant 350 000).</li>
<li>Cotisation maximale : <strong>27 050 francs</strong> par an (50 × la minimale ; auparavant 26 500) — atteinte dès <strong>9 160 000 francs</strong> (auparavant 8 950 000) ; le seuil intermédiaire passe de 1 750 000 à 1 760 000 francs.</li>
<li>Pour les couples mariés, la fortune et le revenu de rente des deux conjoints sont additionnés puis divisés par deux.</li></ul>
<p>Cela concerne les employeurs en cas de <strong>congé non payé, de retraite anticipée et de conjoints accompagnants</strong> d'expatriés : quiconque quitte la vie active — ou travaille moins de la moitié du taux usuel — peut devenir cotisable comme personne sans activité lucrative, et la caisse de compensation se manifeste en général l'année suivante. Les nouvelles tables (p. 25–30 du doc. 318.114) valent dès le 1.1.2027.</p>"""),
 ("Calendrier de la paie : du bouclement de décembre au 31 janvier",
  """<p>La transition est obligatoire mais planifiable. L'agenda jusqu'à fin janvier 2027 :</p>
<ol><li><strong>Novembre/décembre 2026 :</strong> installer la mise à jour du 4e trimestre du logiciel de paie (paramètres AVS/AI/APG 2027, nouveaux plafonds) et importer dès leur parution les nouvelles tables des caisses de compensation pour salariés — en général en novembre/décembre.</li>
<li><strong>Décompte de décembre :</strong> les salaires de décembre tournent encore sur les valeurs 2026 ; les paramètres 2027 s'appliquent au premier salaire de janvier. Si vous traitez déjà en décembre des avances pour janvier, il vous faut les nouvelles valeurs maintenant.</li>
<li><strong>1er trimestre 2027 :</strong> les acomptes de cotisations à la caisse de compensation sont recalculés sur la nouvelle masse salariale — après d'importantes augmentations ou réductions d'effectifs, faites vérifier le niveau des acomptes.</li>
<li><strong>Caisse de pension :</strong> seuil d'entrée 23 040 fr., déduction de coordination 26 880 fr., plafond 92 160 fr. (RS 2026 547). Vérifiez si des salariés à temps partiel passent sous ou sur le nouveau seuil en 2027 et si le règlement de votre caisse reprend les valeurs au 1.1.2027.</li>
<li><strong>Jusqu'à fin janvier 2027 :</strong> la déclaration annuelle de la masse salariale (annonce des salaires déterminants 2026) à la caisse de compensation — encore sur les anciennes valeurs. Manquer l'échéance coûte cher : la caisse procède alors à une taxation d'office.</li>
<li><strong>À vérifier séparément (cantonal) :</strong> taux des allocations familiales (CAF) et barèmes de l'impôt à la source 2027 — les deux évoluent indépendamment de l'indexation AVS.</li>
<li><strong>Informer les collaborateurs :</strong> des droits à la rente plus élevés ne naissent que de cotisations sans lacunes. Un extrait du compte individuel révèle les lacunes : <a href="ahv-beitragsluecken-pruefen-nachzahlen.html">vérifier et combler les lacunes de cotisation AVS</a>.</li></ol>
<p><strong>État des lieux (21.10.2026) :</strong> toutes les valeurs marquées « décidé » ci-dessus sont publiées au Recueil officiel et donc définitives. Restent ouverts uniquement les tables d'exécution des caisses de compensation pour salariés et une éventuelle décision séparée sur les taux AC 2027 — en général connus début décembre.</p>"""),
 ("En bref",
  """<ul><li>Conseil fédéral du 2.10.2026 : rentes AVS/AI +1,59 % au 1.1.2027 ; rente minimale 1 280 fr., maximale 2 560 fr. par mois (RS 2026 542).</li>
<li>Les taux salariés/employeurs restent à 5,3 % chacun pour AVS/AI/APG (plus AC 1,1 % jusqu'à 148 200 fr.) — le plafond du revenu annuel déterminant passe à 307 200 fr.</li>
<li>Cotisation minimale indépendants/sans activité lucrative : 530 → 541 fr. ; barème désormais 10 300–61 500 fr. ; cotisation maximale sans activité lucrative 27 050 fr. (seuils de fortune 360 000/9 160 000 fr.).</li>
<li>LPP au 1.1.2027 : seuil d'entrée 23 040 fr., déduction de coordination 26 880 fr., plafond 92 160 fr. (RS 2026 547).</li>
<li>Inchangés : seuil bagatelle 2 500 fr., indemnités journalières APG (275/220 fr.), franchise à l'âge de référence 16 800 fr. ; taux AC 2027 séparés (inchangés à ce jour).</li>
<li>Mise à jour du logiciel de paie en décembre, premier décompte concerné : janvier 2027 ; déclaration annuelle 2026 jusqu'à fin janvier 2027.</li>
<li>Information générale, pas un conseil individuel — faites contrôler votre paie 2027 par un spécialiste breveté.</li></ul>"""),
]

# =================================================================== Italian ===
it_title = "Buste paga 2027: nuovi valori AVS/AI/IPG"
it_meta = "Decisione del Consiglio federale del 2.10.2026: nuovi valori AVS/AI/IPG dal 1.1.2027. Contributi, massimali e scadenze per i datori di lavoro."
it_sections = [
 ("Cosa ha deciso il Consiglio federale il 2 ottobre 2026",
  """<p>Nella sua seduta del <strong>2 ottobre 2026</strong> il Consiglio federale ha aumentato le rendite AVS/AI di circa l'<strong>1,59 %</strong> dal <strong>1° gennaio 2027</strong> (indice misto prezzi/salari; fattore esatto 1,587 %, nuovo indice delle rendite 232,7 punti). La rendita minima sale da 1'260 a <strong>1'280 franchi</strong>, la massima da 2'520 a <strong>2'560 franchi</strong> al mese.</p>
<p>Per i pensionati la questione è chiusa — l'aumento è automatico (dettagli nel nostro articolo <a href="ahv-rentenerhoehung-2027-neue-betraege.html">Rendite AVS 2027</a>). Per <strong>datori di lavoro, uffici paghe e fiduciari</strong>, invece, la decisione del 2 ottobre è solo l'inizio: la medesima ordinanza di adattamento (<strong>RU 2026 542</strong>, pubblicata il 14.10.2026, in vigore dal 1.1.2027) innalza anche i valori contributivi — contributi minimi, tavola scalare degli indipendenti e soglie di sostanza delle persone senza attività lucrativa. In parallelo il Consiglio federale ha adeguato gli importi limite della previdenza professionale (<strong>RU 2026 547</strong>: soglia d'entrata 23'040 fr., deduzione di coordinamento 26'880 fr., limite superiore 92'160 fr.).</p>
<p>Le aliquote contributive in quanto tali (AVS/AI/IPG complessivamente 10,6 % del salario AVS, per metà a carico di datore di lavoro e dipendente) restano invariate — cambiano i <strong>valori quadro</strong>. Devono essere caricati nel software paghe prima del conteggio di gennaio 2027; chi prepara la chiusura di dicembre ne ha già bisogno.</p>"""),
 ("Valori contributivi 2027 a colpo d'occhio: 2026 vs 2027",
  """<p>Il confronto completo — stato al 21 ottobre 2026. « Deciso » significa che il valore è pubblicato nella Raccolta ufficiale (Fedlex) ed è vincolante dal 1.1.2027. « Aperto » significa che il Consiglio federale o le casse di compensazione decideranno o pubblicheranno solo più tardi.</p>
<table><thead><tr><th>Valore chiave</th><th>2026</th><th>2027</th><th>Stato</th></tr></thead><tbody>
<tr><td>Rendita minima completa AVS/AI (fr./mese)</td><td>1'260</td><td>1'280</td><td>deciso</td></tr>
<tr><td>Rendita massima completa AVS/AI (fr./mese)</td><td>2'520</td><td>2'560</td><td>deciso</td></tr>
<tr><td>Aliquota AVS/AI/IPG dipendente + datore (ciascuno)</td><td>5,3 %</td><td>5,3 %</td><td>legale, invariata</td></tr>
<tr><td>Massimale del reddito annuo determinante (fr./anno)</td><td>302'400</td><td>307'200</td><td>derivato (art. 23 LAVS)</td></tr>
<tr><td>Contributo minimo AVS/AI/IPG indipendenti + senza attività lucrativa (fr./anno)</td><td>530</td><td>541</td><td>deciso</td></tr>
<tr><td>– di cui AVS / AI / IPG (fr.)</td><td>435 / 70 / 25</td><td>444 / 71 / 26</td><td>deciso</td></tr>
<tr><td>Contributo minimo AVS/AI facoltativa (fr./anno)</td><td>1'010</td><td>1'030</td><td>deciso</td></tr>
<tr><td>Tavola scalare indipendenti: limite inferiore/superiore (fr.)</td><td>10'100 / 60'500</td><td>10'300 / 61'500</td><td>deciso</td></tr>
<tr><td>Contributo massimo senza attività lucrativa (50× minimo, fr./anno)</td><td>26'500</td><td>27'050</td><td>deciso</td></tr>
<tr><td>Soglie di sostanza senza attività lucrativa: contributo min./max. (fr.)</td><td>350'000 / 8'950'000</td><td>360'000 / 9'160'000</td><td>deciso</td></tr>
<tr><td>Importo esente all'età di riferimento, indipendenti (fr./anno)</td><td>16'800</td><td>16'800</td><td>invariato</td></tr>
<tr><td>Soglia bagatella per salario di poca entità (fr. per datore e anno)</td><td>2'500</td><td>2'500</td><td>invariata</td></tr>
<tr><td>Aliquota AD (ciascuna parte) / salario massimo assicurato</td><td>1,1 % / 148'200</td><td>a oggi: invariata</td><td>aperta (regola separata)</td></tr>
<tr><td>Indennità IPG: massimali totale / adozione (fr./giorno)</td><td>275 / 220</td><td>275 / 220</td><td>deciso (invariati)</td></tr>
<tr><td>LPP: soglia d'entrata / deduzione di coordinamento / limite superiore (fr.)</td><td>22'680 / 26'460 / 90'720</td><td>23'040 / 26'880 / 92'160</td><td>deciso (RU 2026 547)</td></tr>
</tbody></table>
<p><strong>Nota operativa:</strong> le tabelle contributive mensili per <em>dipendenti e datori di lavoro</em> (tabelle delle casse di compensazione) escono tradizionalmente solo a <strong>novembre/dicembre</strong> — ma i valori qui sopra sono già fissati da ordinanza o da legge e i produttori di software paghe li rilasciano con l'aggiornamento del 4° trimestre.</p>"""),
 ("Busta paga da gennaio 2027: le aliquote restano, i massimali si spostano",
  """<p>La buona notizia per l'ufficio paghe: nelle percentuali non cambia nulla. Datore di lavoro e dipendente continuano a versare <strong>ciascuno il 5,3 %</strong> di AVS/AI/IPG (AVS 4,35 % + AI 0,7 % + IPG 0,25 %) sul salario AVS — in totale il 10,6 %. A oggi anche l'AD resta all'1,1 % per ciascuna parte fino a un salario assicurato di 148'200 franchi (il contributo di solidarietà non esiste più dal 2023); un'eventuale modifica delle aliquote AD sarebbe oggetto di una decisione separata del Consiglio federale, di norma a fine autunno.</p>
<p>Si sposta invece il <strong>massimale</strong>: i contributi sui salari oltre l'ultima classe della tabella sono prelevati come un decimo del reddito determinante (art. 23 cpv. 1 LAVS), fino a dieci volte il limite della tabella — ossia fino a <strong>307'200 franchi</strong> di reddito annuo (2026: 302'400 fr.); l'eccedenza è restituita (art. 23 cpv. 2 LAVS). In concreto:</p>
<ul><li>Chi nel 2027 guadagna esattamente il massimale versa il 5,3 % di 307'200 fr. = <strong>16'281.60 fr.</strong> l'anno per ciascuna parte (2026: 16'027.20 fr.) — un aumento di 254.40 fr. per parte, 508.80 fr. in totale.</li>
<li>I salari tra 302'400 e 307'200 franchi diventano pienamente assoggettati a contributi nel 2027 — un punto da verificare nella pianificazione della massa salariale.</li></ul>
<p>Per le IPG restano invariati anche i massimali giornalieri: indennità complessiva massima 275 franchi al giorno, indennità di adozione 220 franchi al giorno (art. 7 dell'ordinanza di adattamento).</p>
<p><strong>Consiglio pratico:</strong> prima del budget, simulate gli scenari di costo del lavoro 2027 con il nostro <a href="rechner.html">calcolatore</a> — soprattutto per salari vicini al massimale e per impieghi a tempo parziale multipli (ogni rapporto di lavoro ha il proprio massimale AD).</p>"""),
 ("Esempio di calcolo: costi del datore di lavoro con un salario di 7'000 franchi al mese",
  """<p>Un esempio interamente calcolato per il conteggio di gennaio 2027 — salario mensile di <strong>7'000 franchi</strong> (84'000 fr. l'anno, sotto tutti i massimali), impiego standard senza particolarità:</p>
<table><thead><tr><th>Contributo (1° pilastro)</th><th>Aliquota</th><th>Datore/mese</th><th>Deduzione dipendente/mese</th></tr></thead><tbody>
<tr><td>AVS/AI/IPG</td><td>5,3 % ciascuno</td><td>371.00 fr.</td><td>371.00 fr.</td></tr>
<tr><td>AD (fino a 148'200 fr.)</td><td>1,1 % ciascuno</td><td>77.00 fr.</td><td>77.00 fr.</td></tr>
<tr><td><strong>Totale</strong></td><td><strong>6,4 % ciascuno</strong></td><td><strong>448.00 fr.</strong></td><td><strong>448.00 fr.</strong></td></tr>
</tbody></table>
<p>Il carico complessivo del primo pilastro ammonta quindi a <strong>896 franchi al mese</strong> (12,8 % del salario lordo). Non sono compresi: i contributi alla cassa pensioni (secondo regolamento), gli assegni familiari (diversi per cantone, datore ca. 1,0–2,8 % del salario; in Vallese anche i dipendenti versano lo 0,42 %), l'assicurazione contro gli infortuni professionali LAINF (datore) e non professionali (dipendente).</p>
<p>Poiché le aliquote non cambiano nel 2027, questo calcolo è identico per il 2026 e il 2027 — la differenza riguarda esclusivamente massimali e contributi minimi (vedi tabella sopra). Per questo il passaggio di gennaio è privo di sorprese per i salari standard: caricate per tempo i parametri del software e i conteggi proseguono senza lavoro manuale.</p>""" + CTA_MID["it"]),
 ("Indipendenti e amministratori: nuovo contributo minimo, nuova scala",
  """<p>Per SA nelle mani del proprietario, ditte individuali e mandatari retribuiti dalla propria azienda cambiano i valori fissi:</p>
<ul><li>Il <strong>contributo minimo</strong> AVS/AI/IPG di indipendenti e persone senza attività lucrativa sale da 530 a <strong>541 franchi</strong> l'anno (AVS 444 + AI 71 + IPG 26), ossia 45.10 franchi al mese.</li>
<li>La <strong>tavola scalare dei contributi</strong> si applica ora ai redditi tra <strong>10'300 e 61'500 franchi</strong> (prima 10'100–60'500); l'aliquota più bassa della scala è del 5,371 %, quella massima del 10 % vale da 61'500 franchi.</li>
<li>L'<strong>importo esente all'età di riferimento</strong> (contributi solo sul reddito eccedente 16'800 fr.) resta invariato.</li>
<li>Il contributo minimo dell'<strong>AVS/AI facoltativa</strong> (Svizzeri all'estero) sale da 1'010 a 1'030 franchi.</li></ul>
<p>Le nuove tabelle contributive per indipendenti e persone senza attività lucrativa (doc. 318.114, versione 14) sono già state pubblicate dall'UFAS il <strong>7 ottobre 2026</strong> — valide dal 1.1.2027. Contesto ed esempi di calcolo per titolari: <a href="ahv-mindestbeitrag-selbststaendige.html">contributo minimo AVS degli indipendenti</a>.</p>
<p>Le <strong>indennità di amministratore</strong> restano reddito da attività dipendente: la società preleva i consueti 5,3 % + 5,3 % AVS/AI/IPG (più AD), indipendentemente dall'importo. Chi combina indennità e dividendi deve mantenere una retribuzione complessiva conforme al mercato — sulla giurisprudenza attuale si veda il nostro articolo sulla <a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">DTF 9C_532/2025 (dividendi invece del salario)</a>.</p>"""),
 ("Mini-jobs e ausiliari: la soglia di 2'500 franchi resta",
  """<p>L'ordinanza di adattamento <strong>non</strong> tocca la soglia per i salari di poca entità: chi paga a un ausiliario al massimo <strong>2'500 franchi</strong> per anno civile e datore di lavoro di principio non conteggia contributi AVS/AI/IPG/AD — salvo richiesta esplicita della persona assicurata (procedura semplificata; promemoria 2.04). L'importo era appena stato innalzato da 2'300 a 2'500 franchi dal 1.1.2025 e resta invariato per il 2027.</p>
<p>Attenzione in dicembre e gennaio con il personale stagionale e gli ausiliari: i 2'500 franchi sono una <strong>soglia, non una deduzione</strong>. Superata di un franco, l'intero salario diventa assoggettato a contributi — tutte le retribuzioni dello stesso datore nell'anno civile si sommano, accessori e prestazioni in natura inclusi. Dettagli: <a href="minijobs-lohnschwelle-ahv-pflicht.html">mini-jobs e soglia salariale AVS</a>.</p>"""),
 ("Persone senza attività lucrativa: nuove soglie per contributo minimo e massimo",
  """<p>Anche l'obbligo contributivo delle persone senza attività lucrativa (calcolato sulla sostanza più 20 volte il reddito annuo da rendita) è aggiornato dal 1.1.2027:</p>
<ul><li>Contributo minimo: <strong>541 franchi</strong> l'anno (prima 530) — dovuto se sostanza + 20 × reddito da rendita restano sotto <strong>360'000 franchi</strong> (prima 350'000).</li>
<li>Contributo massimo: <strong>27'050 franchi</strong> l'anno (50 × il minimo; prima 26'500) — raggiunto da <strong>9'160'000 franchi</strong> (prima 8'950'000); la soglia intermedia sale da 1'750'000 a 1'760'000 franchi.</li>
<li>Per le coppie coniugate, sostanza e reddito da rendita di entrambi i coniugi sono sommati e poi dimezzati.</li></ul>
<p>Il tema riguarda i datori di lavoro in caso di <strong>congedo non pagato, pensionamento anticipato e partner al seguito</strong> di espatriati: chi esce dall'attività lucrativa — o lavora meno della metà del grado usuale — può diventare assoggettato a contributi come persona senza attività lucrativa, e la cassa di compensazione si annuncia di norma l'anno successivo. Le nuove tabelle (pp. 25–30 del doc. 318.114) valgono dal 1.1.2027.</p>"""),
 ("Calendario per l'ufficio paghe: dalla chiusura di dicembre al 31 gennaio",
  """<p>La transizione è obbligatoria ma pianificabile. L'agenda fino a fine gennaio 2027:</p>
<ol><li><strong>Novembre/dicembre 2026:</strong> installare l'aggiornamento del 4° trimestre del software paghe (parametri AVS/AI/IPG 2027, nuovi massimali) e importare appena pubblicate le nuove tabelle delle casse di compensazione per i dipendenti — di norma a novembre/dicembre.</li>
<li><strong>Conteggio di dicembre:</strong> i salari di dicembre girano ancora sui valori 2026; i parametri 2027 scattano con il primo salario di gennaio. Se a dicembre elaborate già acconti per gennaio, vi servono ora i nuovi valori.</li>
<li><strong>1° trimestre 2027:</strong> gli acconti contributivi alla cassa di compensazione sono ricalcolati sulla nuova massa salariale — dopo importanti aumenti salariali o riduzioni di organico, fate verificare proattivamente l'entità degli acconti.</li>
<li><strong>Cassa pensioni:</strong> soglia d'entrata 23'040 fr., deduzione di coordinamento 26'880 fr., limite superiore 92'160 fr. (RU 2026 547). Verificate se nel 2027 dipendenti a tempo parziale scendono sotto o salgono sopra la nuova soglia d'entrata e se il regolamento della vostra cassa recepisce i valori dal 1.1.2027.</li>
<li><strong>Entro fine gennaio 2027:</strong> la dichiarazione annuale della massa salariale (comunicazione dei salari determinanti 2026) alla cassa di compensazione — ancora sui vecchi valori. Mancare la scadenza costa caro: la cassa procede a una tassazione d'ufficio.</li>
<li><strong>Da verificare separatamente (cantonale):</strong> aliquote degli assegni familiari (CAF) e tariffe dell'imposta alla fonte 2027 — entrambe cambiano indipendentemente dall'indicizzazione AVS.</li>
<li><strong>Informare i collaboratori:</strong> diritti a rendite più elevati nascono solo da contributi senza lacune. Un estratto del conto individuale rivela le lacune: <a href="ahv-beitragsluecken-pruefen-nachzahlen.html">verificare e colmare le lacune contributive AVS</a>.</li></ol>
<p><strong>Stato dei lavori (21.10.2026):</strong> tutti i valori indicati come « deciso » sono pubblicati nella Raccolta ufficiale e quindi definitivi. Restano aperti solo le tabelle di esecuzione delle casse di compensazione per i dipendenti ed eventuali decisioni separate sulle aliquote AD 2027 — di norma noti entro inizio dicembre.</p>"""),
 ("In breve",
  """<ul><li>Consiglio federale del 2.10.2026: rendite AVS/AI +1,59 % dal 1.1.2027; rendita minima 1'280 fr., massima 2'560 fr. al mese (RU 2026 542).</li>
<li>Le aliquote per dipendenti e datori restano al 5,3 % ciascuna per AVS/AI/IPG (più AD 1,1 % fino a 148'200 fr.) — il massimale del reddito annuo determinante sale a 307'200 fr.</li>
<li>Contributo minimo indipendenti/senza attività lucrativa: 530 → 541 fr.; scala ora 10'300–61'500 fr.; contributo massimo senza attività lucrativa 27'050 fr. (soglie di sostanza 360'000/9'160'000 fr.).</li>
<li>LPP dal 1.1.2027: soglia d'entrata 23'040 fr., deduzione di coordinamento 26'880 fr., limite superiore 92'160 fr. (RU 2026 547).</li>
<li>Invariati: soglia bagatella 2'500 fr., indennità giornaliere IPG (275/220 fr.), importo esente all'età di riferimento 16'800 fr.; aliquote AD 2027 separate (a oggi invariate).</li>
<li>Aggiornamento del software paghe a dicembre, primo conteggio interessato: gennaio 2027; dichiarazione annuale 2026 entro fine gennaio 2027.</li>
<li>Informazione generale, non consulenza individuale — fate ricontrollare i vostri conteggi salariali 2027 da uno specialista diplomato.</li></ul>"""),
]

LANG_DATA = {"de": (de_title, de_meta, de_sections),
             "en": (en_title, en_meta, en_sections),
             "fr": (fr_title, fr_meta, fr_sections),
             "it": (it_title, it_meta, it_sections)}

for lang in ["de", "en", "fr", "it"]:
    title, meta, sections = LANG_DATA[lang]
    assert len(title) <= 40, (lang, len(title), title)
    assert len(title + " | steuerberatung.ch") <= 62, (lang, len(title))
    assert len(meta) <= 158, (lang, len(meta), meta)
    build(lang, SLUG, title, meta, sections, related=RELATED, sources=SOURCES[lang])

# ------------------------- self-validation + report -------------------------
def body_text(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"<main>(.*)</main>", t, re.S)
    t = m.group(1) if m else t
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return htmllib.unescape(re.sub(r"\s+", " ", t)).strip()

report = {"slug": SLUG, "date": "2026-10-21", "card": "data/content-research.jsonl (run 2026-10-21, pin-2026-11-30)",
          "languages": {}}
EXAMPLE_H = {"de": "Beispiel", "en": "Example", "fr": "Exemple", "it": "Esempio"}
for lang in LANG_DATA:
    p = os.path.join(BASE, "" if lang == "de" else lang, SLUG + ".html")
    raw = open(p, encoding="utf-8").read()
    txt = body_text(p)
    h2s = re.findall(r'<h2 id="s\d+">([^<]+)</h2>', raw)
    report["languages"][lang] = {
        "path": os.path.relpath(p, BASE),
        "bytes": len(raw),
        "main_words": len(txt.split()),
        "cta_mid": raw.count('class="cta-mid"'),
        "example": any(EXAMPLE_H[lang].lower() in h.lower() for h in h2s),
        "h2_sections": len(h2s),
        "table": raw.count("<table>"),
        "title_len": len(LANG_DATA[lang][0]),
        "meta_len": len(LANG_DATA[lang][1]),
        "related": RELATED,
    }
    assert report["languages"][lang]["cta_mid"] == 1, (lang, "cta-mid count")
    assert report["languages"][lang]["example"], (lang, "no example section")
    assert report["languages"][lang]["h2_sections"] >= 8, (lang, "too few sections")

# cross-language leakage check
leaks = []
checks = {
    "en": ["beschlossen", "Beispielrechnung", "beitragspflichtig", "Lohnabrechnung", "kurz gesagt", "Kurz gesagt"],
    "de": ["worked example", "employer/month", "payroll timetable", "In short", "décidé", "deciso"],
    "fr": ["beschlossen", "Beispielrechnung", "In short", "deciso", "buste paga"],
    "it": ["beschlossen", "Beispielrechnung", "In short", "décidé", "En bref"],
}
for lang, needles in checks.items():
    txt = body_text(os.path.join(BASE, "" if lang == "de" else lang, SLUG + ".html"))
    for n in needles:
        if n in txt:
            leaks.append(f"{lang}: found '{n}'")
report["cross_language_leaks"] = leaks
assert not leaks, leaks

rp = os.path.join(HERE, "_publish_20261021_lohnabrechnung2027_report.json")
json.dump(report, open(rp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("report:", rp)
print(json.dumps(report["languages"], ensure_ascii=False, indent=1))
