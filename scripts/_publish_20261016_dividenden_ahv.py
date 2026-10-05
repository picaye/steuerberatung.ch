#!/usr/bin/env python3
"""Build the BGE 9C_532/2025 dividend/AHV article in all 4 languages.

Slug: dividenden-ahv-pflicht-bge-9c-532-2025
Sources (all primary, verified 2026-10-05):
- BGE 9C_532/2025 full text, bundesgericht.ch (relevancy.bger.ch)
- BSV WML 318.102.02 d, Stand 1. Mai 2026 (sozialversicherungen.admin.ch/de/d/6944)
- AHVG SR 831.10 Art. 4/5 (lexfind mirror of fedlex text)
- admin.ch Medienmitteilung 15.10.2025 (Postulat Herzog 22.4450)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "dividenden-ahv-pflicht-bge-9c-532-2025"
RELATED = ["verrechnungssteuer-schweiz-35-prozent.html",
           "verrechnungssteuer-rueckerstattungsfrist-ablauf.html",
           "ahv-mindestbeitrag-selbststaendige.html"]

# ---------------- German ----------------
de_title = "Dividenden statt Lohn: Was das AHV-Urteil 9C_532/2025 für Inhaber-AGs bedeutet"
de_meta = "Das Bundesgericht hat am 25. Juni 2026 (9C_532/2025) den Durchgriff auf Dividenden über eine Holding bestätigt. Wer als Inhaber-AG den Lohn zu tief und die Dividende zu hoch ansetzt, zahlt AHV-Beiträge nach. Die Klärung gehört vor den GV-Beschluss per 31.12.2026."
de_sections = [
 ("Was das Bundesgericht entschieden hat",
  """<p>Am 25. Juni 2026 hat das Bundesgericht in der Sache <strong>9C_532/2025</strong> ein Grundsatzurteil zum AHV-Beitragsrecht gefällt: Schüttet eine Aktiengesellschaft Dividenden an eine vom arbeitenden Inhaber beherrschte Holding aus, kann die Ausgleichskasse einen Teil dieser Dividenden als <strong>beitragspflichtigen Lohn</strong> nachveranlagen – trotz der zwischengeschalteten Gesellschaft. Die Beschwerde der betroffenen AG wurde abgewiesen.</p>
<p>Das Bundesamt für Sozialversicherungen (BSV) hat den Entscheid am 4. August 2026 in seiner Rechtsprechungsauswahl <strong>Nr. 85</strong> publiziert – eine eigene Kreisschreiben-Nummer zum Thema existiert nicht; die massgebenden Vollzugsvorgaben stehen in der Wegleitung über den massgebenden Lohn (WML).</p>
<p>Neu ist an dem Entscheid nicht die Umqualifikation selbst: dass die Ausgleichskassen eine zu tiefe Entlöhnung zusammen mit einer überhöhten Dividende korrigieren dürfen, ist seit Jahren gefestigte Rechtsprechung (BGE 141 V 634, BGE 145 V 50). Das Neue ist der <strong>Durchgriff durch die Holding</strong>: Die rechtliche Selbstständigkeit einer zwischengeschalteten Gesellschaft bleibt unbeachtet, wenn das Konstrukt im Wesentlichen auf die Vermeidung der AHV-abgaberechtlichen Folgen abzielt und die Holding keine wesentliche eigene Geschäftstätigkeit entfaltet.</p>
<p><strong>Praxistipp:</strong> Wer seine Dividenden über eine Personal- oder Holding-GmbH laufen lässt, darf sich nicht in Sicherheit wiegen – das Bundesgericht prüft die wirtschaftliche Realität, nicht die Struktur auf dem Papier.</p>"""),
 ("Wann eine Dividende zu AHV-pflichtigem Lohn wird",
  """<p>AHV-Beiträge werden nur vom Erwerbseinkommen erhoben, nicht vom Vermögensertrag (Art. 4 und 5 AHVG). Dividenden sind grundsätzlich beitragsfreier Kapitalertrag. Die Behörden weichen von der gewählten Aufteilung zwischen Lohn und Dividende aber ab, wenn <strong>kumulativ</strong> zwei Voraussetzungen erfüllt sind (E. 2.2 des Urteils):</p>
<ol><li>Der Lohn ist im Vergleich zu branchenüblichen Gehältern <strong>unangemessen tief</strong>, und</li>
<li>die Dividende ist <strong>offensichtlich überhöht</strong> – nach der Wegleitung des BSV über den massgebenden Lohn (WML) vermutungsweise dann, wenn sie 10 % des Steuerwerts der Aktien übersteigt.</li></ol>
<p>Beides sind Vorgaben der Verwaltungspraxis: Die 10-Prozent-Vermutung und die Aufrechnung «bis zur Höhe eines branchenüblichen Gehalts» stehen in der WML (Rz 2010 ff.), nicht im Gesetz. Die Angemessenheit des Lohns beurteilen die Kassen anhand von Pflichtenheft, Verantwortung, Pensum und Branchenvergleich – als Orientierung dient u. a. der Lohnrechner Salarium des Bundesamtes für Statistik.</p>
<p>Im beurteilten Fall war der Lohn des alleinigen Aktionärs und 100-%-Angestellten auf exakt jenes Einkommen festgesetzt worden, das gemäss Rententabelle gerade die maximale AHV-Vollrente ergibt (Fr. 86'040.-). Das Gericht durfte dies als <strong>Indiz für eine beitragsrechtlich motivierte Lohnfestsetzung</strong> werten.</p>
<p><strong>Praxistipp:</strong> Dokumentieren Sie die Herleitung Ihres Inhaberlohns (Stellenbeschrieb, Pensum, Branchenvergleich) – die beste Verteidigung gegen eine Nachforderung ist ein marktgerechter Lohn, der von Anfang an plausibel ist.</p>"""),
 ("Der konkrete Fall: Zahlen aus der Arztpraxis-AG",
  """<p>Die beteiligte AG (hervorgegangen aus einer Einzelunternehmung) schüttete in den Jahren 2021 und 2022 Dividenden von <strong>Fr. 582'000.- (2021)</strong> und <strong>Fr. 650'000.- (2022)</strong> an ihre Alleinaktionärin aus – eine Holding-GmbH, die am selben Tag gegründet wurde, an dem sie sämtliche Aktien übernahm. Der Alleininhaber der Holding arbeitete zu 100 % in der AG und bezog dort Fr. 86'040.- Lohn.</p>
<p>Merkmale der Holding laut Bundesgericht: 96,5 % ihrer Einnahmen stammten aus der Beteiligung an der AG, sie beschäftigte keine AHV-pflichtigen Mitarbeitenden, und die Gelder flossen über Dividenden und Darlehen umgehend an den Inhaber weiter. Die behaupteten Zwecke (Immobilienverwaltung, Nachfolgeregelung) vermochten die Struktur nicht plausibel zu erklären.</p>
<p>Die Ausgleichskasse rechnete nach der Einsprache <strong>Fr. 99'044.- (2021)</strong> und <strong>Fr. 98'346.- (2022)</strong> als massgebenden Lohn auf – die Differenz zum branchenüblichen Lohn von rund Fr. 185'000.-. Daraus resultierte eine Nachforderung von AHV/IV/EO-, ALV- und Familienzulagenbeiträgen samt Verzugszins. Die Höhe der Aufrechnung selbst war vor Bundesgericht nicht mehr bestritten.</p>"""),
 ("Was Inhaber-AGs bis zum 31. Dezember 2026 prüfen sollten",
  """<p>Das Urteil setzt keine gesetzliche Frist – aber der Kalender tut es: Der Gewinnverteilungsbeschluss für das Geschäftsjahr 2026 fällt an der Generalversammlung bzw. in der Jahresendplanung, also <strong>spätestens bis zum 31. Dezember 2026</strong>. Wer die Aufteilung Lohn/Dividende für 2026 und die Folgejahre klären will, sollte das vor diesem Termin tun – die Revision der Ausgleichskasse prüft die Jahre 2021 bis 2026, und AHV-Beiträge verjähren erst fünf Jahre nach Ablauf des Beitragsjahres (Art. 16 Abs. 1 AHVG).</p>
<ol><li><strong>Lohn prüfen:</strong> Ist der Inhaberlohn für Pensum, Verantwortung und Branche vertretbar? Ein Lohn auf exakt der Rentenskala-Obergrenze ist ein Warnsignal.</li>
<li><strong>Dividende einordnen:</strong> Übersteigt die Dividende 10 % des Steuerwerts der Beteiligung, greift die Vermutung der Überhöhung (WML).</li>
<li><strong>Holding begründen:</strong> Eine Holding schützt nur, wenn sie eine eigene wirtschaftliche Tätigkeit hat – eigene Mitarbeitende, Substanz, plausible Zwecke jenseits der Abgabenoptimierung.</li>
<li><strong>Dokumentieren:</strong> Branchenvergleich, Pflichtenheft und Beschlussprotokolle aufbewahren – im Kontrollfall entscheidet die Aktenlage.</li></ol>
<p><strong>Praxistipp:</strong> Die AHV-Beitragsfolgen sind getrennt von den Steuerfolgen zu denken: Die Dividende ist zwar teilbesteuert, spart aber Sozialversicherungsbeiträge – und genau diese Verlagerung beobachten die Ausgleichskassen seit den Unternehmenssteuerreformen.</p>"""),
 ("Die 2/3-bis-1/3-Regel: Faustregel, keine Norm",
  """<p>In der Beratungspraxis kursiert die Daumenregel, der Inhaber solle «mindestens zwei Drittel des Gewinns als Lohn, höchstens ein Drittel als Dividende» ausrichten. Wichtig zu wissen: <strong>Weder das AHVG noch die AHVV noch die WML enthalten ein solches Verhältnis.</strong> Auch das Bundesgericht stellt nicht auf Prozente des Gewinns ab, sondern auf das offensichtliche Missverhältnis zwischen Arbeitsleistung und Lohn einerseits und zwischen eingesetztem Vermögen und Dividende andererseits. Die Faustregel ist eine verbreitete Orientierungshilfe – rechtlich verbindlich ist sie nicht.</p>"""),
 ("Ausblick: Die AHV-Reform kommt",
  """<p>Der Bundesrat hält die bisherigen Massnahmen gegen überhöhte Dividenden für lückenhaft. Am 15. Oktober 2025 verabschiedete er den Bericht zum Postulat Herzog (22.4450): Geprüft wird, Dividenden, die eine gewisse Renditeschwelle übersteigen, <strong>grundsätzlich als Lohn</strong> einzustufen – ohne dass die Kassen zusätzlich einen unangemessen tiefen Lohn nachweisen müssten. Eine gesetzliche Verankerung ist angekündigt, aber offen; bis dahin gilt die im Urteil 9C_532/2025 bestätigte Praxis.</p>"""),
 ("Kurz gesagt",
  """<ul><li>Bundesgericht 9C_532/2025 vom 25. Juni 2026: Dividenden über eine substanzlose Holding können als AHV-pflichtiger Lohn aufgerechnet werden.</li>
<li>Voraussetzung bleibt das kumulierte Missverhältnis: unangemessen tiefer Lohn plus offensichtlich überhöhte Dividende (Vermutung ab 10 % des Aktien-Steuerwerts – Weisungspraxis, nicht Gesetz).</li>
<li>Die Aufteilung Lohn/Dividende für 2026 gehört vor den Gewinnverteilungsbeschluss bis 31.12.2026; Nachforderungen drohen bis fünf Jahre rückwirkend.</li>
<li>Die 2/3–1/3-Regel ist eine Faustregel ohne gesetzliche Grundlage.</li>
<li>Dies ist allgemeine Information, keine individuelle Beratung – lassen Sie Ihre Struktur von Treuhand oder Steuerberater prüfen.</li></ul>"""),
]

# ---------------- English ----------------
en_title = "Dividends Instead of Salary: What Federal Supreme Court Ruling 9C_532/2025 Means for Owner-Managed AGs"
en_meta = "On 25 June 2026 the Federal Supreme Court (9C_532/2025) confirmed that dividends routed through a holding company can be reclassified as AHV/AVS-contributable salary. Owner-managed companies should settle the salary/dividend split before the 31 December 2026 profit distribution decision."
en_sections = [
 ("What the Federal Supreme Court decided",
  """<p>On 25 June 2026 the Federal Supreme Court ruled in case <strong>9C_532/2025</strong>: where a company pays dividends to a holding company controlled by the working owner, the compensation fund may reclassify part of those dividends as <strong>salary subject to social security contributions</strong> — despite the intermediate company. The AG's appeal was dismissed.</p>
<p>The Federal Social Insurance Office (FSIO) published the ruling on 4 August 2026 in its case-law selection <strong>No. 85</strong>; there is no dedicated circular number on the topic — the operative guidance sits in the Wegleitung über den massgebenden Lohn (WML).</p>
<p>The reclassification itself is not new: funds have long been entitled to correct a salary that is too low combined with an excessive dividend (BGE 141 V 634, BGE 145 V 50). What is new is the <strong>look-through of the holding</strong>: the separate legal personality of an intermediate company is disregarded where the structure essentially aims at avoiding AHV/AVS contribution consequences and the holding has no substantial business activity of its own.</p>
<p><strong>Practical tip:</strong> routing dividends through a personal holding company no longer provides automatic protection — the Court looks at economic reality, not the paper structure.</p>"""),
 ("When a dividend becomes AHV-contributable salary",
  """<p>Social security contributions are levied only on employment income, not on investment income (Art. 4 and 5 AHVG). Dividends are in principle contribution-free capital yield. Authorities depart from the chosen salary/dividend split only where <strong>both</strong> conditions are met cumulatively (E. 2.2 of the ruling):</p>
<ol><li>the salary is <strong>unreasonably low</strong> compared with industry-standard pay, and</li>
<li>the dividend is <strong>manifestly excessive</strong> — under the BSV Wegleitung über den massgebenden Lohn (WML) presumptively so once it exceeds 10 % of the tax value of the shares.</li></ol>
<p>Both are administrative practice, not statute: the 10 % presumption and the reclassification "up to the level of an industry-standard salary" appear in the WML (marginal nos. 2010 ff.), not in the AHVG. Reasonableness of the salary is assessed by job profile, responsibility, workload and industry comparison — the Federal Statistical Office's Salarium wage calculator serves as one reference.</p>
<p>In the case at hand, the sole shareholder's salary had been set at exactly the income level that yields the maximum AHV pension under the federal rent tables (CHF 86'040.-). The Court accepted this as an <strong>indicator of contribution-driven salary setting</strong>.</p>"""),
 ("The concrete case: figures from the medical practice AG",
  """<p>The AG (converted from a sole proprietorship) distributed dividends of <strong>CHF 582'000.- (2021)</strong> and <strong>CHF 650'000.- (2022)</strong> to its sole shareholder — a holding GmbH founded on the very day it acquired all the shares. The holding's sole owner worked 100 % for the AG on a salary of CHF 86'040.-.</p>
<p>Holding features noted by the Court: 96.5 % of its income came from the participation in the AG, it employed no contribution-liable staff, and the funds flowed on to the owner immediately via dividends and loans. The asserted purposes (real-estate administration, succession planning) did not plausibly explain the structure.</p>
<p>After the objection procedure the fund reclassified <strong>CHF 99'044.- (2021)</strong> and <strong>CHF 98'346.- (2022)</strong> as contributable salary — the gap to an industry-standard salary of roughly CHF 185'000.- — resulting in back contributions for AHV/IV/EO, ALV and family allowances plus default interest.</p>"""),
 ("What owner-managed AGs should review before 31 December 2026",
  """<p>The ruling sets no statutory deadline — the calendar does: the profit distribution decision for the 2026 financial year is taken at the shareholders' meeting or in year-end planning, i.e. <strong>no later than 31 December 2026</strong>. AHV contributions become time-barred only five years after the end of the contribution year (Art. 16 para. 1 AHVG), so audits can reach back to 2021.</p>
<ol><li><strong>Salary:</strong> defensible for workload, responsibility and industry? A salary set exactly at the pension-scale ceiling is a red flag.</li>
<li><strong>Dividend:</strong> above 10 % of the tax value of the participation, the presumption of excess applies (WML).</li>
<li><strong>Holding:</strong> protected only with genuine activity — own staff, substance, purposes beyond contribution planning.</li>
<li><strong>Documentation:</strong> keep industry comparisons, job profiles and meeting minutes — in an audit the file decides.</li></ol>"""),
 ("The 2/3–1/3 rule: a rule of thumb, not law",
  """<p>Advisory practice often quotes a "at least two thirds salary, at most one third dividend" split. To be clear: <strong>neither the AHVG, the AHVV nor the WML contains any such ratio.</strong> The Court tests the manifest disproportion between work and pay on one side and invested capital and dividend on the other — not percentages of profit. The rule of thumb is a common orientation, legally non-binding.</p>"""),
 ("Outlook: legislative reform is coming",
  """<p>In its report of 15 October 2025 implementing postulate Herzog (22.4450), the Federal Council considers the current tools against excessive dividends inadequate and examines classifying dividends above a yield threshold as salary by law — without funds having to prove an unreasonably low salary additionally. Legislation is announced but open; until then the practice confirmed in 9C_532/2025 governs.</p>"""),
 ("In short",
  """<ul><li>BGE 9C_532/2025 of 25 June 2026: dividends routed through a substance-less holding can be reclassified as AHV-contributable salary.</li>
<li>Still required: manifest disproportion — unreasonably low salary plus manifestly excessive dividend (presumed above 10 % of the shares' tax value — administrative guidance, not statute).</li>
<li>Settle the 2026 salary/dividend split before the profit distribution decision due by 31 December 2026; back claims reach five years.</li>
<li>The 2/3–1/3 split is a rule of thumb without statutory basis.</li>
<li>General information, not individual advice — have your structure reviewed by a licensed fiduciary or tax adviser.</li></ul>"""),
]

# ---------------- French ----------------
fr_title = "Dividendes au lieu du salaire : ce que l'arrêt 9C_532/2025 change pour les SA détenues par leur dirigeant"
fr_meta = "Le 25 juin 2026, le Tribunal fédéral (9C_532/2025) a confirmé que des dividendes versés via une holding peuvent être requalifiés en salaire soumis aux cotisations AVS/AI. Les SA unipersonnelles doivent clarifier la répartition salaire/dividende avant la décision de répartition du bénéfice du 31.12.2026."
fr_sections = [
 ("Ce que le Tribunal fédéral a jugé",
  """<p>Le 25 juin 2026, le Tribunal fédéral a statué dans la cause <strong>9C_532/2025</strong> : lorsqu'une société verse des dividendes à une holding contrôlée par son dirigeant-actionnaire, la caisse de compensation peut requalifier une partie de ces dividendes en <strong>salaire soumis aux cotisations sociales</strong> — malgré la société interposée. Le recours de la SA a été rejeté.</p>
<p>L'Office fédéral des assurances sociales (OFAS) a publié l'arrêt le 4 août 2026 dans sa sélection de jurisprudence <strong>n° 85</strong> ; il n'existe pas de numéro de circulaire propre au thème — les règles d'exécution figurent dans le Commentaire sur le salaire déterminant (CSD).</p>
<p>La requalification n'est pas nouvelle : les caisses corrigent depuis années un salaire manifestement trop bas couplé à un dividende excessif (ATF 141 V 634, ATF 145 V 50). La nouveauté, c'est le <strong>percement de la holding</strong> : la personnalité juridique distincte de la société interposée reste non avenue lorsque la structure vise essentiellement à éluder les conséquences cotisatives et que la holding n'a pas d'activité économique propre substantielle.</p>
<p><strong>Conseil pratique :</strong> transiter par une holding personnelle ne protège plus automatiquement — le Tribunal regarde la réalité économique, pas le montage sur papier.</p>"""),
 ("Quand un dividende devient un salaire cotisable",
  """<p>Les cotisations AVS ne frappent que le revenu de l'activité lucrative, non le revenu de la fortune (art. 4 et 5 LAVS). Les dividendes sont en principe un rendement de capital non cotisable. Les autorités s'écartent de la répartition choisie uniquement si les deux conditions sont réunies <strong>cumulativement</strong> (consid. 2.2 de l'arrêt) :</p>
<ol><li>le salaire est <strong>démesurément bas</strong> par rapport aux salaires usuels de la branche, et</li>
<li>le dividende est <strong>manifestement excessif</strong> — présumé tel, selon le Commentaire de l'OFAS sur le salaire déterminant (CSD), dès qu'il dépasse 10 % de la valeur fiscale des actions.</li></ol>
<p>Ces deux critères relèvent de la pratique administrative : la présomption des 10 % et la requalification « jusqu'à concurrence du salaire usuel de la branche » figurent au CSD (marges 2010 ss.), non dans la loi. Le caractère approprié du salaire s'apprécie d'après le cahier des charges, la responsabilité, le taux d'activité et la comparaison sectorielle (outil : le calculateur salarial Salarium de l'Office fédéral de la statistique).</p>
<p>Dans le cas jugé, le salaire de l'actionnaire unique avait été fixé exactement au revenu ouvrant droit à la rente AVS maximale (CHF 86'040.-). Le Tribunal a pu y voir un <strong>indice d'une fixation du salaire motivée par les cotisations</strong>.</p>"""),
 ("Le cas concret : les chiffres d'une SA de cabinet médical",
  """<p>La SA (issue d'une entreprise individuelle) a distribué des dividendes de <strong>CHF 582'000.- (2021)</strong> et <strong>CHF 650'000.- (2022)</strong> à son actionnaire unique — une GmbH holding immatriculée le jour même où elle a repris toutes les actions. Le propriétaire unique de la holding travaillait à 100 % dans la SA pour un salaire de CHF 86'040.-.</p>
<p>Signes relevés par le Tribunal : 96,5 % des revenus de la holding provenaient de sa participation, elle n'employait aucun salarié cotisable, et les fonds étaient immédiatement relayés vers le dirigeant sous forme de dividendes ou de prêts. Les buts invoqués (gestion immobilière, planification de la succession) n'expliquaient pas plausiblement la structure.</p>
<p>Après opposition, la caisse a requalifié en salaire cotisable <strong>CHF 99'044.- (2021)</strong> et <strong>CHF 98'346.- (2022)</strong> — la différence avec un salaire usuel de la branche d'environ CHF 185'000.- — d'où un rappel de cotisations AVS/AI/APG, AC et allocations familiales plus intérêts moratoires.</p>"""),
 ("Ce que les SA dirigeant-propriétaire doivent vérifier avant le 31 décembre 2026",
  """<p>L'arrêt ne fixe aucun délai légal — le calendrier, si : la décision de répartition du bénéfice pour l'exercice 2026 tombe à l'assemblée générale ou dans la planification de fin d'année, donc <strong>au plus tard le 31 décembre 2026</strong>. Les cotisations AVS ne se prescrivent que cinq ans après la fin de l'année de cotisation (art. 16 al. 1 LAVS) : les contrôles peuvent remonter jusqu'en 2021.</p>
<ol><li><strong>Salaire :</strong> défendable vu l'activité, la responsabilité et la branche ? Un salaire calé exactement sur le plafond de l'échelle des rentes est un signal d'alerte.</li>
<li><strong>Dividende :</strong> au-delà de 10 % de la valeur fiscale de la participation, la présomption d'excès s'applique (CSD).</li>
<li><strong>Holding :</strong> protégée seulement si elle a une activité propre — collaborateurs, substance, buts autres que l'optimisation cotisative.</li>
<li><strong>Documentation :</strong> conservez comparaisons sectorielles, descriptions de poste et procès-verbaux — en cas de contrôle, le dossier décide.</li></ol>"""),
 ("La règle des 2/3–1/3 : un repère, pas une norme",
  """<p>La pratique de conseil cite souvent la répartition « au moins deux tiers en salaire, un tiers en dividende ». À savoir : <strong>ni la LAVS, ni l'RAVS, ni le CSD ne contiennent un tel rapport.</strong> Le Tribunal teste le déséquilibre manifeste entre prestation de travail et salaire d'une part, capital investi et dividende d'autre part — pas des pourcentages du bénéfice. Le repère est courant ; il n'a aucune force obligatoire.</p>"""),
 ("Perspectives : la révision de l'AVS arrive",
  """<p>Dans son rapport du 15 octobre 2025 donnant suite au postulat Herzog (22.4450), le Conseil fédéral juge les outils actuels insuffisants et examine l'inscription dans la loi d'une requalification en salaire des dividendes dépassant un certain seuil de rendement — sans que les caisses doivent prouver en plus un salaire anormalement bas. Une base légale est annoncée mais ouverte ; en attendant, c'est la pratique confirmée par 9C_532/2025 qui s'applique.</p>"""),
 ("En bref",
  """<ul><li>ATF 9C_532/2025 du 25 juin 2026 : des dividendes transitant par une holding sans substance peuvent être requalifiés en salaire cotisable AVS.</li>
<li>Conditions inchangées : déséquilibre manifeste — salaire démesurément bas plus dividende manifestement excessif (présomption dès 10 % de la valeur fiscale des actions — directive administrative, non loi).</li>
<li>Arrêtez la répartition salaire/dividende 2026 avant la décision de répartition du bénéfice du 31.12.2026 ; les rappels couvrent cinq ans.</li>
<li>La règle 2/3–1/3 est un repère sans base légale.</li>
<li>Information générale, pas un conseil individuel — faites examiner votre structure par un fiduciaire ou conseiller fiscal breveté.</li></ul>"""),
]

# ---------------- Italian ----------------
it_title = "Dividendi invece del salario: cosa cambia per le SA di proprietà con la sentenza 9C_532/2025"
it_meta = "Il 25 giugno 2026 il Tribunale federale (9C_532/2025) ha confermato che i dividendi transitati per una holding possono essere riqualificati come salario soggetto ai contributi AVS/AI. Le SA unipersonnelle devono chiarire la ripartizione salario/dividendi prima della decisione di ripartizione dell'utile del 31.12.2026."
it_sections = [
 ("Cosa ha deciso il Tribunale federale",
  """<p>Il 25 giugno 2026, nella causa <strong>9C_532/2025</strong>, il Tribunale federale ha stabilito: se una società distribuisce dividendi a una holding controllata dal socio che vi lavora, la cassa di compensazione può riqualificare parte di quei dividendi come <strong>salario soggetto ai contributi sociali</strong> — nonostante la società interposta. Il ricorso della SA è stato respinto.</p>
<p>L'Ufficio federale delle assicurazioni sociali (UFAS) ha pubblicato la sentenza il 4 agosto 2026 nella sua raccolta di giurisprudenza <strong>n. 85</strong>; non esiste un numero di circolare proprio sul tema — le regole d'esecuzione figurano nella Guida sul salario determinante (GSD).</p>
<p>La riqualificazione in sé non è nuova: da anni le casse correggono un salario sproporzionatamente basso abbinato a un dividente eccessivo (DTF 141 V 634, DTF 145 V 50). La novità è il <strong>superamento della holding</strong>: l'autonomia giuridica della società interposta resta non riconosciuta quando la struttura mira essenzialmente a eludere gli effetti contributivi e la holding non svolge un'attività economica propria sostanziale.</p>
<p><strong>Consiglio pratico:</strong> far transitare i dividendi per una holding personale non protegge più automaticamente — il Tribunale guarda la realtà economica, non l'architettura cartacea.</p>"""),
 ("Quando un dividendo diventa salario assoggettato a contributi",
  """<p>I contributi AVS colpiscono solo il reddito da attività lucrativa, non il rendimento della sostanza (art. 4 e 5 LAVS). I dividendi sono di principio rendimento di capitale esente da contributi. Le autorità si discostano dalla ripartizione scelta solo se ricorrono <strong>cumulativamente</strong> due condizioni (consid. 2.2 della sentenza):</p>
<ol><li>il salario è <strong>sproporzionatamente basso</strong> rispetto ai salari usuali del settore, e</li>
<li>il dividendo è <strong>manifestamente eccessivo</strong> — secondo la Guida dell'UFAS sul salario determinante (GSD) presunto tale già supera il 10 % del valore fiscale delle azioni.</li></ol>
<p>Sono prescrizioni amministrative, non legge: la presunzione del 10 % e la riqualificazione «fino all'importo del salario usuale del settore» figurano nella GSD (nm. 2010 segg.), non nella LAVS. L'adeguatezza del salario si valuta in base a mansioni, responsabilità, grado di occupazione e confronto settoriale (strumento di riferimento: il calcolatore salariale Salarium dell'Ufficio federale di statistica).</p>
<p>Nel caso giudicato, il salario dell'unico azionista era stato fissato esattamente al reddito che secondo le tavole delle rendite dà diritto alla rendita AVS massima (CHF 86'040.-). Il Tribunale ha potuto considerarlo un <strong>indizio di una fissazione del salario motivata dai contributi</strong>.</p>"""),
 ("Il caso concreto: i numeri di una SA di uno studio medico",
  """<p>La SA (nata da un'impresa individuale) ha distribuito dividendi di <strong>CHF 582'000.- (2021)</strong> e <strong>CHF 650'000.- (2022)</strong> alla sua unica azionista — una GmbH holding iscritta al registro di commercio lo stesso giorno in cui ha rilevato tutte le azioni. L'unico proprietario della holding lavorava al 100 % nella SA con un salario di CHF 86'040.-.</p>
<p>Elementi rilevati dal Tribunale: il 96,5 % degli introiti della holding proveniva dalla partecipazione, la holding non occupava dipendenti assoggettati a contributi e i fondi fluivano immediatamente al titolare tramite dividendi o prestiti. Le finalità addotte (amministrazione immobiliare, pianificazione della successione) non spiegavano plausibilmente la struttura.</p>
<p>Dopo l'opposizione la cassa ha riqualificato come salario determinante <strong>CHF 99'044.- (2021)</strong> e <strong>CHF 98'346.- (2022)</strong> — la differenza rispetto a un salario usuale del settore di circa CHF 185'000.- — con conseguente credito contributivo AVS/AI/IPG, AD e assegni familiari più interessi moratori.</p>"""),
 ("Cosa le SA di proprietà dovrebbero verificare entro il 31 dicembre 2026",
  """<p>La sentenza non fissa un termine legale — lo fa il calendario: la decisione di ripartizione dell'utile per l'esercizio 2026 cade in assemblea o nella pianificazione di fine anno, dunque <strong>al più tardi il 31 dicembre 2026</strong>. I contributi AVS cadono in prescrizione solo cinque anni dopo la fine dell'anno contributivo (art. 16 cpv. 1 LAVS): i controlli possono risalire fino al 2021.</p>
<ol><li><strong>Salario:</strong> difendibile per mansioni, responsabilità e settore? Un salario ancorato esattamente al tetto della scala delle rendite è un segnale d'allarme.</li>
<li><strong>Dividendo:</strong> oltre il 10 % del valore fiscale della partecipazione scatta la presunzione di eccesso (GSD).</li>
<li><strong>Holding:</strong> protetta solo se ha un'attività propria — dipendenti, sostanza, scopi diversi dall'ottimizzazione contributiva.</li>
<li><strong>Documentazione:</strong> conservate confronti settoriali, descrizioni delle mansioni e verbali — in caso di controllo decide il fascicolo.</li></ol>"""),
 ("La regola dei 2/3–1/3: un orientamento, non una norma",
  """<p>Nella prassi consulenziale circola la regola «almeno due terzi a salario, un terzo a dividendi». Da sapere: <strong>né la LAVS, né l'OAVS, né la GSD contengono un simile rapporto.</strong> Il Tribunale verifica il sproporzionato squilibrio tra prestazione lavorativa e salario da un lato e capitale investito e dividendo dall'altro — non le percentuali dell'utile. L'orientamento è diffuso, ma giuridicamente non vincolante.</p>"""),
 ("Prospettive: la revisione dell'AVS arriva",
  """<p>Nel rapporto del 15 ottobre 2025 di risposta al postulato Herzog (22.4450), il Consiglio federale giudica carenti gli strumenti attuali ed esamina di qualificare per legge come salario i dividendi che superano una certa soglia di rendimento — senza che le casse debbano provare in aggiunta un salario iniquamente basso. Una base legale è annunciata ma aperta; nel frattempo vale la prassi confermata dalla sentenza 9C_532/2025.</p>"""),
 ("In breve",
  """<ul><li>DTF 9C_532/2025 del 25 giugno 2026: dividendi transitati per una holding senza sostanza possono essere riqualificati come salario assoggettato a contributi AVS.</li>
<li>Condizioni invariate: squilibrio manifesto — salario sproporzionatamente basso più dividendo manifestamente eccessivo (presunzione dal 10 % del valore fiscale delle azioni — direttiva amministrativa, non legge).</li>
<li>Chiarite la ripartizione salario/dividendi 2026 prima della decisione di ripartizione dell'utile del 31.12.2026; i recuperi coprono cinque anni.</li>
<li>La regola 2/3–1/3 è un orientamento senza base legale.</li>
<li>Informazione generale, non consulenza individuale — fate esaminare la vostra struttura da un fiduciario o consulente fiscale diplomato.</li></ul>"""),
]

for lang, title, meta, sections in [("de", de_title, de_meta, de_sections),
                                    ("en", en_title, en_meta, en_sections),
                                    ("fr", fr_title, fr_meta, fr_sections),
                                    ("it", it_title, it_meta, it_sections)]:
    build(lang, SLUG, title, meta, sections, related=RELATED)
print("done")
