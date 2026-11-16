#!/usr/bin/env python3
"""publish_picker.py — deterministic topic picker for the "steuer content
publish" cron (card t_4fa4b841).

WHY THIS EXISTS. Topic selection lived only as prompt prose ("pick the best
pending topic; pinned records within 7 days of the pin date ahead of demand
ranking"). That prose consulted the queue-side hold_until / pin-YYYY-MM-DD
fields and NEVER scripts/publish_calendar.py's FIXED dict. Evidence:
arbeitgeber-3a-beitrag-lohnausweis was FIXED-pinned for 2026-12-11
(publish_calendar.py @ 7998b4b, 2026-10-21) but the daily publish cron
shipped it on Fri 2026-11-13 (bdb388b) — four weeks early — because the
queue-side hold_until had drifted to the publish day, so validate_queue
rule 5 saw nothing and the script-side pin was invisible to the picker.
This script is the machine-checkable picker; the cron prompt must run it
and publish only its `pick`.

RULES (all deterministic):
  * Candidates: status:"pending" with type None/"article" — the same filter
    as publish_calendar.plan().
  * Pin sources per slug: FIXED[slug] in the calendar script (authoritative
    product intent), the record's hold_until, and its priority matching
    pin-YYYY-MM-DD. The BINDING slot is the LATEST well-formed source date:
    if any source pins to a future Friday, that intent wins — a drifted
    queue date must not launder a script-side FIXED pin (the incident shape).
  * Pinned cards are selectable only inside the prep window:
    binding_slot - today <= PREP_WINDOW_DAYS (7, defined in
    publish_calendar.py). On the Friday-only grid the first run that admits
    a slot-Friday card is the preceding Friday (week N-1 prep window);
    week N-2 or earlier (>= 14 days out) MUST be skipped.
  * Unpinned pending cards are always selectable (demand-ranked) — they are
    off-calendar by construction; the planner places only pinned cards.
  * Ordering: admitted pinned cards first (earliest slot first, then demand,
    then oldest date, then slug), then unpinned cards (demand
    high > medium > low > unknown, then oldest date, then slug).
  * Disagreeing pin sources are reported as drift warnings — reconciliation
    is the Monday maintenance cron (publish_calendar.py --fix), never a
    silent pick here.

USAGE (from repo root):
    python3 scripts/publish_picker.py
    python3 scripts/publish_picker.py --today 2026-11-13 --queue /tmp/f.jsonl
    python3 scripts/publish_picker.py --check <slug>

EXIT CODES:
    0  ran (JSON on stdout; `pick` may be null)
    1  --check: slug not found among pending article cards
    2  unreadable/broken queue or calendar file
    3  --check: card exists but its pin slot is outside the prep window
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_QUEUE = REPO / "data" / "content-research.jsonl"
DEFAULT_CALENDAR = REPO / "scripts" / "publish_calendar.py"

_PIN_RE = re.compile(r"^pin-(\d{4}-\d{2}-\d{2})$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DEMAND_RANK = {"high": 0, "medium": 1, "low": 2}


def load_calendar(path: Path):
    """Load FIXED + PREP_WINDOW_DAYS from a publish_calendar.py file."""
    spec = importlib.util.spec_from_file_location("_pubcal", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FIXED, getattr(mod, "PREP_WINDOW_DAYS", 7)


def _parse(d):
    if not (isinstance(d, str) and _DATE_RE.match(d)):
        return None
    try:
        return dt.date.fromisoformat(d)
    except ValueError:
        return None


def pin_sources(slug, rec, fixed):
    """All known pin dates for a card: {source_name: iso-date}.

    Only well-formed values count; a malformed date is reported separately
    by the caller via the returned warnings list.
    """
    sources, warnings = {}, []
    fx = fixed.get(slug)
    if fx is not None:
        if _parse(fx):
            sources["FIXED"] = fx
        else:
            warnings.append(f"malformed FIXED date for {slug}: {fx!r}")
    hu = rec.get("hold_until")
    if hu is not None:
        if _parse(hu):
            sources["hold_until"] = hu
        else:
            warnings.append(f"malformed hold_until for {slug}: {hu!r}")
    pr = rec.get("priority")
    if isinstance(pr, str):
        m = _PIN_RE.match(pr)
        if m:
            sources["priority"] = m.group(1)
    return sources, warnings


def evaluate(cards, fixed, today: dt.date, window: int):
    """Split pending article cards into eligible/blocked, with warnings."""
    eligible, blocked, warnings = [], [], []
    for c in cards:
        slug = c.get("slug")
        if not slug:
            continue
        sources, warns = pin_sources(slug, c, fixed)
        warnings.extend(warns)
        dates = sorted({_parse(v) for v in sources.values() if _parse(v)})
        if not dates:
            eligible.append({
                "slug": slug, "title": c.get("title", slug),
                "demand": c.get("demand"), "pinned": False,
                "slot": None, "days_until": None, "sources": {},
            })
            continue
        slot = dates[-1]  # binding slot = latest pin intent wins
        entry = {
            "slug": slug, "title": c.get("title", slug),
            "demand": c.get("demand"), "pinned": True,
            "slot": slot.isoformat(), "days_until": (slot - today).days,
            "sources": sources,
        }
        if len({d.isoformat() for d in dates}) > 1:
            warnings.append(
                f"drift: {slug} pins disagree "
                + ", ".join(f"{k}={v}" for k, v in sorted(sources.items()))
                + f" — binding slot {slot.isoformat()}; Monday --fix must reconcile"
            )
        if entry["days_until"] <= window:
            eligible.append(entry)
        else:
            blocked.append(entry)
    blocked.sort(key=lambda e: (e["slot"], e["slug"]))
    return eligible, blocked, warnings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--queue", default=str(DEFAULT_QUEUE))
    ap.add_argument("--calendar", default=str(DEFAULT_CALENDAR),
                    help="publish_calendar.py to read FIXED/PREP_WINDOW_DAYS "
                         "from (test seam; default: the repo's own)")
    ap.add_argument("--today", default=None,
                    help="YYYY-MM-DD override for the clock (deterministic runs)")
    ap.add_argument("--check", metavar="SLUG", default=None,
                    help="answer for one slug only: exit 0 selectable / 3 blocked")
    args = ap.parse_args(argv)

    today = dt.date.today()
    if args.today:
        today = _parse(args.today)
        if today is None:
            print(f"publish_picker: --today must be YYYY-MM-DD, got {args.today!r}",
                  file=sys.stderr)
            return 2
    try:
        fixed, window = load_calendar(Path(args.calendar))
    except Exception as exc:
        print(f"publish_picker: cannot load calendar {args.calendar}: {exc}",
              file=sys.stderr)
        return 2
    records, line_errors = [], []
    try:
        for ln in Path(args.queue).read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            try:
                records.append(json.loads(ln))
            except json.JSONDecodeError:
                line_errors.append(ln[:120])
    except OSError as exc:
        print(f"publish_picker: cannot read queue {args.queue}: {exc}",
              file=sys.stderr)
        return 2

    # inject creation date for the oldest-first tie-break
    records_ok = [c for c in records if isinstance(c, dict)]
    cards = [c for c in records_ok
             if c.get("status") == "pending"
             and c.get("type") in (None, "article")]
    by_slug = {}
    for c in cards:
        s = c.get("slug")
        if s and s not in by_slug:
            by_slug[s] = c
    el, bl, wn = evaluate(cards, fixed, today, window)
    warnings = list(wn)
    if line_errors:
        warnings.append(f"{len(line_errors)} malformed JSONL line(s) skipped")
    # oldest-first within equal (pinned, slot, demand): attach date, re-sort
    for lst in (el, bl):
        for e in lst:
            e["_date"] = by_slug.get(e["slug"], {}).get("date") or "9999-99-99"
        lst.sort(key=lambda e: (
            not e["pinned"],
            e["slot"] or "9999-99-99",
            _DEMAND_RANK.get(str(e["demand"]).lower(), 3),
            e["_date"],
            e["slug"],
        ))
    for lst in (el, bl):
        for e in lst:
            e.pop("_date", None)

    out = {"today": today.isoformat(), "window_days": window,
           "pick": None, "eligible": el, "blocked": bl, "warnings": warnings}
    if args.check:
        hit = next((e for e in el if e["slug"] == args.check), None)
        block = next((e for e in bl if e["slug"] == args.check), None)
        out["check"] = {"slug": args.check,
                        "selectable": hit is not None,
                        "entry": hit or block}
        if hit is not None:
            out["pick"] = dict(hit, why=_why(hit, window, len(bl)))
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0
        if block is not None:
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 3
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1
    if el:
        out["pick"] = dict(el[0], why=_why(el[0], window, len(bl)))
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def _why(e, window, n_blocked=0):
    if e["pinned"]:
        w = (f"pinned slot {e['slot']} inside the {window}-day "
             f"prep window (days_until={e['days_until']})")
    else:
        w = f"unpinned; demand={e.get('demand') or 'unknown'}"
    if n_blocked:
        w += f" ({n_blocked} pinned card(s) skipped: slot still in the future)"
    return w


if __name__ == "__main__":
    sys.exit(main())
