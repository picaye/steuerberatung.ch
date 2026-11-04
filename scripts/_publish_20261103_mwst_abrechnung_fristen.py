#!/usr/bin/env python3
"""Build mwst-abrechnung-fristen in all 4 languages (todo-worker, 2026-11-03).

Pino task (todo.md 2026-11-03 19:2x): generate articles for keyword research —
"mwst abrechnung frist" + "mehrwertsteuer jahresabrechnung frist" share ONE
evergreen article. No year in title/H1; datePublished = build day only.

EVERY figure claim-checked 2026-11-03 via scripts/claim_check.py
(model jev-latest): data/claim-check/claims-mwst-fristen.json +
sources-mwst-fristen.json -> results-mwst-fristen.json: 11/11 supports,
0 needs_review, 0 contradictions. Primary sources: fedlex MWSTG (SR 641.20)
Art. 35/35a/71/72/86/86a/87/88 + ESTV «Fristverlängerung für die Einreichung
der MWST-Abrechnung» (deadline table; updated 22.9.2026, curl 200 today).
Source URLs re-curled 200 today: fedlex de/fr/it/en + estv.de pages.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build, BASE

SLUG = "mwst-abrechnung-fristen"
RELATED3 = ["mwst-100k-pflicht-schweiz.html",
            "mwst-ausfuhr-0-prozent-nachweis.html",
            "transparenzregister-tjpg-meldepflicht.html"]

URLS_DE = [
 ("https://www.fedlex.admin.ch/eli/cc/2009/615/de",
  "FedLex: Bundesgesetz über die Mehrwertsteuer (MWSTG, SR 641.20)"),
 ("https://www.estv.admin.ch/de/mwst-fristverlaengerung-einreichung-abrechnung",
  "ESTV: Fristverlängerung für die Einreichung der MWST-Abrechnung"),
 ("https://www.estv.admin.ch/de/mehrwertsteuer-abrechnen",
  "ESTV: Mehrwertsteuer abrechnen"),
]
URLS_OTHER = [
 ("https://www.fedlex.admin.ch/eli/cc/2009/615/{l}", None),
 ("https://www.estv.admin.ch/de/mwst-fristverlaengerung-einreichung-abrechnung", "DE"),
 ("https://www.estv.admin.ch/de/mehrwertsteuer-abrechnen", "DE"),
]
LAB = {
 "en": ["FedLex: Federal Act on Value Added Tax (VAT Act, MWSTG, SR 641.20)",
        "FTA: extension of the deadline for filing VAT returns (German)",
        "FTA: settling VAT (German)"],
 "fr": ["FedLex : loi fédérale régissant la TPA (LTVA, RS 641.20)",
        "AFC : prolongation du délai de dépôt du décompte TVA (all.)",
        "AFC : décompte TVA (all.)"],
 "it": ["FedLex: legge federale sull’imposta sul valore aggiunto (LIVA, RS 641.20)",
        "AFC: proroga del termine per il recapito del conteggio IVA (ted.)",
        "AFC: conteggio IVA (ted.)"],
}
def sources(lang):
    if lang == "de":
        return URLS_DE
    return [(u.replace("{l}", lang), LAB[lang][i]) for i,(u,_) in enumerate(URLS_OTHER)]

CTA = {
 "de": '<div class="cta-mid"><strong>Unsicher, welche Abrechnungsperiode für Ihr Unternehmen die richtige ist?</strong> Eine <a href="partner-pruefung.html">geprüfte Fachperson</a> prüft Ihre Zahlen und erledigt das Gesuch bei der ESTV – die Erstberatung ist kostenlos: <a href="kontakt.html">unverbindliche Offerte anfragen</a>.</div>',
 "en": '<div class="cta-mid"><strong>Not sure which settlement period fits your company?</strong> A <a href="partner-pruefung.html">vetted professional</a> reviews your numbers and files the request with the FTA – first consultation free: <a href="kontakt.html">request a no-obligation quote</a>.</div>',
 "fr": '<div class="cta-mid"><strong>Vous ne savez pas quelle période de décompte convient à votre entreprise ?</strong> Un <a href="partner-pruefung.html">spécialiste vérifié</a> examine vos chiffres et dépose la demande auprès de l’AFC – premier conseil gratuit : <a href="kontakt.html">demandez une offre sans engagement</a>.</div>',
 "it": '<div class="cta-mid"><strong>Non siete sicuri di quale periodo di conteggio sia giusto per la vostra azienda?</strong> Un <a href="partner-pruefung.html">consulente verificato</a> esamina i vostri numeri e presenta la richiesta all’AFC – prima consulenza gratuita: <a href="kontakt.html">richiedete un’offerta senza impegno</a>.</div>',
}

# ---------------- DE ----------------
de_sections = [
 ("Die 60-Tage-Regel: Einreichen und Zahlen laufen parallel",
  """<p>Die wichtigste Frist der Mehrwertsteuer: <strong>innert 60 Tagen nach Ablauf jeder Abrechnungsperiode</strong> ist die Abrechnung unaufgefordert bei der Eidgenössischen Steuerverwaltung (ESTV) einzureichen – und die in dieser Periode entstandene Steuerforderung ist in derselben Frist zu begleichen (Art. 71 Abs. 1 und Art. 86 Abs. 1 MWSTG). Die ESTV mahnt nicht vorher; die Pflicht tritt automatisch mit jeder Periode ein.</p>
<p>Bei verspäteter <strong>Zahlung</strong> wird ohne Mahnung ein Verzugszins geschuldet (Art. 87 Abs. 1 MWSTG). Umgekehrt wirkt die Frist zugunsten der steuerpflichtigen Person: Erstattet die ESTV einen Überschuss aus der Abrechnung nicht innert 60 Tagen nach deren Eintreffen, so wird ab dem 61. Tag ein Vergütungszins ausgerichtet (Art. 88 Abs. 4 MWSTG).</p>
<p><em>Praxis-Tipp:</em> Die Termine fallen jedes Jahr auf dieselben Daten – siehe Tabelle unten. Wer die Abrechnungsperioden als wiederkehrende Einträge im Kalender führt, verpasst nichts.</p>"""),
 ("Welche Abrechnungsperiode für Ihr Unternehmen gilt",
  """<p>Das Gesetz sieht ein gestaffeltes System vor (Art. 35 MWSTG):</p>
<ul>
<li><strong>Vierteljährliche Abrechnung</strong> – die Regel für alle Unternehmen, die nach der effektiven Methode abrechnen.</li>
<li><strong>Halbjährliche Abrechnung</strong> – für Unternehmen, die die Saldosteuersatzmethode anwenden.</li>
<li><strong>Jährliche Abrechnung</strong> – auf Antrag möglich bei einem Umsatz aus steuerbaren Leistungen von höchstens CHF 5'005'000 pro Jahr.</li>
<li><strong>Monatliche Abrechnung</strong> – auf Antrag bei regelmässigem Vorsteuerüberschuss; so fliesst die Erstattung schneller.</li>
</ul>
<p>Zwei Regeln zum Wechseln, die oft übersehen werden: Wechsel sind nur auf Beginn einer Steuerperiode (in der Regel das Kalenderjahr) möglich, und die jährliche Abrechnung muss mindestens eine ganze Steuerperiode beibehalten werden. Wer von jährlich auf monatlich, vierteljährlich oder halbjährlich wechselt, kann frühestens nach drei Steuerperioden zur jährlichen Abrechnung zurückkehren. Kommt ein Unternehmen Abrechnungs- und Zahlungspflichten nicht nach, kann die ESTV die Genehmigung für die jährliche Abrechnung verweigern oder widerrufen (Art. 35a MWSTG).</p>""" + CTA["de"]),
 ("Die Fristen auf einen Blick (ESTV-Tabelle)",
  """<p>Die ESTV publiziert die Einreichefristen je Periode. Massgebend ist stets die 60-Tage-Regel; die festen Stichtage daraus:</p>
<table><thead><tr><th>Abrechnung</th><th>Abrechnungsperiode</th><th>Eingereicht und bezahlt bis</th></tr></thead><tbody>
<tr><td>1. Quartal</td><td>1. Januar – 31. März</td><td>31. Mai</td></tr>
<tr><td>2. Quartal</td><td>1. April – 30. Juni</td><td>31. August</td></tr>
<tr><td>3. Quartal</td><td>1. Juli – 30. September</td><td>30. November</td></tr>
<tr><td>4. Quartal</td><td>1. Oktober – 31. Dezember</td><td>28./29. Februar</td></tr>
<tr><td>1. Semester</td><td>1. Januar – 30. Juni</td><td>31. August</td></tr>
<tr><td>2. Semester</td><td>1. Juli – 31. Dezember</td><td>28./29. Februar</td></tr>
<tr><td>Jahresrechnung</td><td>1. Januar – 31. Dezember</td><td>28./29. Februar</td></tr>
<tr><td>Monatsbeispiel</td><td>1. – 31. Januar</td><td>31. März</td></tr>
</tbody></table>
<p>Endet die Steuerpflicht, läuft die 60-Tage-Frist ab diesem Zeitpunkt (Art. 71 Abs. 2 MWSTG) – die Schlussabrechnung gehört also nicht automatisch ans Kalenderjahresende.</p>"""),
 ("Jährliche Abrechnung: Raten ersetzen die Quartalsabrechnung",
  """<p>Wer jährlich abrechnet, zahlt die Steuer nicht erst nach Jahresende: Die ESTV erhebt einen provisorischen Steuerbezug in Raten (Art. 86a MWSTG). Bei der effektiven Methode und bei Pauschalsteuersätzen beträgt jede Rate <strong>ein Viertel</strong> der Steuerforderung der letzten Steuerperiode, fällig bis zum <strong>150., 240. und 330. Tag</strong> nach Beginn der Steuerperiode; bei den Saldosteuersätzen ist die <strong>Hälfte</strong> bis zum 240. Tag zu zahlen. Die Raten werden an die Jahresabrechnung angerechnet. Sind Raten zu hoch oder zu tief, kann eine Anpassung beantragt werden; wer Raten verspätet oder unvollständig zahlt, schuldet ohne Mahnung Verzugszins (Art. 87 Abs. 1bis MWSTG).</p>
<div class="cta-mid"><strong>Rechenbeispiel (fiktive Zahlen):</strong> Effektive Abrechnung, Steuerforderung der letzten Periode CHF 12'000. Die ESTV stellt drei Raten zu je CHF 4'000 in Rechnung – fällig am 150., 240. und 330. Tag des laufenden Kalenderjahres, in der Praxis Ende Mai, Ende August und Ende November. Die eigentliche Jahresabrechnung reicht die Unternehmung bis am 28./29. Februar des Folgejahres ein; die Raten werden angerechnet.<br><br><em>Illustratives Beispiel ohne Gewähr; massgebend ist die je Periode festgelegte Steuerforderung.</em></div>"""),
 ("Fristverlängerung: kostenlos – aber nur im ESTV-Portal",
  """<p>Für die Einreichung der Abrechnung gewährt die ESTV kostenlose Fristverlängerungen – ausschliesslich über den Service «MWST abrechnen» im ESTV-Portal. Gesuche per Brief oder E-Mail können nicht bewilligt werden, weil das elektronische Verfahren vorgeschrieben ist (Art. 123 MWSTV als Teil der Einreichung). Unternehmen, die mit der Software «MWST-Abrechnung pro» arbeiten, verlängern die Frist direkt in der Übersicht.</p>
<p>Wichtig ist der Unterschied zwischen den beiden Pflichten: Die Verlängerung betrifft nur das <strong>Einreichen</strong> der Abrechnung, nicht die <strong>Zahlung</strong>. Wer nach dem ordentlichen 60-Tage-Termin zahlt, schuldet Verzugszins (Art. 87 Abs. 1 MWSTG) – auch mit bewilligter Erstreckung. Praxislösung: geschätzten Steuerbetrag vor dem Termin als Akonto überweisen und die Abrechnung danach einreichen.</p>"""),
 ("Fehler korrigieren: die 180-Tage-Frist",
  """<p>Stellt ein Unternehmen im Rahmen des Jahresabschlusses Fehler in seinen Steuerabrechnungen fest, muss es diese spätestens in der Abrechnung über jene Periode korrigieren, in die der <strong>180. Tag nach Ende des Geschäftsjahres</strong> fällt (Art. 72 Abs. 1 MWSTG). Erkannte Mängel in älteren Steuerperioden sind nachträglich zu korrigieren, solange die Steuerforderungen nicht rechtskräftig oder verjährt sind (Abs. 2).</p>
<p>Wer korrigiert, bevor die ESTV beanstandet, vermeidet Sanktionen: Strafbestimmungen greifen bei Hinterziehung erst, wenn die Korrekturfrist von Art. 72 Abs. 1 abgelaufen ist und der Fehler nicht berichtigt wurde.</p>"""),
 ("Kurz gesagt",
  """<ul>
<li>Innert 60 Tagen nach Periodenende: Abrechnung einreichen <em>und</em> Steuer zahlen – unaufgefordert (Art. 71 Abs. 1 und Art. 86 Abs. 1 MWSTG).</li>
<li>Regel ist die Quartalsabrechnung; Saldosteuersatz halbjährlich; auf Antrag jährlich (bis CHF 5'005'000 Umsatz) oder monatlich bei Vorsteuerüberschuss (Art. 35 MWSTG).</li>
<li>Jährliche Abrechnung mit Raten am 150., 240. und 330. Tag bzw. Hälfte am 240. Tag (Art. 86a MWSTG).</li>
<li>Fristverlängerung kostenlos, nur im ESTV-Portal – und nur fürs Einreichen, nicht fürs Zahlen (Art. 123 MWSTV, Art. 87 MWSTG).</li>
<li>Fehler aus dem Jahresabschluss: Korrektur bis zum 180. Tag nach Geschäftsjahresende (Art. 72 Abs. 1 MWSTG).</li>
<li>Allgemeine Information, keine individuelle Beratung – geprüfte Fachpersonen finden Sie <a href="partner-pruefung.html">hier</a>, Offerte auf <a href="kontakt.html">kontakt.html</a>.</li>
</ul>"""),
]
de_title = "MWST-Abrechnung: Fristen pro Periode"
de_meta = "Fristen der MWST-Abrechnung: 60-Tage-Regel, Quartals-, Semester- und Jahresabrechnung, Raten, Verlängerung im ESTV-Portal, 180-Tage-Korrektur."

# ---------------- EN ----------------
en_sections = [
 ("The 60-day rule: filing and payment run in parallel",
  """<p>The key VAT deadline: <strong>within 60 days after the end of each settlement period</strong> the return must be filed unprompted with the Federal Tax Administration (FTA) — and the tax due for that period must be paid within the same window (Art. 71 para. 1 and Art. 86 para. 1 VAT Act).</p>
<p>Late <strong>payment</strong> triggers default interest without any reminder (Art. 87 para. 1). The other way round favours the taxpayer: if the FTA does not refund a credit surplus within 60 days of receiving the return, it owes compensation interest from day 61 (Art. 88 para. 4).</p>
<p><em>Practical tip:</em> these dates fall on the same days every year (table below). Put the settlement periods in your calendar as recurring events.</p>"""),
 ("Which settlement period applies to your company",
  """<p>The law provides a tiered system (Art. 35 VAT Act):</p>
<ul>
<li><strong>Quarterly settlement</strong> — the default for effective (itemised) accounting.</li>
<li><strong>Semi-annual settlement</strong> — for the flat-rate (balance) tax method.</li>
<li><strong>Annual settlement</strong> — on request, if taxable turnover is at most CHF 5,005,000 a year.</li>
<li><strong>Monthly settlement</strong> — on request for regular input-tax surpluses; refunds then arrive faster.</li>
</ul>
<p>Two switching rules are often missed: changes only take effect at the start of a tax period, and an annual settlement must be kept for at least one full period. Anyone leaving the annual method for monthly, quarterly or semi-annual returns can come back earliest after three tax periods. Companies that neglect filing or payment duties can have the annual permission refused or revoked (Art. 35a).</p>""" + CTA["en"]),
 ("All deadlines at a glance (FTA table)",
  """<p>The FTA publishes the filing dates per period — all derived from the 60-day rule:</p>
<table><thead><tr><th>Return</th><th>Settlement period</th><th>Filed and paid by</th></tr></thead><tbody>
<tr><td>Q1</td><td>1 January – 31 March</td><td>31 May</td></tr>
<tr><td>Q2</td><td>1 April – 30 June</td><td>31 August</td></tr>
<tr><td>Q3</td><td>1 July – 30 September</td><td>30 November</td></tr>
<tr><td>Q4</td><td>1 October – 31 December</td><td>28/29 February</td></tr>
<tr><td>1st half-year</td><td>1 January – 30 June</td><td>31 August</td></tr>
<tr><td>2nd half-year</td><td>1 July – 31 December</td><td>28/29 February</td></tr>
<tr><td>Annual return</td><td>1 January – 31 December</td><td>28/29 February</td></tr>
<tr><td>Monthly example</td><td>1 – 31 January</td><td>31 March</td></tr>
</tbody></table>
<p>When the tax liability ends, the 60-day clock starts at that moment (Art. 71 para. 2) — the final return does not automatically land at calendar year-end.</p>"""),
 ("Annual settlement: instalments replace quarterly returns",
  """<p>Annual filers do not wait a year to pay: the FTA levies provisional tax in instalments (Art. 86a). Under effective accounting and the flat-rate tax, each instalment is <strong>one quarter</strong> of the previous period's tax claim, due on the <strong>150th, 240th and 330th day</strong> of the current tax period; under the balance tax method, <strong>one half</strong> is due on day 240. Instalments are credited against the annual return. They can be adjusted on request; late or incomplete instalments accrue default interest without reminder (Art. 87 para. 1bis).</p>
<div class="cta-mid"><strong>Worked example (fictitious figures):</strong> effective settlement, previous period's tax claim CHF 12,000. The FTA bills three instalments of CHF 4,000 — due on day 150, 240 and 330 of the current calendar year, in practice end of May, end of August and end of November. The annual return itself is due by 28/29 February of the following year; instalments are credited.<br><br><em>Illustrative example without guarantee; the assessed tax claim of each period is decisive.</em></div>"""),
 ("Deadline extension: free of charge — but only in the FTA portal",
  """<p>The FTA grants free extensions for filing — exclusively through the «Settle VAT» service in the ePortal. Paper or e-mail requests cannot be approved, because the electronic procedure is mandatory (Art. 123 of the VAT Ordinance). Businesses working with the FTA's «MWST-Abrechnung pro» software extend the deadline directly in the overview.</p>
<p>The distinction matters: an extension covers <strong>filing</strong> only — not <strong>payment</strong>. Money arriving after the ordinary 60-day date accrues default interest (Art. 87 para. 1) even with an approved extension. Pragmatic fix: pay an estimated amount before the due date and file the return afterwards.</p>"""),
 ("Correcting errors: the 180-day rule",
  """<p>Errors found while preparing the annual accounts must be corrected at the latest in the return covering the period into which the <strong>180th day after the close of the business year</strong> falls (Art. 72 para. 1). Mistakes in older tax periods must be corrected retrospectively as long as those claims are neither final nor time-barred (para. 2).</p>
<p>Correcting before the authority objects avoids sanctions: penalty provisions on evasion only bite once the Art. 72 para. 1 correction window has expired uncorrected.</p>"""),
 ("In short",
  """<ul>
<li>60 days after each period: file the return <em>and</em> pay — unprompted (Art. 71 para. 1, Art. 86 para. 1).</li>
<li>Quarterly is the default; balance tax: semi-annual; on request annual (≤ CHF 5,005,000 turnover) or monthly with input-tax surpluses (Art. 35).</li>
<li>Annual settlement runs on instalments at day 150/240/330, or half at day 240 (Art. 86a).</li>
<li>Extensions are free, portal-only — and cover filing, not payment (Art. 123 VAT Ordinance, Art. 87).</li>
<li>Year-end corrections: by the 180th day after the close of the business year (Art. 72 para. 1).</li>
<li>General information, not individual advice — find vetted professionals on <a href="partner-pruefung.html">this page</a> or request a quote at <a href="kontakt.html">kontakt.html</a>.</li>
</ul>"""),
]
en_title = "VAT Settlement: Deadlines per Period"
en_meta = "Swiss VAT deadlines: 60-day rule, quarterly, semi-annual and annual settlement, instalments, portal extension, 180-day correction duty."

# ---------------- FR ----------------
fr_sections = [
 ("La règle des 60 jours : dépôt et paiement en parallèle",
  """<p>L’échéance essentielle de la TVA : <strong>dans les 60 jours qui suivent la fin de chaque période de décompte</strong>, le décompte doit être déposé spontanément auprès de l’Administration fédérale des contributions (AFC) – et l’impôt dû pour cette période doit être payé dans le même délai (art. 71 al. 1 et art. 86 al. 1 LTVA). L’AFC ne rappelle pas avant ; l’obligation naît automatiquement à chaque période.</p>
<p>En cas de paiement tardif, un intérêt moratoire court sans mise en demeure (art. 87 al. 1). En sens inverse : si l’AFC ne rembourse pas un excédent en faveur de l’assujetti dans les 60 jours de la réception du décompte, un intérêt compensatoire est dû dès le 61<sup>e</sup> jour (art. 88 al. 4).</p>
<p><em>Conseil pratique :</em> ces dates reviennent chaque année (voir tableau). Inscrivez les périodes de décompte comme rendez-vous récurrents dans votre agenda.</p>"""),
 ("Quelle période de décompte pour votre entreprise",
  """<p>La loi prévoit un système échelonné (art. 35 LTVA) :</p>
<ul>
<li><strong>Décompte trimestriel</strong> – la règle pour la méthode réelle (analytique).</li>
<li><strong>Décompte semestriel</strong> – pour la méthode du taux de l’impôt sur le solde (Saldosteuersatz).</li>
<li><strong>Décompte annuel</strong> – sur demande, si le chiffre d’affaires imposable ne dépasse pas CHF 5'005'000 par an.</li>
<li><strong>Décompte mensuel</strong> – sur demande en cas d’excédent régulier de l’impôt préalable ; les remboursements viennent plus vite.</li>
</ul>
<p>Deux règles de changement sont souvent oubliées : tout changement prend effet au début d’une période fiscale, et le décompte annuel doit être conservé au moins une période complète. Qui passe de l’annuel au mensuel, trimestriel ou semestriel ne peut revenir à l’annuel qu’après trois périodes. Une entreprise qui néglige ses obligations peut se voir refuser ou retirer l’autorisation annuelle (art. 35a).</p>""" + CTA["fr"]),
 ("Tous les délais en un coup d’œil (tableau AFC)",
  """<p>L’AFC publie les délais de dépôt par période – tous découlent de la règle des 60 jours :</p>
<table><thead><tr><th>Décompte</th><th>Période de décompte</th><th>Déposé et payé jusqu’au</th></tr></thead><tbody>
<tr><td>1er trimestre</td><td>1er janvier – 31 mars</td><td>31 mai</td></tr>
<tr><td>2e trimestre</td><td>1er avril – 30 juin</td><td>31 août</td></tr>
<tr><td>3e trimestre</td><td>1er juillet – 30 septembre</td><td>30 novembre</td></tr>
<tr><td>4e trimestre</td><td>1er octobre – 31 décembre</td><td>28/29 février</td></tr>
<tr><td>1er semestre</td><td>1er janvier – 30 juin</td><td>31 août</td></tr>
<tr><td>2e semestre</td><td>1er juillet – 31 décembre</td><td>28/29 février</td></tr>
<tr><td>Décompte annuel</td><td>1er janvier – 31 décembre</td><td>28/29 février</td></tr>
<tr><td>Exemple mensuel</td><td>1er – 31 janvier</td><td>31 mars</td></tr>
</tbody></table>
<p>Si l’assujettissement prend fin, le délai de 60 jours court dès ce moment (art. 71 al. 2) – le décompte final ne coïncide donc pas forcément avec la fin de l’année civile.</p>"""),
 ("Décompte annuel : des acomptes remplacent les trimestres",
  """<p>Qui décompte annuellement ne paie pas seulement en fin d’année : l’AFC perçoit un impôt provisoire par acomptes (art. 86a). En méthode réelle et en taux forfaitaires, chaque acompte représente <strong>un quart</strong> de la créance fiscale de la dernière période, échéant aux <strong>150<sup>e</sup>, 240<sup>e</sup> et 330<sup>e</sup> jours</strong> de la période en cours ; en méthode du solde, <strong>la moitié</strong> échoit au 240<sup>e</sup> jour. Les acomptes sont imputés sur le décompte annuel. Ils peuvent être adaptés sur demande ; un acompte tardif ou incomplet entraîne un intérêt moratoire sans mise en demeure (art. 87 al. 1bis).</p>
<div class="cta-mid"><strong>Exemple (chiffres fictifs) :</strong> décompte réel, créance fiscale de la période précédente CHF 12'000. L’AFC facture trois acomptes de CHF 4'000 – échéant aux 150<sup>e</sup>, 240<sup>e</sup> et 330<sup>e</sup> jours de l’année civile, en pratique fin mai, fin août et fin novembre. Le décompte annuel proprement dit doit être déposé jusqu’au 28/29 février de l’année suivante ; les acomptes sont imputés.<br><br><em>Exemple illustratif sans garantie ; seule la créance fixée pour chaque période est déterminante.</em></div>"""),
 ("Prolongation du délai : gratuite – mais uniquement dans le portail AFC",
  """<p>L’AFC accorde des prolongations gratuites pour le dépôt – exclusivement via le service « Décompte TVA » du portail électronique. Les demandes par lettre ou e-mail ne peuvent pas être approuvées, la voie électronique étant prescrite (art. 123 OTVA, comme partie intégrante du dépôt). Les entreprises qui utilisent le logiciel « Décompte TVA pro » prolongent le délai directement depuis l’aperçu.</p>
<p>La distinction est capitale : la prolongation ne couvre que le <strong>dépôt</strong>, jamais le <strong>paiement</strong>. Un versement qui arrive après l’échéance ordinaire de 60 jours génère des intérêts moratoires (art. 87 al. 1) – même avec une prolongation accordée. Solution pratique : payer une provision avant l’échéance et déposer le décompte ensuite.</p>"""),
 ("Corriger les erreurs : la règle des 180 jours",
  """<p>Les erreurs constatées lors de l’établissement des comptes annuels doivent être corrigées au plus tard dans le décompte de la période englobant le <strong>180<sup>e</sup> jour après la fin de l’exercice</strong> (art. 72 al. 1). Les défauts touchant des périodes plus anciennes doivent être corrigés a posteriori tant que les créances ne sont ni entrées en force ni prescrites (al. 2).</p>
<p>Corriger avant toute réclamation de l’autorité évite des sanctions : les normes pénales relatives à la soustraction ne s’appliquent qu’une fois le délai de correction de l’art. 72 al. 1 écoulé sans correction.</p>"""),
 ("En bref",
  """<ul>
<li>60 jours après chaque période : déposer le décompte <em>et</em> payer – spontanément (art. 71 al. 1, art. 86 al. 1).</li>
<li>Trimestriel par défaut ; méthode du solde : semestriel ; sur demande annuel (≤ CHF 5'005'000 de CA) ou mensuel en cas d’excédent d’impôt préalable (art. 35).</li>
<li>Décompte annuel avec acomptes aux 150<sup>e</sup>/240<sup>e</sup>/330<sup>e</sup> jours, respectivement moitié au 240<sup>e</sup> jour (art. 86a).</li>
<li>Prolongation gratuite, uniquement via le portail – pour le dépôt, pas pour le paiement (art. 123 OTVA, art. 87).</li>
<li>Corrections de clôture : jusqu’au 180<sup>e</sup> jour après la fin de l’exercice (art. 72 al. 1).</li>
<li>Information générale, pas un conseil individuel – trouvez des spécialistes vérifiés sur <a href="partner-pruefung.html">cette page</a> ou demandez une offre sur <a href="kontakt.html">kontakt.html</a>.</li>
</ul>"""),
]
fr_title = "TVA : délais par période de décompte"
fr_meta = "Délais TVA Suisse : règle des 60 jours, décompte trimestriel, semestriel ou annuel, acomptes, prolongation en ligne, correction à 180 jours."

# ---------------- IT ----------------
it_sections = [
 ("La regola dei 60 giorni: recapito e pagamento in parallelo",
  """<p>La scadenza principale dell’IVA: <strong>entro 60 giorni dalla fine di ogni periodo di conteggio</strong> il conteggio va recapitato d’ufficio all’Amministrazione federale delle contribuzioni (AFC) e l’imposta dovuta per quel periodo va versata nella medesima finestra (art. 71 cpv. 1 e art. 86 cpv. 1 LIVA). L’AFC non sollecita prima: l’obbligo scatta automaticamente a ogni periodo.</p>
<p>In caso di pagamento tardivo decorre un interesse moratorio senza intimazione (art. 87 cpv. 1). Vale anche a favore del contribuente: se l’AFC non rimborsa un’eccedenza entro 60 giorni dal recapito del conteggio, dal 61° giorno è dovuto un interesse compensatorio (art. 88 cpv. 4).</p>
<p><em>Suggerimento pratico:</em> queste date si ripetono ogni anno (vedi tabella). Segnate i periodi di conteggio nel calendario come appuntamenti ricorrenti.</p>"""),
 ("Quale periodo di conteggio si applica alla vostra azienda",
  """<p>La legge prevede un sistema scaglionato (art. 35 LIVA):</p>
<ul>
<li><strong>Conteggio trimestrale</strong> – regola per il metodo effettivo (analitico).</li>
<li><strong>Conteggio semestrale</strong> – per il metodo dell’aliquota saldo.</li>
<li><strong>Conteggio annuale</strong> – su richiesta, con un fatturato imponibile fino a CHF 5'005'000 l’anno.</li>
<li><strong>Conteggio mensile</strong> – su richiesta in caso di eccedenza ricorrente dell’imposta precedente (Vorsteuer); i rimborsi arrivano prima.</li>
</ul>
<p>Due regole spesso trascurate: i passaggi avvengono solo all’inizio di un periodo fiscale e il conteggio annuale va mantenuto almeno per un periodo completo. Chi passa dall’annuale al mensile, trimestrale o semestrale può tornare all’annuale al più presto dopo tre periodi. Chi trascura gli obblighi di conteggio e pagamento rischia il rifiuto o la revoca dell’autorizzazione annuale (art. 35a).</p>""" + CTA["it"]),
 ("Tutte le scadenze in un colpo d’occhio (tabella AFC)",
  """<p>L’AFC pubblica i termini di recapito per periodo – tutti derivano dalla regola dei 60 giorni:</p>
<table><thead><tr><th>Conteggio</th><th>Periodo di conteggio</th><th>Recapitato e pagato fino al</th></tr></thead><tbody>
<tr><td>1° trimestre</td><td>1° gennaio – 31 marzo</td><td>31 maggio</td></tr>
<tr><td>2° trimestre</td><td>1° aprile – 30 giugno</td><td>31 agosto</td></tr>
<tr><td>3° trimestre</td><td>1° luglio – 30 settembre</td><td>30 novembre</td></tr>
<tr><td>4° trimestre</td><td>1° ottobre – 31 dicembre</td><td>28/29 febbraio</td></tr>
<tr><td>1° semestre</td><td>1° gennaio – 30 giugno</td><td>31 agosto</td></tr>
<tr><td>2° semestre</td><td>1° luglio – 31 dicembre</td><td>28/29 febbraio</td></tr>
<tr><td>Conteggio annuale</td><td>1° gennaio – 31 dicembre</td><td>28/29 febbraio</td></tr>
<tr><td>Esempio mensile</td><td>1° – 31 gennaio</td><td>31 marzo</td></tr>
</tbody></table>
<p>Se l’obbligo fiscale termina, i 60 giorni decorrono da quel momento (art. 71 cpv. 2) – il conteggio finale non cade dunque automaticamente a fine anno civile.</p>"""),
 ("Conteggio annuale: gli acconti sostituiscono i trimestri",
  """<p>Chi conta annualmente non paga solo a fine anno: l’AFC riscuote un’imposta provvisoria tramite acconti (art. 86a). Con il metodo effettivo e le aliquote forfettarie ogni acconto ammonta a <strong>un quarto</strong> dell’esigibile dell’ultimo periodo, in scadenza al <strong>150°, 240° e 330° giorno</strong> del periodo in corso; con l’aliquota saldo è dovuta <strong>metà</strong> entro il 240° giorno. Gli acconti sono accreditati sul conteggio annuale e possono essere adattati su richiesta; in caso di acconti tardivi o incompleti decorre l’interesse moratorio senza intimazione (art. 87 cpv. 1bis).</p>
<div class="cta-mid"><strong>Esempio di calcolo (numeri fittizi):</strong> conteggio effettivo, esigibile dell’ultimo periodo CHF 12'000. L’AFC fattura tre acconti da CHF 4'000 – in scadenza al 150°, 240° e 330° giorno dell’anno civile, in pratica a fine maggio, fine agosto e fine novembre. Il conteggio annuale vero e proprio va recapitato entro il 28/29 febbraio dell’anno successivo; gli acconti sono accreditati.<br><br><em>Esemplo illustrativo senza garanzia; determinante è l’esigibile fissato per ciascun periodo.</em></div>"""),
 ("Proroga del termine: gratuita – ma solo nel portale AFC",
  """<p>L’AFC concede proroghe gratuite per il recapito – esclusivamente tramite il servizio «Conteggio IVA» del portale elettronico. Domande cartacee o per e-mail non possono essere approvate, poiché la via elettronica è prescritta (art. 123 OIVA, quale parte del recapito). Le aziende che lavorano con il software «Conteggio IVA pro» prolungano il termine direttamente dalla schermata di riepilogo.</p>
<p>La distinzione è decisiva: la proroga riguarda solo il <strong>recapito</strong>, non il <strong>pagamento</strong>. Versamenti che arrivano dopo il termine ordinario dei 60 giorni generano interessi moratori (art. 87 cpv. 1) – anche con proroga accordata. Soluzione pratica: versare un acconto stimato prima della scadenza e recapitare il conteggio in seguito.</p>"""),
 ("Correggere gli errori: la regola dei 180 giorni",
  """<p>Gli errori rilevati in sede di chiusura contabile vanno corretti al più tardi nel conteggio del periodo che comprende il <strong>180° giorno dopo la fine dell’esercizio</strong> (art. 72 cpv. 1). Difetti concernenti periodi più vecchi vanno rettificati successivamente finché i crediti d’imposta non sono passati in giudicato o prescritti (cpv. 2).</p>
<p>Chi corregge prima di qualsiasi contestazione dell’autorità evita sanzioni: le norme penali sulla sottrazione si applicano solo se il termine di correzione di cui all’art. 72 cpv. 1 è scaduto senza correzione.</p>"""),
 ("In breve",
  """<ul>
<li>Entro 60 giorni dalla fine di ogni periodo: recapitare il conteggio <em>e</em> pagare – senza sollecito (art. 71 cpv. 1, art. 86 cpv. 1).</li>
<li>Trimestrale di regola; aliquota saldo: semestrale; su richiesta annuale (fatturato ≤ CHF 5'005'000) o mensile in caso di eccedenza ricorrente (art. 35).</li>
<li>Conteggio annuale con acconti al 150°/240°/330° giorno, rispettivamente metà al 240° (art. 86a).</li>
<li>Proroga gratuita, solo nel portale – riguarda il recapito, non il pagamento (art. 123 OIVA, art. 87).</li>
<li>Correzioni di chiusura: entro il 180° giorno dalla fine dell’esercizio (art. 72 cpv. 1).</li>
<li>Informazione generale, non consulenza individuale – consulenti verificati su <a href="partner-pruefung.html">questa pagina</a>, offerta su <a href="kontakt.html">kontakt.html</a>.</li>
</ul>"""),
]
it_title = "IVA: scadenze per periodo di conto"
it_meta = "Scadenze IVA Svizzera: regola dei 60 giorni, conto trimestrale, semestrale o annuale, acconti, proroga online, correzione entro 180 giorni."

# ---------------- wiring: related_map, ratgeber ticks, audience_map, card ----------------
MAP = os.path.join(BASE, "scripts", "related_map.json")
rel = json.load(open(MAP, encoding="utf-8"))
rel[SLUG + ".html"] = RELATED3
# symmetric backlink from mwst-100k: swap weakest link
b = rel.get("mwst-100k-pflicht-schweiz.html", [])
if SLUG + ".html" not in b and b:
    b = [SLUG + ".html"] + [x for x in b if x != "eu-zoll-3-euro-kleinsendungen.html"]
    rel["mwst-100k-pflicht-schweiz.html"] = b
json.dump(rel, open(MAP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("related_map updated")

TICK = {
 "de": "MWST-Abrechnung: Fristen pro Quartal, Semester und Jahr",
 "en": "VAT settlement: quarterly, half-year and annual deadlines",
 "fr": "TVA : délais trimestriels, semestriels et annuels",
 "it": "IVA: scadenze trimestrali, semestrali e annuali",
}
for lang, path in [("de", os.path.join(BASE, "ratgeber.html"))] + [(l, os.path.join(BASE, l, "ratgeber.html")) for l in ("en","fr","it")]:
    s = open(path, encoding="utf-8").read()
    entry = f'<li><a href="{SLUG}.html">{TICK[lang]}</a></li>'
    if SLUG not in s:
        s = s.replace('<ul class="tick">', '<ul class="tick">\n      ' + entry, 1)
        open(path, "w", encoding="utf-8").write(s)
        print("ratgeber tick inserted:", path)

AUD = os.path.join(BASE, "data", "audience_map.json")
a = json.load(open(AUD, encoding="utf-8"))
a[SLUG] = ["firma"]
json.dump(a, open(AUD, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("audience_map:", SLUG, "-> firma")

JL = os.path.join(BASE, "data", "content-research.jsonl")
card = {
 "date": "2026-11-03", "type": "article", "status": "published", "slug": SLUG,
 "title": de_title, "meta": de_meta, "demand": "high",
 "why": "Pino-Keyword-Recherche 2026-11-03 (todo 4701): 'mwst abrechnung frist' + 'mehrwertsteuer jahresabrechnung frist' — beide ohne eigenen Artikel; ESTV-Fristentabelle = Kern-Compliance-Query der MWST-Cluster. Alle Zahlen claim-check-verifiziert (results-mwst-fristen.json 11/11 supports jev-latest); evergreen ohne Datums-Trick.",
 "facts": ["60-Tage-Regel Einreichung (Art. 71 Abs.1 MWSTG) und Entrichtung (Art. 86 Abs.1)",
  "Perioden: quartalsweise Regel, Saldo halbjährlich, jährlich <=5'005'000, monatlich bei Vorsteuerueberschuss (Art. 35)",
  "ESTV-Fristen: Q1 31.5./Q2 31.8./Q3 30.11./Q4 28./29.2./Semester/Jahr 28./29.2.",
  "Raten 150./240./330. Tag bzw. Haelfte am 240. (Art. 86a)",
  "Verlaengerung kostenlos nur elektronisch (Art. 123 MWSTV), nur Einreichen nicht Zahlung; Verzugszins Art. 87",
  "Korrektur 180. Tag nach Geschaeftsjahresende (Art. 72 Abs.1)"],
 "langs": ["de", "en", "fr", "it"],
 "published_at": "2026-11-03",
}
with open(JL, "a", encoding="utf-8") as f:
    f.write(json.dumps(card, ensure_ascii=False) + "\n")
print("card appended (status:published)")

# ---------------- build 4 pages ----------------
build("de", SLUG, de_title, de_meta, de_sections, related=RELATED3, sources=sources("de"))
build("en", SLUG, en_title, en_meta, en_sections, related=RELATED3, sources=sources("en"))
build("fr", SLUG, fr_title, fr_meta, fr_sections, related=RELATED3, sources=sources("fr"))
build("it", SLUG, it_title, it_meta, it_sections, related=RELATED3, sources=sources("it"))
print("all four built")
