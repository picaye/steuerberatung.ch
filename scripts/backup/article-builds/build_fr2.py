#!/usr/bin/env python3
# FR translation of grenzgaenger-de-fr-it-steuern (vouvoiement)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import article_template as at

def P(s): return f'<p>{s}</p>'
def UL(items): return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def OL(items): return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

at.build('fr', 'grenzgaenger-de-fr-it-steuern',
 "Frontaliers DE/FR/IT : impôt à la source de 4,5 % et formulaires",
 "Frontaliers franco-allemands-suisses : 4,5 % d'impôt à la source suisse (art. 15a CDI CH-DE), formulaire Gre-1, 60 jours de non-retour, échéance allemande 31 juillet. FR et IT suivent d'autres règles – l'aperçu 2026.",
 [
 ("Qui est frontalier au sens fiscal",
  P("Vous n'êtes frontalier au sens du droit fiscal que si toutes les conditions sont remplies : domicile à l'étranger (DE, FR ou IT), employeur et lieu de travail en Suisse, <strong>retour quotidien</strong> au domicile – et ce retour doit être raisonnable. En pratique, les cantons admettent : au maximum 100 kilomètres en voiture ou au maximum 1,5 heure en transports publics.")
  + P("Attention : l'autorisation de frontalier (attestation G) est autre chose – elle ne confère pas le statut fiscal de frontalier. Qui ne rentre pas quotidiennement est résident international de semaine et est taxé à la source aux tarifs ordinaires suisses.")),
 ("Allemagne : 4,5 % d'impôt à la source – mais avec Gre-1 seulement",
  P("Les vrais frontaliers allemands sont imposés en Suisse à forfait à <strong>4,5 pour cent du salaire brut</strong> (art. 15a CDI CH-DE). Mais ce n'est pas automatique : vous devez remettre à l'employeur le <strong>certificat de résidence, formulaire Gre-1</strong>, établi par votre fisc allemand. Sans Gre-1, l'employeur facture au tarif ordinaire – souvent nettement plus.")
  + P("Gre-1 vaut pour une année civile et doit être remis à l'employeur chaque année ; après la première année, le fisc allemand le délivre en général automatiquement. Un formulaire distinct est nécessaire par employeur.")),
 ("La limite des 60 jours de non-retour",
  P("Si, pour des raisons professionnelles (voyages d'affaires, astreinte, formation), vous ne rentrez pas chez vous <strong>plus de 60 jours</strong> dans l'année civile, vous perdez le tarif de frontalier. Votre revenu suisse est recalculé aux tarifs ordinaires et taxé ultérieurement. Les jours de non-retour professionnels doivent être certifiés par l'employeur avec le <strong>formulaire Gre-3</strong> – dans le canton de Zurich par écrit, par employeur et au plus tard le <strong>31 mars de l'année suivante</strong> auprès du service fiscal cantonal (le délai varie selon les cantons). Les nuitées privées ne comptent pas.")),
 ("Allemagne : déclaration d'impôt jusqu'au 31 juillet",
  P("Même si la Suisse a perçu 4,5 % : en Allemagne, vous êtes imposable sur l'ensemble de vos revenus et devez déclarer les revenus de frontalier dans votre déclaration d'impôt. Le délai général de dépôt pour la déclaration allemande 2025 expire le <strong>31 juillet 2026</strong> ; avec une assistance fiscale (Lohnsteuerhilfeverein, conseiller fiscal), plus tard. L'impôt suisse à la source est imputé en Allemagne pour éviter une double imposition durable.")),
 ("France et Italie : des règles totalement différentes",
  P("<strong>France :</strong> la convention de frontalier de 1983 ne s'applique qu'aux lieux de travail situés dans les cantons BE, BL, BS, JU, NE, SO, VD et VS. Hors de cette zone – Genève par exemple – c'est la CDI ordinaire qui s'applique, avec impôt à la source suisse au tarif ordinaire et imposition en France avec imputation ; les détails dépendent du canton d'activité.")
  + P("<strong>Italie :</strong> depuis la convention révisée (entrée en vigueur le 17 juillet 2023, applicable dès 2024), les « nouveaux » frontaliers – engagement après le 17 juillet 2023 – peuvent être imposés en Suisse jusqu'à concurrence de 80 pour cent de l'impôt à la source ordinaire ; l'Italie impute cet impôt. Pour les frontaliers engagés avant cette date, une règle transitoire vaut jusqu'à fin 2033. Le télétravail est possible jusqu'à 25 pour cent du temps de travail sans mettre en péril le statut.")),
 ("Les erreurs les plus fréquentes",
  UL([
   "<strong>Attestation G = statut fiscal ?</strong> Non – ce qui compte, c'est le retour quotidien et son caractère raisonnable.",
   "<strong>Oublier Gre-1</strong> → tarif ordinaire au lieu de 4,5 %, correction fastidieuse.",
   "<strong>Jours de non-retour mal documentés</strong> → Gre-3 déposé hors délai, taxation ultérieure au tarif ordinaire.",
   "<strong>« Formulaires 130/140/150 à l'AVS » ?</strong> N'existe pas – l'AVS n'a jamais été compétente pour l'impôt à la source ; les attestations passent par l'employeur et les services fiscaux cantonaux."])),
 ("En bref",
  OL([
   "4,5 % d'impôt à la source suisse pour les vrais frontaliers allemands – avec formulaire Gre-1 remis à l'employeur.",
   "Plus de 60 jours de non-retour professionnels (Gre-3) → tarif ordinaire, taxation ultérieure.",
   "Côté allemand : annexe N-GRE, échéance déclaration 2025 au 31 juillet 2026.",
   "FR : convention de 1983 limitée à 8 cantons frontaliers ; IT : nouveau régime dès 2024 (jusqu'à 80 % d'impôt à la source CH, imputation, transition jusqu'en 2033)."])
  + P("Vous avez passé une année en télétravail avec de nombreux jours de voyage ? C'est exactement là que ça se complique. Via la <a href=\"kontakt.html\">page de contact</a>, nous vous mettons en relation avec un partenaire vérifié – avec un devis transparent avant tout mandat.")),
 ])
print("FR2 done")
