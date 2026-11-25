#!/usr/bin/env python3
"""inflow_gate.py — hard cap on content-research topic inflow (t_376b7fb7).

The Friday publish grid drains 1 article/week while the daily research cron
appends ~5 topics/day (card t_a1d592fa capacity decision, 2026-10-28). At
HEAD 5c1133b the queue held 200 pending cards (93 pinned + 107 unpinned) and
grew ~34/week. Decision: cap inflow at PENDING_CAP pending cards; a gated
research run must NOT append new topics — it flips to backlog-hygiene mode
(see the STEP 0 branch of the research cron prompt, job c54c8fb04ab1).

SECOND GATE — calendar saturation (t_e0dbafb1, 2026-11-25): the pending>=cap
gate alone proved insufficent because the STEP 0' auto-drain demotes pending to
<= 98 on every gated run, re-opening the gate the next day; the run then
appends 5 topics, pushing pending back over 100, and the cycle repeats
(commits 6c185fb / 22b6bc1 / b750b0f, live churn 11-21..11-25). Since the
Friday grid has 0 free slots to 2028-06-30, appended topics have NO publish
path — the drain just demotes fresh HIGH-demand topics to backlog. New rule:
while publish_calendar reports zero free Fridays (today..horizon), the gate is
closed regardless of the pending count. Fail-open: if the calendar cannot be
computed, only the pending cap gates (old behavior), with a stderr warning.

Contract (consumed by the cron prompt, not by CI):
  stdout: one JSON object {"pending": N, "cap": PENDING_CAP, "gated": bool,
                           "free_fridays": int|null,
                           "gate_reason": "pending_cap"|"no_free_fridays"|null}
  exit 0  -> not gated (pending < cap AND calendar has a free Friday),
             or queue file missing (pending: 0)
  exit 3  -> gated   (pending >= cap OR free_fridays == 0)
  The cron branches on the exit code only; free_fridays/gate_reason are
  additive observability fields.

Malformed lines are tolerated exactly like scripts/validate_queue.py does:
blank lines are skipped, a line that is not valid JSON or not an object is
skipped with a stderr warning (never crash the gate), and only records
carrying BOTH `slug` and `status` count as queue cards — event lines
(type:recommendation/correction, ...) are ignored. Only status=="pending"
counts; "published" and "superseded" cards are excluded.

Stdlib only. `--file` exists for tests; the cron uses the default repo path.
"""

import argparse
import json
import os
import sys
import datetime


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_QUEUE = os.path.join(REPO_ROOT, "data", "content-research.jsonl")
PENDING_CAP = 100
FREE_FRIDAYS_REPORT_LIMIT = 20  # mirrors publish_calendar.py --free


def count_pending(path):
    """Return (pending_count, malformed_count). Missing file -> (0, 0)."""
    pending = 0
    malformed = 0
    try:
        with open(path, encoding="utf-8") as fh:
            for line_no, raw in enumerate(fh, 1):
                if not raw.strip():
                    continue
                try:
                    rec = json.loads(raw)
                except json.JSONDecodeError:
                    print(
                        f"WARN: line {line_no} — invalid JSON (skipped, "
                        "validate_queue.py will flag it)",
                        file=sys.stderr,
                    )
                    malformed += 1
                    continue
                if not isinstance(rec, dict):
                    print(
                        f"WARN: line {line_no} — not an object (skipped)",
                        file=sys.stderr,
                    )
                    malformed += 1
                    continue
                # Same card definition as validate_queue.py: a queue card
                # carries both slug and status; event lines do not.
                if rec.get("slug") and rec.get("status") == "pending":
                    pending += 1
    except FileNotFoundError:
        return 0, 0
    return pending, malformed


def read_cards(path):
    """Parse queue lines, keeping only dict records that carry a slug —
    the shape publish_calendar.plan() consumes. Malformed lines: skip."""
    cards = []
    try:
        with open(path, encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    rec = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if isinstance(rec, dict) and rec.get("slug"):
                    cards.append(rec)
    except FileNotFoundError:
        pass
    return cards


def count_free_fridays(cards, today=None):
    """Free Friday publish slots (today..HORIZON_END), counted exactly like
    publish_calendar.py --free (capped at FREE_FRIDAYS_REPORT_LIMIT).
    Returns None if the calendar cannot be computed — the gate then fails
    OPEN so a planner bug can never silently freeze content inflow."""
    try:
        scripts_dir = os.path.join(REPO_ROOT, "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        import publish_calendar as pc
        cal, _unplaced = pc.plan(cards)
        today = today or datetime.date.today()
        n = 0
        for s in pc.fridays():
            if s not in cal and s >= today:
                n += 1
                if n >= FREE_FRIDAYS_REPORT_LIMIT:
                    break
        return n
    except Exception as exc:  # noqa: BLE001 — fail-open by design
        print(f"WARN: calendar saturation check failed ({exc}); "
              "gating on the pending cap only", file=sys.stderr)
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", default=DEFAULT_QUEUE,
                    help="queue jsonl path (default: repo data/"
                         "content-research.jsonl)")
    args = ap.parse_args(argv)

    pending, _malformed = count_pending(args.file)
    free = count_free_fridays(read_cards(args.file))
    if pending >= PENDING_CAP:
        gated, reason = True, "pending_cap"
    elif free == 0:
        gated, reason = True, "no_free_fridays"
    else:
        gated, reason = False, None
    print(json.dumps({"pending": pending, "cap": PENDING_CAP, "gated": gated,
                      "free_fridays": free, "gate_reason": reason}))
    if gated:
        print(f"inflow_gate: GATED ({reason}) — pending={pending}, "
              f"cap={PENDING_CAP}, free_fridays={free}; no unpinned appends "
              "this run, flip to backlog hygiene", file=sys.stderr)
    return 3 if gated else 0


if __name__ == "__main__":
    sys.exit(main())
