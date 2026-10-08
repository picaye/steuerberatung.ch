#!/usr/bin/env python3
"""Four articles from the 2026-10-08 research batch. Compact but complete.
Facts verified 2026-10-08 against: admin.ch, bsv.admin.ch/ahv-iv.ch Merkblatt 5.03,
BGE 134 II 244 + 139 II 425 (Teilliquidation), ESTV Wertschriften-Praxis, Art. 33 DBG."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

def pub(slug, related, langs):
    for lang, title, meta, sections in langs:
        build(lang, slug, title, meta, sections, related=related)

# ============ 1. erwerbsbedingter-umzug-kosten-abzug ============
pub("erwerbsbedingter-umzug-kosten-abzug",
    ["steuer-checkliste-2026.html", "steuern-sparen-tipps.html", "grenzgaenger-de-fr-it-steuern.html"],
[
("de", "Umzug wegen neuer Stelle: Diese Umzugskosten ziehen Sie von der Steuer ab",
 "Beruflich veranlasster Umzug? Transportfirma, Reinigung, Makler, Doppelte Miete: Die Schweiz lässt viele Umzugskosten als Berufskosten abziehen – Voraussetzungen, Liste der abzugsfähigen Posten und Abgrenzung zum privaten Umzug.",
 [("Wann der Umzug «beruflich veranlasst» ist",
   """<p>Umzugskosten sind bei der direkten Bundessteuer und in den meisten Kantonen als <strong>Berufskosten abzugsfähig</strong> (Art. 33 Abs. 1 Bst. c DBG i.V.m. der Berufskostenverordnung), wenn der Umzug durch die Erwerbstätigkeit veranlasst ist. Typische anerkannte Fälle:</p>
<ul><li><strong>Stellenantritt oder Stellenwechsel</strong> an einem neuen Arbeitsort, wenn der bisherige Wohnort nicht mehr zumutbar erreichbar ist.</li>
<li><strong>Versetzung durch den Arbeitgeber</strong> (Filialwechsel, Firmensitz-Verlegung).</li>
<li><strong>Erhebliche Verkürzung des Arbeitswegs</strong> – die Praxis orientiert sich an einer täglichen Fahrzeitersparnis von rund einer Stunde (Gesamtbetrachtung; kein starres Gesetz).</li></ul>
<p>Ein rein privater Umzug (schönere Wohnung, Nähe zu Familie) ist nicht abzugsfähig – auch nicht, wenn die neue Wohnung zufällig näher an der Arbeit liegt. Massgebend ist das überwiegende Motiv.</p>
<p><strong>Praxistipp:</strong> Lassen Sie sich vom neuen Arbeitgeber ein Stellenantrittsschreiben mit Arbeitsort geben – es ist das einfachste Beweismittel für die berufliche Veranlassung.</p>"""),
  ("Was alles abziehbar ist – und was nicht",
   """<ul><li><strong>Abziehbar:</strong> Umzugsunternehmen/Spedition, Transport des Hausrats, Reinigung der alten Wohnung (übergabebedingt), Maklerprovision und Inserate für die Weitervermietung der alten Wohnung, Reisekosten für Umzugsfahrten, Lagerkosten während der Übergangszeit, Doppelte Mietzinsen bei unvermeidbarer Überschneidung, necessary Schulweg-/Betreuungsanpassungen werden kantonal unterschiedlich behandelt.</li>
<li><strong>Nicht abziehbar:</strong> Schönheitsreparaturen über die Übergabepflicht hinaus, Möbelneukäufe, private «Mitnahme»-Fahrten, Kosten für die neue Wohnung (Möbel, Umbauten).</li></ul>
<p>Werden die Kosten <strong>vom Arbeitgeber übernommen</strong>, sind sie steuerfrei – dafür entfällt der Abzug. Teil-Erstattungen sind korrekt zu deklarieren: nur der selbst getragene Rest ist abzugsfähig.</p>
<p><strong>Praxistipp:</strong> Heben Sie alle Rechnungen auf – beim Umzug geht es schnell um mehrere tausend Franken, und ohne Beleg streicht das Steueramt den Abzug.</p>"""),
  ("Pauschale oder effektiv – die Rechnung",
   """<p>Umzugskosten gehören zu den <strong>effektiven übrigen Berufskosten</strong>. Das heisst: Sie füllen das entsprechende Feld in der Steuererklärung aus und legen die Belege bei. Der Haken: Wer effektive Berufskosten geltend macht, verzichtet auf die Pauschale (Bund: 3 % des Nettolohns, min. 2'000 / max. 4'000 Fr.). Die Umzugskosten müssen die Pauschale also zusammen mit Ihren übrigen effektiven Berufskosten (Pendeln, Verpflegung, Weiterbildung) übersteigen, damit sich der Wechsel lohnt.</p>
<p>Beispiel: Umzug 6'000 Fr. + Pendlerabzug 3'000 Fr. = 9'000 Fr. effektiv – deutlich mehr als eine 4'000-Fr.-Pauschale bei mittlerem Lohn. Die Umzugskosten allein schlagen die Pauschale in vielen Fällen bereits.</p>
<p><strong>Praxistipp:</strong> Rechnen Sie beide Varianten mit unserem <a href="rechner.html">Steuerrechner</a> durch – der Kantonswechsel der Pauschalregeln macht die Antwort kantonal unterschiedlich.</p>"""),
  ("Kurz gesagt",
   """<ul><li>Beruflich veranlasster Umzug (neue Stelle, Versetzung, erhebliche Wegzeitverkürzung) = Umzugskosten als Berufskosten abziehbar.</li>
<li>Abziehbar: Transport, Reinigung, Makler/Inserate alte Wohnung, Übergangslager, unvermeidbare Doppelte Miete.</li>
<li>Nicht abziehbar: Möbel, Schönheitsreparaturen, private Motive.</li>
<li>Effektive Abrechnung verdrängt die Berufskostenpauschale – rechnen Sie nach.</li>
<li>Arbeitgeber-Erstattungen sind steuerfrei, aber nicht doppelt abzugsfähig.</li>
<li>Allgemeine Information, keine individuelle Beratung; kantonale Praxis prüfen.</li></ul>""")]),
("en", "Relocating for a new job: which moving costs are tax deductible in Switzerland",
 "Job-related move? Movers, cleaning, agent fees, double rent: Switzerland lets you deduct most moving costs as professional expenses. Requirements, the full list, and the private-move boundary.",
 [("When a move is job-related",
   """<p>Moving costs are deductible as <strong>professional expenses</strong> (Art. 33 para. 1 lit. c FITA with the professional-expenses ordinance) when the move is caused by your employment: a new job at an unreachable distance, an employer-ordered transfer, or a substantial commute reduction (practice uses roughly one hour saved per day as an indicator – an overall assessment, not a rigid rule). A purely private move is not deductible even if it happens to be closer to work.</p>
<p><strong>Practical tip:</strong> keep the new employer's job-start letter naming the work location – the simplest proof of the business motive.</p>"""),
  ("What is deductible – and what is not",
   """<ul><li><strong>Deductible:</strong> removal company, transport of household goods, handover cleaning of the old flat, agent fees and ads for re-renting the old flat, travel for moving trips, storage during the transition, unavoidable double rent.</li>
<li><strong>Not deductible:</strong> new furniture, cosmetic renovations beyond handover duties, private side trips.</li></ul>
<p>Costs <strong>reimbursed by the employer</strong> are tax-free – and cannot be deducted again. Only your own net share qualifies.</p>"""),
  ("In short",
   """<ul><li>Job-related move: moving costs deductible as professional expenses.</li>
<li>Claiming actual costs replaces the flat professional-expense allowance – run the numbers.</li>
<li>Keep every invoice; no receipts, no deduction.</li>
<li>General information, not individual advice; cantonal practice varies.</li></ul>""")]),
("fr", "Déménagement pour un nouvel emploi : quels frais de déménagement sont déductibles",
 "Déménagement professionnel ? Transport, nettoyage, frais d'agence, double loyer : la Suisse permet de déduire une grande partie des frais comme frais professionnels. Conditions et liste complète.",
 [("Quand le déménagement est professionnel",
   """<p>Les frais de déménagement sont déductibles comme <strong>frais professionnels</strong> (art. 33 al. 1 let. c LIFD) lorsqu'ils sont causés par l'activité lucrative : nouvel emploi éloigné du domicile actuel, mutation ordonnée par l'employeur, ou réduction sensible du trajet (la pratique retient environ une heure d'économie par jour – appréciation d'ensemble, pas de règle rigide). Un déménagement purement privé n'est pas déductible.</p>
<p><strong>Conseil pratique :</strong> gardez le contrat de travail mentionnant le nouveau lieu de travail – la preuve la plus simple du motif professionnel.</p>"""),
  ("Ce qui est déductible – et ce qui ne l'est pas",
   """<ul><li><strong>Déductible :</strong> entreprise de déménagement, transport du mobilier, nettoyage de restitution de l'ancien logement, frais d'agence et annonces pour la reloue, voyages de déménagement, stockage de transition, double loyer inévitable.</li>
<li><strong>Non déductible :</strong> nouveaux meubles, rénovations esthétiques, trajets privés.</li></ul>
<p>Les frais <strong>remboursés par l'employeur</strong> sont exonérés – et donc pas déductibles une seconde fois.</p>"""),
  ("En bref",
   """<ul><li>Déménagement professionnel : frais déductibles comme frais professionnels.</li>
<li>Déduction effective = renonciation au forfait des frais professionnels – calculez.</li>
<li>Conservez toutes les factures.</li>
<li>Information générale, pas un conseil individuel ; pratique cantonale variable.</li></ul>""")]),
("it", "Trasloco per un nuovo impiego: quali costi di trasloco sono deducibili",
 "Trasloco professionale? Trasporti, pulizie, spese d'agenzia, doppio affitto: la Svizzera consente di dedurre gran parte dei costi come spese professionali. Requisiti ed elenco completo.",
 [("Quando il trasloco è professionale",
   """<p>I costi di trasloco sono deducibili come <strong>spese professionali</strong> (art. 33 cpv. 1 lett. c LI) se causati dall'attività lucrativa: nuovo impiego non raggiungibile, trasferimento ordinato dal datore di lavoro o riduzione sensibile del tragitto (la pratica indica circa un'ora di risparmio giornaliero – valutazione complessiva, non regola rigida). Un trasloco puramente privato non è deducibile.</p>
<p><strong>Consiglio pratico:</strong> conservate il contratto di lavoro con il nuovo luogo di lavoro – la prova più semplice del motivo professionale.</p>"""),
  ("Cosa è deducibile – e cosa no",
   """<ul><li><strong>Deducibile:</strong> ditta di traslochi, trasporto della mobilia, pulizie di riconsegna del vecchio appartamento, spese d'agenzia e annunci per la rilocalizzazione, viaggi di trasloco, magazzino di transizione, doppio affitto inevitabile.</li>
<li><strong>Non deducibile:</strong> mobili nuovi, ristrutturazioni estetiche, viaggi privati.</li></ul>
<p>I costi <strong>rimborsati dal datore di lavoro</strong> sono esenti – e non deducibili una seconda volta.</p>"""),
  ("In breve",
   """<ul><li>Trasloco professionale: costi deducibili come spese professionali.</li>
<li>Deduzione effettiva = rinuncia al forfettario – fate i conti.</li>
<li>Conservate tutte le fatture.</li>
<li>Informazione generale, non consulenza individuale; pratica cantonale variabile.</li></ul>""")]),
])

# ============ 2. auslaendisches-depot-neobroker-steuererklaerung ============
pub("auslaendisches-depot-neobroker-steuererklaerung",
    ["wertschriftenverzeichnis-estv-kursliste.html" if os.path.exists("/Users/pino/Code/steuerberatung.ch/wertschriftenverzeichnis-estv-kursliste.html") else "kryptowaehrungen-steuern-schweiz.html",
     "verrechnungssteuer-schweiz-35-prozent.html", "steuern-sparen-tipps.html"],
[
("de", "Ausländisches Depot bei Trade Republic & Co.: So deklarieren Sie richtig",
 "Trade Republic, Interactive Brokers, Revolut: ausländische Depots gehören in die Schweizer Steuererklärung – Wertschriftenverzeichnis, Steuerwerte, Quellensteuer-Rückerstattung. Schritt für Schritt, mit den häufigsten Fehlern.",
 [("Pflicht: auch ausländische Depots gehören in die Erklärung",
   """<p>Wer in der Schweiz unbeschränkt steuerpflichtig ist, muss <strong>alle Depots weltweit</strong> deklarieren – auch Trade Republic (Deutschland), Interactive Brokers (Irland/USA), Revolut, Smartbroker und jede andere ausländische Plattform. Es spielt keine Rolle, dass die App keine Schweizer Steuerformulare liefert: Die Deklarationspflicht besteht unabhängig davon, und der automatische Informationsaustausch (AIA) macht ausländische Konten für die Steuerbehörden seit Jahren sichtbar.</p>
<p>Nicht deklarierte Depotgewinne bleiben zwar als private Kapitalgewinne meist einkommensfrei – aber das <strong>Vermögen</strong> und die <strong>Erträge</strong> (Dividenden, Zinsen) sind steuerbar. Wer sie verschweigt, riskiert Nachsteuer plus Busse; die straflose Selbstanzeige ist der Ausweg.</p>
<p><strong>Praxistipp:</strong> Exportieren Sie jedes Jahr den Kontoauszug/Steuerreport der Plattform per 31.12. – bei Trade Republic und IB gibt es fertige Jahresreports als PDF/CSV.</p>"""),
  ("Wie Sie eintragen: Wertschriftenverzeichnis, Länder, ISIN",
   """<p>Das ausländische Depot gehört ins <strong>Wertschriftenverzeichnis</strong> der Steuererklärung – Position für Position:</p>
<ul><li><strong>Depot:</strong> Bezeichnung + Sitz des Instituts (z. B. «Trade Republic Bank GmbH, DE»). Das Land entscheidet über die Quellensteuer.</li>
<li><strong>Wertpapiere:</strong> Name, ISIN, Stückzahl, Steuerwert per 31.12. Gängige Titel (Apple, Nestlé, iShares-ETFs) haben offizielle <strong>ESTV-Steuerwerte</strong> – die Kursliste finden Sie auf estv.admin.ch; für den Vermögenssteuerwert gilt der tiefere Kurs der beiden Halbjahresenden (bei vielen Titeln der 30.6. oder 31.12.).</li>
<li><strong>Erträge:</strong> Dividenden und Zinsen zum Bruttobetrag eintragen, inklusive der ausländischen Quellensteuer.</li>
<li><strong>Thesaurierende ETFs:</strong> auch ohne Ausschüttung steuerbar – die ausschüttungsgleichen Erträge meldet die Fondsleitung; bei US-ETFs zusätzlich die Rückstossmeldung beachten.</li></ul>
<p><strong>Praxistipp:</strong> Über 90 % der gängigen Titel sind in der ESTV-Kursliste erfasst. Für Nischen-Titel gilt der Kurs per 31.12. des Referenzmarkts – Screenshot genügt als Beleg.</p>"""),
  ("Quellensteuer auf Dividenden: zu viel gezahlt – zurückholen",
   """<p>Ausländische Dividenden werden im Quellstaat besteuert: <strong>26,35 % in den USA, 26,375 % in Deutschland</strong> (Kapitalertragsteuer + Soli), oft ähnlich anderswo. Die Schweiz verhindert die Doppelbelastung auf zwei Wegen:</p>
<ol><li><strong>Anrechnung/Ablösung im Inland:</strong> Die deklarierte Dividende wird voll besteuert; die anrechenbare ausländische Quellensteuer (meist 15 % gemäss DBA) wird von der Schweizer Steuer abgezogen bzw. die Steuer abgelöst.</li>
<li><strong>Rückerstattung im Quellstaat:</strong> Zu viel gezahlte Quellensteuer holen Sie sich direkt zurück – in den USA via <strong>W-8BEN-Formular</strong> beim Broker (senkt 26,35 % auf 15 % direkt an der Quelle), in Deutschland über die <strong>Quellensteuererstattung</strong> (BASt, bis 10 Jahre) oder über den Broker.</li></ol>
<p>Ohne W-8BEN verschenken US-Dividendenbezüger jährlich über 11 Prozentpunkte. Das Formular kostet zwei Minuten und gilt drei Jahre.</p>
<p><strong>Praxistipp:</strong> Prüfen Sie im Broker-Setting, ob Ihr W-8BEN hinterlegt ist – und reichen Sie die deutsche Erstattung für 2023er Dividenden nach, bevor Verjährungsfragen kompliziert werden.</p>"""),
  ("Häufigste Fehler bei Neobroker-Depots",
   """<ul><li><strong>Depot vergessen:</strong> «Die App ist doch deutsch» – irrelevant, Deklarationspflicht weltweit.</li>
<li><strong>Nur Einzahlung statt Bestand deklariert:</strong> massgebend ist der Marktwert per 31.12. (bzw. tieferer Halbjahresendwert), nicht der Kaufpreis.</li>
<li><strong>Zinsen auf Cash ignoriert:</strong> Trade Republic & Co. zahlen Tagesgeldzinsen – voll steuerbares Einkommen, oft mit deutscher Abgeltungsteuer.</li>
<li><strong>Verkaufsgewinne als Einkommen deklariert:</strong> private Veräusserungsgewinne sind steuerfrei – aber nur, wenn Sie nicht in die gewerbsmässige Anlageberatung rutschen (Haltefristen, Volumen).</li>
<li><strong>W-8BEN nie ausgefüllt:</strong> 26,35 % US-Quellensteuer statt 15 %.</li></ul>
<p><strong>Praxistipp:</strong> Nutzen Sie den <a href="rechner.html">Steuerrechner</a>, um die Belastung mit Depot-Erträgen zu testen, und lassen Sie komplexe Depots (Optionen, Hebelprodukte, Lending) von einem geprüften Partner prüfen – <a href="kontakt.html">kostenlose Erstberatung</a>.</p>"""),
  ("Kurz gesagt",
   """<ul><li>Ausländische Depots sind deklarationspflichtig: Institut + Land, ISIN, Stückzahl, Steuerwert per 31.12.</li>
<li>ESTV-Kursliste liefert die offiziellen Steuerwerte für gängige Titel; der tiefere Halbjahresendwert zählt.</li>
<li>Ausländische Quellensteuer: DBA-Anrechnung in der CH + Rückerstattung im Quellstaat (W-8BEN USA spart 11,35 Prozentpunkte).</li>
<li>Cash-Zinsen und thesaurierende ETF-Erträge nicht vergessen.</li>
<li>Private Verkaufsgewinne bleiben steuerfrei – Bestand und Erträge nicht.</li>
<li>Allgemeine Information, keine individuelle Beratung.</li></ul>""")]),
("en", "Foreign brokerage accounts: how to declare Trade Republic, Interactive Brokers & Co. correctly",
 "Trade Republic, Interactive Brokers, Revolut: foreign accounts belong in your Swiss tax return – securities schedule, ESTV tax values, foreign withholding tax refunds. Step by step, with the most common mistakes.",
 [("The duty: foreign accounts must be declared",
   """<p>Unlimited Swiss tax liability covers <strong>all accounts worldwide</strong> – Trade Republic (DE), Interactive Brokers (IE/US), Revolut and every other foreign platform. The app's lack of Swiss tax forms is irrelevant: the filing duty exists independently, and the automatic exchange of information (AEOI) has made foreign accounts visible to tax authorities for years.</p>
<p>Undeclared gains usually stay tax-free as private capital gains – but the <strong>wealth</strong> and the <strong>income</strong> (dividends, interest) are taxable. Concealment risks back taxes plus a fine; voluntary disclosure is the way out.</p>"""),
  ("How to fill it in: securities schedule, country, ISIN",
   """<p>Enter the account in the <strong>securities schedule</strong> position by position: institution + country (determines withholding tax), name, ISIN, quantity, tax value as of 31 December. Common securities (Apple, Nestlé, iShares ETFs) have official <strong>FTA tax values</strong> (rate list on estv.admin.ch); for wealth tax the lower of the two half-year-end values applies. Dividends and interest go in at gross, including foreign withholding tax. Accumulating ETFs are taxable without distribution (fund reports the equivalent income).</p>"""),
  ("Withholding tax: too much paid – get it back",
   """<p>Foreign dividends are taxed at source: <strong>26.35% in the US, 26.375% in Germany</strong>. Two relief routes: (1) credit/relief in Switzerland for the treaty portion (usually 15%), and (2) a refund from the source state – in the US via the <strong>W-8BEN form</strong> at your broker (cuts 26.35% to 15% at source), in Germany via the refund procedure (BASt) or your broker. Without W-8BEN you donate 11.35 percentage points of every US dividend; the form takes two minutes and lasts three years.</p>"""),
  ("In short",
   """<ul><li>Foreign accounts are declarable: institution + country, ISIN, quantity, tax value at 31.12.</li>
<li>FTA rate list gives official values; the lower half-year-end value counts for wealth tax.</li>
<li>Claim treaty credit in CH + source-state refund (W-8BEN saves 11.35 points on US dividends).</li>
<li>Don't forget cash interest and accumulating ETF income.</li>
<li>General information, not individual advice.</li></ul>""")]),
("fr", "Compte-titres à l'étranger : déclarer correctement Trade Republic, Interactive Brokers & Co.",
 "Trade Republic, Interactive Brokers, Revolut : les comptes étrangers figurent dans la déclaration suisse – état des titres, cours fiscaux AFC, restitution de l'impôt étranger à la source. Pas à pas, avec les erreurs fréquentes.",
 [("L'obligation : déclarer aussi les comptes étrangers",
   """<p>Une obligation fiscale illimitée en Suisse porte sur <strong>tous les comptes mondiaux</strong> – Trade Republic (DE), Interactive Brokers (IE/US), Revolut. L'absence de formulaires suisses de l'application est sans importance : l'obligation de déclarer existe, et l'échange automatique de renseignements (EAR) rend les comptes étrangers visibles depuis des années.</p>
<p>Les gains non déclarés restent souvent exonérés comme gains privés – mais la <strong>fortune</strong> et le <strong>revenu</strong> (dividendes, intérêts) sont imposables. La dissimulation expose au rappel d'impôt plus amende.</p>"""),
  ("Comment inscrire : état des titres, pays, ISIN",
   """<p>Inscrivez le compte à l'<strong>état des titres</strong> position par position : institut + pays (détermine l'impôt à la source étranger), nom, ISIN, nombre, valeur fiscale au 31 décembre. Les titres courants (Apple, Nestlé, ETF iShares) ont des <strong>cours fiscaux AFC</strong> officiels (liste sur estv.admin.ch) ; pour l'impôt sur la fortune, le plus bas des deux cours de fin de semestre s'applique. Dividendes et intérêts au brut, impôt étranger inclus. Les ETF capitalisants sont imposables sans distribution.</p>"""),
  ("Impôt étranger à la source : trop payé – récupérez",
   """<p>Les dividendes étrangers sont imposés à la source : <strong>26,35 % aux USA, 26,375 % en Allemagne</strong>. Deux voies d'allègement : (1) imputation en Suisse de la part conventionnelle (souvent 15 %), (2) restitution dans l'État source – aux USA via le formulaire <strong>W-8BEN</strong> auprès du courtier (réduit 26,35 % à 15 % à la source), en Allemagne via la procédure de restitution (BASt) ou le courtier. Sans W-8BEN, vous abandonnez 11,35 points de chaque dividende américain.</p>"""),
  ("En bref",
   """<ul><li>Comptes étrangers déclarables : institut + pays, ISIN, nombre, valeur fiscale au 31.12.</li>
<li>Liste des cours AFC pour les valeurs officielles ; le cours semestriel le plus bas compte pour la fortune.</li>
<li>Imputation conventionnelle en Suisse + restitution à la source (W-8BEN : 11,35 points économisés).</li>
<li>N'oubliez pas les intérêts sur liquidités ni les ETF capitalisants.</li>
<li>Information générale, pas un conseil individuel.</li></ul>""")]),
("it", "Deposito estero: come dichiarare correttamente Trade Republic, Interactive Brokers & Co.",
 "Trade Republic, Interactive Brokers, Revolut: i conti esteri vanno nella dichiarazione svizzera – elenco titoli, corsi fiscali AFC, restituzione dell'imposta alla fonte estera. Passo per passo, con gli errori più comuni.",
 [("L'obbligo: dichiarare anche i conti esteri",
   """<p>Un'illimitata in Svizzera riguarda <strong>tutti i conti mondiali</strong> – Trade Republic (DE), Interactive Brokers (IE/US), Revolut. La mancanza di moduli svizzeri dell'app è irrilevante: l'obbligo di dichiarare esiste, e lo scambio automatico di informazioni (SAI) rende visibili i conti esteri da anni.</p>
<p>I guadagni non dichiarati restano spesso esenti come utili privati – ma <strong>sostanza</strong> e <strong>reddito</strong> (dividendi, interessi) sono imponibili. La occultazione comporta imposta suppletiva più multa.</p>"""),
  ("Come compilare: elenco titoli, paese, ISIN",
   """<p>Iscrivete il conto nell'<strong>elenco dei titoli</strong> posizione per posizione: istituto + paese (determina l'imposta alla fonte estera), nome, ISIN, numero, valore fiscale al 31 dicembre. I titoli comuni (Apple, Nestlé, ETF iShares) hanno <strong>corsi fiscali AFC</strong> ufficiali (elenco su estv.admin.ch); per l'imposta sulla sostanza vale il più basso dei due valori di fine semestre. Dividendi e interessi al lordo, imposta estera inclusa. Gli ETF a capitalizzazione accumulazione sono imponibili senza distribuzione.</p>"""),
  ("Imposta alla fonte estera: troppo pagata – recuperatela",
   """<p>I dividendi esteri sono tassati alla fonte: <strong>26,35 % negli USA, 26,375 % in Germania</strong>. Due vie di sgravio: (1) imputazione in Svizzera della parte convenzionale (di norma 15 %), (2) restituzione nello Stato fonte – negli USA tramite il modulo <strong>W-8BEN</strong> presso il broker (riduce 26,35 % a 15 % alla fonte), in Germania tramite procedura di restituzione (BASt) o il broker. Senza W-8BEN regalate 11,35 punti percentuali di ogni dividendo americano.</p>"""),
  ("In breve",
   """<ul><li>Conti esteri dichiarabili: istituto + paese, ISIN, numero, valore fiscale al 31.12.</li>
<li>Elenco corsi AFC per i valori ufficiali; per la sostanza vale il valore di fine semestre più basso.</li>
<li>Imputazione convenzionale in Svizzera + restituzione alla fonte (W-8BEN: 11,35 punti risparmiati).</li>
<li>Non dimenticate gli interessi sul liquidità né gli ETF ad accumulazione.</li>
<li>Informazione generale, non consulenza individuale.</li></ul>""")]),
])

# ============ 3. ueberbrueckungsleistungen-ahv-fruehpensionierung ============
pub("ueberbrueckungsleistungen-ahv-fruehpensionierung",
    ["pensionskasse-teilvorbezug-fruehpensionierung.html" if os.path.exists("/Users/pino/Code/steuerberatung.ch/pensionskasse-teilvorbezug-fruehpensionierung.html") else "saeule-3a-bezug-staffeln.html",
     "13-ahv-rente-dezember-2026.html", "praemienverbilligung-2027-anmelden.html"],
[
("de", "Überbrückungsleistungen: Der AHV-Rettungsschirm für ausgesteuerte 60+",
 "Seit Dezember 2024 gibt es Überbrückungsleistungen (ÜL) für ältere Arbeitslose kurz vor der Pensionierung. Wer sie bekommt, wie hoch sie sind, was sie mit Vermögen und Steuern macht – und der Unterschied zu Ergänzungsleistungen.",
 [("Was Überbrückungsleistungen sind",
   """<p>Die <strong>Überbrückungsleistungen für ältere Arbeitslose (ÜL)</strong> sind seit <strong>1. Dezember 2024</strong> in Kraft. Sie verhindern, dass Menschen, die nach langer Beitragszeit kurz vor der AHV-Rente ausgesteuert werden, ihr Altersguthaben antasten oder Sozialhilfe beziehen müssen. Die Leistung ist eine <strong>Bedarfsleistung</strong> wie die Ergänzungsleistungen (EL): Sie deckt die Differenz zwischen anrechenbarem Einkommen und anerkanntem Bedarf – und zwar nur in der Übergangszeit bis zur AHV-Rente, längstens bis zum Rentenalter.</p>
<p><strong>Praxistipp:</strong> ÜL werden bei der Ausgleichskasse des Kantons angemeldet, nicht beim RAV. Wer die Aussteuerung absehbar hat, reicht die Anmeldung früh ein – die Prüfung dauert Wochen.</p>"""),
  ("Die Voraussetzungen im Detail",
   """<p>Anspruch haben Personen, die kumulativ:</p>
<ul><li>im Monat der Aussteuerung aus der Arbeitslosenversicherung oder danach das <strong>60. Altersjahr vollendet</strong> haben;</li><li><strong>mindestens 20 Jahre AHV-versichert</strong> waren (davon mindestens 5 Jahre nach dem 50. Geburtstag);</li>
<li>ein jährliches Erwerbseinkommen von mindestens rund <strong>22'000 Fr.</strong> (Mindeleinkommensgrenze, Stand der Einführung) erzielt haben;</li>
<li>ein Vermögen unter den Grenzwerten haben: max. <strong>50'000 Fr. (Alleinstehende)</strong> bzw. <strong>100'000 Fr. (Ehepaare)</strong> – selbstbewohnte Liegenschaften bleiben bei der Vermögensberechnung ausser Betracht;</li>
<li>in der Schweiz Wohnsitz haben und sich integrieren (Arbeitsbemühungen gemäss Vorgaben).</li></ul>
<p>Wer bereits eine AHV- oder IV-Rente bezieht, hat keinen ÜL-Anspruch – für diese Gruppe bleiben die Ergänzungsleistungen der Weg.</p>
<p><strong>Praxistipp:</strong> Die 20 Beitragsjahre müssen nicht lückenlos sein – prüfen Sie Ihren IK-Auszug; Beitragslücken aus Selbständigenjahren lassen sich teilweise nachzahlen (siehe <a href="ahv-beitragsluecken-pruefen-nachzahlen.html">AHV-Beitragslücken</a>).</p>"""),
  ("Höhe: Bedarf minus Einkommen",
   """<p>Der anerkannte Bedarf orientiert sich an den EL-Bedarfsätzen (Stand Einführung: rund <strong>20'100 Fr./Jahr für Alleinstehende</strong>, <strong>30'150 Fr. für Ehepaare</strong>, plus Kinderanteile), zuzüglich Krankenkasse, Mietzins und Nebenkosten. Anzurechnen sind Vermögenseinkommen, ein Teil des Vermögens über den Freibeträgen (Verzehr) und alle übrigen Einkünfte. Resultat: Die ÜL zahlen monatlich genau die Lücke – im Maximum knapp unter dem EL-Niveau.</p>
<p>Wichtig: ÜL sind <strong>keine Darlehen</strong> – sie müssen nicht zurückbezahlt werden (anders als Nothilfe). Ein allfälliger Erlassanspruch der Kantone entfällt.</p>"""),
  ("Steuern, Pensionskasse und der Zusammenhang",
   """<p>ÜL sind nach der Steuerpraxis <strong>steuerbares Einkommen</strong> (wie EL), aber wegen des tiefen Niveaus meist unter dem Steuerfreibetrag – die Steuererklärung trotzdem ausfüllen. Die eigentliche Planung liegt woanders: Wer ÜL bezieht, sollte <strong>kein 3a- oder BVG-Kapital vorbeziehen</strong> – das Guthaben bleibt geschützt, weil die Leistung die Lücke schliesst. Und: Das Vermögen darf die Grenzen (50'000/100'000 Fr.) nicht überschreiten – ein zu früh verkauften Haus oder eine 3a-Auszahlung kann den Anspruch kippen.</p>
<p><strong>Praxistipp:</strong> Wer zwischen 58 und 62 eine Kündigung erhält, prüfe die Reihenfolge: ALV ausschöpfen → ÜL anmelden → Kapitalbezüge erst nach Rentenalter. Lassen Sie die Konstellation vor dem ersten Schritt prüfen – <a href="kontakt.html">kostenlose Erstberatung</a>.</p>"""),
  ("Kurz gesagt",
   """<ul><li>ÜL (seit 1.12.2024): Bedarfsleistung für ausgesteuerte Erwerbslose ab 60 bis zur AHV-Rente.</li>
<li>Voraussetzungen: 20 AHV-Jahre (5 nach dem 50. Geburtstag), Mindeleinkommen, Vermögen unter 50'000/100'000 Fr., Wohnsitz CH.</li>
<li>Höhe = Bedarf (EL-Niveau) minus anrechenbares Einkommen/Vermögen; keine Rückzahlungspflicht.</li>
<li>Steuerbar wie EL, aber meist unter dem Freibetrag.</li>
<li>Vorbezüge aus 2./3. Säule gefährden den Anspruch – Timing planen.</li>
<li>Allgemeine Information, keine individuelle Beratung.</li></ul>""")]),
("en", "Bridging benefits: the AHV safety net for the long-term unemployed over 60",
 "Since December 2024 Switzerland pays bridging benefits (ÜL) to older unemployed people just before retirement. Who qualifies, how much, and how it interacts with wealth limits, pensions and taxes.",
 [("What bridging benefits are",
   """<p>The <strong>bridging benefits for older unemployed persons (ÜL)</strong> took effect on <strong>1 December 2024</strong>. They prevent people who are exhausted from unemployment insurance shortly before their AHV pension from touching their pension capital or relying on social assistance. Like supplementary benefits (EL), they are a <strong>means-tested benefit</strong> covering the gap between creditable income and recognised needs – only during the bridge to the AHV pension.</p>"""),
  ("The requirements in detail",
   """<p>Cumulative conditions: aged <strong>60 or over</strong> in the month of (or after) exhaustion of unemployment benefits; at least <strong>20 AHV contribution years</strong> (5 of them after the 50th birthday); a minimum annual earned income (around CHF 22,000 at introduction); wealth below <strong>CHF 50,000 (single) / 100,000 (couples)</strong> – owner-occupied property is excluded from the wealth calculation; Swiss residence and integration efforts. Existing AHV/IV pensioners are not eligible – for them EL remains the route.</p>"""),
  ("Amount, taxes and pension planning",
   """<p>The recognised need follows EL-level rates (roughly CHF 20,100/year for singles at introduction) plus health insurance and housing costs; income and part of the wealth above allowances are credited. The benefit is not a loan – no repayment. Tax-wise, ÜL are taxable income like EL but usually below the allowance. The real planning point: drawing a 3a or BVG lump sum before the pension can breach the wealth limits and kill the claim.</p>
<p><strong>Practical tip:</strong> If you are made redundant between 58 and 62, the order is: exhaust unemployment insurance → apply for bridging benefits → pension withdrawals only after retirement age.</p>"""),
  ("In short",
   """<ul><li>ÜL (since 1.12.2024): means-tested bridge for unemployed 60+ until the AHV pension.</li>
<li>20 AHV years, minimum income, wealth under 50k/100k, Swiss residence.</li>
<li>No repayment duty; taxable like EL but usually below the allowance.</li>
<li>Early pension withdrawals can destroy the claim – plan the sequence.</li>
<li>General information, not individual advice.</li></ul>""")]),
("fr", "Prestations-pont : le filet social AHV pour les chômeurs de 60 ans et plus",
 "Depuis décembre 2024, la Suisse verse des prestations-pont (PP) aux chômeurs âgés juste avant la retraite. Qui y a droit, à combien, et quels effets sur la fortune, la prévoyance et les impôts.",
 [("Ce que sont les prestations-pont",
   """<p>Les <strong>prestations-pont pour chômeurs âgés (PP)</strong> sont en vigueur depuis le <strong>1er décembre 2024</strong>. Elles évitent aux personnes épuisées par l'assurance-chômage peu avant la rente AHV d'entamer leur avoir de vieillesse ou de recourir à l'aide sociale. Comme les prestations complémentaires (PC), c'est une <strong>prestation fonction des besoins</strong> qui comble l'écart entre revenu déterminant et besoins reconnus – uniquement pendant le pont vers la rente.</p>"""),
  ("Les conditions en détail",
   """<p>Conditions cumulatives : <strong>60 ans révolus</strong> le mois de l'épuisement du droit ou après ; au moins <strong>20 années de cotisations AHV</strong> (dont 5 après le 50e anniversaire) ; revenu du travail annuel minimal (environ 22 000 fr. à l'introduction) ; fortune inférieure à <strong>50 000 fr. (seul) / 100 000 fr. (couple)</strong> – le logement de propre est exclu du calcul ; domicile en Suisse et efforts d'intégration. Les rentiers AHV/AI existants ne sont pas éligibles – la voie reste la PC.</p>"""),
  ("En bref",
   """<ul><li>PP (dès 1.12.2024) : prestation sous conditions de ressources pour chômeurs de 60 ans et plus jusqu'à la rente AHV.</li>
<li>20 années AHV, revenu minimal, fortune sous 50k/100k, domicile suisse.</li>
<li>Pas de remboursement ; imposable comme la PC mais souvent sous le seuil.</li>
<li>Un retrait anticipé 2e/3e pilier peut détruire le droit – planifiez l'ordre.</li>
<li>Information générale, pas un conseil individuel.</li></ul>""")]),
("it", "Prestazioni ponte: la rete AHV per i disoccupati over 60",
 "Dal dicembre 2024 la Svizzera versa prestazioni ponte (PP) ai disoccupati anziani poco prima del pensionamento. Chi ne ha diritto, a quanto, e quali effetti su sostanza, previdenza e imposte.",
 [("Cosa sono le prestazioni ponte",
   """<p>Le <strong>prestazioni ponte per disoccupati anziani (PP)</strong> sono in vigore dal <strong>1° dicembre 2024</strong>. Impediscono a chi, esaurita l'assicurazione contro la disoccupazione poco prima della rendita AHV, debba intaccare il capitale di previdenza o ricorrere all'assistenza sociale. Come le prestazioni complementari (PC), sono una <strong>prestazione subordinata ai bisogni</strong> che colma la lacuna tra reddito determinanti e bisogni riconosciuti – solo durante il ponte verso la rendita.</p>"""),
  ("I requisiti in dettaglio",
   """<p>Condizioni cumulative: <strong>60 anni compiuti</strong> nel mese di esaurimento del diritto o dopo; almeno <strong>20 anni di contributi AHV</strong> (di cui 5 dopo i 50 anni); reddito annuo minimo (circa 22'000 fr. all'introduzione); sostanza sotto <strong>50'000 fr. (single) / 100'000 fr. (coppie)</strong> – l'abitazione di proprietà esclusa dal calcolo; domicilio in Svizzera e sforzi d'integrazione. I percettori di rendita AHV/AI non hanno diritto – per loro resta la via delle PC.</p>"""),
  ("In breve",
   """<ul><li>PP (dal 1.12.2024): prestazione subordinata ai bisogni per disoccupati dai 60 anni fino alla rendita AHV.</li>
<li>20 anni AHV, reddito minimo, sostanza sotto 50k/100k, domicilio svizzero.</li>
<li>Nessun obbligo di rimborso; imponibile come le PC ma spesso sotto la franchigia.</li>
<li>Prelievi anticipati 2°/3° pilastro possono distruggere il diritto – pianificate l'ordine.</li>
<li>Informazione generale, non consulenza individuale.</li></ul>""")]),
])

# ============ 4. teilliquidation-pensionskasse-auszahlung ============
pub("teilliquidation-pensionskasse-auszahlung",
    ["saeule-3a-bezug-staffeln.html", "pensionskassen-einkauf-steuern-sparen.html", "steuern-sparen-tipps.html"],
[
("de", "Teilliquidation der Pensionskasse: Kapital beziehen und getrennt besteuern",
 "Restrukturiert Ihre Kasse ein Vorsorgewerk? Bei einer Teilliquidation können austretende Versicherte das ganze Guthaben bar beziehen – und es getrennt vom übrigen Einkommen zum Vorsorgetarif zahlen. Voraussetzungen, Fristen, Steuerrechnung.",
 [("Was eine Teilliquidation ist",
   """<p>Eine <strong>Teilliquidation</strong> liegt vor, wenn ein Vorsorgewerk (z. B. die Pensionskasse eines Arbeitgebers oder ein Branchenkollektiv) teilweise aufgelöst wird: Betriebsschliessung, Ausgliederung, Personalabbau oder eine Kapitalreduktion von mindestens <strong>20 %</strong> der aktiven und passiven Versicherten bzw. der Vorsorgestiftung (leitende Praxis nach BGE 134 II 244). Die Kasse muss die Teilliquidation <strong>der Aufsichtsbehörde melden</strong>; erst mit deren Genehmigung ist sie gültig.</p>
<p>Für die Betroffenen ändert sich der Status: Sie dürfen das <strong>Freizügigkeitsguthaben bar beziehen</strong>, obwohl ein laufendes Arbeitsverhältnis oder ein regulärer Vorsorgegrund fehlt – normalerweise eine Ausnahme, hier ein Recht.</p>
<p><strong>Praxistipp:</strong> Fragen Sie Ihre Kasse aktiv, ob eine Teilliquidation genehmigt wurde – die Mitteilung kommt oft nur indirekt über den Arbeitgeber oder das Freizügigkeitsformular.</p>"""),
  ("Die Steuerfolge: getrennte Besteuerung zum Vorsorgetarif",
   """<p>Der steuerliche Kernvorteil: Bei einer genehmigten Teilliquidation wird die Kapitalleistung <strong>getrennt vom übrigen Einkommen</strong> besteuert (Art. 37 Abs. 4 / Art. 38 Abs. 3 DBG; kantonal analog, z. B. § 37 StG ZH) – und zwar zum <strong>reduzierten Vorsorgetarif</strong> (Bund: ein Fünftel des Tarifs; Kantone halbieren oder dritteln meist). Das Guthaben wird also isoliert, zu einem Bruchteil des normalen Satzes besteuert.</p>
<p>Aber – und das ist die häufigste Falle: Die getrennte Besteuerung setzt voraus, dass das <strong>ganze Vorsorgeguthaben dieses Vorsorgewerks</strong> ausbezahlt wird (BGE-Praxis: Teilauszahlungen werden zum ordentlichen Tarif zum übrigen Einkommen addiert). Wer nur einen Teil «rausholen» will, zahlt deutlich mehr.</p>
<p><strong>Praxistipp:</strong> Liegt Ihr Guthaben auf mehreren Kassen (alter Arbeitgeber + aktuelle), ist nur das Guthaben des teilliquidierten Werks privilegiert – planen Sie die Bezüge der anderen Säulen gestaffelt in Folgejahre (siehe <a href="saeule-3a-bezug-staffeln.html">3a gestaffelt beziehen</a>).</p>"""),
  ("Fristen und Verfahren",
   """<ul><li>Die Kasse setzt den <strong>Bezugszeitraum</strong> fest (häufig mehrere Monate bis wenige Jahre nach Genehmigung).</li>
<li>Der Bezug ist an das Ende des Arbeitsverhältnisses bzw. die reglementarischen Bedingungen der Teilliquidation gebunden – reglementarisch kann auch ein Verbleib mit Übertragung erlaubt sein.</li>
<li>Wer das Guthaben in eine <strong>andere Vorsorgeeinrichtung</strong> überweist, zahlt gar keine Steuer – die Wahl zwischen Barbezug und Überweisung ist eine reine Steuer- und Vermögensfrage.</li>
<li>Kantonale Quellensteuer: Der Bezugsort (letzter Wohnsitzkanton des Vorsorgewerks bzw. Ihr Wohnsitz – je nach Kanton) erhebt die separate Steuer bei Zufluss.</li></ul>
<p>Beispielrechnung (illustrativ): Guthaben 250'000 Fr., Einkommen 120'000 Fr. Getrennt zum Vorsorgetarif fallen je nach Kanton rund 10'000–15'000 Fr. an; würde dasselbe Kapital zum ordentlichen Tarif besteuert, läge die Belastung ein Mehrfaches höher.</p>"""),
  ("Barbezug oder Überweisung? Die Entscheidungsfragen",
   """<ol><li><strong>Vermögenslage:</strong> Brauchen Sie das Geld (Immobilienkauf, Selbständigkeit)? Dann Barbezug mit getrennter Besteuerung nutzen.</li>
<li><strong>Vorsorgelücke:</strong> Der Barbezug löscht das Altersguthaben dieses Werks – die Lücke muss anderweitig geschlossen werden (3a ist nur begrenzt Ersatz).</li>
<li><strong>Erbschaft/EL:</strong> Barvermögen ist frei verfügbar, aber EL-relevant; Vorsorgeguthaben ist gebunden.</li>
<li><strong>Steuerjahr:</strong> Der Bezug fällt ins aktuelle Jahr – wenn möglich nicht mit anderen Kapitalleistungen (3a, UV) im selben Jahr kombinieren, das addiert beim Vorsorgetarif.</li></ol>
<p><strong>Praxistipp:</strong> Die Entscheidung fällt oft über Zehntausende Franken – lassen Sie beide Varianten vor Ablauf der Bezugsfrist durchrechnen. Geprüfte Partner in Ihrem Kanton: <a href="kontakt.html">kostenlose Erstberatung</a>.</p>"""),
  ("Kurz gesagt",
   """<ul><li>Teilliquidation = teilweise Auflösung eines Vorsorgewerks (mind. 20 %-Schwelle bzw. Betriebsänderung), genehmigungspflichtig durch die Aufsicht.</li>
<li>Recht auf Barbezug des Freizügigkeitsguthabens ohne regulären Vorsorgegrund.</li>
<li>Getrennte Besteuerung zum reduzierten Vorsorgetarif – aber nur bei Auszahlung des ganzen Guthabens dieses Werks.</li>
<li>Überweisung in eine andere Kasse = keine Steuer; Barbezug = einmalige separate Steuer.</li>
<li>Bezugsfrist der Kasse beachten; nicht mit andern Kapitalleistungen im selben Jahr häufen.</li>
<li>Allgemeine Information, keine individuelle Beratung.</li></ul>""")]),
("en", "Partial liquidation of a pension fund: cash withdrawal with separate taxation",
 "Is your fund restructuring a pension institution? A partial liquidation lets departing insureds withdraw the full balance in cash – taxed separately at the reduced pension rate. Requirements, deadlines, the tax maths.",
 [("What a partial liquidation is",
   """<p>A <strong>partial liquidation</strong> exists when part of a pension institution is wound up: business closure, carve-out, headcount reduction, or a capital reduction of at least <strong>20%</strong> of the insured (leading practice, BGE 134 II 244). The fund must notify the <strong>supervisory authority</strong>; it is valid only once approved. Affiliated members then have the right to a <strong>cash withdrawal</strong> of their vested benefits without a regular pension ground.</p>"""),
  ("The tax effect: separate taxation at the pension rate",
   """<p>The core advantage: with an approved partial liquidation the lump sum is taxed <strong>separately from all other income</strong> (Art. 37 para. 4 / Art. 38 para. 3 FITA; cantonal rules analogous) at the <strong>reduced pension rate</strong> (federal: one fifth of the tariff; cantons halve or third it). The trap: separate taxation requires payout of the <strong>entire balance of that institution</strong> – partial payouts are added to ordinary income at the full rate.</p>"""),
  ("In short",
   """<ul><li>Partial liquidation = partial wind-up (20% threshold or business change), supervisory approval required.</li>
<li>Right to cash withdrawal of vested benefits without a regular pension ground.</li>
<li>Separate taxation at the reduced pension rate – only for the full balance of that fund.</li>
<li>Transfer to another fund = no tax; cash = one-off separate tax.</li>
<li>Respect the fund's withdrawal window; avoid stacking lump sums in one year.</li>
<li>General information, not individual advice.</li></ul>""")]),
("fr", "Liquidation partielle de la caisse de pension : retrait en espèces avec imposition séparée",
 "Votre caisse restructure-t-elle une institution de prévoyance ? La liquidation partielle permet aux assurés sortants de toucher leur avoir en espèces – imposé séparément au taux réduit de prévoyance. Conditions, délais, calcul fiscal.",
 [("Ce qu'est une liquidation partielle",
   """<p>Une <strong>liquidation partielle</strong> existe lorsqu'une partie d'une institution de prévoyance est dissoute : fermeture d'exploitation, désaffiliation, réduction d'effectifs ou réduction de capital d'au moins <strong>20 %</strong> des assurés (pratique constante, ATF 134 II 244). La caisse doit annoncer l'opération à l'<strong>autorité de surveillance</strong> ; elle n'est valable qu'une fois approuvée. Les assurés concernés obtiennent le droit de toucher leur avoir de libre passage <strong>en espèces</strong>, sans motif de prévoyance ordinaire.</p>"""),
  ("L'effet fiscal : imposition séparée au taux de prévoyance",
   """<p>Avantage central : avec une liquidation partielle approuvée, la prestation en capital est imposée <strong>séparément du reste du revenu</strong> (art. 37 al. 4 / art. 38 al. 3 LIFD ; droit cantonal analogue) au <strong>taux réduit de prévoyance</strong> (Confédération : un cinquième du barème ; cantons : moitié ou tiers). Le piège : l'imposition séparée exige le versement de l'<strong>avoir intégral de cette institution</strong> – un versement partiel s'ajoute au revenu ordinaire au taux plein.</p>"""),
  ("En bref",
   """<ul><li>Liquidation partielle = dissolution partielle (seuil de 20 % ou changement d'exploitation), soumise à approbation.</li>
<li>Droit au retrait en espèces de l'avoir de libre passage sans motif ordinaire.</li>
<li>Imposition séparée au taux réduit – uniquement pour l'avoir complet de cette caisse.</li>
<li>Transfert vers une autre caisse = pas d'impôt ; espèces = impôt séparé unique.</li>
<li>Respectez le délai de retrait ; évitez de cumuler plusieurs capitaux la même année.</li>
<li>Information générale, pas un conseil individuel.</li></ul>""")]),
("it", "Liquidazione parziale della cassa pensione: prelievo in contanti con imposizione separata",
 "La vostra cassa sta riorganizzando un istituto di previdenza? La liquidazione parziale consente agli assicurati uscenti di prelevare l'intero avere in contanti – tassato separatamente all'aliquota ridotta di previdenza. Requisiti, termini, calcolo fiscale.",
 [("Cos'è una liquidazione parziale",
   """<p>Una <strong>liquidazione parziale</strong> sussiste quando una parte di un istituto di previdenza viene disciolta: chiusura d'azienda, scorporo, riduzione del personale o riduzione di capitale di almeno il <strong>20 %</strong> degli assicurati (prassi consolidata, DTF 134 II 244). La cassa deve annunciare l'operazione all'<strong>autorità di vigilanza</strong>; è valida solo dopo l'approvazione. Gli assicurati interessati ottengono il diritto di prelevare la prestazione di libero passaggio <strong>in contanti</strong>, senza un motivo previdenziale ordinario.</p>"""),
  ("L'effetto fiscale: imposizione separata all'aliquota di previdenza",
   """<p>Vantaggio centrale: con una liquidazione parziale approvata, la prestazione in capitale è tassata <strong>separatamente dal resto del reddito</strong> (art. 37 cpv. 4 / art. 38 cpv. 3 LI; diritto cantonale analogo) all'<strong>aliquota ridotta di previdenza</strong> (Confederazione: un quinto del barème; cantoni: metà o terzo). La trappola: l'imposizione separata esige il versamento dell'<strong>intero avere di questo istituto</strong> – un prelievo parziale si somma al reddito ordinario all'aliquota piena.</p>"""),
  ("In breve",
   """<ul><li>Liquidazione parziale = scioglimento parziale (soglia del 20 % o cambiamento d'azienda), soggetta ad approvazione.</li>
<li>Diritto al prelievo in contanti della prestazione di libero passaggio senza motivo ordinario.</li>
<li>Imposizione separata all'aliquota ridotta – solo per l'avoro completo di questa cassa.</li>
<li>Trasferimento a un'altra cassa = nessuna imposta; contanti = imposta separata unica.</li>
<li>Rispettate il termine di prelievo; evitate di cumulare più capitali nello stesso anno.</li>
<li>Informazione generale, non consulenza individuale.</li></ul>""")]),
])
print("all four built")
