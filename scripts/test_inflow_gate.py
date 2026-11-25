#!/usr/bin/env python3
"""test_inflow_gate.py — regression guards for scripts/inflow_gate.py
(t_376b7fb7 cap gate; t_e0dbafb1 second gate: calendar saturation).

Guards under test:
  G1  below cap + free Fridays -> {"pending": N<100, "gated": false,
      "gate_reason": null}, exit 0 (normal research behaviour untouched).
  G2  exactly at cap (pending == PENDING_CAP) -> gated, exit 3, reason
      pending_cap. The cap is inclusive: cron contract `pending=N >= cap=100`.
  G3  above cap -> gated, exit 3.
  G4  only status=="pending" counts — published/superseded/backlog cards
      excluded; event lines (no slug/status pair) ignored.
  G5  missing queue file -> {"pending": 0, "gated": false}, exit 0.
  G6  malformed lines tolerated validate_queue-style (skip + stderr warning).
  G7  contract stability: stdout is exactly one JSON object with keys
      pending/cap/gated/free_fridays/gate_reason; cap == PENDING_CAP.
  G8  SECOND GATE (t_e0dbafb1): pending < cap but ZERO free Fridays from
      today to horizon -> gated, exit 3, reason no_free_fridays. This kills
      the add↔drain churn: the STEP 0' auto-drain can reopen the pending cap,
      but with a saturated Friday grid the gate stays closed.
  G9  free-Friday counting mirrors publish_calendar --free exactly (uses
      pc.fridays(), counts slots not in plan() output and >= today).
  G10 fail-open: if the calendar cannot be computed (free_fridays null),
      ONLY the pending cap gates — a planner bug never freezes inflow.
  G11 precedence: both conditions true -> gate_reason is pending_cap.

    python3 scripts/test_inflow_gate.py

Exit 0 = every guard holds; exit 1 = a guard regressed.
"""
from __future__ import annotations

import contextlib
import datetime
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import types
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "inflow_gate.py"
sys.path.insert(0, str(REPO / "scripts"))
import publish_calendar as pc  # noqa: E402

FAILURES: list[str] = []
CHECKS = 0


def check(name: str, cond: bool, detail: str = ""):
    global CHECKS
    CHECKS += 1
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


def card(slug: str, status: str, hold_until=None) -> str:
    return json.dumps({"date": "2026-10-28", "slug": slug, "title": slug,
                       "meta": "", "demand": 1, "facts": [],
                       "status": status, "hold_until": hold_until})


def write_queue(lines):
    tmp = Path(tempfile.mkdtemp()) / "content-research.jsonl"
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return tmp


def saturated_cards():
    """Pending cards pinning EVERY Friday slot from today to horizon — the
    live 2026-11-25 state (grid full to 2028)."""
    today = datetime.date.today()
    return [json.loads(card(f"pin{i}", "pending", s.isoformat()))
            for i, s in enumerate(pc.fridays()) if s >= today]


def main():
    gate = load_gate()
    cap = gate.PENDING_CAP
    check("G7a PENDING_CAP constant is 100", cap == 100, f"got {cap}")

    # G1 below cap (fresh temp queue pins nothing -> free Fridays > 0)
    q = write_queue([card(f"s{i}", "pending") for i in range(cap - 1)])
    proc, out = run_gate(q)
    check("G1 below cap + free calendar: not gated, exit 0",
          out["pending"] == cap - 1 and out["cap"] == cap
          and out["gated"] is False and out["gate_reason"] is None
          and out["free_fridays"] > 0
          and proc.returncode == 0, f"{out} rc={proc.returncode}")

    # G2 exactly at cap (inclusive)
    q = write_queue([card(f"s{i}", "pending") for i in range(cap)])
    proc, out = run_gate(q)
    check("G2 at cap: gated, exit 3, reason pending_cap",
          out["pending"] == cap and out["gated"] is True
          and out["gate_reason"] == "pending_cap"
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
        + [card(f"bl{i}", "backlog") for i in range(20)]
        + [json.dumps({"type": "recommendation", "text": "event line, no slug"}),
           json.dumps({"date": "2026-10-20"})]  # status-less record
    )
    proc, out = run_gate(write_queue(lines))
    check("G4 published/superseded/backlog/event lines excluded",
          out["pending"] == 5 and out["gated"] is False
          and proc.returncode == 0, f"{out} rc={proc.returncode}")

    # G5 missing file
    proc, out = run_gate(Path(tempfile.mkdtemp()) / "absent.jsonl")
    check("G5 missing file: pending 0, not gated, exit 0",
          out["pending"] == 0 and out["gated"] is False
          and out["gate_reason"] is None
          and proc.returncode == 0, f"{out} rc={proc.returncode}")

    # G6 malformed lines tolerated (validate_queue-style skip, no crash)
    good = [card(f"s{i}", "pending") for i in range(3)]
    q = write_queue(good[:1] + ["{not json at all", "[1,2,3]"]
                    + good[1:2] + [""] + good[2:])
    proc, out = run_gate(q)
    check("G6 malformed lines skipped, valid cards still counted",
          out["pending"] == 3 and out["gated"] is False
          and proc.returncode == 0
          and "line 2" in proc.stderr, f"{out} rc={proc.returncode} stderr={proc.stderr!r}")

    # G7b stdout contract: exactly one JSON object, keys fixed
    proc, out = run_gate(write_queue([card("x", "pending")]))
    check("G7b stdout keys are exactly pending/cap/gated/free_fridays/gate_reason",
          proc.stdout.strip().startswith("{")
          and proc.stdout.strip().endswith("}")
          and set(out) == {"pending", "cap", "gated", "free_fridays", "gate_reason"}
          and proc.stdout.strip().count("\n") == 0,
          f"stdout={proc.stdout!r}")

    # G8 second gate: saturated grid, pending well below cap -> gated
    saturated = saturated_cards()
    check("G8 setup: saturation fixture pins > 0 Fridays", len(saturated) > 0,
          f"got {len(saturated)} pin cards")
    saved = gate.count_free_fridays
    try:
        gate.count_free_fridays = lambda cards, today=None: 0
        buf_out, buf_err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
            rc = gate.main(["--file", str(write_queue([card("only1", "pending")]))])
        payload = json.loads(buf_out.getvalue())
        check("G8 pending<cap + 0 free Fridays: gated, rc 3, reason no_free_fridays",
              rc == 3 and payload["gated"] is True
              and payload["gate_reason"] == "no_free_fridays"
              and payload["pending"] == 1,
              f"rc={rc} {payload}")
        check("G8 gated run prints GATED decision line to stderr",
              "GATED" in buf_err.getvalue(), f"stderr={buf_err.getvalue()!r}")

        # G11 precedence: pending over cap AND saturated -> pending_cap
        q11 = write_queue([card(f"s{i}", "pending") for i in range(cap + 5)])
        buf_out, buf_err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
            rc = gate.main(["--file", str(q11)])
        payload = json.loads(buf_out.getvalue())
        check("G11 both gates closed: reason is pending_cap",
              rc == 3 and payload["gate_reason"] == "pending_cap",
              f"rc={rc} {payload}")

        # G10 fail-open: calendar unavailable -> cap alone gates. Simulate
        # an unavailable planner by poisoning the publish_calendar module
        # the gate imports inside count_free_fridays (NOT the function —
        # the fail-open must come from inside its own try/except).
        gate.count_free_fridays = saved
        broken = types.ModuleType("publish_calendar")
        def _boom(*a, **k):
            raise RuntimeError("planner exploded")
        broken.plan = _boom
        broken.fridays = _boom
        saved_mod = sys.modules.get("publish_calendar")
        sys.modules["publish_calendar"] = broken
        try:
            buf_out, buf_err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                rc = gate.main(["--file", str(write_queue([card("x", "pending")]))])
            payload = json.loads(buf_out.getvalue())
            check("G10 calendar failure + pending<cap: NOT gated (fail-open), rc 0",
                  rc == 0 and payload["gated"] is False
                  and payload["free_fridays"] is None
                  and payload["gate_reason"] is None,
                  f"rc={rc} {payload}")
            check("G10a fail-open prints stderr WARN",
                  "WARN" in buf_err.getvalue(), f"stderr={buf_err.getvalue()!r}")
            buf_out, buf_err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                rc = gate.main(["--file", str(q11)])
            payload = json.loads(buf_out.getvalue())
            check("G10b calendar failure + pending>=cap: still gated via cap",
                  rc == 3 and payload["gate_reason"] == "pending_cap",
                  f"rc={rc} {payload}")
        finally:
            sys.modules["publish_calendar"] = saved_mod
    finally:
        gate.count_free_fridays = saved

    # G9 free-count parity with publish_calendar --free on the SAME file
    # (real computation, no monkeypatching): saturated fixture -> 0
    q9 = write_queue([json.dumps(c) for c in saturated])
    n_direct = gate.count_free_fridays(gate.read_cards(q9))
    check("G9 saturated fixture computes free_fridays == 0 via real planner",
          n_direct == 0, f"got {n_direct}")
    proc, out9 = run_gate(q9)
    # pending here is len(saturated); gated either way — assert the calendar field
    check("G9b end-to-end on saturated fixture: free_fridays 0 and gated rc 3",
          out9["free_fridays"] == 0 and out9["gated"] is True
          and proc.returncode == 3, f"{out9} rc={proc.returncode}")

    print(f"\n{CHECKS} guards run, {len(FAILURES)} failed"
          + (f": {FAILURES}" if FAILURES else ""))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
