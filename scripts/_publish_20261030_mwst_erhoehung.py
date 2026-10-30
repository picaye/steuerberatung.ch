#!/usr/bin/env python3
"""Build mwst-erhoehung-2027-ahv-armee in all 4 languages (cron 2026-10-30, pin fired).

Facts verified 2026-10-30 against official sources (all curl 200):
- BSV vote page (bsv.admin.ch/de/abstimmung-13-ahv-rente): vote on the
  Zusatzfinanzierung is 29.11.2026; parliament decision June 2026:
  Normalsatz 8.1 -> 8.5 % (+0.4 pp), Sondersatz Hotellerie 3.8 -> 4.0 %
  (+0.2 pp), reduzierter Satz 2.6 % UNCHANGED; Ertrag ~CHF 1 Mrd. 2028,
  ~1.4 Mrd./Jahr ab 2029; Inkrafttreten fruehestens Anfang 2028; 13. Rente
  Dec 2026 an ~2.6 Mio. Rentner (unverheiratet bis 2'520/Jahr, Ehepaare bis
  3'780); Kosten >4 Mrd. 2026, >5 Mrd./Jahr ab 2035; Defizit 2035 ~3 statt
  ~5 Mrd.; AHV-Fonds 2035 ~70 % statt ~50 %; unbefristet (NR wollte Befristung
  Ende 2033, StR lehnte Befristung ab); Lohnbeitragserhoehung 0.2 pp vom NR
  abgelehnt (98:96).
- admin.ch Volksabstimmung 29.11.2026: 4 Vorlagen, Nr. 1 = Bundesbeschluss
  vom 19. Juni 2026 ueber die Zusatzfinanzierung der AHV (obligatorische
  Volksabstimmung, Volk+Staende).
- ESTV Rate page (estv.admin.ch/de/mwst-steuersaetze-schweiz): current
  8.1/2.6/3.8 since 1.1.2024.
- Fedlex BBl 2026 2354 (de/fr/it) + MM 12.08.2026 (admin.ch/newnsb/
  oGUkWkIOK86tJ_eqjt5Ng): Botschaft Ruestungsfinanzierung: Normalsatz
  +0.5 pp BEFRISTET 12 Jahre ab 2028, Sondersatz +0.3 pp (+0.2 pp falls
  AHV-Vorlage angenommen), reduzierter Satz nicht erhoeht; Mehreinnahmen
  ~24 Mrd. (15 Mrd. Faehigkeitsaufbau + 9 Mrd. Preissteigerungen);
  verschuldungsfaehiger Ruestungsfonds, Schulden max 6 Mrd., schuldenfrei
  am Ende der Befristung; Ziel Volksabstimmung Sommer 2027; Geschaeft 26.051.
- SRG-Trendumfrage 1. Welle (Erhebung bis 18.10.2026, Mitte): Nein 49 % /
  Ja 46 %. (Erwaehnt als Zwischenstand.)
- ESTV-Schaetzung Mehrkosten ~CHF 180/Jahr/Haushalt (via SRF-Abstimmungs-
  dossier, beruht auf ESTV-Angabe).
Rechenbeispiele: node-Arithmetik (Preisdurchleitung, gross-price basis):
  +0.4 pp => *108.5/108.1 = +0.370 % auf Normalsatz-Konsum;
  +0.9 pp => *109.0/108.1 = +0.833 %;
  Familie (16'800 Konsum normal + 2'000 Hotellerie): +66 CHF/J (AHV yes),
  +148 CHF/J (AHV+Armee); Hotellerie 3.8->4.0 = 104.0/103.8, ->4.2 = 104.2/103.8;
  Selbststaendige 160'000 Umsatz: 12'960 -> 13'600 (+640 reine Durchleitung);
  Rentner netto: 2'520 - 180 = +2'340/Jahr.
Rollenverteilung laut Correction-Cards 2026-09-19/2026-10-07: dieses Stueck
ist das Erklaer-Stueck zur Abstimmung; Betriebs-Praxis des Satzwechsels
(Anzahlungen, Dauerrechnungen) gehoert zum Card mwst-wechsel-8-5-prozent-praxis
(pin 2027-03-12) — hier nur zusammengefasst erwaehnt.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "mwst-erhoehung-2027-ahv-armee"
RELATED = ["13-ahv-rente-dezember-2026.html",
           "mwst-100k-pflicht-schweiz.html",
           "steuer-checkliste-2026.html"]

SOURCES = {
 "de": [
   ("https://www.bsv.admin.ch/de/abstimmung-13-ahv-rente",
    "BSV: 13. AHV-Rente – Volksabstimmung über die Zusatzfinanzierung (29.11.2026)"),
   ("https://www.admin.ch/de/volksabstimmung-vom-29-november-2026",
    "Bundeskanzlei: Vorlage «AHV-Zusatzfinanzierung» am 29. November 2026"),
   ("https://www.estv.admin.ch/de/mwst-steuersaetze-schweiz",
    "ESTV: Schweizer Mehrwertsteuersätze"),
   ("https://www.fedlex.admin.ch/eli/fga/2026/2354/de",
    "BBl 2026 2354: Botschaft zur Finanzierung der Rüstungsausgaben (12.8.2026)"),
   ("https://www.admin.ch/de/newnsb/oGUkWkIOK86tJ_eqjt5Ng",
    "Medienmitteilung des Bundesrats: befristete MWST-Erhöhung als Sicherheitsbeitrag"),
 ],
 "en": [
   ("https://www.bsv.admin.ch/de/abstimmung-13-ahv-rente",
    "FSO: 13th AHV pension – referendum on additional financing (29.11.2026, German)"),
   ("https://www.admin.ch/de/volksabstimmung-vom-29-november-2026",
    "Federal Chancellery: AHV additional financing vote of 29 November 2026 (German)"),
   ("https://www.estv.admin.ch/de/mwst-steuersaetze-schweiz",
    "FTA: Swiss VAT rates (German)"),
   ("https://www.fedlex.admin.ch/eli/fga/2026/2354/de",
    "FFe 2026 2354: Federal Council message on arms financing, 12.8.2026 (German)"),
   ("https://www.admin.ch/de/newnsb/oGUkWkIOK86tJ_eqjt5Ng",
    "Federal Council press release: temporary VAT increase for security (German)"),
 ],
 "fr": [
   ("https://www.bsv.admin.ch/de/abstimmung-13-ahv-rente",
    "OFAS : 13e rente AVS – votation sur le financement additionnel (29.11.2026, VO)"),
   ("https://www.admin.ch/de/volksabstimmung-vom-29-november-2026",
    "Chancellerie fédérale : objet « financement additionnel AVS » (VO)"),
   ("https://www.estv.admin.ch/de/mwst-steuersaetze-schweiz",
    "AFC : taux de la TVA en Suisse (VO)"),
   ("https://www.fedlex.admin.ch/eli/fga/2026/2354/fr",
    "FF 2026 2354 : message sur le financement des dépenses d'armement (12.8.2026)"),
   ("https://www.admin.ch/de/newnsb/oGUkWkIOK86tJ_eqjt5Ng",
    "Communiqué du Conseil fédéral : hausse temporaire de la TVA (VO)"),
 ],
 "it": [
   ("https://www.bsv.admin.ch/de/abstimmung-13-ahv-rente",
    "UFA: 13a rendita AVS – votazione sul finanziamento aggiuntivo (29.11.2026, TE)"),
   ("https://www.admin.ch/de/volksabstimmung-vom-29-november-2026",
    "Cancelleria federale: oggetto «finanziamento aggiuntivo AVS» (TE)"),
   ("https://www.estv.admin.ch/de/mwst-steuersaetze-schweiz",
    "AFC: aliquote dell'IVA svizzera (TE)"),
   ("https://www.fedlex.admin.ch/eli/fga/2026/2354/it",
    "FF 2026 2354: messaggio sul finanziamento delle spese militari (12.8.2026)"),
   ("https://www.admin.ch/de/newnsb/oGUkWkIOK86tJ_eqjt5Ng",
    "Comunicato del Consiglio federale: aumento temporaneo dell'IVA (TE)"),
 ],
}

# ---------------------------------------------------------------- tables
def table(lang):
    if lang == "de":
        return ('<table><tr><th>Kategorie</th><th>Heute (2026/27)</th><th>Ab 2028: AHV-Ja</th>'
                '<th>Ab 2028: AHV + Armee</th></tr>'
                '<tr><td>Normalsatz (meiste Waren &amp; Dienstleistungen)</td><td>8,1&nbsp;%</td>'
                '<td>8,5&nbsp;%</td><td>9,0&nbsp;%</td></tr>'
                '<tr><td>Sondersatz Beherbergung (Hotels)</td><td>3,8&nbsp;%</td>'
                '<td>4,0&nbsp;%</td><td>~4,2&nbsp;%</td></tr>'
                '<tr><td>Reduzierter Satz (Lebensmittel, Medikamente, Bücher)</td><td>2,6&nbsp;%</td>'
                '<td>2,6&nbsp;% <em>(unverändert)</em></td><td>2,6&nbsp;% <em>(unverändert)</em></td></tr>'
                '<tr><td>Mehrkosten Beispielhaushalt (CHF/Jahr)</td><td>–</td>'
                '<td>+66</td><td>+148</td></tr></table>')
    if lang == "en":
        return ('<table><tr><th>Category</th><th>Today (2026/27)</th><th>From 2028: AHV yes</th>'
                '<th>From 2028: AHV + army</th></tr>'
                '<tr><td>Standard rate (most goods &amp; services)</td><td>8.1&nbsp;%</td>'
                '<td>8.5&nbsp;%</td><td>9.0&nbsp;%</td></tr>'
                '<tr><td>Special rate, accommodation (hotels)</td><td>3.8&nbsp;%</td>'
                '<td>4.0&nbsp;%</td><td>~4.2&nbsp;%</td></tr>'
                '<tr><td>Reduced rate (food, medicine, books)</td><td>2.6&nbsp;%</td>'
                '<td>2.6&nbsp;% <em>(unchanged)</em></td><td>2.6&nbsp;% <em>(unchanged)</em></td></tr>'
                '<tr><td>Extra cost, example household (CHF/year)</td><td>–</td>'
                '<td>+66</td><td>+148</td></tr></table>')
    if lang == "fr":
        return ('<table><tr><th>Catégorie</th><th>Aujourd’hui (2026/27)</th><th>Dès 2028 : oui AVS</th>'
                '<th>Dès 2028 : AVS + armée</th></tr>'
                '<tr><td>Taux normal (la plupart des biens et services)</td><td>8,1&nbsp;%</td>'
                '<td>8,5&nbsp;%</td><td>9,0&nbsp;%</td></tr>'
                '<tr><td>Taux spécial, hébergement (hôtels)</td><td>3,8&nbsp;%</td>'
                '<td>4,0&nbsp;%</td><td>~4,2&nbsp;%</td></tr>'
                '<tr><td>Taux réduit (denrées, médicaments, livres)</td><td>2,6&nbsp;%</td>'
                '<td>2,6&nbsp;% <em>(inchangé)</em></td><td>2,6&nbsp;% <em>(inchangé)</em></td></tr>'
                '<tr><td>Coût supplémentaire, ménage type (CHF/an)</td><td>–</td>'
                '<td>+66</td><td>+148</td></tr></table>')
    return ('<table><tr><th>Categoria</th><th>Oggi (2026/27)</th><th>Dal 2028: sì AVS</th>'
            '<th>Dal 2028: AVS + esercito</th></tr>'
            '<tr><td>Aliquota normale (la maggior parte di beni e servizi)</td><td>8,1&nbsp;%</td>'
            '<td>8,5&nbsp;%</td><td>9,0&nbsp;%</td></tr>'
            '<tr><td>Aliquota speciale, alloggi (alberghi)</td><td>3,8&nbsp;%</td>'
            '<td>4,0&nbsp;%</td><td>~4,2&nbsp;%</td></tr>'
            '<tr><td>Aliquota ridotta (alimenti, medicinali, libri)</td><td>2,6&nbsp;%</td>'
            '<td>2,6&nbsp;% <em>(invariata)</em></td><td>2,6&nbsp;% <em>(invariata)</em></td></tr>'
            '<tr><td>Costi supplementari, nucleo tipo (CHF/anno)</td><td>–</td>'
            '<td>+66</td><td>+148</td></tr></table>')

# ---------------------------------------------------------------- German
de_title = "MWST-Erhöhung: Was AHV und Armee kosten"
de_meta = ("Am 29.11.2026 stimmt die Schweiz über +0,4 % MWST für die 13. AHV-Rente ab; "
           "der Armee-Fonds folgt 2027. Rechenbeispiele: was die neuen Sätze ab 2028 kosten.")
de_sections = [
("Was am 29. November 2026 zur Abstimmung steht",
 """<p>Am <strong>29. November 2026</strong> entscheiden die Stimmberechtigten über den «Bundesbeschluss vom 19. Juni 2026 über die Zusatzfinanzierung der AHV durch eine Erhöhung der Mehrwertsteuer». Es ist der Finanzierungsteil der 13. AHV-Rente, die das Volk im März 2024 mit 58 % angenommen hat: Die erste zusätzliche Rente wird im <strong>Dezember 2026</strong> an rund 2,6 Millionen Pensionierte ausbezahlt – unverheiratete Rentenbezüger erhalten bis zu <strong>CHF 2'520</strong> mehr pro Jahr, Ehepaare bis zu <strong>CHF 3'780</strong>. Die Kosten für die AHV: anfangs über 4, ab 2035 über 5 Milliarden Franken pro Jahr.</p>
<p>Dazu schlägt das Parlament eine Teilfinanzierung vor: Der <strong>Normalsatz steigt von 8,1 auf 8,5 %</strong> (+0,4 Prozentpunkte), der <strong>Sondersatz für Hotellerie von 3,8 auf 4,0 %</strong>. Der <strong>reduzierte Satz von 2,6 %</strong> auf Güter des täglichen Bedarfs – Lebensmittel, Medikamente, Zeitungen, Bücher – bleibt unverändert; eine ebenso diskutierte Erhöhung der AHV-Lohnbeiträge um 0,2 Punkte lehnte der Nationalrat knapp ab (98 zu 96). Die Erhöhung ist <em>unbefristet</em>.</p>
<p>Weil die Bundesverfassung geändert wird, gilt die <strong>obligatorische Volksabstimmung</strong>: nötig ist das Doppelmehr aus Volk und Ständen; Bundesrat und Parlament empfehlen die Vorlage zur Annahme. Die Mehreinnahmen betragen rund <strong>1 Milliarde Franken im Jahr 2028</strong> und ab 2029 geschätzt <strong>1,4 Milliarden pro Jahr</strong>. Wichtig für die Einordnung: In Kraft treten kann die Erhöhung <strong>frühestens Anfang 2028</strong> – die 13. Renten 2026 und 2027 werden in jedem Fall aus dem AHV-Ausgleichsfonds bezahlt, ohne Zusatzfinanzierung.</p>
<p><em>Praxis-Tipp:</em> Die Dezember-Auszahlung 2026 ist vom Urnenentscheid nicht betroffen. Ein Nein streicht die Rente nicht – es verschiebt nur die Antwort, wie sie bezahlt wird.</p>"""),
("Der Armee-Fonds: die zweite MWST-Erhöhung ab 2028",
 """<p>Das zweite Mehrwertsteuer-Projekt steckt in der Parlamentsberatung: Der Bundesrat hat am <strong>12. August 2026</strong> die Botschaft zur Finanzierung der Rüstungsausgaben der Armee vorgelegt (BBl 2026 2354, Geschäft 26.051). Vorgeschlagen: Der Normalsatz steigt per <strong>1. Januar 2028 um weitere 0,5 Prozentpunkte – befristet auf 12 Jahre</strong>, der Ertrag ist ausschliesslich für Rüstungsbeschaffungen zweckgebunden. Der Beherbergungssatz soll proportional um 0,3 Punkte steigen – um 0,2 Punkte, falls die AHV-Vorlage vorher angenommen wird. Auch hier bleibt der reduzierte Satz unangetastet.</p>
<p>Der Bedarf: rund <strong>24 Milliarden Franken</strong> – 15 Milliarden für den schnellen Fähigkeitsaufbau gegen die wahrscheinlichsten Bedrohungen (Luftverteidigung, Cyberabwehr, Drohnenabortung, Schutz kritischer Infrastruktur, Munitionsbevorratung) plus 9 Milliarden für die Preissteigerungen auf dem globalen Rüstungsmarkt. Das Geld fliesst in einen neu zu schaffenden, <strong>verschuldungsfähigen Rüstungsfonds</strong> (maximal 6 Milliarden Franken Schulden, die bis Ende der Befristung abgebaut sein müssen); über die Mittelverwendung befindet das Parlament.</p>
<p>Für die Planung zählt beides zusammen: Auch der Armee-Beschluss erfordert eine Verfassungsänderung und kommt vors Volk – der Bundesrat strebt die <strong>Volksabstimmung für den Sommer 2027</strong> an, damit die Erhöhung wie die AHV-Vorlage auf Anfang 2028 in Kraft treten kann. Bei einem Doppel-Ja läge der Normalsatz ab 2028 bei <strong>9,0 %</strong>, der Hotelsatz bei rund 4,2 %. Der Unterschied: Die Armee-Punkte sind nach 12 Jahren wieder weg, die AHV-Punkte bleiben.</p>
<p><em>Praxis-Tipp:</em> Beurteilen Sie die beiden Vorlagen getrennt – am 29. November 2026 liegt nur die AHV-Finanzierung an der Urne, die Armee-Vorlage folgt voraussichtlich 2027.</p>"""),
("Rechenbeispiel: Was die Erhöhung einen Haushalt kostet",
 """<p>Entscheidend ist nicht der Prozentpunkt, sondern die Preiswirkung auf den Konsum: Die MWST klebt auf dem Bruttopreis. Von 8,1 auf 8,5 % steigt ein normalsatz-besteuertes Produkt um 108,5/108,1 = <strong>+0,37 %</strong>; bei angenommenem Armee-Fonds (Total 9,0 %) sind es 109,0/108,1 = <strong>+0,83 %</strong>. Beispiel einer Familie mit zwei Kindern: Sie gibt pro Monat <strong>CHF 1'400</strong> für Normalsatz-Konsum aus (Restaurant, Kleidung, Benzin, Telecom, Coiffeur), <strong>CHF 600</strong> für den Grundbedarf zum reduzierten Satz und pro Jahr <strong>CHF 2'000</strong> für Hotelübernachtungen.</p>
<p>Rechnung: Nur das AHV-Ja kostet diese Familie rund <strong>CHF 66 mehr pro Jahr</strong> (CHF 62 auf den Normalsatz-Ausgaben + CHF 4 Hotellerie). Kommt der Armee-Fonds dazu, steigen die Mehrkosten auf rund <strong>CHF 148 pro Jahr</strong> – gegen CHF 12 pro Monat. Der Wocheneinkauf bleibt komplett verschont. Die ESTV schätzt die durchschnittliche Belastung durch die +0,4 Prozentpunkte auf rund <strong>CHF 180 pro Haushalt und Jahr</strong>; ein vergleichsweise hoher Normalsatz-Konsum von rund CHF 48'500 im Jahr ist dafür die Basis. Auf der Gegenseite: Eine allein stehende Pensionierte bezieht mit der 13. Rente bis zu CHF 2'520 und trägt über die MWST rund CHF 180 bei – per Saldo etwa <strong>CHF 2'340 netto pro Jahr</strong> mehr.</p>
""" + table("de") + """
<p><em>Praxis-Tipp:</em> Die Beträge gehen von einer vollen Weitergabe der Steuer aus – Detailhändler können einen Teil selbst tragen. Die Hotellerie-Werte «AHV + Armee» basieren auf dem Bundesratsentwurf; final entscheidet Parlament und Volk. Ihre persönliche Gesamtbelastung (inkl. Einkommens- und Vermögenssteuer) zeigt der <a href="rechner.html">Rechner</a>.</p>
<div class="cta-mid"><strong>Interessiert Sie Ihre Steuerbelastung über die MWST hinaus?</strong> Rechnen Sie Einkommen und Vermögen gratis im <a href="rechner.html">Steuerrechner</a> – oder lassen Sie Ihre Situation von einer geprüften Fachperson prüfen: <a href="kontakt.html">unverbindliche Offerte anfragen</a>.</div>"""),
("Bundessteuer statt Kantönligeist: überall dieselben Sätze",
 """<p>Die Mehrwertsteuer ist eine reine Bundesabgabe: erhoben von der ESTV, fliesst sie an die Bundeskasse – beim AHV-Beschluss zweckgebunden an den AHV-Ausgleichsfonds. Darum gilt die Erhöhung <strong>in allen 26 Kantonen gleich</strong>: 8,1 % heute, 8,5 % allfällig ab 2028 – in Zürich wie in Chiasso, in Genf wie in St. Gallen. Anders als bei Einkommens-, Vermögens- oder Handänderungssteuer gibt es bei der MWST keine kantonalen Unterschiede und keinen Steuerwettbewerb; ein Umzug ändert an der Konsumbelastung nichts.</p>
<p>Auch der soziale Ausgleich ist eidgenössisch einheitlich geregelt: Der reduzierte Satz auf dem Grundbedarf – Lebensmittel, Medikamente, Zeitungen, Bücher, Produkte der Monatshygiene – bleibt in <em>beiden</em> Vorlagen unverändert bei 2,6 %. Für Haushalte mit tiefem Einkommen, deren Konsumanteil am Grundbedarf hoch ist, fällt die relative Belastung deshalb kleiner aus als im Durchschnitt. Und für Grenzgänger gilt: Konsumieren sie in Deutschland, Frankreich oder Italien, zahlen sie dortige Umsatzsteuer – die Schweizer MWST-Erhöhung trifft nur den Konsum in der Schweiz.</p>
<p><em>Praxis-Tipp:</em> Rechnen Sie für MWST-Fragen nie mit Kantonsangaben aus Foren – die Zahl ist landesweit identisch. Kantonale Unterschiede gibt es erst wieder bei den direkten Steuern: Ein <a href="rechner.html">Vergleich</a> lohnt sich dort gleich doppelt.</p>"""),
("Selbstständige: Was bis zum Satzwechsel 2028 zu tun ist",
 """<p>Für MWST-pflichtige Selbstständige ist der Satzwechsel eine Buchungs-, keine Kostenfrage: Sie stellen die Steuer ihren Kunden in Rechnung und leiten sie weiter. Beispiel: Auf <strong>CHF 160'000</strong> steuerbarem Umsatz (ohne Steuer) liefert ein Coiffeurbetrieb bei 8,1 % <strong>CHF 12'960</strong> ab, bei 8,5 % <strong>CHF 13'600</strong> – die Differenz von CHF 640 gehört der Bundeskasse, und die Vorsteuer auf den eigenen Einkäufen steigt gleichzeitig. Wer unter der Umsatzgrenze von CHF 100'000 bleibt und nicht freiwillig registriert ist, stellt ohnehin keine MWST in Rechnung.</p>
<p>Zu tun bleibt bis Mitte 2027: Registrierkasse und Fakturierung rechtzeitig auf den neuen Satz stellen, laufende Dauerrechnungen und lange Aufträge mit einer Satzwechsel-Klausel versehen und ab dem Datum der Inkraftsetzung die Bruttopreise nach der Preisbekanntgabeverordnung mit dem neuen Satz ausweisen. Für Kleinbetriebe mit Saldosteuer-Methode passt die ESTV die Branchenätze an; Übergangsregelungen für Anzahlungen und Leistungen rund um den Satzwechsel kündigt der Bundesrat im MWSTG an. Die Ausführlichkeiten zum Satzwechsel – Anzahlungen, Teilleistungen, Periodenabgrenzung – behandeln wir separat, sobald Datum und Sätze fix sind.</p>
<p><em>Praxis-Tipp:</em> Wer den AGOV-Zugang zum ESTV-ePortal noch nicht hat, richtet ihn jetzt ein – Pflicht für alle Abrechnungen seit dem 31. Oktober 2026 (siehe <a href="mwst-agov-pflicht-oktober-2026.html">AGOV-Artikel</a>). Ohne Zugang keine fristgerechte Abrechnung, egal wie hoch der Satz ist.</p>"""),
("Was ein Nein ändert – und was Sie schon heute tun können",
 """<p>Wird die Vorlage am 29. November abgelehnt, bleibt die 13. Rente bestehen – das Finanzierungsloch aber auch. Ohne Zusatzeinnahmen wächst das jährliche AHV-Defizit bis 2035 auf fast <strong>5 Milliarden Franken</strong>; der AHV-Fonds sänke auf rund 50 % einer Jahresausgabe (mit Erhöhung: knapp 70 % und ein Defizit von noch rund 3 Milliarden). Der Bundesrat hat im Rahmen der laufenden AHV-2030-Reform bereits Szenarien in die Vernehmlassung gegeben – darunter mehr MWST und tiefere Renten. Eine knappe Sache: In der ersten SRG-Trendumfrage (Erhebungsstand Mitte Oktober 2026) lag die Vorlage mit 49 % Nein zu 46 % Ja im Graben.</p>
<p>Für Ihre eigenen Zahlen gilt: Bis Ende 2027 ändert sich an den Sätzen nichts (8,1 / 2,6 / 3,8 %). Wer 2028 budgetiert, plant den Effekt als Konsument – und kann ihn gegensteuern, wo es steuerlich am meisten bringt: Ein <strong>Säule-3a-Einzahlung</strong> (2026 bis <strong>CHF 7'258</strong> mit Pensionskassen-Anschluss) spart je nach Tarif ein Mehrfaches dessen, was die MWST-Erhöhung einen Haushalt pro Jahr kostet. Ihren persönlichen Maximalbetrag rechnet der <a href="3a-rechner.html">3a-Rechner</a>, Fristen und Abzüge bündelt die <a href="steuer-checkliste-2026.html">Steuer-Checkliste</a>.</p>
<p><strong>Kurz gesagt:</strong></p>
<ul><li>29.11.2026: Volksabstimmung über +0,4 MWST-Punkte für die 13. AHV-Rente (Normalsatz 8,1 → 8,5 %, Hotelsatz 3,8 → 4,0 %, Grundbedarf bleibt bei 2,6 %).</li>
<li>In Kraft frühestens per 1.1.2028 – die 13. Renten 2026/2027 werden in jedem Fall ausbezahlt.</li>
<li>Armee-Fonds: +0,5 Punkte befristet auf 12 Jahre, Abstimmung voraussichtlich Sommer 2027 → bei Doppel-Ja Normalsatz 9,0 %.</li>
<li>Belastung: ESTV rechnet mit ~CHF 180 pro Haushalt und Jahr (AHV-Vorlage); unser Beispielhaushalt zahlt CHF 66–148.</li>
<li>Kein Kantönligeist: MWST gilt in allen 26 Kantonen gleich.</li>
<li>steuerberatung.ch liefert Sachinformationen, keine Wahlempfehlung und keine individuelle Steuerberatung.</li></ul>"""),
]

# ---------------------------------------------------------------- English
en_title = "VAT rise: what AHV and army cost you"
en_meta = ("On 29 Nov 2026 Switzerland votes on +0.4% VAT for the 13th AHV pension; the army fund follows in 2027. "
           "Worked examples: what the new rates cost from 2028.")
en_sections = [
("What is on the ballot on 29 November 2026",
 """<p>On <strong>29 November 2026</strong> Swiss voters decide on the «Federal decree of 19 June 2026 on additional AHV financing through a VAT increase» – the funding half of the 13th AHV pension, which the people accepted in March 2024 with 58 %. The first extra pension is paid in <strong>December 2026</strong> to some 2.6 million retirees: unmarried pensioners receive up to <strong>CHF 2,520</strong> more per year, married couples up to <strong>CHF 3,780</strong>. The cost to the AHV: over CHF 4 billion initially, more than CHF 5 billion a year from 2035.</p>
<p>Parliament proposes partial financing: the <strong>standard rate rises from 8.1 to 8.5 %</strong> (+0.4 percentage points) and the <strong>special hotel rate from 3.8 to 4.0 %</strong>. The <strong>reduced rate of 2.6 %</strong> on essentials – food, medicine, newspapers, books – stays unchanged; a proposed 0.2-point rise in AHV payroll contributions was narrowly rejected by the National Council (98 to 96). The VAT increase is <em>unlimited in time</em>.</p>
<p>Because the constitution must be amended, the vote is <strong>mandatory</strong> and requires a double majority of people and cantons; Federal Council and Parliament recommend acceptance. The extra revenue is some <strong>CHF 1 billion in 2028</strong> and an estimated <strong>CHF 1.4 billion per year from 2029</strong>. For perspective: the increase can enter into force <strong>no earlier than early 2028</strong> – the 13th pensions of 2026 and 2027 are paid from the AHV compensation fund in any case, without additional funding.</p>
<p><em>Practical tip:</em> The December 2026 payout does not depend on the vote. A «no» does not scrap the 13th pension – it only postpones the answer of how it gets paid for.</p>"""),
("The army fund: a second VAT rise from 2028",
 """<p>The second VAT project is already in parliamentary committee: on <strong>12 August 2026</strong> the Federal Council submitted its message on financing army procurement (FFe 2026 2354, bill 26.051). The proposal: from <strong>1 January 2028</strong> the standard rate rises by a further <strong>0.5 percentage points – limited to 12 years</strong> – with the entire yield ring-fenced for armament spending. The accommodation rate would rise proportionally by 0.3 points (0.2 if the AHV decree is accepted). Here too the reduced rate is untouched.</p>
<p>The need is around <strong>CHF 24 billion</strong>: CHF 15 billion for rapidly building capabilities against the most likely threats (air defence, cyber defence, anti-drone systems, protection of critical infrastructure, ammunition stockpiles), plus CHF 9 billion to absorb price rises on the global armament market. The money flows into a new, <strong>indebtedness-capable armament fund</strong> (maximum CHF 6 billion of debt, which must be repaid by the end of the 12-year period); Parliament decides how the money is spent.</p>
<p>For planning purposes, both projects add up: the army decree also requires a constitutional amendment and a popular vote – the Federal Council targets <strong>summer 2027</strong> so that the increase, like the AHV one, can take effect at the start of 2028. A double «yes» would put the standard rate at <strong>9.0 %</strong> from 2028 and the hotel rate at around 4.2 %. The difference: the army points expire after 12 years, the AHV points do not.</p>
<p><em>Practical tip:</em> Judge the two proposals separately – on 29 November 2026 only the AHV financing is at the ballot box; the army proposal will most likely follow in 2027.</p>"""),
("Worked example: what the rise costs a household",
 """<p>What matters is not the percentage point but the price effect: VAT is levied on the gross price. Moving from 8.1 to 8.5 % raises a standard-rated product by 108.5/108.1 = <strong>+0.37 %</strong>; with an accepted army fund (9.0 % total) it is 109.0/108.1 = <strong>+0.83 %</strong>. Example of a family with two children: they spend <strong>CHF 1,400</strong> a month on standard-rated consumption (restaurants, clothing, fuel, telecoms, hairdresser), <strong>CHF 600</strong> a month on reduced-rated essentials and <strong>CHF 2,000</strong> a year on hotel nights.</p>
<p>The arithmetic: a «yes» to the AHV decree alone costs this family around <strong>CHF 66 per year</strong> (CHF 62 on standard-rated spending plus CHF 4 on hotels). If the army fund passes too, the extra cost grows to about <strong>CHF 148 per year</strong> – roughly CHF 12 a month. The weekly food shop is untouched. The Federal Tax Administration (FTA) estimates the average household burden of the +0.4 points at around <strong>CHF 180 per year</strong>, based on standard-rated consumption of some CHF 48,500. On the benefits side: a single retiree receives up to CHF 2,520 from the 13th pension while contributing about CHF 180 via VAT – a net plus of roughly <strong>CHF 2,340 per year</strong>.</p>
""" + table("en") + """
<p><em>Practical tip:</em> These figures assume full pass-through – retailers may absorb part of the rise. The «AHV + army» hotel rate is the Federal Council's draft; Parliament and the people decide. Your total personal tax burden (income and wealth tax included) is shown by the <a href="rechner.html">calculator</a>.</p>
<div class="cta-mid"><strong>Curious about your total tax bill beyond VAT?</strong> Compute income and wealth tax free of charge in the <a href="rechner.html">tax calculator</a> – or have your situation reviewed by a vetted specialist: <a href="kontakt.html">request a no-obligation quote</a>.</div>"""),
("A federal tax: the same rate in all 26 cantons",
 """<p>VAT is a purely federal levy: collected by the FTA and remitted to the federal treasury – under the AHV decree, ring-fenced for the AHV compensation fund. That is why the increase applies <strong>identically in all 26 cantons</strong>: 8.1 % today, 8.5 % from 2028 if accepted – in Zurich as in Chiasso. Unlike income, wealth or property-gain tax, there is no cantonal table for VAT and no tax competition; moving house changes nothing about your consumption burden.</p>
<p>The social buffer is equally uniform: the reduced rate on essentials – food, medicine, newspapers, books, menstrual-hygiene products – stays at 2.6 % in <em>both</em> proposals. Low-income households, which spend a larger share on essentials, are therefore hit relatively less than average. And for cross-border commuters: consumption in Germany, France or Italy is taxed under those countries' VAT – the Swiss increase only affects spending in Switzerland.</p>
<p><em>Practical tip:</em> Never trust canton-specific forum numbers on VAT – the rate is identical countrywide. Cantonal differences start where direct taxes are concerned: there a <a href="rechner.html">comparison</a> is worth real money.</p>"""),
("Self-employed: what to prepare before 2028",
 """<p>For VAT-registered self-employed persons the rate change is a bookkeeping matter, not a cost: you invoice the tax to customers and pass it on. Example: on <strong>CHF 160,000</strong> of taxable revenue (excl. tax) a hairdressing business remits <strong>CHF 12,960</strong> at 8.1 % and <strong>CHF 13,600</strong> at 8.5 % – the CHF 640 difference belongs to the treasury, and input tax on your own purchases rises at the same time. Anyone below the CHF 100,000 turnover threshold who is not registered charges no VAT at all.</p>
<p>What remains to be done before the switch: update your till and invoicing software in good time, give long-term contracts and standing invoices a rate-change clause, and from the effective date show gross prices at the new rate under the price-display rules. Small businesses on the flat-rate (balance) method will see the FTA adjust the branch rates; the Federal Council has announced transitional provisions in the VAT act for advance payments and supplies straddling the changeover date. We cover the full rate-change playbook – deposits, partial supplies, period allocation – separately once the date and rates are final.</p>
<p><em>Practical tip:</em> If you do not have AGOV access to the FTA ePortal yet, set it up now – it has been mandatory for all VAT returns since 31 October 2026 (see the <a href="mwst-agov-pflicht-oktober-2026.html">AGOV article</a>). No access, no timely filing, whatever the rate.</p>"""),
("What a «no» changes – and what you can do today",
 """<p>If the decree is rejected on 29 November, the 13th pension itself stays – but the financing hole remains. Without extra revenue the annual AHV deficit grows to almost <strong>CHF 5 billion by 2035</strong>; the AHV fund would sink to around 50 % of one year's expenditure (with the increase: just under 70 % and a deficit of about 3 billion). The Federal Council has already put scenarios out for consultation within the ongoing AHV 2030 reform – including more VAT and lower pensions. The race is tight: the first SRG trend poll (fieldwork to mid-October 2026) had it at 49 % no versus 46 % yes.</p>
<p>For your own numbers: nothing changes until end-2027 (8.1 / 2.6 / 3.8 %). Anyone budgeting for 2028 prices the effect in as a consumer – and can offset it where the tax leverage is largest: a <strong>pillar 3a</strong> contribution (up to <strong>CHF 7,258</strong> in 2026 with a pension-fund affiliation) typically saves several times what the VAT increase costs a household per year. The <a href="3a-rechner.html">3a calculator</a> shows your personal maximum; the <a href="steuer-checkliste-2026.html">tax checklist</a> bundles the year-end deadlines.</p>
<p><strong>In short:</strong></p>
<ul><li>29.11.2026: popular vote on +0.4 VAT points for the 13th AHV pension (standard 8.1 → 8.5 %, hotel 3.8 → 4.0 %, essentials unchanged at 2.6 %).</li>
<li>In force no earlier than 1.1.2028 – the 13th pensions of 2026/2027 are paid either way.</li>
<li>Army fund: +0.5 points limited to 12 years, vote expected summer 2027 → with a double yes the standard rate becomes 9.0 %.</li>
<li>Household impact: the FTA estimates ~CHF 180 per year (AHV proposal); our example family pays CHF 66–148.</li>
<li>No cantonal differences – VAT is uniform across Switzerland.</li>
<li>steuerberatung.ch provides factual information, not a voting recommendation or individual tax advice.</li></ul>"""),
]

# ---------------------------------------------------------------- French
fr_title = "TVA 2028 : ce que coûtent AVS et armée"
fr_meta = ("Le 29 novembre 2026 : vote sur +0,4 % de TVA pour la 13e rente AVS. Le fonds pour l'armée suivra en 2027. "
           "Exemples chiffrés du coût de la hausse dès 2028.")
fr_sections = [
("Ce sur quoi le peuple vote le 29 novembre 2026",
 """<p>Le <strong>29 novembre 2026</strong>, le corps électoral se prononce sur « l'arrêté fédéral du 19 juin 2026 concernant le financement additionnel de l'AVS par une augmentation de la TVA » – le volet financement de la 13e rente AVS, acceptée par le peuple à 58 % en mars 2024. La première rente supplémentaire sera versée en <strong>décembre 2026</strong> à quelque 2,6 millions de rentiers : jusqu'à <strong>2 520 francs</strong> de plus par an pour les personnes seules, jusqu'à <strong>3 780 francs</strong> pour les couples. Coût pour l'AVS : plus de 4 milliards de francs au départ, plus de 5 milliards par an dès 2035.</p>
<p>Le Parlement propose un financement partiel : le <strong>taux normal passe de 8,1 à 8,5 %</strong> (+0,4 point) et le <strong>taux spécial hôtelier de 3,8 à 4,0 %</strong>. Le <strong>taux réduit de 2,6 %</strong> sur les biens de première nécessité – denrées, médicaments, journaux, livres – reste inchangé ; une hausse de 0,2 point des cotisations de salaire AVS, également discutée, a été rejetée de justesse par le Conseil national (98 contre 96). L'augmentation est <em>illimitée dans le temps</em>.</p>
<p>Comme la Constitution doit être modifiée, la <strong>votation obligatoire</strong> s'applique : il faut la double majorité du peuple et des cantons ; Conseil fédéral et Parlement recommandent d'approuver. Les recettes supplémentaires s'élèvent à environ <strong>1 milliard de francs en 2028</strong> et, selon les estimations, <strong>1,4 milliard par an dès 2029</strong>. À noter pour situer les choses : l'augmentation ne peut entrer en vigueur <strong>qu'au plus tôt début 2028</strong> – les 13es rentes 2026 et 2027 sont versées dans tous les cas par le fonds de compensation AVS, sans financement additionnel.</p>
<p><em>Conseil pratique :</em> le versement de décembre 2026 ne dépend pas du résultat des urnes. Un « non » ne supprime pas la 13e rente – il repousse seulement la réponse à la question de son financement.</p>"""),
("Le fonds pour l'armée : une deuxième hausse de TVA dès 2028",
 """<p>Le deuxième projet TVA est déjà en délibération parlementaire : le <strong>12 août 2026</strong>, le Conseil fédéral a transmis son message sur le financement des dépenses d'armement de l'armée (FF 2026 2354, objet 26.051). La proposition : dès le <strong>1er janvier 2028</strong>, le taux normal augmente encore de <strong>0,5 point – limité à 12 ans</strong> –, les recettes étant exclusivement affectées à l'armement. Le taux spécial de l'hébergement progresserait proportionnellement de 0,3 point (0,2 si le peuple approuve l'objet AVS). Là non plus, le taux réduit n'est pas touché.</p>
<p>Le besoin s'élève à environ <strong>24 milliards de francs</strong> : 15 milliards pour développer rapidement les capacités face aux menaces les plus probables (défense aérienne, cyberdéfense, lutte contre les drones, protection des infrastructures critiques, stocks de munitions) et 9 milliards pour absorber la flambée des prix sur le marché mondial de l'armement. L'argent affluera dans un nouveau <strong>fonds d'armement autorisé à s'endetter</strong> (dette maximale de 6 milliards, à rembourser d'ici à la fin de la période de 12 ans) ; le Parlement décide de l'emploi des moyens.</p>
<p>Pour la planification, les deux projets se cumulent : l'arrêté sur l'armée exige lui aussi une modification constitutionnelle et un vote populaire – le Conseil fédéral vise la <strong>votation à l'été 2027</strong>, afin que l'augmentation, comme celle pour l'AVS, puisse entrer en vigueur début 2028. En cas de double « oui », le taux normal atteindrait <strong>9,0 %</strong> dès 2028 et le taux hôtelier environ 4,2 %. La différence : les points « armée » expirent après 12 ans, les points « AVS » restent.</p>
<p><em>Conseil pratique :</em> jugez les deux objets séparément – le 29 novembre 2026, seule le financement de l'AVS est soumis au vote ; l'objet « armée » suivra vraisemblablement en 2027.</p>"""),
("Exemple chiffré : ce que la hausse coûte à un ménage",
 """<p>Ce qui compte n'est pas le point de pourcentage mais l'effet sur les prix : la TVA frappe le prix brut. De 8,1 à 8,5 %, un produit au taux normal renchérit de 108,5/108,1 = <strong>+0,37 %</strong> ; avec un fonds pour l'armée accepté (9,0 % au total), on atteint 109,0/108,1 = <strong>+0,83 %</strong>. Exemple d'une famille avec deux enfants : elle dépense chaque mois <strong>1 400 francs</strong> en consommation au taux normal (restaurant, habits, essence, télécom, coiffeur), <strong>600 francs</strong> en biens de première nécessité au taux réduit et <strong>2 000 francs</strong> par an en nuits d'hôtel.</p>
<p>Le calcul : un « oui » limité à l'objet AVS coûte à cette famille environ <strong>66 francs de plus par an</strong> (62 fr. sur la consommation au taux normal + 4 fr. d'hôtellerie). Si le fonds pour l'armée passe aussi, la surcharge atteint environ <strong>148 francs par an</strong> – près de 12 francs par mois. Les courses de la semaine ne sont pas touchées. L'Administration fédérale des contributions (AFC) estime la charge moyenne de ces +0,4 point à environ <strong>180 francs par ménage et par an</strong>, sur la base d'une consommation au taux normal d'environ 48 500 francs par an. Côté prestations : une rentière seule touche jusqu'à 2 520 francs de 13e rente tout en contribuant environ 180 francs via la TVA – un solde net d'environ <strong>2 340 francs par an</strong>.</p>
""" + table("fr") + """
<p><em>Conseil pratique :</em> ces montants supposent un répercussion intégrale de la taxe – le commerce de détail peut en absorber une partie. Le taux hôtelier « AVS + armée » correspond au projet du Conseil fédéral ; le Parlement et le peuple trancheront. Votre charge fiscale totale (impôt sur le revenu et la fortune compris) se calcule avec le <a href="rechner.html">calculateur</a>.</p>
<div class="cta-mid"><strong>Votre charge fiscale au-delà de la TVA ?</strong> Calculez gratuitement revenu et fortune dans le <a href="rechner.html">calculateur d'impôts</a> – ou faites examiner votre situation par un spécialiste vérifié : <a href="kontakt.html">demandez une offre sans engagement</a>.</div>"""),
("Un impôt fédéral : le même taux dans les 26 cantons",
 """<p>La TVA est un impôt purement fédéral : perçue par l'AFC, elle est versée à la Confédération – et, avec l'objet AVS, affectée au fonds de compensation. C'est pourquoi la hausse s'applique <strong>à l'identique dans les 26 cantons</strong> : 8,1 % aujourd'hui, 8,5 % éventuellement dès 2028 – à Zurich comme à Chiasso. Contrairement à l'impôt sur le revenu, à l'impôt sur la fortune ou aux droits de mutation, il n'existe aucun barème cantonal de TVA ni concurrence fiscale intercantonale ; un déménagement ne change rien à la charge de consommation.</p>
<p>La protection sociale l'est tout autant : le taux réduit sur les biens de première nécessité – denrées, médicaments, journaux, livres, produits d'hygiène menstruelle – reste à 2,6 % dans <em>les deux</em> projets. Les ménages à revenu modeste, dont la part du budget consacrée à ces biens est élevée, sont donc relativement moins touchés que la moyenne. Et pour les frontaliers : une consommation en Allemagne, en France ou en Italie est soumise à la TVA de ces pays – la hausse suisse ne vise que la consommation en Suisse.</p>
<p><em>Conseil pratique :</em> pour la TVA, ne vous fiez jamais à des chiffres « cantonaux » lus sur des forums – le taux est le même dans tout le pays. Les différences cantonales recommencent avec les impôts directs : là, une <a href="rechner.html">comparaison</a> vaut de l'argent.</p>"""),
("Indépendants : ce qu'il faut préparer avant 2028",
 """<p>Pour les indépendants assujettis à la TVA, le changement de taux est une question d'écriture comptable, pas de coût : la taxe est facturée aux clients puis reversée. Exemple : sur <strong>160 000 francs</strong> de chiffre d'affaires imposable (hors taxe), un salon de coiffure reverse <strong>12 960 francs</strong> à 8,1 % et <strong>13 600 francs</strong> à 8,5 % – les 640 francs de différence appartiennent à la caisse fédérale, et la taxe sur les achats propres augmente en parallèle. Quiconque reste sous la limite de 100 000 francs sans inscription volontaire ne facture aucune TVA.</p>
<p>À faire d'ici au changement : mettre à jour caisse et logiciel de facturation à temps, assortir les contrats durables et les factures récurrentes d'une clause de changement de taux, et afficher, dès l'entrée en vigueur, les prix bruts au nouveau taux conformément à l'ordonnance sur l'indication des prix. Pour les petites entreprises qui optent pour le taux de la prestation nette (méthode du taux forfaitaire), l'AFC adaptera les taux sectoriels ; le Conseil fédéral annonce des dispositions transitoires dans la LTVA pour les acomptes et les prestations à cheval sur la date du changement. Le mode d'emploi complet du changement de taux – acomptes, prestations partielles, délimitation des périodes – fera l'objet d'un article distinct dès que la date et les taux seront définitifs.</p>
<p><em>Conseil pratique :</em> si vous n'avez pas encore l'accès AGOV au ePortal de l'AFC, créez-le maintenant – il est obligatoire pour toutes les déclarations depuis le 31 octobre 2026 (voir l'<a href="mwst-agov-pflicht-oktober-2026.html">article AGOV</a>). Sans accès, pas de dépôt dans les délais, quel que soit le taux.</p>"""),
("Ce que changerait un non – et ce que vous pouvez déjà faire",
 """<p>Si l'objet est refusé le 29 novembre, la 13e rente elle-même reste acquise – mais le trou de financement aussi. Sans recettes supplémentaires, le déficit annuel de l'AVS grimperait à près de <strong>5 milliards de francs d'ici à 2035</strong> ; le fonds de compensation retomberait à environ 50 % d'une année de dépenses (avec la hausse : près de 70 %, et un déficit d'environ 3 milliards). Dans le cadre de la réforme AVS 2030 en cours, le Conseil fédéral a déjà mis en consultation des scénarios – dont une TVA plus élevée ou des rentes réduites. Le scrutin est incertain : le premier sondage Tendance de la SSR (terrain jusqu'à la mi-octobre 2026) donnait le non à 49 % contre le oui à 46 %.</p>
<p>Pour vos propres finances : rien ne change jusqu'à fin 2027 (8,1 / 2,6 / 3,8 %). Qui budgète 2028 intègre l'effet en tant que consommateur – et peut le compenser là où le levier fiscal est le plus fort : un versement dans le <strong>pilier 3a</strong> (jusqu'à <strong>7 258 francs</strong> en 2026 avec affiliation à une caisse de pension) économise, selon le barème, un multiple de ce que la hausse de TVA coûte par an à un ménage. Le <a href="3a-rechner.html">calculateur 3a</a> indique votre maximum personnel ; la <a href="steuer-checkliste-2026.html">check-list fiscale</a> récapitule les échéances de fin d'année.</p>
<p><strong>En bref :</strong></p>
<ul><li>29.11.2026 : votation sur +0,4 point de TVA pour la 13e rente AVS (taux normal 8,1 → 8,5 %, hôtels 3,8 → 4,0 %, besoins courants inchangés à 2,6 %).</li>
<li>Entrée en vigueur au plus tôt le 1er janvier 2028 – les 13es rentes 2026/2027 sont versées dans tous les cas.</li>
<li>Fonds pour l'armée : +0,5 point limité à 12 ans, votation attendue à l'été 2027 → en cas de double oui, taux normal de 9,0 %.</li>
<li>Charge : l'AFC table sur ~180 francs par ménage et par an (objet AVS) ; notre ménage d'exemple paie 66 à 148 francs.</li>
<li>Pas de particularités cantonales : la TVA est identique dans toute la Suisse.</li>
<li>steuerberatung.ch fournit des informations objectives, ni recommandation de vote ni conseil fiscal individuel.</li></ul>"""),
]

# ---------------------------------------------------------------- Italian
it_title = "IVA: quanto costano AVS ed esercito"
it_meta = ("Il 29.11.2026 si vota +0,4 % di IVA per la 13a rendita AVS; nel 2027 il fondo per l'esercito. "
           "Esempi pratici: quanto costano le nuove aliquote dal 2028.")
it_sections = [
("Cosa si vota il 29 novembre 2026",
 """<p>Il <strong>29 novembre 2026</strong> il corpo elettorale si esprime sul «Decreto federale del 19 giugno 2026 concernente il finanziamento aggiuntivo dell'AVS mediante un aumento dell'IVA»: è il capitolo finanziario della 13a rendita AVS, accettata dal popolo nel marzo 2024 con il 58 %. La prima rendita supplementare sarà versata nel <strong>dicembre 2026</strong> a circa 2,6 milioni di pensionati: fino a <strong>2 520 franchi</strong> in più all'anno per i single, fino a <strong>3 780</strong> per le coppie. Costi per l'AVS: oltre 4 miliardi di franchi all'inizio, oltre 5 miliardi l'anno dal 2035.</p>
<p>Il Parlamento propone un finanziamento parziale: l'<strong>aliquota normale passa da 8,1 a 8,5 %</strong> (+0,4 punti) e l'<strong>aliquota speciale alberghiera da 3,8 a 4,0 %</strong>. L'<strong>aliquota ridotta del 2,6 %</strong> sui beni di prima necessità – generi alimentari, medicinali, giornali, libri – resta invariata; un pure discusso aumento dello 0,2 % dei contributi salariali AVS è stato respinto di misura dal Consiglio nazionale (98 contro 96). L'aumento è <em>illimitato</em>.</p>
<p>Poiché occorre modificare la Costituzione vale la <strong>votazione obbligatoria</strong>: serve la doppia maggioranza di popolo e Cantoni; Consiglio federale e Parlamento raccomandano l'approvazione. Le maggiori entrate ammontano a circa <strong>1 miliardo di franchi nel 2028</strong> e, secondo le stime, a <strong>1,4 miliardi l'anno dal 2029</strong>. Per inquadrare bene: l'aumento può entrare in vigore <strong>al più presto a inizio 2028</strong> – le 13e rendite 2026 e 2027 sono versate in ogni caso dal fondo di compensazione AVS, senza finanziamento aggiuntivo.</p>
<p><em>Suggerimento pratico:</em> il versamento di dicembre 2026 non dipende dall'esito delle urne. Un «no» non sopprime la 13a rendita – rinvia soltanto la risposta su come viene pagata.</p>"""),
("Fondo per l'esercito: un secondo aumento IVA dal 2028",
 """<p>Il secondo progetto IVA è già in deliberazione parlamentare: il <strong>12 agosto 2026</strong> il Consiglio federale ha trasmesso il messaggio sul finanziamento delle spese militari dell'esercito (FF 2026 2354, incarto 26.051). La proposta: dal <strong>1° gennaio 2028</strong> l'aliquota normale sale di altri <strong>0,5 punti – limitati a 12 anni</strong> –, con gettito interamente vincolato agli armamenti. L'aliquota speciale per i pernottamenti crescerebbe proporzionalmente di 0,3 punti (di 0,2 se il popolo approva il progetto AVS). Anche qui l'aliquota ridotta non è toccata.</p>
<p>Il fabbisogno: circa <strong>24 miliardi di franchi</strong> – 15 per sviluppare rapidamente le capacità contro le minacce più probabili (difesa aerea, cyberdifesa, lotta ai droni, protezione delle infrastrutture critiche, scorte di munizioni) più 9 per assorbire l'aumento dei prezzi sul mercato mondiale degli armamenti. Il denaro confluirà in un nuovo <strong>fondo per gli armamenti autorizzato a indebitarsi</strong> (debito massimo 6 miliardi, da estinguere entro la fine dei 12 anni); il Parlamento decide l'impiego dei mezzi.</p>
<p>Per la pianificazione i due progetti si sommano: anche il decreto sull'esercito esige una modifica costituzionale e una votazione popolare – il Consiglio federale punta alla <strong>votazione nell'estate 2027</strong>, affinché l'aumento possa entrare in vigore, come quello AVS, a inizio 2028. Con un doppio «sì» l'aliquota normale salirebbe al <strong>9,0 %</strong> e quella alberghiera a circa 4,2 %. La differenza: i punti «esercito» scadono dopo 12 anni, quelli «AVS» restano.</p>
<p><em>Suggerimento pratico:</em> giudicate i due oggetti separatamente – il 29 novembre 2026 alle urne c'è solo il finanziamento AVS; il progetto esercito seguirà verosimilmente nel 2027.</p>"""),
("Esempio pratico: quanto costa l'aumento a un nucleo",
 """<p>Che conta non è il punto percentuale ma l'effetto sui prezzi: l'IVA grava sul prezzo lordo. Da 8,1 a 8,5 % un prodotto soggetto all'aliquota normale aumenta di 108,5/108,1 = <strong>+0,37 %</strong>; con un fondo esercito approvato (9,0 % in tutto) si arriva a 109,0/108,1 = <strong>+0,83 %</strong>. Esempio di una famiglia con due figli: spende ogni mese <strong>1 400 franchi</strong> in consumi all'aliquota normale (ristorante, vestiti, benzina, telecomunicazioni, parrucchiere), <strong>600 franchi</strong> in beni di prima necessità all'aliquota ridotta e <strong>2 000 franchi</strong> l'anno in pernottamenti in albergo.</p>
<p>Il conto: un «sì» limitato al progetto AVS costa a questa famiglia circa <strong>66 franchi in più all'anno</strong> (62 sui consumi all'aliquota normale + 4 sui pernottamenti). Se passa anche il fondo per l'esercito, il sovraccarico sale a circa <strong>148 franchi l'anno</strong> – una dodicina al mese. La spesa settimanale non è toccata. L'Amministrazione federale delle contribuzioni (AFC) stima l'onere medio di questi +0,4 punti a circa <strong>180 franchi per nucleo e anno</strong>, su un consumo all'aliquota normale di circa 48 500 franchi l'anno. Sul fronte delle prestazioni: una pensionata single incassa fino a 2 520 franchi di 13a rendita contribuendo circa 180 franchi di IVA – saldo netto di circa <strong>2 340 franchi l'anno</strong>.</p>
""" + table("it") + """
<p><em>Suggerimento pratico:</em> i valori presuppongono il riversamento integrale dell'imposta – il commercio al dettaglio può assorbirne una parte. L'aliquota alberghiera «AVS + esercito» si basa sul progetto del Consiglio federale; decideranno Parlamento e popolo. Il vostro onere fiscale complessivo (imposta sul reddito e sulla fortuna incluse) si calcola con il <a href="rechner.html">calcolatore</a>.</p>
<div class="cta-mid"><strong>Curiosi del vostro carico fiscale al netto dell'IVA?</strong> Calcolate gratuitamente reddito e fortuna nel <a href="rechner.html">calcolatore d'imposte</a> – o fate esaminare la vostra situazione da uno specialista verificato: <a href="kontakt.html">richiedete una valutazione senza impegno</a>.</div>"""),
("Un'imposta federale: aliquote identiche in 26 Cantoni",
 """<p>L'IVA è un'imposta puramente federale: riscossa dall'AFC e versata alla cassa della Confederazione – con il progetto AVS, vincolata al fondo di compensazione. Per questo l'aumento vale <strong>identico in tutti i 26 Cantoni</strong>: 8,1 % oggi, eventualmente 8,5 % dal 2028 – a Zurigo come a Chiasso. A differenza di imposta sul reddito, sulla fortuna o sugli utili immobiliari, per l'IVA non esiste alcuna tabella cantonale né concorrenza fiscale; un trasloco non cambia nulla sul fronte dei consumi.</p>
<p>Uniforme a livello federale è anche l'argine sociale: l'aliquota ridotta sui beni di prima necessità – generi alimentari, medicinali, giornali, libri, prodotti per l'igiene mestruale – resta al 2,6 % in <em>entrambi</em> i progetti. I nuclei a reddito basso, che spendono una quota maggiore in questi beni, sono dunque colpiti relativamente meno della media. E per i frontalieri: chi consuma in Germania, Francia o Italia paga l'IVA di quei Paesi – l'aumento svizzero riguarda solo i consumi in Svizzera.</p>
<p><em>Suggerimento pratico:</em> per l'IVA non credete mai a cifre «cantone per cantone» lette nei forum – l'aliquota è identica in tutto il Paese. Le differenze cantonali ricominciano con le imposte dirette: lì un <a href="rechner.html">confronto</a> vale soldi.</p>"""),
("Indipendenti: cosa preparare prima del 2028",
 """<p>Per gli indipendenti titolari di IVA il cambio di aliquota è una questione contabile, non di costi: l'imposta viene fatturata ai clienti e riversata. Esempio: su <strong>160 000 franchi</strong> di ricavo imponibile (imposta esclusa) un salone da parrucchiere versa <strong>12 960 franchi</strong> all'8,1 % e <strong>13 600</strong> all'8,5 % – i 640 franchi di differenza spettano alla cassa federale, e nel contempo sale l'imposta precedente sugli acquisti propri. Chi resta sotto la soglia dei 100 000 franchi senza registrazione non fattura IVA.</p>
<p>Cosa resta da fare prima del passaggio: aggiornare in tempo cassa e software di fatturazione, dotare i contratti duraturi e le fatture ricorrenti di una clausola sul cambio di aliquota e, dalla data dell'entrata in vigore, indicare i prezzi lordi secondo la nuova aliquota conformemente all'ordinanza sull'indicazione dei prezzi. Per le piccole imprese che liquidano l'IVA aliquote forfettarie (saldo), l'AFC adatterà le aliquote di settore; il Consiglio federale annuncia disposizioni transitorie nella LIVA per gli acconti e le prestazioni a cavallo della data del cambio. Il manuale completo del cambio di aliquota – acconti, prestazioni parziali, delimitazione dei periodi – avrà un articolo dedicato non appena data e aliquote saranno definitive.</p>
<p><em>Suggerimento pratico:</em> se non avete ancora l'accesso AGOV al ePortal dell'AFC, createlo ora – è obbligatorio per tutte le liquidazioni dal 31 ottobre 2026 (vedi l'<a href="mwst-agov-pflicht-oktober-2026.html">articolo AGOV</a>). Senza accesso niente deposito nei termini, qualunque sia l'aliquota.</p>"""),
("Cosa cambierebbe un no – e cosa fate già oggi",
 """<p>Se il 29 novembre l'oggetto fosse respinto, la 13a rendita resterebbe – ma anche il buco di finanziamento. Senza entrate supplementari il deficit annuo dell'AVS crescerebbe fino a quasi <strong>5 miliardi di franchi entro il 2035</strong>; il fondo di compensazione scenderebbe a circa il 50 % di una spesa annua (con l'aumento: quasi 70 %, e un deficit di circa 3 miliardi). Nel quadro della riforma AVS 2030 in corso il Consiglio federale ha già messo in consultazione scenari – IVA più elevata o rendite ridotte. La partita è aperta: il primo sondaggio Tendance SSR (rilevazione fino a metà ottobre 2026) dava il no al 49 % contro il sì al 46 %.</p>
<p>Per i vostri numeri: fino a fine 2027 non cambia nulla (8,1 / 2,6 / 3,8 %). Chi budgetta il 2028 considera l'effetto da consumatore – e può compensarlo dove la leva fiscale è più forte: un versamento nel <strong>pilastro 3a</strong> (nel 2026 fino a <strong>7 258 franchi</strong> con affiliazione a una cassa pensioni) fa risparmiare, a seconda della tariffa, un multiplo di ciò che l'aumento IVA costa a un nucleo all'anno. Il <a href="3a-rechner.html">calcolatore 3a</a> indica il vostro massimo personale; la <a href="steuer-checkliste-2026.html">check-list fiscale</a> riassume le scadenze di fine anno.</p>
<p><strong>In breve:</strong></p>
<ul><li>29.11.2026: votazione su +0,4 punti IVA per la 13a rendita AVS (normale 8,1 → 8,5 %, alberghi 3,8 → 4,0 %, beni di prima necessità invariati al 2,6 %).</li>
<li>Entrata in vigore al più presto il 1.1.2028 – le 13e rendite 2026/2027 sono versate in ogni caso.</li>
<li>Fondo per l'esercito: +0,5 punti limitati a 12 anni, votazione prevista nell'estate 2027 → con doppio sì aliquota normale al 9,0 %.</li>
<li>Onere: l'AFC stima ~180 franchi per nucleo e anno (progetto AVS); il nostro nucleo tipo paga 66–148 franchi.</li>
<li>Nessuna differenza cantonale: l'IVA è identica in tutta la Svizzera.</li>
<li>steuerberatung.ch offre informazioni oggettive, né raccomandazioni di voto né consulenza fiscale individuale.</li></ul>"""),
]

DATA = [("de", de_title, de_meta, de_sections),
        ("en", en_title, en_meta, en_sections),
        ("fr", fr_title, fr_meta, fr_sections),
        ("it", it_title, it_meta, it_sections)]

for lang, title, meta, sections in DATA:
    assert len(title) <= 40, (lang, "title", len(title))
    assert len(meta) <= 158, (lang, "meta", len(meta))
    assert len(sections) == 6, (lang, "sections", len(sections))
    build(lang, SLUG, title, meta, sections, related=RELATED, sources=SOURCES[lang])
    print(f"{lang}: title {len(title)}, meta {len(meta)}, {len(sections)} sections")
print("done")
