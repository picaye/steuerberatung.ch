#!/usr/bin/env python3
"""Build the cashbook/TWINT recording-obligations article in all 4 languages.

Slug: kassabuch-twint-aufzeichnung-pflicht-jahresende
Sources (all primary, verified 2026-10-21):
- MWSTG SR 641.20, fedlex eli/cc/2009/615/de: Art. 70 (Buchführung und Aufbewahrung),
  Art. 72 (Korrektur von Mängeln in der Abrechnung, 180. Tag), Art. 79
  (Ermessenseinschätzung), Art. 42 Abs. 6 (absolute Verjährung 10 Jahre), Art. 10
  Abs. 2 lit. a (100'000-Franken-Schwelle) — Volltext via JS-fähigen Browser gelesen.
- MWSTV SR 641.201, fedlex eli/cc/2009/828/de: Art. 128 Abs. 1 lit. d und Abs. 2
  (Umsatzabstimmung, Positionen a–j).
- OR SR 220, fedlex eli/cc/27/317_321_377/de: Art. 957 (Buchführungspflicht ab
  CHF 500'000 Umsatzerlös; vereinfachte Buchführung darunter), Art. 957a Abs. 2
  (vollständige, wahrheitsgetreue, systematische Erfassung), Art. 958f
  (Aufbewahrung 10 Jahre, elektronisch zulässig). NICHT Art. 958a — dieser regelt
  die Fortführungsannahme, nicht die Zeitnähe (Karten-Claim korrigiert).
- GeBüV SR 221.431, fedlex eli/cc/2002/216/de: Art. 1 (Hauptbuch/Journal,
  chronologische Erfassung), Art. 2 (anerkannte kaufmännische Grundsätze).
- DBG SR 642.11, fedlex eli/cc/1991/1184_1184_1184/de: Art. 125 Abs. 2 lit. b
  (Beilagen bei vereinfachter Buchführung: Einnahmen/Ausgaben, Vermögenslage,
  Privatentnahmen/-einlagen).
- ESTV https://www.estv.admin.ch/de/mwst-jahresabstimmung (curl 200): Abgleichpflicht,
  Formular «Jahresabstimmung (Berichtigungsabrechnung nach Art. 72 MWSTG)»,
  240-Tage-Finalisierungsannahme, Verzugszins ab Fälligkeit (60 Tage bzw. 28.2.).
- ESTV https://www.estv.admin.ch/de/unterlagen-fuer-die-mwst-kontrolle (curl 200):
  Umsatzabstimmung pro Jahr (Art. 128 Abs. 2 MWSTV), Kassabelege, Vorsteuerabstimmung.
- ESTV https://www.estv.admin.ch/de/mwst-kontrolle (curl 200): Selbstveranlagungssteuer,
  Kontrollbefugnis Art. 78 MWSTG.
NICHT zitiert (nicht offiziell verifizierbar): BGE 2A.657/2005 (bundesgericht.ch von
diesem Host nicht erreichbar -> Rechtsprechung allgemein formuliert); «Aufrechnungsverbot
Art. 45 MWSTG» (Art. 45 regelt die Bezugsteuer -> weggelassen); TWINT-spezifische
ESTV-Publikation existiert nicht auffindbar -> Praxisanforderung ohne Rechtszitat;
keine Aussage zu zertifizierten Kassensystemen/TPS (kein offizieller Status, Formulierung
«beweisfähige Aufzeichnung» gemäss Research-Karte).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "kassabuch-twint-aufzeichnung-pflicht-jahresende"
RELATED = ["mwst-100k-pflicht-schweiz.html",
           "mwst-agov-pflicht-oktober-2026.html",
           "mwst-ausfuhr-0-prozent-nachweis.html"]

URLS = [
    "https://www.fedlex.admin.ch/eli/cc/2009/615/de",
    "https://www.fedlex.admin.ch/eli/cc/2009/828/de",
    "https://www.fedlex.admin.ch/eli/cc/27/317_321_377/de",
    "https://www.fedlex.admin.ch/eli/cc/2002/216/de",
    "https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de",
    "https://www.estv.admin.ch/de/mwst-jahresabstimmung",
    "https://www.estv.admin.ch/de/unterlagen-fuer-die-mwst-kontrolle",
    "https://www.estv.admin.ch/de/mwst-kontrolle",
]

CTA_MID = {
    "de": '<div class="cta-mid"><strong>Unklar, was das für Ihre Situation bedeutet?</strong> Eine <a href="partner-pruefung.html">geprüfte Fachperson</a> prüft Ihre Unterlagen und zeigt das konkrete Sparpotenzial – die Erstberatung ist kostenlos: <a href="kontakt.html">unverbindliche Offerte anfragen</a>.</div>',
    "en": '<div class="cta-mid"><strong>Not sure what this means for your situation?</strong> A <a href="partner-pruefung.html">vetted professional</a> reviews your documents and shows your concrete savings potential – first consultation free: <a href="kontakt.html">request a no-obligation quote</a>.</div>',
    "fr": '<div class="cta-mid"><strong>Vous ne savez pas ce que cela implique pour votre situation ?</strong> Un <a href="partner-pruefung.html">conseiller vérifié</a> examine vos documents et chiffre votre potentiel d’économie – premier entretien gratuit : <a href="kontakt.html">demandez une offre sans engagement</a>.</div>',
    "it": '<div class="cta-mid"><strong>Non sapete cosa significa in concreto per la sua situazione?</strong> Un <a href="partner-pruefung.html">consulente verificato</a> esamina i suoi documenti e indica il potenziale di risparmio – primo colloquio gratuito: <a href="kontakt.html">richieda un’offerta senza impegno</a>.</div>',
}

# ---------------- German ----------------
de_title = "Kassabuch-Pflicht: Bar, TWINT & Karte"
de_meta = "Kassabuch täglich führen, TWINT- und Kartenzahlungen belegen, Umsatzabstimmung bis zum 180. Tag: was MWSTG, OR und ESTV von Barbetrieben verlangen."
de_sections = [
 ("Jahresende 2026: Die Kasse entscheidet, ob die Buchhaltung trägt",
  """<p>Die Mehrwertsteuer ist eine <strong>Selbstveranlagungssteuer</strong>: Der Betrieb deklariert und bezahlt die Steuer selbst – die Eidgenössische Steuerverwaltung (ESTV) prüft das Deklarierte in Kontrollen, zu denen sie Art. 78 MWSTG ermächtigt. Dieses System beruht auf Vertrauen in die Aufzeichnungen des Unternehmens – und dieses Vertrauen hat eine Voraussetzung: lückenlose, zeitnahe, belegte Buchungen.</p>
<p>Spätestens im Jahresabschluss 2026 zeigt sich, ob die Buchhaltung trägt. Für bargeldintensive Betriebe – Gastronomie, Detailhandel, Kioske, Coiffeure, Bäckereien, Take-aways – steht dabei das <strong>Kassabuch</strong> im Zentrum: Hier laufen Bareinnahmen, TWINT und Kartenzahlungen täglich zusammen. Dieser Ratgeber zeigt, was MWSTG, Obligationenrecht und die ESTV-Praxis verlangen: von der täglichen Aufzeichnung über die Aufbewahrung und die Umsatzabstimmung bis zu den Fristen, die rund um den Jahresabschluss 2026 gelten.</p>"""),
 ("Wer welche Bücher führen muss: zwei Schwellen, zwei Gesetze",
  """<p>Zwei verschiedene Schwellen, zwei Gesetze – verwechseln sollte man sie nicht:</p>
<ul>
<li><strong>Handelsrechtliche Buchführungspflicht (OR):</strong> Einzelunternehmen und Personengesellschaften führen volle Bücher, sobald sie im Geschäftsjahr mindestens <strong>CHF 500'000</strong> Umsatzerlös erzielen (Art. 957 Abs. 1 Ziff. 1 OR). Darunter genügt es, <strong>Einnahmen, Ausgaben und die Vermögenslage</strong> aufzuzeichnen – die sogenannte «Milchbüchleinrechnung» (Art. 957 Abs. 2 OR); die Grundsätze ordnungsmässiger Buchführung gelten sinngemäss (Abs. 3).</li>
<li><strong>Direkte Steuern:</strong> Wer vereinfacht Buch führt, legt der Steuererklärung Aufstellungen über Einnahmen und Ausgaben, über die Vermögenslage sowie über Privatentnahmen und -einlagen bei (Art. 125 Abs. 2 Bst. b DBG).</li>
<li><strong>Mehrwertsteuer (MWSTG):</strong> Wer MWST-registriert ist – in der Regel ab CHF 100'000 Jahresumsatz (Art. 10 Abs. 2 Bst. a MWSTG) – führt Geschäftsbücher und Aufzeichnungen <strong>nach den handelsrechtlichen Grundsätzen</strong>, unabhängig von der OR-Schwelle (Art. 70 Abs. 1 MWSTG). Die ESTV kann weitergehende Aufzeichnungspflichten erlassen, wenn dies für die ordnungsgemässe Steuererhebung unerlässlich ist.</li>
</ul>
<p><strong>Für die Praxis:</strong> Ein kleiner Take-away mit CHF 300'000 Umsatz braucht nach OR keine Bilanz – ist er MWST-registriert, müssen seine Aufzeichnungen aber einer MWST-Kontrolle standhalten. Das täglich geführte Kassabuch ist dafür das Fundament.</p>"""),
 ("Das tägliche Kassabuch: Inhalt, Form, Kassensturz",
  """<p>Ein bestimmtes Kassensystem oder eine bestimmte Software schreibt das Schweizer Recht nicht vor. Entscheidend ist eine <strong>beweisfähige Aufzeichnung</strong>: vollständig, zeitnah, nachvollziehbar und nicht nachträglich erstellt. In jede Kassabuch-Zeile gehören:</p>
<ul>
<li>das <strong>Datum</strong> (ideal: fortlaufende Nummerierung pro Geschäftstag),</li>
<li>die <strong>Einnahmen getrennt nach Zahlungsart</strong> – Bar, TWINT, Debit-/Kreditkarte,</li>
<li>die <strong>Ausgaben</strong> (Barauslagen wie Kleinkäufe oder Privateinlagen ins Wechselgeld),</li>
<li>der <strong>laufende Zwischenstand bzw. der Kassenendbestand</strong> des Tages.</li>
</ul>
<p>Bei bargeldintensiven Betrieben verlangt die Praxis zudem den <strong>täglichen Kassensturz</strong>: Das tatsächlich vorhandene Bargeld wird bei Geschäftsschluss gezählt, mit dem Soll-Bestand des Kassabuchs verglichen, und jede Differenz wird festgehalten und erklärt. Jede Buchung braucht einen <strong>Beleg</strong> – Quittung, Z-Bon, Rechnung, TWINT- oder Terminalauszug. Die Erfassung hat <strong>chronologisch und systematisch</strong> zu erfolgen: Das Journal der Buchhaltung erfasst alle gebuchten Geschäftsvorfälle chronologisch (Art. 1 Abs. 2 Bst. b GeBüV), und die Buchführung muss vollständig, wahrheitsgetreu und systematisch sein (Art. 957a Abs. 2 OR).</p>
<p><strong>Praxistipp:</strong> Wer das Kassabuch erst am Monatsende aus dem Gedächtnis oder aus Bankauszügen «zusammenstellt», führt ein nachträgliches Kassabuch – genau die Konstellation, die in einer Kontrolle nicht beweiskräftig ist.</p>"""),
 ("TWINT und Karte: unbare Einnahmen sind keine Nebensache",
  """<p>Ein verbreiteter Irrtum: «TWINT und Karten sind kein Bargeld, also gehören sie nicht ins Kassabuch.» Richtig ist: Unbare Einnahmen gehen nicht in den <em>Kassen</em>bestand ein. Falsch ist: Sie wären damit nicht aufzeichnungspflichtig – sie gehören ebenso zu den Entgelten, die lückenlos erfasst und deklariert werden müssen. Für den Alltag heisst das:</p>
<ul>
<li>Führen Sie für jede Zahlungsart eine eigene Spalte oder ein eigenes Nebenbuch: Bar, TWINT, Karte.</li>
<li>Halten Sie die Tagesendsummen aus der TWINT-App und dem Kartenterminal fest – wie beim Bargeld.</li>
<li>Bewahren Sie die <strong>Abrechnungen der Zahlungsabwickler</strong> (Tages- und Monatsabschlüsse) als Buchungsbelege auf und stimmen Sie sie mit den erfassten Beträgen ab.</li>
<li>Buchen Sie die <strong>Bruttoeinnahmen</strong>: Abwickler- und Acquirer-Gebühren sind Aufwand, keine Umsatzminderung.</li>
</ul>
<p>In der Umsatzabstimmung müssen die unbaren Zahlungseingänge nachvollziehbar sein – die Verordnung nennt ausdrücklich die «übrigen Zahlungseingänge, die nicht im ausgewiesenen Betriebsumsatz enthalten sind» (Art. 128 Abs. 2 Bst. f MWSTV). Wo der TWINT-Fluss in der Buchhaltung nicht sichtbar ist, entsteht spätestens in der Kontrolle eine Differenz, die Sie erklären müssen.</p>
<p><strong>Praxistipp:</strong> Nutzen Sie ein privates TWINT-Konto geschäftlich, buchen Sie diese Einnahmen lückenlos in die Geschäftsbuchhaltung um – vermischte private und geschäftliche Zahlungsflüsse sind ein typischer Kontrollbefund.</p>
""" + CTA_MID["de"]),
 ("Aufbewahrung: zehn Jahre – bei Liegenschaften zwanzig",
  """<p>Die Aufbewahrungsfristen im Überblick:</p>
<ul>
<li><strong>MWST:</strong> Geschäftsbücher, Belege, Geschäftspapiere und sonstige Aufzeichnungen sind ordnungsgemäss aufzubewahren, <strong>bis die Steuerforderung absolut verjährt</strong> ist – grundsätzlich zehn Jahre nach Ablauf der Steuerperiode (Art. 70 Abs. 2 i.V.m. Art. 42 Abs. 6 MWSTG).</li>
<li><strong>Handelsrecht:</strong> Geschäftsbücher und Buchungsbelege – ebenso Geschäftsbericht und Revisionsbericht – sind <strong>zehn Jahre</strong> aufzubewahren; die Frist beginnt mit dem Ablauf des Geschäftsjahres (Art. 958f Abs. 1 OR).</li>
<li><strong>Liegenschaften:</strong> Geschäftsunterlagen, die für die Berechnung der Einlageentsteuerung und des Eigenverbrauchs von unbeweglichen Gegenständen benötigt werden, sind <strong>zwanzig Jahre</strong> aufzubewahren (Art. 70 Abs. 3 MWSTG).</li>
</ul>
<p>Elektronisch aufbewahren ist zulässig: Bücher und Belege dürfen auf Papier, elektronisch oder vergleichbar geführt werden, soweit die Übereinstimmung mit den zugrunde liegenden Geschäftsvorfällen gewährleistet ist und sie jederzeit wieder lesbar gemacht werden können (Art. 958f Abs. 3 OR; zu den Grundsätzen ordnungsmässiger Datenverarbeitung Art. 2 Abs. 2 GeBüV). TWINT- und Kartenabrechnungen treffen in der Regel nur elektronisch ein – sichern Sie sie so, dass sie auch in zehn Jahren noch lesbar und reproduzierbar sind.</p>"""),
 ("Die Umsatzabstimmung: was sie ist und was hineingehört",
  """<p>Die <strong>Umsatzabstimmung</strong> macht sichtbar, wie die Deklaration der Steuerperiode – unter Berücksichtigung der verschiedenen Steuersätze bzw. der Saldo- oder Pauschalsteuersätze – mit dem Jahresabschluss in Übereinstimmung gebracht wird (Art. 128 Abs. 2 MWSTV). Namentlich zu berücksichtigen sind laut Verordnung:</p>
<ul>
<li>der in der Jahresrechnung ausgewiesene <strong>Betriebsumsatz</strong>;</li>
<li>Erträge, die auf <strong>Aufwandkonten</strong> verbucht wurden (Aufwandminderungen);</li>
<li><strong>konzerninterne Verrechnungen</strong>, die nicht im Betriebsumsatz enthalten sind;</li>
<li><strong>Verkäufe von Betriebsmitteln</strong>, <strong>Vorauszahlungen</strong> sowie die <strong>übrigen Zahlungseingänge</strong>, die nicht im ausgewiesenen Betriebsumsatz enthalten sind;</li>
<li><strong>geldwerte Leistungen</strong>, <strong>Erlösminderungen</strong> und <strong>Debitorenverluste</strong>;</li>
<li><strong>Abschlussbuchungen</strong> wie zeitliche Abgrenzungen, Rückstellungen und interne Umbuchungen, die nicht umsatzrelevant sind.</li>
</ul>
<p>In einer MWST-Kontrolle verlangt die ESTV die Umsatzabstimmung <strong>pro Jahr</strong> – ausgehend von den Salden der massgebenden Ertragskonten, unter Berücksichtigung von Abgrenzungs- und Sonderposten, gegenüber der Ziffer 200 der Abrechnungsformulare; wer nach der effektiven Methode abrechnet, legt zusätzlich eine Vorsteuerabstimmung vor. Für den Alltag gilt: Stimmen Sie monatlich oder zumindest quartalsweise ab. Wer erst am Jahresende in den Dezember schaut, sucht die Nadel im Heuhaufen.</p>"""),
 ("Fristen: der 180. Tag und die Finalisierung nach 240 Tagen",
  """<p>Rund um den Jahresabschluss greifen zwei Fristen ineinander:</p>
<ul>
<li><strong>Der 180. Tag (Art. 72 Abs. 1 MWSTG):</strong> Stellen Sie im Rahmen des Jahresabschlusses Mängel in den Steuerabrechnungen fest, müssen Sie diese <strong>spätestens in der Abrechnung über jene Abrechnungsperiode korrigieren, in die der 180. Tag seit Ende des Geschäftsjahres fällt</strong>. Für das Geschäftsjahr 2026 (Kalenderjahr) ist der 180. Tag der <strong>29. Juni 2027</strong> – bei quartalsweiser Abrechnung muss die Korrektur also spätestens in der Abrechnung des 2. Quartals 2027 erscheinen.</li>
<li><strong>Finalisierung nach 240 Tagen (Praxis der ESTV):</strong> Geht innert 240 Tagen seit Ende des Geschäftsjahres – für 2026 der <strong>28. August 2027</strong> – keine Berichtigungsabrechnung ein, geht die ESTV davon aus, dass die eingereichten MWST-Abrechnungen vollständig und korrekt sind und die Steuerperiode finalisiert ist.</li>
</ul>
<p>Die Korrektur erfolgt in der von der ESTV vorgeschriebenen Form (Art. 72 Abs. 3 MWSTG) auf dem offiziellen Formular «Jahresabstimmung (Berichtigungsabrechnung nach Art. 72 MWSTG)»; deklariert werden nur die Differenzen zu den bisher eingereichten Abrechnungen. Ergibt der Abgleich mit dem Jahresabschluss keine Mängel, ist keine Berichtigungsabrechnung einzureichen. Und: Erkannte Mängel müssen auch ausserhalb des Jahresabschlusses nachträglich korrigiert werden, soweit die Steuerforderungen nicht in Rechtskraft erwachsen oder verjährt sind (Art. 72 Abs. 2 MWSTG).</p>
<p><strong>Es geht um Geld:</strong> Erfolgt die Korrektur erst im Zeitpunkt der Finalisierung mit der Berichtigungsabrechnung, wird ein <strong>Verzugszins</strong> geschuldet – er läuft ab dem Verfalldatum der betreffenden Steuerperiode (in der Regel 60 Tage nach Ablauf der Steuerperiode bzw. der 28. Februar des Folgejahres). Wer früh korrigiert, spart Zins.</p>"""),
 ("Rechenbeispiel: ein Gastro-Tag und ein Abstimmungs-Monat (illustrativ)",
  """<p><strong>Beispiel (illustrativ):</strong> ein Gastronomiebetrieb an einem Dienstag im September 2026 – eine Zeile im Kassabuch:</p>
<ul>
<li>Anfangsbestand Kasse: CHF 300.00</li>
<li>Bareinnahmen (Speisen, Getränke): CHF 1'240.00</li>
<li>TWINT-Einnahmen: CHF 860.00</li>
<li>Kartenzahlungen: CHF 1'900.00</li>
<li>Barausgabe (Auslagekasse an Lieferant): CHF 150.00</li>
<li>Soll-Kassenbestand: 300.00 + 1'240.00 − 150.00 = <strong>CHF 1'390.00</strong></li>
<li>Kassensturz bei Geschäftsschluss (Ist): CHF 1'390.00 – Differenz: CHF 0.00</li>
<li>Tagesumsatz total über alle Zahlungsarten: CHF 4'000.00</li>
</ul>
<p><strong>Monatliche Umsatzabstimmung (illustrativ), September 2026:</strong></p>
<ul>
<li>Betriebsumsatz laut Erlöskonten der Buchhaltung: CHF 97'500.00</li>
<li>abzüglich Erlösminderungen (Skonti, Rabatte): CHF 1'000.00</li>
<li>abzüglich Verkauf Betriebsmittel (alte Espressomaschine, nicht im Betriebsumsatz): CHF 500.00</li>
<li>= deklarierter Umsatz in der MWST-Abrechnung, Ziffer 200: <strong>CHF 96'000.00</strong> – abgestimmt, die Differenz ist erklärt.</li>
</ul>
<p>Beide Beispiele verwenden frei erfundene, rein illustrative Beträge; sie erläutern die Methode und sind keine Empfehlung für den konkreten Einzelfall.</p>"""),
 ("Lücken, nachträgliche Bücher – und was dann passiert",
  """<p>Liegen keine oder nur unvollständige Aufzeichnungen vor oder stimmen die ausgewiesenen Ergebnisse mit dem wirklichen Sachverhalt offensichtlich nicht überein, so <strong>schätzt die ESTV die Steuerforderung nach pflichtgemässem Ermessen ein</strong> (Ermessenseinschätzung, Art. 79 Abs. 1 MWSTG). Für bargeldintensive Betriebe hat das Bundesgericht in ständiger Rechtsprechung präzisiert, was ein Kassabuch wert ist: eine erst nachträglich erstellte Kassenaufzeichnung und Aufzeichnungen ohne zeitnahe Belege sind nicht beweiskräftig; im ungünstigen Fall wird die Buchhaltung insgesamt verworfen und der Umsatz geschätzt. Schätzungen gehen regelmässig zuungunsten des Betriebs aus – mit Aufrechnungen, Nachsteuer und Verzugszins.</p>
<p>Die Lücken wirken zudem über die MWST hinaus in die <strong>direkten Steuern</strong>: Die Jahresrechnung ist Grundlage der Gewinndefinition – hält das Kassabuch nicht stand, wird auch der deklarierte Gewinn von den Steuerbehörden nicht unbesehen übernommen. Es geht also nicht um Formalismus, sondern um die Substanz: Kann jeder Franken deklarierter Umsatz vom Beleg über die Abrechnung bis in die Steuererklärung nachvollzogen werden – und zurück? Ein täglich geführtes Kassabuch mit sauber abgelegten TWINT- und Kartenbelegen ist die Antwort auf diese Frage, lange bevor eine Kontrolle ansteht.</p>"""),
 ("Checkliste bis zum Jahresabschluss 2026",
  """<ul>
<li><strong>Täglich:</strong> Kassabuch am selben Tag führen – mit Spalten für Bar, TWINT und Karte, Tagesendsumme und Kassensturz bei Geschäftsschluss (Differenzen festhalten).</li>
<li><strong>Belege:</strong> Zu jeder Buchung ein Beleg; Terminal-, TWINT- und Abwicklerabrechnungen mindestens zehn Jahre lesbar aufbewahren (Liegenschaftsunterlagen: zwanzig Jahre).</li>
<li><strong>Monatlich:</strong> Erlöskonten mit den MWST-Abrechnungen abstimmen (Umsatzabstimmung) – nicht erst am Jahresende; bei effektiver Methode auch die Vorsteuer abstimmen.</li>
<li><strong>Jahresende 2026:</strong> Mängel in den Abrechnungen 2026 bis spätestens <strong>29. Juni 2027</strong> (180. Tag) per Berichtigungsabrechnung in der dann offenen Abrechnungsperiode korrigieren; ab <strong>28. August 2027</strong> gilt die Steuerperiode bei der ESTV als finalisiert.</li>
<li><strong>Zinsen sparen:</strong> Frühe Korrektur vor der Finalisierung vermeidet Verzugszins ab dem ursprünglichen Verfalldatum.</li>
</ul>
<p>Dieser Artikel ist allgemeine Information und keine individuelle Beratung – lassen Sie Ihre Aufzeichnungen, Fristen und die Umsatzabstimmung von einer Treuhänderin oder einem Steuerberater prüfen.</p>"""),
]

# ---------------- English ----------------
en_title = "Cashbook duties: cash, TWINT & cards"
en_meta = "Daily cashbook, TWINT and card receipts as evidence, turnover reconciliation by day 180: what Swiss VAT law, the Code of Obligations and the FTA require."
en_sections = [
 ("Year-end 2026: the cash register decides whether the books hold",
  """<p>Swiss VAT is a <strong>self-assessed tax</strong>: the business declares and pays the tax itself, and the Federal Tax Administration (FTA) reviews what was declared in audits it is empowered to carry out under Art. 78 of the VAT Act. The system relies on trust in the company's records – and that trust has one precondition: complete, contemporaneous entries backed by documents.</p>
<p>By the 2026 year-end close at the latest, it becomes clear whether the accounting holds. For cash-intensive businesses – restaurants, retail, kiosks, hairdressers, bakeries, take-aways – the <strong>cashbook</strong> is at the centre: cash receipts, TWINT and card payments converge there every day. This guide sets out what the VAT Act, the Code of Obligations and FTA practice require: from daily recording through retention and turnover reconciliation to the deadlines that apply around the 2026 financial statements.</p>"""),
 ("Who must keep which books: two thresholds, two laws",
  """<p>Two different thresholds, two laws – do not confuse them:</p>
<ul>
<li><strong>Commercial-law duty to keep accounts (CO):</strong> sole proprietorships and partnerships keep full accounts once they achieve revenue of at least <strong>CHF 500'000</strong> in the financial year (Art. 957 para. 1 no. 1 CO). Below that, it suffices to record <strong>income, expenditure and the financial position</strong> – the so-called simplified accounts (Art. 957 para. 2 CO); the principles of proper accounting apply by analogy (para. 3).</li>
<li><strong>Direct taxes:</strong> anyone keeping simplified accounts files, with the tax return, statements of income and expenditure, of the financial position and of private withdrawals and contributions (Art. 125 para. 2 let. b of the Federal Act on Direct Federal Tax, DBG).</li>
<li><strong>VAT (VAT Act):</strong> anyone VAT-registered – as a rule from CHF 100'000 of annual turnover (Art. 10 para. 2 let. a VAT Act) – must keep business books and records <strong>in accordance with commercial-law principles</strong>, regardless of the CO threshold (Art. 70 para. 1 VAT Act). The FTA may impose further recording duties where indispensable for proper tax collection.</li>
</ul>
<p><strong>In practice:</strong> a small take-away with CHF 300'000 of revenue needs no balance sheet under the CO – but if it is VAT-registered, its records must withstand a VAT audit. The daily cashbook is the foundation of that.</p>"""),
 ("The daily cashbook: content, form, cash count",
  """<p>Swiss law does not prescribe a specific till or cashbook system. What matters is a <strong>record capable of serving as evidence</strong>: complete, contemporaneous, comprehensible and not reconstructed after the fact. Each cashbook row should contain:</p>
<ul>
<li>the <strong>date</strong> (ideally with consecutive numbering per business day),</li>
<li><strong>receipts separated by payment type</strong> – cash, TWINT, debit/credit card,</li>
<li><strong>payments out</strong> (cash disbursements such as petty purchases or topping up the float),</li>
<li>the <strong>running balance and the closing cash figure</strong> for the day.</li>
</ul>
<p>For cash-intensive businesses, practice also requires the <strong>daily cash count</strong>: at closing, the actual cash is counted, compared with the cashbook's expected balance, and every difference is recorded and explained. Every entry needs a <strong>supporting document</strong> – receipt, till roll (Z-bon), invoice, TWINT or terminal extract. Recording must be <strong>chronological and systematic</strong>: the accounting journal captures all posted transactions in chronological order (Art. 1 para. 2 let. b of the Business Records Ordinance, GeBüV), and the accounts must be complete, truthful and systematic (Art. 957a para. 2 CO).</p>
<p><strong>Practical tip:</strong> anyone who "assembles" the cashbook at month-end from memory or bank statements is producing an after-the-fact record – precisely the constellation that carries no evidentiary weight in an audit.</p>"""),
 ("TWINT and cards: electronic receipts are not a side note",
  """<p>A widespread misconception: "TWINT and cards are not cash, so they do not belong in the cashbook." True, electronic receipts do not enter the <em>cash</em> balance – but they are every bit as subject to the recording obligation and form part of the consideration that must be captured without gaps and declared. For day-to-day operations that means:</p>
<ul>
<li>Keep a separate column or subsidiary record for each payment type: cash, TWINT, card.</li>
<li>Capture the daily totals from the TWINT app and the card terminal – just as you do for cash.</li>
<li>Keep the <strong>payment processors' settlement reports</strong> (daily and monthly closes) as accounting documents and reconcile them with the recorded amounts.</li>
<li>Post the <strong>gross receipts</strong>: processor and acquirer fees are an expense, not a reduction of turnover.</li>
</ul>
<p>In the turnover reconciliation the electronic receipts must remain traceable – the ordinance expressly lists "other incoming payments not included in the reported operating revenue" (Art. 128 para. 2 let. f of the VAT Ordinance, MWSTV). Wherever the TWINT flow is invisible in the accounting, an audit will sooner or later surface a difference you must explain.</p>
<p><strong>Practical tip:</strong> if a private TWINT account is used for business takings, transfer those receipts into the business records without gaps – mixed private/business payment flows are a classic audit finding.</p>
""" + CTA_MID["en"]),
 ("Retention: ten years – twenty for real estate",
  """<p>The retention periods at a glance:</p>
<ul>
<li><strong>VAT:</strong> business books, supporting documents, business papers and other records must be properly kept <strong>until the tax claim is absolutely time-barred</strong> – as a rule ten years after the end of the tax period (Art. 70 para. 2 in conjunction with Art. 42 para. 6 VAT Act).</li>
<li><strong>Commercial law:</strong> business books and accounting documents – as well as the annual and audit reports – must be kept for <strong>ten years</strong>; the period starts at the end of the financial year (Art. 958f para. 1 CO).</li>
<li><strong>Real estate:</strong> business documents needed to calculate input-tax relief on immovable property and own use must be kept for <strong>twenty years</strong> (Art. 70 para. 3 VAT Act).</li>
</ul>
<p>Electronic retention is permitted: books and documents may be kept on paper, electronically or in a comparable manner, provided consistency with the underlying transactions is guaranteed and they can be made readable again at any time (Art. 958f para. 3 CO; on proper data processing, Art. 2 para. 2 GeBüV). TWINT and card settlement reports usually arrive electronically only – store them so that they remain readable and reproducible ten years from now.</p>"""),
 ("Turnover reconciliation: what it is and what belongs in it",
  """<p>The <strong>turnover reconciliation (Umsatzabstimmung)</strong> shows how the declaration for the tax period – taking account of the different tax rates or of the net/flat rates – is brought into line with the annual accounts (Art. 128 para. 2 MWSTV). The ordinance lists, in particular:</p>
<ul>
<li>the <strong>operating revenue</strong> shown in the annual accounts;</li>
<li>income posted to <strong>expense accounts</strong> (expense reductions);</li>
<li><strong>intra-group offsets</strong> not included in operating revenue;</li>
<li><strong>sales of fixed assets</strong>, <strong>advance payments</strong> and the <strong>other incoming payments</strong> not included in the reported operating revenue;</li>
<li><strong>benefits in kind</strong>, <strong>revenue reductions</strong> and <strong>debtor losses</strong>;</li>
<li><strong>closing entries</strong> such as accruals, provisions and internal reclassifications that are not turnover-relevant.</li>
</ul>
<p>In a VAT audit the FTA requires the turnover reconciliation <strong>for each year</strong> – starting from the balances of the relevant revenue accounts, taking account of accruals and special items, against figure 200 of the settlement forms; businesses accounting under the effective method additionally provide an input-tax reconciliation. For everyday work: reconcile monthly or at least quarterly. Anyone who only looks at December once the year has closed is hunting for a needle in a haystack.</p>"""),
 ("Deadlines: day 180 and the 240-day finalisation",
  """<p>Two deadlines interlock around the year-end close:</p>
<ul>
<li><strong>Day 180 (Art. 72 para. 1 VAT Act):</strong> if, when preparing the annual accounts, you discover defects in your tax settlements, you must correct them <strong>no later than in the settlement for the accounting period into which the 180th day after the end of the financial year falls</strong>. For the 2026 financial year (calendar year), day 180 is <strong>29 June 2027</strong> – with quarterly accounting, the correction must therefore appear in the Q2 2027 settlement at the latest.</li>
<li><strong>Finalisation after 240 days (FTA practice):</strong> if no correcting settlement reaches the FTA within 240 days of the end of the financial year – <strong>28 August 2027</strong> for 2026 – the FTA assumes the submitted VAT settlements are complete and correct and that the tax period is finalised.</li>
</ul>
<p>Corrections are made in the form prescribed by the FTA (Art. 72 para. 3 VAT Act) using the official form "Jahresabstimmung (Berichtigungsabrechnung nach Art. 72 MWSTG)"; only the differences from the settlements submitted so far are declared. If the comparison with the annual accounts reveals no defects, no correcting settlement is required. And note: recognised defects must also be corrected after the fact outside the year-end close, as long as the tax claims are neither res judicata nor time-barred (Art. 72 para. 2 VAT Act).</p>
<p><strong>Money is at stake:</strong> if the correction happens only at finalisation via the correcting settlement, <strong>default interest</strong> is owed – it runs from the due date of the tax period concerned (in general 60 days after the end of the tax period, respectively 28 February of the following year). Correcting early saves interest.</p>"""),
 ("Worked example: a restaurant day and a reconciliation month (illustrative)",
  """<p><strong>Example (illustrative):</strong> a restaurant on a Tuesday in September 2026 – one row in the cashbook:</p>
<ul>
<li>Opening cash balance: CHF 300.00</li>
<li>Cash receipts (food, drinks): CHF 1'240.00</li>
<li>TWINT receipts: CHF 860.00</li>
<li>Card payments: CHF 1'900.00</li>
<li>Cash payment out (petty cash to supplier): CHF 150.00</li>
<li>Expected cash balance: 300.00 + 1'240.00 − 150.00 = <strong>CHF 1'390.00</strong></li>
<li>Cash count at closing (actual): CHF 1'390.00 – difference: CHF 0.00</li>
<li>Total daily turnover across all payment types: CHF 4'000.00</li>
</ul>
<p><strong>Monthly turnover reconciliation (illustrative), September 2026:</strong></p>
<ul>
<li>Operating revenue per the revenue accounts: CHF 97'500.00</li>
<li>less revenue reductions (discounts, rebates): CHF 1'000.00</li>
<li>less sale of a fixed asset (old espresso machine, not in operating revenue): CHF 500.00</li>
<li>= turnover declared in the VAT settlement, figure 200: <strong>CHF 96'000.00</strong> – reconciled, the difference is explained.</li>
</ul>
<p>Both examples use invented, purely illustrative amounts; they explain the method and are not advice for any individual case.</p>"""),
 ("Gaps, retroactive books – and what happens then",
  """<p>Where records do not exist or are incomplete, or where the reported results obviously do not match the true state of affairs, the FTA <strong>assesses the tax claim at its discretion</strong> (Ermessenseinschätzung, Art. 79 para. 1 VAT Act). For cash-intensive businesses, the Federal Supreme Court's long-standing case law spells out what a cashbook is worth: a cash record reconstructed after the fact, and entries without contemporaneous supporting documents, carry no evidentiary weight; in the worst case the accounts as a whole are rejected and turnover is estimated. Such estimates regularly go against the business – with uplifts, back taxes and default interest.</p>
<p>Gaps also reach beyond VAT into the <strong>direct taxes</strong>: the annual accounts are the basis for determining profit – if the cashbook does not hold, the tax authorities will not take the declared profit at face value either. The point is not formalism but substance: can every franc of declared turnover be traced from the supporting document through the settlement into the tax return – and back? A daily cashbook with properly filed TWINT and card documents answers that question long before any audit.</p>"""),
 ("Checklist to the 2026 year-end close",
  """<ul>
<li><strong>Daily:</strong> complete the cashbook the same day – with columns for cash, TWINT and card, a daily total and a cash count at closing (record any difference).</li>
<li><strong>Documents:</strong> one supporting document per entry; keep terminal, TWINT and processor settlement reports readable for at least ten years (real-estate documents: twenty years).</li>
<li><strong>Monthly:</strong> reconcile the revenue accounts with the VAT settlements (turnover reconciliation) – not only at year-end; under the effective method, reconcile input tax too.</li>
<li><strong>2026 year-end:</strong> correct defects in the 2026 settlements by <strong>29 June 2027</strong> at the latest (day 180) via a correcting settlement in the then-open accounting period; from <strong>28 August 2027</strong> the FTA treats the tax period as finalised.</li>
<li><strong>Save interest:</strong> correcting early, before finalisation, avoids default interest running from the original due date.</li>
</ul>
<p>This article is general information, not individual advice – have your records, deadlines and turnover reconciliation reviewed by a fiduciary or tax adviser.</p>"""),
]

# ---------------- French ----------------
fr_title = "Livre de caisse : espèces et TWINT"
fr_meta = "Livre de caisse quotidien, pièces pour TWINT et cartes, rapprochement du chiffre d'affaires au 180e jour : ce qu'exigent la LTVA, le CO et l'AFC."
fr_sections = [
 ("Fin d'année 2026 : la caisse décide si la comptabilité tient",
  """<p>La TVA est un impôt fondé sur l'<strong>auto-taxation</strong> : l'entreprise déclare et paie elle-même l'impôt, et l'Administration fédérale des contributions (AFC) vérifie le déclaré lors de contrôles que l'art. 78 LTVA l'autorise à mener. Ce système repose sur la confiance dans les enregistrements de l'entreprise – et cette confiance a une condition : des écritures complètes, contemporaines et pièces à l'appui.</p>
<p>Au plus tard à la clôture 2026, on saura si la comptabilité tient. Pour les entreprises à forte circulation d'espèces – restauration, commerce de détail, kiosques, salons de coiffure, boulangeries, take-aways – le <strong>livre de caisse</strong> est au centre : recettes en espèces, TWINT et paiements par carte s'y rejoignent chaque jour. Ce guide présente ce qu'exigent la LTVA, le Code des obligations et la pratique de l'AFC : de l'enregistrement quotidien à la conservation et au rapprochement du chiffre d'affaires, jusqu'aux délais applicables autour de la clôture 2026.</p>"""),
 ("Qui doit tenir quels livres : deux seuils, deux lois",
  """<p>Deux seuils différents, deux lois – à ne pas confondre :</p>
<ul>
<li><strong>Obligation de tenir des comptes (CO) :</strong> les entreprises individuelles et les sociétés de personnes tiennent une comptabilité complète dès qu'elles réalisent un chiffre d'affaires d'au moins <strong>CHF 500'000</strong> dans l'exercice (art. 957 al. 1 ch. 1 CO). En dessous, il suffit d'enregistrer <strong>les recettes, les dépenses et la situation patrimoniale</strong> – la comptabilité simplifiée dite « Milchbüchleinrechnung » (art. 957 al. 2 CO) ; les principes d'une comptabilité régulière s'appliquent par analogie (al. 3).</li>
<li><strong>Impôts directs :</strong> en cas de comptabilité simplifiée, la déclaration d'impôt doit être accompagnée d'états des recettes et des dépenses, de la situation patrimoniale ainsi que des prélèvements et apports privés (art. 125 al. 2 let. b LIFD).</li>
<li><strong>TVA (LTVA) :</strong> quiconque est assujetti à la TVA – en règle générale dès CHF 100'000 de chiffre d'affaires annuel (art. 10 al. 2 let. a LTVA) – tient ses livres et enregistrements <strong>selon les principes de la comptabilité commerciale</strong>, quel que soit le seuil du CO (art. 70 al. 1 LTVA). L'AFC peut prescrire des obligations d'enregistrement supplémentaires lorsque cela est indispensable à une perception régulière de l'impôt.</li>
</ul>
<p><strong>En pratique :</strong> un petit take-away réalisant CHF 300'000 de chiffre d'affaires n'a pas besoin de bilan selon le CO – mais s'il est assujetti à la TVA, ses enregistrements doivent résister à un contrôle TVA. Le livre de caisse tenu au jour le jour en est le fondement.</p>"""),
 ("Le livre de caisse quotidien : contenu, forme, comptage",
  """<p>Le droit suisse ne prescrit aucun système de caisse ni logiciel déterminé. Ce qui compte, c'est un <strong>enregistrement propre à servir de preuve</strong> : complet, contemporain, compréhensible et non reconstitué après coup. Chaque ligne du livre de caisse doit comporter :</p>
<ul>
<li>la <strong>date</strong> (idéalement une numérotation continue par jour ouvrable),</li>
<li>les <strong>recettes séparées par mode de paiement</strong> – espèces, TWINT, cartes de débit/crédit,</li>
<li>les <strong>dépenses</strong> (sorties d'espèces : petits achats, appoint du fonds de caisse),</li>
<li>le <strong>solde courant et l'encaisse de fin de journée</strong>.</li>
</ul>
<p>Pour les entreprises à forte circulation d'espèces, la pratique exige en outre le <strong>comptage quotidien de la caisse</strong> : à la fermeture, on compte les espèces effectivement présentes, on les compare au solde théorique du livre de caisse, et tout écart est consigné et expliqué. Chaque écriture nécessite une <strong>pièce justificative</strong> – reçu, rouleau de caisse (Z-Bon), facture, relevé TWINT ou terminal. L'enregistrement doit être <strong>chronologique et systématique</strong> : le journal comptable saisit chronologiquement toutes les opérations (art. 1 al. 2 let. b de l'ordonnance sur les livres comptables, Olico/GeBüV), et la comptabilité doit être complète, véridique et systématique (art. 957a al. 2 CO).</p>
<p><strong>Conseil pratique :</strong> quiconque « reconstitue » le livre de caisse en fin de mois, de mémoire ou d'après les relevés bancaires, produit un livre de caisse après coup – précisément la configuration dépourvue de force probante en cas de contrôle.</p>"""),
 ("TWINT et cartes : les recettes électroniques ne sont pas une annexe",
  """<p>Idée reçue fréquente : « TWINT et les cartes ne sont pas des espèces, donc ils n'ont pas leur place dans le livre de caisse. » Vrai : les recettes électroniques n'entrent pas dans l'encaisse <em>espèces</em>. Faux : elles ne seraient pas soumises à l'obligation d'enregistrement – elles font tout autant partie des contre-prestations à saisir sans lacune et à déclarer. Au quotidien, cela signifie :</p>
<ul>
<li>Tenez une colonne ou un livre auxiliaire propre à chaque mode de paiement : espèces, TWINT, cartes.</li>
<li>Consignez les totaux journaliers de l'app TWINT et du terminal de cartes – comme pour les espèces.</li>
<li>Conservez les <strong>décomptes des prestataires de paiement</strong> (clôtures journalières et mensuelles) comme pièces comptables et rapprochez-les des montants enregistrés.</li>
<li>Comptabilisez les <strong>recettes brutes</strong> : les frais de prestataires et d'acquéreurs sont une charge, pas une diminution du chiffre d'affaires.</li>
</ul>
<p>Dans le rapprochement du chiffre d'affaires, les encaissements électroniques doivent rester traçables – l'ordonnance mentionne expressément « les autres entrées de paiements qui ne sont pas comprises dans le chiffre d'affaires comptabilisé » (art. 128 al. 2 let. f OTVA). Là où le flux TWINT est invisible dans la comptabilité, un contrôle finira par révéler un écart qu'il faudra expliquer.</p>
<p><strong>Conseil pratique :</strong> si un compte TWINT privé sert aux encaissements de l'entreprise, transposez ces recettes sans lacune dans la comptabilité commerciale – des flux privés et commerciaux mélangés sont une constatation classique de contrôle.</p>
""" + CTA_MID["fr"]),
 ("Conservation : dix ans – vingt ans pour les immeubles",
  """<p>Les délais de conservation en bref :</p>
<ul>
<li><strong>TVA :</strong> livres comptables, pièces, papiers d'affaires et autres enregistrements doivent être conservés régulièrement <strong>jusqu'à la prescription absolue de la créance fiscale</strong> – en règle générale dix ans après la fin de la période fiscale (art. 70 al. 2 en lien avec l'art. 42 al. 6 LTVA).</li>
<li><strong>Droit commercial :</strong> livres comptables et pièces justificatives – ainsi que le rapport de gestion et le rapport de révision – se conservent <strong>dix ans</strong> ; le délai court dès la fin de l'exercice (art. 958f al. 1 CO).</li>
<li><strong>Immeubles :</strong> les documents servant au calcul de la déduction de l'impôt préalable sur les immeubles et de la consommation propre se conservent <strong>vingt ans</strong> (art. 70 al. 3 LTVA).</li>
</ul>
<p>La conservation électronique est admise : livres et pièces peuvent être tenus sur papier, électroniquement ou d'une manière comparable, pour autant que la concordance avec les opérations sous-jacentes soit garantie et qu'ils puissent être rendus lisibles en tout temps (art. 958f al. 3 CO ; sur le traitement régulier des données, art. 2 al. 2 Olico). Les décomptes TWINT et de cartes n'arrivent en général qu'en version électronique – conservez-les de façon à ce qu'ils restent lisibles et reproductibles dans dix ans.</p>"""),
 ("Rapprochement du chiffre d'affaires : contenu et méthode",
  """<p>Le <strong>rapprochement du chiffre d'affaires (Umsatzabstimmung)</strong> montre comment la déclaration de la période fiscale – compte tenu des différents taux d'imposition ou des taux de la dette fiscale nette / des taux forfaitaires – est mise en concordance avec les comptes annuels (art. 128 al. 2 OTVA). L'ordonnance cite notamment :</p>
<ul>
<li>le <strong>chiffre d'affaires comptabilisé</strong> dans les comptes annuels ;</li>
<li>les produits enregistrés dans des <strong>comptes de charges</strong> (réductions de charges) ;</li>
<li>les <strong>compensations internes au groupe</strong> non comprises dans le chiffre d'affaires ;</li>
<li>les <strong>ventes de moyens d'exploitation</strong>, les <strong>paiements anticipés</strong> et les <strong>autres entrées de paiements</strong> non comprises dans le chiffre d'affaires comptabilisé ;</li>
<li>les <strong>prestations en nature</strong>, les <strong>diminutions de produits</strong> et les <strong>pertes sur débiteurs</strong> ;</li>
<li>les <strong>écritures de clôture</strong> telles que délimitations temporelles, provisions et reclassements internes sans incidence sur le chiffre d'affaires.</li>
</ul>
<p>Lors d'un contrôle TVA, l'AFC exige le rapprochement du chiffre d'affaires <strong>par année</strong> – en partant des soldes des comptes de produits déterminants, compte tenu des éléments de délimitation et des postes spéciaux, face au chiffre 200 des formulaires de décompte ; les entreprises décomptant selon la méthode effective produisent en outre un rapprochement de l'impôt préalable. Au quotidien : rapprochez chaque mois, ou au moins chaque trimestre. Qui ne regarde décembre qu'une fois l'année close cherche une aiguille dans une botte de foin.</p>"""),
 ("Délais : le 180e jour et la finalisation à 240 jours",
  """<p>Deux délais s'articulent autour de la clôture :</p>
<ul>
<li><strong>Le 180e jour (art. 72 al. 1 LTVA) :</strong> si, en établissant les comptes annuels, vous constatez des irrégularités dans vos décomptes fiscaux, vous devez les corriger <strong>au plus tard dans le décompte de la période qui inclut le 180e jour suivant la fin de l'exercice</strong>. Pour l'exercice 2026 (année civile), le 180e jour est le <strong>29 juin 2027</strong> – avec un décompte trimestriel, la correction doit donc figurer au plus tard dans le décompte du 2e trimestre 2027.</li>
<li><strong>Finalisation après 240 jours (pratique de l'AFC) :</strong> si aucun décompte de rectification ne parvient à l'AFC dans les 240 jours suivant la fin de l'exercice – le <strong>28 août 2027</strong> pour 2026 – l'AFC considère que les décomptes TVA déposés sont complets et corrects et que la période fiscale est finalisée.</li>
</ul>
<p>La correction s'opère dans la forme prescrite par l'AFC (art. 72 al. 3 LTVA) au moyen du formulaire officiel « Jahresabstimmung (Berichtigungsabrechnung nach Art. 72 MWSTG) » ; seules les différences par rapport aux décomptes déjà déposés y sont déclarées. Si la comparaison avec les comptes annuels ne révèle aucune irrégularité, aucun décompte de rectification n'est requis. À noter : les irrégularités constatées doivent aussi être corrigées ultérieurement en dehors de la clôture, tant que les créances fiscales ne sont pas entrées en force ni prescrites (art. 72 al. 2 LTVA).</p>
<p><strong>Question d'argent :</strong> si la correction n'intervient qu'au moment de la finalisation avec le décompte de rectification, un <strong>intérêt moratoire</strong> est dû – il court dès l'échéance de la période fiscale concernée (en règle générale 60 jours après la fin de la période, respectivement le 28 février de l'année suivante). Corriger tôt économise des intérêts.</p>"""),
 ("Exemple chiffré : une journée de restaurant et un mois de rapprochement (illustratif)",
  """<p><strong>Exemple (illustratif) :</strong> un établissement de restauration, un mardi de septembre 2026 – une ligne du livre de caisse :</p>
<ul>
<li>Encaisse d'ouverture : CHF 300.00</li>
<li>Recettes en espèces (plats, boissons) : CHF 1'240.00</li>
<li>Recettes TWINT : CHF 860.00</li>
<li>Paiements par carte : CHF 1'900.00</li>
<li>Dépense en espèces (caisse de menu frais au fournisseur) : CHF 150.00</li>
<li>Encaisse théorique : 300.00 + 1'240.00 − 150.00 = <strong>CHF 1'390.00</strong></li>
<li>Comptage à la fermeture (effectif) : CHF 1'390.00 – écart : CHF 0.00</li>
<li>Chiffre d'affaires du jour, tous modes de paiement : CHF 4'000.00</li>
</ul>
<p><strong>Rapprochement mensuel du chiffre d'affaires (illustratif), septembre 2026 :</strong></p>
<ul>
<li>Chiffre d'affaires selon les comptes de produits : CHF 97'500.00</li>
<li>déduction faite des diminutions de produits (escomptes, rabais) : CHF 1'000.00</li>
<li>déduction faite de la vente d'un moyen d'exploitation (vieille machine à expresso, hors chiffre d'affaires) : CHF 500.00</li>
<li>= chiffre d'affaires déclaré dans le décompte TVA, chiffre 200 : <strong>CHF 96'000.00</strong> – rapproché, l'écart est expliqué.</li>
</ul>
<p>Les deux exemples utilisent des montants inventés, purement illustratifs ; ils expliquent la méthode et ne constituent pas une recommandation pour un cas concret.</p>"""),
 ("Lacunes, livres reconstitués – et ce qui s'ensuit",
  """<p>Lorsqu'il n'existe pas d'enregistrements, qu'ils sont incomplets ou que les résultats déclarés ne correspondent manifestement pas à la réalité, l'AFC <strong>procède à une estimation de la créance fiscale selon son pouvoir d'appréciation</strong> (taxation d'office, art. 79 al. 1 LTVA). Pour les entreprises à forte circulation d'espèces, la jurisprudence constante du Tribunal fédéral précise ce que vaut un livre de caisse : un enregistrement reconstitué après coup et des écritures sans pièces contemporaines n'ont aucune force probante ; dans le pire des cas, la comptabilité entière est écartée et le chiffre d'affaires est estimé. Les estimations se font régulièrement au détriment de l'entreprise – suppléments d'impôt, rappel et intérêt moratoire.</p>
<p>Les lacunes déploient aussi leurs effets au-delà de la TVA, dans les <strong>impôts directs</strong> : les comptes annuels fondent la détermination du bénéfice – si le livre de caisse ne tient pas, les autorités fiscales ne reprendront pas non plus le bénéfice déclaré sans examen. Il ne s'agit pas de formalisme mais de substance : chaque franc de chiffre d'affaires déclaré peut-il être suivi de la pièce justificative au décompte, puis à la déclaration d'impôt – et en sens inverse ? Un livre de caisse tenu au jour le jour, avec les pièces TWINT et cartes classées proprement, répond à cette question bien avant tout contrôle.</p>"""),
 ("Check-list jusqu'à la clôture 2026",
  """<ul>
<li><strong>Chaque jour :</strong> tenir le livre de caisse le jour même – colonnes espèces, TWINT et cartes, total journalier et comptage à la fermeture (consigner les écarts).</li>
<li><strong>Pièces :</strong> une pièce par écriture ; conserver les décomptes de terminal, TWINT et prestataires lisibles pendant au moins dix ans (documents immobiliers : vingt ans).</li>
<li><strong>Chaque mois :</strong> rapprocher les comptes de produits des décomptes TVA (rapprochement du chiffre d'affaires) – pas seulement en fin d'année ; sous la méthode effective, rapprocher aussi l'impôt préalable.</li>
<li><strong>Fin d'année 2026 :</strong> corriger les irrégularités des décomptes 2026 au plus tard le <strong>29 juin 2027</strong> (180e jour) par un décompte de rectification dans la période de décompte encore ouverte ; dès le <strong>28 août 2027</strong>, l'AFC considère la période fiscale comme finalisée.</li>
<li><strong>Économiser des intérêts :</strong> une correction avant la finalisation évite l'intérêt moratoire dès l'échéance initiale.</li>
</ul>
<p>Cet article constitue une information générale, non un conseil individuel – faites vérifier vos enregistrements, délais et rapprochements par un fiduciaire ou un conseiller fiscal.</p>"""),
]

# ---------------- Italian ----------------
it_title = "Libro di cassa: contanti, TWINT, carte"
it_meta = "Libro di cassa giornaliero, giustificativi per TWINT e carte, riconciliazione della cifra d'affari entro il 180° giorno: cosa richiedono LIVA, CO e AFC."
it_sections = [
 ("Fine anno 2026: è la cassa a decidere se la contabilità regge",
  """<p>L'imposta sul valore aggiunto è un'imposta basata sull'<strong>autotassazione</strong>: l'azienda dichiara e versa l'imposta da sé, e l'Amministrazione federale delle contribuzioni (AFC) verifica il dichiarato in controlli che l'art. 78 LIVA la autorizza a effettuare. Il sistema si fonda sulla fiducia nelle registrazioni dell'azienda – e questa fiducia ha una condizione: scritture complete, contemporanee e documentate.</p>
<p>Al più tardi con la chiusura del 2026 si vede se la contabilità regge. Per le aziende con intenso uso di contante – ristorazione, commercio al dettaglio, chioschi, parrucchieri, panetterie, take-away – il <strong>libro di cassa</strong> è al centro: incassi in contanti, TWINT e pagamenti con carta vi confluiscono ogni giorno. Questa guida illustra cosa richiedono la LIVA, il Codice delle obbligazioni e la prassi dell'AFC: dalla registrazione giornaliera alla conservazione e alla riconciliazione della cifra d'affari, fino alle scadenze applicabili attorno alla chiusura 2026.</p>"""),
 ("Chi deve tenere quali libri: due soglie, due leggi",
  """<p>Due soglie diverse, due leggi – da non confondere:</p>
<ul>
<li><strong>Obbligo di tenere la contabilità (CO):</strong> le imprese individuali e le società di persone tengono una contabilità completa non appena realizzano una cifra d'affari di almeno <strong>CHF 500'000</strong> nell'esercizio (art. 957 cpv. 1 n. 1 CO). Al di sotto basta registrare <strong>entrate, uscite e situazione patrimoniale</strong> – la contabilità semplificata (art. 957 cpv. 2 CO); i principi di una tenuta regolare dei conti si applicano per analogia (cpv. 3).</li>
<li><strong>Imposte dirette:</strong> chi tiene una contabilità semplificata allega alla dichiarazione d'imposta i prospetti di entrate e uscite, della situazione patrimoniale nonché dei prelievi e apporti privati (art. 125 cpv. 2 lett. b LIFD).</li>
<li><strong>IVA (LIVA):</strong> chi è registrato all'IVA – di regola da CHF 100'000 di cifra d'affari annua (art. 10 cpv. 2 lett. a LIVA) – tiene libri commerciali e registrazioni <strong>secondo i principi della contabilità commerciale</strong>, indipendentemente dalla soglia del CO (art. 70 cpv. 1 LIVA). L'AFC può prescrivere ulteriori obblighi di registrazione quando sono indispensabili per una corretta riscossione dell'imposta.</li>
</ul>
<p><strong>In pratica:</strong> un piccolo take-away con CHF 300'000 di cifra d'affari non ha bisogno di un bilancio secondo il CO – ma se è registrato all'IVA, le sue registrazioni devono resistere a un controllo IVA. Il libro di cassa tenuto giornalmente ne è la base.</p>"""),
 ("Il libro di cassa giornaliero: contenuto, forma, conteggio",
  """<p>Il diritto svizzero non prescrive un determinato sistema di cassa o software. Decisiva è una <strong>registrazione idonea a servire da prova</strong>: completa, contemporanea, comprensibile e non ricostruita dopo il fatto. Ogni riga del libro di cassa deve contenere:</p>
<ul>
<li>la <strong>data</strong> (idealmente con numerazione progressiva per giorno lavorativo),</li>
<li>gli <strong>incassi separati per modalità di pagamento</strong> – contanti, TWINT, carte di debito/credito,</li>
<li>le <strong>uscite</strong> (pagamenti in contanti: piccoli acquisti, reintegro del fondo cassa),</li>
<li>il <strong>saldo corrente e la consistenza di cassa di fine giornata</strong>.</li>
</ul>
<p>Per le aziende con intenso uso di contante la prassi richiede inoltre il <strong>conteggio giornaliero della cassa</strong>: alla chiusura si contano i contanti effettivamente presenti, si confrontano con il saldo teorico del libro di cassa e ogni differenza viene annotata e spiegata. Ogni scrittura necessita di un <strong>giustificativo</strong> – scontrino, rotolo di cassa (Z-Bon), fattura, estratto TWINT o del terminale. La registrazione deve essere <strong>cronologica e sistematica</strong>: il giornale contabile registra cronologicamente tutte le operazioni (art. 1 cpv. 2 lett. b dell'ordinanza sulla tenuta dei libri contabili, OLCo/GeBüV) e la contabilità deve essere completa, veritiera e sistematica (art. 957a cpv. 2 CO).</p>
<p><strong>Consiglio pratico:</strong> chi «ricostruisce» il libro di cassa a fine mese, a memoria o dagli estratti bancari, produce un libro di cassa a posteriori – proprio la configurazione priva di forza probatoria in un controllo.</p>"""),
 ("TWINT e carte: gli incassi elettronici non sono un dettaglio",
  """<p>Un equivoco diffuso: «TWINT e carte non sono contanti, quindi non appartengono al libro di cassa». Vero: gli incassi elettronici non entrano nella <em>cassa</em> contanti. Falso: non sarebbero soggetti all'obbligo di registrazione – anch'essi fanno parte delle controprestazioni da rilevare senza lacune e da dichiarare. Nella pratica quotidiana ciò significa:</p>
<ul>
<li>Tenete una colonna o un libro ausiliario per ogni modalità di pagamento: contanti, TWINT, carte.</li>
<li>Annotate i totali giornalieri dell'app TWINT e del terminale carte – come per i contanti.</li>
<li>Conservate i <strong>rendiconti dei prestatori di servizi di pagamento</strong> (chiusure giornaliere e mensili) come giustificativi contabili e riconciliateli con gli importi registrati.</li>
<li>Registrate gli <strong>incassi lordi</strong>: le commissioni dei prestatori e degli acquirer sono un costo, non una riduzione della cifra d'affari.</li>
</ul>
<p>Nella riconciliazione della cifra d'affari gli incassi elettronici devono restare tracciabili – l'ordinanza menziona espressamente «le altre entrate di pagamenti non comprese nella cifra d'affari contabilizzata» (art. 128 cpv. 2 lett. f OIVA). Dove il flusso TWINT non è visibile in contabilità, un controllo finirà per far emergere una differenza da spiegare.</p>
<p><strong>Consiglio pratico:</strong> se un conto TWINT privato è usato per incassi aziendali, riportate senza lacune queste entrate nella contabilità aziendale – flussi privati e aziendali mescolati sono un tipico rilievo di controllo.</p>
""" + CTA_MID["it"]),
 ("Conservazione: dieci anni – venti per gli immobili",
  """<p>I termini di conservazione in sintesi:</p>
<ul>
<li><strong>IVA:</strong> libri commerciali, giustificativi, documenti d'affari e altre registrazioni vanno conservati regolarmente <strong>fino alla prescrizione assoluta del credito fiscale</strong> – di regola dieci anni dalla fine del periodo fiscale (art. 70 cpv. 2 in relazione con l'art. 42 cpv. 6 LIVA).</li>
<li><strong>Diritto commerciale:</strong> libri commerciali e giustificativi – così come il rapporto di gestione e il rapporto di revisione – si conservano per <strong>dieci anni</strong>; il termine decorre dalla fine dell'esercizio (art. 958f cpv. 1 CO).</li>
<li><strong>Immobili:</strong> i documenti necessari al calcolo della sgravio dell'imposta precedente sugli immobili e della prestazione a sé stessi si conservano per <strong>venti anni</strong> (art. 70 cpv. 3 LIVA).</li>
</ul>
<p>La conservazione elettronica è ammessa: libri e giustificativi possono essere tenuti su carta, in forma elettronica o in modo analogo, per quanto sia garantita la corrispondenza con le operazioni sottostanti e possano essere resi leggibili in qualsiasi momento (art. 958f cpv. 3 CO; sui principi di un trattamento regolare dei dati, art. 2 cpv. 2 OLCo). I rendiconti TWINT e delle carte arrivano di norma solo in forma elettronica – conservateli in modo che restino leggibili e riproducibili tra dieci anni.</p>"""),
 ("Riconciliazione della cifra d'affari: cos'è e cosa contiene",
  """<p>La <strong>riconciliazione della cifra d'affari (Umsatzabstimmung)</strong> mostra come la dichiarazione del periodo fiscale – tenendo conto delle varie aliquote o delle aliquote saldo/forfettarie – viene portata in conformità con il conto annuale (art. 128 cpv. 2 OIVA). L'ordinanza cita in particolare:</p>
<ul>
<li>la <strong>cifra d'affari contabilizzata</strong> nel conto annuale;</li>
<li>i proventi registrati in <strong>conti di costo</strong> (riduzioni di costi);</li>
<li>le <strong>compensazioni interne al gruppo</strong> non comprese nella cifra d'affari;</li>
<li>le <strong>vendite di mezzi d'esercizio</strong>, i <strong>pagamenti anticipati</strong> e le <strong>altre entrate di pagamenti</strong> non comprese nella cifra d'affari contabilizzata;</li>
<li>le <strong>prestazioni in natura</strong>, le <strong>riduzioni dei proventi</strong> e le <strong>perdite su debitori</strong>;</li>
<li>le <strong>scritture di chiusura</strong> quali delimitazioni temporali, accantonamenti e riclassifiche interne senza rilevanza per la cifra d'affari.</li>
</ul>
<p>In un controllo IVA l'AFC richiede la riconciliazione della cifra d'affari <strong>per ogni anno</strong> – partendo dai saldi dei conti di ricavo determinanti, tenendo conto delle poste di delimitazione e delle voci speciali, rispetto alla cifra 200 dei moduli di rendiconto; chi rendiconta secondo il metodo effettivo presenta inoltre una riconciliazione dell'imposta precedente. Nella pratica quotidiana: riconciliate ogni mese, o almeno ogni trimestre. Chi guarda dicembre solo a anno chiuso cerca un ago in un pagliaio.</p>"""),
 ("Scadenze: il 180° giorno e la finalizzazione a 240 giorni",
  """<p>Due scadenze si intrecciano attorno alla chiusura:</p>
<ul>
<li><strong>Il 180° giorno (art. 72 cpv. 1 LIVA):</strong> se, allestendo il conto annuale, constatate irregolarità nei vostri rendiconti fiscali, dovete correggerle <strong>al più tardi nel rendiconto del periodo di conteggio in cui cade il 180° giorno dalla fine dell'esercizio</strong>. Per l'esercizio 2026 (anno civile) il 180° giorno è il <strong>29 giugno 2027</strong> – con rendiconti trimestrali, la correzione deve quindi comparire al più tardi nel rendiconto del 2° trimestre 2027.</li>
<li><strong>Finalizzazione dopo 240 giorni (prassi AFC):</strong> se entro 240 giorni dalla fine dell'esercizio non giunge all'AFC alcun rendiconto di rettifica – per il 2026 il <strong>28 agosto 2027</strong> – l'AFC presume che i rendiconti IVA depositati siano completi e corretti e che il periodo fiscale sia finalizzato.</li>
</ul>
<p>La correzione avviene nella forma prescritta dall'AFC (art. 72 cpv. 3 LIVA) con il modulo ufficiale «Jahresabstimmung (Berichtigungsabrechnung nach Art. 72 MWSTG)»; vi si dichiarano solo le differenze rispetto ai rendiconti finora depositati. Se il confronto con il conto annuale non rivela irregolarità, nessun rendiconto di rettifica è necessario. Da notare: le irregolarità riconosciute vanno corrette anche al di fuori della chiusura, finché i crediti fiscali non sono passati in giudicato o prescritti (art. 72 cpv. 2 LIVA).</p>
<p><strong>Si tratta di denaro:</strong> se la correzione avviene solo al momento della finalizzazione con il rendiconto di rettifica, è dovuto un <strong>interesse di mora</strong> – che decorre dalla scadenza del periodo fiscale interessato (di regola 60 giorni dalla fine del periodo, rispettivamente il 28 febbraio dell'anno successivo). Chi corregge presto risparmia interessi.</p>"""),
 ("Esempio di calcolo: una giornata di ristorante e un mese di riconciliazione (illustrativo)",
  """<p><strong>Esempio (illustrativo):</strong> un ristorante in un martedì di settembre 2026 – una riga del libro di cassa:</p>
<ul>
<li>Consistenza iniziale di cassa: CHF 300.00</li>
<li>Incassi in contanti (pietanze, bevande): CHF 1'240.00</li>
<li>Incassi TWINT: CHF 860.00</li>
<li>Pagamenti con carta: CHF 1'900.00</li>
<li>Uscita in contanti (pagamento al fornitore dal fondo cassa): CHF 150.00</li>
<li>Consistenza teorica di cassa: 300.00 + 1'240.00 − 150.00 = <strong>CHF 1'390.00</strong></li>
<li>Conteggio alla chiusura (effettivo): CHF 1'390.00 – differenza: CHF 0.00</li>
<li>Cifra d'affari del giorno, tutte le modalità di pagamento: CHF 4'000.00</li>
</ul>
<p><strong>Riconciliazione mensile della cifra d'affari (illustrativa), settembre 2026:</strong></p>
<ul>
<li>Cifra d'affari secondo i conti di ricavo: CHF 97'500.00</li>
<li>dedotte le riduzioni dei proventi (sconti, ribassi): CHF 1'000.00</li>
<li>dedotta la vendita di un mezzo d'esercizio (vecchia macchina per espresso, fuori cifra d'affari): CHF 500.00</li>
<li>= cifra d'affari dichiarata nel rendiconto IVA, cifra 200: <strong>CHF 96'000.00</strong> – riconciliata, la differenza è spiegata.</li>
</ul>
<p>Entrambi gli esempi usano importi inventati, puramente illustrativi; spiegano il metodo e non costituiscono una raccomandazione per il caso singolo.</p>"""),
 ("Lacune, libri ricostruiti – e cosa succede",
  """<p>Se le registrazioni non esistono o sono incomplete, oppure se i risultati esposti non corrispondono manifestamente alla situazione reale, l'AFC <strong>stima il credito fiscale secondo il proprio prudente apprezzamento</strong> (tassazione d'ufficio, art. 79 cpv. 1 LIVA). Per le aziende con intenso uso di contante la giurisprudenza costante del Tribunale federale precisa quanto vale un libro di cassa: una registrazione di cassa ricostruita dopo il fatto e scritture senza giustificativi contemporanei non hanno forza probatoria; nel caso peggiore l'intera contabilità viene scartata e la cifra d'affari è stimata. Le stime vanno regolarmente a sfavore dell'azienda – con riprese d'imposta, recuperi e interessi di mora.</p>
<p>Le lacune si ripercuotono inoltre oltre l'IVA, nelle <strong>imposte dirette</strong>: il conto annuale è la base per determinare l'utile – se il libro di cassa non regge, nemmeno le autorità fiscali accoglieranno l'utile dichiarato senza esame. Non si tratta di formalismo ma di sostanza: ogni franco di cifra d'affari dichiarata può essere seguito dal giustificativo al rendiconto fino alla dichiarazione d'imposta – e a ritroso? Un libro di cassa tenuto giornalmente, con i giustificativi TWINT e carte archiviati in ordine, risponde a questa domanda ben prima di qualsiasi controllo.</p>"""),
 ("Checklist fino alla chiusura del 2026",
  """<ul>
<li><strong>Ogni giorno:</strong> tenere il libro di cassa lo stesso giorno – con colonne per contanti, TWINT e carte, totale giornaliero e conteggio della cassa alla chiusura (annotare le differenze).</li>
<li><strong>Giustificativi:</strong> un giustificativo per ogni scrittura; conservare i rendiconti di terminale, TWINT e prestatori leggibili per almeno dieci anni (documenti relativi a immobili: venti anni).</li>
<li><strong>Ogni mese:</strong> riconciliare i conti di ricavo con i rendiconti IVA (riconciliazione della cifra d'affari) – non solo a fine anno; con il metodo effettivo riconciliare anche l'imposta precedente.</li>
<li><strong>Fine anno 2026:</strong> correggere le irregolarità dei rendiconti 2026 entro il <strong>29 giugno 2027</strong> (180° giorno) con un rendiconto di rettifica nel periodo di conteggio ancora aperto; dal <strong>28 agosto 2027</strong> l'AFC considera il periodo fiscale finalizzato.</li>
<li><strong>Risparmiare interessi:</strong> correggere prima della finalizzazione evita l'interesse di mora dalla scadenza originaria.</li>
</ul>
<p>Questo articolo è informazione generale e non consulenza individuale – fate verificare registrazioni, scadenze e riconciliazione della cifra d'affari da un fiduciario o consulente fiscale.</p>"""),
]

SOURCES = {
    "de": list(zip(URLS, [
        "MWSTG (SR 641.20) – Art. 42, 70, 72, 79",
        "MWSTV (SR 641.201) – Art. 128 (Umsatzabstimmung)",
        "Obligationenrecht (SR 220) – Art. 957, 957a, 958f",
        "Geschäftsbücherverordnung (SR 221.431) – Art. 1–2",
        "DBG (SR 642.11) – Art. 125",
        "ESTV: MWST-Jahresabstimmung (Berichtigungsabrechnung nach Art. 72 MWSTG)",
        "ESTV: Unterlagen für die MWST-Kontrolle",
        "ESTV: MWST-Kontrolle"])),
    "en": list(zip(URLS, [
        "VAT Act (SR 641.20) – Art. 42, 70, 72, 79",
        "VAT Ordinance (SR 641.201) – Art. 128 (turnover reconciliation)",
        "Code of Obligations (SR 220) – Art. 957, 957a, 958f",
        "Business Records Ordinance (SR 221.431) – Art. 1–2",
        "Federal Act on Direct Federal Tax (SR 642.11) – Art. 125",
        "FTA: VAT year-end reconciliation (correcting settlement under Art. 72 VAT Act)",
        "FTA: Documents for the VAT control",
        "FTA: VAT control"])),
    "fr": list(zip(URLS, [
        "LTVA (RS 641.20) – art. 42, 70, 72, 79",
        "OTVA (RS 641.201) – art. 128 (rapprochement du chiffre d'affaires)",
        "Code des obligations (RS 220) – art. 957, 957a, 958f",
        "Ordonnance sur les livres comptables (RS 221.431) – art. 1–2",
        "LIFD (RS 642.11) – art. 125",
        "AFC : décompte annuel TVA (décompte de rectification selon l'art. 72 LTVA)",
        "AFC : documents pour le contrôle TVA",
        "AFC : contrôle TVA"])),
    "it": list(zip(URLS, [
        "LIVA (RS 641.20) – art. 42, 70, 72, 79",
        "OIVA (RS 641.201) – art. 128 (riconciliazione della cifra d'affari)",
        "Codice delle obbligazioni (RS 220) – art. 957, 957a, 958f",
        "Ordinanza sulla tenuta dei libri contabili (RS 221.431) – art. 1–2",
        "LIFD (RS 642.11) – art. 125",
        "AFC: riconciliazione annuale IVA (rendiconto di rettifica secondo l'art. 72 LIVA)",
        "AFC: documenti per il controllo IVA",
        "AFC: controllo IVA"])),
}

DATA = [("de", de_title, de_meta, de_sections),
        ("en", en_title, en_meta, en_sections),
        ("fr", fr_title, fr_meta, fr_sections),
        ("it", it_title, it_meta, it_sections)]

for lang, title, meta, sections in DATA:
    assert len(title) <= 40, (lang, "title", len(title))
    assert len(meta) <= 158, (lang, "meta", len(meta))
    assert 8 <= len(sections) <= 10, (lang, "sections", len(sections))
    build(lang, SLUG, title, meta, sections, related=RELATED, sources=SOURCES[lang])
    print(f"{lang}: title {len(title)} chars, meta {len(meta)} chars, {len(sections)} sections")
print("done")
