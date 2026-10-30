#!/usr/bin/env python3
"""test_mark_published.py — regression guards for scripts/mark_published.py (t_6544e449).

Root cause guarded: the Fri 2026-10-30 cron publish of mwst-erhoehung-2027-ahv-armee
(e6a46723) stamped the queue under the WRONG KEY — `published_date` instead of the
schema field `published_at` (t_fcff6abc / backfill c474a136) — and left the card's
`hold_until` / `priority` / `release_intent` scheduling fields stale on a live record.
The stamp FIRED; it fired under the wrong name.

Guards under test:
  R1  a flip writes `published_at` (schema field) — the exact regression: a flip
      that only produced `published_date` must FAIL this test.
  R2  rename semantics: `published_date` never survives a flip (popped).
  R3  stale scheduling fields `hold_until`, `priority`, `release_intent` are
      cleared on the flip (@PM 2026-10-30 verdict, AC c/e — release_intent is a
      pre-publish intent, not a post-publish record; the pinned-Friday
      hold_until/priority is the calendar slot of record and is consumed).
      Exception: a hold_until/pin dated AFTER the publish date survives as
      early-publish evidence for validate_queue rule 5 (R7).
  R4  CLI compat: the old `--published-date` flag still works and lands on
      `published_at`.
  R5  idempotence: re-running on an already-published card exits 1 and leaves
      the file byte-identical.
  R6  the written queue still passes scripts/validate_queue.py (mark_published
      validates before writing; a flip must not reopen the pin/hold defects).
  R7  breach tripwire (601d990): an EARLY flip keeps future-dated
      hold_until/priority so rule 5 can still fail CI; release_intent clears.
  R8  validator rule 8: a published record without well-formed published_at
      fails validation (the exact 2026-10-30 regression state).

    python3 scripts/test_mark_published.py

Exit 0 = every guard holds; exit 1 = a guard regressed.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "mark_published.py"
VALIDATOR = REPO / "scripts" / "validate_queue.py"

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = ""):
    status = "ok" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def make_queue(tmp: Path, rec: dict) -> Path:
    q = tmp / "content-research.jsonl"
    q.write_text(json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8")
    return q


def run_flip(queue: Path, slug: str, extra: list[str],
             validate: bool = False) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(SCRIPT), slug, "--file", str(queue)]
    if not validate:
        cmd.append("--no-validate")
    return subprocess.run(cmd + extra, capture_output=True, text=True)


def base_rec(**over) -> dict:
    rec = {
        "date": "2026-09-18",
        "slug": "test-slug-regression",
        "title": "Test card",
        "type": "article",
        "status": "pending",
        "langs": "de",  # the str form the script exists to normalize
        "hold_until": "2026-10-30",
        "priority": "pin-2026-10-30",
        "release_intent": "2026-11-02",
    }
    rec.update(over)
    return rec


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)

        # R1 + R2 + R3 + R4: one flip, canonical flag off (default today),
        # checked for schema key, wrong-key removal and stale-field clearing.
        q = make_queue(tmp, base_rec())
        r = run_flip(q, "test-slug-regression",
                     ["--langs", "de,en", "--published-at", "2026-10-30"])
        check("flip exits 0", r.returncode == 0, r.stderr)
        rec = json.loads(q.read_text(encoding="utf-8"))
        check("R1 flip writes published_at (schema field)",
              rec.get("published_at") == "2026-10-30",
              f"got published_at={rec.get('published_at')!r}")
        check("R1 flip does NOT write published_date",
              "published_date" not in rec)
        check("R2 pre-existing wrong key published_date never survives a flip",
              "published_date" not in rec)
        check("R3 hold_until cleared on flip", "hold_until" not in rec,
              repr(rec.get("hold_until")))
        check("R3 priority cleared on flip", "priority" not in rec,
              repr(rec.get("priority")))
        check("R3 release_intent cleared on flip", "release_intent" not in rec,
              repr(rec.get("release_intent")))
        check("langs normalized to list", rec.get("langs") == ["de", "en"],
              repr(rec.get("langs")))

        # R4: legacy alias --published-date still accepted, lands on published_at
        q2 = make_queue(tmp, base_rec(slug="test-slug-alias"))
        r2 = run_flip(q2, "test-slug-alias",
                      ["--langs", "de", "--published-date", "2026-10-29"])
        check("R4 legacy --published-date exits 0", r2.returncode == 0, r2.stderr)
        rec2 = json.loads(q2.read_text(encoding="utf-8"))
        check("R4 legacy flag stamps published_at",
              rec2.get("published_at") == "2026-10-29"
              and "published_date" not in rec2)

        # R5: idempotence on an already-published card
        before = q.read_bytes()
        r3 = run_flip(q, "test-slug-regression",
                      ["--langs", "de,en", "--published-at", "2026-10-30"])
        check("R5 re-run on published card exits 1", r3.returncode == 1,
              f"rc={r3.returncode}")
        check("R5 re-run leaves file byte-identical", q.read_bytes() == before)

        # R6: a flipped queue passes the validator (no --no-validate)
        q3 = make_queue(tmp, base_rec(slug="test-slug-validated"))
        r4 = run_flip(q3, "test-slug-validated",
                      ["--langs", "de", "--published-at", "2026-10-30"],
                      validate=True)
        check("R6 flip with validator enabled exits 0", r4.returncode == 0,
              r4.stdout + r4.stderr)

        # R7 (601d990 tripwire): flipping EARLY (hold_until/pin after the
        # publish date) must KEEP those fields as breach evidence so
        # validate_queue rule 5 still fires; release_intent always clears.
        rec7 = base_rec(slug="test-slug-breach", hold_until="2026-12-18",
                        priority="pin-2026-12-18", release_intent="2026-11-02")
        q7 = make_queue(tmp, rec7)
        r7 = run_flip(q7, "test-slug-breach",
                      ["--langs", "de", "--published-at", "2026-10-30"])
        got7 = json.loads(q7.read_text(encoding="utf-8"))
        check("R7 early flip keeps future hold_until/pin, drops release_intent",
              r7.returncode == 0 and got7.get("hold_until") == "2026-12-18"
              and got7.get("priority") == "pin-2026-12-18"
              and "release_intent" not in got7,
              f"got={got7!r} rc={r7.returncode} err={r7.stderr}")

        # R8 (null-check tripwire): validator rejects published w/o published_at
        rec8 = {"slug": "test-slug-nullstamp", "status": "published",
                "priority": "none", "published_date": "2026-10-30"}
        q8 = tmp / "queue-r8.jsonl"
        q8.write_text(json.dumps(rec8, ensure_ascii=False) + "\n", encoding="utf-8")
        r8 = subprocess.run([sys.executable, str(VALIDATOR), "--file", str(q8)],
                            capture_output=True, text=True)
        check("R8 validator fails published w/o published_at",
              r8.returncode == 1 and "published_at" in r8.stdout,
              f"rc={r8.returncode} out={r8.stdout!r}")

    print()
    if FAILURES:
        print(f"test_mark_published: {len(FAILURES)} guard(s) REGRESSED: "
              + ", ".join(FAILURES))
        return 1
    print("test_mark_published: all guards hold (R1-R8)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
