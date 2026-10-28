#!/usr/bin/env python3
"""test_inflow_gate.py — regression guards for scripts/inflow_gate.py (t_376b7fb7).

Guards under test:
  G1  below cap -> {"pending": N<100, "gated": false}, exit 0 (normal
      research behaviour must be untouched).
  G2  exactly at cap (pending == PENDING_CAP) -> gated, exit 3. The cap is
      inclusive: the cron log line contract is `pending=N >= cap=100`.
  G3  above cap -> gated, exit 3 (the live queue sits here: 200 pending).
  G4  only status=="pending" counts — published and superseded cards are
      excluded; event lines (no slug/status pair) are ignored.
  G5  missing queue file -> {"pending": 0, "gated": false}, exit 0 (a fresh
      checkout must never trip the gate).
  G6  malformed lines are tolerated validate_queue-style: invalid JSON /
      non-object lines are skipped with a warning, valid cards still count,
      exit code reflects only the pending count.
  G7  contract stability: stdout is exactly one JSON object with keys
      pending/cap/gated and cap == the module constant PENDING_CAP.

    python3 scripts/test_inflow_gate.py

Exit 0 = every guard holds; exit 1 = a guard regressed.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "inflow_gate.py"

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = ""):
    status = "ok" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def load_gate():
    spec = importlib.util.spec_from_file_location("inflow_gate", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_gate(queue_path: Path):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--file", str(queue_path)],
        capture_output=True, text=True,
    )
    payload = json.loads(proc.stdout)
    return proc, payload


def card(slug: str, status: str) -> str:
    return json.dumps({"date": "2026-10-28", "slug": slug, "title": slug,
                       "meta": "", "demand": 1, "facts": [], "status": status})


def write_queue(lines):
    tmp = Path(tempfile.mkdtemp()) / "content-research.jsonl"
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return tmp


def main():
    gate = load_gate()
    cap = gate.PENDING_CAP
    check("G7a PENDING_CAP constant is 100", cap == 100, f"got {cap}")

    # G1 below cap
    q = write_queue([card(f"s{i}", "pending") for i in range(cap - 1)])
    proc, out = run_gate(q)
    check("G1 below cap: not gated, exit 0",
          out == {"pending": cap - 1, "cap": cap, "gated": False}
          and proc.returncode == 0, f"{out} rc={proc.returncode}")

    # G2 exactly at cap (inclusive)
    q = write_queue([card(f"s{i}", "pending") for i in range(cap)])
    proc, out = run_gate(q)
    check("G2 at cap: gated, exit 3",
          out == {"pending": cap, "cap": cap, "gated": True}
          and proc.returncode == 3, f"{out} rc={proc.returncode}")

    # G3 above cap
    q = write_queue([card(f"s{i}", "pending") for i in range(cap + 100)])
    proc, out = run_gate(q)
    check("G3 above cap: gated, exit 3",
          out["pending"] == cap + 100 and out["gated"] is True
          and proc.returncode == 3, f"{out} rc={proc.returncode}")

    # G4 status filtering: only pending counts
    lines = (
        [card(f"p{i}", "pending") for i in range(5)]
        + [card(f"pub{i}", "published") for i in range(20)]
        + [card(f"sup{i}", "superseded") for i in range(20)]
        + [json.dumps({"type": "recommendation", "text": "event line, no slug"}),
           json.dumps({"date": "2026-10-20"})]  # status-less record
    )
    proc, out = run_gate(write_queue(lines))
    check("G4 published/superseded/event lines excluded",
          out == {"pending": 5, "cap": cap, "gated": False}
          and proc.returncode == 0, f"{out} rc={proc.returncode}")

    # G5 missing file
    proc, out = run_gate(Path(tempfile.mkdtemp()) / "absent.jsonl")
    check("G5 missing file: pending 0, not gated, exit 0",
          out == {"pending": 0, "cap": cap, "gated": False}
          and proc.returncode == 0, f"{out} rc={proc.returncode}")

    # G6 malformed lines tolerated (validate_queue-style skip, no crash)
    good = [card(f"s{i}", "pending") for i in range(3)]
    q = write_queue(good[:1] + ["{not json at all", "[1,2,3]"]
                    + good[1:2] + [""] + good[2:])
    proc, out = run_gate(q)
    check("G6 malformed lines skipped, valid cards still counted",
          out == {"pending": 3, "cap": cap, "gated": False}
          and proc.returncode == 0
          and "line 2" in proc.stderr, f"{out} rc={proc.returncode} stderr={proc.stderr!r}")

    # G7b stdout contract: exactly one JSON object, keys fixed
    proc, out = run_gate(write_queue([card("x", "pending")]))
    check("G7b stdout is one JSON object with keys pending/cap/gated",
          proc.stdout.strip().startswith("{")
          and proc.stdout.strip().endswith("}")
          and set(out) == {"pending", "cap", "gated"}
          and proc.stdout.strip().count("\n") == 0,
          f"stdout={proc.stdout!r}")

    print(f"\n{7 + 1} guards run, {len(FAILURES)} failed"
          + (f": {FAILURES}" if FAILURES else ""))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
