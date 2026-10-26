#!/usr/bin/env python3
"""Validate the publish queue in data/content-research.jsonl (gh#6).

The "pin without hold_until" defect recurred three times (grenzgaenger
revert b2e19d6, Jan-peak batch backfilled 16bbe2d, Oct-12 research run
backfilled e4d494f). The publish cron's 6-day selection rule only protects
cards that HAVE hold_until, so a pin-less card stays selectable until a
human notices. This script is the validate-time gate: run it after every
research append and in CI; it never modifies anything (read-only).

Rules for queue cards (records carrying both `slug` and `status`; event
lines like type:recommendation/correction are ignored):

1. status:pending with priority `pin-YYYY-MM-DD` must have `hold_until`
   equal to the pin date. Missing or mismatched hold_until -> FAIL.
2. A `pin-` priority that is not a well-formed pin-YYYY-MM-DD date -> FAIL.
3. Past pin dates on pending cards -> FAIL (the pin slot already passed;
   the card needs re-pinning, not another silent sweep).
4. Duplicate slugs among pending cards, or a pending card whose slug was
   already published -> FAIL (double-append / re-pick of published work).

Exit 0 = clean, exit 1 = violations (each printed as `FAIL: <slug> — ...`).
Stdlib only. `--file` and `--today` exist for tests; CI uses the defaults.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys

PIN_RE = re.compile(r"^pin-(\d{4}-\d{2}-\d{2})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_QUEUE = os.path.join(REPO_ROOT, "data", "content-research.jsonl")


def parse_date(s):
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None


def validate(path, today):
    failures = []
    cards = []  # (line_no, record)
    try:
        with open(path, encoding="utf-8") as fh:
            for line_no, raw in enumerate(fh, 1):
                if not raw.strip():
                    continue
                try:
                    rec = json.loads(raw)
                except json.JSONDecodeError as exc:
                    failures.append(
                        f"FAIL: line {line_no} — invalid JSON: {exc}"
                    )
                    continue
                if not isinstance(rec, dict):
                    failures.append(f"FAIL: line {line_no} — not an object")
                    continue
                # Event lines (recommendation, correction, ...) carry no
                # slug/status pair — they are not queue cards.
                if rec.get("slug") and rec.get("status"):
                    cards.append((line_no, rec))
    except OSError as exc:
        failures.append(f"FAIL: cannot read {path}: {exc}")
        return failures, 0

    seen_pending = {}
    published_slugs = set()
    pending_pins = 0

    # Pass 1: every slug already claimed by a published card — including the
    # published_slug mapping (research slug != final article slug).
    for _, rec in cards:
        if rec["status"] == "published":
            published_slugs.add(rec["slug"])
            if rec.get("published_slug"):
                published_slugs.add(rec["published_slug"])

    # Pass 2: rules on selectable (pending) cards.
    for line_no, rec in cards:
        slug = rec["slug"]
        status = rec["status"]
        priority = rec.get("priority")
        hold_until = rec.get("hold_until")

        # Rule 6 (added 2026-10-26, card t_52601755): langs is a list field.
        # The 2026-10-23 publish hand-wrote "langs": "de,en,fr,it" (a
        # comma-joined string) onto fairness-initiative-ehepaare-2026; the
        # string passed only because nothing consumed the field. Mark cards
        # with scripts/mark_published.py, which always emits a list.
        langs = rec.get("langs")
        if langs is not None and not isinstance(langs, list):
            failures.append(
                f"FAIL: {slug} (line {line_no}) — langs {langs!r} is a "
                f"{type(langs).__name__}, must be a JSON list like "
                f'["de", "en"]; use scripts/mark_published.py to mark cards'
            )

        if status == "published":
            # Rule 5 (added 2026-10-15 after the 601d990 breach): a card
            # published BEFORE its hold_until date consumed a future slot.
            hu = hold_until if isinstance(hold_until, str) and DATE_RE.match(hold_until or "") else None
            if hu is None and isinstance(priority, str):
                m5 = PIN_RE.match(priority)
                if m5:
                    hu = m5.group(1)
            if hu and parse_date(hu) and parse_date(hu) > today:
                failures.append(
                    f"FAIL: {slug} (line {line_no}) — published before "
                    f"hold_until {hu!r} (today {today.isoformat()}): a pinned "
                    f"card was self-published early; restore it to pending "
                    f"or annotate hold_until to the actual publish date "
                    f"with a breach note"
                )
            continue  # published/superseded etc. — pin rules otherwise N/A

        if slug in published_slugs:
            failures.append(
                f"FAIL: {slug} (line {line_no}) — pending card duplicates an "
                f"already-published slug; the publish cron would re-pick it"
            )
        if slug in seen_pending:
            failures.append(
                f"FAIL: {slug} (line {line_no}) — duplicate pending card "
                f"(first seen line {seen_pending[slug]})"
            )
        else:
            seen_pending[slug] = line_no

        if not isinstance(priority, str) or not priority.startswith("pin-"):
            continue

        pending_pins += 1
        m = PIN_RE.match(priority)
        if not m:
            failures.append(
                f"FAIL: {slug} (line {line_no}) — malformed pin priority "
                f"{priority!r}; expected pin-YYYY-MM-DD"
            )
            continue
        pin_date = parse_date(m.group(1))
        if pin_date is None:
            failures.append(
                f"FAIL: {slug} (line {line_no}) — pin priority {priority!r} "
                f"is not a real calendar date"
            )
            continue
        if pin_date < today:
            failures.append(
                f"FAIL: {slug} (line {line_no}) — pin date {m.group(1)} is in "
                f"the past (today {today.isoformat()}); re-pin or clear the "
                f"priority"
            )
        if hold_until is None:
            failures.append(
                f"FAIL: {slug} (line {line_no}) — pin without hold_until: "
                f"priority {priority!r} requires \"hold_until\": "
                f"\"{m.group(1)}\" (the 6-day selection rule cannot protect "
                f"a pin-less card)"
            )
        elif hold_until != m.group(1):
            failures.append(
                f"FAIL: {slug} (line {line_no}) — hold_until {hold_until!r} "
                f"does not match pin date {m.group(1)!r}"
            )

    return failures, pending_pins


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", default=DEFAULT_QUEUE,
                    help="queue JSONL path (default: repo data/content-research.jsonl)")
    ap.add_argument("--today", default=None,
                    help="override 'today' as YYYY-MM-DD (for tests)")
    args = ap.parse_args(argv)

    if args.today:
        today = parse_date(args.today)
        if today is None:
            print("FAIL: --today is not YYYY-MM-DD", file=sys.stderr)
            return 2
    else:
        today = dt.date.today()

    failures, pending_pins = validate(args.file, today)
    for f in failures:
        print(f)
    if failures:
        print(f"validate_queue: {len(failures)} violation(s) in {args.file}")
        return 1
    print(
        f"validate_queue: OK — {args.file} clean "
        f"({pending_pins} pending pin card(s) checked against today "
        f"{today.isoformat()})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
