#!/usr/bin/env python3
"""auto_drain.py — standing auto-drain on inflow-gate hit (t_1d5bd391).

CTO standing ruling 2026-11-09 (jev-gated): when scripts/inflow_gate.py trips
(pending >= PENDING_CAP), the gated research run must NOT wait for a manual
drain pass — it auto-demotes the lowest-demand UNPINNED pending cards to
`status: "backlog"` until pending lands back at cap - margin. Invariance:
cap stays 100, pinned Friday-grid records (hold_until != null) are NEVER
touched. Mechanism follows the proven manual drains a8aff7e / 05a829f: flip
`"status": "pending"` -> `"status": "backlog"` on the jsonl record, all other
fields untouched.

Selection (deterministic, no randomness):
  candidates = records with slug, status=="pending", and hold_until
               absent-or-null (pinned excluded absolutely);
  order      = demand ascending (unknown/missing/other sorts lowest,
               then low < med == medium < high),
               tie-break oldest `date` first, then original file order;
  count      = minimum n such that pending_after <= cap - margin,
               always >= 1 per triggering event (capped by candidate
               availability — if unpinned candidates run out before the
               target is met, demote them all and WARN on stderr).

Contract (consumed by the research-cron STEP 0 gated branch):
  stdout: exactly ONE audit JSON line
    {"demoted": ["slug(demand)", ...], "pending_before": N,
     "pending_after": M, "cap": 100, "margin": 2}
  exit 0 = handled (drained, or below cap -> no-op, or nothing demotable).
  exit 2 = bad arguments. Malformed lines are tolerated exactly like
  scripts/inflow_gate.py / scripts/validate_queue.py do (skipped with a
  stderr warning, never crash the drain, never rewritten).

`--dry-run` prints the same audit line (with would-be counts) and writes
nothing. `--file`/`--cap`/`--margin` exist for tests; the cron uses defaults.
Stdlib only. The inflow_gate.py read-path is intentionally untouched.
"""

import argparse
import json
import os
import sys

PENDING_CAP = 100          # mirrors scripts/inflow_gate.py PENDING_CAP
DRAIN_MARGIN = 2           # land at pending <= cap - margin

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_QUEUE = os.path.join(REPO_ROOT, "data", "content-research.jsonl")

# Demand ordering for demotion (lowest demand goes first). Anything not
# listed — missing field, non-string, novel label — sorts lowest (unknown).
DEMAND_RANK = {"low": 1, "med": 2, "medium": 2, "high": 3}
RANK_UNKNOWN = 0


def demand_rank(value):
    if isinstance(value, str):
        return DEMAND_RANK.get(value.strip().lower(), RANK_UNKNOWN)
    return RANK_UNKNOWN


def is_pinned(rec):
    """Pinned == hold_until present AND non-null. Excluded absolutely."""
    return rec.get("hold_until") is not None


def demote_line(raw, rec, slug, warns, line_no):
    """Return raw with status pending->backlog, minimal-diff.

    Prefer an in-place string flip (keeps every other byte identical); fall
    back to a key-order-preserving json.dumps rewrite if the token is not
    uniquely findable in the line."""
    token = '"status": "pending"'
    if raw.count(token) == 1:
        return raw.replace(token, '"status": "backlog"', 1)
    rec = dict(rec)
    rec["status"] = "backlog"
    warns.append(
        f"WARN: line {line_no} ({slug}) — status token not unique in raw "
        "line; rewrote record via json.dumps (fields preserved)")
    return json.dumps(rec, ensure_ascii=False)


def drain(lines, cap, margin, warns):
    """Pure core: takes raw file lines, returns
    (new_lines, demoted_labels, pending_before, pending_after)."""
    parsed = []  # (line_no, raw, rec|None)
    pending_idx = []  # positions in `lines` of pending cards
    for i, raw in enumerate(lines):
        if not raw.strip():
            parsed.append((i, raw, None))
            continue
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError:
            print(f"WARN: line {i + 1} — invalid JSON (skipped, "
                  "validate_queue.py will flag it)", file=sys.stderr)
            warns.append(f"line {i + 1}: invalid JSON (left untouched)")
            parsed.append((i, raw, None))
            continue
        if not isinstance(rec, dict):
            print(f"WARN: line {i + 1} — not an object (skipped)",
                  file=sys.stderr)
            warns.append(f"line {i + 1}: not an object (left untouched)")
            parsed.append((i, raw, None))
            continue
        parsed.append((i, raw, rec))
        # Same card definition as inflow_gate.py / validate_queue.py.
        if rec.get("slug") and rec.get("status") == "pending":
            pending_idx.append(i)

    pending_before = len(pending_idx)
    demoted_labels = []
    new_lines = list(lines)

    if pending_before < cap:
        # Not gated — no-op.
        return new_lines, [], pending_before, pending_before

    candidates = []
    for i in pending_idx:
        rec = parsed[i][2]
        if is_pinned(rec):
            continue
        candidates.append(
            (demand_rank(rec.get("demand")), str(rec.get("date") or ""), i,
             rec))
    candidates.sort(key=lambda c: (c[0], c[1], c[2]))

    target = cap - margin
    need = max(pending_before - target, 1)
    chosen = candidates[:need]
    if len(chosen) < need:
        warns.append(
            f"insufficient unpinned candidates: demoted all {len(chosen)}, "
            f"pending_after={pending_before - len(chosen)} still > "
            f"cap-margin={target} — pinned grid must not be drained")

    for _rank, _date, i, rec in chosen:
        slug = rec["slug"]
        label = f"{slug}({rec.get('demand', 'unknown')})"
        new_lines[i] = demote_line(new_lines[i], rec, slug, warns, i + 1)
        demoted_labels.append(label)

    return new_lines, demoted_labels, pending_before, (
        pending_before - len(demoted_labels))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", default=DEFAULT_QUEUE,
                    help="queue jsonl path (default: repo data/"
                         "content-research.jsonl)")
    ap.add_argument("--cap", type=int, default=PENDING_CAP,
                    help=f"pending cap (default: {PENDING_CAP}, mirrors "
                         "inflow_gate.py)")
    ap.add_argument("--margin", type=int, default=DRAIN_MARGIN,
                    help=f"headroom below cap to land at (default: "
                         f"{DRAIN_MARGIN})")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the audit line, write nothing")
    args = ap.parse_args(argv)

    if args.cap < 1 or args.margin < 0 or args.margin >= args.cap:
        print("ERROR: need cap >= 1 and 0 <= margin < cap", file=sys.stderr)
        return 2

    try:
        with open(args.file, encoding="utf-8") as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        lines = []

    warns = []
    new_lines, demoted, before, after = drain(lines, args.cap, args.margin,
                                              warns)
    for w in warns:
        print(f"WARN: {w}", file=sys.stderr)

    print(json.dumps({"demoted": demoted, "pending_before": before,
                      "pending_after": after, "cap": args.cap,
                      "margin": args.margin}))

    if args.dry_run:
        print("auto_drain: dry-run — file not modified", file=sys.stderr)
        return 0
    if demoted:
        tmp = args.file + ".auto-drain.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.writelines(new_lines)
        os.replace(tmp, args.file)
        if not new_lines or not new_lines[-1].endswith("\n"):
            # keep the file newline-terminated like every prior drain
            with open(args.file, "a", encoding="utf-8") as fh:
                fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
