#!/usr/bin/env python3
"""test_publish_picker.py — regression guards for the t_4fa4b841 pins gate.

Incident replayed: topic arbeitgeber-3a-beitrag-lohnausweis was FIXED-pinned
for 2026-12-11 (publish_calendar.py @ 7998b4b, 2026-10-21) but the daily
publish cron shipped it Fri 2026-11-13 (bdb388b) — four weeks early — because
the picker consulted only the queue-side hold_until (which had drifted to the
publish day) and never the script-side FIXED dict, so validate_queue rule 5
(jsonl-only) saw nothing.

Guards (a synthetic calendar fixture via --calendar pins every date; the
picker reads FIXED + PREP_WINDOW_DAYS from it exactly like the real one):
  G1  THE INCIDENT: a card FIXED for slot Friday, run date 4 weeks earlier,
      is NOT picked — it lands in `blocked` and never in `eligible`.
  G2  week N-1 boundary: run on slot-7d (the preceding Friday) -> admitted
      (that is the prep window); run on slot-14d -> still blocked.
      This is the exact acceptance line.
  G3  in-window publish works unchanged: mark_published flips a FIXED card
      stamped on its slot day, exit 0, published_at lands.
  G4  binding slot = LATEST pin source: drifted jsonl hold_until (past day)
      cannot launder a future FIXED slot; drift is also reported.
  G5  unpinned pending cards stay selectable, demand-ordered (high>medium>
      low>unknown), oldest-first within equal demand.
  G6  admitted pinned cards outrank unpinned ones (earliest slot first).
  G7  mark_published REFUSES a FIXED card whose slot is > PREP_WINDOW_DAYS
      after the stamp (bdb388b shape), file byte-identical after refusal.
  G8  slot_override is the only escape and lifts G7 (human call).
  G9  a card NOT in FIXED is never gated by mark_published (R-suite compat);
      and jsonl-only pins keep their existing breach-evidence flow.
  G10 --check exit codes: selectable 0 / future-pin 3 / unknown slug 1.
  G11 non-article records and non-pending statuses never appear in output.
  G12 malformed date sources warn and are skipped, never crash the picker.

    python3 scripts/test_publish_picker.py

Exit 0 = every guard holds; exit 1 = a guard regressed.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PICKER = REPO / "scripts" / "publish_picker.py"
MARKER = REPO / "scripts" / "mark_published.py"

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = ""):
    status = "ok" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


# --- synthetic calendar -----------------------------------------------------
# Mirrors the real publish_calendar.py surface the picker/gate consume.
CAL = '''GRID_START = __import__("datetime").date(2026, 10, 23)
HORIZON_END = __import__("datetime").date(2029, 1, 1)
PREP_WINDOW_DAYS = 7
FIXED = {
    "incident-topic": "2026-12-11",
    "clean-pin": "2026-12-11",
}
DEADLINE = {}
'''

# --- card fixtures -----------------------------------------------------------


def card(slug, demand="medium", date="2026-10-01", hold_until=None,
         status="pending", ptype="article", **extra):
    rec = {"date": date, "slug": slug, "title": slug, "meta": "m",
           "facts": [], "status": status}
    if ptype is not None:
        rec["type"] = ptype
    if demand is not None:
        rec["demand"] = demand
    if hold_until is not None:
        rec["hold_until"] = hold_until
        rec["priority"] = f"pin-{hold_until}"
    rec.update(extra)
    return json.dumps(rec, ensure_ascii=False)


def run_picker(q: Path, cal: Path, today: str, extra=None):
    cmd = [sys.executable, str(PICKER), "--queue", str(q),
           "--calendar", str(cal), "--today", today]
    r = subprocess.run(cmd + (extra or []), capture_output=True, text=True)
    out = json.loads(r.stdout) if r.stdout.strip() else {}
    return r, out


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cal = tmp / "cal.py"
        cal.write_text(CAL)

        # G1/G4: the incident — FIXED 2026-12-11, drifted past hold_until,
        # run four weeks early.
        q = tmp / "g1.jsonl"
        q.write_text("\n".join([
            card("incident-topic", demand="high",
                 hold_until="2026-11-13"),  # drifted to the publish day
            card("hot-unpinned", demand="high", date="2026-09-15"),
        ]) + "\n")
        r, out = run_picker(q, cal, "2026-11-13")
        elig = {e["slug"] for e in out["eligible"]}
        blocked = {e["slug"]: e for e in out["blocked"]}
        check("G1 incident run: FIXED-pinned card not picked",
              "incident-topic" not in elig and "incident-topic" in blocked,
              f"eligible={elig} blocked={list(blocked)}")
        check("G1 binding slot is the FIXED date, not the drifted one",
              blocked.get("incident-topic", {}).get("slot") == "2026-12-11",
              str(blocked.get("incident-topic")))
        check("G1 the unpinned card still gets published",
              out.get("pick", {}).get("slug") == "hot-unpinned",
              str(out.get("pick")))
        check("G4 drift reported when pin sources disagree",
              any("drift" in w and "incident-topic" in w
                  for w in out["warnings"]),
              str(out["warnings"]))

        # G2: prep-window boundary (acceptance line: week N-1 Friday).
        q2 = tmp / "g2.jsonl"
        q2.write_text(card("clean-pin", demand="medium") + "\n")
        r, out = run_picker(q2, cal, "2026-11-27")  # slot-14d -> blocked
        check("G2 run at slot-14d: still blocked",
              not out["eligible"] and out["pick"] is None,
              str(out.get("pick")))
        r, out = run_picker(q2, cal, "2026-12-04")  # slot-7d -> admitted
        check("G2 run at slot-7d (week N-1 prep window): admitted",
              out.get("pick", {}).get("slug") == "clean-pin",
              str(out.get("pick")))

        # G3: in-window publish unchanged — flip on the slot day works.
        q3 = tmp / "g3.jsonl"
        q3.write_text(card("clean-pin", demand="medium",
                           hold_until="2026-12-11") + "\n")
        r = subprocess.run(
            [sys.executable, str(MARKER), "clean-pin", "--langs", "de,en",
             "--file", str(q3), "--calendar", str(cal), "--no-validate",
             "--published-at", "2026-12-11"],
            capture_output=True, text=True)
        rec3 = json.loads(q3.read_text().splitlines()[0])
        check("G3 slot-day flip passes the gate",
              r.returncode == 0 and rec3["status"] == "published"
              and rec3["published_at"] == "2026-12-11",
              r.stdout + r.stderr)

        # G7/G8: writer gate + slot_override escape.
        q4 = tmp / "g4.jsonl"
        q4.write_text(card("incident-topic", demand="high",
                           hold_until="2026-11-13") + "\n")
        before = q4.read_bytes()
        r = subprocess.run(
            [sys.executable, str(MARKER), "incident-topic", "--langs", "de",
             "--file", str(q4), "--calendar", str(cal), "--no-validate",
             "--published-at", "2026-11-13"],
            capture_output=True, text=True)
        check("G7 bdb388b shape REFUSED at the writer",
              r.returncode == 1 and "REFUSED" in r.stderr, r.stderr)
        check("G7 refused write leaves the queue byte-identical",
              q4.read_bytes() == before)

        q5 = tmp / "g5.jsonl"
        q5.write_text(card("incident-topic", demand="high",
                           slot_override="founder ruling t_x") + "\n")
        r = subprocess.run(
            [sys.executable, str(MARKER), "incident-topic", "--langs", "de",
             "--file", str(q5), "--calendar", str(cal), "--no-validate",
             "--published-at", "2026-11-13"],
            capture_output=True, text=True)
        check("G8 slot_override lifts the gate (human call)",
              r.returncode == 0, r.stdout + r.stderr)

        # G9: unpinned card never gated; jsonl-only drift keeps old flow.
        q6 = tmp / "g6.jsonl"
        q6.write_text(card("free-topic", demand="high",
                           hold_until="2026-12-18") + "\n")
        r = subprocess.run(
            [sys.executable, str(MARKER), "free-topic", "--langs", "de",
             "--file", str(q6), "--calendar", str(cal), "--no-validate",
             "--published-at", "2026-11-13"],
            capture_output=True, text=True)
        rec6 = json.loads(q6.read_text().splitlines()[0])
        check("G9 non-FIXED card not gated; future hold_until survives "
              "as rule-5 evidence (existing flow unchanged)",
              r.returncode == 0 and rec6.get("hold_until") == "2026-12-18",
              r.stdout + r.stderr)

        # G5: demand ordering + oldest-first tie-break among unpinned.
        q7 = tmp / "g7.jsonl"
        q7.write_text("\n".join([
            card("late-low", demand="low", date="2026-08-01"),
            card("old-high", demand="high", date="2026-06-01"),
            card("new-high", demand="high", date="2026-09-01"),
            card("no-demand", demand=None, date="2026-01-01"),
        ]) + "\n")
        r, out = run_picker(q7, cal, "2026-11-13")
        order = [e["slug"] for e in out["eligible"]]
        check("G5 unpinned order high(oldest)>high>low>unknown",
              order == ["old-high", "new-high", "late-low", "no-demand"],
              str(order))

        # G6: admitted pinned outranks unpinned high-demand.
        q8 = tmp / "g8.jsonl"
        q8.write_text("\n".join([
            card("clean-pin", demand="low", hold_until="2026-12-11"),
            card("hot-unpinned", demand="high", date="2026-12-01"),
        ]) + "\n")
        r, out = run_picker(q8, cal, "2026-12-11")
        check("G6 pinned-in-window ranks ahead of unpinned high demand",
              out["pick"]["slug"] == "clean-pin", str(out["pick"]))

        # G10: --check exit codes.
        _, _ = run_picker(q, cal, "2026-11-13")
        r = subprocess.run(
            [sys.executable, str(PICKER), "--queue", str(q),
             "--calendar", str(cal), "--today", "2026-11-13",
             "--check", "incident-topic"],
            capture_output=True, text=True)
        check("G10 --check future pin -> exit 3", r.returncode == 3,
              r.stderr)
        r = subprocess.run(
            [sys.executable, str(PICKER), "--queue", str(q),
             "--calendar", str(cal), "--today", "2026-11-13",
             "--check", "hot-unpinned"],
            capture_output=True, text=True)
        check("G10 --check selectable -> exit 0", r.returncode == 0,
              r.stderr)
        r = subprocess.run(
            [sys.executable, str(PICKER), "--queue", str(q),
             "--calendar", str(cal), "--today", "2026-11-13",
             "--check", "does-not-exist"],
            capture_output=True, text=True)
        check("G10 --check unknown slug -> exit 1", r.returncode == 1,
              r.stderr)

        # G11: filters.
        q9 = tmp / "g9.jsonl"
        q9.write_text("\n".join([
            card("rec-line", ptype="recommendation", status=None),
            card("pub-card", status="published"),
            card("back-card", status="backlog"),
            card("real-pending", demand="high"),
        ]) + "\n")
        r, out = run_picker(q9, cal, "2026-11-13")
        seen = {e["slug"] for e in out["eligible"] + out["blocked"]}
        check("G11 only pending article cards compete",
              seen == {"real-pending"}, str(seen))

        # G12: malformed pins warn, never crash.
        q10 = tmp / "g10.jsonl"
        q10.write_text(card("broken-pin", hold_until=None,
                            priority="pin-notadate",
                            release_intent="31.12.2026") + "\n")
        r, out = run_picker(q10, cal, "2026-11-13")
        check("G12 malformed priority skipped (card stays unpinned)",
              r.returncode == 0 and out["pick"]["slug"] == "broken-pin",
              r.stdout + r.stderr)
        q11 = tmp / "g11.jsonl"
        q11.write_text(card("broken-hu", hold_until="13.11.2026",
                            priority="13.11.2026").replace(
                                '"priority": "pin-13.11.2026"',
                                '"priority": "13.11.2026"') + "\n")
        r, out = run_picker(q11, cal, "2026-11-13")
        check("G12 malformed hold_until warns and skips",
              r.returncode == 0
              and any("malformed hold_until" in w for w in out["warnings"]),
              str(out))

    print()
    if FAILURES:
        print(f"FAILED ({len(FAILURES)}): " + ", ".join(FAILURES))
        return 1
    print("all guards hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
