#!/usr/bin/env python3
"""Build the IT mirror of mwst-ausfuhr-0-prozent-nachweis.html from the DE article.

Figures kept EXACTLY as in DE (per site rule): 0 %, 8.1 %, 1.1.2026, 31.12.2025,
Mod. 11.44, 10 anni. IT terms per multilang-glossary: IVA, prova d'esportazione,
AFC, traffico turistico. Register: formal (voi, matching existing IT MWST article).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "mwst-ausfuhr-0-prozent-nachweis"
RELATED = ["eu-zoll-3-euro-kleinsendungen.html",
           "mwst-agov-pflicht-oktober-2026.html",
           "mwst-100k-pflicht-schweiz.html"]

IT_TITLE = "IVA 0 % all'esportazione: i documenti d'esportazione accettati dall'AFC"
IT_META = ("La merce esportata all'estero è esente da IVA, ma solo con una prova d'esportazione valida. "
           "Dal 2026 la dichiarazione d'esportazione passa da e-dec a Passar: quali documenti valgono "
           "(eVV Export, Mod. 11.44, documento d'esportazione per il traffico turistico) e cosa succede "
           "senza prova.")

IT_SECTIONS = [
    ("L'aliquota 0 % è una questione di prova",
     "<p>Le forniture all'estero sono esenti dall'imposta sul valore aggiunto oppure imponibili "
     "all'aliquota 0 % (Art. 6 cpv. 2 lett. a LTVA). Ma attenzione: l'esenzione <strong>non è un "
     "diritto automatico, bensì una questione di prova</strong>. L'AFC segue il principio secondo cui "
     "spetta al fornitore soggetto all'IVA dimostrare l'avvenuta esportazione. Se la prova non riesce, "
     "la fornitura viene tassata retroattivamente come operazione interna — con l'aliquota nazionale "
     "attualmente dell'8.1 %, anche se il cliente estero ha pagato netto.</p>"
     "<p>È il riscontro classico nelle verifiche IVA: vendita contabilizzata, imposta dichiarata allo "
     "0 %, ma nessun documento d'esportazione valido agli atti. La pretesa di restituzione dell'imposta "
     "incide per intero sul margine.</p>"),
    ("Passar ha sostituito e-dec Export (dal 1.1.2026)",
     "<p>Per la prova d'esportazione il 2026 ha portato un cambiamento fondamentale: l'UFD ha "
     "<strong>messo fuori servizio e-dec Export il 31.12.2025</strong>. Le dichiarazioni "
     "d'esportazione transitano <strong>dal 1.1.2026 esclusivamente tramite Passar</strong> "
     "(www.passar.admin.ch). Per gli esportatori ne derivano conseguenze pratiche:</p>"
     "<ul><li>La <strong>disposizione di sdoganamento elettronica esportazione (eVV Export)</strong> è "
     "il documento centrale della prova: va ritirata attivamente da Passar, manualmente con lo "
     "strumento «Chartera Output» o in modo automatizzato tramite un software doganale, e poi "
     "archiviata elettronicamente.</li>"
     "<li>La disposizione ha valore giuridico in formato PDF solo <strong>con la parte XML "
     "incorporata</strong> — uno screenshot o una semplice stampa non bastano.</li>"
     "<li>Per i prodotti a base di tabacco valgono termini transitori più lunghi; il <strong>Mod. "
     "11.44</strong> (copia della dichiarazione doganale vidimata dall'ufficio doganale per tabacco "
     "greggio e prodotti a base di tabacco) resta valido come forma di prova.</li>"
     "<li>e-dec Web può essere utilizzato provvisoriamente; la sostituzione definitiva sarà comunicata "
     "separatamente.</li></ul>"),
    ("Questi documenti d'esportazione sono accettati dall'AFC",
     "<p>L'UFD enuncia in linea di principio in modo esaustivo le prove d'esportazione valide:</p>"
     "<ol><li><strong>Disposizione di sdoganamento elettronica esportazione (eVV Export)</strong> con "
     "firma digitale — il caso normale delle esportazioni commerciali (dal 2026 da Passar).</li>"
     "<li><strong>Copia vidimata dall'ufficio doganale della dichiarazione doganale per tabacco greggio "
     "e prodotti a base di tabacco (Mod. 11.44).</strong></li>"
     "<li><strong>«Documento d'esportazione per il traffico turistico» confermato dall'ufficio "
     "doganale</strong> — il documento per i negozi che vendono merce a viaggiatori (procedura "
     "tax-free; dettagli presso l'AFC alla voce «VAT-Refund: Rückerstattung an Unternehmen im "
     "Ausland»).</li>"
     "<li><strong>Documenti doganali che attestano procedure regolarmente concluse</strong> — ad es. "
     "quando un oggetto importato temporaneamente in Svizzera viene esportato e sdoganato "
     "all'estero.</li></ol>"
     "<p>Se l'esportazione non può essere dimostrata con nessuno di questi documenti, scatta la regola "
     "residuale: le forniture devono essere tassate come operazioni interne.</p>"),
    ("Traffico turistico: il documento al valico di frontiera",
     "<p>Se un negozio vende a turisti, il <strong>documento d'esportazione per il traffico "
     "turistico</strong> sostituisce la dichiarazione doganale commerciale: la merce viene annunciata "
     "all'uscita presso l'ufficio doganale e vidimata oppure confermata elettronicamente (annuncio "
     "d'esportazione). Senza questo documento la fornitura è considerata un ricavo interno — il "
     "rimborso dell'imposta pagata alla clientela fallisce per mancanza di prova. Per le imprese con "
     "clientela dell'UE lo stesso procedimento vale, al contrario, anche per la verifica dei rimborsi "
     "tax-free.</p>"),
    ("Conservazione e prassi di controllo",
     "<p>I documenti commerciali — e quindi ogni prova d'esportazione — vanno conservati "
     "<strong>10 anni</strong> (Art. 49 cpv. 2 LTVA). Nelle verifiche l'AFC non controlla a campione "
     "«se si è esportato», ma <strong>se per ogni posizione esiste un documento</strong>. Il "
     "collegamento pulito tra fattura commerciale, dichiarazione Passar ed eVV Export (XML incluso) è "
     "metà della verifica IVA.</p>"
     "<p>Consiglio pratico: l'eVV Export contiene la conferma dello sdoganamento dell'esportazione; "
     "chi la «ritira e archivia proattivamente» (così raccomanda l'UFD) invece di lasciarla nel "
     "sistema evita la costellazione di errore più frequente: merce uscita, documento mai ritirato, "
     "imposta richiesta indietro.</p>"),
    ("Checklist per le imprese esportatrici",
     "<ol><li><strong>Onboarding Passar</strong> completato? UID registrata nell'amministrazione dei "
     "clienti doganali (ZKV), ruolo «Ritiro documenti nel traffico merci» attivato "
     "nell'ePortal?</li>"
     "<li><strong>Ritiro dell'eVV Export</strong> organizzato (Chartera Output o software doganale) — "
     "inclusa l'archiviazione del PDF con XML?</li>"
     "<li><strong>Traffico turistico:</strong> processi definiti per gli annunci d'esportazione al "
     "valico di frontiera?</li>"
     "<li><strong>Tabacco:</strong> disposizioni transitorie e Mod. 11.44 rispettati?</li>"
     "<li><strong>Fatturazione:</strong> aliquota 0 % con indicazione della prestazione "
     "d'esportazione; riferimento al numero della dichiarazione doganale?</li>"
     "<li><strong>Conservazione:</strong> documenti archiviati in modo a prova di revisione per "
     "10 anni?</li></ol>"),
    ("In breve",
     "<ul><li>Esenzione IVA all'esportazione = onere della prova a carico del fornitore; senza "
     "documento si riapplica retroattivamente l'8.1 %.</li>"
     "<li>Dal 1.1.2026: esportazione solo tramite Passar; e-dec Export è spento. La prova centrale è "
     "l'eVV Export con firma digitale (PDF valido solo con XML incorporato).</li>"
     "<li>Altri documenti validi: Mod. 11.44 (tabacco), documento d'esportazione per il traffico "
     "turistico, documenti doganali di procedura.</li>"
     "<li>Obbligo di conservazione: 10 anni.</li>"
     "<li>Informazione generale, non consulenza per casi singoli — in caso di dubbio rivolgersi "
     "all'AFC o a uno specialista IVA.</li></ul>"),
]

if __name__ == "__main__":
    build("it", SLUG, IT_TITLE, IT_META, IT_SECTIONS, related=RELATED)
