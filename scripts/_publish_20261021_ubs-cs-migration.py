#!/usr/bin/env python3
"""Build the UBS/CS migration + tax return 2026 article in all 4 languages.

Slug: ubs-cs-migration-steuererklaerung-2026
Sources (all primary/first-party, verified 2026-10-21):
- UBS media release 18.3.2026 "UBS successfully completes the client migration
  in Switzerland" (browser-verified 200; ubs.com bot-walls curl with 403):
  ~1.2m clients transferred globally, integration substantially complete by
  end of 2026.
- UBS/CS client FAQ "Ihre Reise zu UBS" (ubs.com welcome hub): old CS IBAN
  payments forwarded >= 24 months; standing orders/LSV transferred
  automatically; two separate fee invoices in the migration month; contact
  exclusively via letter or CS Online & Mobile Banking; documents of accounts
  closed before transfer downloadable in CS e-banking only until 3 months
  after transfer (incl. 3a payment confirmations and interest statements).
- ESTV Kurslisten (ICTax), estv.admin.ch (curl 200): December year-end rates =
  tax value at 31 December (Art. 14/17 Abs. 1 StHG).
- ESTV Dossier Steuerinformationen, Vermögenssteuer natürlicher Personen
  (estv2.admin.ch, curl 200): valuation date 31.12; 2026 return filed 2027;
  listed securities valued per ESTV rate list.
- ESTV Dossier Steuerinformationen, Einkommenssteuer natürlicher Personen
  (estv2.admin.ch, curl 200): capital gains on movable private assets tax-free
  (Art. 16 Abs. 3 DBG); third-party asset management costs deductible.
- Kanton Zürich, Steuererklärung Privatpersonen (curl 200): filing deadline
  31 March of the following year, extensions possible.
- fedlex StHG SR 642.14 (curl 200).

Omitted per [verifizieren] flags (no first-party confirmation available):
- whether the UBS tax statement 2026 covers the CS partial period (phrased as
  advice to reconcile/ask UBS instead of a factual claim);
- treatment of All-in-Banking certificates / registered shares renumbered at
  migration (only a generic reconciliation caveat is given);
- whether updating bank details on withholding-tax refund form 8.1 is
  mandatory (only general advice to keep bank details current).
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "ubs-cs-migration-steuererklaerung-2026"
RELATED = ["auslaendisches-depot-neobroker-steuererklaerung.html",
           "verrechnungssteuer-rueckerstattungsfrist-ablauf.html",
           "saeule-3a-nachzahlen.html"]

SRC_MR = "https://www.ubs.com/global/en/media/display-page-ndp/en-20260318-client-migration.html"
SRC_FAQ = "https://www.ubs.com/microsites/welcome-international/de/crossborder.html"
SRC_ICTAX = "https://www.estv.admin.ch/de/kurslisten-ictax"
SRC_VST = "https://www.estv2.admin.ch/stp/ds/d-vermoegenssteuer-np-de.pdf"
SRC_EST = "https://www.estv2.admin.ch/stp/ds/d-einkommenssteuer-natuerlicher-personen-gesamter-text-de.pdf"
SRC_ZH = "https://www.zh.ch/de/steuern-finanzen/steuern/steuern-natuerliche-personen/steuererklaerung-natuerliche-personen.html"
SRC_STHG = "https://www.fedlex.admin.ch/eli/cc/1993/2642_2642_2642/de"

CTA_MID = {
    "de": '<div class="cta-mid"><strong>Unklar, was das für Ihre Situation bedeutet?</strong> Eine <a href="partner-pruefung.html">geprüfte Fachperson</a> prüft Ihre Unterlagen und zeigt das konkrete Sparpotenzial – die Erstberatung ist kostenlos: <a href="kontakt.html">unverbindliche Offerte anfragen</a>.</div>',
    "en": '<div class="cta-mid"><strong>Not sure what this means for your situation?</strong> A <a href="partner-pruefung.html">vetted professional</a> reviews your documents and shows your concrete savings potential – first consultation free: <a href="kontakt.html">request a no-obligation quote</a>.</div>',
    "fr": '<div class="cta-mid"><strong>Vous ne savez pas ce que cela implique pour votre situation ?</strong> Un <a href="partner-pruefung.html">conseiller vérifié</a> examine vos documents et chiffre votre potentiel d’économie – premier entretien gratuit : <a href="kontakt.html">demandez une offre sans engagement</a>.</div>',
    "it": '<div class="cta-mid"><strong>Non sapete cosa significa in concreto per la sua situazione?</strong> Un <a href="partner-pruefung.html">consulente verificato</a> esamina i suoi documenti e indica il potenziale di risparmio – primo colloquio gratuito: <a href="kontakt.html">richieda un’offerta senza impegno</a>.</div>',
}

# ---------------- German ----------------
de_title = "UBS-Depot in der Steuererklärung 2026"
de_meta = "Seit März 2026 sind alle Ex-CS-Kunden bei UBS. So deklarieren Sie Ihr Depot 2026: Steuerauszug, Stichtag 31.12., alte CS-Belege, neue IBAN."
de_sections = [
 ("Was 2026 passiert ist: alle CS-Konten sind jetzt UBS-Konten",
  """<p>Am <strong>18. März 2026</strong> hat UBS per Medienmitteilung bestätigt: Mit der Migration der in der Schweiz gebuchten Kunden sind <strong>alle ehemaligen Credit-Suisse-Kunden weltweit auf die UBS-Infrastruktur übertragen</strong> – rund <strong>1,2 Millionen Kunden</strong> haben die Plattform gewechselt. Die Integration soll bis Ende 2026 «weitgehend» abgeschlossen sein.</p>
<p>Rechtlich ist die Credit Suisse (Schweiz) AG bereits seit dem <strong>1. Juli 2024</strong> Geschichte: Sie ging durch Fusion in der UBS Switzerland AG auf, die alle Rechte und Pflichten übernahm. 2025 und im ersten Quartal 2026 folgten die technischen Migrationen der Kundenbeziehungen – jeweils über ein Wochenende, angekündigt per Brief.</p>
<p>Für Ihre Steuern bedeutet das: Das <strong>Steuerjahr 2026</strong> ist das erste Jahr, in dem alle ehemaligen CS-Kunden per Jahresende ein UBS-Depot halten. Je nach Migrationsdatum war Ihr Jahr 2026 in eine CS- und eine UBS-Teilperiode geteilt – das hat konkrete Folgen für Belege, Erträge und die Deklaration.</p>"""),
 ("Steuerjahr 2026: eine Erklärung, möglicherweise zwei Belegsets",
  """<p>Die Steuererklärung 2026 reichen Sie <strong>im Jahr 2027</strong> ein – die Vermögenssteuer wird nach dem Stand am Ende der Steuerperiode bemessen (sog. Postnumerando-Verfahren, Art. 17 StHG). Die Frist ist kantonal unterschiedlich; im Kanton Zürich etwa endet sie am <strong>31. März des Folgejahrs</strong> und kann erstreckt werden. Wer sein Depot 2026 migriert bekam, sollte mit <strong>zwei Belegsets</strong> rechnen:</p>
<ul>
<li><strong>CS-Teilperiode</strong> (1. Januar bis zum Migrationswochenende): letzte CS-Kontoauszüge, Zins- und Dividendenabrechnungen, allfällige Schlussabrechnungen der ehemaligen CS-Einheit.</li>
<li><strong>UBS-Teilperiode</strong> (ab Migration bis 31. Dezember): UBS-Kontoauszüge, der UBS-Steuerausweis bzw. die Jahresenddokumente 2026.</li>
</ul>
<p>Die Steuererklärung selbst bleibt <strong>eine einzige</strong>: Deklariert wird das gesamte Jahreseinkommen und das Vermögen per 31. Dezember 2026 – unabhängig davon, bei welcher Einheit es angefallen ist. Prüfen Sie anhand der Belege beider Teilperioden, ob der UBS-Steuerausweis 2026 das ganze Jahr abdeckt oder ob Sie CS-Erträge der ersten Jahreswochen separat ergänzen müssen; im Zweifel fragen Sie bei Ihrem UBS-Kundenberater nach, bevor Sie die Erklärung einreichen.</p>"""),
 ("Wertschriftenverzeichnis und Steuerauszug: was sich geändert hat",
  """<p>Der jährliche Steuerauszug kommt jetzt im UBS-Format. Für die Deklaration gilt unverändert:</p>
<ul>
<li><strong>Kotierte Titel:</strong> ISIN und Valorennummer bleiben gleich – die Titel sind dieselben geblieben, nur die Depotstelle hat gewechselt. Im Wertschriftenverzeichnis deklarieren Sie sie wie bisher.</li>
<li><strong>Steuerwert per 31.12.2026:</strong> Massgebend ist der Kurs am letzten Börsentag im Dezember gemäss der <a href="https://www.estv.admin.ch/de/kurslisten-ictax" rel="noopener">Kursliste (ICTax) der ESTV</a>; diese Kurse gelten als Steuerwert am 31. Dezember (Art. 14 und 17 Abs. 1 StHG). Die Steuerprogramme der Kantone sind mit der Kursliste verknüpft – die Valorennummer genügt meist als Eingabe.</li>
<li><strong>Kein steuerbarer Vorgang:</strong> Die Migration war kein Verkauf. Selbst wenn Titel übertragen wurden: Kapitalgewinne aus der Veräusserung von beweglichem Privatvermögen sind bei der direkten Bundessteuer steuerfrei (Art. 16 Abs. 3 DBG), und Ihre <strong>Anschaffungskosten</strong> für eine allfällige spätere Veräusserung bleiben gültig – übernehmen Sie sie aus Ihren alten CS-Belegen.</li>
</ul>
<p>Haben Sie neben dem UBS-Depot noch Positionen bei Neobrokern oder ausländischen Banken? Dann gelten dieselben Deklarationsregeln – Details im Ratgeber <a href="auslaendisches-depot-neobroker-steuererklaerung.html">Ausländisches Depot &amp; Neobroker in der Steuererklärung</a>.</p>
<p><strong>Praxistipp:</strong> Vergleichen Sie Positionsliste und Steuerauszug Position für Position. Sollten einzelne Produkte im Zuge der Migration neue Nummern erhalten haben (betrifft vereinzelte Spezialprodukte), klären Sie die Zuordnung vor dem Einreichen.</p>"""),
 ("Beispiel: Ein 2026 migriertes Depot in der Steuererklärung",
  """<p><strong>Beispiel:</strong> Frau B. wurde mit ihrem Depot Mitte Mai 2026 zu UBS migriert (<em>alle Zahlen fiktiv und illustrierend</em>). Im Wertschriftenverzeichnis der Steuererklärung 2026 deklariert sie:</p>
<table><thead><tr><th>Position</th><th>Wert (CHF)</th><th>Quelle</th></tr></thead><tbody>
<tr><td>100 Aktien eines kotierten CH-Unternehmens, Anschaffungskosten 48'000</td><td>Steuerwert 52'300 per 31.12.2026</td><td>ESTV-Kursliste (ICTax)</td></tr>
<tr><td>Dividende April 2026 (CS-Teilperiode)</td><td>620 brutto</td><td>letzte CS-Ertragsabrechnung</td></tr>
<tr><td>Dividende September 2026 (UBS-Teilperiode)</td><td>1'240 brutto</td><td>UBS-Steuerausweis 2026</td></tr>
<tr><td>Kontoguthaben per 31.12.2026</td><td>21'400</td><td>UBS-Jahresendauszug</td></tr>
</tbody></table>
<p>In die Steuererklärung trägt sie den <strong>Steuerwert per 31.12.</strong> (52'300 + 21'400) im Wertschriftenverzeichnis ein und die <strong>gesamten Bruttoerträge des Jahres</strong> (620 + 1'240 = 1'860) beim Wertschriftenertrag – beide Teilperioden zusammen. Die auf den Erträgen abgezogene Verrechnungssteuer von 35 % holt sie sich mit der vollständigen Deklaration über die Veranlagung zurück. Der Umstand, dass die April-Dividende noch «von der CS» stammte, ändert steuerlich nichts: Die CS-Einheit war bereits seit 2024 Teil der UBS Switzerland AG.</p>"""),
 ("Alte CS-Dokumente: die Download-Frist ist abgelaufen",
  """<p>Das Übertragungs-FAQ von UBS hielt fest: Dokumente von Konten, die <strong>vor der Übertragung geschlossen und saldiert</strong> wurden, wurden nicht zu UBS mitübertragen. Sie standen im Credit Suisse Online &amp; Mobile Banking nur <strong>bis drei Monate nach der Übertragung</strong> zum Download bereit – ausdrücklich auch steuerrelevante Dokumente wie <strong>Bestätigungen von 3a-Einzahlungen</strong> und Zinsabschlüsse von Konten und Hypotheken. Das CS-e-Banking selbst blieb nach der Migration ebenfalls nur drei Monate lang zum Dokumentenabruf zugänglich.</p>
<p>Da die letzten Migrationen im März 2026 stattfanden, ist dieses Zeitfenster inzwischen <strong>für alle Kunden geschlossen</strong>. Konkret heisst das:</p>
<ol>
<li><strong>Inventur jetzt:</strong> Prüfen Sie, welche CS-Steuerbelege 2024–2026 Sie bereits gesichert haben (PDF oder Papier) – insbesondere 3a-Einzahlungsbestätigungen, Zinsabschlüsse und Erträgnisaufstellungen.</li>
<li><strong>Fehlendes bestellen:</strong> Was fehlt, fordern Sie direkt über Ihre UBS-Kundenberatung bzw. den UBS-Kundendienst an – UBS Switzerland AG ist Rechtsnachfolgerin der ehemaligen CS-Einheit.</li>
<li><strong>Aufbewahren:</strong> Private Steuerbelege behalten Sie am besten mindestens bis zur rechtskräftigen Veranlagung; bei Geschäftsvermögen gilt die zehnjährige Aufbewahrungspflicht.</li>
</ol>""" + CTA_MID["de"]),
 ("Neue IBAN: Zahlungen und Abzüge ab 2027 korrekt steuern",
  """<p>Mit der Migration haben Sie <strong>neue UBS-Kontonummern und neue IBAN</strong> erhalten – die alten CS-Nummern konnten technisch nicht übernommen werden. Laut UBS-FAQ gilt:</p>
<ul>
<li>Zahlungen, die auf Ihren alten CS-IBAN eingehen, werden <strong>mindestens 24 Monate</strong> auf Ihre neuen UBS-Konten weitergeleitet.</li>
<li>Bereits erfasste <strong>Daueraufträge und LSV-Lastschriften</strong> wurden automatisch auf die neuen UBS-Konten übertragen.</li>
<li>Für den Migrationsmonat erhielten Sie <strong>zwei separate Gebührenrechnungen</strong> – eine bis zur Übertragung, eine für den Rest des Monats. Heben Sie beide auf: Depot- und Vermögensverwaltungskosten durch Dritte sind beim beweglichen Privatvermögen abziehbar.</li>
</ul>
<p>Verlassen Sie sich trotzdem nicht auf die Weiterleitung: Informieren Sie Zahlungspartner (Arbeitgeber, Vermieter, Krankenkasse, Säule-3a-Stiftung, Spendenorganisationen) aktiv über Ihre neue IBAN. Steuerlich entscheidend: <strong>Zahlungsbeleg ist Abzugsbeleg</strong>. Säule-3a-Einzahlungen, Spenden und Unterhaltsbeiträge müssen nachweisbar von Ihrem Konto an den korrekten Empfänger geflossen sein – stellen Sie sicher, dass solche Zahlungen ab 2027 über die neue UBS-IBAN laufen und die Bestätigungen der Empfänger (z. B. der 3a-Stiftung) vorliegen.</p>"""),
 ("Verrechnungssteuer: 35 % zurückholen, Bankangaben aktuell halten",
  """<p>Auf Zinsen und Dividenden aus schweizerischen Quellen zieht die Bank weiterhin <strong>35 % Verrechnungssteuer</strong> ab – neu eben als UBS. Zurückholen Sie diese über die ordentliche Deklaration in der Steuererklärung: Wer die Erträge vollständig angibt, erhält die Verrechnungssteuer mit der Veranlagung zurück. Details im Ratgeber <a href="verrechnungssteuer-schweiz-35-prozent.html">Verrechnungssteuer: die 35 Prozent erklärt</a>.</p>
<p>Zwei Punkte sind nach der Migration besonders relevant:</p>
<ol>
<li><strong>Beide Teilperioden deklarieren:</strong> Fehlende CS-Wochen im Januar bis März 2026 führen sonst zu Differenzen zwischen Ihrer Erklärung und den Bankmeldungen.</li>
<li><strong>Bankangaben prüfen:</strong> Hinterlegen Sie für Auszahlungen (z. B. Verrechnungssteuer-Rückerstattungen) Ihre aktuelle UBS-Verbindung – alte CS-Kontodaten in Formularen oder bei Behörden gehören ersetzt. Beachten Sie auch die <a href="verrechnungssteuer-rueckerstattungsfrist-ablauf.html">Rückerstattungsfrist</a>: Wer die Verrechnungssteuer nicht rechtzeitig geltend macht, verliert den Anspruch.</li>
</ol>"""),
 ("Phishing im Namen der Migration: so erkennen Sie Betrug",
  """<p>Grossmigrationen sind Hochsaison für Betrüger. Das UBS-FAQ stellt klar: Zur Vorbereitung der Übertragung kontaktierte die Bank ihre Kunden <strong>ausschliesslich per Briefpost oder über das (ehemalige) Credit Suisse Online &amp; Mobile Banking</strong>. Weder UBS noch Steuerbehörden fordern Sie per E-Mail, SMS oder Telefon auf, persönliche Daten preiszugeben oder Geld auf ein anderes Konto zu überweisen.</p>
<p>Seit dem Abschluss der Migration ist zusätzlich Vorsicht geboten bei angeblichen «Migrations»- oder «Rückerstattungs»-Nachrichten, die Ihre «neuen UBS-Zugangsdaten» bestätigen wollen. Wie solche Maschen aussehen und woran Sie sie erkennen, zeigt unser Ratgeber <a href="phishing-steuerbescheid-agov-betrug.html">Phishing mit Steuerbescheid und AGOV</a>. Grundregel: Loggen Sie sich immer direkt über die offizielle Adresse ein und prüfen Sie, ob ein Schreiben Ihre persönliche Kundennummer enthält.</p>"""),
 ("Checkliste: Steuererklärung 2026 mit UBS-Depot",
  """<p>Die wichtigsten Schritte in der Übersicht – abhaken, bevor Sie die Steuererklärung 2026 im Frühjahr 2027 einreichen:</p>
<table><thead><tr><th>Punkt</th><th>Was tun</th><th>Beleg / Quelle</th></tr></thead><tbody>
<tr><td>UBS-Steuerausweis 2026</td><td>Im UBS-e-Banking herunterladen oder bestellen</td><td>UBS-Jahresenddokumente</td></tr>
<tr><td>CS-Teilperiode</td><td>Ausstände Januar bis Migrationsdatum ergänzen</td><td>letzte CS-Auszüge, Schlussabrechnungen</td></tr>
<tr><td>Wertschriftenverzeichnis</td><td>Positionen per 31.12.2026 mit Steuerwert eintragen</td><td>ESTV-Kursliste (ICTax), Steuerprogramm</td></tr>
<tr><td>Erträge</td><td>Dividenden und Zinsen beider Teilperioden addieren</td><td>Erträgnisaufstellungen CS + UBS</td></tr>
<tr><td>Verrechnungssteuer</td><td>Erträge vollständig deklarieren → 35 % zurück</td><td>Steuererklärung, Rückerstattungsantrag</td></tr>
<tr><td>Säule 3a</td><td>Einzahlungsbestätigung 2026 beilegen</td><td>3a-Stiftung / Bank</td></tr>
<tr><td>Depotkosten</td><td>Gebührenrechnungen sammeln (inkl. zweite Rechnung im Migrationsmonat)</td><td>UBS-Gebührenausweise</td></tr>
<tr><td>Neue IBAN</td><td>Zahlungspartner informieren, Daueraufträge prüfen</td><td>UBS-Brief mit neuen Kontodaten</td></tr>
<tr><td>Alte CS-Dokumente</td><td>Fehlendes bei UBS anfordern (Download-Frist abgelaufen)</td><td>UBS-Kundendienst</td></tr>
<tr><td>Frist</td><td>Kantonale Abgabefrist notieren, ggf. erstrecken</td><td>Gemeinde- bzw. kantonales Steueramt</td></tr>
</tbody></table>
<p>Allgemeine Tipps zur Erklärung selbst: <a href="steuer-checkliste-2026.html">Steuer-Checkliste 2026</a>; den mutmasslichen Steuerbetrag können Sie vorab mit unseren <a href="rechner.html">Steuerrechnern</a> schätzen.</p>"""),
 ("Kurz gesagt",
  """<ul>
<li>Seit dem <strong>18. März 2026</strong> sind alle ehemaligen CS-Kunden auf UBS-Systemen (rund 1,2 Mio. Kunden weltweit); die Integration soll Ende 2026 weitgehend abgeschlossen sein.</li>
<li>Die Steuererklärung 2026 (Einreichung Anfang 2027, Frist kantonal) ist die erste Erklärung mit UBS-Depot per Stichtag <strong>31.12.2026</strong>.</li>
<li>Migration ≠ Verkauf: Kein steuerbarer Vorgang, ISINs kotierter Titel bleiben gleich, Anschaffungskosten übernehmen; private Kapitalgewinne sind steuerfrei (Art. 16 Abs. 3 DBG).</li>
<li>Belege der CS-Teilperiode 2026 sammeln; das Download-Fenster für alte CS-Dokumente (3 Monate nach Übertragung) ist abgelaufen – Fehlendes direkt bei UBS anfordern.</li>
<li>Neue IBAN aktiv kommunizieren: Alte CS-IBAN werden mindestens 24 Monate weitergeleitet, aber Zahlungsbeleg = Abzugsbeleg (3a, Spenden, Alimente).</li>
<li>Vorsicht Phishing: UBS kontaktierte ausschliesslich per Brief oder e-Banking – niemals Daten auf Zuruf per Mail/SMS/Telefon preisgeben.</li>
<li>Dies ist allgemeine Information, keine individuelle Beratung – klären Sie Ihren Einzelfall mit einer Fachperson.</li>
</ul>"""),
]

# ---------------- English ----------------
en_title = "Your UBS Depot in the 2026 Tax Return"
en_meta = "Since March 2026 all former CS clients bank with UBS. How to declare your depot for 2026: tax statement, 31 Dec valuation, old CS documents, new IBAN."
en_sections = [
 ("What happened in 2026: every CS account is now a UBS account",
  """<p>On <strong>18 March 2026</strong> UBS confirmed by media release that, with the migration of the Swiss-booked clients, <strong>all former Credit Suisse clients globally have been transferred to UBS infrastructure</strong> – around <strong>1.2 million clients</strong> in total. The integration is expected to be substantially complete by the end of 2026.</p>
<p>In legal terms, Credit Suisse (Schweiz) AG ceased to exist on <strong>1 July 2024</strong>, when it merged into UBS Switzerland AG, which succeeded to all its rights and obligations. The technical migration of client relationships followed through 2025 and the first quarter of 2026, each over a weekend and announced by letter.</p>
<p>For your taxes this means: <strong>tax year 2026</strong> is the first year in which all former CS clients hold a UBS depot at year-end. Depending on your migration date, 2026 was split into a CS partial period and a UBS partial period – with concrete consequences for statements, income and declaration.</p>"""),
 ("Tax year 2026: one return, possibly two sets of statements",
  """<p>You file the 2026 tax return <strong>during 2027</strong> – wealth tax is assessed on the position at the end of the tax period (the post-numerando method, Art. 17 LHTA). Deadlines are cantonal; in Zurich, for instance, the return is due by <strong>31 March of the following year</strong>, with extensions available. If your depot was migrated during 2026, expect <strong>two sets of documents</strong>:</p>
<ul>
<li><strong>CS partial period</strong> (1 January until your migration weekend): final CS account statements, interest and dividend advices, any closing statements from the former CS unit.</li>
<li><strong>UBS partial period</strong> (from migration to 31 December): UBS account statements and the 2026 UBS tax statement / year-end documents.</li>
</ul>
<p>The return itself remains <strong>a single filing</strong>: you declare the full year's income and your wealth as of 31 December 2026, regardless of which entity generated it. Use the statements from both partial periods to check whether the UBS 2026 tax statement covers the whole year or whether you must add CS income from the first weeks of January separately; if in doubt, ask your UBS client adviser before filing.</p>"""),
 ("Securities schedule and tax statement: what changed",
  """<p>The annual tax statement now comes in UBS format. The declaration rules are unchanged:</p>
<ul>
<li><strong>Listed securities:</strong> ISIN and security number stay the same – the instruments are identical, only the custodian changed. Declare them in the securities schedule as before.</li>
<li><strong>Tax value as of 31.12.2026:</strong> the relevant figure is the closing rate of the last trading day in December per the <a href="https://www.estv.admin.ch/de/kurslisten-ictax" rel="noopener">Federal Tax Administration's rate lists (ICTax)</a>; these rates count as the tax value at 31 December (Art. 14 and 17 para. 1 LHTA). Cantonal tax software links to the rate list – entering the security number is usually enough.</li>
<li><strong>No taxable event:</strong> the migration was not a sale. Even where instruments were transferred: capital gains on movable private assets are exempt from federal income tax (Art. 16 para. 3 FITA), and your <strong>acquisition costs</strong> remain valid for any later disposal – carry them over from your old CS statements.</li>
</ul>
<p>Holding additional positions with neobrokers or foreign banks? The same declaration rules apply – see our guide <a href="auslaendisches-depot-neobroker-steuererklaerung.html">Foreign depot &amp; neobroker in the tax return</a>.</p>
<p><strong>Practical tip:</strong> reconcile the position list and the tax statement item by item. If individual products received new numbers during the migration (a few special products only), clarify the mapping before filing.</p>"""),
 ("Example: a depot migrated in 2026 in the tax return",
  """<p><strong>Example:</strong> Ms B.'s depot was migrated to UBS in mid-May 2026 (<em>all figures fictional and illustrative</em>). In the securities schedule of her 2026 return she declares:</p>
<table><thead><tr><th>Item</th><th>Value (CHF)</th><th>Source</th></tr></thead><tbody>
<tr><td>100 shares of a listed Swiss company, acquisition cost 48,000</td><td>tax value 52,300 as of 31.12.2026</td><td>FTA rate list (ICTax)</td></tr>
<tr><td>Dividend April 2026 (CS partial period)</td><td>620 gross</td><td>final CS income statement</td></tr>
<tr><td>Dividend September 2026 (UBS partial period)</td><td>1,240 gross</td><td>UBS 2026 tax statement</td></tr>
<tr><td>Cash balance as of 31.12.2026</td><td>21,400</td><td>UBS year-end statement</td></tr>
</tbody></table>
<p>She enters the <strong>tax values as of 31 December</strong> (52,300 + 21,400) in the securities schedule and the <strong>full year's gross income</strong> (620 + 1,240 = 1,860) as investment income – both partial periods combined. The 35 % withholding tax deducted from that income is reimbursed through the assessment once the income is fully declared. The fact that the April dividend came "from CS" changes nothing: the CS unit had been part of UBS Switzerland AG since 2024.</p>"""),
 ("Old CS documents: the download window has closed",
  """<p>The UBS transfer FAQ stated that documents of accounts <strong>closed and settled before the transfer</strong> were not migrated. They were available for download in Credit Suisse Online &amp; Mobile Banking <strong>only until three months after the transfer</strong> – explicitly including tax-relevant documents such as <strong>pillar 3a payment confirmations</strong> and interest statements on accounts and mortgages. CS e-banking itself also remained accessible for document retrieval for only three months after migration.</p>
<p>Since the last migrations took place in March 2026, that window is now <strong>closed for all clients</strong>. In practice:</p>
<ol>
<li><strong>Take stock now:</strong> check which CS tax documents 2024–2026 you have already secured (PDF or paper) – in particular 3a payment confirmations, interest statements and income statements.</li>
<li><strong>Order what is missing:</strong> request missing documents via your UBS client adviser or customer service – UBS Switzerland AG is the legal successor of the former CS unit.</li>
<li><strong>Keep them:</strong> retain personal tax documents at least until the assessment is final; business assets are subject to the ten-year retention duty.</li>
</ol>""" + CTA_MID["en"]),
 ("New IBAN: steering payments and deductions correctly from 2027",
  """<p>With the migration you received <strong>new UBS account numbers and IBANs</strong> – the old CS numbers could not be carried over for technical reasons. According to the UBS FAQ:</p>
<ul>
<li>payments arriving on your old CS IBAN are forwarded to your new UBS accounts for <strong>at least 24 months</strong>;</li>
<li>existing <strong>standing orders and LSV direct debits</strong> were transferred to the new UBS accounts automatically;</li>
<li>for the migration month you received <strong>two separate fee invoices</strong> – one up to the transfer, one for the rest of the month. Keep both: third-party asset management costs on movable private assets are deductible.</li>
</ul>
<p>Do not rely on the forwarding service alone: actively inform payment partners (employer, landlord, health insurer, pillar 3a foundation, charities) of your new IBAN. The tax-relevant rule: <strong>the payment record is the deduction record</strong>. Pillar 3a contributions, donations and maintenance payments must verifiably have flowed from your account to the correct recipient – make sure such payments run via the new UBS IBAN from 2027 and that you hold the recipients' confirmations (e.g. from the 3a foundation).</p>"""),
 ("Withholding tax: reclaim the 35 %, keep bank details current",
  """<p>Interest and dividends from Swiss sources remain subject to <strong>35 % withholding tax</strong> – now deducted by UBS. You reclaim it through ordinary declaration in your tax return: fully declared income means the withholding tax is reimbursed with the assessment. Details in our guide <a href="verrechnungssteuer-schweiz-35-prozent.html">Swiss withholding tax: the 35 percent</a>.</p>
<p>Two points matter especially after the migration:</p>
<ol>
<li><strong>Declare both partial periods:</strong> missing CS weeks from January to March 2026 otherwise create discrepancies between your return and bank reports.</li>
<li><strong>Check your bank details:</strong> provide your current UBS account for payouts (e.g. withholding-tax refunds) and replace old CS details in any forms or with authorities. Also mind the <a href="verrechnungssteuer-rueckerstattungsfrist-ablauf.html">refund deadline</a>: claims not filed in time are lost.</li>
</ol>"""),
 ("Phishing in the name of the migration: how to spot fraud",
  """<p>Large migrations are peak season for fraudsters. The UBS FAQ is explicit: to prepare the transfer, the bank contacted clients <strong>exclusively by letter or via (former) Credit Suisse Online &amp; Mobile Banking</strong>. Neither UBS nor the tax authorities will ever ask you by e-mail, SMS or phone to disclose personal data or transfer money to another account.</p>
<p>Now that the migration is complete, be extra wary of fake "migration" or "refund" messages asking you to "confirm your new UBS credentials". Our guide <a href="phishing-steuerbescheid-agov-betrug.html">Phishing with tax assessments and AGOV</a> shows how these schemes work. Golden rule: always log in directly via the official address and check whether a letter contains your personal client number.</p>"""),
 ("Checklist: your 2026 tax return with a UBS depot",
  """<p>The key steps at a glance – tick them off before filing your 2026 return in spring 2027:</p>
<table><thead><tr><th>Item</th><th>What to do</th><th>Document / source</th></tr></thead><tbody>
<tr><td>UBS 2026 tax statement</td><td>download or order via UBS e-banking</td><td>UBS year-end documents</td></tr>
<tr><td>CS partial period</td><td>add income from January to your migration date</td><td>final CS statements and closing advices</td></tr>
<tr><td>Securities schedule</td><td>enter positions as of 31.12.2026 with tax values</td><td>FTA rate list (ICTax), tax software</td></tr>
<tr><td>Income</td><td>add dividends and interest from both partial periods</td><td>CS + UBS income statements</td></tr>
<tr><td>Withholding tax</td><td>declare income in full → reclaim the 35 %</td><td>tax return, refund claim</td></tr>
<tr><td>Pillar 3a</td><td>attach the 2026 payment confirmation</td><td>3a foundation / bank</td></tr>
<tr><td>Depot costs</td><td>collect fee invoices (incl. the second one from the migration month)</td><td>UBS fee statements</td></tr>
<tr><td>New IBAN</td><td>inform payment partners, check standing orders</td><td>UBS letter with new account data</td></tr>
<tr><td>Old CS documents</td><td>order missing items from UBS (download window closed)</td><td>UBS customer service</td></tr>
<tr><td>Deadline</td><td>note your cantonal filing deadline, request an extension if needed</td><td>communal / cantonal tax office</td></tr>
</tbody></table>
<p>General filing tips: <a href="steuer-checkliste-2026.html">Tax checklist 2026</a>; estimate your likely tax bill with our <a href="rechner.html">calculators</a>.</p>"""),
 ("In short",
  """<ul>
<li>Since <strong>18 March 2026</strong> all former CS clients run on UBS systems (about 1.2 million clients globally); the integration should be substantially complete by end-2026.</li>
<li>The 2026 tax return (filed in early 2027, cantonal deadlines) is the first return with a UBS depot as of the <strong>31.12.2026</strong> valuation date.</li>
<li>Migration ≠ sale: no taxable event, listed ISINs unchanged, acquisition costs carry over; private capital gains are tax-free (Art. 16 para. 3 FITA).</li>
<li>Collect statements for the 2026 CS partial period; the 3-month download window for old CS documents has closed – order anything missing directly from UBS.</li>
<li>Communicate your new IBAN: old CS IBANs are forwarded for at least 24 months, but the payment record is the deduction record (3a, donations, maintenance).</li>
<li>Mind phishing: UBS contacted clients exclusively by letter or e-banking – never disclose data on request by mail/SMS/phone.</li>
<li>This is general information, not individual advice – have your specific case reviewed by a professional.</li>
</ul>"""),
]

# ---------------- French ----------------
fr_title = "Dépôt UBS : déclaration d'impôt 2026"
fr_meta = "Depuis mars 2026, tous les ex-clients CS sont chez UBS. Déclarer votre dépôt 2026 : relevé fiscal, valeur au 31.12, anciens documents CS, nouvel IBAN."
fr_sections = [
 ("Ce qui a changé en 2026 : tous les comptes CS sont devenus des comptes UBS",
  """<p>Le <strong>18 mars 2026</strong>, UBS a confirmé par communiqué : avec la migration des clients domiciliés en Suisse, <strong>tous les anciens clients Credit Suisse du monde entier ont été transférés sur l'infrastructure UBS</strong> – environ <strong>1,2 million de clients</strong> au total. L'intégration devrait être « largement » achevée d'ici fin 2026.</p>
<p>Sur le plan juridique, Credit Suisse (Schweiz) AG a disparu le <strong>1er juillet 2024</strong> par fusion dans UBS Switzerland AG, qui a repris tous ses droits et obligations. Les migrations techniques des relations clients ont suivi en 2025 et au premier trimestre 2026, chacune sur un week-end et annoncée par courrier.</p>
<p>Pour vos impôts, cela signifie : l'<strong>année fiscale 2026</strong> est la première où tous les ex-clients CS détiennent un dépôt UBS au 31 décembre. Selon votre date de migration, 2026 se divise en une période partielle CS et une période partielle UBS – avec des conséquences concrètes pour les justificatifs, les revenus et la déclaration.</p>"""),
 ("Année fiscale 2026 : une déclaration, éventuellement deux jeux de justificatifs",
  """<p>Vous déposerez la déclaration 2026 <strong>en 2027</strong> – l'impôt sur la fortune est établi d'après la situation à la fin de la période fiscale (méthode postnumerando, art. 17 LHID). Les délais varient selon les cantons ; à Zurich par exemple, la déclaration doit être remise <strong>au 31 mars de l'année suivante</strong>, avec possibilité de prolongation. Si votre dépôt a été migré courant 2026, attendez-vous à <strong>deux jeux de documents</strong> :</p>
<ul>
<li><strong>Période partielle CS</strong> (1er janvier jusqu'au week-end de migration) : derniers relevés CS, décomptes d'intérêts et de dividendes, éventuels décomptes finals de l'ex-entité CS.</li>
<li><strong>Période partielle UBS</strong> (de la migration au 31 décembre) : relevés UBS et attestation fiscale UBS / documents de fin d'année 2026.</li>
</ul>
<p>La déclaration reste <strong>unique</strong> : vous déclarez l'ensemble du revenu annuel et la fortune au 31 décembre 2026, quelle que soit l'entité qui les a générés. Vérifiez, pièces des deux périodes à l'appui, si l'attestation fiscale UBS 2026 couvre toute l'année ou si vous devez compléter les revenus CS des premières semaines ; en cas de doute, interrogez votre conseiller UBS avant de déposer.</p>"""),
 ("Inventaire des titres et attestation fiscale : ce qui a changé",
  """<p>L'attestation fiscale annuelle est désormais au format UBS. Les règles de déclaration restent inchangées :</p>
<ul>
<li><strong>Titres cotés :</strong> l'ISIN et le numéro de valeur restent identiques – les titres sont les mêmes, seul le dépositaire a changé. Déclarez-les comme avant dans l'inventaire des titres.</li>
<li><strong>Valeur fiscale au 31.12.2026 :</strong> le cours déterminant est celui du dernier jour de bourse de décembre selon les <a href="https://www.estv.admin.ch/de/kurslisten-ictax" rel="noopener">listes de cours (ICTax) de l'Office fédéral des contributions</a> ; ces cours valent comme valeur fiscale au 31 décembre (art. 14 et 17 al. 1 LHID). Les logiciels fiscaux cantonaux sont reliés aux listes de cours – le numéro de valeur suffit généralement.</li>
<li><strong>Aucun fait imposable :</strong> la migration n'était pas une vente. Même en cas de transfert de titres : les gains en capital sur la fortune privée mobilière sont exonérés de l'impôt fédéral direct (art. 16 al. 3 LIFD) et vos <strong>coûts d'acquisition</strong> restent valables pour une vente ultérieure – reprenez-les de vos anciens justificatifs CS.</li>
</ul>
<p>Vous détenez aussi des positions chez des néo-courtiers ou des banques étrangères ? Les mêmes règles s'appliquent – voir notre guide <a href="auslaendisches-depot-neobroker-steuererklaerung.html">Dépôt étranger &amp; néo-courtier dans la déclaration d'impôt</a>.</p>
<p><strong>Conseil pratique :</strong> comparez la liste des positions et l'attestation fiscale ligne par ligne. Si certains produits ont reçu de nouveaux numéros lors de la migration (quelques produits spéciaux uniquement), clarifiez la correspondance avant le dépôt.</p>"""),
 ("Exemple : un dépôt migré en 2026 dans la déclaration d'impôt",
  """<p><strong>Exemple :</strong> le dépôt de Mme B. a été migré chez UBS à la mi-mai 2026 (<em>chiffres fictifs et illustratifs</em>). Dans l'inventaire des titres de sa déclaration 2026, elle indique :</p>
<table><thead><tr><th>Position</th><th>Valeur (CHF)</th><th>Source</th></tr></thead><tbody>
<tr><td>100 actions d'une société suisse cotée, coût d'acquisition 48 000</td><td>valeur fiscale 52 300 au 31.12.2026</td><td>liste de cours AFC (ICTax)</td></tr>
<tr><td>Dividende avril 2026 (période partielle CS)</td><td>620 brut</td><td>dernier décompte de revenus CS</td></tr>
<tr><td>Dividende septembre 2026 (période partielle UBS)</td><td>1 240 brut</td><td>attestation fiscale UBS 2026</td></tr>
<tr><td>Avoir en compte au 31.12.2026</td><td>21 400</td><td>relevé de fin d'année UBS</td></tr>
</tbody></table>
<p>Elle reporte la <strong>valeur fiscale au 31.12</strong> (52 300 + 21 400) dans l'inventaire des titres et les <strong>revenus bruts de toute l'année</strong> (620 + 1 240 = 1 860) sous « rendement de la fortune » – les deux périodes partielles additionnées. L'impôt anticipé de 35 % déduit de ces revenus lui est remboursé via la taxation, à condition d'une déclaration complète. Que le dividende d'avril provienne « du CS » ne change rien fiscalement : l'entité CS faisait partie d'UBS Switzerland AG depuis 2024.</p>"""),
 ("Anciens documents CS : le délai de téléchargement est échu",
  """<p>La FAQ de transfert d'UBS précisait : les documents des comptes <strong>fermés et soldés avant le transfert</strong> n'étaient pas repris chez UBS. Ils restaient téléchargeables dans Credit Suisse Online &amp; Mobile Banking <strong>jusqu'à trois mois après le transfert</strong> – y compris expressément les documents fiscaux tels que les <strong>confirmations de versements 3a</strong> et les décomptes d'intérêts de comptes et d'hypothèques. Le CS e-banking lui-même n'est resté accessible que trois mois après la migration, uniquement pour consulter des documents.</p>
<p>Les dernières migrations ayant eu lieu en mars 2026, cette fenêtre est désormais <strong>fermée pour tous les clients</strong>. Concrètement :</p>
<ol>
<li><strong>Faites l'inventaire maintenant :</strong> vérifiez quels justificatifs fiscaux CS 2024–2026 vous avez déjà sécurisés (PDF ou papier) – notamment confirmations 3a, décomptes d'intérêts et relevés de revenus.</li>
<li><strong>Commandez ce qui manque :</strong> demandez les documents manquants directement via votre conseiller UBS ou le service client – UBS Switzerland AG est la successeure juridique de l'ex-entité CS.</li>
<li><strong>Conservez :</strong> gardez les justificatifs privés au moins jusqu'à l'entrée en force de la taxation ; pour la fortune commerciale, l'obligation de conservation est de dix ans.</li>
</ol>""" + CTA_MID["fr"]),
 ("Nouvel IBAN : piloter paiements et déductions dès 2027",
  """<p>Avec la migration, vous avez reçu de <strong>nouveaux numéros de compte et IBAN UBS</strong> – les anciens numéros CS ne pouvaient pas être repris pour des raisons techniques. Selon la FAQ d'UBS :</p>
<ul>
<li>les paiements arrivant sur vos anciens IBAN CS sont transférés vers vos nouveaux comptes UBS pendant <strong>au moins 24 mois</strong> ;</li>
<li>les <strong>ordres permanents et débits LSV</strong> existants ont été transférés automatiquement vers les nouveaux comptes UBS ;</li>
<li>pour le mois de la migration, vous avez reçu <strong>deux factures de frais séparées</strong> – l'une jusqu'au transfert, l'autre pour le reste du mois. Conservez-les : les frais de gestion de fortune par des tiers sur la fortune privée mobilière sont déductibles.</li>
</ul>
<p>Ne vous reposez pas pour autant sur le mécanisme de transfert : informez activement vos partenaires de paiement (employeur, bailleur, caisse maladie, fondation de libre passage 3a, organisations caritatives) de votre nouvel IBAN. Règle fiscalement décisive : <strong>la preuve de paiement vaut preuve de déduction</strong>. Versements 3a, dons et contributions d'entretien doivent avoir transité de manière vérifiable de votre compte vers le bon destinataire – faites-les passer par le nouvel IBAN UBS dès 2027 et conservez les confirmations des destinataires (p. ex. de la fondation 3a).</p>"""),
 ("Impôt anticipé : récupérer les 35 %, tenir les coordonnées bancaires à jour",
  """<p>Les intérêts et dividendes de source suisse restent frappés de <strong>35 % d'impôt anticipé</strong> – désormais prélevés par UBS. Vous le récupérez via la déclaration ordinaire dans votre déclaration d'impôt : qui déclare intégralement les revenus obtient le remboursement avec la taxation. Détails dans notre guide <a href="verrechnungssteuer-schweiz-35-prozent.html">L'impôt anticipé suisse : les 35 pour cent</a>.</p>
<p>Deux points sont particulièrement importants après la migration :</p>
<ol>
<li><strong>Déclarer les deux périodes partielles :</strong> sinon les semaines CS manquantes de janvier à mars 2026 créent des écarts entre votre déclaration et les annonces bancaires.</li>
<li><strong>Vérifier vos coordonnées bancaires :</strong> indiquez votre relation UBS actuelle pour les versements (p. ex. remboursements d'impôt anticipé) et remplacez les anciennes coordonnées CS dans les formulaires et auprès des autorités. Respectez aussi le <a href="verrechnungssteuer-rueckerstattungsfrist-ablauf.html">délai de remboursement</a> : une demande tardive fait perdre le droit.</li>
</ol>"""),
 ("Hameçonnage au nom de la migration : reconnaître les arnaques",
  """<p>Les grandes migrations sont la haute saison des escrocs. La FAQ d'UBS est claire : pour préparer le transfert, la banque a contacté ses clients <strong>exclusivement par courrier ou via le Credit Suisse Online &amp; Mobile Banking (alors existant)</strong>. Ni UBS ni les autorités fiscales ne vous demanderont jamais par e-mail, SMS ou téléphone de divulguer des données personnelles ou de virer de l'argent sur un autre compte.</p>
<p>Depuis la fin de la migration, redoublez de vigilance face aux faux messages de « migration » ou de « remboursement » qui veulent vous faire « confirmer vos nouveaux accès UBS ». Notre guide <a href="phishing-steuerbescheid-agov-betrug.html">Hameçonnage avec décisions fiscales et AGOV</a> montre ces procédés. Règle d'or : connectez-vous toujours directement via l'adresse officielle et vérifiez qu'un courrier contient votre numéro de client personnel.</p>"""),
 ("Liste de contrôle : déclaration d'impôt 2026 avec dépôt UBS",
  """<p>Les étapes essentielles en un coup d'œil – à cocher avant de déposer votre déclaration 2026 au printemps 2027 :</p>
<table><thead><tr><th>Point</th><th>À faire</th><th>Justificatif / source</th></tr></thead><tbody>
<tr><td>Attestation fiscale UBS 2026</td><td>la télécharger ou la commander dans l'e-banking UBS</td><td>documents de fin d'année UBS</td></tr>
<tr><td>Période partielle CS</td><td>compléter les revenus de janvier à la date de migration</td><td>derniers relevés et décomptes finaux CS</td></tr>
<tr><td>Inventaire des titres</td><td>saisir les positions au 31.12.2026 avec leur valeur fiscale</td><td>liste de cours AFC (ICTax), logiciel fiscal</td></tr>
<tr><td>Revenus</td><td>additionner dividendes et intérêts des deux périodes partielles</td><td>relevés de revenus CS + UBS</td></tr>
<tr><td>Impôt anticipé</td><td>déclarer intégralement → récupérer les 35 %</td><td>déclaration, demande de remboursement</td></tr>
<tr><td>Pilier 3a</td><td>joindre la confirmation de versement 2026</td><td>fondation 3a / banque</td></tr>
<tr><td>Frais de dépôt</td><td>réunir les factures de frais (y c. la seconde du mois de migration)</td><td>décomptes de frais UBS</td></tr>
<tr><td>Nouvel IBAN</td><td>informer les partenaires de paiement, vérifier les ordres permanents</td><td>courrier UBS avec les nouvelles coordonnées</td></tr>
<tr><td>Anciens documents CS</td><td>commander les manquants auprès d'UBS (délai de téléchargement échu)</td><td>service client UBS</td></tr>
<tr><td>Délai</td><td>noter le délai cantonal, demander une prolongation si besoin</td><td>office des impôts communal / cantonal</td></tr>
</tbody></table>
<p>Conseils généraux de déclaration : <a href="steuer-checkliste-2026.html">Liste de contrôle fiscale 2026</a> ; estimez votre charge probable avec nos <a href="rechner.html">calculateurs</a>.</p>"""),
 ("En bref",
  """<ul>
<li>Depuis le <strong>18 mars 2026</strong>, tous les ex-clients CS sont sur les systèmes UBS (env. 1,2 million de clients dans le monde) ; l'intégration devrait être largement achevée fin 2026.</li>
<li>La déclaration 2026 (déposée début 2027, délais cantonaux) est la première avec un dépôt UBS au jour de référence <strong>31.12.2026</strong>.</li>
<li>Migration ≠ vente : aucun fait imposable, ISIN des titres cotés inchangés, coûts d'acquisition repris ; les gains en capital privés sont exonérés (art. 16 al. 3 LIFD).</li>
<li>Réunissez les justificatifs de la période partielle CS 2026 ; la fenêtre de téléchargement de 3 mois pour les anciens documents CS est fermée – commandez les manquants directement auprès d'UBS.</li>
<li>Communiquez votre nouvel IBAN : les anciens IBAN CS sont transférés au moins 24 mois, mais la preuve de paiement vaut preuve de déduction (3a, dons, contributions d'entretien).</li>
<li>Attention à l'hameçonnage : UBS n'a contacté ses clients que par courrier ou e-banking – ne divulguez jamais de données sur demande par e-mail/SMS/téléphone.</li>
<li>Information générale, pas un conseil individuel – faites examiner votre cas par une personne qualifiée.</li>
</ul>"""),
]

# ---------------- Italian ----------------
it_title = "Deposito UBS e dichiarazione 2026"
it_meta = "Da marzo 2026 tutti gli ex clienti CS sono in UBS. Come dichiarare il deposito 2026: certificato fiscale, valore al 31.12, vecchi documenti CS, nuovo IBAN."
it_sections = [
 ("Cosa è cambiato nel 2026: tutti i conti CS sono ora conti UBS",
  """<p>Il <strong>18 marzo 2026</strong> UBS ha confermato con un comunicato stampa: con la migrazione dei clienti con conti in Svizzera, <strong>tutti gli ex clienti Credit Suisse a livello mondiale sono stati trasferiti sull'infrastruttura UBS</strong> – circa <strong>1,2 milioni di clienti</strong>. L'integrazione dovrebbe essere «largamente» completata entro fine 2026.</p>
<p>Giuridicamente, Credit Suisse (Schweiz) AG è scomparsa il <strong>1° luglio 2024</strong>, fusa in UBS Switzerland AG che ne ha assunto tutti i diritti e gli obblighi. Le migrazioni tecniche delle relazioni clienti sono seguite nel 2025 e nel primo trimestre 2026, ciascuna in un fine settimana e annunciata per lettera.</p>
<p>Per le vostre imposte ciò significa: il <strong>periodo fiscale 2026</strong> è il primo in cui tutti gli ex clienti CS detengono a fine anno un deposito UBS. A seconda della data di migrazione, il 2026 si divide in un periodo parziale CS e uno UBS – con conseguenze concrete per giustificativi, redditi e dichiarazione.</p>"""),
 ("Periodo fiscale 2026: una dichiarazione, eventualmente due set di giustificativi",
  """<p>La dichiarazione 2026 si compila e si consegna <strong>nel 2027</strong> – l'imposta sulla sostanza è calcolata secondo la situazione a fine periodo fiscale (metodo postnumerando, art. 17 LAID). I termini variano da cantone a cantone; a Zurigo, ad esempio, la dichiarazione va consegnata <strong>entro il 31 marzo dell'anno seguente</strong>, con possibilità di proroga. Se il vostro deposito è stato migrato nel corso del 2026, mettete in conto <strong>due set di documenti</strong>:</p>
<ul>
<li><strong>Periodo parziale CS</strong> (1° gennaio fino al fine settimana di migrazione): ultimi estratti conto CS, conteggi di interessi e dividendi, eventuali conteggi finali dell'ex entità CS.</li>
<li><strong>Periodo parziale UBS</strong> (dalla migrazione al 31 dicembre): estratti conto UBS e certificato fiscale UBS / documenti di fine anno 2026.</li>
</ul>
<p>La dichiarazione resta <strong>unica</strong>: si dichiara l'intero reddito dell'anno e la sostanza al 31 dicembre 2026, indipendentemente dall'entità che li ha generati. Verificate, con i documenti di entrambi i periodi, se il certificato fiscale UBS 2026 copre tutto l'anno o se dovete integrare i redditi CS delle prime settimane; nel dubbio, chiedete al vostro consulente UBS prima di consegnare.</p>"""),
 ("Elenco dei titoli e certificato fiscale: cosa è cambiato",
  """<p>Il certificato fiscale annuale è ora in formato UBS. Le regole di dichiarazione restano invariate:</p>
<ul>
<li><strong>Titoli quotati:</strong> ISIN e numero di valore restano identici – i titoli sono gli stessi, è cambiato solo il depositario. Dichiarateli come prima nell'elenco dei titoli.</li>
<li><strong>Valore fiscale al 31.12.2026:</strong> determinante è il corso dell'ultimo giorno di borsa di dicembre secondo gli <a href="https://www.estv.admin.ch/de/kurslisten-ictax" rel="noopener">elenchi dei corsi (ICTax) dell'Amministrazione federale delle contribuzioni</a>; questi corsi valgono come valore fiscale al 31 dicembre (art. 14 e 17 cpv. 1 LAID). I software fiscali cantonali sono collegati agli elenchi dei corsi – di norma basta il numero di valore.</li>
<li><strong>Nessun fatto imponibile:</strong> la migrazione non è stata una vendita. Anche in caso di trasferimento di titoli: i guadagni di capitale sulla sostanza privata mobiliare sono esenti dall'imposta federale diretta (art. 16 cpv. 3 LIFD) e i vostri <strong>costi d'acquisto</strong> restano validi per un'eventuale vendita futura – riprendeteli dai vecchi documenti CS.</li>
</ul>
<p>Avete anche posizioni presso neobroker o banche estere? Valgono le stesse regole – vedi la nostra guida <a href="auslaendisches-depot-neobroker-steuererklaerung.html">Deposito estero e neobroker nella dichiarazione d'imposte</a>.</p>
<p><strong>Consiglio pratico:</strong> confrontate riga per riga l'elenco delle posizioni e il certificato fiscale. Se singoli prodotti hanno ricevuto nuovi numeri con la migrazione (riguarda pochi prodotti speciali), chiarite la corrispondenza prima della consegna.</p>"""),
 ("Esempio: un deposito migrato nel 2026 nella dichiarazione d'imposte",
  """<p><strong>Esempio:</strong> il deposito della signora B. è stato migrato in UBS a metà maggio 2026 (<em>cifre fittizie e illustrative</em>). Nell'elenco dei titoli della sua dichiarazione 2026 indica:</p>
<table><thead><tr><th>Posizione</th><th>Valore (CHF)</th><th>Fonte</th></tr></thead><tbody>
<tr><td>100 azioni di una società svizzera quotata, costi d'acquisto 48'000</td><td>valore fiscale 52'300 al 31.12.2026</td><td>elenco dei corsi AFC (ICTax)</td></tr>
<tr><td>Dividendo aprile 2026 (periodo parziale CS)</td><td>620 lordo</td><td>ultimo conteggio dei redditi CS</td></tr>
<tr><td>Dividendo settembre 2026 (periodo parziale UBS)</td><td>1'240 lordo</td><td>certificato fiscale UBS 2026</td></tr>
<tr><td>Avere in conto al 31.12.2026</td><td>21'400</td><td>estratto di fine anno UBS</td></tr>
</tbody></table>
<p>Riporta il <strong>valore fiscale al 31.12</strong> (52'300 + 21'400) nell'elenco dei titoli e i <strong>redditi lordi dell'intero anno</strong> (620 + 1'240 = 1'860) come rendimento della sostanza – sommando i due periodi parziali. L'imposta preventiva del 35 % dedotta da questi redditi le viene rimborsata con la tassazione, a condizione di una dichiarazione completa. Che il dividendo di aprile provenisse «dal CS» non cambia nulla fiscalmente: l'entità CS faceva parte di UBS Switzerland AG già dal 2024.</p>"""),
 ("Vecchi documenti CS: il termine di download è scaduto",
  """<p>La FAQ sul trasferimento di UBS precisava: i documenti dei conti <strong>chiusi e saldati prima del trasferimento</strong> non venivano ripresi in UBS. Restavano scaricabili nel Credit Suisse Online &amp; Mobile Banking <strong>solo fino a tre mesi dopo il trasferimento</strong> – inclusi espressamente i documenti fiscalmente rilevanti come le <strong>conferme dei versamenti 3a</strong> e i conteggi degli interessi di conti e ipoteche. Anche l'e-banking CS restava accessibile, solo per il reperimento di documenti, per tre mesi dalla migrazione.</p>
<p>Poiché le ultime migrazioni sono avvenute a marzo 2026, questa finestra è ormai <strong>chiusa per tutti i clienti</strong>. In pratica:</p>
<ol>
<li><strong>Fate l'inventario ora:</strong> verificate quali giustificativi fiscali CS 2024–2026 avete già messo al sicuro (PDF o carta) – in particolare conferme 3a, conteggi degli interessi ed elenchi dei redditi.</li>
<li><strong>Ordinate ciò che manca:</strong> richiedete i documenti mancanti direttamente tramite il vostro consulente UBS o il servizio clienti – UBS Switzerland AG è la successora giuridica dell'ex entità CS.</li>
<li><strong>Conservate:</strong> tenete i giustificativi privati almeno fino al passaggio in giudicato della tassazione; per la sostanza commerciale vige l'obbligo di conservazione decennale.</li>
</ol>""" + CTA_MID["it"]),
 ("Nuovo IBAN: gestire correttamente pagamenti e deduzioni dal 2027",
  """<p>Con la migrazione avete ricevuto <strong>nuovi numeri di conto e IBAN UBS</strong> – i vecchi numeri CS non potevano essere ripresi per motivi tecnici. Secondo la FAQ di UBS:</p>
<ul>
<li>i pagamenti in arrivo sui vostri vecchi IBAN CS vengono inoltrati ai nuovi conti UBS per <strong>almeno 24 mesi</strong>;</li>
<li>gli <strong>ordini permanenti e gli addebitamenti LSV</strong> esistenti sono stati trasferiti automaticamente ai nuovi conti UBS;</li>
<li>per il mese della migrazione avete ricevuto <strong>due conteggi delle spese separati</strong> – uno fino al trasferimento, uno per il resto del mese. Conservateli entrambi: i costi di gestione della fortuna patrimoniale privata mobiliare da parte di terzi sono deducibili.</li>
</ul>
<p>Non fate però affidamento solo sull'inoltro automatico: informate attivamente i vostri partner di pagamento (datore di lavoro, locatore, cassa malati, fondazione di previdenza 3a, organizzazioni di utilità pubblica) del nuovo IBAN. Regola fiscalmente decisiva: <strong>la prova di pagamento è la prova della deduzione</strong>. Versamenti 3a, donazioni e contributi di mantenimento devono essere transitati in modo verificabile dal vostro conto al corretto destinatario – effettuate tali pagamenti dal 2027 con il nuovo IBAN UBS e conservate le conferme dei destinatari (p. es. della fondazione 3a).</p>"""),
 ("Imposta preventiva: recuperare il 35 %, tenere aggiornati i dati bancari",
  """<p>Interessi e dividendi di fonte svizzera restano gravati dall'<strong>imposta preventiva del 35 %</strong> – ora trattenuta da UBS. La recuperate con la dichiarazione ordinaria nella dichiarazione d'imposte: chi dichiara integralmente i redditi ottiene il rimborso con la tassazione. Dettagli nella nostra guida <a href="verrechnungssteuer-schweiz-35-prozent.html">Imposta preventiva svizzera: il 35 per cento</a>.</p>
<p>Dopo la migrazione due punti sono particolarmente importanti:</p>
<ol>
<li><strong>Dichiarare entrambi i periodi parziali:</strong> altrimenti le settimane CS mancanti da gennaio a marzo 2026 creano discrepanze tra la vostra dichiarazione e le comunicazioni bancarie.</li>
<li><strong>Verificare i dati bancari:</strong> indicate la vostra relazione UBS attuale per i versamenti (p. es. rimborsi dell'imposta preventiva) e sostituite i vecchi dati CS nei moduli e presso le autorità. Rispettate anche il <a href="verrechnungssteuer-rueckerstattungsfrist-ablauf.html">termine di rimborso</a>: una richiesta tardiva fa perdere il diritto.</li>
</ol>"""),
 ("Phishing in nome della migrazione: come riconoscere le truffe",
  """<p>Le grandi migrazioni sono l'alta stagione dei truffatori. La FAQ di UBS è chiara: per preparare il trasferimento, la banca ha contattato i clienti <strong>esclusivamente per lettera o tramite il Credit Suisse Online &amp; Mobile Banking (allora esistente)</strong>. Né UBS né le autorità fiscali vi chiederanno mai per e-mail, SMS o telefono di rivelare dati personali o di trasferire denaro su un altro conto.</p>
<p>Ora che la migrazione è conclusa, massima prudenza verso finti messaggi di «migrazione» o di «rimborso» che vogliono farvi «confermare i nuovi accessi UBS». La nostra guida <a href="phishing-steuerbescheid-agov-betrug.html">Phishing con decisioni fiscali e AGOV</a> illustra questi metodi. Regola d'oro: accedete sempre direttamente tramite l'indirizzo ufficiale e verificate che una lettera contenga il vostro numero di cliente personale.</p>"""),
 ("Lista di controllo: dichiarazione d'imposte 2026 con deposito UBS",
  """<p>Le tappe principali in sintesi – da spuntare prima di consegnare la dichiarazione 2026 nella primavera 2027:</p>
<table><thead><tr><th>Punto</th><th>Cosa fare</th><th>Giustificativo / fonte</th></tr></thead><tbody>
<tr><td>Certificato fiscale UBS 2026</td><td>scaricarlo o ordinarlo nell'e-banking UBS</td><td>documenti di fine anno UBS</td></tr>
<tr><td>Periodo parziale CS</td><td>integrare i redditi da gennaio alla data di migrazione</td><td>ultimi estratti e conteggi finali CS</td></tr>
<tr><td>Elenco dei titoli</td><td>inserire le posizioni al 31.12.2026 con il valore fiscale</td><td>elenco dei corsi AFC (ICTax), software fiscale</td></tr>
<tr><td>Redditi</td><td>sommare dividendi e interessi di entrambi i periodi parziali</td><td>conteggi dei redditi CS + UBS</td></tr>
<tr><td>Imposta preventiva</td><td>dichiarare integralmente → recuperare il 35 %</td><td>dichiarazione, domanda di rimborso</td></tr>
<tr><td>Pilastro 3a</td><td>allegare la conferma di versamento 2026</td><td>fondazione 3a / banca</td></tr>
<tr><td>Costi di deposito</td><td>raccogliere i conteggi delle spese (incl. il secondo del mese di migrazione)</td><td>conteggi delle spese UBS</td></tr>
<tr><td>Nuovo IBAN</td><td>informare i partner di pagamento, verificare gli ordini permanenti</td><td>lettera UBS con i nuovi dati di conto</td></tr>
<tr><td>Vecchi documenti CS</td><td>ordinare i mancanti presso UBS (termine di download scaduto)</td><td>servizio clienti UBS</td></tr>
<tr><td>Termine</td><td>annotare il termine cantonale, chiedere una proroga se necessario</td><td>ufficio imposte comunale / cantonale</td></tr>
</tbody></table>
<p>Consigli generali per la dichiarazione: <a href="steuer-checkliste-2026.html">Lista di controllo fiscale 2026</a>; stimate l'onere probabile con i nostri <a href="rechner.html">calcolatori</a>.</p>"""),
 ("In breve",
  """<ul>
<li>Dal <strong>18 marzo 2026</strong> tutti gli ex clienti CS operano sui sistemi UBS (circa 1,2 milioni di clienti a livello mondiale); l'integrazione dovrebbe essere largamente completata entro fine 2026.</li>
<li>La dichiarazione 2026 (consegnata a inizio 2027, termini cantonali) è la prima con deposito UBS alla data di riferimento <strong>31.12.2026</strong>.</li>
<li>Migrazione ≠ vendita: nessun fatto imponibile, ISIN dei titoli quotati invariati, costi d'acquisto ripresi; i guadagni di capitale privati sono esenti (art. 16 cpv. 3 LIFD).</li>
<li>Raccogliete i giustificativi del periodo parziale CS 2026; la finestra di download di 3 mesi per i vecchi documenti CS è chiusa – ordinate i mancanti direttamente presso UBS.</li>
<li>Comunicate il nuovo IBAN: i vecchi IBAN CS vengono inoltrati per almeno 24 mesi, ma la prova di pagamento è la prova della deduzione (3a, donazioni, contributi di mantenimento).</li>
<li>Attenzione al phishing: UBS ha contattato i clienti esclusivamente per lettera o e-banking – non rivelate mai dati su richiesta via e-mail/SMS/telefono.</li>
<li>Informazione generale, non consulenza individuale – fate esaminare il vostro caso da una persona qualificata.</li>
</ul>"""),
]

SRC_LABELS = {
    "de": [
        (SRC_MR, "UBS-Medienmitteilung vom 18.03.2026: «UBS successfully completes the client migration in Switzerland»"),
        (SRC_FAQ, "UBS-FAQ «Ihre Reise zu UBS» – Übertragung der Bankbeziehung (IBAN-Weiterleitung, Dokumente, Betrugsschutz)"),
        (SRC_ICTAX, "ESTV: Kurslisten (ICTax) – Steuerwerte per 31. Dezember (Art. 14 und 17 Abs. 1 StHG)"),
        (SRC_VST, "ESTV, Dossier Steuerinformationen: Vermögenssteuer natürlicher Personen (Stichtag 31.12., Postnumerando-Verfahren)"),
        (SRC_EST, "ESTV, Dossier Steuerinformationen: Einkommenssteuer natürlicher Personen (Kapitalgewinne bewegliches Privatvermögen steuerfrei, Art. 16 Abs. 3 DBG)"),
        (SRC_ZH, "Kanton Zürich: Steuererklärung Privatpersonen – Frist 31. März des Folgejahrs, Fristerstreckung"),
        (SRC_STHG, "Bundesgesetz über die Harmonisierung der direkten Steuern der Kantone und Gemeinden (StHG), SR 642.14 – fedlex"),
    ],
    "en": [
        (SRC_MR, "UBS media release of 18 March 2026: \"UBS successfully completes the client migration in Switzerland\""),
        (SRC_FAQ, "UBS FAQ \"Your journey to UBS\" – transfer of the banking relationship (IBAN forwarding, documents, fraud protection)"),
        (SRC_ICTAX, "FTA: Rate lists (ICTax) – tax values as of 31 December (Art. 14 and 17 para. 1 LHTA)"),
        (SRC_VST, "FTA, Tax Information dossier: Wealth taxation of individuals (valuation date 31.12., post-numerando method)"),
        (SRC_EST, "FTA, Tax Information dossier: Income taxation of individuals (capital gains on movable private assets exempt, Art. 16 para. 3 FITA)"),
        (SRC_ZH, "Canton of Zurich: tax return for individuals – deadline 31 March of the following year, extensions"),
        (SRC_STHG, "Federal Act on the Harmonisation of Direct Taxation at Cantonal and Communal Levels (LHTA), SR 642.14 – fedlex"),
    ],
    "fr": [
        (SRC_MR, "Communiqué UBS du 18.03.2026 : « UBS successfully completes the client migration in Switzerland »"),
        (SRC_FAQ, "FAQ UBS « Votre passage chez UBS » – transfert de la relation bancaire (transfert d'IBAN, documents, protection contre la fraude)"),
        (SRC_ICTAX, "AFC : Listes de cours (ICTax) – valeurs fiscales au 31 décembre (art. 14 et 17 al. 1 LHID)"),
        (SRC_VST, "AFC, Dossier Informations fiscales : Impôt sur la fortune des personnes physiques (jour de référence 31.12., méthode postnumerando)"),
        (SRC_EST, "AFC, Dossier Informations fiscales : Impôt sur le revenu des personnes physiques (gains en capital sur la fortune mobilière privée exonérés, art. 16 al. 3 LIFD)"),
        (SRC_ZH, "Canton de Zurich : déclaration d'impôt des personnes physiques – délai au 31 mars de l'année suivante, prolongation"),
        (SRC_STHG, "Loi fédérale sur l'harmonisation des impôts directs des cantons et des communes (LHID), RS 642.14 – fedlex"),
    ],
    "it": [
        (SRC_MR, "Comunicato stampa UBS del 18.03.2026: «UBS successfully completes the client migration in Switzerland»"),
        (SRC_FAQ, "FAQ UBS «Il vostro passaggio a UBS» – trasferimento della relazione bancaria (inoltro IBAN, documenti, protezione dalle frodi)"),
        (SRC_ICTAX, "AFC: Elenchi dei corsi (ICTax) – valori fiscali al 31 dicembre (art. 14 e 17 cpv. 1 LAID)"),
        (SRC_VST, "AFC, Dossier Informazioni fiscali: Imposta sulla sostanza delle persone fisiche (data di riferimento 31.12., metodo postnumerando)"),
        (SRC_EST, "AFC, Dossier Informazioni fiscali: Imposta sul reddito delle persone fisiche (guadagni di capitale su sostanza privata mobiliare esenti, art. 16 cpv. 3 LIFD)"),
        (SRC_ZH, "Canton Zurigo: dichiarazione d'imposte delle persone fisiche – termine 31 marzo dell'anno seguente, proroga"),
        (SRC_STHG, "Legge federale sull'armonizzazione delle imposte dirette dei Cantoni e dei Comuni (LAID), RS 642.14 – fedlex"),
    ],
}

def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

for lang, title, meta, sections in [("de", de_title, de_meta, de_sections),
                                    ("en", en_title, en_meta, en_sections),
                                    ("fr", fr_title, fr_meta, fr_sections),
                                    ("it", it_title, it_meta, it_sections)]:
    assert len(title) <= 40, f"{lang} title too long: {len(title)}"
    assert len(meta) <= 158, f"{lang} meta too long: {len(meta)}"
    if lang == "de":
        words = sum(len(strip_tags(b).split()) for _, b in sections)
        assert 1200 <= words <= 1800, f"DE word count {words} outside 1200-1800"
        assert 8 <= len(sections) <= 10, "need 8-10 h2 sections"
    build(lang, SLUG, title, meta, sections, related=RELATED,
          sources=SRC_LABELS[lang])
if True:
    words = sum(len(strip_tags(b).split()) for _, b in de_sections)
    print("DE word count:", words, "| sections:", len(de_sections))
print("done")
