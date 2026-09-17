#!/usr/bin/env python3
# FR translation of verrechnungssteuer-schweiz-35-prozent (vouvoiement, figures identical)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import article_template as at

def P(s): return f'<p>{s}</p>'
def UL(items): return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def OL(items): return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

at.build('fr', 'verrechnungssteuer-schweiz-35-prozent',
 "Impôt anticipé de 35 % : récupérer vos dividendes et intérêts",
 "Impôt anticipé suisse : 35 % sur dividendes et intérêts (art. 13 LIA). Comment le récupérer via la déclaration d'impôt – délai de 3 ans (art. 32 LIA), sans confusion avec le formulaire 110.",
 [
 ("Qu'est-ce que l'impôt anticipé",
  P("L'impôt anticipé est un impôt fédéral sur les revenus du capital : les dividendes, les intérêts et les gains issus de jeux d'argent sont amputés de <strong>35 pour cent</strong> (art. 13 al. 1 let. a LIA). Les rentes viagères et les pensions sont taxées à 15 pour cent, les autres prestations d'assurance à 8 pour cent.")
  + P("Ce n'est pas l'État qui effectue le prélèvement, mais le débiteur : votre banque ou la société retient l'impôt à l'échéance et le verse à l'Administration fédérale des contributions (AFC). Il doit rendre la fraude fiscale sur les revenus du capital plus difficile – c'est pourquoi son taux est volontairement supérieur à votre charge fiscale réelle.")),
 ("L'impôt n'est pas une perte – il est payé d'avance",
  P("Pour les personnes physiques domiciliées en Suisse et pleinement assujetties, l'impôt anticipé n'est pas un impôt définitif mais un impôt de garantie : vous pouvez en demander la restitution si vous déclarez correctement les revenus. Qui ne la réclame pas fait don de son argent – avec un dépôt de CHF 2'000 de dividendes et intérêts, ce sont déjà CHF 700 par an.")),
 ("La voie simple : la déclaration d'impôt",
  P("Si vous déposez une déclaration d'impôt, sa remise vaut en pratique demande de restitution : l'autorité compétente est celle du canton où vous aviez votre domicile à la fin de l'année d'échéance (art. 30 LIA). L'état des titres de la déclaration fait office de demande – les cantons restituent l'impôt en règle générale à concurrence de votre impôt cantonal et communal (art. 31 LIA).")
  + P("Important pour les détenteurs de dépôt : inscrivez tous les dividendes et intérêts, y compris les petits montants, dans l'état des titres. Une position oubliée, c'est exactement ce montant qui manque à la restitution.")),
 ("Sans déclaration d'impôt : formulaire 25",
  P("Qui ne dépose pas de déclaration d'impôt (par exemple parce que son canton de domicile n'en exige pas) demande la restitution avec le <strong>formulaire 25</strong> via le portail de l'AFC. Attention, confusion fréquente : <strong>le formulaire 110 n'est pas pour vous</strong> – il sert à la société débitrice pour annonçer son décompte (dans les 30 jours suivant l'assemblée générale). En tant que particulier, vous n'y récupérez rien.")),
 ("Délai : trois ans après l'année d'échéance",
  P("Le droit à la restitution s'éteint si la demande n'est pas déposée <strong>dans les trois ans suivant la fin de l'année civile</strong> au cours de laquelle la prestation est devenue due (art. 32 al. 1 LIA). Exemple : dividende payé le 15 mai 2023 → échéance du délai le 31 décembre 2026. Un délai manqué est perdu définitivement, même pour de bonnes raisons.")),
 ("Les erreurs fréquentes en un coup d'œil",
  UL([
   "<strong>« Restitution dans les 30 jours »</strong> – faux. Le délai de 30 jours concerne l'annonce de la société débitrice (formulaire 110), pas votre demande.",
   "<strong>« L'impôt est perdu si je ne fais rien »</strong> – il est perdu si vous ne faites rien pendant trois ans. Sinon, on vous le rend.",
   "<strong>« L'impôt à la source étranger est remboursé par la Suisse »</strong> – non, c'est la convention de double imposition applicable qui le gère ; l'impôt anticipé suisse est indépendant de cela."])),
 ("En bref",
  OL([
   "35 % sur dividendes/intérêts, 15 % sur rentes/pensions, 8 % sur autres prestations d'assurance (art. 13 LIA).",
   "Avec la déclaration d'impôt, la déclaration complète vaut demande de restitution auprès du canton de domicile (art. 30 LIA).",
   "Sans déclaration d'impôt : formulaire 25 via le portail de l'AFC.",
   "Délai : 3 ans après la fin de l'année d'échéance (art. 32 al. 1 LIA) – pas 30 jours."])
  + P("Vous n'êtes pas sûr que votre état des titres soit complet ? Via la <a href=\"kontakt.html\">page de contact</a>, nous vous mettons en relation avec un partenaire vérifié de votre canton – le premier devis montre en toute transparence ce que coûte l'examen.")),
 ])
print("FR1 done")
