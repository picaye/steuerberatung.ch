#!/usr/bin/env python3
"""Build the EN version of the mortgage-deduction article via article_template.

Source: hypothek-steuerabzug-schweiz.html (DE). Terminology and statute-citation
style mirror en/ratgeber.html ("Art. 33 para. 1 lit. a DBG", "private debt
interest ... up to taxable investment income plus CHF 50'000", "imputed rental
value") and en/erbschaftssteuer-schenkungssteuer-schweiz.html (concise Swiss
business English, "you"). Figures kept identical: CHF 50'000, 5 % (debunked),
Formular 14 -> Schedule of Debts (Form 14).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import article_template as at


def P(s):
    return f'<p>{s}</p>'

def UL(items):
    return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def OL(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


TITLE_EN = "Mortgage and taxes: interest, deductions and limits explained"

META_EN = ("Deduct mortgage interest 2026: private debt interest up to taxable "
           "investment income plus CHF 50'000 (Art. 33 para. 1 lit. a DBG). "
           "How to declare it correctly \u2013 and what you CANNOT deduct.")

SECTIONS = [
 ("The principle: imputed rental value vs. deductions",
  P("If you live in your own home, you pay tax on the <strong>imputed rental value</strong> "
    "\u2013 a notional rent that is added to your income. In return, you may deduct the costs "
    "of the property: above all mortgage interest, maintenance, and contributions to "
    "energy-saving and protective measures. The system is meant to put rented and "
    "owner-occupied property on a similar tax footing \u2013 it is not a gift.")),

 ("Mortgage interest: deductible, but capped",
  P("Mortgage interest on owner-occupied residential property is <strong>private debt "
    "interest</strong>. For direct federal tax, private debt interest is deductible \u2013 but "
    "not without limits: only up to <strong>taxable investment income plus a further "
    "CHF 50'000</strong> (Art. 33 para. 1 lit. a DBG). If you have little income from assets "
    "(interest, dividends, rent), the cap applies: not everything the bank charges you during "
    "the year ends up in the tax calculation. The cantons handle private debt interest "
    "differently \u2013 for your own tax return, the respective cantonal law is what counts.")),

 ("Declaring it correctly: Schedule of Debts (Form 14)",
  P("Enter all mortgages and loans in the <strong>Schedule of Debts (Form 14)</strong>: "
    "creditor, outstanding balance at year-end, interest amount. The supporting document is "
    "the <strong>interest statement from your bank</strong> \u2013 without it, the tax office "
    "will not accept the deduction. The debt itself also reduces your taxable assets; your "
    "wealth tax falls.")),

 ("What you CANNOT deduct",
  UL([
    "<strong>Construction loan interest during the building phase:</strong> it is capital "
    "expenditure on the building, not an income deduction \u2013 recoverable later through "
    "depreciation of the construction costs.",
    "<strong>Luxury expenditure:</strong> tax authorities regularly do not accept fitted "
    "items of a luxurious nature (whirlpools, special wellness fittings) as maintenance.",
    "<strong>Invented rules:</strong> a \u201c5 % interest deduction on the loan\u201d does "
    "not exist \u2013 nor do forms \u201cat the AHV\u201d: the AHV is never responsible "
    "for mortgages."])),

 ("Strategy: amortise or repay?",
  P("Higher mortgage rates make amortisation attractive: every repayment stage saves future "
    "interest \u2013 but it also lowers your deduction and increases your net taxable income. "
    "If you are close to the cap on private debt interest, amortising is often the better move "
    "than the (blocked) interest deduction. The imputed-rental-value-versus-deductions "
    "comparison is a matter of canton and individual case \u2013 this is where individual "
    "advice pays off more than almost anywhere else.")),

 ("In short",
  OL([
    "Mortgage interest is deductible \u2013 but private debt interest is capped at investment "
    "income + CHF 50'000 at the federal level (Art. 33 para. 1 lit. a DBG).",
    "Declare it in the Schedule of Debts (Form 14); supporting document = bank interest "
    "statement.",
    "Construction-phase interest is capital expenditure, not an income deduction.",
    "Check cantonal differences \u2013 especially for amortisation and the imputed rental "
    "value."])
  + P("Not sure whether your deductions hit the cap? Through the "
      "<a href=\"kontakt.html\">contact page</a> we will find a vetted partner in your "
      "region \u2013 with a quote before any engagement.")),
]

at.build('en', 'hypothek-steuerabzug-schweiz', TITLE_EN, META_EN, SECTIONS)
print("EN built: hypothek-steuerabzug-schweiz,", len(SECTIONS), "sections")
