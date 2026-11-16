#!/usr/bin/env python3
"""Canonical record-writer for publishing a queue card (card t_52601755).

Why this exists: publishes hand-edited data/content-research.jsonl inline,
and the 2026-10-23 publish wrote "langs": "de,en,fr,it" — a comma-joined
string — onto fairness-initiative-ehepaare-2026 while every other published
record carries a JSON list. validate_queue.py now rejects non-list langs
(Rule 6), so from now on the publish step marks cards ONLY through this
script, which cannot produce the broken shape.

Guarantees:
  * the publish stamp lands on the SCHEMA field `published_at` (card
    t_6544e449: until 2026-10-30 this script wrote `published_date`, so every
    new publish re-opened the null-published_at hole the c474a136 backfill
    closed; nothing else in scripts/ reads `published_date`, and any leftover
    on a touched record is dropped — rename semantics).
  * scheduling fields are stale the moment a card flips to published, so
    `hold_until`, `priority` AND `release_intent` are cleared on the flip
    (t_6544e449 finding 1; @PM 2026-10-30 verdict: the pinned-Friday
    hold_until/priority is the calendar slot of record and release_intent
    was a stale off-grid Monday — treat it as a stale field too, AC e
    sign-off granted).
  * langs is always emitted as a JSON list of 2-letter codes ("de,en,fr,it"
    input is split for you; duplicates removed, order preserved).
  * exactly one line of the queue changes; anything else aborts the write.
  * the candidate file must pass scripts/validate_queue.py before it
    replaces the original (atomic replace).
  * serialization matches the queue convention: json.dumps(...,
    ensure_ascii=False), one record per line.

Usage (from repo root, on publish day, alongside building the pages):
    python3 scripts/mark_published.py <slug> --langs de,en,fr,it
    # override the stamp date if re-running for an earlier publish:
    python3 scripts/mark_published.py <slug> --langs de,en,fr,it --published-at 2026-10-23

Exit codes: 0 written, 1 usage/validation failure, 2 file/format error.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jsonl_guard  # noqa: E402  size guard for the queue, t_2ed95a27
import publish_calendar  # noqa: E402  FIXED pins gate, t_4fa4b841

_PIN_RE = re.compile(r"^pin-(\d{4}-\d{2}-\d{2})$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REPO = Path(__file__).resolve().parent.parent
DEFAULT_QUEUE = str(REPO / "data" / "content-research.jsonl")
VALIDATOR = str(REPO / "scripts" / "validate_queue.py")


def normalize_langs(value: str | list) -> list[str]:
    """Coerce any plausible langs input into an ordered, deduped list."""
    if isinstance(value, list):
        parts = [str(v) for v in value]
    else:
        parts = str(value).replace(";", ",").split(",")
    out: list[str] = []
    for p in parts:
        code = p.strip().lower()
        if not code:
            continue
        if len(code) != 2 or not code.isalpha():
            raise ValueError(f"not a 2-letter language code: {p!r}")
        if code not in out:
            out.append(code)
    if not out:
        raise ValueError("langs resolved to an empty list")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("slug", help="queue card slug to mark published")
    ap.add_argument("--langs", required=True,
                    help='published language set, e.g. "de,en,fr,it" '
                         '(always written as a JSON list)')
    ap.add_argument("--published-at", "--published-date", dest="published_at",
                    default=None,
                    help="YYYY-MM-DD stamp for the schema field "
                         "published_at (default: today); "
                         "--published-date kept as a compat alias")
    ap.add_argument("--file", default=DEFAULT_QUEUE)
    ap.add_argument("--calendar", default=None,
                    help="publish_calendar.py to read FIXED/PREP_WINDOW_DAYS "
                         "from (test seam; default: the repo's own)")
    ap.add_argument("--no-validate", action="store_true",
                    help="skip the validate_queue.py subprocess — unit tests "
                         "with synthetic queue records only")
    ap.add_argument("--force", action="store_true",
                    help="allow the write even if the size guard (t_2ed95a27) "
                         "would reject it")
    args = ap.parse_args(argv)

    try:
        langs = normalize_langs(args.langs)
    except ValueError as exc:
        print(f"mark_published: bad langs: {exc}", file=sys.stderr)
        return 1

    if args.published_at:
        try:
            dt.date.fromisoformat(args.published_at)
        except ValueError:
            print("mark_published: --published-at must be YYYY-MM-DD",
                  file=sys.stderr)
            return 1
        stamp = args.published_at
    else:
        stamp = dt.date.today().isoformat()

    path = Path(args.file)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"mark_published: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    hits = []
    for idx, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"mark_published: {path} line {idx + 1} is not valid JSON: {exc}",
                  file=sys.stderr)
            return 2
        if isinstance(rec, dict) and rec.get("slug") == args.slug and rec.get("status"):
            hits.append((idx, rec))

    if len(hits) != 1:
        print(f"mark_published: expected exactly 1 card with slug {args.slug!r}, "
              f"found {len(hits)} — aborting", file=sys.stderr)
        return 1
    idx, rec = hits[0]
    if rec.get("status") == "published":
        print(f"mark_published: {args.slug} is already "
              f"published_at={rec.get('published_at', rec.get('published_date'))!r} "
              f"langs={rec.get('langs')!r} — nothing to do", file=sys.stderr)
        return 1

    # t_4fa4b841: FIXED calendar pins gate the write too. Evidence chain:
    # arbeitgeber-3a-beitrag-lohnausweis was FIXED-pinned for 2026-12-11
    # (publish_calendar.py @ 7998b4b) but published Fri 2026-11-13 (bdb388b)
    # because neither the picker prose nor this writer consulted the FIXED
    # dict — the queue-side hold_until had drifted to the publish day, so
    # validate_queue rule 5 (jsonl-only) could not see the breach. A card
    # whose FIXED slot is more than PREP_WINDOW_DAYS after the publish stamp
    # is REFUSED here; a human-set slot_override is the only escape
    # (CTO ruling 2026-10-15: slot calendar changes are the founder's call).
    cal_mod = publish_calendar
    if args.calendar:
        import importlib.util
        _spec = importlib.util.spec_from_file_location(
            "_pubcal", args.calendar)
        cal_mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(cal_mod)
    fixed_slot = cal_mod.FIXED.get(args.slug)
    if isinstance(fixed_slot, str) and _DATE_RE.match(fixed_slot):
        window = getattr(cal_mod, "PREP_WINDOW_DAYS", 7)
        days_early = (dt.date.fromisoformat(fixed_slot)
                      - dt.date.fromisoformat(stamp)).days
        if days_early > window:
            if rec.get("slot_override"):
                print(f"mark_published: {args.slug} is FIXED for "
                      f"{fixed_slot} but the card carries slot_override="
                      f"{rec['slot_override']!r} — proceeding (human call)",
                      file=sys.stderr)
            else:
                print(f"mark_published: REFUSED — {args.slug} is FIXED-pinned "
                      f"for {fixed_slot} in scripts/publish_calendar.py, "
                      f"{days_early} days after the {stamp} stamp "
                      f"(prep window is {window} days). Publishing early "
                      f"defeats the cluster-spread hygiene the Friday grid "
                      f"encodes (incident: bdb388b). Run "
                      f"scripts/publish_picker.py for the week's selection; "
                      f"only a human-set slot_override lifts this gate.",
                      file=sys.stderr)
                return 1

    rec["status"] = "published"
    rec["published_at"] = stamp  # schema field (t_fcff6abc); NOT published_date
    rec.pop("published_date", None)  # rename semantics: wrong key never survives a flip
    # Scheduling fields are stale the moment the card is live: the Friday
    # pin/hold grid no longer applies, and release_intent is a pre-publish
    # intent, not a post-publish record (@PM 2026-10-30 verdict, AC c/e).
    # EXCEPTION: a hold_until/pin dated AFTER the publish date is
    # early-publish evidence (601d990 precedent) — keep it so validate_queue
    # rule 5 can still fail CI on a flip that jumped its slot.
    cleared = []
    for k in ("hold_until", "priority", "release_intent"):
        v = rec.get(k)
        if v is None:
            continue
        if k == "priority":
            m = _PIN_RE.match(v) if isinstance(v, str) else None
            d = m.group(1) if m else None
        elif k == "hold_until":
            d = v if isinstance(v, str) and _DATE_RE.match(v) else None
        else:  # release_intent: always a pre-publish intent
            d = None
        if d is not None and d > stamp:
            continue  # breach evidence — leave for rule 5
        cleared.append(k)
        rec.pop(k)
    rec["langs"] = langs  # list, always — this is the whole point of the script

    new_line = json.dumps(rec, ensure_ascii=False)
    old_lines = list(lines)
    lines[idx] = new_line
    changed = [i + 1 for i in range(len(lines)) if lines[i] != old_lines[i]]
    if changed != [idx + 1] or len(lines) != len(old_lines):
        print(f"mark_published: sanity check failed — would change lines {changed}; "
              "aborting", file=sys.stderr)
        return 1

    # t_2ed95a27 size guard: never let a publish mark shrink the queue.
    rejected, msg = jsonl_guard.shrink_rejected(old_lines, lines,
                                                force=args.force)
    if msg:
        print(msg, file=sys.stderr)
    if rejected:
        return 1

    # Write a temp sibling, validate it, then atomically replace.
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".mark_pub_",
                               suffix=".jsonl")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + ("\n" if any(l.strip() for l in old_lines) else ""))
        if not args.no_validate:
            res = subprocess.run([sys.executable, VALIDATOR, "--file", tmp],
                                 capture_output=True, text=True)
            if res.returncode != 0:
                print((res.stdout + res.stderr).strip(), file=sys.stderr)
                print("mark_published: validator rejected the candidate file; "
                      "original untouched", file=sys.stderr)
                return 1
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

    print(f"mark_published: line {idx + 1} {args.slug} -> "
          f"status=published published_at={stamp} langs={langs} cleared={cleared}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
