#!/usr/bin/env python3
"""Build the Italian version of eu-zoll-3-euro-kleinsendungen from the DE article."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

TITLE_IT = ("Shop online svizzeri verso l'UE: dal luglio 2026 dazi sulle spedizioni "
            "di scarso valore")

META_IT = ("L'UE ha abolito la franchigia doganale di 150 EUR (VO (UE) 2026/382, in vigore "
           "dal 1° luglio 2026): per le vendite a distanza da Paesi terzi – anche dalla "
           "Svizzera – si applica un dazio forfettario di 3 EUR per categoria di merci, con "
           "regime transitorio fino a metà 2028. Cosa devono verificare ora gli shop "
           "svizzeri riguardo a IOSS, checkout e costi dei colli.")

SECTIONS_IT = [
    ("Cosa è cambiato il 1° luglio 2026",
     "<p>Chi vende dalla Svizzera verso l'UE conosce la vecchia regola: i colli con un "
     "valore delle merci fino a 150 EUR erano esenti da dazi. Questa franchigia non esiste "
     "più. Il Consiglio dell'Unione europea l'11 febbraio 2026 ha adottato la "
     "<strong>VO (UE) 2026/382</strong>, che modifica il precedente regolamento sulle "
     "franchigie doganali (CE) n. 1186/2009 – <strong>con effetto dal 1° luglio 2026</strong>."
     "</p>\n"
     "<p>Da allora, per le spedizioni in vendita a distanza da Paesi terzi – quindi anche "
     "dalla Svizzera – si applica un <strong>dazio forfettario di 3 EUR per categoria di "
     "merci</strong>. «Categoria di merci» significa: per ciascuna voce della dichiarazione "
     "doganale. Un collo con tre gruppi di articoli diversi costa quindi 9 EUR di dazio, non "
     "3.</p>\n"
     "<p>L'amministrazione doganale tedesca (zoll.de) e il Ministero delle finanze austriaco "
     "(bmf.gv.at) confermano la disciplina in modo concorde. Importante: si tratta del "
     "<strong>dazio</strong> – l'IVA all'importazione continua a essere dovuta "
     "indipendentemente da ciò (la franchigia di 22 EUR per le imposte era già stata abolita "
     "nel 2021).</p>"),

    ("Spedizioni IOSS: sempre 3 EUR, nessuna preferenza",
     "<p>Molti shop svizzeri gestiscono i pacchi verso l'UE tramite la <strong>procedura "
     "IOSS</strong> (Import One-Stop-Shop): l'IVA viene riscossa già al checkout e versata "
     "attraverso uno Stato membro dell'UE. Per il dazio, IOSS non cambia nulla sul piano "
     "dell'obbligo di pagamento – anzi:</p>\n"
     "<p>Secondo il BMF austriaco, per le spedizioni IOSS l'art. 2 lett. a della VO (UE) "
     "2026/382 <strong>prevede in linea generale il dazio di 3 EUR; una preferenza doganale "
     "è esclusa</strong>. Nella dichiarazione doganale va indicato a tal fine il codice di "
     "preferenza «500». Chi vende tramite IOSS, quindi, calcoli stabilmente i 3 EUR per voce "
     "merceologica nel margine.</p>\n"
     "<p>Per le spedizioni non-IOSS in vendita a distanza fino a 150 EUR il dazio forfettario "
     "si applica ugualmente – in questo caso una preferenza (ad es. l'accordo di libero "
     "scambio Svizzera–UE) può eventualmente applicarsi, purché siano disponibili prove "
     "d'origine. A verificarlo è il prestatore di servizi doganali, caso per caso.</p>"),

    ("Cosa significa in concreto per gli shop svizzeri",
     "<p>Il dazio forfettario è piccolo – l'effetto, invece, non sempre:</p>\n"
     "<ul><li><strong>Valore del carrello:</strong> per un prodotto da 25 EUR, 3 EUR di dazio "
     "più i costi di sdoganamento sono un sovrapprezzo sensibile – e un classico motivo di "
     "abbandono al checkout, se il cliente lo scopre solo alla consegna.</li>\n"
     "<li><strong>Contare le voci:</strong> i pacchi misti sono fatturati per categorie di "
     "merci. Raggruppare l'assortimento (più esemplari della stessa categoria per pacco) "
     "resta vantaggioso dal punto di vista doganale.</li>\n"
     "<li><strong>Consegna vs. DDP:</strong> chi offre «Delivered Duty Paid» (sdoganamento a "
     "cura dello shop) deve anticipare i 3 EUR e calcolarli nel prezzo; chi lascia il "
     "pagamento al cliente rischia rifiuti alla consegna e resi.</li>\n"
     "<li><strong>Periodo natalizio:</strong> novembre e dicembre sono il primo picco sotto "
     "la nuova disciplina – la prima prova del fuoco per la logica del checkout e per la "
     "comunicazione.</li></ul>"),

    ("Regime transitorio fino a metà 2028",
     "<p>Il dazio forfettario di 3 EUR è espressamente una <strong>soluzione transitoria a "
     "termine</strong>. La vera riforma doganale dell'UE prevede una piattaforma centrale "
     "dei dati doganali dell'UE (Customs Data Hub) tramite la quale in futuro i prelievi "
     "all'importazione dovranno essere riscossi interamente in digitale – al più presto dal "
     "2028. Fino ad allora vale il regime forfettario per le spedizioni di scarso valore; i "
     "dettagli sugli importi di riferimento e sulle prove di sicurezza li disciplina il "
     "regolamento di esecuzione (UE) 2015/2447 (art. 155, par. 3, lett. c, delle "
     "disposizioni di applicazione del codice doganale dell'Unione, modificato dalla VO (UE) "
     "2026/1200).</p>\n"
     "<p>Per i venditori svizzeri ciò significa: i 3 EUR sono l'inizio, non la fine della "
     "regolamentazione. Chi oggi tiene in ordine i propri dati (codici merceologici, valori, "
     "origine) sarà avvantaggiato nel 2028.</p>"),

    ("Checklist: questi sei punti da verificare ora",
     "<ol><li><strong>Registrazione IOSS</strong> aggiornata? Numero di identificazione UE "
     "visibile al checkout?</li>\n"
     "<li><strong>Codici merceologici (codici CN)</strong> curati per ogni articolo – così la "
     "dichiarazione doganale raggruppa correttamente le voci?</li>\n"
     "<li><strong>Presentazione dei prezzi:</strong> il checkout indica «dazi inclusi» oppure "
     "«prezzo più prelievi all'importazione»? Entrambe le varianti sono lecite, fuorviare i "
     "clienti no.</li>\n"
     "<li><strong>Contratto logistico:</strong> chi effettua lo sdoganamento – corriere, "
     "spedizioniere doganale, shop? Chi sostiene i 3 EUR in caso di DDP?</li>\n"
     "<li><strong>Comunicazione con i clienti:</strong> testo informativo sulla pagina "
     "prodotto e nel tracciamento della spedizione.</li>\n"
     "<li><strong>Margine:</strong> 3 EUR per voce merceologica calcolati nell'assortimento – "
     "anche sulla merce in promozione?</li></ol>"),

    ("In sintesi",
     "<ul><li>Dal 1° luglio 2026: nella UE non esiste più la franchigia doganale di 150 EUR "
     "(VO (UE) 2026/382 del Consiglio dell'11 febbraio 2026).</li>\n"
     "<li>3 EUR di dazio per categoria di merci (per voce della dichiarazione doganale) per "
     "le spedizioni in vendita a distanza da Paesi terzi – anche dalla Svizzera.</li>\n"
     "<li>Per le spedizioni IOSS il dazio forfettario è sempre dovuto; preferenza doganale "
     "esclusa (codice 500).</li>\n"
     "<li>L'IVA all'importazione continua a essere dovuta indipendentemente.</li>\n"
     "<li>Regime transitorio fino alla piattaforma doganale UE (al più presto 2028) – curare "
     "i dati conviene due volte.</li>\n"
     "<li>Informazione generale, non consulenza legale – per il caso concreto si rivolga a "
     "uno spedizioniere doganale o a un avvocato specializzato.</li></ul>"),
]

build('it', 'eu-zoll-3-euro-kleinsendungen', TITLE_IT, META_IT, SECTIONS_IT,
      related=['mwst-ausfuhr-0-prozent-nachweis.html',
               'mwst-100k-pflicht-schweiz.html',
               'transparenzregister-tjpg-meldepflicht.html'])
