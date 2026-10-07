#!/usr/bin/env python3
"""Build the expat taxation guide in all 4 languages.

Slug: expats-steuern-schweiz
Sources (primary, verified 2026-10-06):
- ESTV Merkblatt 'Besteuerung an der Quelle' (estv2.admin.ch) — NOV thresholds
- Art. 89/89a DBG, Art. 33a/33b StHG — obligatorische/fakultative NOV
- Kreisschreiben Nr. 45 ESTV
- SAHK/Estv: 3a Maximalbeträge 2026 (7'258 / 36'288)
- Art. 33 Abs. 3 lit. c DBG — Drittbetreuungskosten bis 25'000/Kind (Bund)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "expats-steuern-schweiz"
RELATED = ["grenzgaenger-de-fr-it-steuern.html",
           "steuern-sparen-tipps.html",
           "kryptowaehrungen-steuern-schweiz.html"]

# ---------------- German ----------------
de_title = "Expats in der Schweiz: Steuern, Quellensteuer und die 120'000-Falle"
de_meta = "Als Expat in der Schweiz: Was Sie zur Quellensteuer, zur obligatorischen nachträglichen ordentlichen Veranlagung ab 120'000 Franken Weltlohn, zur Deklaration von Weltvermögen und zu den wichtigsten Abzügen 2026 wissen müssen."
de_sections = [
 ("Wer in der Schweiz steuerpflichtig ist",
  """<p>Sobald Sie Ihren Wohnsitz in die Schweiz verlegen – mit Ausweis B oder C – sind Sie hier <strong>unbeschränkt steuerpflichtig</strong>: besteuert werden Ihr <strong>Welteneinkommen und Ihr Weltvermögen</strong>, also auch Konten, Depots und Liegenschaften im Ausland. Massgebend ist der tatsächliche Lebensmittelpunkt, nicht die Staatsangehörigkeit.</p>
<p>Kurzzeitige Aufenthalte ohne Wohnsitz (z. B. Entsendung unter 90 Tagen) bleiben meist im Heimatland steuerpflichtig; wer aber einen Aufenthalt von mehr als 30 Tagen mit Erwerbsarbeit oder über 90 Tage insgesamt hat, begründet in der Regel eine Steuerpflicht in der Schweiz. Doppelbesteuerungsabkommen (DBA) verteilen die Besteuerungsrechte – sie ersetzen die Schweizer Deklarationspflicht nicht, sie begrenzen nur, was die Schweiz besteuern darf.</p>
<p><strong>Praxistipp:</strong> Melden Sie sich bei Zuzug aus dem Ausland beim Gemeindesteueramt – die Quellensteuer regelt der Arbeitgeber, aber die Deklaration von Auslandvermögen und -einkünften ist allein Ihre Pflicht.</p>"""),
 ("Quellensteuer: das Startsystem für B-Bewilligte",
  """<p>Mit Aufenthaltsbewilligung B werden Lohn und die meisten Einkünfte <strong>an der Quelle besteuert</strong>: Der Arbeitgeber zieht die Quellensteuer direkt vom Bruttolohn ab und meldet sie der Steuerbehörde. Sie erhalten den Nettolohn ausgezahlt – erst einmal ohne eigene Steuererklärung. Der angewendete Tarif berücksichtigt pauschal den Kinderabzug, den Sozialabzug und die üblichen Berufskosten (Pauschale).</p>
<p>Mit <strong>Niederlassungsbewilligung C</strong> fallen Sie in die ordentliche Veranlagung: Sie füllen die normale Steuererklärung aus und zahlen nach Veranlagung.</p>
<p>Wichtig zu wissen: Der Quellensteuertarif ist eine <strong>Pauschale</strong>. Tatsächliche Kosten – hohe Berufskosten, Weiterbildungen, Krankheitskosten, Versicherungen – sind darin meist nicht enthalten. Genau hier liegt für viele Expats Geld brach.</p>"""),
 ("Die 120'000-Falle: obligatorische nachträgliche ordentliche Veranlagung",
  """<p>Erreichen Sie als quellensteuerpflichtige Person ein <strong>Bruttojahreseinkommen ab CHF 120'000</strong> (vor Abzügen, auf 12 Monate hochgerechnet bei unterjährigem Zuzug), wird zwingend eine <strong>nachträgliche ordentliche Veranlagung (NOV)</strong> durchgeführt (Art. 89 DBG, Art. 33a StHG): Sie müssen eine volle Steuererklärung über Ihr Welteneinkommen und Weltvermögen ausfüllen. Die bezahlte Quellensteuer wird angerechnet.</p>
<p>Auch unter 120'000 können Sie die NOV <strong>freiwillig beantragen</strong> – Frist: in der Regel bis zum 31. März des Folgejahres (Art. 89a DBG). Das lohnt sich fast immer, wenn Sie höhere effektive Kosten haben als die Tarifpauschale: Pensionskasseneinkauf, Säule 3a, effektive Berufskosten, Drittbetreuungskosten, Schuldzinsen im Ausland.</p>
<p><strong>Praxistipp:</strong> Prüfen Sie jedes Jahr, ob Sie über oder unter 120'000 liegen – und nutzen Sie unter der Grenze aktiv die freiwillige NOV. Wer sie nicht beantragt, verschenkt regelmäßig mehrere tausend Franken.</p>"""),
 ("Weltvermögen deklarieren: Konten, Depots, Krypto, Liegenschaften",
  """<p>Die Schweiz besteuert Ihr gesamtes Vermögen – auch im Ausland: Bankkonten, Depots, Kryptowährungen, Liegenschaften. Tragen Sie alles im Wertschriftenverzeichnis ein; ausländische Liegenschaften zum Belegwert (in der Regel Verkehrswert laut ausländischer Steuerrechnung).</p>
<p>Erträge aus ausländischen Liegenschaften (Eigenmietwert bzw. Mieteinnahmen) sind in der Schweiz steuerbar – die Schweiz gewährt dafür meist eine Befreiung mit Progressionsvorbehalt, je nach DBA. Krypto gilt als Privatvermögen: Bestand ja (Vermögenssteuer), private Veräusserungsgewinne in der Regel steuerfrei.</p>
<p><strong>Praxistipp:</strong> Das automatische Informationsaustausch-Netz (AIA/CRS) erfasst Auslandkonten bereits heute; ab 2027/2028 folgt mit CARF auch Krypto. Lücken in der Deklaration fallen auf – vollständige Deklaration von Anfang an ist der günstigste Weg.</p>"""),
 ("Die wichtigsten Abzüge für Expats 2026",
  """<ul><li><strong>Säule 3a:</strong> bis CHF 7'258 (mit Pensionskasse) bzw. 20 % des Erwerbseinkommens, max. CHF 36'288 (ohne) – voll abzugsfähig; ab 2026 sind Nachzahlungen für lückenhafte Jahre möglich.</li>
<li><strong>Pensionskasseneinkauf:</strong> freiwillige Einkäufe in die 2. Säule senken das steuerbare Einkommen – Rückbezugssperre von 3 Jahren beachten (Art. 79b BV).</li>
<li><strong>Berufskosten:</strong> Pendlerabzug (max. CHF 8'000 Bund), Weiterbildung, Mehrkosten der Verpflegung – bei Quellensteuer nur pauschal enthalten, via NOV effektiv abziehbar.</li>
<li><strong>Kinderdrittbetreuung:</strong> bis CHF 25'000 pro Kind (Bund, Art. 33 Abs. 3 lit. c DBG) bei Kinder unter 16 – Kita, Hort, Au-pair-Betreuungsanteile.</li>
<li><strong>Verrechnungssteuer:</strong> 35 % auf Schweizer Bankzinsen und Dividenden – rückforderbar via Steuererklärung bzw. Erstattungsverfahren (Frist 3 Jahre).</li></ul>
<p><strong>Praxistipp:</strong> Expats mit hohem Lohn und Familie haben fast immer effektiv höhere Kosten als die Pauschalen des Quellensteuertarifs – die NOV ist ihr wichtigster Hebel.</p>"""),
 ("Wegzug und Rückkehr: Sperrfristen und Kapitalleistungen",
  """<p>Beim Wegzug in ein DBA-Land können Sie Ihre <strong>2. Säule bar beziehen</strong> (ganze Austrittsleistung), bei Wegzug in ein EU/EFTA-Land ohne selbstständige Tätigkeit nur das Altersguthaben der 2. Säule (das BVG-Altersguthaben), nicht das Überobligatorium. Die <strong>Säule 3a</strong> bleibt bis zum ordentlichen Rentenalter gesperrt (Ausnahme: endgültiger Wegzug aus der Schweiz – dann Bezug möglich, Quellensteuer auf Kapitalleistungen des Wegzugjahres).</p>
<p>Der Wegzug selbst ist steuerfrei – solange Sie in den letzten 5 Jahren nicht überwiegend in der Schweiz steuerpflichtig waren und die Liegenschaften im Privatvermögen bleiben. Wer kurz nach dem Wegzug verkauft, riskiert eine Nachbesteuerung in der Schweiz.</p>
<p><strong>Praxistipp:</strong> Planen Sie Kapitalbezüge und Verkäufe vor dem Wegzug – nach dem Wegzug gelten die Regeln des neuen Wohnsitzlandes, und die Schweiz prüft Umwegkonstruktionen genau.</p>"""),
 ("Kurz gesagt",
  """<ul><li>Wohnsitz Schweiz = unbeschränkte Steuerpflicht auf Welteneinkommen und Weltvermögen – Deklaration der Auslandwerte ist Ihre Pflicht.</li>
<li>B-Bewilligung: Quellensteuer mit Pauschaltarifen; C-Bewilligung: ordentliche Veranlagung.</li>
<li>Ab CHF 120'000 Bruttolohn: obligatorische nachträgliche ordentliche Veranlagung (NOV) – darunter freiwillig beantragen und Abzüge nachholen.</li>
<li>Grösste Hebel: 3a (7'258), Pensionskasseneinkauf, effektive Berufskosten via NOV, Kinderdrittbetreuung bis 25'000/Kind.</li>
<li>Wegzug: 2. Säule meist beziehbar, 3a gesperrt bis Auswanderung – Timing entscheidet.</li>
<li>Dies ist allgemeine Information, keine individuelle Beratung – lassen Sie Ihre Situation von einem Treuhänder oder Steuerberater mit DBA-Erfahrung prüfen (kostenlose Erstberatung via kontakt.html).</li></ul>"""),
]

# ---------------- English ----------------
en_title = "Expats in Switzerland: Taxes, source tax and the CHF 120,000 trap"
en_meta = "Moving to Switzerland as an expat? What you need to know in 2026 about source tax, the mandatory retroactive ordinary assessment above CHF 120,000 world salary, declaring worldwide assets, and the key deductions."
en_sections = [
 ("Who becomes tax resident in Switzerland",
  """<p>Once you move your residence to Switzerland – with a B or C permit – you are subject to <strong>unlimited tax liability</strong>: your <strong>worldwide income and worldwide wealth</strong> are taxable, including foreign bank accounts, portfolios and real estate. What counts is your actual centre of life, not your nationality.</p>
<p>Short stays without residence (e.g. secondment under 90 days) usually remain taxable in your home country; but a stay of more than 30 days with gainful activity, or more than 90 days overall, generally creates Swiss tax liability. Double tax treaties (DTT) allocate taxing rights – they do not replace your Swiss filing duty, they only limit what Switzerland may tax.</p>
<p><strong>Practical tip:</strong> register with the municipal tax office when you arrive. Your employer handles source tax – but declaring foreign assets and income is solely your responsibility.</p>"""),
 ("Source tax: the starting system for B-permit holders",
  """<p>With a B residence permit, your salary and most income are <strong>taxed at source</strong>: the employer deducts the tax from your gross salary and remits it to the tax authority. You receive the net salary – initially without filing your own return. The tariff applied includes flat-rate allowances for children, social deductions and typical professional expenses.</p>
<p>With a <strong>C settlement permit</strong> you move to ordinary assessment: you file the regular tax return and pay after assessment.</p>
<p>Key point: the source tax tariff is a <strong>flat rate</strong>. Actual costs – high professional expenses, further training, health costs, insurance – are mostly not included. That is exactly where many expats leave money on the table.</p>"""),
 ("The 120,000 trap: mandatory retroactive ordinary assessment",
  """<p>If a source-taxed person reaches a <strong>gross annual income of CHF 120,000 or more</strong> (before deductions; annualised for partial years), a <strong>retroactive ordinary assessment (NOV)</strong> is mandatory (Art. 89 FITA, Art. 33a HTA): you must file a full tax return covering worldwide income and wealth. Tax already paid at source is credited.</p>
<p>Below 120,000 you can <strong>request the NOV voluntarily</strong> – usually until 31 March of the following year (Art. 89a FITA). It almost always pays off if your actual costs exceed the flat allowances: pension fund buy-ins, pillar 3a, effective professional expenses, third-party childcare, foreign mortgage interest.</p>
<p><strong>Practical tip:</strong> check every year whether you are above or below 120,000 – and actively use the voluntary NOV below the threshold. Skipping it regularly forfeits several thousand francs.</p>"""),
 ("Declaring worldwide wealth: accounts, portfolios, crypto, property",
  """<p>Switzerland taxes your entire wealth – including abroad: bank accounts, securities portfolios, crypto assets, real estate. Enter everything in the securities schedule; foreign property at documented value (usually the market value from the foreign tax bill).</p>
<p>Income from foreign real estate (imputed rent or rental income) is taxable in Switzerland – Switzerland usually grants an exemption with progression reservation, depending on the DTT. Crypto counts as private wealth: holdings yes (wealth tax), private capital gains generally tax-free.</p>
<p><strong>Practical tip:</strong> the automatic exchange of information (AEOI/CRS) already captures foreign accounts today; CARF extends this to crypto from 2027/2028. Gaps in declarations get noticed – full declaration from day one is the cheapest path.</p>"""),
 ("The most important deductions for expats 2026",
  """<ul><li><strong>Pillar 3a:</strong> up to CHF 7,258 (with pension fund) or 20% of employment income, max CHF 36,288 (without) – fully deductible; from 2026, catch-up contributions for deficient years are possible.</li>
<li><strong>Pension fund buy-in:</strong> voluntary buy-ins into the 2nd pillar reduce taxable income – observe the 3-year blocking period for later withdrawals (Art. 79b Federal Constitution).</li>
<li><strong>Professional expenses:</strong> commuting deduction (max CHF 8,000 federal), further training, extra meal costs – only flat-rated in source tax, deductible at actual cost via the NOV.</li>
<li><strong>Third-party childcare:</strong> up to CHF 25,000 per child (federal, Art. 33 para. 3 lit. c FITA) for children under 16 – nursery, daycare, au-pair care shares.</li>
<li><strong>Withholding tax:</strong> 35% on Swiss bank interest and dividends – reclaimable via the tax return or refund procedure (3-year deadline).</li></ul>
<p><strong>Practical tip:</strong> expats with high salaries and families almost always have actual costs above the source tax flat allowances – the NOV is their biggest lever.</p>"""),
 ("Leaving and returning: blocking periods and lump sums",
  """<p>When you leave to a DTT country you can generally withdraw your <strong>2nd pillar in cash</strong> (full vested benefits); when leaving to an EU/EFTA country without self-employment, only the BVG old-age accounts, not the extra-mandatory part. <strong>Pillar 3a</strong> stays blocked until ordinary retirement age (exception: definitive departure from Switzerland – then withdrawal is possible, subject to source tax on the lump sum).</p>
<p>The move itself is tax-free – provided you were not predominantly tax-liable in Switzerland during the last 5 years and the properties remain private assets. Selling shortly after leaving risks retroactive Swiss taxation.</p>
<p><strong>Practical tip:</strong> plan lump-sum withdrawals and sales before you leave – after departure the rules of your new country apply, and Switzerland scrutinises indirect routes.</p>"""),
 ("In short",
  """<ul><li>Swiss residence = unlimited tax liability on worldwide income and wealth – declaring foreign values is your duty.</li>
<li>B permit: source tax with flat tariffs; C permit: ordinary assessment.</li>
<li>From CHF 120,000 gross salary: mandatory retroactive ordinary assessment (NOV) – below that, request it voluntarily and reclaim deductions.</li>
<li>Biggest levers: 3a (7,258), pension buy-in, actual professional expenses via NOV, childcare up to 25,000 per child.</li>
<li>Departure: 2nd pillar mostly withdrawable, 3a blocked until emigration – timing decides.</li>
<li>This is general information, not individual advice – have your situation reviewed by a fiduciary or tax advisor with DTT experience (free initial review via kontakt.html).</li></ul>"""),
]

# ---------------- French ----------------
fr_title = "Expats en Suisse : impôts, impôt à la source et le piège des 120 000 francs"
fr_meta = "Installation en Suisse en tant qu'expat : ce qu'il faut savoir en 2026 sur l'impôt à la source, la taxation ordinaire ultérieure (TOU) obligatoire dès 120 000 francs de salaire brut, la déclaration du patrimoine mondial et les principales déductions."
fr_sections = [
 ("Qui devient résident fiscal en Suisse",
  """<p>Dès que vous établissez votre domicile en Suisse – avec une autorisation B ou C – vous êtes soumis à une <strong>obligation fiscale illimitée</strong> : vos <strong>revenu et fortune mondiaux</strong> sont imposables, y compris comptes, portefeuilles et biens immobiliers à l'étranger. Le critère décisif est le centre réel de vos intérêts, non la nationalité.</p>
<p>Les séjours courts sans domicile (p. ex. détachement de moins de 90 jours) restent en général imposables dans le pays d'origine ; mais un séjour de plus de 30 jours avec activité lucrative, ou de plus de 90 jours au total, crée en règle générale une obligation fiscale en Suisse. Les conventions de double imposition (CDI) répartissent les droits d'imposition – elles ne remplacent pas votre obligation de déclarer en Suisse, elles limitent seulement ce que la Suisse peut imposer.</p>
<p><strong>Conseil pratique :</strong> annoncez-vous à l'office communal de l'impôt à votre arrivée. L'employeur gère l'impôt à la source – mais la déclaration des valeurs étrangères est uniquement votre responsabilité.</p>"""),
 ("L'impôt à la source : le régime de départ des titulaires d'un permis B",
  """<p>Avec une autorisation de séjour B, le salaire et la plupart des revenus sont <strong>prélevés à la source</strong> : l'employeur déduit l'impôt du salaire brut et le reverse à l'autorité fiscale. Vous recevez le salaire net – sans d'abord déposer de déclaration. Le barème appliqué inclut des forfaits pour les déductions pour enfants, la déduction sociale et les frais professionnels usuels.</p>
<p>Avec une <strong>autorisation d'établissement C</strong>, vous passez à la taxation ordinaire : vous déposez la déclaration habituelle et payez après taxation.</p>
<p>À savoir : le barème d'impôt à la source est un <strong>forfait</strong>. Les coûts effectifs – frais professionnels élevés, formations, maladies, assurances – n'y figurent pour la plupart pas. C'est exactement là que beaucoup d'expats laissent de l'argent.</p>"""),
 ("Le piège des 120 000 : la taxation ordinaire ultérieure obligatoire",
  """<p>Si un contribuable soumis à l'impôt à la source atteint un <strong>revenu brut annuel d'au moins 120 000 francs</strong> (avant déductions ; annualisé en cas d'année partielle), une <strong>taxation ordinaire ultérieure (TOU)</strong> est obligatoire (art. 89 LIFD, art. 33a LHID) : vous devez déposer une déclaration complète portant sur le revenu et la fortune mondiaux. L'impôt déjà perçu à la source est imputé.</p>
<p>En dessous de 120 000, vous pouvez <strong>demander la TOU volontairement</strong> – en général jusqu'au 31 mars de l'année suivante (art. 89a LIFD). Cela vaut presque toujours le coup si vos frais effectifs dépassent les forfaits du barème : rachats LPP, pilier 3a, frais professionnels effectifs, garde d'enfants par des tiers, intérêts hypothécaires à l'étranger.</p>
<p><strong>Conseil pratique :</strong> vérifiez chaque année si vous êtes au-dessus ou en dessous de 120 000 – et utilisez activement la TOU volontaire sous le seuil. Ne pas la demander, c'est souvent renoncer à plusieurs milliers de francs.</p>"""),
 ("Déclarer la fortune mondiale : comptes, portefeuilles, crypto, immobilier",
  """<p>La Suisse impose l'ensemble de votre fortune – aussi à l'étranger : comptes bancaires, portefeuilles titres, cryptomonnaies, biens immobiliers. Inscrivez tout à l'état des titres ; les biens immobiliers étrangers à leur valeur justifiée (en général la valeur vénale de l'avis fiscal étranger).</p>
<p>Les revenus immobiliers étrangers (valeur locative ou loyers) sont imposables en Suisse – la Suisse accorde le plus souvent une exonération avec réserve de progressivité, selon la CDI. La crypto relève de la fortune privée : l'avoir oui (impôt sur la fortune), les gains privés de aliénation en règle générale exonérés.</p>
<p><strong>Conseil pratique :</strong> l'échange automatique de renseignements (EAR/CRS) capte déjà les comptes étrangers aujourd'hui ; le CARF l'étendra aux crypto dès 2027/2028. Les lacunes dans les déclarations se remarquent – tout déclarer dès le départ est la voie la moins chère.</p>"""),
 ("Les principales déductions pour les expats en 2026",
  """<ul><li><strong>Pilier 3a :</strong> jusqu'à 7 258 francs (avec caisse de pension) ou 20 % du revenu de l'activité lucrative, max. 36 288 francs (sans) – entièrement déductible ; dès 2026, des versements ultérieurs pour les années lacunaires sont possibles.</li>
<li><strong>Rachat LPP :</strong> les rachats volontaires dans le 2e pilier réduisent le revenu imposable – respecter le blocage de 3 ans avant tout retrait anticipé (art. 79b Cst.).</li>
<li><strong>Frais professionnels :</strong> déduction trajets domicile-travail (max. 8 000 francs Confédération), formations, frais supplémentaires de repas – seulement forfaitaires dans l'impôt à la source, déductibles en réel via la TOU.</li>
<li><strong>Garde d'enfants par des tiers :</strong> jusqu'à 25 000 francs par enfant (Confédération, art. 33 al. 3 let. c LIFD) pour les enfants de moins de 16 ans – crèche, accueil extrascolaire, part de garde de la personne au pair.</li>
<li><strong>Impôt anticipé :</strong> 35 % sur les intérêts bancaires suisses et les dividendes – récupérable via la déclaration ou la procédure de restitution (délai de 3 ans).</li></ul>
<p><strong>Conseil pratique :</strong> les expats à haut salaire avec famille ont presque toujours des frais effectifs supérieurs aux forfaits du barème – la TOU est leur principal levier.</p>"""),
 ("Départ et retour : blocages et prestations en capital",
  """<p>En cas de départ vers un pays lié par une CDI, vous pouvez en principe toucher votre <strong>2e pilier en espèces</strong> (prestation de libre passage intégrale) ; vers un pays UE/AELE sans activité indépendante, seuls les avoirs de vieillesse LPP, pas la partie surobligatoire. Le <strong>3e pilier</strong> reste bloqué jusqu'à l'âge ordinaire de la retraite (exception : départ définitif de Suisse – alors un retrait est possible, avec impôt à la source sur la prestation en capital).</p>
<p>Le départ lui-même est sans imposition – à condition de ne pas avoir été principalement soumis à l'impôt en Suisse durant les 5 dernières années et que les biens restent de la fortune privée. Vendre peu après le départ risque une imposition rétroactive en Suisse.</p>
<p><strong>Conseil pratique :</strong> planifiez retraits en capital et ventes avant le départ – après, ce sont les règles du nouveau pays de domicile qui s'appliquent, et la Suisse examine de près les montages indirects.</p>"""),
 ("En bref",
  """<ul><li>Domicile en Suisse = obligation fiscale illimitée sur le revenu et la fortune mondiaux – déclarer les valeurs étrangères est votre devoir.</li>
<li>Permis B : impôt à la source avec barèmes forfaitaires ; permis C : taxation ordinaire.</li>
<li>Dès 120 000 francs de salaire brut : taxation ordinaire ultérieure (TOU) obligatoire – en dessous, demandez-la volontairement et récupérez vos déductions.</li>
<li>Principaux leviers : 3a (7 258), rachat LPP, frais professionnels effectifs via TOU, garde d'enfants jusqu'à 25 000 par enfant.</li>
<li>Départ : 2e pilier en grande partie retirable, 3e pilier bloqué jusqu'à l'expatriation – le timing décide.</li>
<li>Ceci est une information générale, pas un conseil individuel – faites examiner votre situation par un fiduciaire ou conseiller fiscal expérimenté en CDI (premier entretien gratuit via kontakt.html).</li></ul>"""),
]

# ---------------- Italian ----------------
it_title = "Expats in Svizzera: imposte, imposta alla fonte e la trappola dei 120'000 franchi"
it_meta = "Trasferimento in Svizzera come expat: cosa sapere nel 2026 sull'imposta alla fonte, sulla tassazione ordinaria successiva obbligatoria da 120'000 franchi di salario lordo, sulla dichiarazione del patrimonio mondiale e sulle principali deduzioni."
it_sections = [
 ("Chi diventa fiscalmente residente in Svizzera",
  """<p>Con il trasferimento del domicilio in Svizzera – con permesso B o C – siete soggetti a <strong>imposizione illimitata</strong>: sono tassati il <strong>reddito e la sostanza mondiali</strong>, quindi anche conti, portafogli e immobili all'estero. Il criterio decisivo è il centro effettivo degli interessi, non la cittadinanza.</p>
<p>Soggiorni brevi senza domicilio (p. es. distacchi sotto 90 giorni) restano di norma tassati nel Paese d'origine; ma un soggiorno di oltre 30 giorni con attività lucrativa, o oltre 90 giorni in totale, crea in genere un'obbligazione fiscale in Svizzera. Le convenzioni contro la doppia imposizione (CDI) ripartiscono i diritti d'imposta – non sostituiscono l'obbligo di dichiarare in Svizzera, limitano solo ciò che la Svizzera può tassare.</p>
<p><strong>Consiglio pratico:</strong> annunciatevi all'ufficio comunale delle imposte al vostro arrivo. Il datore gestisce l'imposta alla fonte – ma la dichiarazione dei valori esteri è soltanto responsabilità vostra.</p>"""),
 ("Imposta alla fonte: il sistema di partenza per i titolari di permesso B",
  """<p>Con permesso di dimora B, il salario e la maggior parte dei redditi sono <strong>tassati alla fonte</strong>: il datore deduce l'imposta dal salario lordo e la versa all'autorità fiscale. Ricevete il salario netto – senza presentare una dichiarazione. La tariffa applicata include forfette per deduzioni per figli, deduzione sociale e spese professionali usuali.</p>
<p>Con il <strong>permesso di domicilio C</strong> si passa alla tassazione ordinaria: presentate la normale dichiarazione d'imposte e pagate secondo la tassazione.</p>
<p>Da sapere: la tariffa dell'imposta alla fonte è una <strong>forfetta</strong>. I costi effettivi – spese professionali elevate, formazioni, malattie, assicurazioni – per lo più non vi figurano. È esattamente lì che molti expat lasciano denaro.</p>"""),
 ("La trappola dei 120'000: tassazione ordinaria successiva obbligatoria",
  """<p>Se un contribuente soggetto all'imposta alla fonte raggiunge un <strong>reddito lordo annuo di almeno 120'000 franchi</strong> (al lordo delle deduzioni; annualizzato in caso di anno parziale), scatta la <strong>tassazione ordinaria successiva (TOS)</strong> obbligatoria (art. 89 LI, art. 33a LITD): dovete presentare una dichiarazione completa su reddito e sostanza mondiali. L'imposta già versata alla fonte viene accreditata.</p>
<p>Sotto i 120'000 potete <strong>richiedere la TOS volontariamente</strong> – di norma fino al 31 marzo dell'anno successivo (art. 89a LI). Conviene quasi sempre se i vostri costi effettivi superano le forfette tariffali: acquisti nella cassa pensione, pilastro 3a, spese professionali effettive, cura extrafamiliare dei figli, interessi ipotecari all'estero.</p>
<p><strong>Consiglio pratico:</strong> verificate ogni anno se siete sopra o sotto i 120'000 – e sotto la soglia chiedete attivamente la TOS volontaria. Rinunciarvi significa spesso regalare parecchi migliaia di franchi.</p>"""),
 ("Dichiarare la sostanza mondiale: conti, portafogli, crypto, immobili",
  """<p>La Svizzera tassa l'intera vostra sostanza – anche all'estero: conti bancari, portafogli titoli, criptovalute, immobili. Iscrivete tutto nell'elenco dei titoli; gli immobili esteri al valore documentato (di norma il valore di mercato secondo la fattura fiscale estera).</p>
<p>I redditi da immobili esteri (valore locativo o fitti) sono imponibili in Svizzera – la Svizzera concede di norma un'esenzione con riserva di progressione, secondo la CDI. Le crypto valgono come sostanza privata: consistenza sì (imposta sulla sostanza), utili di alienazione privati di regola esenti.</p>
<p><strong>Consiglio pratico:</strong> lo scambio automatico di informazioni (SAI/CRS) già oggi capta i conti esteri; dal 2027/2028 il CARF estenderà la cosa alle crypto. Le lacune dichiarative emergono – dichiarare tutto fin dall'inizio è la via più economica.</p>"""),
 ("Le principali deduzioni per expat nel 2026",
  """<ul><li><strong>Pilastro 3a:</strong> fino a 7'258 franchi (con cassa pensione) o 20% del reddito da attività lucrativa, max 36'288 franchi (senza) – interamente deducibili; dal 2026 sono possibili versamenti recuperativi per gli anni lacunosi.</li>
<li><strong>Acquisto nella cassa pensione:</strong> gli acquisti volontari nel 2° pilastro riducono il reddito imponibile – rispettare il blocco di 3 anni prima di ogni prelievo anticipato (art. 79b Cost.).</li>
<li><strong>Spese professionali:</strong> deduzione tragitto casa-lavoro (max 8'000 franchi Confederazione), formazioni, spese supplementari di vitto – solo forfettarie nell'imposta alla fonte, deducibili in concreto via TOS.</li>
<li><strong>Cura extrafamiliare dei figli:</strong> fino a 25'000 franchi per figlio (Confederazione, art. 33 cpv. 3 lett. c LI) per figli sotto i 16 anni – asilo nido, accudimento extrascolastico, quote di accudimento dell'au pair.</li>
<li><strong>Imposta preventiva:</strong> 35% su interessi bancari svizzeri e dividendi – rimborsabile tramite dichiarazione o procedura di restituzione (termine 3 anni).</li></ul>
<p><strong>Consiglio pratico:</strong> gli expat con salari elevati e famiglia hanno quasi sempre costi effettivi superiori alle forfette della tariffa – la TOS è la loro leva più importante.</p>"""),
 ("Partenza e rientro: blocchi e prestazioni in capitale",
  """<p>In caso di partenza verso un Paese legato da una CDI potete in principio prelevare il <strong>2° pilastro in contanti</strong> (intera prestazione di libero passaggio); verso un Paese UE/AELS senza attività indipendente, solo gli averi di vecchiaia LPP, non la parte sovraobbligatoria. Il <strong>3° pilastro</strong> resta bloccato fino all'età ordinaria di pensionamento (eccezione: partenza definitiva dalla Svizzera – allora il prelievo è possibile, con imposta alla fonte sulla prestazione in capitale).</p>
<p>La partenza in sé è esente – a condizione di non essere stati principalmente soggetti a imposizione illimitata in Svizzera negli ultimi 5 anni e che gli immobili restino sostanza privata. Vendere poco dopo la partenza rischia un'imposta retroattiva in Svizzera.</p>
<p><strong>Consiglio pratico:</strong> pianificate prelievi in capitale e vendite prima della partenza – dopo valgono le regole del nuovo Stato di domicilio, e la Svizzera esamina attentamente i costrutti indiretti.</p>"""),
 ("In breve",
  """<ul><li>Domicilio in Svizzera = imposizione illimitata su reddito e sostanza mondiali – dichiarare i valori esteri è un vostro dovere.</li>
<li>Permesso B: imposta alla fonte con tariffe forfettarie; permesso C: tassazione ordinaria.</li>
<li>Da 120'000 franchi di salario lordo: tassazione ordinaria successiva (TOS) obbligatoria – sotto la soglia, chiedetela volontariamente e recuperate le deduzioni.</li>
<li>Leve principali: 3a (7'258), acquisto cassa pensione, spese professionali effettive via TOS, cura figli fino a 25'000 per figlio.</li>
<li>Partenza: 2° pilastro in gran parte prelevabile, 3° pilastro bloccato fino all'emigrazione – decide il tempismo.</li>
<li>Queste sono informazioni generali, non una consulenza individuale – fate esaminare la vostra situazione da un fiduciario o consulente fiscale con esperienza CDI (primo colloquio gratuito tramite kontakt.html).</li></ul>"""),
]

for lang, title, meta, sections in [("de", de_title, de_meta, de_sections),
                                    ("en", en_title, en_meta, en_sections),
                                    ("fr", fr_title, fr_meta, fr_sections),
                                    ("it", it_title, it_meta, it_sections)]:
    build(lang, SLUG, title, meta, sections, related=RELATED)
print("done")
