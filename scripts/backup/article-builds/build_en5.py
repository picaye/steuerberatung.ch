#!/usr/bin/env python3
"""Build the EN version of ahv-mindestbeitrag-selbststaendige via article_template.
Translation of the DE source (figures pre-verified in DE rounds, claim_check.py):
8.1 + 1.4 + 0.5 = 10.0 %; sliding scale from 5.371 % (from CHF 10'100) to full rate
at CHF 60'500; minimum contribution CHF 530; pensions 1'260-2'520/month;
married cap 3'780/month; 13th pension (8.333 %) first paid with December 2026 pension.
Decimal style mirrors existing EN pages (decimal point, not comma)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
from article_template import build


def P(s):
    return f'<p>{s}</p>'

def UL(items):
    return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def OL(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


TITLE = "AHV 2026: minimum contribution CHF 530 and the contribution scale for self-employed persons"
META = ("AHV/IV/EO for the self-employed in 2026: 10.0 % total (AHV 8.1 %, DI 1.4 %, EO 0.5 %), "
        "sliding scale below CHF 60'500, minimum contribution CHF 530. Plus minimum/maximum "
        "pensions and the 13th monthly pension from December 2026.")

sections = [
    ("What self-employed persons pay",
     P("Self-employed people pay the contributions to the AHV (Old-Age and Survivors Insurance), "
       "the DI (Disability Insurance) and the EO income replacement scheme "
       "<strong>entirely themselves</strong> – there is no employer covering half. "
       "The 2026 rate: AHV 8.1 % + DI 1.4 % + EO 0.5 % = <strong>10.0 % in total</strong> "
       "of the net income from your self-employed activity. For context: employees and "
       "employers together share 10.6 %, 5.3 % each.")),
    ("The sliding scale: lower income, lower rate",
     P("For annual income <strong>below CHF 60'500</strong> a lower contribution rate applies – "
       "the \u201csliding scale\u201d (information sheet AHV 2.02). It starts at "
       "<strong>5.371 percent</strong> for income from CHF 10'100 and rises in steps to the "
       "full 10.0 percent from CHF 60'500. Example: with income of CHF 40'500 you pay 6.728 % "
       "\u2248 CHF 2'725 instead of the full CHF 4'050. What counts is the net income that your "
       "compensation fund establishes by assessment decision.")),
    ("Minimum contribution of CHF 530",
     P("If you earn less than CHF 10'100 a year, you pay the <strong>minimum contribution of "
       "CHF 530 per year</strong> (which corresponds to an annual salary of CHF 5'000). "
       "Non-working persons also pay at least CHF 530 and at most CHF 26'500. If you have "
       "already paid the minimum contribution on a salary, you can request that your "
       "self-employment contributions be charged only at the lowest scale rate (5.371 %).")
     + P("Side business: if you carry out the self-employed activity only on a side basis and "
         "the annual income from it is at most CHF 2'500, contributions are charged only on "
         "your explicit request (information sheet 2.02).")),
    ("AHV pensions in 2026",
     P("The full pension (with a complete contribution period) ranges in 2026 between "
       "<strong>CHF 1'260 and CHF 2'520 per month</strong> – that is <strong>CHF 15'120 to "
       "CHF 30'240 per year</strong> (BSV). Married couples receive two individual pensions, "
       "capped together at 150 percent of the maximum pension: at most <strong>CHF 3'780 per "
       "month</strong> (CHF 45'360 per year). The amount depends on your contribution period "
       "and your average income from gainful activity.")),
    ("The 13th AHV pension is coming – first paid in December 2026",
     P("The voters approved the 13th old-age pension. It will be paid out <strong>for the "
       "first time together with the December 2026 pension</strong> as a supplement: one "
       "twelfth (8.333 percent) of all monthly pensions received from January to December "
       "2026. Anyone drawing an old-age pension in December 2026 receives the supplement "
       "automatically from the AHV compensation fund – no application is required.")),
    ("Common mistakes",
     UL([
         "<strong>Confusing the contribution base:</strong> what counts is the net profit of "
         "the self-employed activity as assessed, not a \u201csalary\u201d.",
         "<strong>5 % default interest:</strong> if you pay the annual bill more than 30 days "
         "after the invoice date, it gets expensive.",
         "<strong>Minimum contribution paid twice</strong> despite being covered on your "
         "salary – correctable with proof.",
         "<strong>Forgetting the family compensation fund:</strong> depending on the canton, "
         "a contribution to family allowances is added on top of the 10 %."])),
    ("In short",
     OL([
         "Self-employed: 10.0 % AHV/DI/EO (8.1 + 1.4 + 0.5), full rate from CHF 60'500.",
         "Below that: sliding scale from 5.371 % (from CHF 10'100); below CHF 10'100: "
         "minimum contribution CHF 530.",
         "Pensions 2026: CHF 1'260\u20132'520 per month (15'120\u201330'240 per year), "
         "married-couple cap CHF 3'780 per month.",
         "13th AHV pension: first supplement with the December 2026 pension, paid "
         "automatically."])
     + P("Want to know how to optimise your contributions and what contribution gaps cost? "
         "Via the <a href=\"kontakt.html\">contact page</a> we will match you with a vetted "
         "partner – the first quote is transparent, before any engagement.")),
]

build('en', 'ahv-mindestbeitrag-selbststaendige', TITLE, META, sections)
