#!/usr/bin/env python3
"""Translate quellensteuer-nov-zusatzabzuege.html (DE source) into EN and FR site pages.

Uses scripts/article_template.py build() so chrome (switcher, hreflang,
canonical, JSON-LD, related block) is emitted by the template.
Terminology per references/multilang-glossary.md and existing site pages:
Quellensteuer = source tax (EN, as on en/expats + en/grenzgaenger pages) /
impôt à la source (FR); NOV = subsequent ordinary assessment (NOV, EN) /
taxation ordinaire ultérieure (TOU, FR); Zusatzabzüge = additional
deductions / déductions ultérieures; DBG = FATA (EN) / LIFD (FR);
StHG = Tax Harmonisation Act (EN) / LHID (FR); ESTV = FTA / AFC.
Figures kept EXACTLY as in DE: 31 March / 31.3.2027, CHF 120'000,
30 days, 15–25 %, CHF 1'500–3'000, CHF 12'000, pillar 3a / pilier 3a,
Art. 137 DBG, Art. 49 Abs. 2–2ter StHG.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build  # noqa: E402

SLUG = "quellensteuer-nov-zusatzabzuege"
RELATED = [
    "grenzgaenger-de-fr-it-steuern.html",
    "expats-steuern-schweiz.html",
    "saeule-3a-nachzahlen.html",
]

# ---------------------------------------------------------------- English ---
EN_TITLE = "Source tax: claim additional deductions by 31 March"
EN_META = ("Illness costs, further training, real professional expenses, third-party "
           "childcare: deductions the source tax rate does not contain are only "
           "available through the subsequent ordinary assessment (NOV). Application "
           "deadline: 31 March of the following year – for the 2026 period, until "
           "31.3.2027. Who must apply, who should, and what it brings.")

EN_SECTIONS = [
    ("Why the source tax rate deducts too little",
     "<p>The source tax deduction is a <strong>flat-rate final tax</strong>: the rate "
     "only includes professional expenses, insurance premiums and deductions on a "
     "lump-sum basis. Anyone with higher actual costs – effective professional "
     "expenses instead of the flat rate, illness and accident costs, further "
     "training, third-party childcare costs, pillar 3a contributions, maintenance "
     "payments – sees none of it in the monthly payslip.</p>"
     "<p>These <strong>additional deductions</strong> can only be obtained through "
     "the subsequent ordinary assessment (NOV): the tax authority assesses you as in "
     "the ordinary procedure, credits the source tax already paid, and refunds the "
     "difference if it turned out too high.</p>"),
    ("The deadline: 31 March of the following year",
     "<p>The application for a subsequent ordinary assessment is <strong>tied to a "
     "hard deadline</strong>: it must reach the cantonal tax authority by "
     "<strong>the end of March of the year following the tax period</strong> (FTA "
     "information sheet «Besteuerung an der Quelle»; likewise the canton of Zurich's "
     "source tax ordinance: «bis Ende März des Folgejahres» – until the end of March "
     "of the following year; confirmed by the Fribourg and Thurgau tax authorities "
     "for period practice). For the <strong>2026 tax period the deadline expires on "
     "31 March 2027</strong>.</p>"
     "<p>Anyone who misses the deadline loses the deductions without a trace: "
     "without an NOV, the source tax definitively replaces the federal, cantonal and "
     "communal taxes on employment income – no additional deductions are granted "
     "afterwards.</p>"),
    ("Who must apply, who should apply",
     "<p>The NOV is <strong>mandatory</strong> for persons subject to source tax with "
     "domicile or residence in Switzerland if their gross income exceeds "
     "<strong>CHF 120'000 per year</strong> (FTA information sheet). Here the "
     "assessment is made ex officio – the application itself is unnecessary, but the "
     "additional deductions must still be claimed.</p>"
     "<p><strong>Voluntarily</strong>, the application pays off for everyone else "
     "whose actual deductions exceed the flat allowances built into the rate. "
     "Typical candidates: people with high real travel and meal costs, families with "
     "third-party childcare, people with illness costs above the deductible "
     "franchises, payers of maintenance.</p>"
     "<p><strong>Non-residents</strong> (cross-border commuters, persons staying "
     "abroad) can also apply for the NOV to claim personal deductions – for them the "
     "procedure is the only route to these deductions; the application must likewise "
     "be filed by 31 March of the following year.</p>"),
    ("Correction vs. additional deductions: two different applications",
     "<p>Not every correction needs an NOV: if the <strong>gross salary was "
     "determined wrongly, the income governing the rate was calculated incorrectly, "
     "or the wrong rate was applied</strong>, an application to recalculate the "
     "source tax suffices (Art. 137 FATA, Art. 49 para. 2–2ter of the Tax "
     "Harmonisation Act) – also by 31 March of the following year. The NOV, by "
     "contrast, opens up the entire deduction logic of ordinary assessment, "
     "including personal circumstances (marital status, children, assets).</p>"),
    ("How the application works",
     "<p>The form is available from the cantonal tax authority (in many cantons it "
     "is available online every year from 1 January to 31 March). Married couples "
     "and registered partnerships must <strong>sign the application jointly</strong>; "
     "it must state the tax period. Enclose the usual supporting documents: salary "
     "certificates, proof of professional expenses, illness costs, 3a contributions, "
     "childcare and maintenance costs. The assessment follows ordinary law; the "
     "source tax withheld is credited. The FTA normally issues the assessment by the "
     "end of the application year – after that, the ordinary remedies run "
     "(objection within 30 days).</p>"),
    ("Calculation example: when the application pays off",
     "<p>Rule of thumb: the source tax rate contains a flat allowance for "
     "professional expenses. If the actual costs (commuting, meals, further "
     "training, home office) are clearly above it, the deduction rises by the "
     "difference. By way of example: someone who can prove CHF 12'000 of real "
     "professional expenses instead of the rate's flat allowance of a few thousand "
     "francs lowers their taxable income accordingly – at a marginal rate of 15–25 % "
     "that means a refund in the range of CHF 1'500–3'000 per year. The exact "
     "calculation depends on canton, commune, marital status and children; cantonal "
     "tax authorities and cantonal tax software allow a rough estimate before you "
     "apply.</p>"),
    ("In short",
     "<ul><li>Additional deductions (actual professional expenses, illness, further "
     "training, third-party childcare, pillar 3a, maintenance) are only available "
     "with a subsequent ordinary assessment (NOV).</li>"
     "<li>Deadline: 31 March of the following year – for the 2026 period until "
     "31.3.2027. Without an application, the deductions lapse.</li>"
     "<li>Mandatory from gross income above CHF 120'000 (residents); voluntary for "
     "everyone else, including cross-border commuters.</li>"
     "<li>Wrong rate/incorrect salary → recalculation application (Art. 137 FATA / "
     "Art. 49 Tax Harmonisation Act), same deadline.</li>"
     "<li>General information, not individual advice – the cantonal tax authority "
     "provides guidance.</li></ul>"),
]

# ----------------------------------------------------------------- French ---
FR_TITLE = "Impôt à la source : déclarer vos déductions ultérieures jusqu'au 31 mars"
FR_META = ("Frais de maladie, formation continue, frais professionnels effectifs, "
           "garde par des tiers : les déductions que le tarif de l'impôt à la source "
           "ne contient pas ne s'obtiennent que par la taxation ordinaire ultérieure "
           "(TOU). Requête jusqu'au 31 mars de l'année suivante – pour la période "
           "2026 donc jusqu'au 31.3.2027. Qui doit la déposer, qui devrait le faire, "
           "et ce qu'elle rapporte.")

FR_SECTIONS = [
    ("Pourquoi le tarif de l'impôt à la source déduit trop peu",
     "<p>Le prélèvement à la source est un <strong>impôt définitif forfaitaire</strong> : "
     "le tarif ne contient les frais professionnels, les primes d'assurance et les "
     "déductions que de manière forfaitaire. Quiconque a des coûts réels plus élevés – "
     "frais professionnels effectifs au lieu du forfait, frais de maladie et "
     "d'accident, formation continue, frais de garde par des tiers, cotisations au "
     "pilier 3a, pensions alimentaires – n'en voit rien sur le décompte mensuel.</p>"
     "<p>Ces <strong>déductions ultérieures</strong> ne peuvent être obtenues que par "
     "la taxation ordinaire ultérieure (TOU) : l'autorité fiscale vous taxe comme "
     "dans la procédure ordinaire, impute l'impôt à la source déjà perçu et restitue "
     "la différence s'il s'est avéré trop élevé.</p>"),
    ("Le délai : le 31 mars de l'année suivante",
     "<p>La requête en taxation ordinaire ultérieure est <strong>soumise à un délai "
     "impératif</strong> : elle doit parvenir à l'administration fiscale cantonale "
     "<strong>fin mars de l'année suivant la période fiscale</strong> (notice de "
     "l'AFC «Besteuerung an der Quelle» ; de même l'ordonnance zurichoise sur l'impôt "
     "à la source : «jusqu'à fin mars de l'année suivante» ; confirmé par les "
     "administrations fiscales FR et TG pour la pratique des périodes). Pour la "
     "<strong>période fiscale 2026, le délai expire le 31 mars 2027</strong>.</p>"
     "<p>Qui rate le délai perd les déductions sans bruit : sans TOU, l'impôt à la "
     "source se substitue définitivement aux impôts fédéral, cantonal et communal sur "
     "le revenu de l'activité lucrative – aucune déduction supplémentaire n'est "
     "alors accordée.</p>"),
    ("Qui doit déposer la requête, qui devrait le faire",
     "<p>La TOU est <strong>obligatoire</strong> pour les personnes soumises à l'impôt "
     "à la source domiciliées ou en séjour en Suisse lorsque le revenu brut dépasse "
     "<strong>CHF 120'000 par an</strong> (notice de l'AFC). Ici, la taxation a lieu "
     "d'office – la requête n'est pas nécessaire, mais les déductions ultérieures "
     "doivent quand même être demandées.</p>"
     "<p><strong>À titre volontaire</strong>, la requête vaut pour tous les autres "
     "dont les déductions effectives dépassent les forfaits du tarif. Candidats "
     "typiques : personnes à frais réels de trajet et de repas élevés, familles avec "
     "garde par des tiers, personnes ayant des frais de maladie supérieurs aux "
     "franchises déductibles, débiteurs de pensions alimentaires.</p>"
     "<p><strong>Les non-résidents</strong> (frontaliers, personnes en séjour à "
     "l'étranger) peuvent également demander la TOU pour faire valoir des déductions "
     "personnelles – pour eux, cette procédure est la seule voie vers ces déductions ; "
     "la requête doit elle aussi être déposée jusqu'au 31 mars de l'année "
     "suivante.</p>"),
    ("Rectification vs déductions ultérieures : deux requêtes distinctes",
     "<p>Toute correction ne nécessite pas une TOU : si le <strong>salaire brut a été "
     "déterminé à tort, le revenu déterminant le tarif calculé de façon erronée ou un "
     "mauvais tarif appliqué</strong>, la requête en recalcul de l'impôt à la source "
     "suffit (art. 137 LIFD, art. 49 al. 2–2ter LHID) – également jusqu'au 31 mars de "
     "l'année suivante. La TOU, en revanche, ouvre toute la logique de déductions de "
     "la taxation ordinaire, y compris les rapports personnels (état civil, enfants, "
     "fortune).</p>"),
    ("Comment fonctionne la requête",
     "<p>Le formulaire est disponible auprès de l'administration fiscale cantonale "
     "(dans de nombreux cantons, en ligne chaque année du 1er janvier au 31 mars). "
     "Les époux et les partenaires enregistrés doivent <strong>signer la requête "
     "conjointement</strong> ; elle doit désigner la période fiscale. Joignez les "
     "justificatifs habituels : certificats de salaire, preuves des frais "
     "professionnels, frais de maladie, cotisations 3a, frais de garde et pensions "
     "alimentaires. La taxation suit le droit ordinaire ; l'impôt à la source retenu "
     "est imputé. L'AFC notifie la taxation en règle générale jusqu'à la fin de "
     "l'année de la requête – courent ensuite les voies de droit ordinaires "
     "(réclamation dans les 30 jours).</p>"),
    ("Exemple de calcul : quand la requête vaut le coup",
     "<p>Valeur indicative : le tarif de l'impôt à la source contient un forfait pour "
     "les frais professionnels. Si les coûts effectifs (trajets, repas, formation "
     "continue, bureau à domicile) sont nettement supérieurs, la déduction augmente "
     "de la différence. Exemple : qui peut prouver CHF 12'000 de frais "
     "professionnels réels au lieu du forfait tarifaire de quelques milliers de "
     "francs abaisse d'autant son revenu imposable – avec un taux marginal de 15–25 "
     "%, cela représente une restitution de l'ordre de CHF 1'500–3'000 par an. Le "
     "calcul exact dépend du canton, de la commune, de l'état civil et des enfants ; "
     "les administrations fiscales et les logiciels fiscaux cantonaux permettent une "
     "estimation avant la requête.</p>"),
    ("En bref",
     "<ul><li>Les déductions ultérieures (frais professionnels effectifs, maladie, "
     "formation continue, garde par des tiers, pilier 3a, pensions alimentaires) ne "
     "s'obtiennent que par la taxation ordinaire ultérieure (TOU).</li>"
     "<li>Délai : 31 mars de l'année suivante – pour la période 2026 jusqu'au "
     "31.3.2027. Sans requête, les déductions tombent à l'eau.</li>"
     "<li>Obligatoire dès un revenu brut supérieur à CHF 120'000 (résidents) ; "
     "volontaire pour tous les autres, y compris les frontaliers.</li>"
     "<li>Mauvais tarif/salaire erroné → requête en recalcul (art. 137 LIFD / "
     "art. 49 LHID), même délai.</li>"
     "<li>Information générale, pas de conseil individuel – l'administration fiscale "
     "cantonale renseigne.</li></ul>"),
]

if __name__ == "__main__":
    build("en", SLUG, EN_TITLE, EN_META, EN_SECTIONS, related=RELATED)
    build("fr", SLUG, FR_TITLE, FR_META, FR_SECTIONS, related=RELATED)
