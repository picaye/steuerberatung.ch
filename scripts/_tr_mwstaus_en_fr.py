#!/usr/bin/env python3
"""EN + FR fan-out for mwst-ausfuhr-0-prozent-nachweis.html (DE source).

Glossary (references/multilang-glossary.md): MWST=VAT/TVA, ESTV=FTA/AFC,
BAZG=FOCBS/OFDF, Ausfuhrnachweis=proof of export/justificatif d'export,
Reiseverkehr=travel traffic/trafic touristique; Passar, e-dec, eVV Export,
Chartera Output, Form. 11.44, ZKV stay as system names.
Facts kept EXACT: 0 %, 8.1 % (FR 8,1 %), 1 January 2026 / 1er janvier 2026,
31 December 2025 / 31 décembre 2025, Form. 11.44, 10 years / 10 ans,
Art. 6 para. 2 let. a VAT Act / art. 6 al. 2 let. a LTVA,
Art. 49 para. 2 VAT Act / art. 49 al. 2 LTVA.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build, BASE, RELATED_START, RELATED_END

SLUG = "mwst-ausfuhr-0-prozent-nachweis"
RELATED = [
    "eu-zoll-3-euro-kleinsendungen.html",
    "mwst-agov-pflicht-oktober-2026.html",
    "mwst-100k-pflicht-schweiz.html",
]

EN_TITLE = "VAT at 0 % on Exports: These Are the Export Proofs the FTA Accepts"
EN_META = ("Goods supplied abroad are VAT-exempt – but only with a valid proof of export. "
           "Since 2026 the export declaration runs through Passar instead of e-dec: which documents "
           "count (eVV Export, Form. 11.44, export document in travel traffic), and what happens without proof.")

EN_SECTIONS = [
    ("0 % Tax Is a Question of Proof",
     '<p>Supplies abroad are exempt from VAT, or taxable at the rate of 0 % (Art. 6 para. 2 let. a VAT Act). '
     'But: the exemption is <strong>not a matter of course – it is a question of proof</strong>. The FTA '
     'proceeds from the principle that the taxable supplier must prove the export. If the proof fails, the '
     'supply is reassessed as a domestic transaction – at the current domestic rate of 8.1 % – even though '
     'the foreign customer paid the net amount.</p>'
     '<p>This is precisely the classic finding in VAT audits: sale booked, tax declared at 0 %, but no valid '
     'proof of export on file. The reclaim hits the margin in full.</p>'),
    ("Passar Has Replaced e-dec Export (Since 1 January 2026)",
     '<p>For the proof of export, 2026 brought a fundamental change: the Federal Office for Customs and Border '
     'Security (FOCBS) <strong>took the old e-dec Export system out of service on 31 December 2025</strong>. '
     'Since <strong>1 January 2026, export declarations run exclusively through Passar</strong> '
     '(www.passar.admin.ch). For exporters, this has practical consequences:</p>'
     '<ul><li>The <strong>electronic export assessment decision (eVV Export)</strong> is the central proof of '
     'export – it must be actively retrieved from Passar, manually via the "Chartera Output" tool or '
     'automated via customs software, and then archived electronically.</li>'
     '<li>The decision is legally valid as a PDF only <strong>with the embedded XML part</strong> – a '
     'screenshot or a plain printout is not sufficient.</li>'
     '<li>Extended transitional periods apply to tobacco products; the <strong>Form. 11.44</strong> '
     '(customs-stamped duplicate of the customs declaration for raw tobacco and tobacco products) remains a '
     'valid form of proof.</li>'
     '<li>e-dec Web can temporarily continue to be used; its definitive replacement will be communicated '
     'separately.</li></ul>'),
    ("These Are the Documents the FTA Accepts",
     '<p>The FOCBS lists the suitable proofs of export, in principle exhaustively:</p>'
     '<ol><li><strong>Electronic export assessment decision (eVV Export)</strong> with digital signature – '
     'the standard case for commercial exports (from Passar since 2026).</li>'
     '<li><strong>Customs-stamped duplicate of the customs declaration for raw tobacco and tobacco products '
     '(Form. 11.44).</strong></li>'
     '<li><strong>Customs-confirmed "export document in travel traffic"</strong> – the document for retail '
     'shops that sell goods to travellers (tax-free procedure; details from the FTA under "VAT-Refund: '
     'Rückerstattung an Unternehmen im Ausland").</li>'
     '<li><strong>Customs documents on properly completed procedures</strong> – e.g. when an item is exported '
     'after temporary use in the country and assessed abroad.</li></ol>'
     '<p>If the export cannot be proven with any of these documents, the catch-all rule applies: the supplies '
     'must be taxed domestically.</p>'),
    ("Travel Traffic: The Document at the Border Crossing",
     '<p>When a retail shop sells to tourists, the <strong>export document in travel traffic</strong> replaces '
     'the commercial customs declaration: the goods are declared at the customs office on exit and stamped or '
     'confirmed electronically (export declaration). Without this document the supply counts as domestic '
     'turnover – any refund of the tax paid to the customer fails for lack of proof. For businesses with '
     'customers from the EU, the same procedure applies in reverse for verifying tax-free refunds.</p>'),
    ("Record-Keeping and Audit Practice",
     '<p>Business records – and therefore every proof of export – must be <strong>retained for ten years</strong> '
     '(Art. 49 para. 2 VAT Act). In audits the FTA does not check "whether something was exported" by sampling, '
     'but <strong>whether a document exists for each line item</strong>. The clean linkage of commercial '
     'invoice, Passar declaration and eVV Export (including XML) is half the VAT audit.</p>'
     '<p>Practical tip: the eVV Export contains the assessment confirmation of the export; anyone who "retrieves '
     'and archives it proactively" (the FOCBS recommendation) instead of leaving it in the system avoids the '
     'most common trap: goods gone, document never retrieved, tax reclaimed.</p>'),
    ("Checklist for Exporting Businesses",
     '<ol><li><strong>Passar onboarding</strong> done? UID registered in the customs customer administration '
     '(ZKV), role "document retrieval in goods traffic" activated in the ePortal?</li>'
     '<li><strong>Retrieval of the eVV Export</strong> organised (Chartera Output or customs software) – '
     'including archiving the PDF with XML?</li>'
     '<li><strong>Travel traffic:</strong> processes defined for export declarations at the border crossing?</li>'
     '<li><strong>Tobacco:</strong> transitional rules and Form. 11.44 observed?</li>'
     '<li><strong>Invoicing:</strong> 0 % rate with a note referring to the export supply; reference to the '
     'customs declaration number?</li>'
     '<li><strong>Retention:</strong> documents secured audit-compliantly for 10 years?</li></ol>'),
    ("In Short",
     '<ul><li>VAT exemption on exports = burden of proof on the supplier; without proof, 8.1 % is reassessed.</li>'
     '<li>Since 1 January 2026: exports only via Passar; e-dec Export is switched off. The central proof is the '
     'eVV Export with digital signature (PDF valid only with embedded XML).</li>'
     '<li>Other suitable documents: Form. 11.44 (tobacco), export document in travel traffic, customs procedure '
     'documents.</li>'
     '<li>Retention duty: 10 years.</li>'
     '<li>General information, not individual tax advice – in doubt, consult the FTA or a VAT expert.</li></ul>'),
]

FR_TITLE = "TVA à 0 % à l'exportation : voici les justificatifs d'export acceptés par l'AFC"
FR_META = ("Les marchandises livrées à l'étranger sont exonérées de TVA – mais uniquement avec un justificatif "
           "d'export valide. Depuis 2026, la déclaration d'exportation passe par Passar au lieu d'e-dec : quels "
           "documents comptent (eVV Export, Form. 11.44, document de sortie dans le trafic touristique), et ce "
           "qui se passe sans preuve.")

FR_SECTIONS = [
    ("0 % d'impôt : une question de preuve",
     '<p>Les livraisons à l\'étranger sont exonérées de TVA, respectivement imposables au taux de 0 % '
     '(art. 6 al. 2 let. a LTVA). Mais : l\'exonération n\'est <strong>pas une évidence, c\'est une question '
     'de preuve</strong>. L\'AFC suit le principe selon lequel le prestataire assujetti doit prouver '
     'l\'exportation. Si la preuve échoue, la livraison est taxée rétroactivement comme opération intérieure – '
     'au taux national de 8,1 % actuellement – bien que le client étranger ait payé le montant net.</p>'
     '<p>C\'est exactement le cas classique des contrôles TVA : vente comptabilisée, taxe déclarée à 0 %, mais '
     'aucun justificatif d\'export valide dans le dossier. Le rappel d\'impôt pèse entièrement sur la marge.</p>'),
    ("Passar a remplacé e-dec Export (depuis le 1er janvier 2026)",
     '<p>Pour la preuve de l\'exportation, 2026 a apporté un changement fondamental : l\'Office fédéral de la '
     'douane et de la sécurité des frontières (OFDF) a <strong>mis hors service l\'ancien système e-dec Export '
     'au 31 décembre 2025</strong>. Depuis le <strong>1er janvier 2026, les déclarations d\'exportation passent '
     'exclusivement par Passar</strong> (www.passar.admin.ch). Pour les exportateurs, les conséquences '
     'pratiques sont les suivantes :</p>'
     '<ul><li><strong>La décision de taxation électronique Export (eVV Export)</strong> est le justificatif '
     'd\'export central – elle doit être retirée activement de Passar, manuellement via l\'outil « Chartera '
     'Output » ou automatiquement via un logiciel douanier, puis archivée électroniquement.</li>'
     '<li>La décision n\'est juridiquement valable en PDF qu\'<strong>avec la partie XML intégrée</strong> – '
     'une capture d\'écran ou une simple impression ne suffisent pas.</li>'
     '<li>Des délais transitoires prolongés s\'appliquent aux produits du tabac ; le <strong>Formulaire '
     '11.44</strong> (duplicata de la déclaration en douane visé par la douane pour le tabac brut et les '
     'produits du tabac) reste admis comme justificatif.</li>'
     '<li>e-dec Web peut provisoirement continuer d\'être utilisé ; son remplacement définitif fera l\'objet '
     'd\'une communication séparée.</li></ul>'),
    ("Voici les justificatifs acceptés par l'AFC",
     '<p>L\'OFDF énumère en principe de manière exhaustive les justificatifs d\'export valables :</p>'
     '<ol><li><strong>Décision de taxation électronique Export (eVV Export)</strong> avec signature numérique – '
     'le cas normal des exportations commerciales (depuis 2026, issue de Passar).</li>'
     '<li><strong>Duplicata de la déclaration en douane pour le tabac brut et les produits du tabac, visé par '
     'la douane (Form. 11.44).</strong></li>'
     '<li><strong>« Document de sortie dans le trafic touristique » confirmé par la douane</strong> – le '
     'justificatif pour les commerces de détail qui vendent des marchandises à des voyageurs (procédure '
     'tax-free ; détails auprès de l\'AFC sous « VAT-Refund: Rückerstattung an Unternehmen im Ausland »).</li>'
     '<li><strong>Documents douaniers attestant des procédures régulièrement clôturées</strong> – par exemple '
     'lorsqu\'un objet est exporté après un emploi temporaire à l\'intérieur du pays et taxé à l\'étranger.'
     '</li></ol>'
     '<p>Si l\'exportation ne peut être prouvée par aucun de ces documents, la règle résiduelle s\'applique : '
     'les livraisons doivent être imposées à l\'intérieur du pays.</p>'),
    ("Trafic touristique : le justificatif au passage frontalier",
     '<p>Lorsqu\'un commerce de détail vend à des touristes, le <strong>document de sortie dans le trafic '
     'touristique</strong> remplace la déclaration en douane commerciale : la marchandise est annoncée au '
     'bureau de douane lors de la sortie et visée par un cachet ou confirmée électroniquement (annonce de '
     'sortie). Sans ce document, la livraison est considérée comme un chiffre d\'affaires intérieur – le '
     'remboursement de la taxe payée à la clientèle échoue faute de preuve. Pour les entreprises ayant une '
     'clientèle de l\'UE, la même procédure s\'applique en sens inverse pour la vérification des remboursements '
     'tax-free.</p>'),
    ("Conservation et pratique des contrôles",
     '<p>Les documents commerciaux – et donc chaque justificatif d\'export – doivent être <strong>conservés '
     'pendant dix ans</strong> (art. 49 al. 2 LTVA). Lors des contrôles, l\'AFC ne vérifie pas par sondage '
     '« si quelque chose a été exporté », mais <strong>si un justificatif existe pour chaque position</strong>. '
     'Le rapprochement propre entre facture commerciale, déclaration Passar et eVV Export (XML inclus) fait la '
     'moitié du contrôle TVA.</p>'
     '<p>Conseil pratique : l\'eVV Export contient la confirmation de taxation de l\'exportation ; celui qui la '
     '« retire et archive de manière proactive » (recommandation de l\'OFDF) au lieu de la laisser dans le '
     'système évite le piège le plus fréquent : marchandise partie, justificatif jamais retiré, rappel d\'impôt.</p>'),
    ("Check-list pour les entreprises exportatrices",
     '<ol><li><strong>Onboarding Passar</strong> effectué ? UID enregistrée dans l\'administration des clients '
     'de la douane (ZKV), rôle « retrait de documents dans le trafic des marchandises » activé dans l\'ePortal ?'
     '</li>'
     '<li><strong>Retrait de l\'eVV Export</strong> organisé (Chartera Output ou logiciel douanier) – y compris '
     'l\'archivage du PDF avec XML ?</li>'
     '<li><strong>Trafic touristique :</strong> processus définis pour les annonces de sortie au passage '
     'frontalier ?</li>'
     '<li><strong>Tabac :</strong> règles transitoires et Formulaire 11.44 respectés ?</li>'
     '<li><strong>Facturation :</strong> taux de 0 % avec mention de la prestation d\'exportation ; référence '
     'au numéro de la déclaration en douane ?</li>'
     '<li><strong>Conservation :</strong> justificatifs sécurisés de manière conforme à l\'audit pendant '
     '10 ans ?</li></ol>'),
    ("En résumé",
     '<ul><li>Exonération de TVA à l\'export = charge de la preuve sur le prestataire ; sans justificatif, '
     '8,1 % sont rappelés.</li>'
     '<li>Depuis le 1er janvier 2026 : exportation uniquement via Passar ; e-dec Export est éteint. Le '
     'justificatif central est l\'eVV Export avec signature numérique (PDF valable uniquement avec XML '
     'intégré).</li>'
     '<li>Autres justificatifs valables : Formulaire 11.44 (tabac), document de sortie dans le trafic '
     'touristique, documents de procédure douaniers.</li>'
     '<li>Obligation de conservation : 10 ans.</li>'
     '<li>Information générale, pas de conseil individuel – en cas de doute, s\'adresser à l\'AFC ou à un '
     'expert TVA.</li></ul>'),
]

# Fallback titles if the sibling-language eu-zoll page does not exist yet at
# build time (render_related would otherwise emit a slug-derived title).
FALLBACK_TITLES = {
    "en": {"eu-zoll-3-euro-kleinsendungen.html":
           "Swiss Online Shops Shipping to the EU: Customs Duty on Small Parcels Since July 2026"},
    "fr": {"eu-zoll-3-euro-kleinsendungen.html":
           "Boutiques en ligne suisses vers l'UE : droits de douane sur les petits envois depuis juillet 2026"},
}


def fix_related_fallbacks(lang):
    outpath = os.path.join(BASE, lang, SLUG + ".html")
    doc = open(outpath, encoding="utf-8").read()
    start, end = doc.index(RELATED_START), doc.index(RELATED_END)
    block = doc[start:end]
    for href, title in FALLBACK_TITLES.get(lang, {}).items():
        ugly = href.rsplit(".html", 1)[0].replace("-", " ").capitalize()
        if ugly in block:
            block = block.replace(ugly, title)
    doc = doc[:start] + block + doc[end:]
    open(outpath, "w", encoding="utf-8").write(doc)


if __name__ == "__main__":
    build("en", SLUG, EN_TITLE, EN_META, EN_SECTIONS, related=RELATED)
    fix_related_fallbacks("en")
    build("fr", SLUG, FR_TITLE, FR_META, FR_SECTIONS, related=RELATED)
    fix_related_fallbacks("fr")
    for lang in ("en", "fr"):
        p = os.path.join(BASE, lang, SLUG + ".html")
        print(lang, os.path.getsize(p), "bytes")
