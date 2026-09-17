#!/usr/bin/env python3
"""Build EN version of the withholding tax article via scripts/article_template.py."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
from article_template import build

TITLE = "Withholding tax 35 %: Reclaiming your dividends and interest"
META = ("Withholding tax in Switzerland: 35 % on dividends and interest (Art. 13 VStG). "
        "How to reclaim it via your tax return – 3-year deadline (Art. 32 VStG), no Form 110 confusion.")

SECTIONS = [
    ("What withholding tax is",
     '<p>Withholding tax is a federal tax on investment income: '
     '<strong>35 %</strong> is deducted from dividends, interest and gambling winnings '
     '(Art. 13 para. 1 lit. a of the Withholding Tax Act, VStG). Life annuities and pensions '
     'are subject to 15 %, other insurance benefits to 8 %.</p>'
     '<p>The deduction is not made by the state but by the paying entity: your bank or the '
     'corporation withholds the tax when the payment falls due and remits it to the Federal Tax '
     'Administration (FTA). Its purpose is to make tax evasion on investment income harder – '
     'which is why the rate deliberately exceeds the ordinary tax burden.</p>'),
    ("The tax is not a loss – it has been paid in advance",
     '<p>For individuals with unlimited tax liability in Switzerland, withholding tax is not a '
     'final tax but a securing tax: you can reclaim it provided you declare the income correctly. '
     'Anyone who fails to claim it is giving money away – on a portfolio with CHF 2' + "'" + '000 '
     'in dividends and interest, that alone is CHF 700 per year.</p>'),
    ("The simple route: the tax return",
     '<p>If you file a tax return, submitting it effectively counts as the refund claim in '
     'practice: the responsible authority is the canton in which you were domiciled at the end '
     'of the year the payment fell due (Art. 30 VStG). The securities schedule of the tax return '
     'serves as the claim – as a rule, the cantons refund the tax up to the amount of your '
     'cantonal and municipal tax liability (Art. 31 VStG).</p>'
     '<p>Important for portfolio holders: enter all dividends and interest in full in the '
     'securities schedule – including small amounts. If an item is missing, the refund is short '
     'by exactly that amount.</p>'),
    ("Without a tax return: Form 25",
     '<p>If you do not file a tax return (for example because your residential canton does not '
     'require one), you request the refund using <strong>Form 25</strong> via the FTA portal. '
     'Careful, a common mix-up: <strong>Form 110 is not for you</strong> – it is how the paying '
     'company declares its own settlement (within 30 days of the general meeting). As a private '
     'individual, you reclaim nothing with it.</p>'),
    ("Deadline: three years after the year of payment",
     '<p>The claim expires if you do not assert it <strong>within three years after the end of '
     'the calendar year</strong> in which the payment fell due (Art. 32 para. 1 VStG). Example: '
     'dividend on 15 May 2023 → deadline on 31 December 2026. A missed deadline is lost '
     'permanently, even with good reasons.</p>'),
    ("Common misconceptions at a glance",
     '<ul class="tick">'
     '<li><strong>“Refund within 30 days”</strong> – wrong. The 30-day deadline concerns the '
     'paying company’s declaration (Form 110), not your claim.</li>'
     '<li><strong>“The tax is gone if I do nothing”</strong> – it is gone if you do nothing for '
     'three years. Otherwise you get it back.</li>'
     '<li><strong>“Switzerland refunds foreign withholding tax”</strong> – no; the applicable '
     'double taxation treaty governs that, and Swiss withholding tax is independent of it.</li>'
     '</ul>'),
    ("In short",
     '<ol>'
     '<li>35 % on dividends and interest, 15 % on life annuities and pensions, 8 % on other '
     'insurance benefits (Art. 13 VStG).</li>'
     '<li>With a tax return, full declaration counts as the refund claim with your residential '
     'canton (Art. 30 VStG).</li>'
     '<li>Without a tax return: Form 25 via the FTA portal.</li>'
     '<li>Deadline: 3 years after the end of the year of payment (Art. 32 para. 1 VStG) – '
     'not 30 days.</li>'
     '</ol>'
     '<p>Not sure whether your securities schedule is complete? Via the '
     '<a href="kontakt.html">contact page</a> we put you in touch with a vetted partner in your '
     'canton – the first quote transparently shows what the review costs.</p>'),
]

build("en", "verrechnungssteuer-schweiz-35-prozent", TITLE, META, SECTIONS)
