#!/usr/bin/env python3
"""Translate kapitalsteuer-ag-gmbh.html (DE source) into EN and FR site pages.

Uses scripts/article_template.py build() so chrome (switcher, hreflang,
canonical, JSON-LD, related block) is emitted by the template.
Figures kept EXACTLY as in DE: 0.75 per mille, CHF 2 million, CHF 1'725,
115 %, 0.01 per mille, 7 per mille, 30 %, CHF 500, CHF 50'000, 8.5 %, 35 %,
sections 86 and 88 of the Aargau Tax Act (FR: art. 86/88, values identical).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build  # noqa: E402

SLUG = "kapitalsteuer-ag-gmbh"
RELATED = [
    "verrechnungssteuer-schweiz-35-prozent.html",
    "dividenden-ahv-pflicht-bge-9c-532-2025.html",
    "transparenzregister-tjpg-meldepflicht.html",
]

# ---------------------------------------------------------------- English ---
EN_TITLE = "Capital tax for AG and GmbH: what companies pay even in loss years"
EN_META = ("Not every canton taxes capital, but those that do collect annually – "
           "with no profit in sight. How the capital tax works: levied on equity "
           "capital, credit of the profit tax, minimum tax, cantonal rates between "
           "0 and 7 per mille – and why capital reductions and liquidations must "
           "be modelled through.")

EN_SECTIONS = [
    ("What the capital tax levies on",
     "<p>The capital tax is a <strong>cantonal tax on the taxable equity capital</strong> "
     "of a corporation: stock corporations (AG), limited liability companies (GmbH) and "
     "cooperatives are taxed annually on their balance-sheet equity capital (share capital "
     "plus statutory and voluntary reserves, depending on cantonal law) – "
     "<strong>regardless of whether the company makes a profit</strong>. A loss year does "
     "not exempt you; the tax is still due.</p>"
     "<p>At federal level there is no capital tax – the direct federal tax knows only the "
     "profit tax (8.5 %). Pure profit-tax cantons are rare: the majority of cantons levy a "
     "capital tax, though in very different designs. The canton of Uri, for example, waives "
     "it entirely at cantonal level (FTA publication «Steuersatz und Steuerfuss», as of "
     "1.1.2026), while Uri's communes levy proportional rates between 0.01 and 4 per mille.</p>"),
    ("Rates and tax multipliers: a tour",
     "<p>The statutory rates move in the per-mille range. Example Aargau: "
     "<strong>0.75 per mille of taxable equity capital</strong> (§ 86 para. 1 of the Aargau "
     "Tax Act); at a multiplier of 115 % (2026) that works out to around "
     "<strong>CHF 1'725 capital tax</strong> per year for a company with CHF 2 million of "
     "equity capital. The canton of Lucerne applies a fixed capital tax of only "
     "0.01 per mille to the share of equity capital attributable to participations, patents "
     "and comparable rights as well as intra-group receivables – the typical holding "
     "arrangement (FTA, op. cit.).</p>"
     "<p>The burden is not capped everywhere: the canton of Vaud provides by law that "
     "cantonal and communal taxes together may not exceed <strong>7 per mille of taxable "
     "capital</strong> (and 30 % of taxable net profit). The majority of cantons, by "
     "contrast, provide <strong>no overall burden cap</strong> for legal entities.</p>"),
    ("Tax credit: the double burden has a damper",
     "<p>Many cantons soften the combination of profit tax and capital tax by "
     "<strong>crediting the profit tax against the capital tax</strong> – expressly so in "
     "Aargau (§ 86 para. 4 of the Aargau Tax Act). In practice this means: in profitable "
     "years the capital tax has often already been «absorbed»; the company effectively pays "
     "it on top mainly when the capital tax exceeds the profit tax – i.e. in weak and loss "
     "years.</p>"
     "<p>Minimum taxes remain: corporations and cooperatives pay a minimum tax of "
     "<strong>CHF 500</strong> in Aargau (simple 100 % cantonal tax, § 88 of the Aargau Tax "
     "Act) – even with zero profit and zero capital yield. Associations and foundations "
     "become subject to the capital tax only from <strong>CHF 50'000</strong> of equity "
     "capital (§ 86 para. 3 of the Aargau Tax Act).</p>"),
    ("Who really feels the burden?",
     "<p>The capital tax is a <strong>wealth tax on company money</strong>. Three "
     "constellations hurt:</p>"
     "<ul><li><strong>Cash-rich, profit-poor companies:</strong> saved reserves increase "
     "the equity capital and thus the tax, without any profit having flowed – the tax "
     "becomes a pure liquidity burden.</li>"
     "<li><strong>Loss years:</strong> profit tax zero, capital tax full – the credit "
     "misses its target.</li>"
     "<li><strong>Reorganisation cases:</strong> before capital reductions, "
     "restructurings and liquidations, the capital tax belongs in the modelling: until the "
     "company is struck off the tax is owed annually; a staged capital reduction can lower "
     "it, but depending on the construction it triggers questions on repayment of the "
     "issuance stamp tax or withholding tax.</li></ul>"),
    ("A cantonal location factor – and a permanent political debate",
     "<p>The capital tax is a genuine location criterion: between «no cantonal capital "
     "tax» (Uri) and several per mille including the communal share lie worlds – added to "
     "the profit tax, it burdens capital-intensive models over years. Individual cantons "
     "have cut rates or created special rules for holding substance; the political debate "
     "on total abolition regularly returns at cantonal level.</p>"
     "<p>For practice this means: whoever founds, holds, restructures or liquidates an AG "
     "or GmbH checks the domicile canton's capital tax <strong>anew every year</strong> – "
     "rates, multipliers and credit models change more often than the profit tax.</p>"),
    ("Checklist for AG/GmbH shareholders",
     "<ol><li><strong>Keep a standing register:</strong> taxable equity capital per year "
     "incl. changes in reserves.</li>"
     "<li><strong>Compare cantons:</strong> know the rate, multiplier, credit model and "
     "minimum tax of the domicile canton (FTA «Steuersatz und Steuerfuss» as starting "
     "point).</li>"
     "<li><strong>Plan for loss years:</strong> capital tax + minimum tax flow regardless "
     "of the result.</li>"
     "<li><strong>Reserve policy:</strong> retention decisions raise the capital tax base – "
     "compute dividend vs. reserve on the total effect (incl. 35 % withholding tax).</li>"
     "<li><strong>Model restructurings:</strong> capital reduction, partial liquidation, "
     "liquidation – capital tax savings vs. issuance stamp tax and withholding tax "
     "consequences.</li>"
     "<li><strong>Revalidate annually:</strong> multipliers are often changed.</li></ol>"),
    ("In short",
     "<ul><li>Capital tax = cantonal annual tax on the equity capital of AG/GmbH/"
     "cooperatives – also in loss years.</li>"
     "<li>The federal tax knows no capital tax; cantonal rates lie in the per-mille range "
     "(example Aargau 0.75 ‰; Uri at cantonal level: none; Vaud cap 7 ‰).</li>"
     "<li>The profit tax is usually credited – effectively you pay capital tax mainly in "
     "weak results; minimum taxes remain (Aargau: CHF 500).</li>"
     "<li>In capital reductions and liquidations it belongs in the overall modelling.</li>"
     "<li>General information, not individual advice – engage a fiduciary or tax "
     "expert.</li></ul>"),
]

# ----------------------------------------------------------------- French ---
FR_TITLE = "Impôt sur le capital des SA et Sàrl : ce que paient les entreprises même en année déficitaire"
FR_META = ("Tous les cantons ne taxent pas le capital, mais ceux qui le font perçoivent "
           "l'impôt chaque année – même sans bénéfice. Comment fonctionne l'impôt sur le "
           "capital : assis sur le capital propre, imputation de l'impôt sur le bénéfice, "
           "impôt minimal, taux cantonaux entre 0 et 7 pour mille – et pourquoi les "
           "réductions de capital et les liquidations doivent être chiffrées.")

FR_SECTIONS = [
    ("Ce que frappe l'impôt sur le capital",
     "<p>L'impôt sur le capital est un <strong>impôt cantonal sur le capital propre "
     "imposable</strong> d'une société de capitaux : les sociétés anonymes (SA), les Sàrl "
     "et les coopératives sont taxées chaque année sur leurs capitaux propres au bilan "
     "(capital social majoré des réserves légales et volontaires, selon le droit cantonal) – "
     "<strong>que l'entreprise réalise ou non un bénéfice</strong>. Une année déficitaire "
     "ne dispense pas de l'impôt ; il reste dû.</p>"
     "<p>Au niveau fédéral, il n'existe pas d'impôt sur le capital – l'impôt fédéral direct "
     "ne connaît que l'impôt sur le bénéfice (8,5 %). Les cantons à impôt uniquement sur le "
     "bénéfice sont rares : la majorité des cantons perçoivent un impôt sur le capital, "
     "mais dans des configurations très différentes. Le canton d'Uri, par exemple, y "
     "renonce totalement au niveau cantonal (publication de l'AFC «Steuersatz und "
     "Steuerfuss», état au 1.1.2026), tandis que les communes uranaises perçoivent des "
     "taux proportionnels entre 0,01 et 4 pour mille.</p>"),
    ("Taux et multiplicateurs : un tour d'horizon",
     "<p>Les taux légaux se situent dans la fourchette des pour mille. Exemple Argovie : "
     "<strong>0,75 pour mille du capital propre imposable</strong> (art. 86 al. 1 de la loi "
     "fiscale argovienne) ; avec un multiplicateur de 115 % (2026), cela donne environ "
     "<strong>CHF 1'725 d'impôt sur le capital</strong> par an pour une entreprise dotée de "
     "CHF 2 millions de capital propre. Le canton de Lucerne applique un impôt sur le "
     "capital fixe de seulement 0,01 pour mille à la part du capital propre correspondant "
     "aux participations, brevets et droits comparables ainsi qu'aux créances intra-groupe "
     "– le régime typique des holdings (AFC, op. cit.).</p>"
     "<p>La charge n'est pas plafonnée partout : le canton de Vaud prescrit légalement que "
     "les impôts cantonal et communal ne dépassent pas ensemble <strong>7 pour mille du "
     "capital imposable</strong> (et 30 % du bénéfice net imposable). La majorité des "
     "cantons ne prévoient en revanche <strong>aucun plafond de charge</strong> pour les "
     "personnes morales.</p>"),
    ("Imputation : le double fardeau a un amortisseur",
     "<p>De nombreux cantons atténuent la combinaison impôt sur le bénéfice et impôt sur le "
     "capital en <strong>imputant l'impôt sur le bénéfice sur l'impôt sur le capital</strong> "
     "– c'est expressément le cas en Argovie (art. 86 al. 4 de la loi fiscale argovienne). "
     "En pratique : les années rentables, l'impôt sur le capital est souvent « déjà "
     "absorbé » ; l'entreprise ne le paie réellement en sus que lorsque l'impôt sur le "
     "capital dépasse l'impôt sur le bénéfice – donc dans les années faibles et "
     "déficitaires.</p>"
     "<p>Les impôts minimaux subsistent : en Argovie, les sociétés de capitaux et les "
     "coopératives acquittent un impôt minimal de <strong>CHF 500</strong> (impôt cantonal "
     "simple à 100 %, art. 88 de la loi fiscale argovienne) – même avec bénéfice nul et "
     "rendement du capital nul. Les associations et les fondations ne sont soumises à "
     "l'impôt sur le capital qu'à partir de <strong>CHF 50'000</strong> de capital propre "
     "(art. 86 al. 3 de la loi fiscale argovienne).</p>"),
    ("Qui ressent vraiment la charge ?",
     "<p>L'impôt sur le capital est un <strong>impôt sur la fortune appliqué à l'argent de "
     "l'entreprise</strong>. Trois configurations font mal :</p>"
     "<ul><li><strong>Trésoreries riches, rentabilité naine :</strong> les réserves "
     "épargnées augmentent le capital propre et donc l'impôt, sans qu'un bénéfice ait été "
     "réalisé – l'impôt devient une pure charge de liquidité.</li>"
     "<li><strong>Années déficitaires :</strong> impôt sur le bénéfice nul, impôt sur le "
     "capital intégral – l'imputation tombe à faux.</li>"
     "<li><strong>Opérations de restructuration :</strong> avant toute réduction de "
     "capital, réorganisation ou liquidation, l'impôt sur le capital doit entrer dans le "
     "calcul : jusqu'à la radiation, l'impôt est dû chaque année ; une réduction de capital "
     "échelonnée peut le baisser, mais selon le montage elle soulève des questions de "
     "restitution du droit de timbre d'émission ou déclenche l'impôt anticipé.</li></ul>"),
    ("Un facteur d'emplacement cantonal – et un débat politique récurrent",
     "<p>L'impôt sur le capital est un vrai critère d'emplacement : entre « pas d'impôt "
     "cantonal sur le capital » (Uri) et plusieurs pour mille compris la part communale, il "
     "y a un monde – additionné à l'impôt sur le bénéfice, il pèse des années durant sur "
     "les modèles intensifs en capital. Certains cantons ont abaissé leurs taux ou créé des "
     "régimes spéciaux pour la substance de holding ; le débat politique sur une abolition "
     "complète revient régulièrement au niveau cantonal.</p>"
     "<p>Pour la pratique : quiconque fonde, détient, restructure ou liquide une SA ou une "
     "Sàrl vérifie <strong>chaque année</strong> l'impôt sur le capital du canton de "
     "domicile – les taux, les multiplicateurs et les modèles d'imputation changent plus "
     "souvent que l'impôt sur le bénéfice.</p>"),
    ("Check-list pour les associés de SA/Sàrl",
     "<ol><li><strong>Tenir un registre :</strong> capital propre imposable par année, y "
     "compris les variations des réserves.</li>"
     "<li><strong>Comparer les cantons :</strong> connaître le taux, le multiplicateur, le "
     "modèle d'imputation et l'impôt minimal du canton de domicile (publication AFC "
     "«Steuersatz und Steuerfuss» comme point de départ).</li>"
     "<li><strong>Prévoir les années déficitaires :</strong> impôt sur le capital + impôt "
     "minimal sont dus indépendamment du résultat.</li>"
     "<li><strong>Politique de réserves :</strong> les décisions de mise en réserve "
     "augmentent la base de l'impôt sur le capital – dividende ou réserve : calculer "
     "l'effet global (y compris l'impôt anticipé de 35 %).</li>"
     "<li><strong>Chiffrer les restructurations :</strong> réduction de capital, liquidation "
     "partielle, liquidation – économie d'impôt sur le capital contre conséquences en droit "
     "de timbre d'émission et en impôt anticipé.</li>"
     "<li><strong>Revalider chaque année :</strong> les multiplicateurs sont souvent "
     "modifiés.</li></ol>"),
    ("En bref",
     "<ul><li>Impôt sur le capital = impôt cantonal annuel sur le capital propre des "
     "SA/Sàrl/coopératives – y compris en année déficitaire.</li>"
     "<li>L'impôt fédéral ne connaît pas d'impôt sur le capital ; les taux cantonaux se "
     "situent dans les pour mille (exemple Argovie 0,75 ‰ ; Uri au niveau cantonal : aucun ; "
     "Vaud : plafond de 7 ‰).</li>"
     "<li>L'impôt sur le bénéfice est généralement imputé – en pratique, on paie surtout "
     "l'impôt sur le capital en cas de résultats faibles ; les impôts minimaux subsistent "
     "(Argovie : CHF 500).</li>"
     "<li>Lors d'une réduction de capital ou d'une liquidation, il doit entrer dans le "
     "calcul d'ensemble.</li>"
     "<li>Information générale, pas de conseil individuel – faire appel à un fiduciaire ou "
     "à un expert fiscal.</li></ul>"),
]

if __name__ == "__main__":
    build("en", SLUG, EN_TITLE, EN_META, EN_SECTIONS, related=RELATED)
    build("fr", SLUG, FR_TITLE, FR_META, FR_SECTIONS, related=RELATED)
