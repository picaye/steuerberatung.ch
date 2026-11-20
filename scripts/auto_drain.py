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
     "pending_after": M, "cap": 100, "margin": 2,
     "sentinel": {"type": "drain-sentinel", ...}}
  exit 0 = handled (drained, or below cap -> no-op, or nothing demotable).
  exit 2 = bad arguments. Malformed lines are tolerated exactly like
  scripts/inflow_gate.py / scripts/validate_queue.py do (skipped with a
  stderr warning, never crash the drain, never rewritten).

`--dry-run` prints the same audit line (with would-be counts) and writes
nothing. `--file`/`--cap`/`--margin` exist for tests; the cron uses defaults.
Stdlib only. The inflow_gate.py read-path is intentionally untouched.

Drain guardrail sentinel (t_19d5ba8d, CTO ruling 2026-11-20 — retires the
mis-calibrated t_1d5bd391 ">10/week" alert: with cap=100/margin=2 and 5-7
topics/day inflow, steady-state churn is arithmetically ~25-35 demotions per
week, so the old guardrail tripped structurally since 12 Nov). The check
lives INSIDE this script so every drain emits its verdict into the drain
output — triage reads the sentinel verdict and never re-derives tallies by
hand (the per-commit ">5 demotions" line was deleted from the triage
template; it produced the 9f4434f(7) false trip on 12 Nov). Rule 2, exactly:
  1. rolling-7d AUTO-DRAIN demotions > ROLLING7D_ALERT (45)    -> ALERT
  2. a SINGLE commit demoting > PER_COMMIT_ALERT (10) topics   -> ALERT
  3. HARD FLAG, always (never volume-gated): any commit touching the queue
     that changes the status of, or removes, a PINNED slug (hold_until /
     priority pin-YYYY-MM-DD / publish_calendar.FIXED entry), or performs a
     re-promotion (backlog/superseded -> pending) without an on-card ruling.
     This is the class 92fe28a violated (12 re-promotions; kept as the reason
     the flag exists — no revert per ruling 4). A permitted re-promotion
     commit must carry `ruling: t_XXXXXXXX` in its message citing the
     authorizing card.
Deliberately NOT flagged: pending->published of a pinned card (that is the
pin's designed release) and field-only edits of pinned records with the
status unchanged (publish_calendar.py --fix re-pins on purpose).
Transition detection compares records KEYED BY SLUG between the two blobs a
commit changes, never by pairing raw diff lines: 92fe28a rewrote the queue
file in a new line order, and line-pairing would misread a pure reorder as
mass status flips.

Sentinel read-only modes (for triage / CI / forced dry-runs):
  --sentinel        print the verdict JSON line
                    (exit 0 = OK/SKIPPED, exit 3 = ALERT)
  --sentinel-line   print only `sentinel: OK|ALERT ...` (embeddable in a
                    commit message; same exit codes)
  --days N --rolling-limit N --per-commit-limit N  scan-window overrides
  --fail-on-alert   in drain mode, exit 5 after a written drain whose
                    merged verdict is ALERT (default keeps the historical
                    exit contract: the drain IS the designed valve)
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jsonl_guard  # noqa: E402  size guard for the queue, t_2ed95a27

PENDING_CAP = 100          # mirrors scripts/inflow_gate.py PENDING_CAP
DRAIN_MARGIN = 2           # land at pending <= cap - margin

# Guardrail thresholds — CTO ruling 2026-11-20 rule 2 (t_19d5ba8d). The old
# ">10/week" alert (t_1d5bd391) is RETIRED: it fired structurally against the
# designed relief-valve churn (~25-35/week). Do not "fix" these by lowering
# them back without a new ruling.
ROLLING7D_ALERT = 45       # alert when rolling-7d auto-drain demotions > 45
PER_COMMIT_ALERT = 10      # alert when a single commit demotes > 10 topics

# validate_queue.py rule 1 shape: priority pin-YYYY-MM-DD.
PIN_PRIORITY_RE = re.compile(r"^pin-(\d{4}-\d{2}-\d{2})$")
# The ONLY token that legalizes a re-promotion commit (rule 3 hard flag):
# a citation of the card carrying the ruling, e.g. "ruling: t_19d5ba8d".
RULING_RE = re.compile(r"\bruling[:\s=]*\(?(t_[0-9a-f]{8})\)?", re.IGNORECASE)
DRAIN_MSG_MARK = "auto-drain"  # commit-message marker of the drain stream


def _fixed_slugs():
    """Slugs with a FIXED publish-calendar entry (exact Fridays, do not
    move). Import is defensive: the sentinel must never crash a drain."""
    try:
        import publish_calendar
        return set(publish_calendar.FIXED)
    except Exception:
        return set()


FIXED_SLUGS = _fixed_slugs()

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


def is_pinned(rec, fixed=None):
    """Pinned, guardrail definition (t_19d5ba8d rule 3): hold_until
    non-null, OR priority of shape pin-YYYY-MM-DD (validate_queue rule 1
    says those must carry hold_until — the belt-and-braces union covers the
    recurring "pin without hold_until" defect), OR slug in the FIXED
    publish-calendar set. Drain selection excludes pinned records
    absolutely, so all three classes are never demotable."""
    if rec.get("hold_until") is not None:
        return True
    pri = rec.get("priority")
    if isinstance(pri, str) and PIN_PRIORITY_RE.match(pri.strip()):
        return True
    if fixed is None:
        fixed = FIXED_SLUGS
    return rec.get("slug") in fixed


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


# --------------------------------------------------------------------------
# Drain guardrail sentinel (t_19d5ba8d)
# --------------------------------------------------------------------------

def _git(repo, *args):
    """git helper: (returncode, stdout). Never raises into a drain.

    On failure with empty stdout, return stderr instead: callers fold the
    text into SKIPPED reasons, and dropping stderr turned "fatal: <path>
    is outside repository" into an undiagnosable empty string (t_5ab9cd2b).
    """
    try:
        p = subprocess.run(("git", "-C", repo) + args,
                           capture_output=True, text=True)
        out = p.stdout or (p.stderr if p.returncode != 0 else "")
        return p.returncode, out
    except OSError:
        return 1, ""


def slug_records(text):
    """Parse queue JSONL text into {slug: rec}. Lines without a slug
    (recommendations, malformed) carry no card status semantics and are
    intentionally out of the guardrail's scope."""
    out = {}
    for raw in text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict) and rec.get("slug"):
            out[rec["slug"]] = rec
    return out


def classify_transitions(old_text, new_text):
    """Status-transition events between two queue blobs, keyed by slug.

    Keyed comparison (not diff-line pairing) is mandatory: a commit may
    rewrite the whole file in a different line order (92fe28a did) and only
    per-slug before/after states are meaningful.
    """
    a, b = slug_records(old_text), slug_records(new_text)
    events = []
    for slug in sorted(a.keys() | b.keys()):
        ra, rb = a.get(slug), b.get(slug)
        sa = ra.get("status") if ra else None
        sb = rb.get("status") if rb else None
        if ra is not None and rb is not None:
            if sa == sb:
                continue  # field-only edit (e.g. calendar re-pin): no event
            if sa == "pending" and sb == "backlog":
                kind = "demotion"
            elif sb == "pending" and sa in ("backlog", "superseded"):
                kind = "repro"
            elif sa == "pending" and sb == "published":
                kind = "publish"
            elif sa == "pending" and sb == "superseded":
                kind = "supersede_flip"
            else:
                kind = "status_change"
        elif ra is not None:
            kind = "removed"
        else:
            kind = "added"  # new card: never a guardrail event
        events.append({
            "slug": slug, "kind": kind, "from": sa, "to": sb,
            "pinned_before": ra is not None and is_pinned(ra),
            "pinned_after": rb is not None and is_pinned(rb),
        })
    return events


def _evaluate(events_by_commit, msgs, days, rolling_limit, per_commit_limit):
    """Shared verdict math over scanned history (+ optionally the planned
    commit) -> sentinel dict."""
    rolling_drain = 0
    commits = []
    hard = []
    alerts = []
    for sha7, events in events_by_commit:
        msg = msgs.get(sha7, "")
        dem = [e for e in events if e["kind"] == "demotion"]
        is_drain = DRAIN_MSG_MARK in msg
        if is_drain:
            rolling_drain += len(dem)
        commits.append({"sha": sha7, "drain": is_drain,
                        "demotions": len(dem)})
        if len(dem) > per_commit_limit:
            alerts.append(f"commit {sha7} demoted {len(dem)} > "
                          f"{per_commit_limit} (per-commit limit)")
        for e in dem + [x for x in events
                        if x["kind"] not in ("demotion", "added", "publish")]:
            if e["kind"] == "repro":
                if not RULING_RE.search(msg):
                    hard.append({"sha": sha7, "class": "unruled_repromotion",
                                 "slug": e["slug"], "from": e["from"],
                                 "to": e["to"]})
            elif (e["kind"] in ("supersede_flip", "status_change",
                                "removed")
                  and (e["pinned_before"] or e["pinned_after"])):
                hard.append({"sha": sha7, "class": "pinned_touched",
                             "slug": e["slug"], "from": e["from"],
                             "to": e["to"]})
        # demotion of a pinned slug is also pinned_touched (drain must
        # never produce one; a manual commit that does is a rule-3 hit):
        for e in dem:
            if e["pinned_before"] or e["pinned_after"]:
                hard.append({"sha": sha7, "class": "pinned_touched",
                             "slug": e["slug"], "from": e["from"],
                             "to": e["to"]})
    if rolling_drain > rolling_limit:
        alerts.insert(0, f"rolling-{days}d auto-drain demotions "
                         f"{rolling_drain} > {rolling_limit}")
    for h in hard:
        alerts.append(f"HARD FLAG {h['class']}: {h['slug']} "
                      f"{h['from']}->{h['to']} in {h['sha']}")
    verdict = "ALERT" if alerts else "OK"
    return {"type": "drain-sentinel", "verdict": verdict,
            "window_days": days,
            "rolling_drain_demotions": rolling_drain,
            "rolling_limit": rolling_limit,
            "max_commit_demotions": max([c["demotions"] for c in commits],
                                        default=0),
            "per_commit_limit": per_commit_limit,
            "commits_scanned": len(commits),
            "alerts": alerts, "hard_flags": hard, "commits": commits}


def _scan_history(queue_path, days, as_of=None):
    """Collect (events_by_commit, msgs) for queue-touching commits within
    the window, or (None, SKIPPED-verdict) when history is unavailable."""
    # realpath, not abspath: `git rev-parse --show-toplevel` returns the
    # FULLY RESOLVED root, so both sides of every relpath/toplevel
    # comparison must be resolved too. An unresolved symlink hop (macOS
    # /var -> /private/var tmpdirs; any symlinked checkout) made relpath
    # escape the repo, `git log -- <escaped>` failed rc=128, and the
    # guardrail silently degraded to SKIPPED (t_5ab9cd2b).
    q = os.path.realpath(queue_path)
    rc, toplevel = _git(os.path.dirname(q), "rev-parse", "--show-toplevel")
    toplevel = os.path.realpath(toplevel.strip()) if toplevel.strip() else ""
    if rc != 0 or not toplevel:
        return None, {"type": "drain-sentinel", "verdict": "SKIPPED",
                      "reason": "queue file is not inside a git repo; "
                                "history guardrail unavailable",
                      "alerts": [], "hard_flags": [], "commits_scanned": 0}
    rel = os.path.relpath(q, toplevel).replace(os.sep, "/")
    now = as_of or datetime.datetime.now(datetime.timezone.utc)
    since = now - datetime.timedelta(days=days)
    rc, out = _git(toplevel, "log",
                   f"--since={since.strftime('%Y-%m-%d %H:%M:%S +0000')}",
                   "--format=%h%x1f%P%x1f%B%x1e", "--", rel)
    if rc != 0:
        return None, {"type": "drain-sentinel", "verdict": "SKIPPED",
                      "reason": f"git log failed: {out.strip()}",
                      "alerts": [], "hard_flags": [], "commits_scanned": 0}
    events_by_commit = []
    msgs = {}
    for chunk in out.split("\x1e"):
        chunk = chunk.strip("\n")
        if not chunk.strip():
            continue
        sha7, parents, msg = chunk.split("\x1f", 2)
        msgs[sha7] = msg
        pars = parents.split()
        old_text = ""
        if pars:
            rc2, old_text = _git(toplevel, "show", f"{pars[0]}:{rel}")
            if rc2 != 0:
                old_text = ""
        rc3, new_text = _git(toplevel, "show", f"{sha7}:{rel}")
        if rc3 != 0:
            new_text = ""
        events_by_commit.append((sha7,
                                 classify_transitions(old_text, new_text)))
    return (events_by_commit, msgs), None


def sentinel_scan(queue_path=DEFAULT_QUEUE, days=7,
                  rolling_limit=ROLLING7D_ALERT,
                  per_commit_limit=PER_COMMIT_ALERT, as_of=None):
    """Read-only guardrail verdict over the git history of `queue_path`."""
    hist, skipped = _scan_history(queue_path, days, as_of)
    if skipped:
        return skipped
    return _evaluate(hist[0], hist[1], days, rolling_limit,
                     per_commit_limit)


def sentinel_verdict_for_drain(demoted_labels, prev_lines,
                               queue_path=DEFAULT_QUEUE, days=7,
                               rolling_limit=ROLLING7D_ALERT,
                               per_commit_limit=PER_COMMIT_ALERT,
                               as_of=None):
    """Verdict emitted INTO the drain output: history within the window,
    plus the planned drain commit folded in before the write happens.
    The planned commit is judged exactly like a historical one — rule 1 sees
    its demotions added to the rolling total (it carries the auto-drain
    marker), rule 2 checks its count against the per-commit limit, and rule
    3 hard-flags any pinned slug among it (structurally impossible unless
    the drain selection regressed — the flag is the tripwire)."""
    hist, skipped = _scan_history(queue_path, days, as_of)
    if skipped:
        return skipped
    events_by_commit, msgs = hist
    prev = slug_records("".join(prev_lines))
    planned_events = []
    for lbl in demoted_labels:
        slug = lbl.rsplit("(", 1)[0]
        rec = prev.get(slug, {})
        planned_events.append({"slug": slug, "kind": "demotion",
                               "from": rec.get("status", "pending"),
                               "to": "backlog",
                               "pinned_before": is_pinned(rec),
                               "pinned_after": False})
    if planned_events:
        events_by_commit = list(events_by_commit) + [
            ("PLANNED", planned_events)]
        msgs = dict(msgs)
        msgs["PLANNED"] = f"{DRAIN_MSG_MARK} — planned drain"
    return _evaluate(events_by_commit, msgs, days, rolling_limit,
                     per_commit_limit)


def sentinel_line(verdict):
    """One grep-able line for commit messages / stderr. Triage reads THIS;
    it must never re-derive a tally by hand (t_19d5ba8d rule 2)."""
    if verdict.get("verdict") == "SKIPPED":
        return f"sentinel: SKIPPED ({verdict.get('reason', '?')})"
    # .get everywhere: a degraded verdict dict must render, not KeyError
    # into a live drain (t_5ab9cd2b — host run crashed on a missing
    # rolling_drain_demotions while assembling the check message).
    return (f"sentinel: {verdict.get('verdict', '?')} "
            f"rolling7d={verdict.get('rolling_drain_demotions', '?')}"
            f"/{verdict.get('rolling_limit', '?')} "
            f"per-commit-max={verdict.get('max_commit_demotions', '?')}"
            f"/{verdict.get('per_commit_limit', '?')} "
            f"hard-flags={len(verdict.get('hard_flags', []))}")


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
    ap.add_argument("--force", action="store_true",
                    help="allow the write even if the size guard (t_2ed95a27) "
                         "would reject it")
    ap.add_argument("--sentinel", action="store_true",
                    help="read-only: print the guardrail sentinel verdict "
                         "JSON line for the queue's git history and exit "
                         "0 (OK/SKIPPED) / 3 (ALERT) — no drain, no write")
    ap.add_argument("--sentinel-line", action="store_true",
                    help="read-only: print only the one-line sentinel "
                         "verdict (embeddable in a commit message); same "
                         "exit codes as --sentinel")
    ap.add_argument("--days", type=int, default=7,
                    help="sentinel rolling window in days (default: 7, "
                         "per CTO ruling 2026-11-20)")
    ap.add_argument("--rolling-limit", type=int, default=ROLLING7D_ALERT,
                    help=f"sentinel rule 1 threshold (default: "
                         f"{ROLLING7D_ALERT}; override is for forced "
                         "dry-runs/tests only)")
    ap.add_argument("--per-commit-limit", type=int, default=PER_COMMIT_ALERT,
                    help=f"sentinel rule 2 threshold (default: "
                         f"{PER_COMMIT_ALERT}; override is for forced "
                         "dry-runs/tests only)")
    ap.add_argument("--fail-on-alert", action="store_true",
                    help="in drain mode, exit 5 when the sentinel verdict "
                         "is ALERT (default: verdict is emitted, drain "
                         "still succeeds — demotion is the designed valve)")
    args = ap.parse_args(argv)

    if args.sentinel or args.sentinel_line:
        verdict = sentinel_scan(args.file, days=args.days,
                                rolling_limit=args.rolling_limit,
                                per_commit_limit=args.per_commit_limit)
        print(sentinel_line(verdict) if args.sentinel_line
              else json.dumps(verdict, ensure_ascii=False))
        return 3 if verdict["verdict"] == "ALERT" else 0

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

    # Sentinel verdict folded into the ONE audit line (t_19d5ba8d AC2): the
    # planned commit is judged before the write, together with the rolling
    # window of history. Emitted even when the drain is a no-op, so every
    # drain output carries a guardrail line and triage never tallies by hand.
    verdict = sentinel_verdict_for_drain(
        demoted, lines, args.file, days=args.days,
        rolling_limit=args.rolling_limit,
        per_commit_limit=args.per_commit_limit)
    if verdict["verdict"] == "ALERT":
        for a in verdict["alerts"]:
            print(f"SENTINEL ALERT: {a}", file=sys.stderr)
    print(sentinel_line(verdict), file=sys.stderr)

    print(json.dumps({"demoted": demoted, "pending_before": before,
                      "pending_after": after, "cap": args.cap,
                      "margin": args.margin, "sentinel": verdict}))

    if args.dry_run:
        print("auto_drain: dry-run — file not modified", file=sys.stderr)
        return 5 if (args.fail_on_alert
                     and verdict["verdict"] == "ALERT") else 0
    if demoted:
        # t_2ed95a27 size guard: a drain only flips statuses, so the
        # non-empty line count must not drop below 50% of the original.
        rejected, msg = jsonl_guard.shrink_rejected(lines, new_lines,
                                                    force=args.force)
        if msg:
            print(msg, file=sys.stderr)
        if rejected:
            return 1
        ok, err = jsonl_guard.guarded_replace(args.file, new_lines)
        if not ok:
            print(err, file=sys.stderr)
            return 1
    return 5 if (args.fail_on_alert
                 and verdict["verdict"] == "ALERT") else 0


if __name__ == "__main__":
    sys.exit(main())
