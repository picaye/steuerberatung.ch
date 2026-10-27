#!/usr/bin/env python3
"""test_publish_calendar.py — regression guards for the Friday-grid planner.

Guards under test (scripts/publish_calendar.py):
  P1  THE t_2da26364 DEFECT: fridays() is anchored at the hardcoded
      GRID_START 2026-10-23; once that Friday passed, the pre-fix planner
      re-pinned cards INTO the past slot and validate_queue rejected every
      Monday cron run. --fix must NEVER emit a pin date < today.
  P2  a pin that is already valid (future, on-grid, slot free, deadline not
      passed) is KEPT — idempotent re-runs produce an identical plan.
  P3  cards whose topical deadline has passed are left UNPLACED (de-pinned
      by --fix), never pinned to a slot past their deadline.
  P4  fridays() invariants: strictly increasing, Friday-only, no blackout
      days (EXCLUDED), within [GRID_START, HORIZON_END].
  P5  --fix --dry-run is read-only: exit 0 and no working-tree changes on a
      healthy queue (watchdog contract of the Monday cron wrapper).
  P6  the maintenance commit message is ALWAYS card-stamped: the --fix cron
      stream was the dominant source of uncarded commits on main (t_d0820b72,
      fleet convention t_45ab7c9f; scripts/uncarded_commits.py sweeps).

The planner reads datetime.date.today() internally; tests fake the clock by
swapping the module-global `datetime` name for a shim whose date subclass
overrides today(). Real dates and the subclass compare interchangeably.

    python3 scripts/test_publish_calendar.py

Exit 0 = every guard holds; exit 1 = a guard regressed.
"""
from __future__ import annotations

import datetime
import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "publish_calendar.py"


def load_planner():
    spec = importlib.util.spec_from_file_location("publish_calendar", SCRIPT)
    pc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pc)
    return pc


class FakeClock:
    """Shim for the module-global `datetime` name with a frozen today()."""

    def __init__(self, today: datetime.date):
        self.date = type(
            "_FrozenDate",
            (datetime.date,),
            {"today": classmethod(lambda cls: today)},
        )
        self.timedelta = datetime.timedelta


def plan_at(pc, cards, today: datetime.date):
    """Run pc.plan() as if datetime.date.today() == today."""
    real = pc.datetime
    pc.datetime = FakeClock(today)
    try:
        return pc.plan(cards)
    finally:
        pc.datetime = real


def card(slug, hold_until, demand="medium"):
    return {"slug": slug, "status": "pending", "hold_until": hold_until,
            "demand": demand}


# P1 + P5 --------------------------------------------------------------

def test_fix_never_emits_past_pin(pc):
    """The original defect: a card pinned to the expired GRID_START slot."""
    today = datetime.date(2026, 10, 26)  # day the Monday cron first failed
    cards = [card("test-expired-grid-anchor-card", "2026-10-23")]
    out, unplaced = plan_at(pc, cards, today)
    assert today >= pc.GRID_START, "fixture assumes GRID_START is in the past"
    assert today not in out.values(), "past slot must not be reused"
    from datetime import date as _d
    for slot, slug in out.items():
        if slug in pc.FIXED:
            continue  # fixed fast-lanes are content decisions, tested in P1b
        assert slot >= today, f"P1 VIOLATION: {slug} pinned to past slot {slot}"
    # the expired card must have healed onto a future Friday
    healed = [s for s, g in out.items() if g == "test-expired-grid-anchor-card"]
    assert healed and healed[0] >= today, f"P1: expired card not re-placed: {out}"


def test_fixed_lanes_are_future_or_removed(pc):
    """P1b: FIXED fast-lane dates must not sit on/before GRID_START-era past.
    (Both current FIXED dates are 2027; if one ever expires it must be
    removed from the table, not silently pinned as a past slot.)"""
    for slug, when in pc.FIXED.items():
        assert datetime.date.fromisoformat(when) > pc.GRID_START, (
            f"P1b: FIXED {slug} on {when} is at/before GRID_START")


def test_dry_run_is_readonly(pc):
    """P5: --fix --dry-run exits 0 and leaves the working tree untouched."""
    before = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain"],
                            capture_output=True, text=True).stdout
    r = subprocess.run([sys.executable, str(SCRIPT), "--fix", "--dry-run"],
                       capture_output=True, text=True)
    assert r.returncode == 0, f"P5: dry-run exit {r.returncode}: {r.stdout}{r.stderr}"
    after = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain"],
                           capture_output=True, text=True).stdout
    assert before == after, "P5: dry-run mutated the working tree"


# P2 --------------------------------------------------------------------

def test_valid_pins_kept_idempotent(pc):
    today = datetime.date(2026, 10, 26)
    cards = [card("keep-me-a", "2026-11-20"), card("keep-me-b", "2026-12-04")]
    out1, _ = plan_at(pc, [dict(c) for c in cards], today)
    assert out1.get(datetime.date(2026, 11, 20)) == "keep-me-a"
    assert out1.get(datetime.date(2026, 12, 4)) == "keep-me-b"
    # feed the plan back as pins: a healthy calendar must re-plan to itself
    repinned = [card("keep-me-a", str(datetime.date(2026, 11, 20))),
                card("keep-me-b", str(datetime.date(2026, 12, 4)))]
    out2, _ = plan_at(pc, repinned, today)
    for d in (datetime.date(2026, 11, 20), datetime.date(2026, 12, 4)):
        assert out2.get(d) == out1.get(d), f"P2: valid pin churned: {out1} -> {out2}"


# P3 --------------------------------------------------------------------

def test_expired_deadline_left_unplaced(pc):
    today = datetime.date(2027, 6, 1)
    # 'fairness-initiative-ehepaare-2026' has DEADLINE 2026-11-27 — long past
    cards = [card("fairness-initiative-ehepaare-2026", "2027-05-28")]
    out, unplaced = plan_at(pc, cards, today)
    placed = [s for s, g in out.items() if g == "fairness-initiative-ehepaare-2026"]
    assert not placed, f"P3: expired-deadline card pinned to {placed}"
    assert any(c["slug"] == "fairness-initiative-ehepaare-2026" for c in unplaced), \
        "P3: expired-deadline card must be reported unplaced"


# P4 --------------------------------------------------------------------

def test_fridays_invariants(pc):
    fs = pc.fridays()
    assert fs and fs[0] >= pc.GRID_START and fs[-1] <= pc.HORIZON_END
    assert all(b > a for a, b in zip(fs, fs[1:])), "P4: grid not increasing"
    for d in fs:
        assert d.weekday() == 4, f"P4: {d} is not a Friday"
        assert (d.month, d.day) not in pc.EXCLUDED, f"P4: blackout day {d} in grid"


# P6 --------------------------------------------------------------------

def test_maintenance_commit_message_is_stamped(pc):
    msg = pc.maintenance_commit_message(3, 0)
    assert msg.startswith("publish calendar maintenance: re-pinned 3 card(s)")
    assert "de-pinned" not in msg, "P6: zero de-pins must not appear in message"
    assert pc.CARD_STAMP_RE.fullmatch(pc.MAINTENANCE_CARD), \
        f"P6: MAINTENANCE_CARD {pc.MAINTENANCE_CARD!r} is not a card id"
    assert pc.MAINTENANCE_CARD in msg, "P6: maintenance commit lacks its card stamp"
    msg2 = pc.maintenance_commit_message(2, 1)
    assert "de-pinned 1" in msg2 and pc.MAINTENANCE_CARD in msg2
    # The commit call must build its message through this function — an
    # inline f-string would bypass the stamp guard.
    src = SCRIPT.read_text()
    assert 'maintenance_commit_message(len(changed), len(cleared))' in src, \
        "P6: --fix no longer commits via maintenance_commit_message()"


def main() -> int:
    pc = load_planner()
    tests = [t for t in globals().values()
             if callable(t) and getattr(t, "__name__", "").startswith("test_")]
    failed = []
    for t in sorted(tests, key=lambda f: f.__name__):
        name = t.__name__
        try:
            t(pc)
            print(f"  PASS  {name}")
        except AssertionError as e:
            failed.append(name)
            print(f"  FAIL  {name}: {e}")
        except Exception as e:  # noqa: BLE001 — surface, don't mask
            failed.append(name)
            print(f"  ERROR {name}: {type(e).__name__}: {e}")
    print(f"test_publish_calendar: {len(tests) - len(failed)}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
