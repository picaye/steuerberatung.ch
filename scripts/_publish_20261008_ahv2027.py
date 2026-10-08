#!/usr/bin/env python3
"""AHV/IV rent increase 2027 + all new pension figures. DE/EN/FR/IT.

Slug: ahv-rentenerhoehung-2027-neue-betraege
Sources (primary, verified 2026-10-08):
- admin.ch Medienmitteilung Bundesrat 02.10.2026 'AHV/IV-Minimalrente steigt um 20 Franken'
- weka.ch Grenzwerte table (530->541 Selbständige, 3a 7'373/36'864)
- 13. AHV-Rente ab Dezember 2026 (Volksabstimmung 2022, Ausführung BSV)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "ahv-rentenerhoehung-2027-neue-betraege"
RELATED = ["13-ahv-rente-dezember-2026.html",
           "saeule-3a-nachzahlen.html",
           "ahv-beitragsluecken-pruefen-nachzahlen.html"]

de_title = "AHV-Renten 2027: +1,59 % – und was die Erhöhung für Säule 3a, BVG und Steuern bedeutet"
de_meta = "Der Bundesrat hat am 2.10.2026 die AHV/IV-Renten per 1.1.2027 um 1,59 % erhöht: Minimalrente 1'280 Fr., Maximalrente 2'560 Fr. neu. Die Folge: höhere 3a-Maximalbeträge (7'373/36'864), neue BVG-Grenzwerte und angepasste EL/ÜL-Bedarfsätze – die Zahlen für Ihre Planung 2027."
de_sections = [
 ("Was der Bundesrat beschlossen hat",
  """<p>An seiner Sitzung vom <strong>2. Oktober 2026</strong> hat der Bundesrat die AHV- und IV-Renten per <strong>1. Januar 2027</strong> um <strong>1,59 Prozent</strong> erhöht (Mischindex aus Preis- und Lohnentwicklung). Die neuen Richtwerte für eine volle Beitragsdauer:</p>
<ul><li>Minimale Monatsrente: <strong>1'260 → 1'280 Fr.</strong> (+20 Fr.)</li>
<li>Maximale Monatsrente: <strong>2'520 → 2'560 Fr.</strong> (+40 Fr.)</li>
<li>Maximales Jahreseinkommen für die Beitragsberechnung: <strong>30'240 → 30'720 Fr.</strong> (das 3-fache der Maximalrente)</li></ul>
<p>Dazu kommt erstmals die <strong>13. AHV-Rente</strong>: Sie wird im <strong>Dezember 2026</strong> das erste Mal ausbezahlt. Wer 2026 eine volle Rente bezieht, erhält 13 Monatsrenten – die Planung der Vorsorgelücke ab 2027 darf diese Zusatzmilliarden nicht vergessen.</p>
<p><strong>Praxistipp:</strong> Die Rentenanpassung erfolgt automatisch – Sie müssen nichts beantragen. Die neue Rentenhöhe steht auf der Individuellen Kontoauszug (IK-Auszug), der 2027 neu zugestellt wird.</p>"""),
 ("Säule 3a: neue Maximalbeträge 2027",
  """<p>Der 3a-Höchstbetrag ist an die AHV-Renten gekoppelt – mit der Erhöhung steigen beide Beträge:</p>
<ul><li>mit Pensionskasse (8 % des maximalen AHV-Jahreseinkommens): <strong>7'258 → 7'373 Fr.</strong></li>
<li>ohne Pensionskasse (20 % des Erwerbseinkommens, max. 5 einfache Maximalrente): <strong>36'288 → 36'864 Fr.</strong></li></ul>
<p>Wichtig für den Kalender: Für die <strong>Steuerperiode 2026</strong> gilt weiterhin der alte Maximalbetrag von 7'258 Fr. – die Einzahlung dafür muss bis <strong>31. Dezember 2026</strong> auf dem 3a-Konto sein. Der neue Betrag 7'373 Fr. gilt ab der Einzahlung für 2027 (Frist wieder 31.12.2027).</p>
<p>Neu seit 2026 kombinierbar: Wer Lücken ab 2025 hat, kann zusätzlich zum Jahresbeitrag <strong>nachzahlen</strong> (bis 10 Jahre rückwirkend, je nach Anbieter). Die Erhöhung der Maximalbeträge vergrössert auch diese Nachzahlungsfenster.</p>
<p><strong>Praxistipp:</strong> Zahlen Sie den 3a-Beitrag wie die 2026er Nachzahlung noch im Dezember ein – Banken und Vorsorgestiftungen brauchen einige Arbeitstage für die Verbuchung. Details zur Nachzahlung: <a href="saeule-3a-nachzahlen.html">Säule 3a nachzahlen</a>.</p>"""),
 ("BVG: neue Eintrittsschwelle und Koordinationsabzug",
  """<p>Auch die obligatorische berufliche Vorsorge passt ihre Grenzwerte an die AHV an (per 1.1.2027):</p>
<ul><li>Eintrittsschwelle (mindestens versicherter Lohn): <strong>22'680 → 23'040 Fr.</strong></li>
<li>Koordinationsabzug (nicht versicherter Lohnanteil): <strong>26'460 → 26'880 Fr.</strong></li>
<li>Oberer Grenzwert (obligatorisch versichertes Maximum): <strong>90'720 → 92'160 Fr.</strong></li></ul>
<p>Praktische Folge: Teilzeitbeschäftigte und Personen mit tiefen Löhnen rutschen eher unter die Eintrittsschwelle – ihr Lohn ist dann nicht mehr obligatorisch BVG-versichert, sofern die Kasse keine günstigeren Reglemente kennt. Für Versicherte mit überobligatorischer Vorsorge kann sich der koordinierte Lohn leicht verändern; viele Kassen passen ihre Reglemente an.</p>
<p><strong>Praxistipp:</strong> Prüfen Sie per Anfang 2027 Ihren Vorsorgeausweis: Steht Ihr Lohn noch über der neuen Eintrittsschwelle 23'040 Fr.? Und kontrollieren Sie den Koordinationsabzug – er bestimmt, wie viel Ihres Lohns obligatorisch versus weiter versichert ist.</p>"""),
 ("Beiträge und Ergänzungsleistungen: die weiteren neuen Zahlen",
  """<p>Zur Vollständigkeit die weiteren Anpassungen per 1.1.2027 (Bundesrat 2.10.2026):</p>
<ul><li>Mindestbeitrag AHV/IV/EO für Selbständigerwerbende ohne Einkommen: <strong>530 → 541 Fr.</strong> pro Jahr.</li>
<li>Beitragssätze und Grenzwerte für Nichterwerbstätige steigen mit der Rentenskala (massgebend ist das 30-fache der Minimalsatz-Rente).</li>
<li>Ergänzungsleistungen (EL): individuelle Jahresbedarfsätze und Vermögensfreibeträge werden ebenfalls um 1,59 % erhöht.</li>
<li>Überbrückungsleistungen (ÜL): Bedarfsätze und Einkommensgrenzen folgen der AHV-Anpassung.</li></ul>
<p>Für Steuerpflichtige mit EL-Bezug oder mit Angehörigen in bescheidenen Verhältnissen lohnt sich der Blick auf die neuen Berechnungsblätter der kantonalen EL-Stellen Anfang 2027 – kleine Rentenerhöhungen können die EL kürzen; eine <a href="praemienverbilligung-2027-anmelden.html">Prämienverbilligung 2027</a> muss trotzdem aktiv beantragt werden.</p>"""),
 ("Was das steuerlich für Sie bedeutet",
  """<p>Drei konkrete Planungseffekte der Erhöhung:</p>
<ol><li><strong>Mehr 3a-Spielraum:</strong> 115 Fr. zusätzlicher Abzug (7'373 statt 7'258) – bei 35 % Grenzsteuerbelastung rund 40 Fr. Ersparnis; der grosse Betrag für Selbstständige ohne 2. Säule: 576 Fr. mehr Abzug.</li>
<li><strong>Rentenbesteuerung:</strong> AHV-Renten bleiben voll steuerbar (ab 2021); die höhere Rente erhöht das steuerbare Einkommen leicht – wer über die EL-Schwelle rutscht, verliert dafür Ansprüche.</li>
<li><strong>Beitragslücken prüfen:</strong> Wer 2026 in die Pensionierung geht, sollte die Beitragjahre lückenlos kontrollieren – ein fehlendes Beitragsjahr kostet ca. 1/44 der Maximalrente, dauerhaft. So geht's: <a href="ahv-beitragsluecken-pruefen-nachzahlen.html">AHV-Beitragslücken prüfen</a>.</li></ol>
<p><strong>Praxistipp:</strong> Nutzen Sie den Rechner auf dieser Seite, um Ihre Steuerbelastung 2027 mit neuer Rente und neuem 3a-Betrag durchzuspielen – die Kantone passen ihre Tarife erst 2027/2028 an, die kalte Progression bleibt ein Thema.</p>"""),
 ("Kurz gesagt",
  """<ul><li>Bundesrat 2.10.2026: AHV/IV-Renten +1,59 % per 1.1.2027 – Minimum 1'280 Fr., Maximum 2'560 Fr. pro Monat.</li>
<li>Erste 13. AHV-Rente im Dezember 2026.</li>
<li>Säule 3a 2027: 7'373 Fr. (mit PK) / 36'864 Fr. (ohne PK) – für 2026 gilt weiterhin 7'258 Fr. bis 31.12.</li>
<li>BVG: Eintrittsschwelle 23'040 Fr., Koordinationsabzug 26'880 Fr., oberer Grenzwert 92'160 Fr.</li>
<li>EL, ÜL und Selbständigen-Mindestbeitrag (541 Fr.) steigen mit.</li>
<li>Dies ist allgemeine Information, keine individuelle Beratung.</li></ul>"""),
]

en_title = "AHV pensions 2027: +1.59% – what the rise means for pillar 3a, BVG and your taxes"
en_meta = "On 2 Oct 2026 the Federal Council raised AHV/IV pensions by 1.59% from 1 Jan 2027: minimum CHF 1,280, maximum CHF 2,560 per month. New pillar 3a ceilings (7,373/36,864), BVG thresholds and EL/ÜL rates – the figures for your 2027 planning."
en_sections = [
 ("What the Federal Council decided",
  """<p>At its meeting on <strong>2 October 2026</strong> the Federal Council raised AHV and IV pensions by <strong>1.59 per cent</strong> as of <strong>1 January 2027</strong> (mixed price/wage index). New reference amounts for a full contribution period:</p>
<ul><li>Minimum monthly pension: <strong>CHF 1,260 → 1,280</strong></li>
<li>Maximum monthly pension: <strong>CHF 2,520 → 2,560</strong></li>
<li>Maximum annual income for contribution purposes: <strong>CHF 30,240 → 30,720</strong> (3× the maximum pension)</li></ul>
<p>In addition, the <strong>13th AHV pension</strong> is paid for the first time in <strong>December 2026</strong> – anyone drawing a full pension in 2026 receives 13 monthly payments.</p>
<p><strong>Practical tip:</strong> The adjustment happens automatically. The new pension amount appears on the individual account statement (IK-Auszug) issued in 2027.</p>"""),
 ("Pillar 3a: new maximum amounts 2027",
  """<p>The 3a ceiling is linked to AHV pensions – both rise:</p>
<ul><li>With a pension fund (8% of max AHV annual income): <strong>CHF 7,258 → 7,373</strong></li>
<li>Without a pension fund (20% of earned income, capped): <strong>CHF 36,288 → 36,864</strong></li></ul>
<p>Calendar note: for <strong>tax year 2026</strong> the old ceiling of CHF 7,258 still applies – the contribution must reach your 3a account by <strong>31 December 2026</strong>. The new CHF 7,373 applies to 2027 contributions.</p>
<p>Since 2026 you can also <strong>catch up</strong> contribution gaps from 2025 onwards (up to 10 years retroactively) on top of the annual amount – the higher ceilings widen those windows too.</p>"""),
 ("BVG: new entry threshold and coordination deduction",
  """<p>Occupational pensions adjust their limits to the AHV rise (as of 1.1.2027):</p>
<ul><li>Entry threshold (minimum insured salary): <strong>CHF 22,680 → 23,040</strong></li>
<li>Coordination deduction: <strong>CHF 26,460 → 26,880</strong></li>
<li>Upper limit of mandatory cover: <strong>CHF 90,720 → 92,160</strong></li></ul>
<p>Effect: part-time earners may fall below the new entry threshold unless their fund keeps more generous rules. Check your 2027 pension statement in January.</p>"""),
 ("In short",
  """<ul><li>AHV/IV pensions +1.59% from 1.1.2027: minimum CHF 1,280, maximum CHF 2,560 per month.</li>
<li>First 13th AHV pension in December 2026.</li>
<li>Pillar 3a 2027: CHF 7,373 (with pension fund) / CHF 36,864 (without); 2026 deadline stays at CHF 7,258 by 31.12.2026.</li>
<li>BVG: entry threshold 23,040, coordination deduction 26,880, upper limit 92,160.</li>
<li>EL, bridging benefits and the self-employed minimum contribution (CHF 541) rise as well.</li>
<li>General information, not individual advice.</li></ul>"""),
]

fr_title = "Rentes AHV 2027 : +1,59 % – ce que la hausse change pour le pilier 3a, la LPP et vos impôts"
fr_meta = "Le 2 octobre 2026, le Conseil fédéral a relevé les rentes AHV/AVS de 1,59 % au 1er janvier 2027 : minimum 1 280 fr., maximum 2 560 fr. par mois. Nouveaux plafonds 3a (7 373/36 864), seuils LPP et montants complémentaires – les chiffres pour planifier 2027."
fr_sections = [
 ("Ce que le Conseil fédéral a décidé",
  """<p>Lors de sa séance du <strong>2 octobre 2026</strong>, le Conseil fédéral a relevé les rentes AHV et AI de <strong>1,59 %</strong> au <strong>1er janvier 2027</strong> (indice mixte prix/salaires). Nouvelles valeurs de référence pour une cotisation complète :</p>
<ul><li>Rente mensuelle minimale : <strong>1 260 → 1 280 fr.</strong></li>
<li>Rente mensuelle maximale : <strong>2 520 → 2 560 fr.</strong></li>
<li>Revenu annuel maximal cotisable : <strong>30 240 → 30 720 fr.</strong> (3× la rente maximale)</li></ul>
<p>S'y ajoute la <strong>13e rente AHV</strong>, versée pour la première fois en <strong>décembre 2026</strong> – quiconque touche une rente complète en 2026 perçoit 13 mensualités.</p>
<p><strong>Conseil pratique :</strong> l'adaptation est automatique ; le nouveau montant figure sur le décompte individuel de compte (DIC) envoyé en 2027.</p>"""),
 ("Pilier 3a : nouveaux plafonds 2027",
  """<p>Le plafond du 3a est lié aux rentes AHV – les deux augmentent :</p>
<ul><li>Avec caisse de pension (8 % du revenu AHV annuel max) : <strong>7 258 → 7 373 fr.</strong></li>
<li>Sans caisse de pension (20 % du revenu, plafonné) : <strong>36 288 → 36 864 fr.</strong></li></ul>
<p>Note calendrier : pour la <strong>période fiscale 2026</strong>, l'ancien plafond de 7 258 fr. s'applique encore – le versement doit parvenir sur le compte 3a avant le <strong>31 décembre 2026</strong>. Le nouveau plafond de 7 373 fr. vaut pour les versements 2027.</p>
<p>Depuis 2026, les lacunes de cotisation dès 2025 peuvent aussi être <strong>rattrapées</strong> (jusqu'à 10 ans en arrière) en plus du versement annuel.</p>"""),
 ("LPP : nouveau seuil d'entrée et déduction de coordination",
  """<p>La prévoyance professionnelle aligne ses limites (au 1.1.2027) :</p>
<ul><li>Seuil d'entrée (salaire minimal assuré) : <strong>22 680 → 23 040 fr.</strong></li>
<li>Déduction de coordination : <strong>26 460 → 26 880 fr.</strong></li>
<li>Plafond de la couverture obligatoire : <strong>90 720 → 92 160 fr.</strong></li></ul>
<p>Effet : les revenus partiels peuvent passer sous le nouveau seuil d'entrée si la caisse n'a pas de règlement plus généreux – vérifiez votre certificat de prévoyance 2027 en janvier.</p>"""),
 ("En bref",
  """<ul><li>Rentes AHV/AI +1,59 % au 1.1.2027 : minimum 1 280 fr., maximum 2 560 fr. par mois.</li>
<li>Première 13e rente AHV en décembre 2026.</li>
<li>Pilier 3a 2027 : 7 373 fr. (avec caisse) / 36 864 fr. (sans) ; pour 2026, 7 258 fr. avant le 31.12.</li>
<li>LPP : seuil d'entrée 23 040 fr., déduction de coordination 26 880 fr., plafond 92 160 fr.</li>
<li>PC, prestations-pont et cotisation minimale des indépendants (541 fr.) augmentent aussi.</li>
<li>Information générale, pas un conseil individuel.</li></ul>"""),
]

it_title = "Pensioni AHV 2027: +1,59 % – cosa comporta per pilastro 3a, LPP e imposte"
it_meta = "Il 2 ottobre 2026 il Consiglio federale ha aumentato le rendite AHV/AVS dell'1,59 % dal 1° gennaio 2027: minimo 1'280 fr., massimo 2'560 fr. al mese. Nuovi importi massimi 3a (7'373/36'864), soglie LPP e prestazioni complementari – i numeri per pianificare il 2027."
it_sections = [
 ("Cosa ha deciso il Consiglio federale",
  """<p>Nella seduta del <strong>2 ottobre 2026</strong> il Consiglio federale ha aumentato le rendite AHV e AI dell'<strong>1,59 %</strong> dal <strong>1° gennaio 2027</strong> (indice misto prezzi/salari). Nuovi valori di riferimento per una durata di contribuzione completa:</p>
<ul><li>Rendita mensile minima: <strong>1'260 → 1'280 fr.</strong></li>
<li>Rendita mensile massima: <strong>2'520 → 2'560 fr.</strong></li>
<li>Reddito annuo massimo assicurabile: <strong>30'240 → 30'720 fr.</strong> (3× la rendita massima)</li></ul>
<p>Si aggiunge la <strong>13a rendita AHV</strong>, versata per la prima volta nel <strong>dicembre 2026</strong>: chi percepisce una rendita completa nel 2026 riceve 13 mensilità.</p>
<p><strong>Consiglio pratico:</strong> l'adeguamento è automatico; il nuovo importo figura sull'estratto conto individuale (ECI) spedito nel 2027.</p>"""),
 ("Pilastro 3a: nuovi importi massimi 2027",
  """<p>L'importo massimo del 3a è legato alle rendite AHV – entrambi crescono:</p>
<ul><li>Con cassa pensione (8 % del reddito AHV annuo massimo): <strong>7'258 → 7'373 fr.</strong></li>
<li>Senza cassa pensione (20 % del reddito, limitato): <strong>36'288 → 36'864 fr.</strong></li></ul>
<p>Nota di calendario: per il <strong>periodo d'imposta 2026</strong> vale ancora il vecchio massimo di 7'258 fr. – il versamento deve essere accreditato sul conto 3a entro il <strong>31 dicembre 2026</strong>. Il nuovo importo si applica ai versamenti 2027.</p>
<p>Dal 2026 è possibile anche <strong>recuperare</strong> gli anni lacunosi dal 2025 in poi (fino a 10 anni indietro) oltre al versamento ordinario.</p>"""),
 ("LPP: nuova soglia d'ingresso e deduzione di coordinazione",
  """<p>Anche la previdenza professionale adegua i limiti (dal 1.1.2027):</p>
<ul><li>Soglia d'ingresso (salario minimo assicurato): <strong>22'680 → 23'040 fr.</strong></li>
<li>Deduzione di coordinazione: <strong>26'460 → 26'880 fr.</strong></li>
<li>Importo massimo della copertura obbligatoria: <strong>90'720 → 92'160 fr.</strong></li></ul>
<p>Effetto: i salari part-time possono scendere sotto la nuova soglia d'ingresso se la cassa non prevede regolamenti più generosi – verificare il certificato di previdenza 2027 a gennaio.</p>"""),
 ("In breve",
  """<ul><li>Rendite AHV/AI +1,59 % dal 1.1.2027: minimo 1'280 fr., massimo 2'560 fr. al mese.</li>
<li>Prima 13a rendita AHV nel dicembre 2026.</li>
<li>Pilastro 3a 2027: 7'373 fr. (con cassa) / 36'864 fr. (senza); per il 2026 resta 7'258 fr. entro il 31.12.</li>
<li>LPP: soglia d'ingresso 23'040 fr., deduzione di coordinazione 26'880 fr., limite massimo 92'160 fr.</li>
<li>Aumentano anche PC, prestazioni ponte e contributo minimo dei indipendenti (541 fr.).</li>
<li>Informazione generale, non consulenza individuale.</li></ul>"""),
]

for lang, title, meta, sections in [("de", de_title, de_meta, de_sections),
                                    ("en", en_title, en_meta, en_sections),
                                    ("fr", fr_title, fr_meta, fr_sections),
                                    ("it", it_title, it_meta, it_sections)]:
    build(lang, SLUG, title, meta, sections, related=RELATED)
print("done")
