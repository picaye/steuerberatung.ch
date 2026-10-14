#!/usr/bin/env python3
"""Italian mirror of minijobs-lohnschwelle-ahv-pflicht.html (7 h2 sections).

Terms per references/multilang-glossary.md: AVS/AI/IPG/AD for AHV/IV/EO/ALV,
LAVS for AHVG, 'lavoro domestico', 'lavori occasionali di tasca',
imposta alla fonte, frontaliere. Formal Lei. Figures kept EXACTLY as DE:
CHF 2'500, CHF 750, 25 anni, 1.1.2025, Art. 52 LAVS.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

TITLE_IT = ("Mini-job e personale stagionale: quando scattano i contributi "
            "salariali e gli obblighi di annuncio")

META_IT = ("Impieghi brevi e irregolari fino a CHF 2'500 di salario per persona e "
           "per anno possono essere esenti da AVS – ma solo se il limite per datore "
           "di lavoro è rispettato. Soglia e non franchigia, eccezione per il lavoro "
           "domestico già dal primo franco, cultura e media inclusi dal 2026: la "
           "checklist per i datori di lavoro nel periodo natalizio.")

SECTIONS_IT = [
    ("Il limite di 2'500 franchi: salari di minima entità",
     "<p>Chi versa a un collaboratore occasionale <strong>al massimo CHF 2'500.-</strong> per "
     "anno civile, in linea di principio <strong>non deve conteggiare contributi AVS, AI, IPG e "
     "AD</strong> – salvo che la persona assicurata lo esiga espressamente. È la soglia di "
     "esenzione per compensi di minima entità (scheda informativa 2.04 delle casse di "
     "compensazione AVS). L'importo è stato aumentato dal 1° gennaio 2025 da CHF 2'300.- a "
     "CHF 2'500.-.</p>\n"
     "<p>Determinante: il limite vale <strong>per datore di lavoro e per anno civile</strong>. "
     "Tutte le retribuzioni che un datore di lavoro versa alla stessa persona nel corso "
     "dell'anno – inclusi accessori salariali, mance e prestazioni in natura – vanno sommate.</p>"),

    ("Soglia, non franchigia – l'errore classico",
     "<p>Se CHF 2'500.- è superato anche solo di un franco, <strong>non è soggetto a contributi "
     "soltanto l'importo eccedente, ma l'intero salario</strong>. Le casse di compensazione "
     "parlano deliberatamente di un limite, non di una deduzione. Chi a dicembre, con il terzo "
     "impiego, fa scattare la soglia, versa i contributi sul salario annuo a posteriori – "
     "interessi di mora inclusi.</p>\n"
     "<p>I contributi si calcolano sull'aliquota piena: 5,3 % AVS/AI/IPG più 1,1 % AD per parte "
     "(datore di lavoro e lavoratore: in totale 12,8 %, più spese amministrative e assegni "
     "familiari secondo la cassa cantonale).</p>"),

    ("Eccezioni: economie domestiche private, cultura e media",
     "<p>Per due ambiti la soglia di esenzione <strong>non si applica</strong> – i contributi "
     "sono dovuti già dal primo franco:</p>\n"
     "<ul><li><strong>Economie domestiche private</strong> (lavoro domestico: pulizie, giardino, "
     "cura dei figli, aiuto familiare): sempre soggetti a contributi (scheda informativa 2.06). "
     "Eccezione «lavori occasionali di tasca»: chi compie al massimo 25 anni nell'anno civile "
     "considerato guadagna fino a CHF 750.- per economia domestica privata e per anno senza "
     "contributi (al 2026: classi di nascita 2001–2008; oltre il limite non si applica più).</li>\n"
     "<li><strong>Operatori culturali e mediatici:</strong> i salari di produzioni di danza e "
     "teatro, produttori di suono e immagine, radio e televisione nonché istituti di formazione "
     "artistica sono sempre soggetti a contributi. <strong>Dal 1° gennaio 2026</strong> il "
     "Consiglio federale ha esteso l'obbligo contributivo, mediante una modifica della legge "
     "sulle prestazioni complementari (LPC), ad altri settori – tra cui design, musei, media e "
     "cori (informazione della cassa di compensazione AVS Soletta).</li></ul>"),

    ("Chi può esigere i contributi – e chi risponde",
     "<p>Anche sotto CHF 2'500.- la persona assicurata può <strong>esigere il versamento dei "
     "contributi</strong>. Conviene in particolare a studenti e giovani attivi: i contributi "
     "colmano le lacune contributive sul conto individuale AVS e possono essere successivamente "
     "computati nel contributo per persone senza attività lucrativa dei coniugi.</p>\n"
     "<p>Viceversa: se il lavoratore accetta il salario integrale senza deduzioni, il datore di "
     "lavoro <strong>non può più esigere retroattivamente</strong> i contributi della parte "
     "salariata. E chi, come datore di lavoro, non versa i contributi o li versa in ritardo, "
     "risponde secondo l'<strong>Art. 52 LAVS</strong> per l'intero danno – e quindi anche della "
     "quota del lavoratore, senza diritto di regresso.</p>"),

    ("Obblighi di annuncio e imposta alla fonte per i salari brevi",
     "<p>L'esenzione dai contributi non significa anonimato: anche i collaboratori con impiego di "
     "minima entità vanno annunciati alla cassa di compensazione non appena i contributi sono "
     "dovuti o richiesti. Per <strong>gli stranieri senza domicilio in Svizzera</strong> "
     "(frontalieri, persone in breve soggiorno) scatta inoltre l'<strong>imposta alla fonte già "
     "dal primo franco</strong> – la soglia AVS non protegge da essa. Il certificato di salario "
     "va emesso anche per i mini-job.</p>"),

    ("Checklist per l'inizio della stagione (da novembre a gennaio)",
     "<ol><li><strong>Registrare il salario annuo per persona e per datore di lavoro</strong> – "
     "inclusi tutti gli accessori salariali; prima di ogni nuovo impiego verificare l'importo "
     "cumulato.</li>\n"
     "<li><strong>Verificare il settore:</strong> economia domestica privata, cultura, design, "
     "media, museo, coro? Allora contributi dal primo franco.</li>\n"
     "<li><strong>Annotare l'età</strong> del collaboratore occasionale (regola dei lavori "
     "occasionali di tasca fino a 25 anni nelle economie domestiche).</li>\n"
     "<li><strong>Documentare l'esigibilità dei contributi</strong> se la persona desidera i "
     "versamenti.</li>\n"
     "<li><strong>Prevedere l'obbligo dell'imposta alla fonte</strong> dal primo franco in caso "
     "di domicilio all'estero.</li>\n"
     "<li><strong>Emettere e conservare il certificato di salario</strong> anche per i mini-job "
     "(10 anni).</li></ol>"),

    ("In breve",
     "<ul><li>Fino a CHF 2'500.- di salario per persona e per datore di lavoro nell'anno civile: "
     "nessun contributo AVS/AI/IPG/AD – salvo che la persona li richieda (scheda informativa "
     "2.04; limite in vigore dal 1.1.2025).</li>\n"
     "<li>Superamento = contributi sull'intero salario (soglia, non franchigia) – riscossione "
     "successiva con interessi di mora.</li>\n"
     "<li>Economie domestiche private nonché ambito cultura/media (dal 2026 esteso a design, "
     "musei, media, cori): contributi dal primo franco.</li>\n"
     "<li>Il datore di lavoro risponde secondo l'Art. 52 LAVS delle quote salariali non "
     "dedotte.</li>\n"
     "<li>L'imposta alla fonte in caso di domicilio all'estero si applica indipendentemente dal "
     "limite AVS.</li>\n"
     "<li>Informazione generale, non consulenza per casi individuali – le domande vanno rivolte "
     "alla cassa di compensazione competente.</li></ul>"),
]

build(
    "it",
    "minijobs-lohnschwelle-ahv-pflicht",
    TITLE_IT,
    META_IT,
    SECTIONS_IT,
    related=[
        "quellensteuer-nov-zusatzabzuege.html",
        "grenzgaenger-de-fr-it-steuern.html",
        "ahv-mindestbeitrag-selbststaendige.html",
    ],
)
