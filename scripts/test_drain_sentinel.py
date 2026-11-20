#!/usr/bin/env python3
"""test_drain_sentinel.py — regression guards for the drain guardrail
sentinel in scripts/auto_drain.py (t_19d5ba8d, CTO ruling 2026-11-20).

Style mirrors scripts/test_auto_drain.py (standalone runner, [ok]/FAIL
lines, exit 0/1; function names also pytest-collectable).

Every guard builds a SYNTHETIC git repo under a temp dir with the queue at
data/content-research.jsonl, commits driven by explicit dates/subjects, and
calls auto_drain.sentinel_scan / sentinel_verdict_for_drain on it. Guards:

  S1   thresholds are the ruling constants: 45 / 10 (grep-verifiable AC1).
  S2   rolling-7d auto-drain demotions == 45 -> OK; == 46 -> ALERT
       (strict ">45", drain-marked commits only).
  S3   commits outside the window do not count toward the rolling total.
  S4   manual (non-drain) demotion commits count toward the per-commit
       rule but NOT toward rolling-7d auto-drain volume.
  S5   single commit demoting 10 -> OK; 11 -> ALERT (strict ">10").
  S6   HARD flag, 1 demotion only (no volume): demotion of a hold_until
       pinned card -> pinned_touched.
  S7   pinned classes: priority pin-YYYY-MM-DD without hold_until, and
       FIXED-calendar slug, are also protected.
  S8   re-promotion (backlog->pending, superseded->pending) without a
       ruling token -> unruled_repromotion; with "ruling: t_XXXXXXXX" -> OK.
  S9   NOT flagged: pinned pending->published (Friday release), pinned
       field-only edit / re-pin (calendar --fix stream), new-card adds.
  S10  full-file REORDER with zero status changes -> no events (the
       92fe28a trap: line-diff pairing would misread mass flips).
  S11  92fe28a replay shape: reorder + 5 pending->superseded of pinned +
       12 re-promotions -> exactly 12 unruled_repromotion + 5
       pinned_touched hard flags.
  S12  pinned record REMOVAL from the queue -> pinned_touched.
  S13  drain-mode integration: audit line carries "sentinel" verdict;
       a clean repo drain -> OK; --per-commit-limit override -> ALERT on
       stderr + "SENTINEL ALERT" lines; exit stays 0 (valve by design).
  S14  --fail-on-alert makes the drained run exit 5 on ALERT.
  S15  --sentinel CLI mode exits 3 on ALERT, 0 on OK (read-only contract).
  S16  verdict SKIPPED (not crash) when the queue is not inside a git repo;
       drain still exits 0.

    python3 scripts/test_drain_sentinel.py

Exit 0 = every guard holds; exit 1 = a guard regressed.
"""
from __future__ import annotations

import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "auto_drain.py"
sys.path.insert(0, str(REPO / "scripts"))
import auto_drain  # noqa: E402

FAILURES: list[str] = []
NOW = datetime.datetime(2026, 11, 20, 12, 0, 0, tzinfo=datetime.timezone.utc)
REL = "data/content-research.jsonl"


def check(name: str, cond: bool, detail: str = ""):
    status = "ok" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def rec(slug, status="pending", demand="high", date="2026-10-01",
        hold_until=None, priority=None):
    r = {"date": date, "slug": slug, "title": slug, "meta": "m",
         "facts": [], "demand": demand, "status": status}
    if hold_until is not None:
        r["hold_until"] = hold_until
    if priority is not None:
        r["priority"] = priority
    return r


def git(repo, *args, env_date=None):
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
           "PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(repo)}
    if env_date:
        iso = env_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        env["GIT_AUTHOR_DATE"] = iso
        env["GIT_COMMITTER_DATE"] = iso
    p = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, env=env)
    assert p.returncode == 0, f"git {' '.join(args)}: {p.stderr}"
    return p.stdout


def mkrepo(tmp: Path) -> Path:
    repo = tmp / "repo"
    (repo / "data").mkdir(parents=True)
    git(repo, "init", "-q", "-b", "main")
    return repo


def commit_queue(repo: Path, records, subject, day=19, hour=10,
                 minutes_back=0):
    """Write records (list of dicts, list order = file order) and commit."""
    q = repo / REL
    q.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                         for r in records), encoding="utf-8")
    dt = NOW - datetime.timedelta(days=day, minutes=minutes_back)
    dt = dt.replace(hour=hour)
    git(repo, "add", "-A", env_date=dt)
    git(repo, "commit", "-q", "-m", subject, env_date=dt)
    return q


def scan(repo: Path, **kw):
    kw.setdefault("as_of", NOW)
    return auto_drain.sentinel_scan(str(repo / REL), **kw)


def drain_commit_slugs(n, prefix="d"):
    """n pending->backlog demotions as auto-drain commits, 1 slug each."""
    return [f"{prefix}{i}" for i in range(n)]


def build_rolling(repo: Path, total, commits=None, day=3, subject=None):
    """Seed repo so auto-drain commits within the window demote `total`
    slugs in total across `commits` commits. Cumulative: each commit keeps
    previously demoted slugs in backlog (otherwise the fixture itself would
    be a re-promotion stream)."""
    commits = commits or max(1, total // 5)
    per = [total // commits] * commits
    for i in range(total - sum(per)):
        per[i] += 1
    slugs = drain_commit_slugs(total)
    commit_queue(repo, [rec(s) for s in slugs] + [rec("keeper")],
                 "seed", day=day + 2)
    done: set = set()
    idx = 0
    for ci, cnt in enumerate(per):
        done |= set(slugs[idx:idx + cnt])
        idx += cnt
        cur = [rec(s, status="backlog" if s in done else "pending")
               for s in slugs] + [rec("keeper")]
        commit_queue(repo, cur,
                     subject or f"content-research: auto-drain {ci}",
                     day=day, minutes_back=ci)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="t19d5ba8d-"))

    # S1 thresholds exactly as rule 2
    check("S1 ROLLING7D_ALERT == 45 and PER_COMMIT_ALERT == 10",
          auto_drain.ROLLING7D_ALERT == 45
          and auto_drain.PER_COMMIT_ALERT == 10,
          f"{auto_drain.ROLLING7D_ALERT}/{auto_drain.PER_COMMIT_ALERT}")

    # S2 rolling 45 OK / 46 ALERT (boundary is strictly >45)
    r = mkrepo(tmp / "s2a")
    build_rolling(r, 45)
    v = scan(r)
    check("S2a rolling7d 45 == limit -> OK (alert is >45)",
          v["verdict"] == "OK" and v["rolling_drain_demotions"] == 45,
          json.dumps(v["alerts"]))
    r = mkrepo(tmp / "s2b")
    build_rolling(r, 46, commits=6)
    v = scan(r)
    check("S2b rolling7d 46 > limit -> ALERT with rolling reason",
          v["verdict"] == "ALERT"
          and any("rolling-7d auto-drain demotions 46 > 45" in a
                  for a in v["alerts"]),
          json.dumps(v["alerts"]))

    # S3 window boundary: same volume at day 8 -> OK
    r = mkrepo(tmp / "s3")
    build_rolling(r, 50, day=8)
    v = scan(r)
    check("S3 out-of-window drain commits excluded from rolling total",
          v["verdict"] == "OK" and v.get("rolling_drain_demotions") == 0,
          json.dumps(v.get("rolling_drain_demotions", v)))

    # S4 manual demotions don't inflate the rolling AUTO-DRAIN volume
    # (8 <= per-commit limit, so the only question is the rolling total)
    r = mkrepo(tmp / "s4")
    slugs = drain_commit_slugs(8)
    commit_queue(r, [rec(s) for s in slugs], "seed", day=5)
    commit_queue(r, [rec(s, status="backlog") for s in slugs],
                 "content-research: manual backlog sweep", day=2)
    v = scan(r)
    check("S4 non-drain commit demotions not counted in rolling7d",
          v["verdict"] == "OK" and v.get("rolling_drain_demotions") == 0
          and v.get("max_commit_demotions") == 8,
          json.dumps({k: v.get(k) for k in
                      ("rolling_drain_demotions", "max_commit_demotions")}))

    # S5 per-commit boundary: 10 OK, 11 ALERT
    for n, expect in ((10, True), (11, False)):
        r = mkrepo(tmp / f"s5-{n}")
        slugs = drain_commit_slugs(n)
        commit_queue(r, [rec(s) for s in slugs], "seed", day=5)
        commit_queue(r, [rec(s, status="backlog") for s in slugs],
                     "content-research: auto-drain — big batch", day=2)
        v = scan(r)
        ok_expect = (v["verdict"] == "OK") if expect else \
                    (v["verdict"] == "ALERT"
                     and any(f"demoted {n} > 10" in a for a in v["alerts"]))
        check(f"S5 single-commit {n} demotions -> {'OK' if expect else 'ALERT'}",
              ok_expect, json.dumps(v["alerts"]))

    # S6 pinned demotion hard flag at volume 1 (not volume-gated)
    r = mkrepo(tmp / "s6")
    commit_queue(r, [rec("pinned1", hold_until="2026-12-04"),
                     rec("free1", demand="low")], "seed", day=5)
    commit_queue(r, [rec("pinned1", hold_until="2026-12-04", status="backlog"),
                     rec("free1", demand="low")],
                 "content-research: auto-drain — Oops", day=2)
    v = scan(r)
    check("S6 demotion of a hold_until pinned card -> hard flag at 1 topic",
          v["verdict"] == "ALERT"
          and any(h["class"] == "pinned_touched" and h["slug"] == "pinned1"
                  for h in v["hard_flags"]),
          json.dumps(v["hard_flags"]))

    # S7 other pinned classes: pin-YYYY-MM-DD priority (defect shape: no
    # hold_until) and FIXED calendar slug
    fixed_slug = next(iter(auto_drain.FIXED_SLUGS or ["ubs-cs-migration-steuererklaerung-2026"]))
    r = mkrepo(tmp / "s7")
    commit_queue(r, [rec("prio_pin", priority="pin-2026-12-11"),
                     rec(fixed_slug)], "seed", day=5)
    commit_queue(r, [rec("prio_pin", priority="pin-2026-12-11", status="backlog"),
                     rec(fixed_slug, status="backlog")],
                 "content-research: manual — Oops", day=2)
    v = scan(r)
    flagged = {h["slug"] for h in v["hard_flags"]}
    check("S7 pin-priority and FIXED-calendar slugs are pinned too",
          "prio_pin" in flagged and fixed_slug in flagged,
          json.dumps(v["hard_flags"]))

    # S8 re-promotion: unruled -> hard flag; ruling: t_XXXXXXXX -> allowed
    r = mkrepo(tmp / "s8a")
    commit_queue(r, [rec("rp1", status="backlog"), rec("rp2", status="superseded")],
                 "seed", day=5)
    commit_queue(r, [rec("rp1"), rec("rp2")],
                 "content-research: hygiene — re-queue 2", day=2)
    v = scan(r)
    check("S8a backlog/superseded -> pending without ruling -> 2 hard flags",
          v["verdict"] == "ALERT"
          and sum(h["class"] == "unruled_repromotion" for h in v["hard_flags"]) == 2,
          json.dumps(v["hard_flags"]))
    r = mkrepo(tmp / "s8b")
    commit_queue(r, [rec("rp1", status="backlog"), rec("rp2", status="superseded")],
                 "seed", day=5)
    commit_queue(r, [rec("rp1"), rec("rp2")],
                 "content-research: hygiene — re-queue 2 ruling: t_ab12cd34",
                 day=2)
    v = scan(r)
    check("S8b re-promotion citing a card ruling -> not flagged",
          v["verdict"] == "OK" and not v["hard_flags"],
          json.dumps(v["alerts"]))

    # S9 designed flows are NOT flagged: pinned Friday publish, calendar
    # re-pin field edit, brand-new card
    r = mkrepo(tmp / "s9")
    commit_queue(r, [rec("friday", hold_until="2026-11-20"),
                     rec("repin", hold_until="2026-11-27")],
                 "seed", day=5)
    commit_queue(r, [rec("friday", hold_until="2026-11-20", status="published"),
                     rec("repin", hold_until="2026-12-04"),
                     rec("fresh")],
                 "publish calendar maintenance: re-pinned (t_d0820b72)", day=2)
    v = scan(r)
    check("S9 Friday publish + re-pin + new card produce no flags",
          v["verdict"] == "OK" and not v["hard_flags"],
          json.dumps(v["alerts"]))

    # S10 pure full-file reorder: keyed comparison sees zero events
    r = mkrepo(tmp / "s10")
    slugs = [f"q{i}" for i in range(30)]
    base = [rec(s, status="backlog" if i < 15 else "pending")
            for i, s in enumerate(slugs)]
    commit_queue(r, base, "seed", day=5)
    commit_queue(r, list(reversed(base)),
                 "content-research: metrics re-order (no status change)", day=2)
    v = scan(r)
    check("S10 whole-file reorder -> zero transitions (92fe28a diff trap)",
          v["verdict"] == "OK" and v["max_commit_demotions"] == 0
          and not v["hard_flags"],
          json.dumps(v["alerts"]))

    # S11 92fe28a replay: reorder + 5 pinned supersede flips + 12 re-promos
    r = mkrepo(tmp / "s11")
    pend = [rec(f"flip{i}", hold_until=f"2026-11-2{i}") for i in range(5)]
    prom = [rec(f"repro{i}", status="backlog" if i % 2 else "superseded")
            for i in range(12)]
    others = [rec(f"o{i}") for i in range(10)]
    commit_queue(r, pend + prom + others, "seed", day=5)
    new_pend = [rec(f"flip{i}", hold_until=f"2026-11-2{i}", status="superseded")
                for i in range(5)]
    new_prom = [rec(f"repro{i}") for i in range(12)]
    commit_queue(r, others[::-1] + new_prom + new_pend,
                 "content-research: hygiene — superseded 5, re-pinned", day=2)
    v = scan(r)
    classes = [(h["class"], h["slug"]) for h in v["hard_flags"]]
    check("S11 92fe28a shape -> 12 unruled_repromotion + 5 pinned_touched",
          sum(c == "unruled_repromotion" for c, _ in classes) == 12
          and sum(c == "pinned_touched" for c, _ in classes) == 5
          and v["verdict"] == "ALERT",
          json.dumps(classes))

    # S12 removal of a pinned record from the queue -> hard flag
    r = mkrepo(tmp / "s12")
    commit_queue(r, [rec("gone", hold_until="2026-12-11"), rec("stay")],
                 "seed", day=5)
    commit_queue(r, [rec("stay")], "content-research: cleanup", day=2)
    v = scan(r)
    check("S12 removing a pinned card -> pinned_touched hard flag",
          any(h["class"] == "pinned_touched" and h["slug"] == "gone"
              for h in v["hard_flags"]),
          json.dumps(v["hard_flags"]))

    # S13 drain-mode integration: audit line carries verdict; forced
    # --per-commit-limit override alerts but drain still succeeds (exit 0)
    r = mkrepo(tmp / "s13")
    slugs = [f"p{i}" for i in range(12)]
    commit_queue(r, [rec(s, demand="low") for s in slugs] + [rec("pinX", hold_until="2026-12-18")],
                 "seed", day=5)
    qpath = r / REL
    p_ok = subprocess.run([sys.executable, str(SCRIPT), "--file", str(qpath),
                           "--cap", "12", "--margin", "2", "--dry-run"],
                          capture_output=True, text=True)
    out_ok = json.loads(p_ok.stdout)
    check("S13a audit line carries sentinel verdict; clean drain -> OK",
          p_ok.returncode == 0
          and out_ok["sentinel"]["type"] == "drain-sentinel"
          and out_ok["sentinel"]["verdict"] == "OK"
          and len(out_ok["demoted"]) == 3,
          p_ok.stdout + p_ok.stderr)
    p_al = subprocess.run([sys.executable, str(SCRIPT), "--file", str(qpath),
                           "--cap", "6", "--margin", "2", "--dry-run",
                           "--per-commit-limit", "3"],
                          capture_output=True, text=True)
    out_al = json.loads(p_al.stdout)
    check("S13b forced per-commit breach -> ALERT verdict + stderr SENTINEL ALERT lines, exit stays 0",
          p_al.returncode == 0
          and out_al["sentinel"]["verdict"] == "ALERT"
          and out_al["sentinel"]["hard_flags"] == []
          and "SENTINEL ALERT" in p_al.stderr
          and any("PLANNED demoted 9 > 3" in a
                  for a in out_al["sentinel"]["alerts"]),
          p_al.stdout + p_al.stderr)

    # S14 --fail-on-alert exit 5 on ALERT
    p5 = subprocess.run([sys.executable, str(SCRIPT), "--file", str(qpath),
                         "--cap", "6", "--margin", "2", "--dry-run",
                         "--per-commit-limit", "3", "--fail-on-alert"],
                        capture_output=True, text=True)
    check("S14 --fail-on-alert turns ALERT into exit 5",
          p5.returncode == 5, f"rc={p5.returncode}")

    # S15 --sentinel read-only CLI: exit 0 OK / exit 3 ALERT, file untouched
    snap15 = qpath.read_bytes()
    p15a = subprocess.run([sys.executable, str(SCRIPT), "--file", str(qpath),
                           "--sentinel", "--days", "7"],
                          capture_output=True, text=True)
    v15a = json.loads(p15a.stdout)
    check("S15a --sentinel prints verdict JSON, exit 0 on OK, file untouched",
          p15a.returncode == 0 and v15a["verdict"] == "OK"
          and qpath.read_bytes() == snap15,
          p15a.stdout + p15a.stderr)
    # land an actual demotion commit in the fixture history, then alert on it
    subprocess.run([sys.executable, str(SCRIPT), "--file", str(qpath),
                    "--cap", "6", "--margin", "2"],
                   capture_output=True, text=True)
    commit_queue_at_now = git(r, "add", "-A", env_date=NOW)
    git(r, "commit", "-q", "-m", "content-research: auto-drain — S15 fixture",
        env_date=NOW)
    assert commit_queue_at_now == ""
    p15b = subprocess.run([sys.executable, str(SCRIPT), "--file", str(qpath),
                           "--sentinel", "--days", "7",
                           "--per-commit-limit", "3"],
                          capture_output=True, text=True)
    check("S15b --sentinel exits 3 on ALERT over real history",
          p15b.returncode == 3
          and json.loads(p15b.stdout)["verdict"] == "ALERT",
          p15b.stdout + p15b.stderr)

    # S16 no git repo -> SKIPPED, drain unaffected
    q16 = tmp / "nogit" / Path(REL)
    q16.parent.mkdir(parents=True)
    q16.write_text("".join(json.dumps(rec(f"s{i}")) + "\n"
                           for i in range(12)), encoding="utf-8")
    p16 = subprocess.run([sys.executable, str(SCRIPT), "--file", str(q16),
                          "--cap", "12", "--margin", "2"],
                         capture_output=True, text=True)
    out16 = json.loads(p16.stdout)
    check("S16 SKIPPED verdict (not crash) when history unavailable; drain exit 0",
          p16.returncode == 0 and out16["sentinel"]["verdict"] == "SKIPPED"
          and len(out16["demoted"]) == 2,
          p16.stdout + p16.stderr)

    # S17 symlinked repo path: git rev-parse --show-toplevel returns the
    # RESOLVED path, so an unresolved queue path escapes the repo in the
    # relpath call and every history scan degrades to SKIPPED
    # (t_5ab9cd2b — host macOS tmpdir /var -> /private/var symptom).
    # Built via an explicit symlink so it fails on ANY platform, not just
    # hosts whose tmpdir happens to be symlinked.
    link = tmp / "repo-link"
    try:
        os.symlink(str(r), str(link))
    except (OSError, NotImplementedError):
        check("S17 symlinked queue path scans history (not SKIPPED)", False,
              "os.symlink unavailable on this platform")
    else:
        v17 = auto_drain.sentinel_scan(str(link / REL), as_of=NOW)
        check("S17 symlinked queue path scans history (not SKIPPED)",
              v17["verdict"] != "SKIPPED"
              and v17.get("commits_scanned", 0) >= 2,
              json.dumps(v17))
        # a degraded SKIPPED dict must still render through every consumer
        try:
            line = auto_drain.sentinel_line(
                {"type": "drain-sentinel", "verdict": "SKIPPED",
                 "reason": "git log failed: fatal: ... outside repository",
                 "alerts": [], "hard_flags": [], "commits_scanned": 0})
            ok18 = line.startswith("sentinel: SKIPPED")
        except KeyError as e:
            ok18, line = False, f"KeyError {e}"
        check("S18 sentinel_line renders a stripped SKIPPED dict",
              ok18, line)

    print(f"\n{18} guards run, {len(FAILURES)} failed"
          + (f": {FAILURES}" if FAILURES else ""))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
