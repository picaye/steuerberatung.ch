#!/usr/bin/env python3
"""Build EN + FR mirrors of minijobs-lohnschwelle-ahv-pflicht.html from the DE article."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "minijobs-lohnschwelle-ahv-pflicht"
RELATED = ["quellensteuer-nov-zusatzabzuege.html",
           "grenzgaenger-de-fr-it-steuern.html",
           "ahv-mindestbeitrag-selbststaendige.html"]

# ---------------- English ----------------
EN_TITLE = "Mini-jobs and seasonal staff: when payroll contributions and reporting duties are triggered"
EN_META = ("Short, irregular assignments up to CHF 2'500 in wages per person and year can be AHV-free "
           "— but only if the limit is respected per employer. A threshold, not an allowance; the private-"
           "household exception from the first franc; culture and media newly included from 2026: the "
           "checklist for employers in the Christmas business.")

EN_SECTIONS = [
    ("The CHF 2'500 limit: minor wages",
     "<p>If you pay an assistant at most <strong>CHF 2'500 per calendar year</strong>, you generally "
     "<strong>do not have to settle contributions to the AHV (old-age and survivors' insurance), IV "
     "(disability insurance), EO (income loss compensation scheme) or ALV (unemployment insurance)</strong> "
     "— unless the insured person explicitly requests them. This is the exemption for minor remuneration "
     "(factsheet 2.04 of the AHV compensation offices). The amount was raised from CHF 2'300 to CHF 2'500 "
     "as of 1 January 2025.</p>"
     "<p>Crucially: the limit applies <strong>per employer and per calendar year</strong>. All remuneration "
     "an employer pays to the same person during the current year — including additional benefits, tips and "
     "benefits in kind — must be added together.</p>"),
    ("A threshold, not an allowance — the classic mistake",
     "<p>If CHF 2'500 is exceeded by even one franc, <strong>the entire wage becomes contribution-"
     "liable — not just the excess amount</strong>. The compensation offices deliberately speak of a limit, "
     "not a deduction. If a third assignment in December pushes you over the threshold, contributions on the "
     "annual wage are owed retroactively — including default interest.</p>"
     "<p>Contributions follow the full rate: 5.3 % AHV/IV/EO plus 1.1 % ALV per side (the employer pays half; "
     "the total is 12.8 %), plus administration costs and family allowances via the cantonal compensation "
     "office.</p>"),
    ("Exceptions: private households, culture and media",
     "<p>For two areas the exemption does <strong>not</strong> apply — contributions are due from the first "
     "franc:</p>"
     "<ul><li><strong>Private households</strong> (domestic work: cleaning, gardening, childcare, "
     "housekeeping): contributions are due in every case (factsheet 2.06). Exception for allowance-type jobs "
     "(Sackgeldjobs): anyone who reaches at most age 25 in the calendar year in question earns up to "
     "CHF 750 per private household and year free of contributions (as of 2026: birth years 2001–2008; "
     "beyond that the limit no longer applies).</li>"
     "<li><strong>Culture and media workers:</strong> wages from dance and theatre productions, audio and "
     "image producers, radio and television, and artistic training institutions are always subject to "
     "contributions. <strong>From 1 January 2026</strong> the Federal Council extended contribution "
     "liability via an EEL amendment to further sectors — now including, among others, design, museums, "
     "media and choirs (information from the AHV compensation office of Solothurn).</li></ul>"),
    ("Who benefits from demanding contributions — and who is liable",
     "<p>Even below CHF 2'500, the insured person can <strong>demand that contributions be paid</strong>. "
     "This is worthwhile especially for students and young professionals: the contributions fill gaps in the "
     "individual AHV account and can later be credited against the non-earning contribution of married "
     "persons.</p>"
     "<p>Conversely: if the employee accepts the wage in full without deduction, the employer can "
     "<strong>no longer reclaim the employee's share retroactively</strong>. And an employer who does not "
     "pay contributions at all, or pays them late, is liable under <strong>Art. 52 AHVG</strong> for the "
     "entire damage — bearing even the employee's share, with no right of recourse.</p>"),
    ("Reporting duties and withholding tax on short-term wages",
     "<p>Contribution exemption does not mean anonymity: even minimally employed persons must be reported to "
     "the compensation office as soon as contributions are owed or demanded. For <strong>foreigners without "
     "residence in Switzerland</strong> (cross-border commuters, short-term residents), <strong>withholding "
     "tax applies from the first franc</strong> — the AHV exemption does not protect against that. The "
     "salary statement must also be issued for mini-jobs.</p>"),
    ("Checklist for the season start (November to January)",
     "<ol><li><strong>Track the annual wage per person and employer</strong> — including all additional "
     "benefits; check the cumulative total before every new assignment.</li>"
     "<li><strong>Check the sector:</strong> private household, culture, design, media, museum, choir? Then "
     "contributions are due from the first franc.</li>"
     "<li><strong>Note the assistant's age</strong> (allowance-type-job rule up to 25 years in private "
     "households).</li>"
     "<li><strong>Document any demand for contributions</strong> if the person wants them paid.</li>"
     "<li><strong>Plan for the withholding-tax duty</strong> from the first franc when the employee resides "
     "abroad.</li>"
     "<li><strong>Issue and retain the salary statement</strong> even for mini-jobs (10 years).</li></ol>"),
    ("In short",
     "<ul><li>Up to CHF 2'500 in wages per person and employer per calendar year: no AHV/IV/EO/ALV "
     "contributions — unless the person requests them (factsheet 2.04; limit in force since 1.1.2025).</li>"
     "<li>Exceeding the limit = contributions on the entire wage (threshold, not allowance) — retroactive "
     "claim including default interest.</li>"
     "<li>Private households and the culture/media sector (extended from 2026 to design, museums, media, "
     "choirs): contributions from the first franc.</li>"
     "<li>The employer is liable under Art. 52 AHVG for employee shares that were not deducted.</li>"
     "<li>Withholding tax on foreign residence applies regardless of the AHV limit.</li>"
     "<li>General information, not individual advice — questions are clarified with the responsible "
     "compensation office.</li></ul>"),
]

# ---------------- French ----------------
FR_TITLE = "Mini-jobs et personnel saisonnier : quand les cotisations salariales et les obligations d'annonce se déclenchent"
FR_META = ("Des engagements courts et irréguliers jusqu'à CHF 2'500 de salaire par personne et par an "
           "peuvent être exonérés de cotisations AHV — mais seulement si la limite est respectée par "
           "employeur. Un seuil et non une franchise, l'exception des ménages privés dès le premier franc, "
           "la culture et les médias inclus dès 2026 : la checklist pour les employeurs en période de Noël.")

FR_SECTIONS = [
    ("La limite de CHF 2'500 : rémunérations de moindre importance",
     "<p>Si vous versez au maximum <strong>CHF 2'500 par année civile</strong> à une personne engagée de "
     "façon temporaire, vous ne devez en principe <strong>pas de cotisations à l'AVS (assurance vieillesse "
     "et survivants, AHV), à l'AI (assurance invalidité), à l'APG (regime des pertes de gain) ni à l'AC "
     "(assurance-chômage)</strong> — sauf si la personne assurée les exige expressément. C'est l'exemption "
     "pour rémunérations de moindre importance (notice 2.04 des caisses de compensation AVS). Le montant est "
     "passé de CHF 2'300 à CHF 2'500 au 1er janvier 2025.</p>"
     "<p>Point décisif : la limite s'applique <strong>par employeur et par année civile</strong>. Toutes les "
     "rémunérations qu'un employeur verse à la même personne au cours de l'année en cours — y compris les "
     "appointements accessoires, les pourboires et les prestations en nature — doivent être additionnées.</p>"),
    ("Un seuil, pas une franchise — l'erreur classique",
     "<p>Dès que CHF 2'500 est dépassé ne serait-ce que d'un franc, <strong>l'entier du salaire est soumis à "
     "cotisations — et non le seul montant dépassé</strong>. Les caisses de compensation parlent "
     "délibérément d'une limite, pas d'une déduction. Si un troisième engagement en décembre fait franchir le "
     "seuil, les cotisations sur le salaire annuel sont dues rétroactivement — intérêts moratoires compris.</p>"
     "<p>Les cotisations suivent le taux plein : 5.3 % AVS/AI/APG plus 1.1 % AC par partie (l'employeur en "
     "paie la moitié ; total 12.8 %), auxquels s'ajoutent les frais d'administration et les allocations "
     "familiales de la caisse cantonale.</p>"),
    ("Exceptions : ménages privés, culture et médias",
     "<p>Pour deux domaines, l'exemption ne s'applique <strong>pas</strong> — les cotisations courent dès le "
     "premier franc :</p>"
     "<ul><li><strong>Ménages privés</strong> (travaux domestiques : nettoyage, jardinage, garde d'enfants, "
     "aide ménagère) : cotisations dues dans tous les cas (notice 2.06). Exception pour les petits boulots "
     "d'appoint (Sackgeldjobs) : quiconque atteint au plus 25 ans dans l'année civile concernée gagne jusqu'à "
     "CHF 750 par ménage privé et par an sans cotisations (état 2026 : générations 2001–2008 ; au-delà, la "
     "limite ne s'applique plus).</li>"
     "<li><strong>Travailleurs de la culture et des médias :</strong> les salaires des productions de danse "
     "et de théâtre, des producteurs de son et d'image, de la radio et de la télévision ainsi que des "
     "institutions de formation artistique sont toujours soumis à cotisations. <strong>Dès le 1er janvier "
     "2026</strong>, le Conseil fédéral a étendu l'assujettissement aux cotisations via une modification du "
     "plan EEL à d'autres branches — désormais notamment le design, les musées, les médias et les chœurs "
     "(information de la caisse de compensation AVS de Soleure).</li></ul>"),
    ("Qui profite de la demande de cotisations — et qui répond du paiement",
     "<p>Même en dessous de CHF 2'500, la personne assurée peut <strong>exiger le paiement des "
     "cotisations</strong>. Cela vaut surtout pour les étudiants et les jeunes actifs : les cotisations "
     "comblent les lacunes de cotisations sur le compte individuel AHV et peuvent plus tard être imputées "
     "sur la cotisation des personnes sans activité lucrative (conjoints).</p>"
     "<p>En sens inverse : si le salarié accepte le salaire en entier sans déduction, l'employeur ne peut "
     "<strong>plus réclimer après coup la part salariale</strong>. Et l'employeur qui ne verse pas les "
     "cotisations, ou les verse trop tard, répond, selon l'<strong>Art. 52 AHVG</strong> (LAVS), de "
     "l'entier du dommage — il supporte alors aussi la part du salarié, sans droit de recours.</p>"),
    ("Obligations d'annonce et impôt à la source pour les salaires de courte durée",
     "<p>L'exonération de cotisations ne signifie pas l'anonymat : même les personnes occupées à un poste de "
     "moindre importance doivent être annoncées à la caisse de compensation dès que des cotisations sont "
     "dues ou exigées. Pour les <strong>étrangers sans domicile en Suisse</strong> (frontaliers, personnes "
     "en séjour de courte durée), <strong>l'impôt à la source s'ajoute dès le premier franc</strong> — la "
     "franchise AHV n'en protège pas. Le certificat de salaire doit également être établi pour les "
     "mini-jobs.</p>"),
    ("Checklist pour le début de saison (de novembre à janvier)",
     "<ol><li><strong>Tenez le compte du salaire annuel par personne et par employeur</strong> — y compris "
     "tous les appointements accessoires ; vérifiez le cumul avant chaque nouvel engagement.</li>"
     "<li><strong>Vérifiez la branche :</strong> ménage privé, culture, design, médias, musée, chœur ? Alors "
     "cotisations dès le premier franc.</li>"
     "<li><strong>Notez l'âge de la personne engagée</strong> (règle des petits boulots d'appoint jusqu'à 25 "
     "ans dans les ménages privés).</li>"
     "<li><strong>Documentez toute demande de cotisations</strong> si la personne souhaite qu'elles soient "
     "versées.</li>"
     "<li><strong>Prévoyez l'obligation d'impôt à la source</strong> dès le premier franc en cas de domicile "
     "à l'étranger.</li>"
     "<li><strong>Établissez et conservez le certificat de salaire</strong> même pour les mini-jobs "
     "(10 ans).</li></ol>"),
    ("En bref",
     "<ul><li>Jusqu'à CHF 2'500 de salaire par personne et par employeur dans l'année civile : pas de "
     "cotisations AVS/AI/APG/AC — sauf si la personne les exige (notice 2.04 ; limite en vigueur depuis le "
     "1.1.2025).</li>"
     "<li>Dépassement = cotisations sur l'entier du salaire (seuil, pas de franchise) — rappel rétroactif "
     "avec intérêts moratoires.</li>"
     "<li>Ménages privés et domaine culture/médias (étendu dès 2026 au design, aux musées, aux médias et "
     "aux chœurs) : cotisations dès le premier franc.</li>"
     "<li>L'employeur répond, selon l'Art. 52 AHVG, des parts salariales non déduites.</li>"
     "<li>L'impôt à la source en cas de domicile à l'étranger s'applique indépendamment de la limite "
     "AHV.</li>"
     "<li>Information générale, sans conseil individualisé — les questions se règlent avec la caisse de "
     "compensation compétente.</li></ul>"),
]

if __name__ == "__main__":
    build("en", SLUG, EN_TITLE, EN_META, EN_SECTIONS, related=RELATED)
    build("fr", SLUG, FR_TITLE, FR_META, FR_SECTIONS, related=RELATED)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for lang in ("en", "fr"):
        p = os.path.join(base, lang, SLUG + ".html")
        print(f"FILE_BYTES {lang} {os.path.getsize(p)}")
