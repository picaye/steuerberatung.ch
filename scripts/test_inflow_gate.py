#!/usr/bin/env python3
"""test_inflow_gate.py — regression guards for scripts/inflow_gate.py
(t_376b7fb7 cap gate; t_e0dbafb1 second gate: calendar saturation;
 t_e0dbafb1 third gate 2026-11-27: cto hard-suspend floor PENDING_SUSPEND_FLOOR=60).

Guards under test:
  G1  below the suspend floor + free Fridays -> {"pending": N<60, "gated": false,
      "gate_reason": null}, exit 0 (normal research behaviour untouched).
      (Was `cap - 1` pre-floor; the cto floor now closes that band by design.)
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
      ONLY the count-based caps gate (pending_cap, and the suspend floor per
      G26) — a planner bug never freezes the saturation half of inflow.
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
        [sys.executable, str(SCRIPT), "--file", str(queue_path),
         "--state-file", str(Path(tempfile.mkdtemp()) / "run_gate.state.json")],
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
    floor = gate.PENDING_SUSPEND_FLOOR
    check("G7c PENDING_SUSPEND_FLOOR constant is 60 and below cap",
          floor == 60 and floor < cap, f"got {floor}")

    # G1 below the suspend floor (fresh temp queue pins nothing -> free
    # Fridays > 0). t_e0dbafb1 floor: was `cap - 1` (99) — that band is now
    # gated by design; see G24-G26.
    q = write_queue([card(f"s{i}", "pending") for i in range(floor - 1)])
    proc, out = run_gate(q)
    check("G1 below floor + free calendar: not gated, exit 0",
          out["pending"] == floor - 1 and out["cap"] == cap
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

    # G7b stdout contract: exactly one JSON object. t_ae7d83c3 extends the
    # schema with severity/saturation_days/ossified; t_e0dbafb1 floor adds
    # suspend_floor; original keys preserved.
    proc, out = run_gate(write_queue([card("x", "pending")]))
    check("G7b stdout keys are exactly pending/cap/suspend_floor/gated/"
          "free_fridays/gate_reason/severity/saturation_days/ossified",
          proc.stdout.strip().startswith("{")
          and proc.stdout.strip().endswith("}")
          and set(out) == {"pending", "cap", "suspend_floor", "gated",
                           "free_fridays", "gate_reason", "severity",
                           "saturation_days", "ossified"}
          and proc.stdout.strip().count("\n") == 0,
          f"stdout={proc.stdout!r}")
    check("G7b original keys keep their pre-t_ae7d83c3 types/values",
          isinstance(out["pending"], int) and out["cap"] == gate.PENDING_CAP
          and isinstance(out["gated"], bool)
          and out["gate_reason"] in (None, "pending_cap", "cto_suspend",
                                     "no_free_fridays"),
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
            rc = gate.main(["--file", str(write_queue([card("only1", "pending")])),
                            "--state-file", str(Path(tempfile.mkdtemp()) / "g8.state.json")])
        payload = json.loads(buf_out.getvalue())
        check("G8 pending<cap + 0 free Fridays: gated, rc 3, reason no_free_fridays",
              rc == 3 and payload["gated"] is True
              and payload["gate_reason"] == "no_free_fridays"
              and payload["pending"] == 1
              and payload["severity"] == "AMBER",
              f"rc={rc} {payload}")
        check("G8 gated run prints GATED decision line to stderr",
              "GATED" in buf_err.getvalue(), f"stderr={buf_err.getvalue()!r}")

        # G11 precedence: pending over cap AND saturated -> pending_cap
        q11 = write_queue([card(f"s{i}", "pending") for i in range(cap + 5)])
        buf_out, buf_err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
            rc = gate.main(["--file", str(q11),
                            "--state-file", str(Path(tempfile.mkdtemp()) / "g11.state.json")])
        payload = json.loads(buf_out.getvalue())
        check("G11 both gates closed: reason is pending_cap",
              rc == 3 and payload["gate_reason"] == "pending_cap"
              and payload["severity"] == "RED",
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
                rc = gate.main(["--file", str(write_queue([card("x", "pending")])),
                                "--state-file", str(Path(tempfile.mkdtemp()) / "g10.state.json")])
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
                rc = gate.main(["--file", str(q11),
                                "--state-file", str(Path(tempfile.mkdtemp()) / "g10b.state.json")])
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

    # ---- G12-G23: severity split + anti-ossification tripwire (t_ae7d83c3)
    # Alerting interpretation ONLY: exit codes and append-blocking from G1-G11
    # must not move. Severity ladder (worst-gate-governs): RED > AMBER > GREEN.
    def days_ago(n):
        return (datetime.date.today() - datetime.timedelta(days=n)).isoformat()

    def seed_state(path, since, last=None):
        path.write_text(json.dumps({
            "saturation_since": since,
            "consecutive_days": 0,  # recomputed from dates; ignored on read
            "last_seen": last or datetime.date.today().isoformat(),
        }), encoding="utf-8")
        return path

    def sat_queue(name, extra_plain=0):
        """Saturated calendar fixture (pins every open Friday -> free==0)
        plus `extra_plain` unpinned pending fillers."""
        lines = [json.dumps(c) for c in saturated]
        lines += [card(f"{name}-fill{i}", "pending") for i in range(extra_plain)]
        return write_queue(lines)

    def run_gate_q(queue_path, state_path):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--file", str(queue_path),
             "--state-file", str(state_path)],
            capture_output=True, text=True)
        return proc, json.loads(proc.stdout)

    def state_of(path):
        return json.loads(path.read_text(encoding="utf-8"))

    from pathlib import Path as _P

    # ---- G12: saturation -> AMBER, counter advances in the REPORT only.
    q = sat_queue("g12")
    st = seed_state(_P(tempfile.mkdtemp()) / "g12.state.json", days_ago(2))
    proc, out = run_gate_q(q, st)
    check("G12 saturation stays gated (exit 3) — behavior unchanged",
          proc.returncode == 3 and out.get("gated") is True, str(out))
    check("G12 saturation severity is AMBER, not RED",
          out.get("severity") == "AMBER" and out.get("ossified") is False,
          str(out))
    check("G12 saturation counter reports day 3 of streak",
          out.get("saturation_days") == 3, str(out))
    check("G12 counter persisted across runs",
          state_of(st).get("consecutive_days") == 3
          and state_of(st).get("saturation_since") == days_ago(2),
          st.read_text(encoding="utf-8").strip())
    _, out_b = run_gate_q(q, st)
    check("G12 same-day repeat run does not double-count",
          out_b.get("saturation_days") == 3, str(out_b))

    # ---- G13: cap-breach -> RED (actionable, unchanged)
    q = write_queue([card(f"g13-{i}", "pending") for i in range(gate.PENDING_CAP)])
    st = seed_state(_P(tempfile.mkdtemp()) / "g13.state.json", days_ago(9))
    proc, out = run_gate_q(q, st)
    check("G13 cap-breach severity is RED",
          proc.returncode == 3 and out.get("gate_reason") == "pending_cap"
          and out.get("severity") == "RED", str(out))
    check("G13 cap-breach with healthy calendar resets streak",
          state_of(st).get("consecutive_days") == 0,
          st.read_text(encoding="utf-8").strip())

    # ---- G14: healthy -> GREEN + tripwire counter RESETS
    q = write_queue([card("g14-0", "pending")])
    st = seed_state(_P(tempfile.mkdtemp()) / "g14.state.json", days_ago(5))
    proc, out = run_gate_q(q, st)
    check("G14 healthy state: rc 0, severity GREEN",
          proc.returncode == 0 and out.get("severity") == "GREEN", str(out))
    check("G14 non-saturating observation resets persisted counter",
          state_of(st).get("consecutive_days") == 0
          and state_of(st).get("saturation_since") is None,
          st.read_text(encoding="utf-8").strip())

    # ---- G15: >14 consecutive saturation days -> RED saturation-ossified
    st = seed_state(_P(tempfile.mkdtemp()) / "g15.state.json", days_ago(15))
    proc, out = run_gate_q(sat_queue("g15"), st)
    check("G15 day-16 saturation escalates to RED (exit 3 unchanged)",
          proc.returncode == 3 and out.get("severity") == "RED", str(out))
    check("G15 escalation flags ossified + carries the streak",
          out.get("ossified") is True and out.get("saturation_days") == 16,
          str(out))
    check("G15 escalation reason visible in stderr",
          "gate_reason=saturation-ossified" in proc.stderr
          and "ESCALATE" in proc.stderr, proc.stderr.strip())

    # ---- G15b: exactly 14-day streak is still AMBER (grace is inclusive)
    st = seed_state(_P(tempfile.mkdtemp()) / "g15b.state.json", days_ago(13))
    _, out = run_gate_q(sat_queue("g15b"), st)
    check("G15b day-14 saturation still AMBER (escalates only past 14)",
          out.get("severity") == "AMBER" and out.get("saturation_days") == 14
          and out.get("ossified") is False, str(out))

    # ---- G16: cap-breach while saturated must NOT reset the streak
    q = sat_queue("g16", extra_plain=gate.PENDING_CAP - len(saturated) + 1)
    st = seed_state(_P(tempfile.mkdtemp()) / "g16.state.json", days_ago(6))
    _, out = run_gate_q(q, st)
    check("G16 cap-breach day keeps severity RED but calendar streak persists",
          out.get("severity") == "RED"
          and state_of(st).get("consecutive_days") == 7,
          str(out) + " " + st.read_text(encoding="utf-8").strip())

    # ---- G17: calendar read failure leaves counter untouched, reports streak
    st = seed_state(_P(tempfile.mkdtemp()) / "g17.state.json", days_ago(4))
    before = state_of(st)
    days_read, since_read = gate.update_saturation_state(str(st), None)
    check("G17 failed calendar read neither resets nor advances persisted state",
          state_of(st) == before, st.read_text(encoding="utf-8").strip())
    check("G17 failed read still reports the elapsed streak",
          days_read == 5 and since_read == before["saturation_since"],
          str((days_read, since_read)))

    # ---- G18: skipped cron runs still advance the streak (calendar days)
    st = seed_state(_P(tempfile.mkdtemp()) / "g18.state.json",
                    days_ago(9), last=days_ago(4))
    _, out = run_gate_q(sat_queue("g18"), st)
    check("G18 gap between runs advances by calendar days",
          out.get("saturation_days") == 10, str(out))

    # ---- G19: severity ladder governs overall (worst-gate contract)
    check("G19 severity ladder RED > AMBER > GREEN",
          gate.SEVERITY_RANK["RED"] > gate.SEVERITY_RANK["AMBER"]
          > gate.SEVERITY_RANK["GREEN"], str(gate.SEVERITY_RANK))

    # ---- G20/G21: headline carries the binding gate_reason; no flattening.
    # t_e0dbafb1 floor: a fully-saturated real grid pins ~84 Fridays, so the
    # queue sits above the suspend floor and the reported reason is
    # cto_suspend (floor outranks the calendar). The no_free_fridays
    # headline itself is guarded by G8 (below-floor queue).
    q = sat_queue("g20")
    st = _P(tempfile.mkdtemp()) / "g20.state.json"
    proc, out = run_gate_q(q, st)
    check("G20 saturating run at/above floor reports gate_reason=cto_suspend + AMBER",
          out.get("gate_reason") == "cto_suspend"
          and out.get("severity") == "AMBER"
          and out.get("free_fridays") == 0
          and "gate_reason=cto_suspend" in proc.stderr, str(out))
    check("G21 AMBER never flattened: gated implies severity != GREEN",
          out.get("gated") is True and out.get("severity") != "GREEN", str(out))

    # ---- G22: append-blocking is unchanged under AMBER (dry-run +5)
    # The gate refusing (exit 3) before AND after +5 unpinned appends is what
    # keeps the drain hook from publishing them; severity split must not move
    # that answer.
    st = seed_state(_P(tempfile.mkdtemp()) / "g22.state.json", days_ago(1))
    proc, out = run_gate_q(sat_queue("g22a"), st)
    check("G22 pre-append saturated gate blocks (AMBER, exit 3)",
          proc.returncode == 3 and out.get("severity") == "AMBER", str(out))
    proc, out = run_gate_q(sat_queue("g22b", extra_plain=5), st)
    check("G22 +5 appends while saturated still refused (exit 3, still AMBER)",
          proc.returncode == 3 and out.get("severity") == "AMBER"
          and out.get("saturation_days") == 2, str(out))

    # ---- G23: missing state file on a saturating day starts the streak at 1
    st = _P(tempfile.mkdtemp()) / "missing" / "state.json"
    proc, out = run_gate_q(sat_queue("g23"), st)
    check("G23 fresh streak starts at day 1 AMBER and creates state file",
          out.get("saturation_days") == 1 and out.get("severity") == "AMBER"
          and st.exists(), str(out))

    # ---- G24-G26: cto hard-suspend floor (t_e0dbafb1, 2026-11-27) ----
    # G24: at the floor with a FULLY OPEN calendar -> gated. The whole point
    # of the directive: adds stop at pending >= 60, not 100. AMBER (a
    # standing directive being executed is not an incident), not ossified.
    q = write_queue([card(f"g24-{i}", "pending") for i in range(floor)])
    proc, out = run_gate_q(q, _P(tempfile.mkdtemp()) / "g24.state.json")
    check("G24 pending == floor, open calendar: gated cto_suspend rc 3 AMBER",
          proc.returncode == 3 and out.get("gated") is True
          and out.get("gate_reason") == "cto_suspend"
          and out.get("severity") == "AMBER"
          and out.get("ossified") is False
          and out.get("free_fridays", 0) > 0
          and out.get("suspend_floor") == floor, str(out))
    check("G24 stderr names the cto directive + the resume condition",
          "gate_reason=cto_suspend" in proc.stderr
          and "no research adds until pending < 60" in proc.stderr,
          proc.stderr.strip())

    # G25: floor outranks no_free_fridays when both hold (in-process so the
    # calendar can be monkeypatched; pending=99 < cap keeps it out of
    # pending_cap). free_fridays stays observable in the JSON.
    saved = gate.count_free_fridays
    gate.count_free_fridays = lambda cards, today=None: 0
    try:
        buf_out, buf_err = io.StringIO(), io.StringIO()
        q99 = write_queue([card(f"g25-{i}", "pending") for i in range(cap - 1)])
        with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
            rc = gate.main(["--file", str(q99),
                            "--state-file",
                            str(_P(tempfile.mkdtemp()) / "g25.state.json")])
        payload = json.loads(buf_out.getvalue())
        check("G25 floor band + saturated grid: reason cto_suspend (priority), "
              "AMBER day 1, free_fridays still reported 0",
              rc == 3 and payload["gate_reason"] == "cto_suspend"
              and payload["free_fridays"] == 0
              and payload["severity"] == "AMBER", f"rc={rc} {payload}")
    finally:
        gate.count_free_fridays = saved

    # G26: the floor is calendar-INDEPENDENT — a planner outage does not
    # reopen the gate for a queue at/above 60. Fail-open (G10/G10b) exempts
    # only the saturation half; below the floor G10 still fails open.
    broken = types.ModuleType("publish_calendar")
    def _boom26(*a, **k):
        raise RuntimeError("planner exploded")
    broken.plan = _boom26
    broken.fridays = _boom26
    saved_mod = sys.modules.get("publish_calendar")
    sys.modules["publish_calendar"] = broken
    try:
        buf_out, buf_err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
            rc = gate.main(["--file", str(write_queue(
                [card(f"g26-{i}", "pending") for i in range(floor + 10)])),
                "--state-file",
                str(_P(tempfile.mkdtemp()) / "g26.state.json")])
        payload = json.loads(buf_out.getvalue())
        check("G26 calendar outage + pending >= floor: still gated via floor "
              "(cto_suspend, free_fridays null)",
              rc == 3 and payload["gate_reason"] == "cto_suspend"
              and payload["free_fridays"] is None
              and payload["severity"] == "AMBER", f"rc={rc} {payload}")
    finally:
        sys.modules["publish_calendar"] = saved_mod

    print(f"\n{CHECKS} guards run, {len(FAILURES)} failed"
          + (f": {FAILURES}" if FAILURES else ""))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
