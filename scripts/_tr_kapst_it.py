#!/usr/bin/env python3
"""Translate kapitalsteuer-ag-gmbh.html (DE source) into an ITALIAN site page.

Uses scripts/article_template.py build() so chrome (switcher, hreflang,
canonical, JSON-LD, related block) is emitted by the template.
Figures kept EXACTLY as in DE: 0,75 per mille, CHF 2 mio, CHF 1'725,
115 %, 0,01 per mille, 7 per mille, 30 %, CHF 500, CHF 50'000, 8,5 %, 35 %,
art. 86/88 of the Aargau Tax Act (IT: cpv., values identical).
IT terms per multilang-glossary: imposta sul capitale, imposta sugli utili,
capitale proprio, moltiplicatore, imputazione, SA, Sagl, imposta preventiva,
AFC, LIFD, fiduciario. Formal Lei register.
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

IT_TITLE = "Imposta sul capitale di SA e Sagl: ciò che costa alle aziende anche negli anni in perdita"
IT_META = ("Non tutti i cantoni tassano il capitale, ma chi lo fa incassa ogni anno – "
           "del tutto senza utile. Come funziona l'imposta sul capitale: prelievo sul "
           "capitale proprio, imputazione dell'imposta sugli utili, imposta minima, "
           "aliquote cantonali tra 0 e 7 per mille – e perché riduzioni del capitale e "
           "liquidazioni vanno calcolate fino in fondo.")

IT_SECTIONS = [
    ("Cosa colpisce l'imposta sul capitale",
     "<p>L'imposta sul capitale è un'<strong>imposta cantonale sul capitale proprio "
     "imponibile</strong> di una società di capitali: le società anonime (SA), le società "
     "a garanzia limitata (Sagl) e le cooperative sono tassate ogni anno sul capitale "
     "proprio di bilancio (capitale sociale più le riserve legali e volontarie, secondo il "
     "diritto cantonale) – <strong>indipendentemente dal fatto che l'azienda realizzi un "
     "utile</strong>. Un anno in perdita non La esonera; l'imposta è comunque dovuta.</p>"
     "<p>A livello federale non esiste un'imposta sul capitale – l'imposta federale "
     "diretta conosce solo l'imposta sugli utili (8,5 %). I cantoni con sola imposta "
     "sugli utili sono rari: la maggioranza dei cantoni riscuote un'imposta sul capitale, "
     "però con configurazioni molto diverse. Il canton Uri, ad esempio, vi rinuncia del "
     "tutto a livello cantonale (pubblicazione AFC «Steuersatz und Steuerfuss», stato al "
     "1.1.2026), mentre i comuni urani riscuotono aliquote proporzionali tra 0,01 e 4 per "
     "mille.</p>"),
    ("Aliquote e moltiplicatori: un giro d'orizzonte",
     "<p>Le aliquote legali si muovono nella fascia dei per mille. Esempio Argovia: "
     "<strong>0,75 per mille del capitale proprio imponibile</strong> (art. 86 cpv. 1 "
     "della legge fiscale argoviese); con un moltiplicatore del 115 % (2026) ne risulta "
     "circa <strong>CHF 1'725 di imposta sul capitale</strong> all'anno per un'azienda con "
     "CHF 2 mio di capitale proprio. Il canton Lucerna applica un'imposta sul capitale "
     "fissa di soli 0,01 per mille alla quota del capitale proprio attribuibile a "
     "partecipazioni, brevetti e diritti comparabili nonché a crediti intragruppo – la "
     "tipica disciplina delle holding (AFC, op. cit.).</p>"
     "<p>Il carico non è limitato ovunque: il canton Vaud prescrive per legge che le "
     "imposte cantonale e comunale insieme non possano superare <strong>7 per mille del "
     "capitale imponibile</strong> (e il 30 % dell'utile netto imponibile). La maggioranza "
     "dei cantoni, invece, non prevede <strong>alcun tetto massimo di onere</strong> per "
     "le persone giuridiche.</p>"),
    ("Imputazione: il doppio onere ha un ammortizzatore",
     "<p>Molti cantoni attenuano la combinazione di imposta sugli utili e imposta sul "
     "capitale <strong>imputando l'imposta sugli utili sull'imposta sul capitale</strong> "
     "– espressamente ad Argovia (art. 86 cpv. 4 della legge fiscale argoviese). In "
     "pratica: negli anni redditizi l'imposta sul capitale è spesso «già assorbita»; "
     "l'azienda la paga effettivamente in aggiunta soprattutto quando l'imposta sul "
     "capitale supera l'imposta sugli utili – quindi negli anni deboli e in perdita.</p>"
     "<p>Le imposte minime restano: le società di capitali e le cooperative versano ad "
     "Argovia un'imposta minima di <strong>CHF 500</strong> (imposta cantonale semplice al "
     "100 %, art. 88 della legge fiscale argoviese) – anche con utile zero e rendimento "
     "del capitale zero. Associazioni e fondazioni sono soggette all'imposta sul capitale "
     "solo a partire da <strong>CHF 50'000</strong> di capitale proprio (art. 86 cpv. 3 "
     "della legge fiscale argoviese).</p>"),
    ("Chi sente davvero il peso?",
     "<p>L'imposta sul capitale è un'<strong>imposta sulla sostanza applicata al denaro "
     "dell'azienda</strong>. Tre configurazioni fanno male:</p>"
     "<ul><li><strong>Liquidità ricche, utili nanerottoli:</strong> le riserve accumulate "
     "aumentano il capitale proprio e quindi l'imposta, senza che sia affluito alcun "
     "utile – l'imposta diventa un puro onere di liquidità.</li>"
     "<li><strong>Anni in perdita:</strong> imposta sugli utili zero, imposta sul capitale "
     "piena – l'imputazione cade a vuoto.</li>"
     "<li><strong>Casi di riorganizzazione:</strong> prima di riduzioni del capitale, "
     "ristrutturazioni e liquidazioni l'imposta sul capitale deve entrare nel calcolo "
     "complessivo: fino alla cancellazione dal registro di commercio l'imposta è dovuta "
     "ogni anno; una riduzione del capitale scaglionata può ridurla, ma a seconda della "
     "struttura solleva questioni di rimborso dell'imposta di emissione o fa scattare "
     "l'imposta preventiva.</li></ul>"),
    ("Un fattore di localizzazione cantonale – e un dibattito politico ricorrente",
     "<p>L'imposta sul capitale è un vero criterio di localizzazione: tra «nessuna imposta "
     "cantonale sul capitale» (Uri) e vari per mille compresa la quota comunale c'è un "
     "mondo – sommandosi all'imposta sugli utili, grava per anni i modelli ad alta "
     "intensità di capitale. Singoli cantoni hanno ridotto le aliquote o creato regimi "
     "speciali per la sostanza di holding; il dibattito politico su un'abolizione "
     "completa ritorna regolarmente a livello cantonale.</p>"
     "<p>Per la pratica vale: chi fonda, detiene, ristruttura o liquida una SA o una Sagl "
     "verifica l'imposta sul capitale del cantone di domicilio <strong>ogni anno di "
     "nuovo</strong> – aliquote, moltiplicatori e modelli di imputazione cambiano più "
     "spesso dell'imposta sugli utili.</p>"),
    ("Checklist per i soci di SA/Sagl",
     "<ol><li><strong>Tenere un registro:</strong> capitale proprio imponibile per anno, "
     "comprese le variazioni delle riserve.</li>"
     "<li><strong>Confrontare i cantoni:</strong> conoscere aliquota, moltiplicatore, "
     "modello di imputazione e imposta minima del cantone di domicilio (pubblicazione AFC "
     "«Steuersatz und Steuerfuss» come punto di partenza).</li>"
     "<li><strong>Preventivare gli anni in perdita:</strong> imposta sul capitale + "
     "imposta minima scorrono indipendentemente dal risultato.</li>"
     "<li><strong>Politica delle riserve:</strong> le decisioni di ritenzione aumentano la "
     "base dell'imposta sul capitale – dividendo vs. riserva: calcolare l'effetto "
     "complessivo (compresa l'imposta preventiva del 35 %).</li>"
     "<li><strong>Simulare le ristrutturazioni:</strong> riduzione del capitale, "
     "liquidazione parziale, liquidazione – risparmio d'imposta sul capitale contro "
     "conseguenze sull'imposta di emissione e sull'imposta preventiva.</li>"
     "<li><strong>Revalidare ogni anno:</strong> i moltiplicatori vengono spesso "
     "modificati.</li></ol>"),
    ("In breve",
     "<ul><li>Imposta sul capitale = imposta cantonale annuale sul capitale proprio di "
     "SA/Sagl/cooperative – anche negli anni in perdita.</li>"
     "<li>L'imposta federale diretta non conosce imposta sul capitale; le aliquote "
     "cantonali sono nella fascia dei per mille (esempio Argovia 0,75 ‰; Uri a livello "
     "cantonale: nessuna; Vaud: tetto di 7 ‰).</li>"
     "<li>L'imposta sugli utili è di norma imputata – in pratica si paga l'imposta sul "
     "capitale soprattutto con risultati deboli; le imposte minime restano (Argovia: "
     "CHF 500).</li>"
     "<li>In caso di riduzione del capitale e di liquidazione va inclusa nel calcolo "
     "complessivo.</li>"
     "<li>Informazione generale, non consulenza per il singolo caso – rivolgersi a un "
     "fiduciario o a un esperto fiscale.</li></ul>"),
]

if __name__ == "__main__":
    build("it", SLUG, IT_TITLE, IT_META, IT_SECTIONS, related=RELATED)
