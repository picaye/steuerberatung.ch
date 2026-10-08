#!/usr/bin/env python3
"""krankenkassenpramien-steuerabzug — daily 4-language publish 2026-10-08.

Facts verified 2026-10-08 against:
- ESTV "Abzüge, Ansätze und Tarife DBST": Pauschalabzug Versicherungen/Sparzinsen
  1'800/2'700 (Übrige), 3'700/5'550 (Verheiratete), 700/Kind — Jahre 2025–2027.
- ESTV Kreisschreiben Nr. 11a (26.5.2026): Krankheitskosten DB = 5 % des nach
  Art. 26–33 verminderten steuerbaren Einkommens; behinderungsbedingte Kosten
  ohne Selbstbehalt.
- Kanton St. Gallen Steuerbuch: kantonal 2 % Selbstbehalt (Beispiel Kantonsvariante).
- BAG Medienmitteilung 29.9.2026: mittlere Prämie 2027 CHF 412/Monat, +5,0 %;
  Erwachsene CHF 487.60 (+4,9 %).
Kantonale Maximalbeträge (Vergleichsportale) wurden NICHT verifiziert und werden
nicht publiziert.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "krankenkassenpramien-steuerabzug"
RELATED = ["praemienverbilligung-2027-anmelden.html",
           "steuer-checkliste-2026.html",
           "steuern-sparen-tipps.html"]

DOC = {}

DOC["de"] = (
    "Krankenkassenprämien und Steuern: Was Sie 2026 wirklich abziehen können",
    "Krankenkassenprämien sind nicht einzeln abziehbar: Pauschalabzug Bund CHF 1'800/3'700 (ohne Säulen 2 und 3a bis CHF 2'700/5'550), CHF 700 pro Kind – plus Krankheitskosten ab 5 % Selbstbehalt. Zur Steuererklärung 2026.",
    [
    ("Die Prämie ist Privatsache – der Gesetzgeber entschädigt pauschal",
     """<p>Die Krankenversicherungsprämie gehört zu den grössten Haushaltsposten der Schweiz: Die mittlere Monatsprämie steigt 2027 auf CHF 412, Erwachsene zahlen im Schnitt CHF 487.60 (+4,9 %) — so das BAG am 29. September 2026. Viele Versicherte erwarten deshalb, die Prämie von der Steuer abziehen zu können. Tut man aber nicht direkt: Prämien der obligatorischen Krankenpflegeversicherung gelten steuerlich als <strong>private Lebenshaltungskosten</strong>.</p>
<p>Als Ausgleich sieht das Bundesgesetz über die direkte Bundessteuer in Art. 33 Abs. 1 Bst. g bzw. Abs. 1bis DBG einen <strong>Pauschalabzug für Versicherungsprämien und Sparzinsen</strong> vor — mit kantonal eigenen, teils deutlich höheren Ansätzen. Der Abzug gilt für die effektiv bezahlten Privatprämien (Krankenkasse, Lebens-, Hausrat- und Haftpflichtversicherungen) zusammen mit den qualifizierten Sparzinsen — jedoch nur bis zum Höchstbetrag.</p>
<p><strong>Praxistipp:</strong> Es handelt sich um einen Höchstbetrag, nicht um einen Pauschalfranken, den jeder automatisch bekommt. Liegen Ihre effektiven Prämien unter dem Limit, wird nur der tiefere Betrag abgezogen — es lohnt sich, alle privaten Policen im Haushalt auszumessen.</p>"""),
    ("Die Beträge beim Bund: von CHF 1'800 bis CHF 5'550",
     """<p>Für die direkte Bundessteuer gelten (Stand Steuerjahre 2025–2027, Quelle: ESTV «Abzüge, Ansätze und Tarife»):</p>
<ul><li><strong>Einzelpersonen mit Beiträgen an Säule 2 und/oder 3a:</strong> max. CHF 1'800.</li>
<li><strong>Einzelpersonen ohne (oder mit unvollständig genützten) Beiträgen an Säulen 2 und 3a:</strong> max. CHF 2'700 — der ungenutzte Vorsorgeplatz wird bis zu CHF 900 zum Prämienabzug «nachgerückt».</li>
<li><strong>Verheiratete, die tatsächlich zusammenleben:</strong> max. CHF 3'700, resp. CHF 5'550 bei ungenützten Säulen 2/3a (Nachrücken bis CHF 1'850).</li>
<li><strong>Pro Kind und pro unterstützter Person:</strong> je zusätzlich CHF 700.</li></ul>
<p>Getrennt lebende Ehegatten gelten als «übrige Steuerpflichtige» (CHF 1'800/2'700). Das höhere «Nachrücken» betrifft typischerweise Selbstständige ohne Pensionskasse oder Personen, die die Säule 3a nicht ausschöpfen können.</p>
<p><strong>Praxistipp:</strong> Wer den vollen Säule-3a-Abzug macht, hat die grösste Vorsorgelücke bereits geschlossen — beim Prämienpauschale bleibt dann in der Regel nur der Basisrahmen von CHF 1'800 bzw. CHF 3'700.</p>"""),
    ("Kantone und Gemeinden: teils deutlich andere Ansätze",
     """<p>Für Kantons- und Gemeindesteuern legen die 26 Kantone <strong>eigene Maximalbeträge</strong> fest. Sie liegen teils über, teils unter den Bundeswerten und kennen zusätzliche Abstufungen — etwa höhere Ansätze für Kinder oder eigene Regeln für getrennt lebende Ehegatten. Vergleichen Sie deshalb nie den Bundesrahmen mit dem kantonalen Formular: Was auf Bundesebene durchs Limit gedeckelt ist, kann im Kanton noch Luft haben — und umgekehrt.</p>
<p>Auch <strong>Zusatzversicherungen</strong> (VVG) sind eidgenössisch nicht abziehbar; einzelne Kantone lassen unter Bedingungen immerhin Abzüge für Krankenkosten-Zusatzversicherungen zu. Ob Ihr Kanton die Prämien der «assurance de base» ganz, teilweise oder mit eigenem Pauschalbetrag berücksichtigt, steht in den Wegleitungen Ihres kantonalen Steueramtes.</p>
<p><strong>Praxistipp:</strong> Schlagen Sie die kantonalen Ansätze in den Instruktionen Ihres Wohnkantons zur Steuererklärung 2026 nach oder fragen Sie die kantonale Steuerverwaltung — wir vermitteln Ihnen gerne einen geprüften Partner in Ihrem Kanton.</p>"""),
    ("Franchise, Selbstbehalt, Zahnarzt: Krankheitskosten jenseits der Belastungsgrenze",
     """<p>Der zweite Weg führt über die <strong>effektiv selbst bezahlten Gesundheitskosten</strong>: Anteile von Franchise und Selbstbehalt, Zahnarztbehandlungen (medizinisch notwendig), Brillen und Kontaktlinsen, Hörgeräte, Physiotherapie, Spital- und Kuraufenthalte, Medikamente, Fahrkosten zu Behandlungen. Bei der direkten Bundessteuer sind sie abzugsfähig, soweit sie <strong>5 % des nach Abzügen verbleibenden steuerbaren Einkommens</strong> übersteigen (Art. 33 Abs. 1 Bst. h DBG; ESTV-Kreisschreiben Nr. 11a, 2026). Die Kantone kennen eigene Belastungsgrenzen — von rund 2 % (z. B. Kanton St. Gallen) bis zu deutlich höheren Quoten.</p>
<p><strong>Nicht abziehbar</strong> sind Vorsorge- und Wellnessausgaben (Fitnessabonnement, Vitamine, Schönheitsoperationen ohne Krankheitscharakter) sowie alles, was die Versicherung ohnehin übernommen hat. Behindertheitsbedingte Kosten sind beim Bund dagegen <strong>ohne Selbstbehalt voll abziehbar</strong> — eine oft übersehene Reserve für Angehörige mit IV-Rente oder Hilflosenentschädigung.</p>
<p><strong>Praxistipp:</strong> Rechnungen und Zahlungsbelege sammeln — gerade grössere Zahnarztrechnungen oder Spitaleinsätze bewegen sich schnell im vier- bis fünfstelligen Bereich. Bei gemeinsam veranlagten Ehepaaren zählt die Belastungsgrenze auf dem gemeinsamen Einkommen; Kosten der unterhaltenen Personen kommen dazu.</p>"""),
    ("Rechenbeispiel: Wann sich der Abzug lohnt",
     """<p>Beispiel auf Bundesebene, einzeln besteuert, steuerbares Einkommen nach Abzügen CHF 90'000: Effektive Privatprämien plus Sparzinsen CHF 2'400 → abziehbar max. CHF 1'800. Selbst getragene Krankheitskosten (Franchise, Selbstbehalt, Brille, Zahnersatz) CHF 12'000 → abzüglich Belastungsgrenze von rund 5 % (CHF 4'500) bleiben CHF 7'500 abzugsfähig. Total senken CHF 9'300 das steuerbare Einkommen — bei einem Grenztarif um 25–30 % sind das grob <strong>CHF 2'300–2'800 weniger Steuern</strong>.</p>
<p>Beim Kanton verschiebt sich das Bild: Andere Limits, andere Belastungsgrenzen, teils eigene Pauschalen. Wer hohe Gesundheitskosten und keine (oder nur teilweise genutzte) Säule-3a-Beiträge hat, holt in der Summe am meisten heraus.</p>
<p><strong>Praxistipp:</strong> Das Krankenkosten-Formular vollständig ausfüllen — der Abzug verfällt, wenn er nicht geltend gemacht wird. Korrekturen sind nur kurzfristig möglich: Einsprache innert 30 Tagen nach der Veranlagung.</p>"""),
    ("Kurz gesagt",
     """<ul><li>Krankenkassenprämien sind nicht einzeln abziehbar; stattdessen Pauschalabzug «Versicherungsprämien und Sparzinsen»: Bund max. CHF 1'800 (Einzelperson) / CHF 3'700 (Ehepaar), ohne Säulen 2 und 3a bis CHF 2'700 / CHF 5'550, plus CHF 700 pro Kind und unterstützte Person.</li>
<li>Die Limits sind Höchstbeträge: abziehbar sind die effektiv bezahlten Privatprämien und Sparzinsen bis zum Anatz.</li>
<li>Kantone und Gemeinden haben eigene Ansätze — teils deutlich höher, teils tiefer als der Bund.</li>
<li>Eigene Krankheitskosten (Franchise, Selbstbehalt, Zahnarzt, Brille) sind ab Belastungsgrenze abzugsfähig: Bund 5 %, Kantonsquote variiert; behinderungsbedingte Kosten beim Bund voll.</li>
<li>Prämienlast 2027: mittlere Prämie CHF 412/Monat (+5,0 %, BAG). Wer sie nicht tragen kann, prüft die <a href="praemienverbilligung-2027-anmelden.html">Prämienverbilligung 2027</a> — die ist unabhängig von der Steuererklärung.</li>
<li>Allgemeine Information, keine individuelle Steuerberatung; kantonale Praxis prüfen.</li></ul>""")])

DOC["en"] = (
    "Health insurance premiums and taxes: what you can actually deduct",
    "Swiss basic-insurance premiums are not individually deductible. Instead: a federal lump-sum deduction for premiums and savings interest (CHF 1,800/3,700, up to CHF 2,700/5,550 without pillar 2/3a contributions, CHF 700 per child), plus out-of-pocket medical costs above the 5% threshold.",
    [
    ("Premiums are private spending — the law compensates with a capped lump sum",
     """<p>Health insurance is one of the largest items in a Swiss household budget: the median monthly premium rises to CHF 412 in 2027, with adults paying CHF 487.60 on average (+4.9%) — per the Federal Office of Public Health on 29 September 2026. Many insured people therefore assume the premium is tax-deductible. It is not — directly. Premiums of the compulsory basic insurance (KVG/LAMal) count as <strong>private living expenses</strong>.</p>
<p>As compensation, the federal direct tax act (Art. 33 para. 1 lit. g and para. 1bis FITA) grants a <strong>lump-sum deduction for insurance premiums and savings interest</strong>, with separate cantonal caps. It covers premiums you actually paid on private policies (basic health, life, household and liability insurance) plus qualifying savings interest — but only up to the maximum amount.</p>
<p><strong>Practical tip:</strong> this is a ceiling, not a flat rate everyone receives automatically. If your effective premiums are below the cap, only the lower amount counts — so gather every private insurance policy in your household before filing.</p>"""),
    ("The federal amounts: CHF 1,800 to CHF 5,550",
     """<p>For federal direct tax the caps are (tax years 2025–2027, source: FSA «Abzüge, Ansätze und Tarife»):</p>
<ul><li><strong>Single persons paying into pillar 2 and/or 3a:</strong> max. CHF 1,800.</li>
<li><strong>Single persons with no (or partly unused) pillar 2/3a contributions:</strong> max. CHF 2,700 — the unused contribution room is «promoted» to the premium deduction, up to CHF 900.</li>
<li><strong>Married couples living together:</strong> max. CHF 3,700, resp. CHF 5,550 when pillars 2/3a are unused (promotion up to CHF 1,850).</li>
<li><strong>Per child and per dependent supported:</strong> CHF 700 each.</li></ul>
<p>Spouses living apart are assessed as «other taxpayers» (CHF 1,800/2,700). The higher promotion typically concerns self-employed persons without a pension fund or taxpayers who cannot use pillar 3a fully.</p>
<p><strong>Practical tip:</strong> if you make full pillar 3a contributions, the largest pension deduction is already used — what remains for the premium lump sum is usually just the base frame of CHF 1,800 resp. CHF 3,700.</p>"""),
    ("Cantons and municipalities: often very different amounts",
     """<p>For cantonal and municipal taxes, the 26 cantons set <strong>their own maximum amounts</strong>. Some sit above, some below the federal figures, with additional gradations — higher child allowances or separate rules for spouses living apart. Never compare the federal cap with the cantonal form without checking: what is limited at federal level may still have room at cantonal level — and vice versa.</p>
<p><strong>Supplementary insurance</strong> (private policies under the VVG) is not deductible federally; a few cantons at least allow partial deductions for supplementary health-cost policies. Whether your canton deducts basic-insurance premiums in full, partly or via its own flat rate is set out in your cantonal tax administration's instructions.</p>
<p><strong>Practical tip:</strong> look up the cantonal amounts in the instructions for your 2026 tax return or ask the cantonal tax office — we are happy to connect you with a vetted partner in your canton.</p>"""),
    ("Franchise, deductible, dentist: medical costs above the threshold",
     """<p>The second route is your <strong>out-of-pocket health costs</strong>: franchise and deductible shares, (medically necessary) dental treatment, glasses and contact lenses, hearing aids, physiotherapy, hospital and spa stays, medication, travel to treatment. For federal direct tax they are deductible insofar as they exceed <strong>5% of the taxable income remaining after deductions</strong> (Art. 33 para. 1 lit. h FITA; FSA Circular No. 11a, 2026). Cantons apply their own thresholds — from about 2% (e.g. canton of St. Gallen) up to considerably higher rates.</p>
<p><strong>Not deductible:</strong> prevention and wellness spending (gym subscriptions, vitamins, cosmetic surgery without illness character) and everything the insurer covered anyway. Disability-related costs, by contrast, are <strong>fully deductible without any threshold</strong> at federal level — an often overlooked reserve for families with an IV pension or constant-attendance allowance.</p>
<p><strong>Practical tip:</strong> collect invoices and payment receipts — large dental or hospital bills easily run into four or five figures, and they only count with proof. For jointly assessed spouses the threshold is computed on the joint income; costs of dependents are added.</p>"""),
    ("Worked example: when the deduction pays off",
     """<p>Federal-level example, single assessment, taxable income after deductions CHF 90,000: effective private premiums plus savings interest CHF 2,400 → deductible max. CHF 1,800. Out-of-pocket medical costs (franchise, deductible, glasses, dental work) CHF 12,000 → minus the 5% threshold (CHF 4,500), CHF 7,500 remain deductible. In total CHF 9,300 lowers the taxable income — at a marginal rate of roughly 25–30% that is about <strong>CHF 2,300–2,800 less tax</strong>.</p>
<p>At cantonal level the picture shifts: different caps, different thresholds, sometimes separate flat rates. Households with high health costs and no (or partly unused) pillar 3a contributions extract the most.</p>
<p><strong>Practical tip:</strong> fill in the medical-cost form completely — the deduction lapses if it is not claimed. Corrections are only possible briefly: an objection must be filed within 30 days of the assessment.</p>"""),
    ("Key points",
     """<ul><li>Health-insurance premiums are not individually deductible; instead a lump-sum deduction for «insurance premiums and savings interest»: federal max. CHF 1,800 (single) / CHF 3,700 (married), up to CHF 2,700 / CHF 5,550 without pillar 2 and 3a contributions, plus CHF 700 per child and supported person.</li>
<li>The caps are maxima: what you actually paid in private premiums and savings interest counts up to the limit.</li>
<li>Cantons and municipalities use their own amounts — often clearly higher or lower than the federal figures.</li>
<li>Your own medical costs (franchise, deductible, dentist, glasses) are deductible above the threshold: 5% federally, cantonal rates vary; disability-related costs fully at federal level.</li>
<li>Premium burden 2027: median premium CHF 412/month (+5.0%, FOP). If you cannot afford it, check <a href="praemienverbilligung-2027-anmelden.html">premium subsidies 2027</a> — they are independent of the tax return.</li>
<li>General information, not individual tax advice; verify cantonal practice.</li></ul>""")])

DOC["fr"] = (
    "Primes d'assurance-maladie et impôts: ce que vous pouvez réellement déduire",
    "Les primes de l'assurance de base ne sont pas déductibles séparément : forfait fédéral pour primes et intérêts d'épargne (CHF 1'800/3'700, jusqu'à CHF 2'700/5'550 sans cotisations 2e pilier/3a, CHF 700 par enfant), plus les frais de maladie au-delà de la quotité de 5 %.",
    [
    ("Les primes relèvent du budget privé – la loi prévoit un forfait plafonné",
     """<p>La prime maladie est l'un des plus gros postes du budget des ménages suisses : la prime mensuelle moyenne atteindra CHF 412 en 2027, et CHF 487.60 pour les adultes (+4,9 %) — selon l'Office fédéral de la santé publique du 29 septembre 2026. Beaucoup d'assurés s'attendent donc à déduire la prime de leurs impôts. Ce n'est pas le cas directement : les primes de l'assurance-maladie obligatoire (LAMal) sont considérées comme des <strong>frais privés de la vie</strong>.</p>
<p>En compensation, la loi sur l'impôt fédéral direct prévoit à l'art. 33 al. 1 let. g et al. 1bis LIFD une <strong>déduction forfaitaire pour primes d'assurance et intérêts d'épargne</strong> — avec des plafonds cantonaux propres, parfois nettement plus élevés. Sont visées les primes effectivement versées pour les assurances privées (maladie, vie, ménage, responsabilité civile) ainsi que les intérêts d'épargne qualifiés, dans la limite du plafond.</p>
<p><strong>Conseil pratique :</strong> il s'agit d'un maximum, pas d'un montant forfaitaire accordé automatiquement à chacun. Si vos primes effectives restent sous le plafond, seule la somme plus basse est déduite — recensez toutes les polices privées du ménage avant de remplir la déclaration.</p>"""),
    ("Les montants fédéraux : de CHF 1'800 à CHF 5'550",
     """<p>Pour l'impôt fédéral direct, les plafonds en vigueur (années fiscales 2025–2027, source : AFC « Déductions, montants et tarifs ») sont les suivants :</p>
<ul><li><strong>Personnes seules versant des cotisations 2e pilier et/ou 3a :</strong> max. CHF 1'800.</li>
<li><strong>Personnes seules sans cotisations (ou partiellement non utilisées) au 2e pilier et au pilier 3a :</strong> max. CHF 2'700 — la marge de cotisation non utilisée est « reportée » sur la déduction pour primes, jusqu'à CHF 900.</li>
<li><strong>Époux vivant effectivement en ménage commun :</strong> max. CHF 3'700, respectivement CHF 5'550 en cas de non-utilisation des piliers 2/3a (report jusqu'à CHF 1'850).</li>
<li><strong>Par enfant et par personne assistée :</strong> CHF 700 chacun.</li></ul>
<p>Les époux séparés de facto sont imposés comme « autres contribuables » (CHF 1'800/2'700). Le report plus élevé concerne typiquement les indépendants sans caisse de pension ou les contribuables qui ne peuvent pas utiliser pleinement le pilier 3a.</p>
<p><strong>Conseil pratique :</strong> qui verse le rachat maximal dans le pilier 3a a déjà épuisé la plus grande déduction prévoyance — il ne reste généralement que le cadre de base de CHF 1'800, resp. CHF 3'700, pour le forfait primes.</p>"""),
    ("Cantons et communes : des plafonds très différents",
     """<p>Pour les impôts cantonal et communal, les 26 cantons fixent <strong>leurs propres montants maximaux</strong>. Ils se situent parfois au-dessus, parfois en dessous des valeurs fédérales, avec des graduations additionnelles — allocations plus élevées par enfant ou règles propres aux époux séparés. Ne comparez jamais le plafond fédéral avec le formulaire cantonal sans vérifier : ce qui est plafonné au niveau fédéral peut encore offrir une marge au niveau cantonal — et inversement.</p>
<p>Les <strong>assurances complémentaires</strong> (LCA) ne sont pas déductibles au niveau fédéral ; certains cantons admettent néanmoins une déduction partielle pour les complémentaires couvrant les frais de guérison. Pour savoir si votre canton déduit les primes de l'assurance de base intégralement, partiellement ou via un forfait propre, consultez le guide de votre administration fiscale cantonale.</p>
<p><strong>Conseil pratique :</strong> cherchez les montants cantonaux dans les instructions de votre déclaration 2026 ou demandez à l'administration fiscale cantonale — nous vous mettons volontiers en relation avec un partenaire agréé dans votre canton.</p>"""),
    ("Franchise, participations, dentiste : les frais de maladie au-delà de la quotité",
     """<p>La seconde voie passe par les <strong>frais de santé effectivement pris en charge</strong> : parts de franchise et de participation aux coûts, traitements dentaires (médicalement nécessaires), lunettes et lentilles, appareils auditifs, physiothérapie, séjours hospitaliers et thermaux, médicaments, frais de transport vers le traitement. À l'impôt fédéral direct, ils sont déductibles pour la part qui dépasse <strong>5 % du revenu imposable après déductions</strong> (art. 33 al. 1 let. h LIFD ; circulaire AFC n° 11a, 2026). Les cantons appliquent leurs propres quotités — d'environ 2 % (par ex. canton de Saint-Gall) à des taux nettement plus élevés.</p>
<p><strong>Non déductibles :</strong> les dépenses de prévention et de bien-être (abonnement fitness, vitamines, chirurgie esthétique sans caractère morbide) et tout ce que l'assurance a déjà pris en charge. Les coûts liés à un handicap sont en revanche <strong>intégralement déductibles sans quotité</strong> au niveau fédéral — une réserve souvent ignorée des familles touchant une rente AI ou une allocation pour impotent.</p>
<p><strong>Conseil pratique :</strong> conservez factures et justificatifs de paiement — une grande réfection dentaire ou un séjour hospitalier atteint vite des montants à quatre ou cinq chiffres, et rien n'est déduit sans preuve. Pour les époux imposés conjointement, la quotité se calcule sur le revenu commun ; les frais des personnes assistées s'y ajoutent.</p>"""),
    ("Exemple chiffré : quand la déduction rapporte",
     """<p>Exemple au niveau fédéral, imposition individuelle, revenu imposable après déductions CHF 90'000 : primes privées effectives plus intérêts d'épargne CHF 2'400 → déductibles à concurrence de CHF 1'800. Frais de maladie assumés (franchise, participations, lunettes, prothèse dentaire) CHF 12'000 → déduction faite de la quotité de 5 % (CHF 4'500), CHF 7'500 restent déductibles. Total : CHF 9'300 de revenu imposable en moins — avec un taux marginal d'environ 25–30 %, cela représente environ <strong>CHF 2'300–2'800 d'impôts en moins</strong>.</p>
<p>Au niveau cantonal, le tableau change : autres plafonds, autres quotités, parfois des forfaits propres. Les ménages avec des frais de santé élevés et sans cotisations (ou partiellement non utilisées) au pilier 3a tirent le meilleur parti de ces déductions.</p>
<p><strong>Conseil pratique :</strong> remplissez intégralement le formulaire des frais de maladie — la déduction tombe si elle n'est pas demandée. Les corrections n'interviennent que brièvement : opposition dans les 30 jours suivant la taxation.</p>"""),
    ("En bref",
     """<ul><li>Les primes maladie ne sont pas déductibles séparément ; le forfait « primes d'assurance et intérêts d'épargne » s'y substitue : plafond fédéral CHF 1'800 (personne seule) / CHF 3'700 (époux), jusqu'à CHF 2'700 / CHF 5'550 sans cotisations aux piliers 2 et 3a, plus CHF 700 par enfant et par personne assistée.</li>
<li>Les plafonds sont des maximums : seules les primes privées et les intérêts d'épargne effectivement versés sont déductibles, dans la limite du montant maximal.</li>
<li>Cantons et communes appliquent leurs propres montants — souvent nettement plus élevés ou plus bas que la Confédération.</li>
<li>Les frais de maladie à votre charge (franchise, participations, dentiste, lunettes) sont déductibles au-delà du seuil : 5 % à l'échelle fédérale, quotités cantonales variables ; les frais liés à un handicap sont intégralement déductibles au fédéral.</li>
<li>Charge des primes 2027 : prime moyenne CHF 412/mois (+5,0 %, OFSP). Si vous ne pouvez pas l'assumer, vérifiez la <a href="praemienverbilligung-2027-anmelden.html">réduction des primes 2027</a> — elle est indépendante de la déclaration d'impôts.</li>
<li>Informations générales, pas de conseil fiscal individuel ; vérifiez la pratique de votre canton.</li></ul>""")])

DOC["it"] = (
    "Premi dell'assicurazione malattie e imposte: cosa potete davvero dedurre",
    "I premi dell'assicurazione di base non sono deducibili singolarmente: forfait federale per premi e interessi di risparmio (CHF 1'800/3'700, fino a CHF 2'700/5'550 senza contributi 2° pilastro/3a, CHF 700 per figlio), più le spese di malattia oltre la soglia del 5 %.",
    [
    ("I premi sono spese private – la legge prevede un forfait con tetto massimo",
     """<p>Il premio dell'assicurazione malattie è una delle voci più pesanti del budget delle economie domestiche svizzere: nel 2027 il premio mensile medio salirà a CHF 412, per gli adulti a CHF 487.60 (+4,9 %) — secondo l'Ufficio federale della sanità pubblica del 29 settembre 2026. Molti assicurati si aspettano dunque di poter dedurre il premio dalle imposte. Non è così, direttamente: i premi dell'assicurazione obbligatoria delle cure medico-sanitarie (LAMal) sono considerati <strong>spese private di sostentamento</strong>.</p>
<p>In via di compensazione, la legge sull'imposta federale diretta prevede all'art. 33 cpv. 1 lett. g e cpv. 1bis LIFD una <strong>deduzione forfettaria per premi assicurativi e interessi di risparmio</strong> — con tetti cantonali propri, in parte sensibilmente più elevati. Sono coperti i premi effettivamente versati per assicurazioni private (malattie, vita, economie domestiche, responsabilità civile) nonché gli interessi di risparmio qualificati, entro il massimale.</p>
<p><strong>Suggerimento pratico:</strong> si tratta di un tetto massimo, non di un forfait accordato automaticamente a tutti. Se i Suoi premi effettivi restano sotto il massimale, è deducibile soltanto l'importo inferiore — faccia l'inventario di tutte le polizze private del nucleo prima di compilare la dichiarazione.</p>"""),
    ("Gli importi federali: da CHF 1'800 a CHF 5'550",
     """<p>Per l'imposta federale diretta vigono i massimali seguenti (anni d'imposta 2025–2027, fonte: AFC «Deduzioni, importi e tariffe»):</p>
<ul><li><strong>Persone single che versano contributi al 2° pilastro e/o al pilastro 3a:</strong> max. CHF 1'800.</li>
<li><strong>Persone single senza contributi (o con contributi solo in parte sfruttati) al 2° pilastro e al pilastro 3a:</strong> max. CHF 2'700 — lo spazio di contribuzione non utilizzato viene «traslato» sulla deduzione per premi, fino a CHF 900.</li>
<li><strong>Sposati che vivono in comunione domestica:</strong> max. CHF 3'700, rispettivamente CHF 5'550 in caso di pilastri 2/3a non sfruttati (traslato fino a CHF 1'850).</li>
<li><strong>Per ogni figlio e per ogni persona assistita:</strong> CHF 700 ciascuno.</li></ul>
<p>Gli sposati separati di fatto sono tassati come «altri contribuenti» (CHF 1'800/2'700). Il traslato più elevato riguarda di norma gli indipendenti senza cassa pensione o i contribuenti che non possono sfruttare plenamente il pilastro 3a.</p>
<p><strong>Suggerimento pratico:</strong> chi versa il massimo nel pilastro 3a ha già esaurito la più grossa deduzione previdenziale — per il forfait premi resta di regola solo il quadro base di CHF 1'800, rispettivamente CHF 3'700.</p>"""),
    ("Cantoni e Comuni: tetti molto differenti",
     """<p>Per le imposte cantonale e comunale i 26 Cantoni fissano <strong>propri importi massimi</strong>. Si situano talvolta sopra, talvolta sotto i valori federali e prevedono graduazioni aggiuntive — assegni più elevati per figlio o norme proprie per gli sposati separati. Non confront mai il tetto federale con il formulario cantonale senza verifica: ciò che a livello federale è limitato può ancora offrire margine a livello cantonale — e viceversa.</p>
<p>Anche le <strong>assicurazioni complementari</strong> (LCa) non sono deducibili a livello federale; alcuni Cantoni ammettono perlomeno deduzioni parziali per le complementari che coprono costi di guarigione. Per sapere se il Suo Cantone deduce i premi dell'assicurazione di base integralmente, in parte o tramite un forfait proprio, consulti le istruzioni dell'amministrazione fiscale cantonale.</p>
<p><strong>Suggerimento pratico:</strong> cerchi gli importi cantonali nelle istruzioni per la dichiarazione 2026 o si rivolga all'amministrazione fiscale del Suo Cantone — La mettiamo volentieri in contatto con un partner qualificato nella Sua regione.</p>"""),
    ("Franchigia, partecipazione ai costi, dentista: le spese di malattia oltre la soglia",
     """<p>La seconda via passa per le <strong>spese sanitarie effettivamente a Suo carico</strong>: quote di franchigia e partecipazione ai costi, cure dentarie (medicamente necessarie), occhiali e lenti a contatto, apparecchi acustici, fisioterapia, degenze ospedaliere e termali, medicamenti, spese di trasporto per le cure. Per l'imposta federale diretta sono deducibili nella parte che eccede <strong>il 5 % del reddito imponibile al netto delle deduzioni</strong> (art. 33 cpv. 1 lett. h LIFD; circolare AFC n. 11a, 2026). I Cantoni applicano soglie proprie — da circa il 2 % (per es. Cantone San Gallo) a quote sensibilmente più alte.</p>
<p><strong>Non deducibili:</strong> le spese di prevenzione e benessere (abbonamento fitness, vitamine, chirurgia estetica senza carattere morboso) e tutto ciò che l'assicurazione ha già assunto. I costi causati da un'invalidità sono invece <strong>integralmente deducibili senza soglia</strong> a livello federale — una riserva spesso ignorata dalle famiglie che percepiscono una rendita AI o un'assegno per grandi invalidi.</p>
<p><strong>Suggerimento pratico:</strong> conservi fatture e prove di pagamento — una grande riabilitazione dentaria o una degenza raggiungono rapidamente importi a quattro o cinque cifre, e senza prova nulla è deducibile. Per gli sposati tassati congiuntamente la soglia è calcolata sul reddito comune; i costi delle persone assistite si aggiungono.</p>"""),
    ("Esempio di calcolo: quando la deduzione conviene",
     """<p>Esempio a livello federale, tassazione individuale, reddito imponibile dopo le deduzioni CHF 90'000: premi privati effettivi più interessi di risparmio CHF 2'400 → deducibili al max. CHF 1'800. Spese di malattia a Suo carico (franchigia, partecipazioni, occhiali, protesi dentaria) CHF 12'000 → detraendo la soglia del 5 % (CHF 4'500) restano deducibili CHF 7'500. In totale CHF 9'300 in meno di reddito imponibile — con un'aliquota marginale di circa 25–30 % sono indicativamente <strong>CHF 2'300–2'800 di imposte in meno</strong>.</p>
<p>A livello cantonale il quadro cambia: altri tetti, altre soglie, talvolta forfait propri. I nuclei con elevate spese sanitarie e senza contributi (o solo in parte sfruttati) al pilastro 3a ottengono il massimo.</p>
<p><strong>Suggerimento pratico:</strong> compili integralmente il formulario delle spese di malattia — la deduzione decade se non è richiesta. Le correzioni sono possibili solo per poco tempo: opposizione entro 30 giorni dalla tassazione.</p>"""),
    ("In breve",
     """<ul><li>I premi delle casse malati non sono deducibili singolarmente; vale invece il forfait «premi assicurativi e interessi di risparmio»: tetto federale CHF 1'800 (persona sola) / CHF 3'700 (sposati), fino a CHF 2'700 / CHF 5'550 senza contributi ai pilastri 2 e 3a, più CHF 700 per figlio e persona assistita.</li>
<li>I massimali sono tetti: sono deducibili soltanto i premi privati e gli interessi di risparmio effettivamente versati.</li>
<li>Cantoni e Comuni applicano importi propri — spesso sensibilmente più alti o più bassi della Confederazione.</li>
<li>Le spese di malattia a Suo carico (franchigia, partecipazioni, dentista, occhiali) sono deducibili oltre la soglia: 5 % a livello federale, quote cantonali variabili; i costi legati a un'invalidità sono integralmente deducibili a livello federale.</li>
<li>Carico premi 2027: premio medio CHF 412/mese (+5,0 %, UFSP). Se non può sostenerlo, verifichi la <a href="praemienverbilligung-2027-anmelden.html">riduzione dei premi 2027</a> — è indipendente dalla dichiarazione d'imposte.</li>
<li>Informazioni generali, non una consulenza fiscale individuale; verifichi la prassi del Suo Cantone.</li></ul>""")])

for lang, (title, meta, sections) in DOC.items():
    rel = RELATED if lang == "de" else None
    build(lang, SLUG, title, meta, sections, related=rel)
print("built", SLUG, "in", ", ".join(DOC))
