#!/usr/bin/env python3
"""test_auto_drain.py — regression guards for scripts/auto_drain.py (t_1d5bd391).

Style mirrors scripts/test_inflow_gate.py. Guards:
  A1  below cap -> no-op, exit 0, file byte-identical, audit demoted == [].
  A2  exactly at cap -> demotes the MINIMUM count to land at cap - margin.
  A3  well above cap -> same minimum-count rule.
  A4  pinned (hold_until != null) records are NEVER selected, even when
      they are the lowest-demand pendings; demotion skips to unpinned.
  A5  demand ordering: unknown/missing < low < med == medium < high.
  A6  tie-break oldest `date` first within equal demand rank.
  A7  audit line is exactly one JSON object with keys
      demoted/pending_before/pending_after/cap/margin; demoted entries are
      "slug(demand)".
  A8  idempotent: a second run against the drained file demotes nothing.
  A9  validate_queue.py exits 0 on drained fixture output.
  A10 --dry-run prints the audit line but leaves the file untouched.
  A11 malformed lines are tolerated validate_queue/gate-style and never
      rewritten (byte-identical pass-through).
  A12 demotion is a pure status flip: all other fields/keys byte-identical
      (single-line diff, '"status": "pending"' -> '"status": "backlog"').

    python3 scripts/test_auto_drain.py

Exit 0 = every guard holds; exit 1 = a guard regressed.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "auto_drain.py"
VALIDATOR = REPO / "scripts" / "validate_queue.py"

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = ""):
    status = "ok" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def card(slug, demand="high", date="2026-10-01", hold_until=None,
         status="pending"):
    rec = {"date": date, "slug": slug, "title": slug, "meta": "m",
           "facts": [], "status": status}
    if demand is not None:
        rec["demand"] = demand
    if hold_until is not None:
        rec["hold_until"] = hold_until
        rec["priority"] = f"pin-{hold_until}"
    return json.dumps(rec, ensure_ascii=False)


def write_queue(lines):
    tmp = Path(tempfile.mkdtemp()) / "content-research.jsonl"
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return tmp


def run_drain(queue_path, *extra):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--file", str(queue_path), *extra],
        capture_output=True, text=True,
    )
    out = json.loads(proc.stdout)
    return proc, out


def main():
    # A1 below cap -> no-op
    q = write_queue([card(f"s{i}") for i in range(9)])
    before_bytes = q.read_bytes()
    proc, out = run_drain(q, "--cap", "10", "--margin", "2")
    check("A1 below cap: no-op, exit 0, file untouched",
          proc.returncode == 0 and out["demoted"] == []
          and out["pending_before"] == out["pending_after"] == 9
          and q.read_bytes() == before_bytes,
          f"{out} rc={proc.returncode}")

    # A2 exactly at cap: 10 pending, cap 10, margin 2 -> demote exactly 2
    q = write_queue([card(f"s{i}", demand="high") for i in range(10)])
    proc, out = run_drain(q, "--cap", "10", "--margin", "2")
    check("A2 at cap: minimum demotions (2) land at cap-margin",
          proc.returncode == 0 and len(out["demoted"]) == 2
          and out["pending_before"] == 10 and out["pending_after"] == 8,
          f"{out} rc={proc.returncode}")

    # A3 above cap: 15 pending, cap 10, margin 2 -> target 8 -> demote 7
    q = write_queue([card(f"s{i}", demand="high") for i in range(15)])
    proc, out = run_drain(q, "--cap", "10", "--margin", "2")
    check("A3 above cap: demotes minimum to land <= cap-margin",
          len(out["demoted"]) == 7 and out["pending_after"] == 8, f"{out}")

    # A4 pinned never selected: 12 pending (cap 10, margin 2 -> target 8,
    # demote 4); the 4 oldest are pinned low; unpinned are high.
    lines = [card(f"pin{i}", demand="low", date=f"2026-01-0{i}",
                  hold_until=f"2026-05-0{i}") for i in range(4)]
    lines += [card(f"unp{i}", demand="high", date=f"2026-02-0{i}")
              for i in range(8)]
    q = write_queue(lines)
    proc, out = run_drain(q, "--cap", "10", "--margin", "2")
    demoted_slugs = [d.split("(")[0] for d in out["demoted"]]
    check("A4 pinned (hold_until) never demoted even if lowest demand",
          all(not s.startswith("pin") for s in demoted_slugs)
          and sorted(demoted_slugs) == ["unp0", "unp1", "unp2", "unp3"],
          f"{out}")
    # and no hold_until value anywhere flipped:
    for raw in q.read_text(encoding="utf-8").splitlines():
        rec = json.loads(raw)
        if raw and rec.get("slug", "").startswith("pin"):
            if rec.get("status") == "backlog":
                check("A4b pinned records keep status", False, rec["slug"])

    # A5 demand ordering: unknown/missing < low < med == medium < high
    lines = [
        card("d_unknown", demand="unknown-label", date="2026-01-01"),
        card("d_missing", demand=None, date="2026-01-02"),
        card("d_low", demand="low", date="2026-01-03"),
        card("d_med", demand="med", date="2026-01-04"),
        card("d_medium", demand="medium", date="2026-01-05"),
        card("d_high", demand="high", date="2026-01-06"),
        card("d_high2", demand="high", date="2026-01-07"),
    ]
    # 7 pending, cap 7, margin 0 -> demote exactly 7? No: cap-margin=7 ->
    # need max(7-7,1)=1: demotes the single lowest-ranked: unknown sorts
    # lowest, tie with missing -> oldest date first -> d_unknown (2026-01-01).
    q = write_queue(lines)
    proc, out = run_drain(q, "--cap", "7", "--margin", "0")
    check("A5a unknown demand sorts lowest, oldest date first",
          out["demoted"] == ["d_unknown(unknown-label)"], f"{out}")
    # margin 6 -> target 1 -> need 6: everything but the LAST in order.
    # expected order: d_unknown, d_missing, d_low, d_med, d_medium, d_high;
    # survivor d_high2 (highest rank, newest). med==medium adjacent.
    q = write_queue(lines)
    proc, out = run_drain(q, "--cap", "7", "--margin", "6")
    got = [d.split("(")[0] for d in out["demoted"]]
    check("A5b full rank order low<med==medium<high, unknown first",
          got == ["d_unknown", "d_missing", "d_low", "d_med", "d_medium",
                  "d_high"] and out["pending_after"] == 1, f"{got}")

    # A6 tie-break oldest date within equal rank
    lines = [card("t_new", demand="low", date="2026-03-15"),
             card("t_old", demand="low", date="2026-01-02"),
             card("t_mid", demand="low", date="2026-02-20")]
    q = write_queue(lines)
    proc, out = run_drain(q, "--cap", "3", "--margin", "1")
    check("A6 equal demand demotes oldest date first",
          out["demoted"] == ["t_old(low)"], f"{out}")

    # A7 audit contract
    q = write_queue([card(f"s{i}") for i in range(11)])
    proc, out = run_drain(q, "--cap", "10", "--margin", "2")
    check("A7 stdout is one JSON object, exact keys, slug(demand) labels",
          proc.stdout.strip().count("\n") == 0
          and set(out) == {"demoted", "pending_before", "pending_after",
                           "cap", "margin"}
          and all("(" in d and d.endswith(")") for d in out["demoted"])
          and out["cap"] == 10 and out["margin"] == 2,
          f"stdout={proc.stdout!r}")

    # A8 idempotent: second run demotes nothing
    proc2, out2 = run_drain(q, "--cap", "10", "--margin", "2")
    check("A8 idempotent: drained file -> no further demotions",
          proc2.returncode == 0 and out2["demoted"] == []
          and out2["pending_before"] == out2["pending_after"] == 8, f"{out2}")

    # A9 validator green on drained output
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), "--file", str(q)],
        capture_output=True, text=True)
    check("A9 validate_queue.py exits 0 on drained fixture",
          proc.returncode == 0, proc.stdout + proc.stderr)

    # A10 dry-run leaves file untouched
    q = write_queue([card(f"s{i}") for i in range(11)])
    snap = q.read_bytes()
    proc, out = run_drain(q, "--cap", "10", "--margin", "2", "--dry-run")
    check("A10 --dry-run prints audit, writes nothing",
          len(out["demoted"]) == 3 and out["pending_after"] == 8
          and q.read_bytes() == snap and "dry-run" in proc.stderr, f"{out}")

    # A11 malformed lines: skipped with warning, passed through byte-exact
    good = [card("g1", demand="low", date="2026-01-01"),
            card("g2", demand="high", date="2026-01-02")]
    q = write_queue(good + ["{not json at all", "[1,2,3]", ""] +
                    [card(f"s{i}") for i in range(9)])
    proc, out = run_drain(q, "--cap", "10", "--margin", "1")
    after = q.read_text(encoding="utf-8").splitlines()
    check("A11 malformed lines never rewritten, valid cards drained",
          proc.returncode == 0 and "{not json at all" in after
          and "[1,2,3]" in after and len(out["demoted"]) == 2,
          f"{out} rc={proc.returncode}")
    check("A11b malformed-line warning on stderr",
          "invalid JSON" in proc.stderr, proc.stderr)

    # A12 status-only diff: other fields byte-identical
    lines = ([card("keep1", demand="low", date="2026-01-01")]
             + [card(f"s{i}") for i in range(10)])
    q = write_queue(lines)
    orig = q.read_text(encoding="utf-8").splitlines()
    proc, out = run_drain(q, "--cap", "10", "--margin", "2")
    new = q.read_text(encoding="utf-8").splitlines()
    changed = [(o, n) for o, n in zip(orig, new) if o != n]
    only_status = all(
        o.replace('"status": "pending"', '"status": "backlog"', 1) == n
        for o, n in changed)
    check("A12 diff touches ONLY the status flip, lines count unchanged",
          len(new) == len(orig) and len(changed) == 3 and only_status,
          f"{len(changed)} lines changed")

    print(f"\n{14} guards run, {len(FAILURES)} failed"
          + (f": {FAILURES}" if FAILURES else ""))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
