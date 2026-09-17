#!/usr/bin/env python3
"""Build the EN translation of mwst-100k-pflicht-schweiz via article_template.
Figures/claims mirror the verified DE original (build_articles_de.py A4, claim_check rounds 2-4):
- VAT liability from CHF 100'000 worldwide turnover, Art. 10 para. 2 VATA (0.84/0.87)
- unsolicited registration within 30 days, Art. 66 para. 1 (0.99); rates 8.1 / 2.6 % (0.93/0.98)
- associations/NGO threshold CHF 250'000, Art. 10 para. 2 lit. c; voluntary registration Art. 11/14;
  VAT invoiced without entitlement is owed, Art. 27.
Citation style mirrors en/kryptowaehrungen-steuern-schweiz.html: "Art. X para. Y <law>",
"Federal Tax Administration (FTA)", decimal point for percentages (matches existing EN pages: 35 %, 78.3 %).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import article_template as at


def P(s):
    return f'<p>{s}</p>'

def OL(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


at.build(
    'en',
    'mwst-100k-pflicht-schweiz',
    "VAT from CHF 100'000: When You Become Liable for Value Added Tax",
    "Swiss VAT liability: from CHF 100'000 worldwide turnover (Art. 10 VATA), registration within 30 days via the FTA online form, rates 8.1 % / 2.6 %. Thresholds, deadlines and exemptions for 2026.",
    [
        ("The threshold: CHF 100'000 &ndash; worldwide",
         P("You become liable for value added tax (VAT) once your business generates <strong>CHF 100'000 or more</strong> a year from supplies that are not excluded from tax (Art. 10 para. 2 of the Value Added Tax Act, VATA). Important: what counts is turnover <strong>at home and abroad</strong>, not just your Swiss turnover. Excluded supplies (for example letting residential property, insurance and banking transactions, certain educational services) are not counted.")
         + P("Anyone who stays below the limit over a year is exempt from VAT liability &ndash; with an exception for associations: non-profit, volunteer-run sports and cultural clubs and charitable organisations have an increased limit of <strong>CHF 250'000</strong> (Art. 10 para. 2 lit. c VATA). The relevant period is always one year; anyone who can foresee exceeding the limit in the next twelve months becomes liable to VAT beforehand.")),
        ("Registration: on your own initiative, within 30 days",
         P("As soon as you exceed the limit (or can foresee exceeding it), you must register in writing with the Federal Tax Administration (FTA) <strong>on your own initiative within 30 days</strong> of the start of tax liability (Art. 66 para. 1 VATA). Nobody will write to you first. Registration runs through the <strong>FTA's online questionnaire</strong>; you will be assigned a non-transferable VAT number. Room for confusion: &laquo;Form 25&raquo; concerns refunds of withholding tax &ndash; for VAT, the FTA's online form is the correct route.")
         + P("Conversely: anyone who stays below the limit can voluntarily waive the exemption and register (Art. 11 and 14 VATA) &ndash; thanks to the input tax deduction, this pays off above all when you have high investments. Warning: anyone who shows VAT on an invoice without being entitled to do so still owes the amount (Art. 27 VATA).")),
        ("The rates in 2026",
         P("The rates are: <strong>standard rate 8.1 per cent</strong>, <strong>reduced rate 2.6 per cent</strong> (Art. 25 VATA). The reduced rate applies, among other things, to foodstuffs within the meaning of the Foodstuffs Act (excluding alcoholic beverages), water in pipes, medicines, books and press products. Watch out &ndash; a widespread misconception: <strong>hospitality services are taxed at the standard rate</strong> &ndash; restaurant service and consumption on the premises are not reduced, even though the food itself would be. Anyone calculating &laquo;catering at 2.6 %&raquo; learned it wrong.")),
        ("Settling your account: quarterly, semi-annually or at balance tax rates (Saldosteuers&auml;tze)",
         P("The standard is <strong>quarterly settlement</strong> via the FTA's VAT portal. Small businesses (a low tax amount per year) may settle semi-annually or annually; many SMEs work with the <strong>balance tax rates (Saldosteuersätze)</strong> &ndash; flat industry-specific rates that cut accounting effort, because the input tax does not have to be substantiated individually.")),
        ("Side job, club, platform: when you are a business all the same",
         P("A business is anyone who pursues, on their own account, an activity aimed at generating sustainable income (Art. 10 para. 1bis VATA) &ndash; also alongside a main job, and also with a 20 per cent workload on a platform. Ongoing consulting assignments, shop sales or letting with infrastructure can trigger tax liability before you notice it. Insignificant remuneration and genuinely one-off transactions do not.")),
        ("In short",
         OL([
            "Liability from CHF 100'000 of worldwide turnover from supplies that are not excluded (Art. 10 para. 2 VATA); sports and cultural clubs and charitable institutions: CHF 250'000.",
            "Registration: within 30 days, on your own initiative, FTA online questionnaire &ndash; not Form 25.",
            "2026 rates: standard 8.1 %, reduced 2.6 %; hospitality = standard rate.",
            "Voluntary registration brings the input tax deduction; VAT shown without entitlement is owed (Art. 27)."])
         + P("You have just (or soon will) passed the CHF 100'000 mark and want to start on a clean footing? Via the <a href=\"kontakt.html\">contact page</a> we match you with a vetted partner for your initial VAT registration &ndash; with a transparent quote before any engagement.")),
    ],
)
