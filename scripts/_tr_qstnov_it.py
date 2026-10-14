#!/usr/bin/env python3
"""Build the Italian version of quellensteuer-nov-zusatzabzuege from the DE article."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

TITLE_IT = ("Imposta alla fonte: deduzioni ulteriori da comunicare entro il 31 marzo")

META_IT = ("Spese di malattia, formazione continua, spese professionali effettive, custodia da "
           "terzi: le deduzioni che la tariffa dell'imposta alla fonte non contiene si ottengono "
           "solo con l'imposizione ordinaria susseguiva su domanda (NOV). Domanda entro il 31 "
           "marzo dell'anno successivo – per il periodo 2026 quindi entro il 31.3.2027. Chi deve, "
           "chi dovrebbe, cosa si guadagna.")

SECTIONS_IT = [
    ("Perché la tariffa dell'imposta alla fonte deduce troppo poco",
     "<p>L'imposta alla fonte è un'<strong>imposta finale forfettaria</strong>: la tariffa "
     "contiene spese professionali, premi di assicurazione e deduzioni solo in modo forfettario. "
     "Chi ha costi effettivi più elevati – spese professionali effettive invece del forfait, "
     "spese di malattia e di infortunio, formazione continua, costi di custodia da terzi, "
     "versamenti al pilastro 3a, contributi di mantenimento – non ne vede traccia nella "
     "fatturazione mensile.</p>\n"
     "<p>Queste <strong>deduzioni ulteriori</strong> si possono ottenere solo tramite "
     "l'imposizione ordinaria susseguiva su domanda (NOV): l'autorità fiscale tassa come nel "
     "procedimento ordinario, imputa l'imposta alla fonte e rimborsa la differenza quando questa "
     "è risultata troppo elevata.</p>"),

    ("Il termine: 31 marzo dell'anno successivo",
     "<p>La domanda di imposizione ordinaria susseguiva è <strong>legata a un termine "
     "perentorio</strong>: deve pervenire all'ufficio cantonale delle contribuzioni <strong>entro "
     "la fine di marzo dell'anno successivo al periodo fiscale</strong> (scheda informativa AFC "
     "«Imposizione alla fonte»; analogamente l'ordinanza sull'imposta alla fonte del Cantone "
     "Zurigo: «entro fine marzo dell'anno successivo»; confermato dagli uffici delle contribuzioni "
     "FR e TG per la prassi dei periodi). Per il <strong>periodo fiscale 2026 il termine scade il "
     "31 marzo 2027</strong>.</p>\n"
     "<p>Chi perde il termine perde le deduzioni senza alcuna possibilità di recupero: senza NOV "
     "l'imposta alla fonte sostituisce definitivamente le imposte federali, cantonali e comunali "
     "sul reddito da attività lucrativa – deduzioni ulteriori non vengono più concesse.</p>"),

    ("Chi deve e chi dovrebbe presentare la domanda",
     "<p><strong>Obbligatoria</strong> è la NOV per le persone soggette all'imposta alla fonte "
     "domiciliate o soggiornanti in Svizzera quando il reddito lordo supera <strong>CHF "
     "120'000.- all'anno</strong> (scheda informativa AFC). In questo caso la tassazione avviene "
     "d'ufficio – la domanda non è necessaria, ma le deduzioni ulteriori vanno fatte valere.</p>\n"
     "<p><strong>Facoltativa</strong>: la domanda conviene a tutti gli altri le cui deduzioni "
     "effettive superano i forfaits della tariffa. Candidati tipici: persone con elevate spese "
     "effettive di tragitto e vitto, famiglie con custodia da terzi, persone con spese di malattia "
     "oltre le franchigie di deduzione, chi versa contributi di mantenimento.</p>\n"
     "<p><strong>Anche i non residenti</strong> (frontalieri, persone con soggiorno all'estero) "
     "possono domandare la NOV per far valere deduzioni personali – per loro il procedimento è "
     "l'unica strada verso queste deduzioni; la domanda va presentata pure entro il 31 marzo "
     "dell'anno successivo.</p>"),

    ("Correzione vs. deduzioni ulteriori: due domande distinte",
     "<p>Non ogni correzione richiede una NOV: se il <strong>salario lordo è stato determinato in "
     "modo errato, il reddito determinante per l'aliquota è stato calcolato male o è stata "
     "applicata una tariffa sbagliata</strong>, basta la domanda di ricalcolo dell'imposta alla "
     "fonte (art. 137 LIFD, art. 49 cpv. 2–2ter LHID) – anch'essa entro il 31 marzo dell'anno "
     "successivo. La NOV invece apre tutta la logica delle deduzioni della tassazione ordinaria, "
     "comprese le condizioni personali (stato civile, figli, sostanza).</p>"),

    ("Come funziona la domanda",
     "<p>Il modulo è disponibile presso l'ufficio cantonale delle contribuzioni (in molti Cantoni "
     "ogni anno online dal 1° gennaio al 31 marzo). Sposati e partner registrati devono "
     "<strong>firmare la domanda congiuntamente</strong>; essa deve indicare il periodo fiscale. "
     "Va corredata dei consueti giustificativi: certificati di salario, prove delle spese "
     "professionali, spese di malattia, versamenti 3a, costi di custodia e di mantenimento. La "
     "tassazione avviene secondo il diritto ordinario; l'imposta alla fonte trattenuta viene "
     "imputata. L'AFC di norma notifica la decisione di tassazione entro la fine dell'anno della "
     "domanda – poi decorrono le vie di diritto ordinarie (reclamo entro 30 giorni).</p>"),

    ("Esempio di calcolo: quando la domanda conviene",
     "<p>Valore orientativo: la tariffa dell'imposta alla fonte contiene un forfait per le spese "
     "professionali. Se i costi effettivi (spese di tragitto, vitto, formazione continua, studio "
     "professionale) sono nettamente superiori, la deduzione aumenta della differenza. A titolo "
     "d'esempio: chi può comprovare CHF 12'000.- di spese professionali vere invece del forfait "
     "tariffario di pochi migliaia di franchi riduce di conseguenza il reddito imponibile – con "
     "un'aliquota marginale del 15–25 % ciò significa un rimborso nell'ordine di CHF "
     "1'500.–3'000.- all'anno. Il calcolo esatto dipende da Cantone, Comune, stato civile e figli; "
     "gli uffici delle contribuzioni e i software fiscali cantonali permettono un calcolo "
     "approssimativo già prima della domanda.</p>"),

    ("In sintesi",
     "<ul><li>Le deduzioni ulteriori (spese professionali effettive, malattia, formazione "
     "continua, custodia da terzi, pilastro 3a, mantenimento) si ottengono solo con "
     "l'imposizione ordinaria susseguiva su domanda (NOV).</li>\n"
     "<li>Termine: 31 marzo dell'anno successivo – per il periodo 2026 entro il 31.3.2027. Senza "
     "domanda le deduzioni decadono.</li>\n"
     "<li>Obbligatoria con reddito lordo superiore a CHF 120'000.- (residenti); facoltativa per "
     "tutti, anche frontalieri.</li>\n"
     "<li>Tariffa sbagliata/salario errato → domanda di ricalcolo (art. 137 LIFD / art. 49 LHID), "
     "stesso termine.</li>\n"
     "<li>Informazione generale, non consulenza per il caso singolo – l'ufficio cantonale delle "
     "contribuzioni fornisce indicazioni.</li></ul>"),
]

build('it', 'quellensteuer-nov-zusatzabzuege', TITLE_IT, META_IT, SECTIONS_IT,
      related=['grenzgaenger-de-fr-it-steuern.html',
               'expats-steuern-schweiz.html',
               'saeule-3a-nachzahlen.html'])
