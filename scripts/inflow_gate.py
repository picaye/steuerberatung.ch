#!/usr/bin/env python3
"""inflow_gate.py — hard cap on content-research topic inflow (t_376b7fb7).

The Friday publish grid drains 1 article/week while the daily research cron
appends ~5 topics/day (card t_a1d592fa capacity decision, 2026-10-28). At
HEAD 5c1133b the queue held 200 pending cards (93 pinned + 107 unpinned) and
grew ~34/week. Decision: cap inflow at PENDING_CAP pending cards; a gated
research run must NOT append new topics — it flips to backlog-hygiene mode
(see the STEP 0 branch of the research cron prompt, job c54c8fb04ab1).

Contract (consumed by the cron prompt, not by CI):
  stdout: one JSON object {"pending": N, "cap": PENDING_CAP, "gated": bool}
  exit 0  -> not gated (pending < cap), or queue file missing (pending: 0)
  exit 3  -> gated   (pending >= cap)

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

PENDING_CAP = 100

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_QUEUE = os.path.join(REPO_ROOT, "data", "content-research.jsonl")


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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", default=DEFAULT_QUEUE,
                    help="queue jsonl path (default: repo data/"
                         "content-research.jsonl)")
    args = ap.parse_args(argv)

    pending, _malformed = count_pending(args.file)
    gated = pending >= PENDING_CAP
    print(json.dumps({"pending": pending, "cap": PENDING_CAP,
                      "gated": gated}))
    return 3 if gated else 0


if __name__ == "__main__":
    sys.exit(main())
