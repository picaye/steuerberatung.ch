#!/usr/bin/env python3
"""Insert the Union Handling Fee update (from DE 2026-10-14 patch) into EN/FR/IT eu-zoll pages."""
import pathlib

ADD = {
 "en": {
  "para": "<p>And there is more to come: on current plans the EU will levy an additional <strong>handling fee (&quot;Union Handling Fee&quot;) of 2 EUR per product category</strong> on distance-sales consignments <strong>from 1 November 2026</strong> – independent of goods value, non-refundable, and owed once the customs declaration is accepted. The 2-EUR amount is still based on drafts that, according to German customs (zoll.de), have not been finally adopted; the mechanism itself has been announced. For a parcel with three product categories, 9 EUR of duty plus 6 EUR of handling fees can quickly stack up from November 2026.</p>",
  "li": "<li><strong>From November 2026:</strong> budget the additional 2-EUR Union Handling Fee per category – adjust checkout pricing before the Christmas peak.</li>",
  "ul": "<li>From 1 Nov 2026 an additional 2-EUR handling fee (Union Handling Fee) per product category is announced – amount still in draft.</li>",
  "anchor_p": "scrapped in 2021).</p>",
  "anchor_li": "even on sale items?</li>",
  "anchor_ul": "owed independently of this.</li>",
 },
 "fr": {
  "para": "<p>Et ce n’est pas tout : selon l’état actuel des projets, l’UE percevra en outre <strong>une redevance de traitement (&quot;Union Handling Fee&quot;) de 2 EUR par catégorie de marchandises</strong> sur les envois de vente à distance <strong>à partir du 1er novembre 2026</strong> – indépendamment de la valeur des marchandises, non remboursable et due dès l’acceptation de la déclaration en douane. Le montant de 2 EUR repose encore sur des projets non définitivement adoptés selon l’administration douanière allemande (zoll.de) ; le mécanisme, lui, est annoncé. Pour un colis contenant trois catégories de marchandises, cela peut rapidement représenter 9 EUR de droits plus 6 EUR de redevances à partir de novembre 2026.</p>",
  "li": "<li><strong>À partir de novembre 2026 :</strong> prévoyez la redevance supplémentaire de 2 EUR par catégorie (Union Handling Fee) – ajustez les prix du checkout avant les fêtes.</li>",
  "ul": "<li>À partir du 1er novembre 2026 : redevance de traitement (Union Handling Fee) de 2 EUR par catégorie annoncée – montant encore à l’état de projet.</li>",
  "anchor_p": "supprimée en 2021).</p>",
  "anchor_li": "même sur les articles en promotion ?</li>",
  "anchor_ul": "reste due indépendamment.</li>",
 },
 "it": {
  "para": "<p>E non è tutto: allo stato attuale dei progetti, l’UE percepirà inoltre <strong>una forfetta di disbrigo (&quot;Union Handling Fee&quot;) di 2 EUR per categoria di merci</strong> sulle spedizioni di vendite a distanza <strong>a partire dal 1° novembre 2026</strong> – indipendentemente dal valore della merce, non rimborsabile e dovuta già con l’accettazione della dichiarazione doganale. L’importo di 2 EUR si basa ancora su progetti non definitivamente adottati secondo l’amministrazione doganale tedesca (zoll.de); il meccanismo è invece annunciato. Per un pacco con tre categorie di merci, da novembre 2026 si sommano rapidamente 9 EUR di dazi più 6 EUR di forfette.</p>",
  "li": "<li><strong>Dal novembre 2026:</strong> mettete in conto la forfetta supplementare di 2 EUR per categoria (Union Handling Fee) – adeguate i prezzi del checkout prima del picco natalizio.</li>",
  "ul": "<li>Dal 1° novembre 2026 è annunciata una forfetta di disbrigo (Union Handling Fee) di 2 EUR per categoria – importo ancora in progetto.</li>",
  "anchor_p": "abolita nel 2021).</p>",
  "anchor_li": "anche sulla merce in offerta?</li>",
  "anchor_ul": "resta dovuta indipendentemente.</li>",
 },
}

for lang, a in ADD.items():
    p = pathlib.Path(f"{lang}/eu-zoll-3-euro-kleinsendungen.html")
    t = p.read_text()
    for anchor, addition in [("anchor_p", "para"), ("anchor_li", "li"), ("anchor_ul", "ul")]:
        key = a[anchor]
        if key not in t:
            print(f"{lang}: ANCHOR MISSING: {key[:40]}")
            continue
        if t.count(key) != 1:
            print(f"{lang}: anchor not unique ({t.count(key)}x): {key[:40]}")
            continue
        t = t.replace(key, key + a[addition], 1)
    p.write_text(t)
    print(f"{lang}: patched, {len(t)} bytes")
