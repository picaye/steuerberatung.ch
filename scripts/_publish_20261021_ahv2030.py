#!/usr/bin/env python3
"""Build the AHV2030 consultation-draft article in all 4 languages.

Slug: ahv2030-reform-beitraege-fruehrente
STATUS: everything described is the Federal Council's CONSULTATION DRAFT
(Vernehmlassung 20.5.–11.9.2026). Nothing is law yet. Message (Botschaft)
planned H1 2027, entry into force earliest ~2031.

Sources (all primary, verified curl HTTP 200 on 2026-10-21):
- BSV dossier AHV2030 (bsv.admin.ch/de/ahv-2030) + FAQ
- BSV Medienmitteilung 20.05.2026 "Bundesrat eröffnet Vernehmlassung zur Reform AHV 2030"
- EDI Mitteilung 20.05.2026 (same MM, EDI mirror)
- Fedlex BBl 2026 1338 (Vernehmlassungsverfahren EDI / AHV 2030)
- Fedlex: "Ziele des Bundesrates 2027" (BBl) — Botschaft im 1. Halbjahr 2027
- BSV Medienmitteilung 05.10.2026 (MWST-Zusatzfinanzierung 13. AHV-Rente, 29.11.2026)
- law.ch News 20.05.2026 (Zeitleiste)
Draft-text details (Art. 5 Abs. 2ter / Art. 8 AHVG-Vorentwurf, 15%-Schwelle auf den
Steuerwert, 10%-Beteiligungsquote, Obergrenze sinkende Skala 40'500) stammen aus dem
erläuternden Bericht / der synoptischen Tabelle des Vernehmlassungspakets und sind
im Text entsprechend als Vorschlag gekennzeichnet.
"""
import sys, os, json, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from article_template import build

SLUG = "ahv2030-reform-beitraege-fruehrente"
RELATED = ["ahv-mindestbeitrag-selbststaendige.html",
           "dividenden-ahv-pflicht-bge-9c-532-2025.html",
           "ueberbrueckungsleistungen-ahv-fruehpensionierung.html"]

# cta-mid blocks copied verbatim from the live 4-language mirrors of
# dividenden-ahv-pflicht-bge-9c-532-2025.html
CTA_DE = '<div class="cta-mid"><strong>Unklar, was das für Ihre Situation bedeutet?</strong> Eine <a href="partner-pruefung.html">geprüfte Fachperson</a> prüft Ihre Unterlagen und zeigt das konkrete Sparpotenzial – die Erstberatung ist kostenlos: <a href="kontakt.html">unverbindliche Offerte anfragen</a>.</div>'
CTA_EN = '<div class="cta-mid"><strong>Not sure what this means for your situation?</strong> A <a href="partner-pruefung.html">vetted professional</a> reviews your documents and shows your concrete savings potential – first consultation free: <a href="kontakt.html">request a no-obligation quote</a>.</div>'
CTA_FR = '<div class="cta-mid"><strong>Vous ne savez pas ce que cela implique pour votre situation ?</strong> Un <a href="partner-pruefung.html">conseiller vérifié</a> examine vos documents et chiffre votre potentiel d’économie – premier entretien gratuit : <a href="kontakt.html">demandez une offre sans engagement</a>.</div>'
CTA_IT = '<div class="cta-mid"><strong>Non sapete cosa significa in concreto per la sua situazione?</strong> Un <a href="partner-pruefung.html">consulente verificato</a> esamina i suoi documenti e indica il potenziale di risparmio – primo colloquio gratuito: <a href="kontakt.html">richieda un’offerta senza impegno</a>.</div>'

SRC_URLS = {
 "bsv_dossier": "https://www.bsv.admin.ch/de/ahv-2030",
 "bsv_mm":      "https://www.bsv.admin.ch/de/newnsb/0vkJwFZtbF9R6b1gYHFwY",
 "edi_mm":      "https://www.edi.admin.ch/de/bundesrat-eroeffnet-vernehmlassung-zur-reform-ahv-2030",
 "fedlex_fga":  "https://www.fedlex.admin.ch/eli/fga/2026/1338/de",
 "fedlex_ziele":"https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/fgae/2026/130/de/pdf-a/fedlex-data-admin-ch-eli-fgae-2026-130-de-pdf-a.pdf",
 "bsv_mwst":    "https://www.bsv.admin.ch/de/newnsb/gZ4zhuBYFjyi",
 "lawch":       "https://law.ch/lawnews/2026/05/reform-ahv-2030-bundesrat-eroeffnet-vernehmlassung/",
 "bsv_faq":     "https://www.bsv.admin.ch/de/ahv-2030/faq",
}
SOURCES = {
 "de": [(SRC_URLS["bsv_dossier"], "BSV-Dossier «AHV2030: Die AHV stabilisieren und modernisieren»"),
        (SRC_URLS["bsv_mm"], "BSV-Medienmitteilung vom 20.05.2026: Bundesrat eröffnet Vernehmlassung zur Reform AHV 2030"),
        (SRC_URLS["edi_mm"], "EDI-Mitteilung vom 20.05.2026 zur Vernehmlassung AHV 2030"),
        (SRC_URLS["fedlex_fga"], "Fedlex BBl 2026 1338: Bekanntmachung des Vernehmlassungsverfahrens (AHV 2030)"),
        (SRC_URLS["fedlex_ziele"], "Ziele des Bundesrates 2027 (BBl): Verabschiedung der Botschaft im ersten Halbjahr 2027"),
        (SRC_URLS["bsv_mwst"], "BSV-Medienmitteilung vom 05.10.2026: MWST-Erhöhung für die 13. AHV-Rente, Abstimmung 29.11.2026"),
        (SRC_URLS["lawch"], "law.ch: Reform AHV 2030 – Zeitleiste des Vernehmlassungsverfahrens"),
        (SRC_URLS["bsv_faq"], "BSV: Fragen und Antworten zu AHV2030 (FAQ)")],
 "en": [(SRC_URLS["bsv_dossier"], "FSIO dossier «AHV2030: Stabilising and modernising the AHV/AVS» (German)"),
        (SRC_URLS["bsv_mm"], "FSIO media release of 20 May 2026: Federal Council opens consultation on AHV 2030 (German)"),
        (SRC_URLS["edi_mm"], "FDHA/EDI media release of 20 May 2026 on the AHV 2030 consultation (German)"),
        (SRC_URLS["fedlex_fga"], "Fedlex FGA 2026 1338: notice of the consultation procedure (German)"),
        (SRC_URLS["fedlex_ziele"], "Federal Council's 2027 objectives (FGA): dispatch to be adopted in the first half of 2027 (German, PDF)"),
        (SRC_URLS["bsv_mwst"], "FSIO media release of 5 Oct 2026: VAT increase for the 13th AHV pension, vote of 29 Nov 2026 (German)"),
        (SRC_URLS["lawch"], "law.ch: AHV 2030 consultation timeline (German)"),
        (SRC_URLS["bsv_faq"], "FSIO: FAQ on AHV2030 (German)")],
 "fr": [(SRC_URLS["bsv_dossier"], "Dossier OFAS « AHV2030 : stabiliser et moderniser l'AVS » (allemand)"),
        (SRC_URLS["bsv_mm"], "Communiqué OFAS du 20.05.2026 : ouverture de la consultation sur AVS 2030 (allemand)"),
        (SRC_URLS["edi_mm"], "Communiqué DFI du 20.05.2026 sur la consultation AVS 2030 (allemand)"),
        (SRC_URLS["fedlex_fga"], "Fedlex FF 2026 1338 : avis de procédure de consultation (allemand)"),
        (SRC_URLS["fedlex_ziele"], "Objectifs du Conseil fédéral 2027 (FF) : message au premier semestre 2027 (allemand, PDF)"),
        (SRC_URLS["bsv_mwst"], "Communiqué OFAS du 05.10.2026 : hausse de la TVA pour la 13e rente AVS, votation du 29.11.2026 (allemand)"),
        (SRC_URLS["lawch"], "law.ch : chronologie de la consultation AVS 2030 (allemand)"),
        (SRC_URLS["bsv_faq"], "OFAS : questions et réponses sur AHV2030 (FAQ, allemand)")],
 "it": [(SRC_URLS["bsv_dossier"], "Dossier UFAS « AHV2030: stabilizzare e modernizzare l'AVS » (tedesco)"),
        (SRC_URLS["bsv_mm"], "Comunicato UFAS del 20.05.2026: apertura della consultazione AVS 2030 (tedesco)"),
        (SRC_URLS["edi_mm"], "Comunicato DFI del 20.05.2026 sulla consultazione AVS 2030 (tedesco)"),
        (SRC_URLS["fedlex_fga"], "Fedlex FF 2026 1338: annuncio della procedura di consultazione (tedesco)"),
        (SRC_URLS["fedlex_ziele"], "Obiettivi del Consiglio federale 2027 (FF): messaggio nel primo semestre 2027 (tedesco, PDF)"),
        (SRC_URLS["bsv_mwst"], "Comunicato UFAS del 05.10.2026: aumento IVA per la 13a rendita AVS, votazione del 29.11.2026 (tedesco)"),
        (SRC_URLS["lawch"], "law.ch: cronologia della consultazione AVS 2030 (tedesco)"),
        (SRC_URLS["bsv_faq"], "UFAS: domande e risposte su AHV2030 (FAQ, tedesco)")],
}

# ---------------- German ----------------
de_title = "AHV2030: Was die Reform ändern würde"
de_meta = "AHV2030: Selbstständigen-Beitrag 8,1→8,7 %, Dividenden ab 15 % Rendite AHV-pflichtig, BVG-Mindestalter 63. Was der Entwurf plant – nichts ist beschlossen."
de_sections = [
 ("AHV2030 ist ein Vernehmlassungsentwurf – noch keine Zeile Gesetz",
  """<p><strong>AHV2030</strong> ist die grösste Sozialversicherungsreform, die in der Schweiz derzeit diskutiert wird. Der Bundesrat will damit die Finanzen der AHV für den Zeitraum 2030 bis 2040 sichern und die Versicherung an die gesellschaftliche Entwicklung anpassen: Die Babyboomer-Jahrgänge gehen in Rente, der Fachkräftemangel verschärft sich, und die 13. AHV-Rente kostet ab Dezember 2026 jährlich über 4 Milliarden Franken.</p>
<p>Wichtig vor jeder Zahl in diesem Artikel: AHV2030 ist <strong>kein beschlossenes Gesetz</strong>. Der Bundesrat hat am 20. Mai 2026 die Vernehmlassung eröffnet; sie dauerte bis zum 11. September 2026. Alle beschriebenen Massnahmen sind <strong>Vorschläge des Vorentwurfs</strong> – Parlament, Referendum und Stimmvolk können jedes Detail noch verändern. Was die Vorlage <em>nicht</em> enthält: eine Erhöhung des AHV-Referenzalters – darauf verzichtet der Bundesrat ausdrücklich; eine Expertenkommission prüft Modelle für spätere Reformen.</p>
<p>Die Reform geht auf einen Auftrag der nationalrätlichen Kommission für soziale Sicherheit und Gesundheit zurück. Betroffen sind vor allem drei Gruppen: <strong>Selbstständigerwerbende</strong> (Beitragssatz), <strong>Inhaberinnen und Inhaber von AG und GmbH</strong> (Dividenden) und alle, die eine <strong>Frühpensionierung</strong> planen (2. Säule).</p>"""),
 ("Fahrplan: Botschaft im ersten Halbjahr 2027, Inkrafttreten frühestens 2031",
  """<p>Der Zeitplan der Reform steht in den offiziellen Dokumenten des Bundes:</p>
<ul>
<li><strong>20. Mai 2026:</strong> Der Bundesrat eröffnet die Vernehmlassung zur Reform AHV 2030.</li>
<li><strong>11. September 2026:</strong> Vernehmlassungsfrist läuft ab; Kantone, Parteien und Verbände haben Stellung genommen.</li>
<li><strong>Erstes Halbjahr 2027:</strong> Der Bundesrat will die Botschaft an das Parlament verabschieden (Ziele des Bundesrates 2027); einfliessen werden die Vernehmlassungsergebnisse, der Ausgang der MWST-Abstimmung vom 29. November 2026 und die aktualisierten Finanzperspektiven.</li>
<li><strong>Danach:</strong> parlamentarische Beratung; je nach Verlauf Referendum und Volksabstimmung (voraussichtlich 2029 oder 2030).</li>
<li><strong>Frühestens 2031:</strong> Inkrafttreten. Der erläuternde Bericht rechnet die finanziellen Wirkungen ab 2031; laut BSV sind Fragen zum Inkrafttreten und zu den Modalitäten heute noch nicht abschliessend beantwortbar.</li>
</ul>
<p>Für Ihre Planung: Es bleibt ein Fenster von mehreren Jahren – aber wer eine AG/GmbH führt oder eine Frühpensionierung erwägt, sollte die Stossrichtung kennen.</p>"""),
 ("Selbstständige: Der AHV-Beitragssatz soll von 8,1 auf 8,7 Prozent steigen",
  """<p>Heute zahlen Selbstständigerwerbende auf ihrem Erwerbseinkommen einen tieferen AHV-Beitragssatz als Arbeitnehmende: maximal <strong>8,1 Prozent</strong> (Art. 8 AHVG), während Arbeitnehmende zusammen mit dem Arbeitgeberanteil auf <strong>8,7 Prozent</strong> kommen (je 4,35 Prozent). Bei tieferen Einkommen greift für Selbstständige die <strong>sinkende Beitragsskala</strong>: Wer unter 60'500 Franken im Jahr verdient, zahlt gestaffelt weniger, bis zum Mindestsatz von 4,35 Prozent. Dazu kommen in beiden Fällen die Beiträge an IV und EO.</p>
<p>Der Vorentwurf schlägt vor, den maximalen Beitragssatz der Selbstständigerwerbenden mit höherem Einkommen <strong>an jenen der Arbeitnehmenden anzugleichen – 8,7 statt 8,1 Prozent</strong>. Die sinkende Beitragsskala bleibt dem Grundsatz nach bestehen, soll aber gemäss Vorentwurf nur noch bis zu einer Obergrenze von <strong>40'500 Franken</strong> gelten (heute 60'500). Der Bundesrat begründet das mit Rechtsgleichheit: Laut erläuterndem Bericht profitieren über 70 Prozent der Selbstständigen von der Skala, ihr Einkommen wird im Schnitt nur mit 7,2 Prozent belastet.</p>
<p><strong>Beispiel:</strong> Eine selbstständig erwerbende Architektin erzielt ein massgebendes Einkommen von <strong>Fr. 90'000</strong>. Nach heutigem Recht beträgt ihr AHV-Beitrag 8,1 % = <strong>Fr. 7'290</strong> pro Jahr (die Beiträge an IV und EO kommen dazu). Nach dem vorgeschlagenen Satz von 8,7 % wären es <strong>Fr. 7'830</strong> – eine Mehrbelastung von <strong>Fr. 540 pro Jahr</strong>. (Illustrative Rechnung mit den im Vorentwurf genannten Sätzen – beschlossen ist sie nicht.)</p>
<p>Der Gegeneffekt: Höhere Beiträge bedeuten ein höheres massgebendes Einkommen und tendenziell <strong>bessere Renten</strong>. Für Selbstständige mit tiefem Einkommen ändert sich wenig – die Skala schützt sie weiterhin. Details zu heutigen Sätzen und Mindestbeitrag finden Sie in unserem Beitrag zum <a href="ahv-mindestbeitrag-selbststaendige.html">AHV-Mindestbeitrag für Selbstständige</a>.</p>"""),
 ("Inhaber von AG und GmbH: Dividenden über 15 Prozent Rendite werden beitragspflichtig",
  """<p>Der zweite grosse Baustein trifft Unternehmeraktionäre. Dividenden sind heute grundsätzlich beitragsfrei – wer sich statt Lohn eine hohe Dividende auszahlt, spart AHV-Beiträge. Das will der Bundesrat mit einer <strong>gesetzlichen Schwelle</strong> bekämpfen: Künftig gilt eine Dividende als «überhöht», wenn ihre <strong>Rendite 15 Prozent des investierten Kapitals übersteigt</strong>. Der darüberliegende Betrag gilt als massgebender Lohn und wird beitragspflichtig.</p>
<p>Der Entwurfstext (neuer Art. 5 Abs. 2ter AHVG) präzisiert: Massgebend ist der Anteil des Einkommens aus Beteiligungsrechten, den der Arbeitgeber ausrichtet und der pro Jahr <strong>15 Prozent des Steuerwerts der Beteiligungsrechte</strong> übersteigt; den Steuerwert ermitteln die kantonalen Steuerbehörden. Gemäss erläuterndem Bericht richtet sich die Regel an Mitarbeiter-Aktionäre, die <strong>mindestens 10 Prozent des Gesellschaftskapitals</strong> halten.</p>
<p>Heute greifen die Ausgleichskassen nur im Einzelfall ein: Sie rechnen Dividenden als Lohn auf, wenn der Lohn unangemessen tief <em>und</em> die Dividende offensichtlich überhöht ist – zuletzt bestätigt vom Bundesgericht (<a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">Urteil 9C_532/2025, Durchgriff durch die Holding</a>). Der Vorentwurf würde diese Praxis in eine feste, automatische Schwelle giessen – ohne Nachweis eines Missverhältnisses im Einzelfall. Genau das war in der Vernehmlassung umstritten: Wirtschaftsnahe Kreise halten 15 Prozent für zu tief.</p>
<p>Wichtig: Auch das ist <strong>ein Vorschlag, kein Gesetz</strong>. Wer als Inhaber-AG oder GmbH heute Lohn und Dividende festlegt, fährt weiterhin nach der geltenden Rechtsprechung – die Schwelle von AHV2030 käme frühestens 2031.</p>""" + CTA_DE),
 ("Beitragslücken schliessen: Taggelder, BVG-Einkäufe und Plattformen",
  """<p>Neben den zwei grossen Hebeln enthält der Vorentwurf eine Reihe weiterer Beitragsmassnahmen, die der Bundesrat als «Schliessen von Beitragslücken» bezeichnet:</p>
<ul>
<li><strong>Kranken- und Unfalltaggelder werden beitragspflichtig.</strong> Bisher sind Taggelder der Kranken- und Unfallversicherung vom AHV-Beitrag ausgenommen – anders als jene der ALV, EO, IV oder MV. Das soll sich angleichen; laut Bundesrat verbessert das die späteren Renten der betroffenen Personen.</li>
<li><strong>Einkäufe in die 2. Säule:</strong> Freiwillige Einkäufe Selbstständiger in die berufliche Vorsorge sollen nicht mehr im heutigen Umfang von der AHV-Beitragspflicht ausgenommen sein – Gleichstellung mit Arbeitnehmenden.</li>
<li><strong>Meldepflicht für Plattformbetreiber:</strong> Elektronische Plattformen sollen Erwerbseinkommen melden, damit Beitragslücken bei Gig- und Nebenerwerben sichtbar werden.</li>
<li><strong>Modernisierung:</strong> verbesserter Datenaustausch über Nichterwerbstätige, vereinfachte Lohnadministration durch spezialisierte Dritte (Payrolling) und Anpassungen bei der Versicherungsunterstellung.</li>
</ul>
<p>Für Arbeitgebende relevant: Werden Taggelder beitragspflichtig, erfasst die Beitragsabrechnung künftig auch Krankentaggelder – ein in der Vernehmlassung kontroverser Punkt.</p>"""),
 ("Frühpensionierung in der 2. Säule: Das Mindestalter steigt von 58 auf 63",
  """<p>Der einschneidendste Punkt für Angestellte betrifft die berufliche Vorsorge: Das <strong>Mindestalter für den vorzeitigen Altersrücktritt soll schrittweise von heute 58 auf 63 Jahre</strong> angehoben werden. Ausnahmen sind gemäss Bundesrat insbesondere bei Unternehmensumstrukturierungen oder im Rahmen von Gesamtarbeitsverträgen möglich; zudem gilt eine <strong>absolute Untergrenze von 60 Jahren</strong>.</p>
<p>Wer vorzeitig ausscheidet, soll weiterhin in der 2. Säule versichert bleiben und die Austrittsleistung übertragen können. Die Modalitäten und Übergangsregeln sind offen – das BSV hält in seinen FAQ fest, dass sich Fragen zum Inkrafttreten und zur Ausgestaltung heute nicht beantworten lassen.</p>
<p>Praktisch: Wer zwischen 58 und 63 eine Frühpensionierung plant, bräuchte künftig eine Ausnahmeregelung (GAV, Umstrukturierung) oder müsste die Lücke bis zum erstmöglichen BVG-Bezug selbst überbrücken. Genau dafür existieren die <a href="ueberbrueckungsleistungen-ahv-fruehpensionierung.html">Überbrückungsleistungen für ältere Arbeitslose</a> (siehe verlinkter Beitrag). Für die meisten Betroffenen ist das ein Planungsthema mit Vorlauf von Jahren, nicht von Monaten.</p>"""),
 ("Weiterarbeiten über das Referenzalter: höherer Freibetrag, Aufschub ohne Alterslimite",
  """<p>Statt das Rentenalter zu erhöhen, will der Bundesrat das Weiterarbeiten attraktiver machen. Drei Anreize stehen im Vorentwurf:</p>
<ol>
<li><strong>Freibetrag rauf:</strong> Wer nach dem Referenzalter weiter erwerbstätig ist, profitiert heute von einem Freibetrag von 16'800 Franken pro Jahr, auf dem keine AHV-Beiträge erhoben werden. Der Vorentwurf hebt ihn auf <strong>22'680 Franken</strong> an, mit regelmässiger Anpassung. Dieses Einkommen wird zudem bei der Rentenberechnung stärker berücksichtigt.</li>
<li><strong>Aufschub über 70:</strong> Heute lässt sich die AHV-Rente höchstens bis zum 70. Geburtstag aufschieben. Diese Limite soll fallen – der Aufschub wäre auch darüber hinaus möglich.</li>
<li><strong>Neue Kürzungs- und Erhöhungssätze:</strong> Die versicherungstechnischen Sätze für Vorbezug und Aufschub sollen künftig nach positiven und negativen Anreizprinzipien festgelegt werden statt rein nach der Lebenserwartung.</li>
</ol>
<p>Flankierend will der Bundesrat die Grundlagen für <strong>flexiblere Rentenmodelle</strong> schaffen, im Hinblick auf eine künftige Individualisierung des Referenzalters. Ob sich Weiterarbeiten im Alter lohnt, ist auch eine Steuerfrage – Modellrechnungen zu Grenzsteuersatz und Abzügen liefert unser <a href="rechner.html">Steuerrechner</a>.</p>"""),
 ("Heutiges Recht und Vorentwurf im Vergleich",
  """<p>Die Tabelle stellt das geltende Recht (Stand Oktober 2026) den Vorschlägen gegenüber. Alles in der rechten Spalte ist <strong>vom Bundesrat in der Vernehmlassung vorgeschlagen</strong> – beschlossen ist nichts davon.</p>
<table>
<thead><tr><th>Bereich</th><th>Heute (gültiges Recht)</th><th>AHV2030-Vorentwurf (Vorschlag)</th></tr></thead>
<tbody>
<tr><td>AHV-Beitragssatz Selbstständige</td><td>max. 8,1 %; sinkende Skala unter Fr. 60'500</td><td>max. 8,7 %; Skala bleibt, Obergrenze gemäss Entwurf Fr. 40'500</td></tr>
<tr><td>Dividenden an Unternehmeraktionäre</td><td>beitragsfrei; Aufrechnung nur im Einzelfall bei unangemessen tiefem Lohn + überhöhter Dividende</td><td>Anteil über 15 % Rendite bzw. 15 % des Steuerwerts der Beteiligung gilt als massgebender Lohn</td></tr>
<tr><td>Kranken-/Unfalltaggelder</td><td>nicht AHV-beitragspflichtig</td><td>beitragspflichtig</td></tr>
<tr><td>BVG-Mindestalter für Frühpensionierung</td><td>58 Jahre</td><td>schrittweise 63 Jahre, absolute Untergrenze 60; Ausnahmen (GAV, Umstrukturierungen)</td></tr>
<tr><td>Freibetrag Erwerbseinkommen nach Referenzalter</td><td>Fr. 16'800 pro Jahr</td><td>Fr. 22'680 pro Jahr, regelmässige Anpassung</td></tr>
<tr><td>Rentenaufschub</td><td>bis zum 70. Geburtstag</td><td>Alterslimite aufgehoben</td></tr>
<tr><td>AHV-Referenzalter</td><td>65 Jahre</td><td>unverändert – keine Erhöhung vorgesehen</td></tr>
</tbody>
</table>"""),
 ("Finanzierung: Alles hängt an der Abstimmung vom 29. November 2026",
  """<p>AHV2030 lässt sich nicht ohne die 13. AHV-Rente denken. Sie wird im <strong>Dezember 2026 erstmals ausbezahlt</strong> und kostet zunächst über 4, später über 5 Milliarden Franken pro Jahr. Das Parlament hat am 19. Juni 2026 eine Teilfinanzierung über die <strong>Mehrwertsteuer</strong> beschlossen: Normalsatz +0,4 Prozentpunkte (8,1 → 8,5 %), Sondersatz Hotellerie 3,8 → 4,0 %; der reduzierte Satz von 2,6 Prozent bleibt unverändert. Weil dafür die Verfassung geändert werden muss, stimmen Volk und Stände am <strong>29. November 2026</strong> ab; Inkrafttreten frühestens Anfang 2028. Mehr dazu im Beitrag zur <a href="13-ahv-rente-dezember-2026.html">13. AHV-Rente im Dezember 2026</a>.</p>
<p>Der Ausgang dieser Abstimmung bestimmt, wie viel Zusatzfinanzierung AHV2030 schultern muss: Wird die 13. Rente langfristig gesichert, braucht es laut Bundesrat grundsätzlich keine zusätzliche Finanzierung im Rahmen von AHV2030. Andernfalls skizziert der Vorentwurf Alternativen – etwa eine MWST-Erhöhung um 0,7 Prozentpunkte oder eine Kombination aus MWST und Beitragssatzerhöhung.</p>
<p>Die im Entwurf enthaltenen Beitragsmassnahmen selbst dürften der AHV bis 2040 Mehreinnahmen von <strong>rund 600 Millionen Franken pro Jahr</strong> bringen. Zur Absicherung ist ein <strong>Interventionsmechanismus</strong> vorgeschlagen: Sinkt der AHV-Ausgleichsfonds innerhalb von drei Jahren voraussichtlich unter 90 Prozent einer Jahresausgabe, müsste der Bundesrat dem Parlament binnen eines Jahres Stabilisierungsmassnahmen unterbreiten.</p>"""),
 ("Kurz gesagt: Was Sie jetzt damit anfangen",
  """<ul>
<li><strong>Nichts ist Gesetz:</strong> Vernehmlassungsentwurf (bis 11.9.2026), Botschaft im ersten Halbjahr 2027, Volksabstimmung möglich, Inkrafttreten frühestens 2031.</li>
<li><strong>Selbstständige</strong> müssten nach dem Entwurf ab hohen Einkommen 8,7 statt 8,1 Prozent AHV-Beitrag zahlen; die sinkende Skala bliebe, aber mit tieferer Obergrenze.</li>
<li><strong>Inhaber von AG/GmbH:</strong> Dividenden über 15 Prozent Rendite auf dem investierten Kapital (bzw. Steuerwert) sollen automatisch als Lohn gelten. Die geltende Praxis aus dem Urteil 9C_532/2025 gilt bis dahin unverändert.</li>
<li><strong>Frühpensionierungspläne vor 2035</strong> gehören neu gerechnet: Das BVG-Mindestalter soll schrittweise von 58 auf 63 steigen (Untergrenze 60, Ausnahmen möglich).</li>
<li><strong>Weiterarbeiten wird attraktiver:</strong> Freibetrag 16'800 → 22'680 Franken, Rentenaufschub auch über 70 hinaus – alles unter Vorbehalt der parlamentarischen Beratung.</li>
<li>Der nächste harte Termin ist die <strong>MWST-Abstimmung vom 29. November 2026</strong> – ihr Ausgang verändert den Finanzierungsbedarf von AHV2030. Wir aktualisieren diesen Beitrag nach der Abstimmung.</li>
<li>Dies ist allgemeine Information, keine individuelle Beratung – lassen Sie Struktur und Vorsorgeplanung von einer geprüften Fachperson prüfen.</li>
</ul>"""),
]

# ---------------- English ----------------
en_title = "AHV2030: What the Reform Would Change"
en_meta = "AHV2030: self-employed AHV rate 8.1→8.7 %, dividends above 15 % return become contribution-liable, BVG minimum age 63. What the draft plans – not yet law."
en_sections = [
 ("AHV2030 is a consultation draft – not one line of it is law yet",
  """<p><strong>AHV2030</strong> is the biggest social-security reform currently under discussion in Switzerland. The Federal Council wants to secure AHV/AVS (first-pillar) finances for 2030 to 2040 and adapt the insurance to social change: the baby-boom cohorts are retiring, skilled labour is scarce, and the 13th AHV pension will cost more than CHF 4 billion a year from December 2026.</p>
<p>Important before any figure in this article: AHV2030 is <strong>not enacted law</strong>. The Federal Council opened the consultation on 20 May 2026; it ran until 11 September 2026. Everything described here is a <strong>proposal of the consultation draft</strong> – parliament, a possible referendum and the voters can still change every detail. What the bill does <em>not</em> contain: any increase of the AHV reference age. The Federal Council explicitly refrains from raising it; an expert commission will examine models for later reforms.</p>
<p>The reform goes back to a motion of the National Council's social security and health committee demanding AHV stabilisation for 2030–2040. Three groups are most affected: the <strong>self-employed</strong> (contribution rate), <strong>owners of AGs and GmbHs</strong> (dividends), and anyone planning <strong>early retirement</strong> (second pillar).</p>"""),
 ("Timeline: dispatch in the first half of 2027, entry into force 2031 at the earliest",
  """<p>The reform timetable is set out in the Confederation's official documents:</p>
<ul>
<li><strong>20 May 2026:</strong> the Federal Council opens the consultation on AHV 2030.</li>
<li><strong>11 September 2026:</strong> the consultation deadline expires; cantons, parties and associations have submitted their positions.</li>
<li><strong>First half of 2027:</strong> the Federal Council intends to adopt the dispatch (Botschaft) to parliament – as stated in its published objectives for 2027. The consultation results, the outcome of the VAT vote of 29 November 2026 and the updated financial outlook will feed into it.</li>
<li><strong>Then:</strong> parliamentary debate; depending on the course of events a referendum is possible, with a popular vote likely in 2029 or 2030.</li>
<li><strong>2031 at the earliest:</strong> entry into force. The explanatory report calculates the financial effects of the measures from 2031; the Federal Social Insurance Office (FSIO/BSV) stresses that questions on entry into force and modalities cannot be answered definitively today.</li>
</ul>
<p>For your planning this means: a window of several years remains – but if you run an AG/GmbH or consider early retirement, you should know the direction of travel, because restructuring takes time.</p>"""),
 ("Self-employed: the AHV rate is to rise from 8.1 to 8.7 per cent",
  """<p>Today the self-employed pay a lower AHV rate on their earned income than employees: a maximum of <strong>8.1 per cent</strong> (Art. 8 AHVG), whereas employees reach <strong>8.7 per cent</strong> together with the employer share (4.35 each). For lower incomes a <strong>degressive scale</strong> applies to the self-employed: anyone earning less than CHF 60,500 a year pays progressively less, down to a minimum rate of 4.35 per cent. In both cases IV and EO contributions are added.</p>
<p>The consultation draft proposes to align the maximum rate for higher-income self-employed <strong>with that of employees – 8.7 instead of 8.1 per cent</strong>. The degressive scale is kept in principle but, per the draft, would only apply up to a ceiling of <strong>CHF 40,500</strong> (today CHF 60,500). The Federal Council justifies this with equal treatment and competitive neutrality: according to the explanatory report, more than 70 per cent of the self-employed benefit from the scale today, and their income is charged at 7.2 per cent on average.</p>
<p><strong>Example:</strong> a self-employed architect has a relevant income of <strong>CHF 90,000</strong>. Under current law her AHV contribution is 8.1 % = <strong>CHF 7,290</strong> a year (IV and EO contributions are added). At the proposed 8.7 % it would be <strong>CHF 7,830</strong> – an increase of <strong>CHF 540 a year</strong>. (Illustrative calculation using the rates named in the draft – nothing is decided.)</p>
<p>The flip side stressed by the Federal Council: higher contributions also mean higher relevant income and therefore tend to produce <strong>better pensions</strong>. Little changes for the self-employed on low incomes – the scale still protects them. Details on today's rates and minimum contribution are in our article on the <a href="ahv-mindestbeitrag-selbststaendige.html">AHV minimum contribution for the self-employed</a>.</p>"""),
 ("Owners of AGs and GmbHs: dividends above a 15 % return become contribution-liable",
  """<p>The second big element targets owner-shareholders. Dividends are in principle contribution-free today – anyone paying themselves a high dividend instead of salary saves AHV contributions. The Federal Council wants to fight this with a <strong>statutory threshold</strong>: in future a dividend would be deemed «excessive» where its <strong>return exceeds 15 per cent of the invested capital</strong>. The amount above that threshold would count as relevant salary and become contribution-liable.</p>
<p>The draft text (new Art. 5 para. 2ter AHVG) is more precise: what counts is the share of income from participation rights paid by the employer that exceeds <strong>15 per cent of the tax value of those rights</strong> per year; the cantonal tax authorities determine the tax value. According to the explanatory report, the rule addresses employee-shareholders holding <strong>at least 10 per cent of the share capital</strong>.</p>
<p>Today the compensation funds intervene only case by case: they reclassify dividends as salary where the salary is unreasonably low <em>and</em> the dividend manifestly excessive – most recently confirmed by the Federal Supreme Court in ruling <a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">9C_532/2025 on the look-through of holdings</a>. The draft would turn this practice into a fixed, automatic threshold – without the fund having to prove a disproportion in the individual case. This was disputed in the consultation: business circles consider 15 per cent too low, arguing that SME equity demands a higher risk return.</p>
<p>Important: this too is <strong>a proposal, not law</strong>. Owner-managed AGs and GmbHs setting salary and dividends today continue to follow the applicable case law – the AHV2030 threshold would arrive in 2031 at the earliest.</p>""" + CTA_EN),
 ("Closing contribution gaps: daily allowances, second-pillar buy-ins and platforms",
  """<p>Beyond the two big levers the draft contains further contribution measures the Federal Council calls «closing contribution gaps»:</p>
<ul>
<li><strong>Sickness and accident daily allowances become contribution-liable.</strong> So far these allowances are exempt from AHV contributions – unlike those of unemployment, EO, IV or military insurance. That is to be aligned; according to the Federal Council this improves the later pensions of the persons concerned.</li>
<li><strong>Second-pillar buy-ins:</strong> the self-employed would no longer be able to shelter voluntary buy-ins into occupational pension schemes from AHV contributions to today's extent – equal treatment with employees.</li>
<li><strong>Reporting duty for platform operators:</strong> electronic platforms would have to report earned income, making contribution gaps from gig and side work visible.</li>
<li><strong>Modernisation:</strong> improved data exchange on persons not in employment, simplified payroll administration by specialised third parties (payrolling), and adjustments to insurance subordination.</li>
</ul>
<p>Relevant for employers: if daily allowances become contribution-liable, payroll accounting would in future also cover social-security contributions on sickness allowances – a point consultation participants judged controversially.</p>"""),
 ("Early retirement in the second pillar: minimum age rises from 58 to 63",
  """<p>The most incisive point for employees concerns occupational pension provision: the <strong>minimum age for early retirement is to be raised step by step from today's 58 to 63 years</strong>. Exceptions are possible per the Federal Council notably in company restructurings or under collective labour agreements; an <strong>absolute floor of 60 years</strong> applies in any case.</p>
<p>People retiring early would remain insured in the second pillar and be able to transfer their vested benefits to a new pension institution. The concrete modalities and transition rules are open – the FSIO notes in its FAQ that questions on entry into force and the design of the increase cannot be answered today.</p>
<p>In practice the proposal means: anyone planning early retirement between 58 and 63 would in future need an exception (GAV, restructuring) or would have to bridge the gap to the earliest possible BVG drawdown themselves. That is exactly what the <a href="ueberbrueckungsleistungen-ahv-fruehpensionierung.html">bridging benefits for older unemployed persons</a> are for – who can claim them and what they pay is explained in the linked article. For most people concerned this is a planning topic with a lead time of years, not months.</p>"""),
 ("Working beyond the reference age: higher tax-free allowance, deferral with no age cap",
  """<p>Instead of raising the retirement age, the Federal Council wants to make working up to and beyond the reference age more attractive. The draft contains three incentives:</p>
<ol>
<li><strong>Higher allowance:</strong> people who keep working after the reference age today benefit from an allowance of CHF 16,800 a year on which no AHV contributions are levied. The draft raises it to <strong>CHF 22,680</strong> and provides for regular indexation. This income would also count more strongly in the pension calculation.</li>
<li><strong>Deferral beyond 70:</strong> today the AHV pension can be deferred at most until the 70th birthday. This cap is to be abolished – deferral would be possible beyond it, with continued contributions to the AHV.</li>
<li><strong>New reduction/increase rates:</strong> the actuarial rates for early drawdown and deferral are to be set according to positive and negative incentive principles in future instead of purely by life expectancy.</li>
</ol>
<p>In parallel the Federal Council wants to create the foundations for <strong>more flexible pension models</strong>, with a view to a future individualisation of the reference age. Whether working longer pays off is also a tax question – our <a href="rechner.html">tax calculator</a> provides model calculations for marginal tax rates and deductions.</p>"""),
 ("Current law and consultation draft compared",
  """<p>The table below contrasts the law in force (as of October 2026) with the proposals of the consultation draft. Everything in the right-hand column was <strong>proposed by the Federal Council in the consultation</strong> – none of it is decided.</p>
<table>
<thead><tr><th>Area</th><th>Today (law in force)</th><th>AHV2030 consultation draft (proposal)</th></tr></thead>
<tbody>
<tr><td>AHV rate for the self-employed</td><td>max. 8.1 %; degressive scale below CHF 60,500</td><td>max. 8.7 %; scale kept, ceiling per draft CHF 40,500</td></tr>
<tr><td>Dividends to owner-shareholders</td><td>contribution-free; reclassification only case by case (unreasonably low salary + excessive dividend)</td><td>share above 15 % return / 15 % of the tax value of the participation counts as relevant salary</td></tr>
<tr><td>Sickness/accident daily allowances</td><td>not AHV-contribution-liable</td><td>contribution-liable</td></tr>
<tr><td>BVG minimum age for early retirement</td><td>58 years</td><td>step by step 63 years, absolute floor 60; exceptions (GAV, restructurings)</td></tr>
<tr><td>Allowance on earned income after the reference age</td><td>CHF 16,800 a year</td><td>CHF 22,680 a year, regularly indexed</td></tr>
<tr><td>Pension deferral</td><td>until the 70th birthday</td><td>age cap abolished</td></tr>
<tr><td>AHV reference age</td><td>65 years</td><td>unchanged – no increase foreseen</td></tr>
</tbody>
</table>"""),
 ("Financing: everything hinges on the vote of 29 November 2026",
  """<p>AHV2030 cannot be thought of without the 13th AHV pension. It is <strong>paid for the first time in December 2026</strong> and costs more than CHF 4 billion a year initially, and more than CHF 5 billion later. On 19 June 2026 parliament decided to finance part of it via <strong>VAT</strong>: the standard rate is to rise by 0.4 percentage points from 8.1 to 8.5 per cent, the special rate for the hotel sector from 3.8 to 4.0 per cent; the reduced rate of 2.6 per cent stays unchanged. Since this requires a constitutional amendment, the people and the cantons vote on <strong>29 November 2026</strong>; the increase could enter into force in early 2028 at the earliest. More in our article on the <a href="13-ahv-rente-dezember-2026.html">13th AHV pension in December 2026</a>.</p>
<p>The outcome of that vote determines how much additional financing AHV2030 must shoulder: if the 13th pension is secured long term, the Federal Council sees in principle no need for additional financing within AHV2030. If the voters reject it or parliament decides on a limited solution only, the draft sketches alternatives – e.g. a VAT increase of 0.7 percentage points or a combination of VAT and contribution-rate increases.</p>
<p>The contribution measures contained in the draft themselves are expected to bring the AHV additional revenue of <strong>around CHF 600 million a year by 2040</strong>. As a safeguard the Federal Council also proposes an <strong>intervention mechanism</strong>: if the AHV compensation fund is set to fall below 90 per cent of one year's expenditure within the next three years, the Federal Council would have to submit stabilisation measures to parliament within a year.</p>"""),
 ("In short: what to take away now",
  """<ul>
<li><strong>Nothing is law.</strong> AHV2030 is a consultation draft (20 May – 11 Sep 2026); the dispatch follows in the first half of 2027, a popular vote is possible, entry into force is expected 2031 at the earliest.</li>
<li><strong>Self-employed</strong> would pay 8.7 instead of 8.1 per cent AHV contributions on higher incomes per the draft; the degressive scale stays but with a lower ceiling.</li>
<li><strong>Owners of AGs/GmbHs:</strong> dividends above a 15 % return on the invested capital (resp. tax value) are to count automatically as salary. The applicable practice from ruling 9C_532/2025 remains unchanged until then.</li>
<li><strong>Early-retirement plans before 2035</strong> need recalculating: the BVG minimum age is to rise step by step from 58 to 63 (floor 60, exceptions possible).</li>
<li><strong>Working longer becomes more attractive:</strong> allowance CHF 16,800 → 22,680, pension deferral also beyond 70 – all subject to parliamentary debate.</li>
<li>The next hard date is the <strong>vote of 29 November 2026</strong> on the VAT financing of the 13th AHV pension; its outcome changes AHV2030's financing needs. We will update this article after the vote.</li>
<li>This is general information, not individual advice – have your structure and pension planning reviewed by a vetted professional.</li>
</ul>"""),
]

# ---------------- French ----------------
fr_title = "AVS 2030 : ce que la réforme changerait"
fr_meta = "AVS 2030: cotisations indépendants 8,1→8,7 %, dividendes dès 15 % de rendement, âge plancher LPP 63. Ce que prévoit l'avant-projet – rien n'est encore loi."
fr_sections = [
 ("AVS 2030 est un projet en consultation – aucune ligne n'est encore loi",
  """<p><strong>AVS 2030 (AHV2030)</strong> est la plus grande réforme des assurances sociales actuellement en discussion en Suisse. Le Conseil fédéral veut sécuriser les finances de l'AVS pour la période 2030 à 2040 et adapter l'assurance aux évolutions de la société : les générations du baby-boom partent à la retraite, la pénurie de main-d'œuvre qualifiée s'aggrave et la 13e rente AVS coûtera plus de 4 milliards de francs par an dès décembre 2026.</p>
<p>Point important avant chaque chiffre de cet article : AVS 2030 n'est <strong>pas une loi adoptée</strong>. Le Conseil fédéral a ouvert la consultation le 20 mai 2026 ; elle a duré jusqu'au 11 septembre 2026. Toutes les mesures décrites ici sont des <strong>propositions de l'avant-projet</strong> – le Parlement, un éventuel référendum et le peuple peuvent encore modifier chaque détail. Ce que le projet ne contient <em>pas</em> : une augmentation de l'âge de référence AVS. Le Conseil fédéral y renonce expressément ; une commission d'experts examinera des modèles pour des réformes ultérieures.</p>
<p>La réforme remonte à une motion de la Commission de la sécurité sociale et de la santé du Conseil national, qui exigeait une stabilisation de l'AVS pour 2030–2040. Trois groupes sont particulièrement concernés : les <strong>indépendants</strong> (taux de cotisation), les <strong>propriétaires de SA et de Sàrl</strong> (dividendes) et toute personne planifiant une <strong>retraite anticipée</strong> (2e pilier).</p>"""),
 ("Calendrier : message au premier semestre 2027, entrée en vigueur au plus tôt en 2031",
  """<p>Le calendrier de la réforme figure dans les documents officiels de la Confédération :</p>
<ul>
<li><strong>20 mai 2026 :</strong> le Conseil fédéral ouvre la consultation sur la réforme AVS 2030.</li>
<li><strong>11 septembre 2026 :</strong> le délai de consultation échoit ; cantons, partis et associations ont pris position.</li>
<li><strong>Premier semestre 2027 :</strong> le Conseil fédéral entend adopter le message au Parlement – comme indiqué dans ses objectifs publiés pour 2027. Les résultats de la consultation, l'issue de la votation TVA du 29 novembre 2026 et les perspectives financières actualisées y seront intégrés.</li>
<li><strong>Ensuite :</strong> délibérations parlementaires ; selon leur cours, un référendum est possible, une votation populaire devrait avoir lieu en 2029 ou 2030.</li>
<li><strong>Au plus tôt 2031 :</strong> entrée en vigueur. Le rapport explicatif calcule les effets financiers des mesures à partir de 2031 ; l'Office fédéral des assurances sociales (OFAS) souligne que les questions sur l'entrée en vigueur et les modalités ne peuvent pas encore être tranchées aujourd'hui.</li>
</ul>
<p>Pour votre planification : il reste une fenêtre de plusieurs années – mais si vous dirigez une SA/Sàrl ou envisagez une retraite anticipée, vous devez connaître la direction, car les restructurations prennent du temps.</p>"""),
 ("Indépendants : le taux AVS passerait de 8,1 à 8,7 pour cent",
  """<p>Aujourd'hui, les indépendants paient un taux AVS plus bas sur leur revenu lucratif que les salariés : au maximum <strong>8,1 pour cent</strong> (art. 8 LAVS), alors que les salariés atteignent <strong>8,7 pour cent</strong> avec la part employeur (4,35 chacun). Pour les revenus plus faibles, une <strong>échelle dégressive</strong> s'applique aux indépendants : quiconque gagne moins de 60 500 francs par an paie progressivement moins, jusqu'à un taux minimal de 4,35 pour cent. Dans les deux cas, les cotisations AI et APG s'y ajoutent.</p>
<p>L'avant-projet propose d'aligner le taux maximal des indépendants à revenu plus élevé <strong>sur celui des salariés – 8,7 au lieu de 8,1 pour cent</strong>. L'échelle dégressive est maintenue dans son principe mais ne s'appliquerait, selon l'avant-projet, que jusqu'à un plafond de <strong>40 500 francs</strong> (60 500 aujourd'hui). Le Conseil fédéral invoque l'égalité de traitement et la neutralité concurrentielle : selon le rapport explicatif, plus de 70 pour cent des indépendants profitent aujourd'hui de l'échelle et leur revenu n'est grevé en moyenne que de 7,2 pour cent.</p>
<p><strong>Exemple :</strong> une architecte indépendante réalise un revenu déterminant de <strong>CHF 90 000</strong>. Selon le droit actuel, sa cotisation AVS s'élève à 8,1 % = <strong>CHF 7 290</strong> par an (cotisations AI et APG en sus). Au taux proposé de 8,7 %, ce serait <strong>CHF 7 830</strong> – une charge supplémentaire de <strong>CHF 540 par an</strong>. (Calcul illustratif avec les taux mentionnés dans l'avant-projet – rien n'est décidé.)</p>
<p>L'effet inverse souligné par le Conseil fédéral : des cotisations plus élevées signifient aussi un revenu déterminant plus élevé et donc tendanciellement de <strong>meilleures rentes</strong>. Peu change pour les indépendants à faible revenu – l'échelle continue de les protéger. Les détails des taux actuels et de la cotisation minimale figurent dans notre article sur la <a href="ahv-mindestbeitrag-selbststaendige.html">cotisation AVS minimale des indépendants</a>.</p>"""),
 ("Propriétaires de SA et Sàrl : les dividendes au-delà de 15 % de rendement deviennent cotisables",
  """<p>Le deuxième grand volet vise les entrepreneurs-actionnaires. Les dividendes sont aujourd'hui en principe exonérés de cotisations – quiconque se verse un dividende élevé au lieu d'un salaire économise des cotisations AVS. Le Conseil fédéral veut lutter contre cela avec un <strong>seuil légal</strong> : à l'avenir, un dividende serait réputé « excessif » lorsque son <strong>rendement dépasse 15 pour cent du capital investi</strong>. La part excédentaire serait considérée comme salaire déterminant et soumise à cotisations.</p>
<p>Le texte de l'avant-projet (nouvel art. 5 al. 2ter LAVS) précise : est déterminante la part du revenu de droits de participation versée par l'employeur qui dépasse, par an, <strong>15 pour cent de la valeur fiscale de ces droits</strong> ; la valeur fiscale est établie par les autorités fiscales cantonales. Selon le rapport explicatif, la règle vise les employés-actionnaires détenant <strong>au moins 10 pour cent du capital social</strong>.</p>
<p>Aujourd'hui, les caisses de compensation n'interviennent qu'au cas par cas : elles requalifient des dividendes en salaire lorsque le salaire est anormalement bas <em>et</em> le dividende manifestement excessif – récemment confirmé par le Tribunal fédéral dans l'arrêt <a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">9C_532/2025 sur le percement de la holding</a>. L'avant-projet transformerait cette pratique en un seuil fixe et automatique – sans que la caisse doive prouver une disproportion dans le cas concret. C'était justement un point controversé en consultation : les milieux économiques jugent 15 pour cent trop bas, les fonds propres de PME exigeant un rendement de risque supérieur.</p>
<p>Important : là encore, il s'agit <strong>d'une proposition, pas d'une loi</strong>. Les SA et Sàrl propriétaires qui fixent aujourd'hui salaire et dividende continuent de suivre la jurisprudence en vigueur – le seuil AVS 2030 n'arriverait qu'en 2031 au plus tôt.</p>""" + CTA_FR),
 ("Combler les lacunes de cotisation : indemnités journalières, rachats LPP et plateformes",
  """<p>Outre les deux grands leviers, l'avant-projet contient d'autres mesures contributives que le Conseil fédéral qualifie de « comblement des lacunes de cotisation » :</p>
<ul>
<li><strong>Les indemnités journalières de l'assurance-maladie et accidents deviennent cotisables.</strong> Jusqu'ici elles sont exemptées des cotisations AVS – contrairement à celles de l'AC, des APG, de l'AI ou de l'AM. Cela doit être aligné ; selon le Conseil fédéral, cela améliore les rentes futures des personnes concernées.</li>
<li><strong>Rachats dans le 2e pilier :</strong> les indépendants ne devraient plus pouvoir soustraire leurs rachats volontaires dans la prévoyance professionnelle aux cotisations AVS dans la mesure actuelle – égalité avec les salariés.</li>
<li><strong>Obligation d'annoncer pour les plateformes :</strong> les plateformes électroniques devraient annoncer les revenus d'activité lucrative, rendant visibles les lacunes liées aux activités « gig » et accessoires.</li>
<li><strong>Modernisation :</strong> meilleur échange de données sur les personnes sans activité lucrative, administration des salaires simplifiée par des tiers spécialisés (payrolling) et adaptations de l'assujettissement.</li>
</ul>
<p>Pertinent pour les employeurs : si les indemnités journalières deviennent cotisables, le décompte salarial inclurait à l'avenir aussi les cotisations sociales sur les indemnités maladie – un point que les participants à la consultation ont jugé controversé.</p>"""),
 ("Retraite anticipée dans le 2e pilier : l'âge minimal passe de 58 à 63 ans",
  """<p>Le point le plus incisif pour les salariés concerne la prévoyance professionnelle : <strong>l'âge minimal de la retraite anticipée doit passer progressivement de 58 à 63 ans</strong>. Des exceptions restent possibles selon le Conseil fédéral, notamment en cas de restructuration d'entreprise ou dans le cadre de conventions collectives de travail ; un <strong>plancher absolu de 60 ans</strong> s'applique dans tous les cas.</p>
<p>Les personnes quittant la vie active de manière anticipée resteraient assurées dans le 2e pilier et pourraient transférer leur prestation de sortie à une nouvelle institution de prévoyance. Les modalités concrètes et les règles transitoires sont ouvertes – l'OFAS indique dans sa FAQ que les questions sur l'entrée en vigueur et l'aménagement du relèvement ne peuvent pas être tranchées aujourd'hui.</p>
<p>Concrètement, la proposition signifie : quiconque planifie une retraite anticipée entre 58 et 63 ans devrait à l'avenir disposer d'une exception (CCT, restructuration) ou combler soi-même la lacune jusqu'au premier retrait LPP possible. C'est précisément le rôle des <a href="ueberbrueckungsleistungen-ahv-fruehpensionierung.html">prestations transitoires pour les chômeurs âgés</a> – qui peut les demander et ce qu'elles versent est expliqué dans l'article lié. Pour la plupart des personnes concernées, c'est un thème de planification qui se compte en années, pas en mois.</p>"""),
 ("Travailler au-delà de l'âge de référence : montant exonéré plus élevé, ajournement sans limite d'âge",
  """<p>Au lieu de relever l'âge de la retraite, le Conseil fédéral veut rendre le travail jusqu'à l'âge de référence et au-delà plus attrayant. Trois incitations figurent dans l'avant-projet :</p>
<ol>
<li><strong>Montant exonéré revu à la hausse :</strong> les personnes qui continuent de travailler après l'âge de référence bénéficient aujourd'hui d'un montant exonéré de 16 800 francs par an, sur lequel aucune cotisation AVS n'est perçue. L'avant-projet le porte à <strong>22 680 francs</strong> et prévoit son adaptation régulière. Ce revenu serait en outre mieux pris en compte dans le calcul de la rente.</li>
<li><strong>Ajournement au-delà de 70 ans :</strong> aujourd'hui, la rente AVS ne peut être ajournée qu'au plus tard jusqu'au 70e anniversaire. Cette limite doit disparaître – l'ajournement serait possible au-delà, avec poursuite des cotisations AVS.</li>
<li><strong>Nouveaux taux de réduction et de majoration :</strong> les taux actuariels du retrait anticipé et de l'ajournement seraient fixés selon des principes d'incitation positifs et négatifs, et non plus selon l'espérance de vie.</li>
</ol>
<p>En parallèle, le Conseil fédéral veut créer les bases de <strong>modèles de rente plus flexibles</strong>, en vue d'une individualisation future de l'âge de référence. Savoir si travailler plus longtemps en vaut la peine est aussi une question fiscale – notre <a href="rechner.html">calculateur d'impôts</a> fournit des calculs types sur le taux marginal et les déductions.</p>"""),
 ("Droit en vigueur et avant-projet en un coup d'œil",
  """<p>Le tableau ci-dessous confronte le droit en vigueur (état : octobre 2026) aux propositions de l'avant-projet. Tout ce qui figure dans la colonne de droite a été <strong>proposé par le Conseil fédéral dans la consultation</strong> – rien n'est décidé.</p>
<table>
<thead><tr><th>Domaine</th><th>Aujourd'hui (droit en vigueur)</th><th>Avant-projet AVS 2030 (proposition)</th></tr></thead>
<tbody>
<tr><td>Taux de cotisation AVS des indépendants</td><td>max. 8,1 % ; échelle dégressive sous CHF 60 500</td><td>max. 8,7 % ; échelle maintenue, plafond selon projet CHF 40 500</td></tr>
<tr><td>Dividendes aux entrepreneurs-actionnaires</td><td>non cotisables ; requalification au cas par cas (salaire anormalement bas + dividende excessif)</td><td>la part dépassant 15 % de rendement / 15 % de la valeur fiscale de la participation est réputée salaire déterminant</td></tr>
<tr><td>Indemnités journalières maladie/accident</td><td>non soumises aux cotisations AVS</td><td>soumises à cotisations</td></tr>
<tr><td>Âge minimal LPP pour la retraite anticipée</td><td>58 ans</td><td>progressivement 63 ans, plancher absolu 60 ; exceptions (CCT, restructurations)</td></tr>
<tr><td>Montant exonéré sur le revenu après l'âge de référence</td><td>CHF 16 800 par an</td><td>CHF 22 680 par an, adaptation régulière</td></tr>
<tr><td>Ajournement de la rente</td><td>jusqu'au 70e anniversaire</td><td>limite d'âge supprimée</td></tr>
<tr><td>Âge de référence AVS</td><td>65 ans</td><td>inchangé – aucune augmentation prévue</td></tr>
</tbody>
</table>"""),
 ("Financement : tout dépend de la votation du 29 novembre 2026",
  """<p>AVS 2030 ne peut pas se penser sans la 13e rente AVS. Elle sera <strong>versée pour la première fois en décembre 2026</strong> et coûte d'abord plus de 4 milliards, puis plus de 5 milliards de francs par an. Le 19 juin 2026, le Parlement a décidé d'en financer une partie via la <strong>TVA</strong> : le taux normal doit augmenter de 0,4 point, de 8,1 à 8,5 pour cent, le taux spécial de l'hôtellerie de 3,8 à 4,0 pour cent ; le taux réduit de 2,6 pour cent reste inchangé. Comme cela exige une modification de la Constitution, le peuple et les cantons voteront le <strong>29 novembre 2026</strong> ; l'augmentation pourrait entrer en vigueur au plus tôt début 2028. Plus de détails dans notre article sur la <a href="13-ahv-rente-dezember-2026.html">13e rente AVS en décembre 2026</a>.</p>
<p>L'issue de cette votation détermine le financement supplémentaire que AVS 2030 devra assumer : si la 13e rente est assurée durablement, il n'y a selon le Conseil fédéral en principe pas besoin de financement additionnel dans AVS 2030. Si le peuple refuse ou si le Parlement ne décide qu'une solution limitée, l'avant-projet esquisse des alternatives – par exemple une hausse de la TVA de 0,7 point ou une combinaison TVA/taux de cotisation.</p>
<p>Les mesures contributives contenues dans le projet devraient apporter à l'AVS des recettes supplémentaires d'<strong>environ 600 millions de francs par an d'ici 2040</strong>. Comme garde-fou, le Conseil fédéral propose en outre un <strong>mécanisme d'intervention</strong> : si le fonds de compensation AVS menace de passer sous 90 pour cent d'une dépense annuelle dans les trois ans, le Conseil fédéral devrait soumettre au Parlement des mesures de stabilisation dans l'année.</p>"""),
 ("En bref : ce que vous pouvez en retenir dès maintenant",
  """<ul>
<li><strong>Rien n'est loi.</strong> AVS 2030 est un avant-projet mis en consultation (20.5.–11.9.2026) ; le message suivra au premier semestre 2027, une votation populaire est possible, l'entrée en vigueur est attendue au plus tôt en 2031.</li>
<li><strong>Indépendants :</strong> selon le projet, les revenus plus élevés seraient cotisés à 8,7 au lieu de 8,1 pour cent ; l'échelle dégressive reste, mais avec un plafond plus bas.</li>
<li><strong>Propriétaires de SA/Sàrl :</strong> les dividendes dépassant 15 pour cent de rendement du capital investi (resp. de la valeur fiscale) seraient automatiquement réputés salaire. La pratique en vigueur issue de l'arrêt 9C_532/2025 reste inchangée d'ici là.</li>
<li><strong>Projets de retraite anticipée avant 2035 :</strong> à recalculer – l'âge minimal LPP doit passer progressivement de 58 à 63 ans (plancher 60, exceptions possibles).</li>
<li><strong>Travailler plus longtemps devient plus attractif :</strong> montant exonéré de 16 800 → 22 680 francs, ajournement de la rente possible au-delà de 70 ans – le tout sous réserve des débats parlementaires.</li>
<li>La prochaine échéance ferme est la <strong>votation du 29 novembre 2026</strong> sur le financement TVA de la 13e rente AVS ; son issue modifie les besoins de financement de AVS 2030. Nous actualiserons cet article après la votation.</li>
<li>Il s'agit d'une information générale, pas d'un conseil individuel – faites examiner votre structure et votre planification de prévoyance par un spécialiste vérifié.</li>
</ul>"""),
]

# ---------------- Italian ----------------
it_title = "Riforma AVS 2030: cosa cambierebbe"
it_meta = "AVS 2030: aliquota indipendenti 8,1→8,7 %, dividendi oltre 15 % di rendimento assoggettati, età minima LPP 63. Cosa prevede il progetto – non è legge."
it_sections = [
 ("AVS 2030 è un progetto in consultazione – nessuna riga è ancora legge",
  """<p><strong>AVS 2030 (AHV2030)</strong> è la più grande riforma delle assicurazioni sociali attualmente in discussione in Svizzera. Il Consiglio federale vuole garantire le finanze dell'AVS per il periodo 2030–2040 e adeguare l'assicurazione all'evoluzione della società: le generazioni del baby boom vanno in pensione, la carenza di personale qualificato si aggrava e la 13esima rendita AVS costerà oltre 4 miliardi di franchi all'anno dal dicembre 2026.</p>
<p>Punto importante prima di ogni cifra di questo articolo: AVS 2030 <strong>non è una legge adottata</strong>. Il Consiglio federale ha aperto la consultazione il 20 maggio 2026, conclusasi l'11 settembre 2026. Tutte le misure qui descritte sono <strong>proposte del progetto preliminare</strong> – Parlamento, eventuale referendum e corpo elettorale possono ancora modificare ogni dettaglio. Ciò che il progetto <em>non</em> contiene: un aumento dell'età di riferimento AVS. Il Consiglio federale vi rinuncia espressamente; una commissione di esperti esaminerà modelli per riforme successive.</p>
<p>La riforma risale a una mozione della Commissione della sicurezza sociale e della sanità del Consiglio nazionale, che chiedeva una stabilizzazione dell'AVS per il 2030–2040. Tre gruppi sono particolarmente toccati: gli <strong>indipendenti</strong> (aliquota contributiva), i <strong>proprietari di SA e Sagl</strong> (dividendi) e chi pianifica un <strong>pensionamento anticipato</strong> (secondo pilastro).</p>"""),
 ("Calendario: messaggio nel primo semestre 2027, entrata in vigore al più presto nel 2031",
  """<p>Il calendario della riforma figura nei documenti ufficiali della Confederazione:</p>
<ul>
<li><strong>20 maggio 2026:</strong> il Consiglio federale apre la consultazione sulla riforma AVS 2030.</li>
<li><strong>11 settembre 2026:</strong> scade il termine di consultazione; Cantoni, partiti e associazioni hanno preso posizione.</li>
<li><strong>Primo semestre 2027:</strong> il Consiglio federale intende adottare il messaggio al Parlamento – come indicato nei suoi obiettivi pubblicati per il 2027. Vi confluiranno i risultati della consultazione, l'esito della votazione IVA del 29 novembre 2026 e le prospettive finanziarie aggiornate.</li>
<li><strong>Successivamente:</strong> deliberazioni parlamentari; a seconda del corso, è possibile un referendum, con una votazione popolare presumibilmente nel 2029 o 2030.</li>
<li><strong>Al più presto 2031:</strong> entrata in vigore. Il rapporto esplicativo calcola gli effetti finanziari delle misure a partire dal 2031; l'Ufficio federale delle assicurazioni sociali (UFAS) sottolinea che le domande sull'entrata in vigore e sulle modalità non possono ancora essere chiarite oggi.</li>
</ul>
<p>Per la vostra pianificazione significa: resta una finestra di alcuni anni – ma chi gestisce una SA/Sagl o valuta un pensionamento anticipato deve conoscere la direzione, perché le ristrutturazioni richiedono tempo.</p>"""),
 ("Indipendenti: l'aliquota AVS salirebbe dall'8,1 all'8,7 per cento",
  """<p>Oggi gli indipendenti versano sul proprio reddito da attività lucrativa un'aliquota AVS più bassa dei salariati: al massimo l'<strong>8,1 per cento</strong> (art. 8 LAVS), mentre i salariati arrivano all'<strong>8,7 per cento</strong> insieme alla quota del datore di lavoro (4,35 ciascuno). Per i redditi più bassi si applica agli indipendenti una <strong>scala decrescente</strong>: chi guadagna meno di 60 500 franchi all'anno versa progressivamente meno, fino a un'aliquota minima del 4,35 per cento. In entrambi i casi si aggiungono i contributi AI e IPG.</p>
<p>Il progetto preliminare propone di allineare l'aliquota massima degli indipendenti con redditi più elevati <strong>a quella dei salariati – 8,7 invece di 8,1 per cento</strong>. La scala decrescente resta in linea di principio, ma secondo il progetto varrebbe solo fino a un tetto di <strong>40 500 franchi</strong> (oggi 60 500). Il Consiglio federale invoca la parità di trattamento e la neutralità concorrenziale: secondo il rapporto esplicativo, oggi oltre il 70 per cento degli indipendenti beneficia della scala e il loro reddito è gravato in media solo del 7,2 per cento.</p>
<p><strong>Esempio:</strong> un'architetta indipendente consegue un reddito determinante di <strong>CHF 90 000</strong>. Secondo il diritto vigente il suo contributo AVS è dell'8,1 % = <strong>CHF 7 290</strong> all'anno (contributi AI e IPG esclusi). Con l'aliquota proposta dell'8,7 % sarebbero <strong>CHF 7 830</strong> – un onere aggiuntivo di <strong>CHF 540 all'anno</strong>. (Calcolo illustrativo con le aliquote indicate nel progetto – nulla è deciso.)</p>
<p>L'effetto opposto sottolineato dal Consiglio federale: contributi più elevati significano anche un reddito determinante più alto e quindi tendenzialmente <strong>rendite migliori</strong>. Poco cambia per gli indipendenti con redditi bassi – la scala continua a proteggerli. I dettagli sulle aliquote attuali e sul contributo minimo sono nel nostro articolo sul <a href="ahv-mindestbeitrag-selbststaendige.html">contributo AVS minimo per gli indipendenti</a>.</p>"""),
 ("Proprietari di SA e Sagl: i dividendi oltre il 15 % di rendimento diventano assoggettati",
  """<p>Il secondo grande pilastro riguarda gli imprenditori-azionisti. I dividendi sono oggi di principio esenti da contributi – chi si versa un dividendo elevato invece del salario risparmia contributi AVS. Il Consiglio federale vuole contrastarlo con una <strong>soglia legale</strong>: in futuro un dividendo sarebbe considerato «eccessivo» quando il suo <strong>rendimento supera il 15 per cento del capitale investito</strong>. L'importo eccedente varrebbe come salario determinante e sarebbe assoggettato a contributi.</p>
<p>Il testo del progetto (nuovo art. 5 cpv. 2ter LAVS) precisa: è determinante la quota del reddito da diritti di partecipazione versata dal datore di lavoro che supera, all'anno, il <strong>15 per cento del valore fiscale di tali diritti</strong>; il valore fiscale è stabilito dalle autorità fiscali cantonali. Secondo il rapporto esplicativo, la regola si rivolge ai dipendenti-azionisti che detengono <strong>almeno il 10 per cento del capitale sociale</strong>.</p>
<p>Oggi le casse di compensazione intervengono solo caso per caso: riqualificano i dividendi come salario quando il salario è iniquamente basso <em>e</em> il dividendo manifestamente eccessivo – da ultimo confermato dal Tribunale federale nella sentenza <a href="dividenden-ahv-pflicht-bge-9c-532-2025.html">9C_532/2025 sul superamento della holding</a>. Il progetto trasformerebbe questa prassi in una soglia fissa e automatica – senza che la cassa debba provare una sproporzione nel caso concreto. Proprio questo era controverso in consultazione: gli ambienti economici ritengono il 15 per cento troppo basso, poiché il capitale proprio delle PMI richiede un rendimento di rischio più elevato.</p>
<p>Importante: anche in questo caso si tratta <strong>di una proposta, non di una legge</strong>. Le SA e Sagl proprietarie che fissano oggi salario e dividendi continuano a seguire la giurisprudenza vigente – la soglia AVS 2030 arriverebbe al più presto nel 2031.</p>""" + CTA_IT),
 ("Colmare le lacune contributive: indennità giornaliere, riscatti LPP e piattaforme",
  """<p>Oltre alle due grandi leve, il progetto contiene altre misure contributive che il Consiglio federale definisce «colmare le lacune contributive»:</p>
<ul>
<li><strong>Le indennità giornaliere di malattia e infortunio diventano assoggettate ai contributi.</strong> Finora sono esenti dai contributi AVS – a differenza di quelle dell'AD, delle IPG, dell'AI o dell'assicurazione militare. La situazione va allineata; secondo il Consiglio federale ciò migliora le rendite future delle persone interessate.</li>
<li><strong>Riscatti nel secondo pilastro:</strong> gli indipendenti non potranno più sottrarre nella misura attuale i riscatti facoltativi nella previdenza professionale dall'assoggettamento AVS – parità con i salariati.</li>
<li><strong>Obbligo di comunicazione per le piattaforme:</strong> le piattaforme elettroniche dovrebbero comunicare i redditi da attività lucrativa, rendendo visibili le lacune dovute a lavori «gig» e attività accessorie.</li>
<li><strong>Modernizzazione:</strong> migliore scambio di dati sulle persone senza attività lucrativa, amministrazione dei salari semplificata tramite terzi specializzati (payrolling) e adeguamenti dell'assoggettamento assicurativo.</li>
</ul>
<p>Rilevante per i datori di lavoro: se le indennità giornaliere diventano assoggettate, il conteggio salariale comprenderebbe in futuro anche i contributi sociali sulle indennità di malattia – un punto giudicato controverso dai partecipanti alla consultazione.</p>"""),
 ("Pensionamento anticipato nel secondo pilastro: l'età minima sale da 58 a 63 anni",
  """<p>Il punto più incisivo per i salariati riguarda la previdenza professionale: <strong>l'età minima per il pensionamento anticipato deve salire gradualmente dagli attuali 58 a 63 anni</strong>. Eccezioni restano possibili secondo il Consiglio federale, in particolare in caso di ristrutturazioni aziendali o nell'ambito di contratti collettivi di lavoro; in ogni caso vale un <strong>limite assoluto di 60 anni</strong>.</p>
<p>Le persone che lasciano anticipatamente la vita attiva resterebbero assicurate nel secondo pilastro e potrebbero trasferire la propria prestazione d'uscita a un nuovo istituto di previdenza. Le modalità concrete e le regole transitorie sono aperte – l'UFAS indica nella sua FAQ che le domande sull'entrata in vigore e sull'impostazione dell'innalzamento non possono essere chiarite oggi.</p>
<p>In pratica la proposta significa: chi pianifica un pensionamento anticipato tra i 58 e i 63 anni dovrebbe in futuro disporre di un'eccezione (CCL, ristrutturazione) o colmare da sé la lacuna fino al primo prelievo LPP possibile. È esattamente il compito delle <a href="ueberbrueckungsleistungen-ahv-fruehpensionierung.html">prestazioni transitorie per i disoccupati anziani</a> – chi può richiederle e cosa erogano è spiegato nell'articolo collegato. Per la maggior parte degli interessati è un tema di pianificazione con un orizzonte di anni, non di mesi.</p>"""),
 ("Lavorare oltre l'età di riferimento: importo esentato più alto, rinvio senza limite d'età",
  """<p>Invece di aumentare l'età di pensionamento, il Consiglio federale vuole rendere più attrattivo il lavoro fino all'età di riferimento e oltre. Tre incentivi figurano nel progetto:</p>
<ol>
<li><strong>Importo esentato più alto:</strong> chi continua a lavorare dopo l'età di riferimento beneficia oggi di un importo esentato di 16 800 franchi all'anno, sul quale non sono prelevati contributi AVS. Il progetto lo porta a <strong>22 680 franchi</strong> e ne prevede l'adeguamento regolare. Questo reddito sarebbe inoltre considerato maggiormente nel calcolo della rendita.</li>
<li><strong>Rinvio oltre i 70 anni:</strong> oggi la rendita AVS può essere rinviata al massimo fino al 70° compleanno. Questo limite deve cadere – il rinvio sarebbe possibile anche oltre, continuando a versare contributi AVS.</li>
<li><strong>Nuove aliquote di riduzione e aumento:</strong> le aliquote attuariali del prelievo anticipato e del rinvio sarebbero fissate secondo principi di incentivo positivi e negativi, e non più in base all'aspettativa di vita.</li>
</ol>
<p>In parallelo, il Consiglio federale vuole creare le basi per <strong>modelli di rendita più flessibili</strong>, in vista di una futura individualizzazione dell'età di riferimento. Se lavorare più a lungo convenga è anche una questione fiscale – il nostro <a href="rechner.html">calcolatore d'imposte</a> offre calcoli tipo su aliquota marginale e deduzioni.</p>"""),
 ("Diritto vigente e progetto preliminare a confronto",
  """<p>La tabella seguente confronta il diritto in vigore (stato: ottobre 2026) con le proposte del progetto preliminare. Tutto ciò che figura nella colonna di destra è stato <strong>proposto dal Consiglio federale nella consultazione</strong> – nulla è deciso.</p>
<table>
<thead><tr><th>Ambito</th><th>Oggi (diritto in vigore)</th><th>Progetto AVS 2030 (proposta)</th></tr></thead>
<tbody>
<tr><td>Aliquota contributiva AVS degli indipendenti</td><td>max. 8,1 %; scala decrescente sotto CHF 60 500</td><td>max. 8,7 %; scala mantenuta, tetto secondo progetto CHF 40 500</td></tr>
<tr><td>Dividendi agli imprenditori-azionisti</td><td>esenti; riqualificazione solo caso per caso (salario iniquamente basso + dividendo eccessivo)</td><td>la quota oltre il 15 % di rendimento / 15 % del valore fiscale della partecipazione vale come salario determinante</td></tr>
<tr><td>Indennità giornaliere malattia/infortunio</td><td>non assoggettate ai contributi AVS</td><td>assoggettate a contributi</td></tr>
<tr><td>Età minima LPP per il pensionamento anticipato</td><td>58 anni</td><td>gradualmente 63 anni, limite assoluto 60; eccezioni (CCL, ristrutturazioni)</td></tr>
<tr><td>Importo esentato sul reddito dopo l'età di riferimento</td><td>CHF 16 800 all'anno</td><td>CHF 22 680 all'anno, adeguamento regolare</td></tr>
<tr><td>Rinvio della rendita</td><td>fino al 70° compleanno</td><td>limite d'età soppresso</td></tr>
<tr><td>Età di riferimento AVS</td><td>65 anni</td><td>invariata – nessun aumento previsto</td></tr>
</tbody>
</table>"""),
 ("Finanziamento: tutto dipende dalla votazione del 29 novembre 2026",
  """<p>AVS 2030 non si può pensare senza la 13esima rendita AVS. Sarà <strong>versata per la prima volta nel dicembre 2026</strong> e costa inizialmente oltre 4 miliardi, in seguito oltre 5 miliardi di franchi all'anno. Il 19 giugno 2026 il Parlamento ha deciso di finanziarne una parte tramite l'<strong>IVA</strong>: l'aliquota normale deve aumentare di 0,4 punti percentuali, dall'8,1 all'8,5 per cento, l'aliquota speciale per l'albergheria dal 3,8 al 4,0 per cento; l'aliquota ridotta del 2,6 per cento resta invariata. Poiché ciò richiede una modifica costituzionale, popolo e Cantoni voteranno il <strong>29 novembre 2026</strong>; l'aumento potrebbe entrare in vigore al più presto all'inizio del 2028. Maggiori dettagli nel nostro articolo sulla <a href="13-ahv-rente-dezember-2026.html">13esima rendita AVS di dicembre 2026</a>.</p>
<p>L'esito di questa votazione determina quanto finanziamento aggiuntivo AVS 2030 dovrà sostenere: se la 13esima rendita sarà assicurata durevolmente, secondo il Consiglio federale in linea di principio non servirà un finanziamento supplementare nell'ambito di AVS 2030. Se il popolo la respinge o il Parlamento decide solo una soluzione limitata, il progetto abbozza alternative – ad esempio un aumento IVA di 0,7 punti o una combinazione IVA/aliquota contributiva.</p>
<p>Le misure contributive contenute nel progetto dovrebbero portare all'AVS entrate supplementari per <strong>circa 600 milioni di franchi all'anno entro il 2040</strong>. Come salvaguardia il Consiglio federale propone inoltre un <strong>meccanismo d'intervento</strong>: se il fondo di compensazione AVS minacciasse di scendere sotto il 90 per cento di una spesa annuale entro i prossimi tre anni, il Consiglio federale dovrebbe sottoporre al Parlamento misure di stabilizzazione entro un anno.</p>"""),
 ("In breve: cosa trarne già ora",
  """<ul>
<li><strong>Nulla è legge.</strong> AVS 2030 è un progetto posto in consultazione (20.5.–11.9.2026); il messaggio seguirà nel primo semestre 2027, una votazione popolare è possibile, l'entrata in vigore è attesa al più presto nel 2031.</li>
<li><strong>Indipendenti:</strong> secondo il progetto, i redditi più elevati sarebbero assoggettati all'8,7 invece dell'8,1 per cento; la scala decrescente resta, ma con un tetto più basso.</li>
<li><strong>Proprietari di SA/Sagl:</strong> i dividendi oltre il 15 per cento di rendimento del capitale investito (risp. del valore fiscale) varrebbero automaticamente come salario. La prassi vigente confermata dalla sentenza 9C_532/2025 resta invariata fino ad allora.</li>
<li><strong>Piani di pensionamento anticipato prima del 2035:</strong> da ricalcolare – l'età minima LPP deve salire gradualmente da 58 a 63 anni (limite 60, eccezioni possibili).</li>
<li><strong>Lavorare più a lungo diventa più attrattivo:</strong> importo esentato da 16 800 a 22 680 franchi, rinvio della rendita possibile anche oltre i 70 anni – il tutto con riserva delle deliberazioni parlamentari.</li>
<li>La prossima scadenza certa è la <strong>votazione del 29 novembre 2026</strong> sul finanziamento IVA della 13esima rendita AVS; il suo esito modifica il fabbisogno di finanziamento di AVS 2030. Aggiorneremo questo articolo dopo la votazione.</li>
<li>Si tratta di informazione generale, non di consulenza individuale – fate esaminare la vostra struttura e la vostra pianificazione previdenziale da uno specialista verificato.</li>
</ul>"""),
]

# ---------------- build + verify ----------------
for lang, title, meta, sections in [("de", de_title, de_meta, de_sections),
                                    ("en", en_title, en_meta, en_sections),
                                    ("fr", fr_title, fr_meta, fr_sections),
                                    ("it", it_title, it_meta, it_sections)]:
    assert len(title) <= 40, f"{lang}: title too long ({len(title)})"
    assert len(title) + len(" | steuerberatung.ch") <= 62, f"{lang}: total title too long"
    assert len(meta) <= 158, f"{lang}: meta too long ({len(meta)})"
    assert 8 <= len(sections) <= 10, f"{lang}: {len(sections)} sections (need 8-10)"
    build(lang, SLUG, title, meta, sections, related=RELATED, sources=SOURCES[lang])

BASE = os.path.dirname(HERE)
def words(path):
    txt = re.sub(r"<(script|style).*?</\1>", " ", open(path, encoding="utf-8").read(), flags=re.S)
    main = re.search(r"<main>(.*?)</main>", txt, re.S)
    txt = main.group(1) if main else txt
    txt = re.sub(r'<nav class="toc">.*?</nav>', " ", txt, flags=re.S)
    txt = re.sub(r'<section class="section sources">.*?</section>', " ", txt, flags=re.S)
    txt = re.sub(r'<!-- RELATED:START -->.*?<!-- RELATED:END -->', " ", txt, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    return len(txt.split())

report = {"slug": SLUG, "date": datetime.date.today().isoformat(), "languages": {}}
for lang in ["de", "en", "fr", "it"]:
    p = os.path.join(BASE, "" if lang == "de" else lang, SLUG + ".html")
    h = open(p, encoding="utf-8").read()
    report["languages"][lang] = {
        "path": os.path.relpath(p, BASE),
        "bytes": len(h),
        "main_words": words(p),
        "cta_mid": '<div class="cta-mid">' in h,
        "example": ("Beispiel:" if lang == "de" else "Example:" if lang == "en" else "Exemple" if lang == "fr" else "Esempio:") in h,
        "h2_sections": h.count('<h2 id="s'),
        "table": "<table>" in h,
    }

# cross-language leakage spot-checks (strip tags/attrs first)
def body_text(path):
    t = open(path, encoding="utf-8").read()
    t = re.sub(r'<(script|style).*?</\1>', " ", t, flags=re.S)
    t = re.sub(r'<[^>]+>', " ", t)
    return t

leaks = []
checks = {
    "en": ["Selbstständig", "Vernehmlassung", "Beitragssatz", "Vorentwurf", "Frühpensionierung"],
    "fr": ["Selbstständig", "Vernehmlassung", "Beitragssatz", "Vorentwurf", "Frühpensionierung"],
    "it": ["Selbstständig", "Vernehmlassung", "Beitragssatz", "Vorentwurf", "Frühpensionierung"],
    "de": ["self-employed", "consultation draft", "indépendants", "indipendenti"],
}
for lang, needles in checks.items():
    txt = body_text(os.path.join(BASE, "" if lang == "de" else lang, SLUG + ".html"))
    for n in needles:
        if n in txt:
            leaks.append(f"{lang}: found '{n}'")
report["cross_language_leaks"] = leaks
assert not leaks, leaks

rp = os.path.join(HERE, "_publish_20261021_ahv2030_report.json")
json.dump(report, open(rp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("report:", rp)
print(json.dumps(report, ensure_ascii=False, indent=2))
