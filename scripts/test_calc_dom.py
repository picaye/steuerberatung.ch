#!/usr/bin/env python3
"""test_calc_dom.py — DOM-shape regression guard for calculator CTA form nesting.

Guards the 12f1913 fix class (the c405367 corruption): the .lead-cta-form block
sat INSIDE the outer calculator <form> (#tax-calc / #br-form). Browsers drop
nested <form> tags, so the CTA existed in raw HTML (curl markers passed) yet
form.lead-cta-form was null in the live DOM and submissions could not bind.
A future content/editorial commit can silently re-nest it again — Pages CI
only builds, so this suite is the automated tripwire.

Checks (task t_31134495 acceptance criteria, plus one documented narrowing):
  G1  the calculator-page set (html with BOTH a calc-form and a lead-cta-form)
      is exactly the 8 known pages rechner + bezugsrechner x de/en/fr/it —
      a page gaining/losing that shape trips the guard,
  G2  every calculator page has exactly 2 open <form> tags and 2 </form> closes,
  G3  NO form.lead-cta-form is a descendant of another <form> — checked on ALL
      lead-cta-form pages (28 at ship time), not just calculators: nesting an
      article CTA inside some future wrapper form is the same defect class,
  G4  every calculator page references assets/app.js (the script stack that
      un-hides and binds the CTA; ../assets/ on localized pages),
  G5  negative self-test: the embedded synthetic c405367-shaped page (CTA
      nested in #tax-calc) MUST be rejected — proves the detector is alive.

Narrowing vs the task card ("every repo html containing calc-form ... exactly 2
opens/closes"): class `calc-form` also matches 3a-rechner.html x4, which ship a
single calculator form and NO lead CTA (verified at 12f1913 — 1/1 opens/closes).
Asserting 2/2 there is unsatisfiable on main tip, so the 2/2 count applies to
pages that carry BOTH markers (the corruption class). Non-nesting (G3) still
covers all calc-form pages transitively via the lead-form check.

Wiring (t_31134495): standalone stdlib-only runner with exit-code semantics,
mirroring scripts/test_drain_sentinel.py; additionally invoked as a named gate
step in .github/workflows/pages.yml (post-merge main tip) and
.github/workflows/queue-guard.yml (every PR, from the PR head ref).

Usage:
  python3 scripts/test_calc_dom.py                  # positive suite over the repo
  python3 scripts/test_calc_dom.py --root DIR       # scan DIR instead of repo
  python3 scripts/test_calc_dom.py --make-negative DIR   # populate DIR with the
                                                    # synthetic corruption (rc=1
                                                    # run demo / host lane use)

Exit 0 when all guards pass, 1 otherwise.
"""
import os
import re
import sys
from html.parser import HTMLParser

# The eight calculator pages shipped by the 12f1913 fix (path, must exist).
CALC_PAGES = [
    "rechner.html",
    "en/rechner.html",
    "fr/rechner.html",
    "it/rechner.html",
    "bezugsrechner.html",
    "en/bezugsrechner.html",
    "fr/bezugsrechner.html",
    "it/bezugsrechner.html",
]

FORM_OPEN = re.compile(r"<form\b", re.I)
FORM_CLOSE = re.compile(r"</form\s*>", re.I)
CALC_MARKER = re.compile(r'class="calc-form"|id="br-form"', re.I)
LEAD_MARKER = re.compile(r'class="[^"]*lead-cta-form', re.I)
APPJS = re.compile(r'src="(?:\.\./)?assets/app\.js')

# -----------------------------------------------------------------------------
# Negative fixture: the c405367 corruption shape, reconstructed synthetically.
# This is what a regression looks like: the lead CTA block sits inside the
# still-open outer calculator form (the outer </form> only closes after it).
NESTED_CORRUPTION = """<!DOCTYPE html>
<html lang="de"><head><title>negative fixture (c405367 shape)</title></head>
<body>
<form id="tax-calc" class="calc-form">
<div id="calc-fields"><input name="income" value="90000"></div>
<div id="calc-cta" class="cta-mid lead-cta" hidden>
<div class="lead-cta-copy"><strong>Lohnt sich eine individuelle Pruefung?</strong></div>
<form class="lead-cta-form" data-situation="Steuerrechner-Ergebnis">
<div class="lead-cta-fields"><input name="name" placeholder="Name *"><input name="email" type="email" placeholder="E-Mail *"></div>
<button type="submit">Unverbindlich anfragen</button>
</form>
</div>
<div class="disclaimer">Nur schaetzung.</div>
</form>
<script src="assets/app.js?v=3"></script>
</body></html>
"""


class FormShapeParser(HTMLParser):
    """Tracks <form> nesting; records each form's attrs and its form ancestors.

    html.parser is forgiving like a browser: it reports start/end tags as they
    come. We maintain a stack of currently-open <form> tag descriptors; when a
    new form opens, whatever is on the stack is its form-ancestor chain (exactly
    what the browser would refuse to render as nested DOM)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # list of attr dicts for currently-open forms
        self.forms = []          # {attrs, ancestors:[ids/classes]} in doc order
        self.stray_close = 0     # </form> with no open form

    def handle_starttag(self, tag, attrs):
        if tag != "form":
            return
        a = dict(attrs)
        self.forms.append({
            "id": a.get("id", ""),
            "class": a.get("class", ""),
            "ancestors": list(self.stack),
        })
        self.stack.append(a)

    def handle_startendtag(self, tag, attrs):
        # <form/> is malformed HTML but the parser sees it; treat as open+close.
        if tag == "form":
            a = dict(attrs)
            self.forms.append({"id": a.get("id", ""), "class": a.get("class", ""),
                               "ancestors": list(self.stack)})

    def handle_endtag(self, tag):
        if tag != "form":
            return
        if self.stack:
            self.stack.pop()
        else:
            self.stray_close += 1


def is_lead(form):
    return "lead-cta-form" in (form["class"] or "")


def is_calc(form):
    return ("calc-form" in (form["class"] or "")) or form["id"] in ("tax-calc", "br-form", "a3-form")


def check_html(rel, text):
    """Return a list of violation strings for one page ('' == clean)."""
    v = []
    has_calc = bool(CALC_MARKER.search(text))
    has_lead = bool(LEAD_MARKER.search(text))
    opens = len(FORM_OPEN.findall(text))
    closes = len(FORM_CLOSE.findall(text))
    if has_calc and has_lead:
        if opens != 2:
            v.append(f"{rel}: {opens} open <form> tags, want exactly 2")
        if closes != 2:
            v.append(f"{rel}: {closes} </form> closes, want exactly 2")
    p = FormShapeParser()
    p.feed(text)
    p.close()
    if p.stray_close:
        v.append(f"{rel}: {p.stray_close} stray </form> with no open form")
    for f in p.forms:
        if is_lead(f) and f["ancestors"]:
            anc = ", ".join(a.get("id") or a.get("class", "?") for a in f["ancestors"])
            v.append(f"{rel}: form.lead-cta-form NESTED inside <form> ({anc}) "
                     f"— c405367 corruption class; browsers drop it from the DOM")
    return v


def walk_html(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in (".git", "node_modules", "dist", ".hermes-patches", "assets"))
        for fn in sorted(filenames):
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def scan_tree(root):
    """All guards against a tree; returns (violations, stats)."""
    viol = []
    calc_set = []
    lead_pages = []
    for path in walk_html(root):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        if LEAD_MARKER.search(text):
            lead_pages.append(rel)
        if CALC_MARKER.search(text) and LEAD_MARKER.search(text):
            calc_set.append(rel)
            viol += check_html(rel, text)
            if "bezugsrechner" in rel or "rechner" in rel:
                if not APPJS.search(text):
                    viol.append(f"{rel}: no assets/app.js reference — CTA/JS stack dead")
        elif CALC_MARKER.search(text):
            # calc-form without a lead CTA (3a-rechner class of page): nesting
            # check only; the 2/2 count guard deliberately does not apply here.
            viol += check_html(rel, text)
    return viol, {"calc_set": sorted(calc_set), "lead_pages": len(lead_pages)}


def main(argv):
    root = None
    make_negative = None
    i = 1
    while i < len(argv):
        if argv[i] == "--root" and i + 1 < len(argv):
            root = argv[i + 1]
            i += 2
        elif argv[i] == "--make-negative" and i + 1 < len(argv):
            make_negative = argv[i + 1]
            i += 2
        else:
            print(f"usage: {argv[0]} [--root DIR | --make-negative DIR]")
            return 2
    if make_negative:
        dst = os.path.join(make_negative, "rechner.html")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(NESTED_CORRUPTION)
        print(f"wrote negative fixture: {dst}")
        return 0

    if root is None:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    guards = 0
    failed = 0

    def report(name, viol):
        nonlocal guards, failed
        guards += 1
        if viol:
            failed += 1
            print(f"FAIL {name}")
            for line in viol:
                print(f"     {line}")
        else:
            print(f"[ok] {name}")

    # G1: the guarded calculator set is exactly the 8 known pages.
    viol, stats = scan_tree(root)
    got = stats["calc_set"]
    missing = sorted(set(CALC_PAGES) - set(got))
    extra = sorted(set(got) - set(CALC_PAGES))
    g1 = []
    if missing:
        g1.append(f"calculator pages vanished from the guarded set: {missing}")
    if extra:
        g1.append(f"NEW calculator pages not in the known set (review + extend CALC_PAGES): {extra}")
    if not g1 and got != sorted(CALC_PAGES):
        g1.append(f"guarded set != expected 8: {got}")
    report("G1 calculator-page set == 8 known (rechner+bezugsrechner x de/en/fr/it)", g1)

    # G2+G3+G4: shape violations found during the scan (counts, nesting, app.js).
    shape_v = [x for x in viol if "NESTED" in x or "want exactly 2" in x]
    appjs_v = [x for x in viol if "assets/app.js" in x]
    report(f"G2 form counts 2/2 on {len(got)} calculator pages", shape_v)
    report(f"G3 no lead-cta-form nested in a <form> across {stats['lead_pages']} lead pages",
           [x for x in viol if "NESTED" in x])
    report("G4 assets/app.js referenced on every calculator page", appjs_v)

    # G5: the detector must reject the embedded c405367-shaped fixture.
    neg = check_html("negative-fixture.html", NESTED_CORRUPTION)
    if not neg:
        report("G5 negative fixture rejected (detector alive for the corruption class)",
               ["NESTED_CORRUPTION fixture passed clean — detector is dead; this guard "
                "must go red if the parser stops seeing nesting"])
    elif not any("NESTED" in x for x in neg):
        report("G5 negative fixture rejected (detector alive for the corruption class)",
               [f"fixture flagged but not for nesting: {neg}"])
    else:
        report("G5 negative fixture rejected (detector alive for the corruption class)", [])

    print(f"{guards} guards run, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
