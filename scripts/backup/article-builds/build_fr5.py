#!/usr/bin/env python3
# FR translation of ahv-mindestbeitrag-selbststaendige (vouvoiement)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import article_template as at

def P(s): return f'<p>{s}</p>'
def UL(items): return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def OL(items): return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

at.build('fr', 'ahv-mindestbeitrag-selbststaendige',
 "AVS 2026 : cotisation minimale de CHF 530 et barème des indépendants",
 "Cotisations AVS/AI/APG des indépendants en 2026 : 10 % au total (AVS 8,1, AI 1,4, APG 0,5), barème dégressif sous CHF 60'500, cotisation minimale CHF 530. Plus les rentes 2026 et la 13e rente dès décembre 2026.",
 [
 ("Ce que paient les indépendants",
  P("Les travailleurs indépendants paient <strong>entièrement à leur charge</strong> les cotisations AVS, AI et APG – aucun employeur n'en reprend la moitié. Taux 2026 : AVS 8,1 % + AI 1,4 % + APG 0,5 % = <strong>10,0 pour cent au total</strong> du revenu net de l'activité indépendante. Pour comparaison : salariés et employeurs se partagent 10,6 % à raison de 5,3 % chacun.")),
 ("Le barème dégressif : revenu moindre, taux moindre",
  P("Pour un revenu annuel <strong>inférieur à CHF 60'500</strong>, un taux réduit s'applique – le « barème dégressif » (notice AVS 2.02). Il démarre à <strong>5,371 pour cent</strong> pour les revenus dès CHF 10'100 et monte par paliers jusqu'au taux plein de 10,0 pour cent dès CHF 60'500. Exemple : avec CHF 40'500 de revenu, vous payez 6,728 % ≈ CHF 2'725 au lieu des 4'050 francs attendus. Le revenu déterminant est le revenu net fixé par votre caisse de compensation par décision de cotisation.")),
 ("Cotisation minimale : CHF 530",
  P("Si votre revenu annuel est inférieur à CHF 10'100, vous payez la <strong>cotisation minimale de CHF 530 par an</strong> (elle correspond à un salaire annuel de CHF 5'000). Les personnes sans activité lucrative paient aussi 530 francs au minimum et CHF 26'500 au maximum. Qui a déjà versé la cotisation minimale sur un salaire peut demander que les cotisations sur l'activité indépendante soient perçues seulement au taux le plus bas du barème (5,371 %).")
  + P("À titre accessoire : si votre activité indépendante est exercée à titre professionnel accessoire et rapporte au maximum CHF 2'500 par an, des cotisations ne sont perçues que sur votre demande expresse (notice 2.02).")),
 ("Rentes AVS 2026",
  P("La rente complète (durée de cotisations entière) se situe en 2026 entre <strong>CHF 1'260 et CHF 2'520 par mois</strong> – soit <strong>15'120 à 30'240 francs par an</strong> (OFAS). Les époux reçoivent deux rentes individuelles, plafonnées ensemble à 150 pour cent de la rente maximale : au plus <strong>CHF 3'780 par mois</strong> (45'360 par an). Le montant dépend de la durée de cotisations et du revenu moyen.")),
 ("La 13e rente AVS arrive – pour la première fois en décembre 2026",
  P("Le peuple a accepté la 13e rente de vieillesse. Elle sera versée <strong>pour la première fois avec la rente de décembre 2026</strong> en complément : un douzième (8,333 pour cent) de toutes les rentes mensuelles perçues de janvier à décembre 2026. Qui touche une rente de vieillesse en décembre 2026 recevra le complément automatiquement de la caisse de compensation AVS – aucune demande n'est nécessaire.")),
 ("Erreurs fréquentes",
  UL([
   "<strong>Confondre les bases de cotisation :</strong> le revenu déterminant est le bénéfice net de l'activité indépendante selon la taxation, pas un « salaire ».",
   "<strong>Intérêt moratoire de 5 % :</strong> payer la facture annuelle plus de 30 jours après sa date la rend nettement plus chère.",
   "<strong>Cotisation minimale double</strong> malgré l'imputation du salaire – corrigeable avec justificatif.",
   "<strong>Caisse d'allocations familiales oubliée :</strong> selon le canton, une cotisation aux allocations familiales s'ajoute aux 10 %."])),
 ("En bref",
  OL([
   "Indépendants : 10,0 % AVS/AI/APG (8,1 + 1,4 + 0,5), taux plein dès CHF 60'500.",
   "En dessous, barème dégressif dès 5,371 % (dès CHF 10'100) ; en dessous : cotisation minimale CHF 530.",
   "Rentes 2026 : 1'260–2'520 CHF/mois (15'120–30'240 CHF/an), max couple 3'780 CHF/mois.",
   "13e rente AVS : premier complément avec la rente de décembre 2026, automatique."])
  + P("Vous voulez savoir comment optimiser vos cotisations et ce que coûtent les lacunes de cotisation ? Via la <a href=\"kontakt.html\">page de contact</a>, nous vous mettons en relation avec un partenaire vérifié – premier devis transparent, avant tout mandat.")),
 ])
print("FR5 done")
