#!/usr/bin/env python3
"""Build EN and FR versions of eu-zoll-3-euro-kleinsendungen from the DE article.

Translation follows references/multilang-glossary.md: IOSS stays IOSS, distance
sales = Fernverkauf, customs duty = Zoll; all figures/regulation numbers kept
exactly as DE (VO (EU) 2026/382, 3 EUR, 150 EUR, code 500, 1 July 2026, 2028).
EN: professional Swiss business English. FR: formal vouvoiement.
"""
import sys
sys.path.insert(0, '/Users/pino/Code/steuerberatung.ch/scripts')
from article_template import build

SLUG = 'eu-zoll-3-euro-kleinsendungen'
RELATED = ['mwst-ausfuhr-0-prozent-nachweis.html',
           'mwst-100k-pflicht-schweiz.html',
           'transparenzregister-tjpg-meldepflicht.html']

# ---------------------------------------------------------------- English ----
TITLE_EN = ("Swiss Online Shops Selling into the EU: Customs Duty on Small "
            "Parcels Since July 2026")
META_EN = ("The EU has scrapped the 150-euro customs duty exemption (Regulation "
           "(EU) 2026/382, in force since 1 July 2026): distance sales from "
           "third countries – including Switzerland – now pay a flat 3 EUR "
           "customs duty per goods category, transitional rules until mid-2028. "
           "What Swiss shops must now review regarding IOSS, checkout and "
           "parcel costs.")

SECTIONS_EN = [
    ("What changed on 1 July 2026",
     '<p>If you sell from Switzerland into the EU, you know the old rule: '
     'parcels with a value of goods up to 150 EUR were duty-free. That '
     'exemption no longer exists. On 11 February 2026 the Council of the '
     'European Union adopted <strong>Regulation (EU) 2026/382</strong>, which '
     'amends the previous Duty Relief Regulation (EC) No 1186/2009 – '
     '<strong>with effect from 1 July 2026</strong>.</p>'
     '<p>Since then, distance-sale consignments from third countries – thus '
     'also from Switzerland – are subject to a <strong>flat customs duty of '
     '3 EUR per goods category</strong>. "Goods category" means: per item line '
     'declared in the customs declaration. A parcel containing three different '
     'product groups therefore incurs 9 EUR in duty, not 3.</p>'
     '<p>German customs (zoll.de) and the Austrian Federal Ministry of Finance '
     '(bmf.gv.at) confirm the rule in identical terms. Important: this concerns '
     'the <strong>customs duty</strong> – import VAT remains due regardless '
     '(the 22-euro tax exemption threshold was already scrapped in 2021).</p>'),

    ("IOSS consignments: always 3 EUR, no preference",
     '<p>Many Swiss shops handle EU parcels through the <strong>IOSS '
     'procedure</strong> (Import One-Stop-Shop): VAT is collected already at '
     'checkout and remitted through one EU member state. As far as customs '
     'duty is concerned, IOSS changes nothing about the payment obligation – '
     'quite the opposite:</p>'
     '<p>According to the Austrian BMF, Article 2(a) of Regulation (EU) '
     '2026/382 provides that for IOSS consignments <strong>the 3-euro duty '
     'applies across the board; customs preference is excluded</strong>. The '
     'preference code "500" must be declared in the customs declaration. If '
     'you sell via IOSS, you should therefore build the 3 EUR per goods line '
     'firmly into your margin.</p>'
     '<p>For non-IOSS distance-sale consignments up to 150 EUR the flat duty '
     'applies as well – here a preference (e.g. the Switzerland–EU free trade '
     'agreement) may apply in individual cases, provided proof of origin is '
     'available. The customs service provider checks this case by case.</p>'),

    ("What this means for Swiss shops in practice",
     '<p>The flat duty is small – its impact is not always:</p>'
     '<ul><li><strong>Cart size:</strong> on a 25-euro product, 3 EUR in duty '
     'plus clearance handling costs is a noticeable surcharge – and a classic '
     'reason for checkout abandonment if the customer only sees it upon '
     'delivery.</li>'
     '<li><strong>Count the item lines:</strong> mixed parcels are billed by '
     'goods category. Assortment bundling (more copies of the same category '
     'per parcel) remains advantageous in customs terms.</li>'
     '<li><strong>Hand-over vs. DDP:</strong> anyone offering "Delivered Duty '
     'Paid" (clearance handled by the shop) must pre-finance the 3 EUR and '
     'factor it into the price; anyone leaving payment to the customer risks '
     'delivery refusals and returns.</li>'
     '<li><strong>Christmas business:</strong> November and December are the '
     'first peak under the new rules – the first real test for checkout logic '
     'and communication.</li></ul>'),

    ("Transitional rules until mid-2028",
     '<p>The 3-euro flat duty is expressly a <strong>time-limited transitional '
     'solution</strong>. The actual EU customs reform envisages a central EU '
     'customs data platform (Customs Data Hub) through which import duties '
     'will eventually be collected entirely digitally – no earlier than 2028. '
     'Until then, the flat-rate regime for small parcels applies; details on '
     'reference amounts and security guarantees are governed by Implementing '
     'Regulation (EU) 2015/2447 (Article 155(3)(c) UCC-IA, as amended by '
     'Regulation (EU) 2026/1200).</p>'
     '<p>For Swiss sellers this means: the 3 EUR are the beginning, not the '
     'end, of regulation. Anyone who keeps their data clean today (commodity '
     'codes, values, origin) will have the advantage in 2028.</p>'),

    ("Checklist: these six points to review now",
     '<ol><li><strong>IOSS registration</strong> up to date? EU identification '
     'number visible at checkout?</li>'
     '<li><strong>Commodity codes (CN codes)</strong> maintained per article – '
     'so the customs declaration groups the item lines correctly?</li>'
     '<li><strong>Price display:</strong> does the checkout show "duty '
     'included" or "plus import duties"? Both are legal; misleading the '
     'customer is not.</li>'
     '<li><strong>Logistics contract:</strong> who handles clearance – '
     'carrier, customs broker, or the shop? Who bears the 3 EUR under DDP?</li>'
     '<li><strong>Customer communication:</strong> information text on the '
     'product page and in shipment tracking.</li>'
     '<li><strong>Margin:</strong> is 3 EUR per goods line calculated into the '
     'assortment – including promotional items?</li></ol>'),

    ("In short",
     '<ul><li>Since 1 July 2026: no more 150-euro customs duty exemption in '
     'the EU (Council Regulation (EU) 2026/382 of 11 February 2026).</li>'
     '<li>3 EUR customs duty per goods category (per item line of the customs '
     'declaration) for distance-sale consignments from third countries – '
     'including Switzerland.</li>'
     '<li>For IOSS consignments the flat duty always applies; customs '
     'preference excluded (code 500).</li>'
     '<li>Import VAT remains due independently of all this.</li>'
     '<li>Transitional rules until the EU customs platform (no earlier than '
     '2028) – clean data pays off twice.</li>'
     '<li>General information, not legal advice – for individual cases consult '
     'a customs broker or specialist lawyer.</li></ul>'),
]

# ----------------------------------------------------------------- French ----
TITLE_FR = ("Boutiques en ligne suisses vers l\u2019UE : droits de douane sur "
            "les petits colis depuis juillet 2026")
META_FR = ("L\u2019UE a supprimé la franchise douanière de 150 euros "
           "(règlement (UE) 2026/382, en vigueur depuis le 1er juillet 2026) : "
           "pour les ventes à distance depuis les pays tiers – y compris la "
           "Suisse –, un droit de douane forfaitaire de 3 EUR par catégorie de "
           "marchandises s\u2019applique, régime transitoire jusqu\u2019à "
           "mi-2028. Ce que les boutiques suisses doivent vérifier : IOSS, "
           "checkout et frais de colis.")

SECTIONS_FR = [
    ("Ce qui a changé le 1er juillet 2026",
     '<p>Si vous vendez depuis la Suisse vers l\u2019UE, vous connaissez '
     'l\u2019ancienne règle : les colis d\u2019une valeur marchande jusqu\u00e0 '
     '150 EUR étaient en franchise de droits. Cette franchise n\u2019existe '
     'plus. Le 11 février 2026, le Conseil de l\u2019Union européenne a adopté '
     'le <strong>règlement (UE) 2026/382</strong>, qui modifie le précédent '
     'règlement d\u2019exemption des droits (CE) n° 1186/2009 – '
     '<strong>avec effet au 1er juillet 2026</strong>.</p>'
     '<p>Désormais, les envois en vente à distance depuis les pays tiers – donc '
     'aussi depuis la Suisse – sont soumis à un <strong>droit de douane '
     'forfaitaire de 3 EUR par catégorie de marchandises</strong>. « Catégorie '
     'de marchandises » signifie : par position déclarée dans la déclaration '
     'en douane. Un colis contenant trois groupes d\u2019articles différents '
     'coûte donc 9 EUR de droits, et non 3.</p>'
     '<p>L\u2019administration des douanes allemande (zoll.de) et le ministère '
     'fédéral des Finances autrichien (bmf.gv.at) confirment cette règle de '
     'manière concordante. Important : il s\u2019agit des <strong>droits de '
     'douane</strong> – la TVA à l\u2019importation reste due indépendamment '
     '(la franchise de 22 EUR pour les taxes avait déjà été supprimée en '
     '2021).</p>'),

    ("Envois IOSS : toujours 3 EUR, aucune préférence douanière",
     '<p>De nombreuses boutiques suisses traitent leurs colis UE via la '
     '<strong>procédure IOSS</strong> (Import One-Stop-Shop) : la TVA est '
     'perçue dès le checkout et reversée par l\u2019intermédiaire d\u2019un '
     'État membre de l\u2019UE. Pour le douane, l\u2019IOSS ne change rien à '
     'l\u2019obligation de paiement – bien au contraire :</p>'
     '<p>Selon le BMF autrichien, l\u2019art. 2, let. a du règlement (UE) '
     '2026/382 prévoit que pour les envois IOSS <strong>le droit de 3 EUR '
     's\u2019applique en principe ; toute préférence douanière est exclue</strong>. '
     'Le code de préférence « 500 » doit être indiqué dans la déclaration en '
     'douane. Si vous vendez via IOSS, vous avez donc intérêt à intégrer '
     'fermement les 3 EUR par position de marchandises dans votre marge.</p>'
     '<p>Pour les envois en vente à distance hors IOSS jusqu\u2019à 150 EUR, '
     'le droit forfaitaire s\u2019applique également – ici, une préférence '
     '(p. ex. l\u2019accord de libre-échange Suisse–UE) peut éventuellement '
     's\u2019appliquer si des preuves d\u2019origine sont disponibles. Le '
     'prestataire douanier l\u2019examine au cas par cas.</p>'),

    ("Ce que cela signifie concrètement pour les boutiques suisses",
     '<p>Le droit forfaitaire est faible – son impact ne l\u2019est pas '
     'toujours :</p>'
     '<ul><li><strong>Taille du panier :</strong> sur un produit à 25 EUR, '
     '3 EUR de droits plus les frais de dédouanement constituent un supplément '
     'sensible – et un motif classique d\u2019abandon au checkout si le client '
     'ne le découvre qu\u2019à la livraison.</li>'
     '<li><strong>Comptez les positions :</strong> les colis mixtes sont '
     'facturés par catégorie de marchandises. Regrouper plusieurs exemplaires '
     'de la même catégorie par colis reste avantageux d\u2019un point de vue '
     'douanier.</li>'
     '<li><strong>Remise vs DDP :</strong> proposer « Delivered Duty Paid » '
     '(dédouanement par la boutique) implique d\u2019avancer les 3 EUR et de '
     'les intégrer au prix ; laisser le paiement au client expose aux refus de '
     'livraison et aux retours.</li>'
     '<li><strong>Ventes de Noël :</strong> novembre et décembre sont le '
     'premier pic sous le nouveau régime – le premier test grandeur nature '
     'pour la logique du checkout et la communication.</li></ul>'),

    ("Régime transitoire jusqu\u2019à mi-2028",
     '<p>Le droit forfaitaire de 3 EUR est expressément une <strong>solution '
     'transitoire à durée limitée</strong>. La véritable réforme douanière de '
     'l\u2019UE prévoit une plateforme centrale de données douanières de '
     'l\u2019UE (Customs Data Hub) via laquelle les droits à l\u2019importation '
     'devront à l\u2019avenir être perçus entièrement en numérique – au plus '
     'tôt à partir de 2028. D\u2019ici là, le régime forfaitaire s\u2019applique '
     'aux petits colis ; les détails relatifs aux montants de référence et aux '
     'garanties sont réglés par le règlement d\u2019application (UE) 2015/2447 '
     '(art. 155, par. 3, let. c du règlement d\u2019application du code des '
     'douanes de l\u2019Union, modifié par le règlement (UE) 2026/1200).</p>'
     '<p>Pour les vendeurs suisses, cela signifie : les 3 EUR ne sont que le '
     'début de la régulation, pas sa fin. Celui qui maintient des données '
     'propres dès aujourd\u2019hui (numéros de marchandises, valeurs, origine) '
     'aura un avantage en 2028.</p>'),

    ("Check-list : ces six points à vérifier maintenant",
     '<ol><li><strong>Enregistrement IOSS</strong> à jour ? Numéro '
     'd\u2019identification UE visible au checkout ?</li>'
     '<li><strong>Numéros de marchandises (codes SH)</strong> entretenus par '
     'article – pour que la déclaration en douane regroupe correctement les '
     'positions ?</li>'
     '<li><strong>Affichage des prix :</strong> le checkout indique-t-il '
     '« droits inclus » ou « droits d\u2019importation en sus » ? Les deux '
     'sont licites, pas la tromperie.</li>'
     '<li><strong>Contrat logistique :</strong> qui dédouane – transporteur, '
     'commissionnaire en douane, boutique ? Qui supporte les 3 EUR en DDP ?</li>'
     '<li><strong>Communication client :</strong> texte informatif sur la page '
     'produit et dans le suivi d\u2019envoi.</li>'
     '<li><strong>Marge :</strong> les 3 EUR par position de marchandises '
     'sont-ils calculés dans l\u2019assortiment – y compris pour les articles '
     'en promotion ?</li></ol>'),

    ("En résumé",
     '<ul><li>Depuis le 1er juillet 2026 : plus de franchise douanière de '
     '150 EUR dans l\u2019UE (règlement (UE) 2026/382 du Conseil du 11 février '
     '2026).</li>'
     '<li>3 EUR de droits de douane par catégorie de marchandises (par '
     'position de la déclaration en douane) pour les envois en vente à '
     'distance depuis les pays tiers – y compris depuis la Suisse.</li>'
     '<li>Pour les envois IOSS, le droit forfaitaire s\u2019applique toujours ; '
     'préférence douanière exclue (code 500).</li>'
     '<li>La TVA à l\u2019importation reste due indépendamment de tout cela.</li>'
     '<li>Régime transitoire jusqu\u2019à la plateforme douanière UE (au plus '
     'tôt 2028) – la qualité des données paie doublement.</li>'
     '<li>Information générale, pas de conseil juridique – pour les cas '
     'particuliers, faites appel à un commissionnaire en douane ou à un '
     'avocat spécialisé.</li></ul>'),
]

build('en', SLUG, TITLE_EN, META_EN, SECTIONS_EN, related=RELATED)
build('fr', SLUG, TITLE_FR, META_FR, SECTIONS_FR, related=RELATED)
