#!/usr/bin/env python3
# IT translations of all 5 new articles (formal register, matching it/kryptowaehrungen style)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import article_template as at

def P(s): return f'<p>{s}</p>'
def UL(items): return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def OL(items): return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

# ---------------- IT1: Verrechnungssteuer ----------------
at.build('it', 'verrechnungssteuer-schweiz-35-prozent',
 "Imposta preventiva del 35 %: recuperare dividendi e interessi",
 "Imposta preventiva Svizzera: il 35 % su dividendi e interessi (art. 13 LIP). Come recuperarla con la dichiarazione d'imposte – termine di 3 anni (art. 32 LIP), senza confusione con il modulo 110.",
 [
 ("Che cos'è l'imposta preventiva",
  P("L'imposta preventiva è un'imposta federale sui rendimenti del capitale: su dividendi, interessi e vincite da giochi in denaro viene trattenuto il <strong>35 per cento</strong> (art. 13 cpv. 1 lett. a LIP). Le rendite vitalizie e le pensioni sono colpite al 15 per cento, le altre prestazioni assicurative all'8 per cento.")
  + P("Il prelievo non lo effettua lo Stato, ma il debitore della prestazione: la vostra banca o la società trattiene l'imposta alla scadenza e la versa all'Amministrazione federale delle contribuzioni (AFC). Deve rendere più difficile l'evasione fiscale sui redditi di capitale – per questo l'aliquota è deliberatamente superiore al vostro carico fiscale effettivo.")),
 ("L'imposta non è una perdita – è pagata in anticipo",
  P("Per le persone fisiche domiciliate in Svizzera e illimitatamente imponibili, l'imposta preventiva non è un'imposta definitiva ma di sicurezza: potete chiederne la restituzione se dichiarate correttamente i rendimenti. Chi non la richiede regala soldi – con un deposito di CHF 2'000 tra dividendi e interessi si tratta già di CHF 700 l'anno.")),
 ("La via semplice: la dichiarazione d'imposte",
  P("Se presentate una dichiarazione d'imposte, il suo inoltro vale in pratica come richiesta di restituzione: è competente l'autorità fiscale del Cantone in cui avevate il domicilio alla fine dell'anno di scadenza (art. 30 LIP). L'elenco dei titoli della dichiarazione fa fede come richiesta – i Cantoni rimborsano l'imposta di regola fino all'importo della vostra imposta cantonale e comunale (art. 31 LIP).")
  + P("Importante per i depositanti: indicate tutti i dividendi e interessi, anche gli importi minori, nell'elenco dei titoli. Una posizione dimenticata è esattamente l'importo che manca alla restituzione.")),
 ("Senza dichiarazione d'imposte: modulo 25",
  P("Chi non presenta una dichiarazione d'imposte (per esempio perché il Cantone di domicilio non la esige) chiede la restituzione con il <strong>modulo 25</strong> tramite il portale AFC. Attenzione, confusione frequente: <strong>il modulo 110 non fa per voi</strong> – serve alla società debitrice per annunciare il proprio conteggio (entro 30 giorni dall'assemblea generale). Come privato non recuperate nulla.")),
 ("Termine: tre anni dopo l'anno di scadenza",
  P("Il diritto alla restituzione si estingue se la richiesta non è presentata <strong>entro tre anni dalla fine dell'anno civile</strong> in cui la prestazione è diventata esigibile (art. 32 cpv. 1 LIP). Esempio: dividendo pagato il 15 maggio 2023 → scadenza del termine il 31 dicembre 2026. Un termine mancato è perso definitivamente, anche per buoni motivi.")),
 ("Gli errori più comuni in sintesi",
  UL([
   "<strong>«Restituzione entro 30 giorni»</strong> – falso. Il termine di 30 giorni riguarda l'annuncio della società debitrice (modulo 110), non la vostra richiesta.",
   "<strong>«Se non faccio nulla l'imposta è persa»</strong> – è persa se non fate nulla per tre anni. Altrimenti la riottenete.",
   "<strong>«L'imposta alla fonte estera la rimborsa la Svizzera»</strong> – no, vale la rispettiva convenzione contro la doppia imposizione; l'imposta preventiva svizzera è indipendente da ciò."])),
 ("In breve",
  OL([
   "35 % su dividendi/interessi, 15 % su rendite/pensioni, 8 % su altre prestazioni assicurative (art. 13 LIP).",
   "Con la dichiarazione d'imposte, la dichiarazione completa vale come richiesta di restituzione presso il Cantone di domicilio (art. 30 LIP).",
   "Senza dichiarazione: modulo 25 tramite portale AFC.",
   "Termine: 3 anni dopo la fine dell'anno di scadenza (art. 32 cpv. 1 LIP) – non 30 giorni."])
  + P("Non siete sicuri che il vostro elenco dei titoli sia completo? Tramite la <a href=\"kontakt.html\">pagina di contatto</a> vi mettiamo in contatto con un partner verificato del vostro Cantone – il primo preventivo mostra in trasparenza quanto costa l'esame.")),
 ])

# ---------------- IT2: Grenzgänger ----------------
at.build('it', 'grenzgaenger-de-fr-it-steuern',
 "Frontalieri DE/FR/IT: imposta alla fonte del 4,5 % e moduli",
 "Frontalieri in Svizzera: 4,5 % di imposta alla fonte (art. 15a CDI CH-DE), modulo Gre-1, 60 giorni di non ritorno, scadenza tedesca 31 luglio. Francia e Italia seguono regole diverse – la panoramica 2026.",
 [
 ("Chi è frontaliere in senso fiscale",
  P("Siete frontaliere in senso fiscale solo se tutte le condizioni sono adempite: domicilio all'estero (DE, FR o IT), datore di lavoro e luogo di lavoro in Svizzera, <strong>ritorno quotidiano</strong> al domicilio – e il ritorno deve essere ragionevole. Nella prassi dei Cantoni ciò significa: al massimo 100 chilometri in auto o al massimo 1,5 ore con i trasporti pubblici.")
  + P("Attenzione: il permesso per frontalieri (attestato G) è un'altra cosa – non conferisce lo status fiscale di frontaliere. Chi non rientra ogni giorno è soggiornante internazionale settimanale e viene tassato alla fonte con le aliquote ordinarie svizzere.")),
 ("Germania: 4,5 % alla fonte – ma solo con Gre-1",
  P("I veri frontalieri tedeschi sono tassati in Svizzera forfettariamente al <strong>4,5 per cento del salario lordo</strong> (art. 15a CDI CH-DE). Ma non è automatico: dovete consegnare al datore di lavoro l'<strong>attestato di residenza, modulo Gre-1</strong>, rilasciato dal fisco tedesco. Senza Gre-1 il datore di lavoro conta all'aliquota ordinaria – spesso nettamente di più.")
  + P("Il Gre-1 vale per un anno civile e va consegnato al datore di lavoro ogni anno di nuovo; dopo il primo anno il fisco tedesco di norma lo rilascia automaticamente. Serve un modulo separato per ogni datore di lavoro.")),
 ("Il limite dei 60 giorni di non ritorno",
  P("Se per motivi professionali (viaggi d'affari, reperibilità, formazione) non rientrate a casa per <strong>più di 60 giorni</strong> nell'anno civile, perdete l'aliquota da frontaliere. Il vostro reddito svizzero è ricalcolato alle aliquote ordinarie e tassato nuovamente. I giorni di non ritorno professionali devono essere certificati dal datore di lavoro con il <strong>modulo Gre-3</strong> – nel Cantone di Zurigo per scritto, per singolo datore di lavoro e entro il <strong>31 marzo dell'anno successivo</strong> presso l'Ufficio cantonale d'imposta (il termine varia per Cantone). I pernottamenti privati non contano.")),
 ("Germania: dichiarazione fino al 31 luglio",
  P("Anche se la Svizzera ha incassato il 4,5 %: in Germania siete illimitatamente imponibili sul reddito mondiale e dovete dichiarare i proventi da frontaliere nella dichiarazione dei redditi. Il termine generale di presentazione per la dichiarazione tedesca 2025 scade il <strong>31 luglio 2026</strong>; con assistenza fiscale (Lohnsteuerhilfeverein, consulente fiscale) più tardi. L'imposta alla fonte svizzera viene accreditata in Germania, così non resta doppia imposizione.")),
 ("Francia e Italia: regole completamente diverse",
  P("<strong>Francia:</strong> la convenzione per frontalieri del 1983 vale solo per luoghi di lavoro nei Cantoni BE, BL, BS, JU, NE, SO, VD e VS. Fuori da questa zona – per esempio Ginevra – vale la CDI ordinaria con imposta alla fonte svizzera ad aliquota ordinaria e imposizione in Francia con accredito; i dettagli dipendono dal Cantone di attività.")
  + P("<strong>Italia:</strong> dalla convenzione riveduta (in vigore dal 17 luglio 2023, applicabile dal 2024) i «nuovi» frontalieri – assunti dopo il 17 luglio 2023 – possono essere tassati in Svizzera fino all'80 per cento dell'imposta alla fonte ordinaria; l'Italia accredita tale imposta. Per i frontalieri assunti prima di tale data vale una disciplina transitoria fino a fine 2033. Il lavoro a domicilio è possibile fino al 25 per cento dell'orario di lavoro senza mettere a rischio lo status.")),
 ("Gli errori più frequenti",
  UL([
   "<strong>Attestato G = status fiscale?</strong> No – contano il ritorno quotidiano e la sua ragionevolezza.",
   "<strong>Dimenticare il Gre-1</strong> → aliquota ordinaria invece del 4,5 %, correzione laboriosa.",
   "<strong>Giorni di non ritorno documentati male</strong> → Gre-3 oltre il termine, tassazione ordinaria successiva.",
   "<strong>«Moduli 130/140/150 all'AVS»?</strong> Non esistono – l'AVS non è mai competente per l'imposta alla fonte; le attestazioni passano dal datore di lavoro e dagli uffici fiscali cantonali."])),
 ("In breve",
  OL([
   "4,5 % di imposta alla fonte svizzera per i veri frontalieri tedeschi – solo con modulo Gre-1 al datore di lavoro.",
   "Oltre 60 giorni di non ritorno professionali (Gre-3) → aliquota ordinaria, tassazione successiva.",
   "Lato tedesco: allegato N-GRE, termine dichiarazione 2025 al 31 luglio 2026.",
   "FR: convenzione 1983 solo in 8 Cantoni di frontiera; IT: nuovo regime dal 2024 (fino a 80 % imposta alla fonte CH, accredito, transizione fino al 2033)."])
  + P("Avete alle spalle un anno di lavoro a domicilio con molti giorni di viaggio? È esattamente lì che si complica. Tramite la <a href=\"kontakt.html\">pagina di contatto</a> vi mettiamo in contatto con un partner verificato – con preventivo trasparente prima di ogni incarico.")),
 ])

# ---------------- IT3: Hypothek ----------------
at.build('it', 'hypothek-steuerabzug-schweiz',
 "Mutuo e imposte: interessi, deduzioni e limiti",
 "Dedurre gli interessi ipotecari nel 2026: interessi passivi privati fino al rendimento della sostanza più CHF 50'000 (art. 33 cpv. 1 lett. a LIFD). Come si dichiarano – e cosa NON potete dedurre.",
 [
 ("Il principio: valore locativo contro deduzioni",
  P("Chi abita in un immobile di proprietà dichiara il <strong>valore locativo</strong> – un canone fittizio aggiunto al reddito. In cambio potete dedurre i costi dell'oggetto: soprattutto gli interessi ipotecari, la manutenzione e i contributi per risparmio energetico e protezione. Il sistema vuole trattare fiscalmente in modo comparabile la proprietà data in affitto e quella abitata – non è un regalo.")),
 ("Interessi ipotecari: deducibili, ma con tetto",
  P("Gli interessi ipotecari per immobili abitati dal proprietario sono <strong>interessi passivi privati</strong>. Nell'imposta federale diretta sono deducibili – ma non senza limiti: solo nella misura dei <strong>rendimenti imponibili della sostanza più ulteriori CHF 50'000</strong> (art. 33 cpv. 1 lett. a LIFD). Se avete pochi rendimenti di capitale (interessi, dividendi, fitti), scatta il tetto: non tutto ciò che la banca vi addebita nell'anno finisce nella dichiarazione. I Cantoni trattano gli interessi passivi privati in modo diverso – per la vostra dichiarazione vale il diritto cantonale.")),
 ("Dichiarare correttamente: elenco dei debiti, modulo 14",
  P("Iscrivete tutti i mutui e i prestiti nell'<strong>elenco dei debiti (modulo 14)</strong>: creditore, debito residuo a fine anno, importo degli interessi. Giustificativo è l'<strong>attestato degli interessi della vostra banca</strong> – senza, l'autorità fiscale non accetta la deduzione. Il debito riduce inoltre la vostra sostanza imponibile; l'imposta sulla sostanza cala.")),
 ("Cosa NON potete dedurre",
  UL([
   "<strong>Interessi del credito di costruzione durante la fase edilizia:</strong> sono costi d'acquisto dell'edificio, non deduzione dal reddito – recuperabili più tardi con l'ammortamento dei costi di costruzione.",
   "<strong>Lusso:</strong> allestimenti di carattere lussuoso (jacuzzi, area benessere su misura) sono regolarmente rifiutati come manutenzione dalle autorità fiscali.",
   "<strong>Regole inventate:</strong> una «deduzione forfettaria del 5 % sul mutuo» non esiste, né moduli «presso l'AVS» – l'AVS non è mai competente per i mutui."])),
 ("Strategia: ammortare o no?",
  P("Interessi ipotecari più alti rendono attraente l'ammortamento: ogni scaglione rimborsato fa risparmiare interessi futuri – ma riduce anche la deduzione e aumenta netta il reddito imponibile. Chi è vicino al tetto degli interessi passivi privati spesso guadagna di più ammortando che contando su una deduzione (bloccata). Il confronto valore locativo/deduzioni è questione cantonale e individuale – qui una consulenza su misura paga più che altrove.")),
 ("In breve",
  OL([
   "Gli interessi ipotecari sono deducibili – ma gli interessi passivi privati sono limitati, a livello federale, al rendimento della sostanza + CHF 50'000 (art. 33 cpv. 1 lett. a LIFD).",
   "Dichiarazione nell'elenco dei debiti, modulo 14; giustificativo = attestato degli interessi della banca.",
   "Gli interessi della fase di costruzione sono costi d'acquisto, non deduzioni dal reddito.",
   "Verificare le differenze cantonali – soprattutto su ammortamento e valore locativo."])
  + P("Incerti se le vostre deduzioni toccano il tetto? Tramite la <a href=\"kontakt.html\">pagina di contatto</a> troviamo un partner verificato della vostra regione – preventivo prima di ogni incarico.")),
 ])

# ---------------- IT4: MWST ----------------
at.build('it', 'mwst-100k-pflicht-schweiz',
 "IVA dai CHF 100'000: quando scatta l'obbligo",
 "Obbligo IVA in Svizzera: da 100'000 CHF di fatturato mondiale (art. 10 LTVA), annuncio entro 30 giorni tramite modulo online AFC, aliquote 8,1 % / 2,6 %. Soglie, termini ed eccezioni 2026.",
 [
 ("La soglia: 100'000 franchi – a livello mondiale",
  P("Diventate soggetti all'IVA se la vostra azienda realizza ogni anno <strong>CHF 100'000 o più</strong> con prestazioni non escluse dall'imposta (art. 10 cpv. 2 LTVA). Importante: il conteggio riguarda il fatturato <strong>in Svizzera e all'estero</strong>, non solo quello svizzero. Le prestazioni escluse (per esempio locazione di abitazioni, operazioni assicurative e bancarie, alcune prestazioni di formazione) non contano.")
  + P("Chi resta sotto la soglia non è soggetto all'imposta – eccezione per le associazioni: società sportive e culturali senza scopo di lucro e gestite a titolo onorifico, nonché organizzazioni di utilità pubblica hanno una soglia maggiorata di <strong>CHF 250'000</strong> (art. 10 cpv. 2 lett. c LTVA). Il riferimento è un anno; chi può prevedere di superare la soglia nei dodici mesi successivi diventa soggetto già prima.")),
 ("Annuncio: spontaneo, entro 30 giorni",
  P("Non appena superate la soglia (o è prevedibile), dovete annunciarvi <strong>spontaneamente entro 30 giorni</strong> dall'inizio della soggezione per scritto all'AFC (art. 66 cpv. 1 LTVA). Nessuno vi scrive per primo. L'annuncio avviene con il <strong>questionario online dell'AFC</strong>; ricevete un numero IVA non cedibile. Pericolo di confusione: il «modulo 25» riguarda la restituzione dell'imposta preventiva – per l'IVA vale il modulo online AFC.")
  + P("Viceversa: chi resta sotto la soglia può rinunciare volontariamente all'esenzione e annunciarsi (art. 11/14 LTVA) – conviene per il diritto alla deduzione dell'IVA precedente soprattutto con investimenti elevati. Attenzione: chi indica l'IVA in fattura senza averne diritto la deve comunque all'AFC (art. 27 LTVA).")),
 ("Le aliquote 2026",
  P("Vigono: <strong>aliquota normale 8,1 per cento</strong>, <strong>aliquota ridotta 2,6 per cento</strong> (art. 25 LTVA). L'aliquota ridotta vale tra l'altro per generi alimentari secondo la legge sugli alimenti (senza bevande alcoliche), acqua di rete, medicinali, libri e stampa. Attenzione, errore diffuso: <strong>per le prestazioni dell'industria alberghiera e della ristorazione vale l'aliquota normale</strong> – servizio al tavolo e consumo sul posto non sono ridotti, anche se i viveri in sé lo sarebbero. Chi calcola «ristorazione al 2,6 %» ha studiato male.")),
 ("Contabilizzazione: trimestrale, semestrale o a saldo",
  P("La regola è il <strong>contabile trimestrale</strong> tramite il portale IVA dell'AFC. Le piccole imprese (poca imposta per anno) possono contabilizzare semestralmente o annualmente; molti PMI usano l'<strong>imposta a saldo</strong> (Saldosteuersätze) – aliquote forfettarie per settore che riducono l'onere contabile, perché l'IVA precedente non va giustificata singolarmente.")),
 ("Secondo lavoro, associazione, piattaforma: quando siete comunque «azienda»",
  P("Azienda è chi esercita un'attività professionale o commerciale orientata alla riscossione duratura di proventi (art. 10 cpv. 1bis LTVA) – anche accanto al lavoro principale e anche al 20 per cento su una piattaforma. Commissioni di consulenza ricorrenti, vendite in shop o locazioni con infrastrutture possono far scattare la soggezione prima che ve ne accorgiate. Prestazioni sporadiche e vere operazioni occasionali no.")),
 ("In breve",
  OL([
   "Obbligo da CHF 100'000 di fatturato mondiale da prestazioni non escluse (art. 10 cpv. 2 LTVA); società sportive/culturali ed enti di utilità pubblica: CHF 250'000.",
   "Annuncio: entro 30 giorni, spontaneo, questionario online AFC – non modulo 25.",
   "Aliquote 2026: 8,1 % normale, 2,6 % ridotta; ristorazione = aliquota normale.",
   "L'annuncio volontario porta la deduzione dell'IVA precedente; l'imposta indicata senza diritto è dovuta (art. 27)."])
  + P("Avete appena (o state per) superare i 100'000 e volete partire in regola? Tramite la <a href=\"kontakt.html\">pagina di contatto</a> vi mettiamo in contatto con un partner verificato per il primo annuncio IVA – con preventivo prima dell'incarico.")),
 ])

# ---------------- IT5: AHV ----------------
at.build('it', 'ahv-mindestbeitrag-selbststaendige',
 "AVS 2026: contributo minimo CHF 530 e scala dei contributi per gli indipendenti",
 "Contributi AVS/AI/IPG degli indipendenti 2026: 10 % totali (AVS 8,1, AI 1,4, IPG 0,5), scala decrescente sotto CHF 60'500, contributo minimo CHF 530. Più le rendite 2026 e la 13a rendita da dicembre 2026.",
 [
 ("Cosa pagano gli indipendenti",
  P("I lavoratori indipendenti pagano <strong>interamente da soli</strong> i contributi AVS, AI e IPG – non c'è un datore di lavoro che ne assume metà. Aliquota 2026: AVS 8,1 % + AI 1,4 % + IPG 0,5 % = <strong>10,0 per cento in totale</strong> sul reddito netto dell'attività indipendente. Per paragone: dipendenti e datori di lavoro si dividono il 10,6 % a metà, 5,3 % ciascuno.")),
 ("La scala decrescente: reddito più basso, aliquota più bassa",
  P("Per redditi annui <strong>sotto i CHF 60'500</strong> vale un'aliquota ridotta – la «scala decrescente» (scheda informativa AVS 2.02). Parte dal <strong>5,371 per cento</strong> per redditi da CHF 10'100 e sale a scaglioni fino al 10,0 per cento pieno da CHF 60'500. Esempio: con CHF 40'500 di reddito pagate 6,728 % ≈ CHF 2'725 invece dei 4'050 franchi pieni. Il reddito determinante è il reddito netto che la vostra cassa di compensazione fissa con decisione di contribuzione.")),
 ("Contributo minimo CHF 530",
  P("Se conseguite meno di CHF 10'100 di reddito annuo, pagate il <strong>contributo minimo di CHF 530 l'anno</strong> (corrisponde a un salario annuo di CHF 5'000). Anche i senza attività lucrativa pagano almeno 530 e al massimo 26'500 franchi. Chi ha già versato il contributo minimo su un salario può chiedere che i contributi sull'attività indipendente siano riscossi solo all'aliquota più bassa della scala (5,371 %).")
  + P("Attività accessoria: se esercitate l'attività indipendente solo in via accessoria e il reddito non supera CHF 2'500 l'anno, i contributi sono riscossi soltanto su vostra espressa richiesta (scheda 2.02).")),
 ("Rendite AVS 2026",
  P("La rendita intera (periodo di contribuzione completo) si colloca nel 2026 tra <strong>CHF 1'260 e CHF 2'520 al mese</strong> – cioè <strong>15'120–30'240 franchi l'anno</strong> (UFAS). Le coppie ricevono due rendite individuali, limitate insieme al 150 per cento della rendita massima: al massimo <strong>CHF 3'780 al mese</strong> (45'360 l'anno). L'importo dipende dal periodo di contribuzione e dal reddito medio.")),
 ("La 13a rendita AVS arriva – prima volta a dicembre 2026",
  P("Il popolo ha approvato la 13a rendita di vecchiaia. Sarà versata <strong>per la prima volta con la rendita di dicembre 2026</strong> come supplemento: un dodicesimo (8,333 per cento) di tutte le rendite mensili percepite da gennaio a dicembre 2026. Chi a dicembre 2026 percepisce una rendita di vecchiaia riceve il supplemento automaticamente dalla cassa di compensazione AVS – non serve alcuna domanda.")),
 ("Errori frequenti",
  UL([
   "<strong>Confondere la base contributiva:</strong> determinante è l'utile netto dell'attività indipendente secondo la tassazione, non uno «stipendio».",
   "<strong>Interesse moratorio del 5 %:</strong> pagare la fattura annua oltre 30 giorni dalla data la rende decisamente più cara.",
   "<strong>Contributo minimo pagato due volte</strong> nonostante l'accredito dal salario – correggibile con giustificativo.",
   "<strong>Cassa assegni familiari dimenticata:</strong> a seconda del Cantone si aggiungono contributi agli assegni familiari."])),
 ("In breve",
  OL([
   "Indipendenti: 10,0 % AVS/AI/IPG (8,1 + 1,4 + 0,5), aliquota piena da CHF 60'500.",
   "Sotto: scala decrescente da 5,371 % (da CHF 10'100); sotto 10'100: contributo minimo CHF 530.",
   "Rendite 2026: 1'260–2'520 CHF/mese (15'120–30'240 CHF/anno), massimo coppia 3'780 CHF/mese.",
   "13a rendita AVS: primo supplemento con la rendita di dicembre 2026, automatico."])
  + P("Volete sapere come ottimizzare i contributi e quanto costano le lacune contributive? Tramite la <a href=\"kontakt.html\">pagina di contatto</a> vi mettiamo in contatto con un partner verificato – primo preventivo trasparente, prima di ogni incarico.")),
 ])
print("ALL IT built")
