#!/usr/bin/env python3
"""Build the English edition of the cross-border commuter article
(grenzgaenger-de-fr-it-steuern) via scripts/article_template.build."""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
from article_template import build

TITLE = "Cross-Border Commuters DE/FR/IT: 4.5 % Source Tax and Filing the Right Forms"

META = ("Switzerland-Germany cross-border commuters: 4.5 % source tax "
        "(Art. 15a DTA CH-DE), form Gre-1, 60 non-return days, German deadline "
        "31 July. Different rules apply for FR/IT \u2013 the 2026 overview.")

SECTIONS = [
    ("When you count as a cross-border commuter for tax purposes",
     '<p>For tax purposes, you are a cross-border commuter only if every condition '
     'is met: residence abroad (DE, FR or IT), employer and place of work in Switzerland, '
     'and <strong>daily return</strong> to your home \u2013 and that return must be '
     'reasonable. In cantonal practice, reasonable means: a driving distance of at most '
     '100 kilometres by car or at most 1.5 hours by public transport.</p>'
     '<p>Note: the cross-border commuter permit (ID G) is something else \u2013 it does '
     'not establish tax cross-border commuter status. Anyone who does not return home '
     'daily is an international weekly resident and is taxed at source under the regular '
     'Swiss tariffs.</p>'),

    ("Germany: 4.5 % source tax \u2013 but only with Gre-1",
     '<p>For genuine German cross-border commuters, Switzerland levies source tax as a '
     'flat rate of <strong>4.5 % of the gross salary</strong> (Art. 15a DTA CH-DE). But '
     'this does not apply automatically: you must give your employer the '
     '<strong>certificate of residence, form Gre-1</strong>, issued by your German tax '
     'office. Without Gre-1, the employer settles accounts under the regular tariff \u2013 '
     'often considerably more.</p>'
     '<p>Gre-1 is valid for one calendar year at a time and must be submitted to the '
     'employer anew every year; after the first year, the tax office usually issues it '
     'automatically. You need a separate form for each employer.</p>'),

    ("The 60-non-return-days limit",
     '<p>If you fail to return home for professional reasons (business trips, on-call '
     'duty, further training) on <strong>more than 60 days</strong> in the calendar year, '
     'you lose the cross-border commuter tariff. Your Swiss income is recalculated under '
     'the regular tariffs and reassessed. The employer must certify the professionally '
     'motivated non-return days using <strong>form Gre-3</strong> \u2013 in the canton of '
     'Zurich, for example, in writing, separately per employer, and filed with the '
     'cantonal tax office no later than <strong>31 March of the following year</strong> '
     '(the deadline varies by canton). Overnight stays for private reasons do not count.</p>'),

    ("Germany: tax return by 31 July",
     '<p>Even if Switzerland has collected 4.5 %: in Germany you are taxed on your '
     'worldwide income and must declare your cross-border commuter income in your income '
     'tax return. The general filing deadline for the 2025 German income tax return ends '
     'on <strong>31 July 2026</strong>; later if you use tax representation (wage tax '
     'assistance association, tax adviser). The Swiss source tax is credited in Germany '
     'so that no double taxation remains.</p>'),

    ("France and Italy: completely different rules",
     '<p><strong>France:</strong> The 1983 cross-border commuter agreement applies only '
     'to places of work in the cantons of BE, BL, BS, JU, NE, SO, VD and VS. Outside '
     'this zone \u2013 for example Geneva \u2013 the regular DTA applies, with the '
     'regular Swiss source-tax tariff and taxation in France with a credit; the details '
     'depend on the canton of work.</p>'
     '<p><strong>Italy:</strong> Under the revised agreement (in force since 17 July 2023, '
     'applicable from 2024), &laquo;new&raquo; cross-border commuters \u2013 those who '
     'started work after 17 July 2023 \u2013 may be taxed in Switzerland at up to 80 % of '
     'the regular source-tax amount; Italy credits this tax. For commuters employed '
     'before the cut-off date, a transitional rule applies until the end of 2033. '
     'Home office is possible for up to 25 % of working hours without jeopardising the '
     'status.</p>'),

    ("The most common mistakes",
     '<ul class="tick">'
     '<li><strong>Is the G permit the same as tax status?</strong> No \u2013 what '
     'decides the matter is daily return and reasonableness.</li>'
     '<li><strong>Forgetting Gre-1</strong> \u2192 regular tariff instead of 4.5 %, a '
     'tedious correction.</li>'
     '<li><strong>Non-return days documented incorrectly</strong> \u2192 Gre-3 not filed '
     'in time, reassessment under the regular tariff.</li>'
     '<li><strong>&laquo;Forms 130/140/150 with the AHV&raquo;?</strong> They do not '
     'exist \u2013 the AHV (social security) is never responsible for source tax; the '
     'certificates run through the employer and the cantonal tax offices.</li>'
     '</ul>'),

    ("In short",
     '<ol>'
     '<li>4.5 % Swiss source tax for genuine German cross-border commuters \u2013 only '
     'with form Gre-1 at the employer.</li>'
     '<li>More than 60 professional non-return days (Gre-3) \u2192 regular tariff, '
     'reassessment.</li>'
     '<li>German side: Anlage N-GRE (German annex N-GRE), filing deadline for the 2025 '
     'return on 31 July 2026.</li>'
     '<li>FR: 1983 agreement only in 8 border cantons; IT: new regime from 2024 (up to '
     '80 % Swiss source tax, credit, transition until 2033).</li>'
     '</ol>'
     '<p>Did you have a home-office year with lots of travel days? That is exactly where '
     'it gets complicated. Via the <a href="kontakt.html">contact page</a> we will match '
     'you with a vetted partner \u2013 with a transparent quote before any mandate.</p>'),
]

if __name__ == "__main__":
    build("en", "grenzgaenger-de-fr-it-steuern", TITLE, META, SECTIONS)
