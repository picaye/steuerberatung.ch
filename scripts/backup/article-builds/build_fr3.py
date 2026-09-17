#!/usr/bin/env python3
# FR translation of hypothek-steuerabzug-schweiz (vouvoiement)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import article_template as at

def P(s): return f'<p>{s}</p>'
def UL(items): return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def OL(items): return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

at.build('fr', 'hypothek-steuerabzug-schweiz',
 "Hypothèque et impôts : intérêts, déduction et limites",
 "Déduire les intérêts hypothécaires en 2026 : intérêts passifs privés jusqu'au revenu de la fortune plus CHF 50'000 (art. 33 al. 1 let. a LIFD). Comment les déclarer correctement – et ce que vous NE POUVEZ PAS déduire.",
 [
 ("Le principe : valeur locative contre déductions",
  P("Qui vit dans son propre bien immobilier déclare la <strong>valeur locative</strong> – un loyer fictif ajouté au revenu. En contrepartie, vous pouvez déduire les frais de l'objet : avant tout les intérêts hypothécaires, l'entretien et les contributions aux économies d'énergie et de protection. Le système vise à traiter fiscalement de façon comparable la propriété louée et la propriété occupée – ce n'est pas un cadeau.")),
 ("Intérêts hypothécaires : déductibles, mais plafonnés",
  P("Les intérêts hypothécaires d'un bien occupé par son propriétaire sont des <strong>intérêts passifs privés</strong>. À l'impôt fédéral direct, ils sont déductibles – mais pas sans limite : seulement à concurrence des <strong>revenus bruts imposables de la fortune augmentés de CHF 50'000</strong> (art. 33 al. 1 let. a LIFD). Si vos revenus de la fortune (intérêts, dividendes, loyers) sont modestes, le plafond s'applique : tout ce que la banque vous facture sur l'année ne passe pas dans la déclaration. Les cantons traitent les intérêts passifs privés différemment – pour votre déclaration, c'est le droit cantonal qui compte.")),
 ("Déclarer correctement : état des dettes, formulaire 14",
  P("Inscrivez toutes les hypothèques et tous les emprunts dans l'<strong>état des dettes (formulaire 14)</strong> : créancier, dette résiduelle au 31 décembre, montant des intérêts. La pièce justificative est l'<strong>attestation d'intérêts de votre banque</strong> – sans elle, l'autorité fiscale refuse la déduction. La dette réduit en outre votre fortune imposable ; l'impôt sur la fortune baisse.")),
 ("Ce que vous NE POUVEZ PAS déduire",
  UL([
   "<strong>Intérêts du crédit de construction pendant la phase de construction :</strong> ce sont des coûts d'acquisition du bâtiment, pas une déduction du revenu – récupérables plus tard via l'amortissement des coûts de construction.",
   "<strong>Frais de luxe :</strong> les aménagements à caractère luxueux (jacuzzi, spa intégré sur mesure) sont régulièrement refusés comme entretien par les autorités fiscales.",
   "<strong>Règles inventées :</strong> un « abattement de 5 % sur le capital emprunté » n'existe pas davantage que des formulaires « auprès de l'AVS » – l'AVS n'a jamais été compétente en matière d'hypothèques."])),
 ("Stratégie : amortir ou pas ?",
  P("Des intérêts hypothécaires plus élevés rendent l'amortissement attrayant : chaque échelon remboursé économise des intérêts futurs – mais réduit aussi votre déduction et augmente nettement votre revenu imposable. Qui se situe près du plafond des intérêts passifs privés s'en sort souvent mieux en amortissant qu'en comptant sur une déduction d'intérêts (bloquée). La comparaison valeur locative/déductions est une affaire cantonale et individuelle – c'est ici qu'un conseil personnalisé porte le plus ses fruits.")),
 ("En bref",
  OL([
   "Les intérêts hypothécaires sont déductibles – mais les intérêts passifs privés sont plafonnés, à l'échelon fédéral, au revenu de la fortune + CHF 50'000 (art. 33 al. 1 let. a LIFD).",
   "Déclaration dans l'état des dettes, formulaire 14 ; justificatif = attestation d'intérêts de la banque.",
   "Les intérêts de la phase de construction sont des coûts d'acquisition, pas des déductions du revenu.",
   "Vérifier les différences cantonales – notamment en matière d'amortissement et de valeur locative."])
  + P("Vous hésitez sur le plafond de vos déductions ? Via la <a href=\"kontakt.html\">page de contact</a>, nous trouvons un partenaire vérifié de votre région – devis avant tout mandat.")),
 ])
print("FR3 done")
