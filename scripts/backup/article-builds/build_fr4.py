#!/usr/bin/env python3
"""Build the FR translation of mwst-100k-pflicht-schweiz.html via article_template.

Full translation of the DE source (mwst-100k-pflicht-schweiz.html, 2026-09-17).
Glossary (as agreed): MWST=TVA, MwStG=LTVA, ESTV=AFC, Vorsteuerabzug=déduction de
l'impôt préalable, Saldosteuersätze=taux de l'impôt forfaitaire, ausgenommen=
prestations exclues, Steuerperiode=période fiscale. Vouvoiement. Citation style
matches existing FR pages (lowercase «art. 10 al. 2 LTVA», cf. fr/kryptowaehrungen
-steuern-schweiz.html: «art. 16 al. 3 LIFD»).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import article_template as at


def P(s):
    return f'<p>{s}</p>'

def OL(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


TITLE = "TVA dès CHF 100'000 : quand votre entreprise devient assujettie"

META = ("Obligation TVA Suisse : dès CHF 100'000 de chiffre d'affaires mondial "
        "(art. 10 al. 2 LTVA), inscription dans les 30 jours via le formulaire en "
        "ligne de l'AFC, taux 8,1 % / 2,6 %. Seuils, délais et exceptions 2026.")

# ---------------------------------------------------------------- S1
h1 = "Le seuil : 100'000 francs – mondial"
b1 = (
    P("Vous devenez assujetti à la TVA si votre entreprise réalise chaque année "
      "<strong>CHF 100'000 ou plus</strong> avec des prestations non exclues de "
      "l'impôt (art. 10 al. 2 LTVA). Important : c'est le chiffre d'affaires "
      "<strong>en Suisse et à l'étranger</strong> qui compte, pas seulement le "
      "chiffre d'affaires suisse. Les prestations exclues (par exemple la location "
      "de logements, les opérations d'assurance et de banque, certaines prestations "
      "de formation) ne sont pas comptées.")
    + P("Quiconque reste sous la limite annuelle est exempté de l'assujettissement "
        "– exception pour les associations : les associations sportives et "
        "culturelles sans but lucratif dirigées à titre bénévole ainsi que les "
        "organisations d'utilité publique bénéficient d'une limite relevée de "
        "<strong>CHF 250'000</strong> (art. 10 al. 2 let. c LTVA). Chaque période "
        "fiscale est déterminante ; quiconque peut prévoir qu'il dépassera la "
        "limite au cours des douze mois prochains devient assujetti déjà avant.")
)

# ---------------------------------------------------------------- S2
h2 = "Inscription : spontanée, dans les 30 jours"
b2 = (
    P("Dès que vous dépassez la limite (ou que le dépassement est prévisible), "
      "vous devez vous annoncer <strong>spontanément dans les 30 jours</strong> "
      "par écrit auprès de l'AFC, à compter du début de l'assujettissement "
      "(art. 66 al. 1 LTVA). Personne ne vous écrira. L'inscription se fait via "
      "le <strong>questionnaire en ligne de l'AFC</strong> ; vous recevez un "
      "numéro de TVA non cessible. Risque de confusion : le « Formulaire 25 » "
      "concerne le remboursement de l'impôt anticipé – pour la TVA, c'est le "
      "formulaire en ligne de l'AFC qui est compétent.")
    + P("Inversement : quiconque reste sous la limite peut renoncer volontairement "
        "à l'exemption et s'annoncer (art. 11 et 14 LTVA) – cela vaut la peine à "
        "cause de la déduction de l'impôt préalable, surtout en cas "
        "d'investissements élevés. Attention : quiconque mentionne la TVA sur une "
        "facture sans y être habilité doit ce montant quand même "
        "(art. 27 LTVA).")
)

# ---------------------------------------------------------------- S3
h3 = "Les taux 2026"
b3 = P(
    "Les taux applicables sont : <strong>taux normal 8,1 pour cent</strong>, "
    "<strong>taux réduit 2,6 pour cent</strong> (art. 25 LTVA). Le taux réduit "
    "vaut notamment pour les denrées alimentaires au sens de la législation sur "
    "les denrées alimentaires (à l'exclusion des boissons alcoolisées), l'eau du "
    "réseau, les médicaments, les livres et les biens de presse. Attention, erreur "
    "courante : <strong>pour les prestations de l'hôtellerie-restauration, le taux "
    "normal s'applique</strong> – service au restaurant et consommation sur place "
    "ne sont pas à taux réduit, même si les denrées alimentaires le seraient en "
    "soi. Quiconque calcule « la restauration à 2,6 % » s'est trompé."
)

# ---------------------------------------------------------------- S4
h4 = "Décompte : trimestriel, semestriel ou au taux de l'impôt forfaitaire"
b4 = P(
    "La règle est le <strong>décompte trimestriel</strong> via le portail TVA de "
    "l'AFC. Les petites entreprises (peu d'impôt par période fiscale) peuvent "
    "décompter par semestre ou par année ; de nombreuses PME utilisent les "
    "<strong>taux de l'impôt forfaitaire</strong> – des taux sectoriels "
    "forfaitaires qui réduisent la charge comptable, car l'impôt préalable ne doit "
    "pas être justifié unité par unité."
)

# ---------------------------------------------------------------- S5
h5 = "Job annexe, association, plateforme : quand vous êtes malgré tout une « entreprise »"
b5 = P(
    "Est une entreprise celui qui exerce une activité orientée vers la réalisation "
    "durable de revenus de manière indépendante (art. 10 al. 1bis LTVA) – y "
    "compris à côté de l'emploi principal et même avec un taux d'occupation de "
    "20 pour cent sur une plateforme. Des mandats de consulting récurrents, le "
    "chiffre d'affaires d'une boutique en ligne ou une location avec "
    "infrastructure peuvent déclencher l'assujettissement avant que vous ne vous "
    "en rendiez compte. Les rétributions de moindre importance et les "
    "opérations réellement occasionnelles ne le font pas."
)

# ---------------------------------------------------------------- S6
h6 = "En bref"
b6 = (
    OL([
        "Assujettissement dès CHF 100'000 de chiffre d'affaires mondial provenant "
        "de prestations non exclues (art. 10 al. 2 LTVA) ; associations "
        "sportives/culturelles et institutions d'utilité publique : CHF 250'000.",
        "Inscription : dans les 30 jours, spontanément, questionnaire en ligne de "
        "l'AFC – pas le Formulaire 25.",
        "Taux 2026 : 8,1 % normal, 2,6 % réduit ; restauration = taux normal.",
        "Une inscription volontaire ouvre droit à la déduction de l'impôt "
        "préalable ; la TVA mentionnée sans habilitation est due (art. 27).",
    ])
    + P("Vous venez (bientôt) de dépasser les 100'000 et vous voulez démarrer "
        "correctement ? Via la <a href=\"kontakt.html\">page de contact</a>, nous "
        "vous mettons en relation avec un partenaire vérifié pour la première "
        "annonce TVA – avec un devis avant le mandat.")
)

sections = [(h1, b1), (h2, b2), (h3, b3), (h4, b4), (h5, b5), (h6, b6)]

if __name__ == "__main__":
    at.build('fr', 'mwst-100k-pflicht-schweiz', TITLE, META, sections)
