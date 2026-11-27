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
computed, only the count-based gates fire (cap AND suspend floor below — both
calendar-independent), with a stderr warning.

THIRD GATE — cto hard-suspend floor (t_e0dbafb1, cto scope call 2026-11-27
"SUSPEND new research adds — do NOT expand capacity"): the saturation gate
still left one hole — if a Friday slot ever freed up, appends would
re-authorize while the queue sat ~97 deep. CTO ruling: no new research adds
until pending < 60. While PENDING_SUSPEND_FLOOR <= pending < PENDING_CAP the
gate is closed regardless of the calendar; the rule is self-lifting (the
condition simply stops firing below the floor) and an early release or a new
floor is a cto decision at the weekly review, not something this script
guesses. Severity is AMBER (executing a standing directive is steady state,
not an incident — cto ruling 2026-11-26), but when the calendar is
simultaneously saturated past the tripwire grace it escalates to RED like
no_free_fridays: suspending adds does not fix the publish grid (97 pending at
1 published/Friday is ~37 weeks to the floor), so escalation pressure must
stay alive.

SEVERITY SPLIT — alerting interpretation only (t_ae7d83c3, cto ruling 2026-11-26):
  Since the grid booked to 2028-06-30, the no_free_fridays gate stays closed
  every day, which made the daily site-verify report RED for months and trained
  everyone to ignore it (alert fatigue). The gate's BEHAVIOR is unchanged — exit
  3 still blocks unpinned appends exactly as before — but its report severity is
  split:
    pending >= cap (cap-breach)        -> RED    (actionable, unchanged)
    cap > pending >= suspend_floor     -> AMBER  (cto suspend directive; the
                                                   headline carries
                                                   gate_reason=cto_suspend,
                                                   RED under ossification)
    free_fridays == 0, pending < floor -> AMBER  (steady-state saturation; the
                                                   headline MUST carry
                                                   gate_reason=no_free_fridays)
    not gated                          -> GREEN
  Report severity ladder (site-verify "worst gate governs", t_6467c6c1):
  RED > AMBER > GREEN. AMBER is visible in the headline and the daily rollup,
  never flattened into GREEN, and still governs overall against any GREEN.
  ANTI-OSSIFICATION TRIPWIRE: saturation is not a free pass forever. Consecutive
  days observed with free_fridays == 0 are counted in .local state; once the
  streak exceeds OSSIFICATION_GRACE_DAYS (14 — the grace window agreed around
  the PM capacity call of 27 Nov), the severity escalates back to RED with
  reason saturation-ossified, forcing the capacity/suspend decision. The counter
  resets on any run that observes free_fridays > 0; a cap-breach run does NOT
  reset it (cap-breach never releases the underlying saturation); a calendar
  read failure (free_fridays == null) leaves the counter untouched (unknown is
  not "not saturated"). The streak counts CALENDAR days since the state file
  was seeded, so skipped cron runs still advance it; same-day repeat runs are
  idempotent. The clock starts at first observation by this code version —
  to hold the line from the 2026-11-25 grid lock instead, seed the state file
  (format below) with "saturation_since": "2026-11-25".

Contract (consumed by the cron prompt, not by CI):
  stdout: one JSON object {"pending": N, "cap": PENDING_CAP,
                           "suspend_floor": PENDING_SUSPEND_FLOOR,
                           "gated": bool,
                           "free_fridays": int|null,
                           "gate_reason": "pending_cap"|"cto_suspend"|
                                          "no_free_fridays"|null,
                           "severity": "RED"|"AMBER"|"GREEN",
                           "saturation_days": int,
                           "ossified": bool}
  exit 0  -> not gated (pending < suspend_floor AND calendar has a free
             Friday), or queue file missing (pending: 0)
  exit 3  -> gated (pending >= cap OR pending >= suspend_floor OR
             free_fridays == 0)  [UNCHANGED by the severity split — appends
             stay blocked under AMBER]
  The cron branches on the exit code only; free_fridays/gate_reason/severity/
  saturation_days/ossified/suspend_floor are additive observability fields.

  State file (.local/inflow_gate_saturation.json, gitignored; --state-file for
  tests): {"saturation_since": "YYYY-MM-DD"|null,
           "consecutive_days": int, "last_seen": "YYYY-MM-DD"|null}

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
# t_e0dbafb1 cto scope call 2026-11-27: hard-suspend research adds while
# pending >= this floor, independent of the calendar. Self-lifting: below the
# floor the condition stops firing; release/floor changes are cto weekly-
# review decisions. 60 chosen so the queue drains toward publish depth
# instead of oscillating 98->103 at the cap.
PENDING_SUSPEND_FLOOR = 60
FREE_FRIDAYS_REPORT_LIMIT = 20  # mirrors publish_calendar.py --free
DEFAULT_STATE = os.path.join(REPO_ROOT, ".local", "inflow_gate_saturation.json")
# t_ae7d83c3: AMBER(no_free_fridays) grace window. Once the consecutive
# saturation streak EXCEEDS this many days, severity escalates to RED with
# reason saturation-ossified (escalation fires on day 15).
OSSIFICATION_GRACE_DAYS = 14
# Severity ladder for the site-verify report ("worst gate governs"):
# RED > AMBER > GREEN. The gate never emits a flattening: AMBER always
# governs overall against GREEN.
SEVERITY_RANK = {"GREEN": 0, "AMBER": 1, "RED": 2}


def _load_state(path):
    """Return state dict, or None if absent/corrupt (corrupt -> fresh start)."""
    try:
        with open(path, encoding="utf-8") as fh:
            st = json.load(fh)
        return st if isinstance(st, dict) else None
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _save_state(path, state):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(state, fh, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, path)
    except OSError as exc:
        # Alerting state must never break the gate's blocking decision.
        print(f"WARN: could not persist saturation state to {path}: {exc}",
              file=sys.stderr)


def update_saturation_state(path, free, today=None):
    """Advance/read the consecutive-saturation-day counter for a calendar
    observation `free` (int or None on read failure). Returns
    (days, since_iso|None):
      free == 0    -> streak start/advance (idempotent within a day;
                      calendar-elapsed since the streak began)
      free > 0     -> reset (calendar open again)
      free == None -> untouched (a failed read is not evidence either way)
    """
    if today is None:
        today = datetime.date.today()
    if free is None:
        st = _load_state(path) or {}
        try:
            since = datetime.date.fromisoformat(st.get("saturation_since"))
        except (TypeError, ValueError):
            return 0, None
        last = st.get("last_seen")
        if last is not None and last > today.isoformat():
            return 0, None
        return ((today - since).days + 1) if since <= today else 0, since.isoformat()
    if free > 0:
        _save_state(path, {"saturation_since": None, "consecutive_days": 0,
                           "last_seen": None})
        return 0, None
    st = _load_state(path) or {}
    since_raw = st.get("saturation_since")
    last_raw = st.get("last_seen")
    try:
        since = datetime.date.fromisoformat(since_raw) if since_raw else None
    except ValueError:
        since = None
    try:
        last = datetime.date.fromisoformat(last_raw) if last_raw else None
    except ValueError:
        last = None
    if since is None or since > today or (last is not None and last > today):
        # Fresh streak (or clock went backwards — restart honestly).
        since = today
    elif last == today:
        pass  # same-day repeat run: idempotent, do not double-count
    # else: gap days (skipped runs) still count — streak is calendar-based.
    days = (today - since).days + 1
    _save_state(path, {"saturation_since": since.isoformat(),
                       "consecutive_days": days,
                       "last_seen": today.isoformat()})
    return days, since.isoformat()


def decide_severity(gate_reason, free, saturation_days):
    """Map a gating decision to a report severity. Exit codes and blocking
    are NOT decided here — this is interpretation only (cto ruling: the gate
    keeps blocking appends exactly as today).

    t_e0dbafb1 floor extension: cto_suspend is AMBER steady state (executing
    a standing directive is not an incident) and shares the tripwire
    escalation ONLY while the calendar is simultaneously observed saturated
    (free == 0). A floor-breach with open Fridays is a pure queue-depth
    signal; the streak may merely be stale from a state file seeded while
    the grid was booked, so it must not escalate."""
    if gate_reason == "pending_cap":
        return "RED"
    if gate_reason == "cto_suspend" and free != 0:
        return "AMBER"
    if gate_reason in ("no_free_fridays", "cto_suspend"):
        return "RED" if saturation_days > OSSIFICATION_GRACE_DAYS else "AMBER"
    return "GREEN"


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
              "gating on the count-based caps only (pending_cap / "
              "cto_suspend)", file=sys.stderr)
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", default=DEFAULT_QUEUE,
                    help="queue jsonl path (default: repo data/"
                         "content-research.jsonl)")
    ap.add_argument("--state-file", default=DEFAULT_STATE,
                    help="saturation tripwire state path (default: repo "
                         ".local/inflow_gate_saturation.json)")
    args = ap.parse_args(argv)

    pending, _malformed = count_pending(args.file)
    free = count_free_fridays(read_cards(args.file))
    if pending >= PENDING_CAP:
        gated, reason = True, "pending_cap"
    elif pending >= PENDING_SUSPEND_FLOOR:
        # The cto suspend floor outranks the calendar reason: at/above it,
        # adds are barred even if a Friday slot opens, so naming the
        # binding constraint keeps the headline honest (t_e0dbafb1).
        gated, reason = True, "cto_suspend"
    elif free == 0:
        gated, reason = True, "no_free_fridays"
    else:
        gated, reason = False, None
    # Tripwire counter: advance/reset on every OBSERVABLE calendar read. A
    # cap-breach day still reads the calendar, so it must not silently reset
    # the saturation streak (cap-breach never releases saturation). free is
    # None (read failure) -> state untouched.
    days, since = update_saturation_state(args.state_file, free)
    severity = decide_severity(reason, free, days)
    ossified = (reason in ("no_free_fridays", "cto_suspend")
                and free == 0 and days > OSSIFICATION_GRACE_DAYS)
    print(json.dumps({"pending": pending, "cap": PENDING_CAP,
                      "suspend_floor": PENDING_SUSPEND_FLOOR, "gated": gated,
                      "free_fridays": free, "gate_reason": reason,
                      "severity": severity,
                      "saturation_days": days,
                      "ossified": ossified}))
    if gated:
        tag = "saturation-ossified" if ossified else reason
        extra = ""
        if reason == "no_free_fridays":
            extra = (f"; saturation_days={days}/{OSSIFICATION_GRACE_DAYS} grace"
                     + (f" since {since} — ESCALATE: capacity/suspend "
                        "decision required" if ossified else ""))
        elif reason == "cto_suspend":
            extra = (f", suspend_floor={PENDING_SUSPEND_FLOOR} — cto directive "
                     "(t_e0dbafb1): no research adds until pending < "
                     f"{PENDING_SUSPEND_FLOOR}")
            if free == 0:
                extra += (f"; saturation_days={days}/{OSSIFICATION_GRACE_DAYS}"
                          " grace")
                if ossified:
                    extra += (" — ESCALATE: publish grid still saturated past "
                              "grace despite suspend; capacity decision "
                              "required at weekly review")
        print(f"inflow_gate: GATED [{severity}] (gate_reason={tag}) — "
              f"pending={pending}, cap={PENDING_CAP}, free_fridays={free}"
              f"{extra}; no unpinned appends this run, flip to backlog "
              "hygiene", file=sys.stderr)
    return 3 if gated else 0


if __name__ == "__main__":
    sys.exit(main())
