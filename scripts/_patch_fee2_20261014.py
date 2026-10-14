#!/usr/bin/env python3
import pathlib, re

INS = {
 "en": [
  (r"(<li><strong>Margin:</strong>[^<]*– including promotional items\?</li>)",
   "<li><strong>From November 2026:</strong> budget the additional 2-EUR Union Handling Fee per category – adjust checkout pricing before the Christmas peak.</li>"),
  (r"(<li>Import VAT remains due independently of all this\.</li>)",
   "<li>From 1 Nov 2026 an additional 2-EUR handling fee (Union Handling Fee) per product category is announced – amount still in draft.</li>"),
 ],
 "fr": [
  (r"(<li><strong>Marge :</strong>[^<]*</li>)",
   "<li><strong>À partir de novembre 2026 :</strong> prévoyez la redevance supplémentaire de 2 EUR par catégorie (Union Handling Fee) – ajustez les prix du checkout avant les fêtes.</li>"),
  (r"(<li>La TVA à l’importation reste due indépendamment de tout cela\.</li>)",
   "<li>À partir du 1er novembre 2026 : redevance de traitement (Union Handling Fee) de 2 EUR par catégorie annoncée – montant encore à l’état de projet.</li>"),
 ],
 "it": [
  (r"(<li><strong>Margine:</strong>[^<]*</li>)",
   "<li><strong>Dal novembre 2026:</strong> mettete in conto la forfetta supplementare di 2 EUR per categoria (Union Handling Fee) – adeguate i prezzi del checkout prima del picco natalizio.</li>"),
  (r"(<li>L'IVA all'importazione continua a essere dovuta indipendentemente\.</li>)",
   "<li>Dal 1° novembre 2026 è annunciata una forfetta di disbrigo (Union Handling Fee) di 2 EUR per categoria – importo ancora in progetto.</li>"),
 ],
}
for lang, pairs in INS.items():
    p = pathlib.Path(f"{lang}/eu-zoll-3-euro-kleinsendungen.html")
    t = p.read_text()
    for pat, add in pairs:
        m = re.search(pat, t)
        if not m:
            print(lang, "NO MATCH", pat[:40]); continue
        t = t[:m.end()] + add + t[m.end():]
    p.write_text(t)
    print(lang, "ok", len(t))
