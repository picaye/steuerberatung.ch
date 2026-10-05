#!/usr/bin/env python3
"""Build transparenzregister-tjpg-meldepflicht in 4 languages via article_template.build()."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
os.chdir('/workspace/steuerberatung')
sys.path.insert(0, '/workspace/steuerberatung/scripts')
from article_template import build

SLUG = "transparenzregister-tjpg-meldepflicht"
RELATED = ["mwst-100k-pflicht-schweiz.html", "verrechnungssteuer-schweiz-35-prozent.html", "erbschaftssteuer-schenkungssteuer-schweiz.html"]

DE = [
("Was sich am 1. Oktober 2026 geändert hat",
"""<p>Mit dem Bundesgesetz über die Transparenz juristischer Personen (TJPG, SR 955.3) und seiner Verordnung (TJPV, SR 955.31) ist am <strong>1. Oktober 2026</strong> das neue <strong>Eidgenössische Transparenzregister</strong> in Kraft getreten. Aktiengesellschaften und GmbH (und weitere Gesellschaftsformen) müssen ihre wirtschaftlich berechtigten Personen neu dem <strong>Bundesamt für Justiz (BJ)</strong> melden – Art. 20 TJPG weist die Führung des Registers ausdrücklich dem BJ zu.</p>
<p>Die bisherige Pflicht aus dem Obligationenrecht, ein <em>internes</em> Verzeichnis der wirtschaftlich berechtigten Personen zu führen (Art. 697j und 790a OR), wird durch die Meldepflicht ans Register ersetzt. Wichtig für die Praxis: Das nach altem Recht erstellte interne Verzeichnis müssen AG und GmbH noch <strong>während zehn Jahren</strong> nach Inkrafttreten aufbewahren (Art. 50 TJPG).</p>"""),
("Wer ist betroffen – und wer nicht",
"""<p>Meldepflichtig sind nach Art. 2 TJPG insbesondere: <strong>Aktiengesellschaften (AG)</strong>, Kommanditaktiengesellschaften, <strong>Gesellschaften mit beschränkter Haftung (GmbH)</strong>, Genossenschaften, SICAV, SICAF und Kommanditgesellschaften für kollektive Kapitalanlagen. Auch ausländische juristische Personen mit eingetragener Zweigniederlassung, tatsächlicher Verwaltung in der Schweiz oder Schweizer Grundbesitz fallen unter das Gesetz. Für Trusts mit Sitz oder Verwaltung in der Schweiz gelten eigene Pflichten der Trustees (Art. 15/16 TJPG).</p>
<p>Ausnahmen sieht Art. 3 TJPG vor: börsenkotierte Gesellschaften (und mehrheitlich von ihnen gehaltene Tochtergesellschaften), Vorsorgeeinrichtungen sowie Rechtseinheiten, die zu mindestens 75 % in der Hand von Gemeinwesen sind.</p>"""),
("Wer gilt als wirtschaftlich berechtigte Person?",
"""<p>Art. 4 TJPG definiert: wirtschaftlich berechtigt ist die natürliche Person, die eine Gesellschaft letztendlich kontrolliert – weil sie direkt oder indirekt, allein oder in gemeinsamer Absprache mit Dritten, <strong>mindestens 25 Prozent des Kapitals oder der Stimmen</strong> hält, oder die Kontrolle auf andere Weise ausübt. Kann niemand so identifiziert werden, gilt subsidiär das <strong>oberste Mitglied des leitenden Organs</strong> (also etwa der CEO oder Präsident) als wirtschaftlich berechtigte Person.</p>
<p>Die Gesellschaft muss die Person identifizieren und ihre Angaben überprüfen, bevor sie meldet (Art. 7 TJPG). Gemeldet werden: Name, Vorname, Geburtsdatum, Staatsangehörigkeit, Wohnsitzgemeinde und -staat sowie Art und Umfang der ausgeübten Kontrolle (Art. 9 Abs. 1 TJPG).</p>"""),
("Die Fristen nach Art. 51 TJPG – gestaffelt, nicht einheitlich",
"""<p>Bestehende Gesellschaften haben je nach Konstellation unterschiedlich Zeit. Massgebend sind Monate bzw. Jahre <em>nach dem Inkrafttreten am 1. Oktober 2026</em>; die berechneten Stichtage in Klammern:</p>
<ul>
<li><strong>Alle wirtschaftlich Berechtigten bereits im Handelsregister</strong> (als Gesellschafter oder Organ eingetragen): <strong>2 Jahre</strong> – spätestens bis 1. Oktober 2028 (Art. 51 Abs. 2).</li>
<li><strong>AG mit ordentlicher Revision</strong>: <strong>3 Monate</strong> – spätestens bis 1. Januar 2027 (Art. 51 Abs. 3 Bst. a).</li>
<li><strong>Andere Gesellschaften mit ordentlicher Revision</strong>: <strong>4 Monate</strong> – spätestens bis 1. Februar 2027 (Art. 51 Abs. 3 Bst. b).</li>
<li><strong>AG ohne Pflicht zur ordentlichen Revision</strong>: <strong>5 Monate</strong> – spätestens bis 1. März 2027 (Art. 51 Abs. 3 Bst. c).</li>
<li><strong>Übrige Gesellschaften ohne eingeschränkte Revisionspflicht und andere juristische Personen</strong>: <strong>6 Monate</strong> – spätestens bis 1. April 2027 (Art. 51 Abs. 3 Bst. d).</li>
</ul>
<p>Zusätzlich: Wer nach Inkrafttreten den Handelsregistereintrag ändert, muss innert <strong>eines Monats nach dieser Änderung</strong> melden (Art. 51 Abs. 1). <strong>Neugründungen</strong> melden innert eines Monats nach der Eintragung ins Handelsregister (Art. 9 Abs. 4). <strong>Änderungen</strong> einer eingetragenen Tatsache sind innert eines Monats nach Kenntnis zu melden (Art. 10). Wer alle Berechtigten im Handelsregister eingetragen hat, kann die Meldung auch über das Handelsregisteramt erstatten (Art. 11).</p>"""),
("Was passiert, wenn man nicht meldet?",
"""<p>Die Sanktionen sitzen dort, wo es wehtut: Wer die Meldepflicht ans Transparenzregister <strong>vorsätzlich verletzt oder falsche Angaben macht</strong>, riskiert eine <strong>Busse bis zu CHF 500'000</strong> (Art. 43 TJPG). Wer sich einer rechtskräftigen Verfügung der Kontrollstelle widersetzt, wird mit Busse bis zu <strong>CHF 100'000</strong> bedroht (Art. 44 TJPG). Die Verfolgung richtet sich nach dem Verwaltungsstrafrecht (Art. 45).</p>
<p>Zudem prüft die registerführende Behörde nach Ablauf der Übergangsfristen, ob die Meldepflicht erfüllt ist, und mahnt die Gesellschaft andernfalls unter Hinweis auf die Folgen (Art. 52 Abs. 2 TJPG). Finanzintermediäre müssen dem Register gemäss Art. 30 TJPG Unterschiede melden, die ihnen auffallen.</p>"""),
("Wer darf ins Register schauen?",
"""<p>Das Transparenzregister ist <strong>nicht öffentlich</strong> einsehbar. Online-Abrufrechte haben die Kontrollstelle und ihre Beauftragten (Art. 25), Strafverfolgungs- und Steuerbehörden, die Meldestelle für Geldwäscherei und weitere Behörden (Art. 26) sowie <strong>Finanzintermediäre und Berater nach dem GwG</strong> zur Erfüllung ihrer Sorgfaltspflichten (Art. 27). Die Gesellschaft selbst kann jederzeit Bestätigung und Auszug verlangen (Art. 28).</p>"""),
("Konkret jetzt zu tun",
"""<ol>
<li>Prüfen, ob Ihre AG/GmbH/Genossenschaft unter Art. 2 TJPG fällt (Ausnahmen: Art. 3).</li>
<li>Wirtschaftlich berechtigte Personen identifizieren (25 %-Schwelle, Kontrollkette durchdenken) und deren Daten dokumentieren.</li>
<li>Frist nach Art. 51 ermitteln – kleine GmbH ohne Revisionsstelle: <strong>sechs Monate bis 1. April 2027</strong>; kleine AG ohne ordentliche Revision: <strong>fünf Monate bis 1. März 2027</strong>.</li>
<li>Meldung elektronisch ans Transparenzregister des BJ (oder via Handelsregisteramt, Art. 11) senden; das oberste Mitglied des leitenden Organs ist verantwortlich (Art. 12).</li>
<li>Internes Verzeichnis nach altem Recht zehn Jahre aufbewahren (Art. 50) und Änderungen innert Monatsfrist nachmelden (Art. 10).</li>
</ol>
<p class="muted">Dies ist allgemeine Information, keine Rechts- oder Steuerberatung. Massgebend ist allein der Gesetzestext (fedlex SR 955.3 / 955.31).</p>"""),
]

EN = [
("What changed on 1 October 2026",
"""<p>The Federal Act on the Transparency of Legal Entities (TJPG, SR 955.3) and its ordinance (TJPV, SR 955.31) entered into force on <strong>1 October 2026</strong>, creating the new <strong>Swiss Federal Transparency Register</strong>. Stock corporations (AG) and limited liability companies (GmbH) — among others — must now report their beneficial owners to the <strong>Federal Office of Justice (FOJ)</strong>; Art. 20 TJPG expressly assigns the register to the FOJ.</p>
<p>The old duty under the Code of Obligations to keep an <em>internal</em> register of beneficial owners (Art. 697j and 790a CO) is replaced by the reporting duty. In practice: AG and GmbH must still retain the internal register created under the old law for <strong>ten years</strong> after entry into force (Art. 50 TJPG).</p>"""),
("Who is covered — and who is not",
"""<p>Art. 2 TJPG covers in particular: <strong>stock corporations (AG)</strong>, partnership companies limited by shares, <strong>limited liability companies (GmbH)</strong>, cooperatives, SICAV, SICAF and limited partnerships for collective investments. Foreign legal entities with a registered Swiss branch, their actual administration in Switzerland, or Swiss real estate are also caught. Trustees of trusts administered from Switzerland have their own duties (Art. 15/16 TJPG).</p>
<p>Art. 3 TJPG exempts listed companies (and majority-owned subsidiaries), occupational pension institutions, and entities at least 75 % owned by public bodies.</p>"""),
("Who counts as a beneficial owner?",
"""<p>Art. 4 TJPG: the beneficial owner is the natural person who ultimately controls the company — directly or indirectly, alone or acting in concert with others, holding <strong>at least 25 % of the capital or votes</strong>, or exercising control by other means. If no such person can be identified, the <strong>top member of the management body</strong> (e.g. the CEO) is deemed the beneficial owner.</p>
<p>The company must identify and verify each beneficial owner before reporting (Art. 7). The report contains: first and last name, date of birth, nationality, municipality and country of residence, and the nature and extent of control exercised (Art. 9 para. 1 TJPG).</p>"""),
("The deadlines under Art. 51 TJPG — staggered, not one size fits all",
"""<p>Existing companies get different grace periods depending on their situation. The statutory clock runs from <em>entry into force on 1 October 2026</em>; the computed cut-off dates are in brackets:</p>
<ul>
<li><strong>All beneficial owners already in the commercial register</strong> (as shareholders or officers): <strong>2 years</strong> — by 1 October 2028 at the latest (Art. 51 para. 2).</li>
<li><strong>AG with ordinary audit</strong>: <strong>3 months</strong> — by 1 January 2027 (Art. 51 para. 3 lit. a).</li>
<li><strong>Other companies with ordinary audit</strong>: <strong>4 months</strong> — by 1 February 2027 (lit. b).</li>
<li><strong>AG not requiring an ordinary audit</strong>: <strong>5 months</strong> — by 1 March 2027 (lit. c).</li>
<li><strong>Other companies without a limited-audit duty and other legal entities</strong>: <strong>6 months</strong> — by 1 April 2027 (lit. d).</li>
</ul>
<p>On top: any change to the commercial register entry after entry into force triggers a report <strong>within one month of that change</strong> (Art. 51 para. 1). <strong>New incorporations</strong> report within one month of registration (Art. 9 para. 4). <strong>Changes</strong> to registered facts must be reported within one month of becoming aware (Art. 10). Companies whose owners are all in the commercial register may file through the commercial register office instead (Art. 11).</p>"""),
("What happens if you fail to report?",
"""<p>The sanctions are substantial: anyone who <strong>intentionally breaches the reporting duty or provides false information</strong> risks a fine of up to <strong>CHF 500'000</strong> (Art. 43 TJPG). Anyone who wilfully disregards a legally binding order of the control body faces a fine of up to <strong>CHF 100'000</strong> (Art. 44 TJPG). Prosecution follows administrative criminal law (Art. 45).</p>
<p>After the transition periods, the register authority checks compliance and reminds defaulting companies of the consequences (Art. 52 para. 2). Financial intermediaries must report discrepancies they spot to the register (Art. 30 TJPG).</p>"""),
("Who can look into the register?",
"""<p>The Transparency Register is <strong>not public</strong>. Online access is granted to the control body and its mandatees (Art. 25), criminal prosecution and tax authorities, the money-laundering reporting office and other authorities (Art. 26), and <strong>financial intermediaries and advisers under the AML Act</strong> for their due-diligence duties (Art. 27). The company itself can request confirmation and an extract at any time (Art. 28).</p>"""),
("What to do now",
"""<ol>
<li>Check whether your AG/GmbH/cooperative falls under Art. 2 TJPG (exemptions: Art. 3).</li>
<li>Identify the beneficial owners (25 % threshold, think through control chains) and document their data.</li>
<li>Determine your Art. 51 deadline — small GmbH without an audit body: <strong>six months, ending 1 April 2027</strong>; small AG without an ordinary audit: <strong>five months, ending 1 March 2027</strong>.</li>
<li>File electronically with the FOJ's Transparency Register (or via the commercial register office, Art. 11); the top member of the management body is responsible (Art. 12).</li>
<li>Keep the old internal register for ten years (Art. 50) and report changes within one month (Art. 10).</li>
</ol>
<p class="muted">General information only — not legal or tax advice. The sole authoritative text is the statute (fedlex SR 955.3 / 955.31).</p>"""),
]

FR = [
("Ce qui a changé le 1er octobre 2026",
"""<p>La loi fédérale sur la transparence des personnes morales (LTPM, RS 955.3) et son ordonnance (OTPM, RS 955.31) sont entrées en vigueur le <strong>1er octobre 2026</strong>, créant le nouveau <strong>registre fédéral de la transparence</strong>. Les sociétés anonymes (SA) et les Sàrl — entre autres — doivent désormais annoncer leurs ayants droit économiques à l'<strong>Office fédéral de la justice (OFJ)</strong> ; l'art. 20 LTPM confie expressément la tenue du registre à l'OFJ.</p>
<p>L'ancienne obligation du code des obligations de tenir un registre <em>interne</em> des ayants droit économiques (art. 697j et 790a CO) est remplacée par l'obligation d'annonce. En pratique : les SA et Sàrl doivent encore conserver le registre interne établi sous l'ancien droit pendant <strong>dix ans</strong> après l'entrée en vigueur (art. 50 LTPM).</p>"""),
("Qui est concerné — et qui ne l'est pas",
"""<p>L'art. 2 LTPM vise notamment : les <strong>sociétés anonymes (SA)</strong>, les sociétés en commandite par actions, les <strong>sociétés à responsabilité limitée (Sàrl)</strong>, les coopératives, les SICAV, les SICAF et les commandites pour placements collectifs. Les personnes morales étrangères avec succursale inscrite, administration effective en Suisse ou immeuble suisse sont aussi visées. Les trustees de trusts administrés depuis la Suisse ont des obligations propres (art. 15/16 LTPM).</p>
<p>L'art. 3 LTPM exclut les sociétés cotées (et leurs filiales détenues à plus de 75 %), les institutions de prévoyance et les entités détenues à au moins 75 % par des collectivités publiques.</p>"""),
("Qui est un ayant droit économique ?",
"""<p>Art. 4 LTPM : est ayant droit économique la personne physique qui contrôle en dernière instance la société — directement ou indirectement, seule ou de concert avec des tiers, détenant <strong>au moins 25 % du capital ou des voix</strong>, ou exerçant le contrôle d'une autre manière. Si personne ne répond à ce critère, le <strong>membre le plus élevé de l'organe de direction</strong> (p. ex. le CEO) est réputé ayant droit économique.</p>
<p>La société doit identifier et vérifier chaque ayant droit avant d'annoncer (art. 7). L'annonce contient : prénom et nom, date de naissance, nationalité, commune et pays de domicile, ainsi que la nature et l'étendue du contrôle exercé (art. 9 al. 1 LTPM).</p>"""),
("Les délais selon l'art. 51 LTPM — échelonnés, pas uniformes",
"""<p>Les sociétés existantes bénéficient de délais différents selon leur situation. Le délai légal court à partir de <em>l'entrée en vigueur du 1er octobre 2026</em> ; les échéances calculées figurent entre parenthèses :</p>
<ul>
<li><strong>Tous les ayants droit déjà inscrits au registre du commerce</strong> (comme associés ou organes) : <strong>2 ans</strong> — au plus tard le 1er octobre 2028 (art. 51 al. 2).</li>
<li><strong>SA avec révision ordinaire</strong> : <strong>3 mois</strong> — au plus tard le 1er janvier 2027 (art. 51 al. 3 let. a).</li>
<li><strong>Autres sociétés avec révision ordinaire</strong> : <strong>4 mois</strong> — au plus tard le 1er février 2027 (let. b).</li>
<li><strong>SA sans révision ordinaire obligatoire</strong> : <strong>5 mois</strong> — au plus tard le 1er mars 2027 (let. c).</li>
<li><strong>Autres sociétés sans révision restreinte obligatoire et autres personnes morales</strong> : <strong>6 mois</strong> — au plus tard le 1er avril 2027 (let. d).</li>
</ul>
<p>En outre : toute modification de l'inscription au registre du commerce après l'entrée en vigueur déclenche une annonce <strong>dans le mois suivant cette modification</strong> (art. 51 al. 1). Les <strong>nouvelles inscriptions</strong> annoncent dans le mois de l'inscription au registre du commerce (art. 9 al. 4). Les <strong>modifications</strong> de faits inscrits doivent être annoncées dans le mois où la société en a connaissance (art. 10). Les sociétés dont tous les ayants droit figurent au registre du commerce peuvent annoncer via l'office du registre du commerce (art. 11).</p>"""),
("Que risque-t-on en cas de non-annonce ?",
"""<p>Les sanctions sont sévères : quiconque <strong>viole intentionnellement l'obligation d'annonce ou fournit de fausses indications</strong> s'expose à une amende pouvant atteindre <strong>500 000 francs</strong> (art. 43 LTPM). Quiconque désobéit intentionnellement à une décision passée en force de l'organe de contrôle risque une amende jusqu'à <strong>100 000 francs</strong> (art. 44 LTPM).</p>
<p>À l'échéance des délais transitoires, l'autorité du registre vérifie le respect de l'obligation et rappelle aux sociétés défaillantes les conséquences de l'inexécution (art. 52 al. 2). Les intermédiaires financiers doivent annoncer les divergences constatées au registre (art. 30 LTPM).</p>"""),
("Qui peut consulter le registre ?",
"""<p>Le registre de la transparence n'est <strong>pas public</strong>. L'accès en ligne est réservé à l'organe de contrôle et à ses mandataires (art. 25), aux autorités pénales et fiscales, au service de communication financière et à d'autres autorités (art. 26), ainsi qu'aux <strong>intermédiaires financiers et conseillers au sens de la LBA</strong> pour leurs obligations de diligence (art. 27). La société elle-même peut exiger une attestation et un extrait (art. 28).</p>"""),
("À faire maintenant",
"""<ol>
<li>Vérifier si votre SA/Sàrl/coopérative tombe sous l'art. 2 LTPM (exceptions : art. 3).</li>
<li>Identifier les ayants droit économiques (seuil de 25 %, réfléchir aux chaînes de contrôle) et documenter leurs données.</li>
<li>Déterminer votre délai selon l'art. 51 — petite Sàrl sans office de révision : <strong>six mois, échéance 1er avril 2027</strong> ; petite SA sans révision ordinaire : <strong>cinq mois, échéance 1er mars 2027</strong>.</li>
<li>Annoncer électroniquement au registre de l'OFJ (ou via l'office du registre du commerce, art. 11) ; le membre le plus élevé de l'organe de direction est responsable (art. 12).</li>
<li>Conserver l'ancien registre interne dix ans (art. 50) et annoncer les modifications dans le mois (art. 10).</li>
</ol>
<p class="muted">Informations générales uniquement — pas de conseil juridique ou fiscal. Seul le texte de la loi fait foi (fedlex RS 955.3 / 955.31).</p>"""),
]

IT = [
("Che cosa è cambiato il 1° ottobre 2026",
"""<p>La legge federale sulla trasparenza delle persone giuridiche (LTras, SR 955.3) e la relativa ordinanza (OLTras, SR 955.31) sono entrate in vigore il <strong>1° ottobre 2026</strong>, creando il nuovo <strong>registro federale della trasparenza</strong>. Le società anonime (SA) e le Sagl — tra l'altro — devono ora annunciare gli aventi diritto economici all'<strong>Ufficio federale di giustizia (UFG)</strong>; l'art. 20 LTras affida espressamente la gestione del registro all'UFG.</p>
<p>L'obbligo previgente dal CO di tenere un registro <em>interno</em> degli aventi diritto economici (art. 697j e 790a CO) è sostituito dall'obbligo di annuncio. In pratica: SA e Sagl devono ancora conservare il registro interno allestito secondo il vecchio diritto per <strong>dieci anni</strong> dall'entrata in vigore (art. 50 LTras).</p>"""),
("Chi è tenuto — e chi no",
"""<p>L'art. 2 LTras riguarda in particolare: <strong>società anonime (SA)</strong>, società in accomandita per azioni, <strong>società a garanzia limitata (Sagl)</strong>, cooperative, SICAV, SICAF e accomandite per capitali collettivi. Sono pure toccate le persone giuridiche estere con succursale iscritta, amministrazione effettiva in Svizzera o immobili in Svizzera. I trustee di trust amministrati dalla Svizzera hanno obblighi propri (art. 15/16 LTras).</p>
<p>L'art. 3 LTras esclude le società quotate (e le controllate detenute per oltre il 75 %), gli istituti di previdenza e le entità detenute per almeno il 75 % da enti pubblici.</p>"""),
("Chi è un avente diritto economico?",
"""<p>Art. 4 LTras: è avente diritto economico la persona fisica che controlla in ultima analisi la società — direttamente o indirettamente, da sola o di concerto con terzi, detenendo <strong>almeno il 25 per cento del capitale o dei voti</strong>, oppure esercitando il controllo in altro modo. Se nessuno soddisfa questi criteri, è considerato avente diritto economico in via sussidiaria il <strong>membro di rango più elevato dell'organo di direzione</strong> (p. es. il CEO).</p>
<p>La società deve identificare e verificare ogni avente diritto prima dell'annuncio (art. 7). L'annuncio contiene: nome e prenome, data di nascita, cittadinanza, comune e Stato di domicilio, nonché natura ed estensione del controllo esercitato (art. 9 cpv. 1 LTras).</p>"""),
("I termini secondo l'art. 51 LTras — scaglionati, non uniformi",
"""<p>Le società esistenti dispongono di termini diversi a seconda della situazione. Il termine legale decorre <em>dall'entrata in vigore del 1° ottobre 2026</em>; le scadenze calcolate sono indicate fra parentesi:</p>
<ul>
<li><strong>Tutti gli aventi diritto già iscritti nel registro di commercio</strong> (in qualità di soci o organi): <strong>2 anni</strong> — al più tardi il 1° ottobre 2028 (art. 51 cpv. 2).</li>
<li><strong>SA con revisione ordinaria</strong>: <strong>3 mesi</strong> — al più tardi il 1° gennaio 2027 (art. 51 cpv. 3 lett. a).</li>
<li><strong>Altre società con revisione ordinaria</strong>: <strong>4 mesi</strong> — al più tardi il 1° febbraio 2027 (lett. b).</li>
<li><strong>SA senza obbligo di revisione ordinaria</strong>: <strong>5 mesi</strong> — al più tardi il 1° marzo 2027 (lett. c).</li>
<li><strong>Altre società senza obbligo di revisione limitata e altre persone giuridiche</strong>: <strong>6 mesi</strong> — al più tardi il 1° aprile 2027 (lett. d).</li>
</ul>
<p>Inoltre: ogni modifica dell'iscrizione nel registro di commercio dopo l'entrata in vigore scatta un annuncio <strong>entro un mese da tale modifica</strong> (art. 51 cpv. 1). Le <strong>nuove iscrizioni</strong> annunciano entro un mese dall'iscrizione (art. 9 cpv. 4). Le <strong>modifiche</strong> dei fatti iscritti vanno annunciate entro un mese dalla loro conoscenza (art. 10). Le società i cui aventi diritto sono tutti iscritti nel registro di commercio possono annunciare tramite l'ufficio del registro di commercio (art. 11).</p>"""),
("Che rischio si corre in caso di mancata comunicazione?",
"""<p>Le sanzioni sono pesanti: chi <strong>viola intenzionalmente l'obbligo di annuncio o fornisce indicazioni false</strong> rischia una multa fino a <strong>500 000 franchi</strong> (art. 43 LTras). Chi disattende intenzionalmente una decisione passata in giudicato dell'organo di controllo rischia una multa fino a <strong>100 000 franchi</strong> (art. 44 LTras).</p>
<p>Scaduti i termini transitori, l'autorità del registro verifica l'adempimento e sollecita le società inadempienti ricordando le conseguenze (art. 52 cpv. 2). Gli intermediari finanziari devono annunciare al registro le divergenze constatate (art. 30 LTras).</p>"""),
("Chi può consultare il registro?",
"""<p>Il registro della trasparenza <strong>non è pubblico</strong>. L'accesso online è riservato all'organo di controllo e ai suoi mandati (art. 25), alle autorità penali e fiscali, al servizio di comunicazione finanziaria e ad altre autorità (art. 26), nonché agli <strong>intermediari finanziari e consulenti ai sensi della LRD</strong> per l'adempimento degli obblighi di diligenza (art. 27). La società stessa può chiedere conferma ed estratto (art. 28).</p>"""),
("Cosa fare ora",
"""<ol>
<li>Verificare se la vostra SA/Sagl/cooperativa rientra nell'art. 2 LTras (eccezioni: art. 3).</li>
<li>Identificare gli aventi diritto economici (soglia del 25 %, ripercorrere le catene di controllo) e documentarne i dati.</li>
<li>Determinare il termine secondo l'art. 51 — piccola Sagl senza ufficio di revisione: <strong>sei mesi, scadenza 1° aprile 2027</strong>; piccola SA senza revisione ordinaria: <strong>cinque mesi, scadenza 1° marzo 2027</strong>.</li>
<li>Annunciare elettronicamente al registro dell'UFG (o tramite l'ufficio del registro di commercio, art. 11); responsabile è il membro di rango più elevato dell'organo di direzione (art. 12).</li>
<li>Conservare il vecchio registro interno per dieci anni (art. 50) e annunciare le modifiche entro un mese (art. 10).</li>
</ol>
<p class="muted">Informazioni generali — non consulenza giuridica o fiscale. Fa fede unicamente il testo di legge (fedlex SR 955.3 / 955.31).</p>"""),
]

TITLES = {
 "de": "Transparenzregister TJPG: AG und GmbH müssen wirtschaftlich Berechtigte dem BJ melden – die Fristen laufen",
 "en": "Transparency register: Swiss AG and GmbH must report beneficial owners to the FOJ — the deadlines are running",
 "fr": "Registre de la transparence : les SA et Sàrl doivent annoncer leurs ayants droit économiques à l'OFJ — les délais courent",
 "it": "Registro della trasparenza: SA e Sagl devono annunciare gli aventi diritto economici all'UFG — i termini corrono",
}
METAS = {
 "de": "Seit 1.10.2026 gilt das neue eidgenössische Transparenzregister: AG und GmbH melden ihre wirtschaftlich berechtigten Personen dem Bundesamt für Justiz. Die Übergangsfristen nach Art. 51 TJPG, Ausnahmen und Bussen bis CHF 500'000.",
 "en": "Since 1 Oct 2026 the new Swiss Federal Transparency Register applies: AG and GmbH must report their beneficial owners to the Federal Office of Justice. Art. 51 transition deadlines, exemptions and fines up to CHF 500'000.",
 "fr": "Depuis le 1.10.2026, le nouveau registre fédéral de la transparence s'applique : les SA et Sàrl doivent annoncer leurs ayants droit économiques à l'OFJ. Délais transitoires (art. 51), exceptions et amendes jusqu'à 500 000 francs.",
 "it": "Dal 1.10.2026 vige il nuovo registro federale della trasparenza: SA e Sagl devono annunciare gli aventi diritto economici all'UFG. Termini transitori (art. 51), eccezioni e multe fino a 500 000 franchi.",
}

for lang, sections in [("de", DE), ("en", EN), ("fr", FR), ("it", IT)]:
    build(lang, SLUG, TITLES[lang], METAS[lang], sections, related=RELATED)
print("done")
