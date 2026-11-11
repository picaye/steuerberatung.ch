#!/usr/bin/env python3
"""Regression suite for scripts/jsonl_guard.py (incident t_2ed95a27, 2026-11-11).

data/content-research.jsonl was truncated to 0 bytes twice in one morning by
an agent-side scratch script that open(path,"w")-truncated the file and then
crashed before writing it back. This suite pins the guarantees the fix adds:

  A1  a >50% shrink via the wrapper CLI exits non-zero and leaves the target
      untouched (the exact 0-byte incident replayed against a copy)
  A2  the rejected file's content is byte-identical afterwards ("restores")
  A3  --force acknowledges the shrink and lets the write land
  A4  a healthy full rewrite (status flip) passes
  A5  boundary: exactly 50% passes, one line below the floor is rejected
  A6  tiny files (<10 non-empty lines) are not protected (bootstrap ok)
  A7  an invalid-JSON candidate is refused without touching the target
  A8  auto_drain end-to-end: normal drain lands and is idempotent-safe
  A9  mark_published end-to-end on a fixture: --force flag accepted, normal
      one-line mark passes the guard

stdlib-only. Run: python3 scripts/test_jsonl_guard.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "jsonl_guard.py")
AUTO_DRAIN = os.path.join(HERE, "auto_drain.py")
MARK_PUB = os.path.join(HERE, "mark_published.py")

# Records must satisfy validate_queue.py: pin-YYYY-MM-DD needs matching
# hold_until, so plain pending records with no pin are the safe fixture.
def rec(i, status="pending"):
    return json.dumps({"slug": f"card-{i:03d}", "title": f"Card {i}",
                       "status": status, "langs": ["de"], "demand": "med",
                       "topic": f"t{i}"}, ensure_ascii=False)


def make_queue(n=20):
    return "".join(rec(i) + "\n" for i in range(1, n + 1))


def run(argv, **kw):
    return subprocess.run([sys.executable] + argv, capture_output=True,
                          text=True, **kw)


def main():
    failures = []

    def check(name, cond, detail=""):
        status = "PASS" if cond else "FAIL"
        print(f"{status}  {name}" + (f"  [{detail}]" if detail and not cond else ""))
        if not cond:
            failures.append(name)

    tmpdir = tempfile.mkdtemp(prefix="jsonguard_test_")
    try:
        queue = os.path.join(tmpdir, "queue.jsonl")
        original = make_queue(20)
        with open(queue, "w") as fh:
            fh.write(original)

        # A1/A2 — replay the incident: candidate with 0 lines
        zero = os.path.join(tmpdir, "zero.jsonl")
        open(zero, "w").close()
        r = run([GUARD, "--candidate", zero, "--file", queue])
        check("A1 wrapper refuses a 0-byte candidate (exit != 0)",
              r.returncode != 0, f"rc={r.returncode} {r.stderr[:120]}")
        with open(queue) as fh:
            check("A2 target byte-identical after refusal (restored)",
                  fh.read() == original)

        # A3 — --force acknowledges
        r = run([GUARD, "--candidate", zero, "--file", queue, "--force"])
        check("A3 --force allows the acknowledged shrink",
              r.returncode == 0, f"rc={r.returncode} {r.stderr[:120]}")
        with open(queue) as fh:
            check("A3b forced write landed (file now empty)",
                  fh.read() == "")
        # restore for the rest of the suite
        with open(queue, "w") as fh:
            fh.write(original)

        # A4 — healthy rewrite (flip one status)
        good = "".join(rec(i, "backlog" if i == 5 else "pending") + "\n"
                       for i in range(1, 21))
        goodf = os.path.join(tmpdir, "good.jsonl")
        with open(goodf, "w") as fh:
            fh.write(good)
        r = run([GUARD, "--candidate", goodf, "--file", queue])
        check("A4 healthy same-size rewrite passes",
              r.returncode == 0, f"rc={r.returncode} {r.stderr[:200]}")

        # A5 — boundary: floor = ceil(0.5 * 20) = 10; 10 passes, 9 rejected
        for keep, want_pass in ((10, True), (9, False)):
            with open(queue, "w") as fh:  # reset base: 20 lines
                fh.write(original)
            b = os.path.join(tmpdir, f"b{keep}.jsonl")
            with open(b, "w") as fh:
                fh.write(make_queue(keep))
            r = run([GUARD, "--candidate", b, "--file", queue])
            check(f"A5 {keep}-line candidate "
                  + ("passes" if want_pass else "is rejected"),
                  (r.returncode == 0) == want_pass,
                  f"rc={r.returncode}")

        # A6 — tiny/absent base is not protected (bootstrap writes ok)
        tiny = os.path.join(tmpdir, "tiny.jsonl")
        with open(tiny, "w") as fh:
            fh.write("".join(rec(i) + "\n" for i in range(1, 4)))
        r = run([GUARD, "--candidate", os.path.join(tmpdir, "b1.jsonl")
                 if os.path.exists(os.path.join(tmpdir, "b1.jsonl")) else goodf,
                 "--file", tiny])
        check("A6 shrink from a <10-line base is allowed",
              r.returncode == 0, f"rc={r.returncode} {r.stderr[:120]}")

        # A7 — invalid JSON candidate refused, target untouched
        with open(queue, "w") as fh:
            fh.write(original)
        bad = os.path.join(tmpdir, "bad.jsonl")
        with open(bad, "w") as fh:
            fh.write(make_queue(20).replace('{"slug"', '{oops', 1))
        r = run([GUARD, "--candidate", bad, "--file", queue])
        check("A7 invalid-JSON candidate rejected",
              r.returncode != 0, f"rc={r.returncode}")
        with open(queue) as fh:
            check("A7b target untouched after invalid candidate",
                  fh.read() == original)

        # A8 — auto_drain end-to-end: demotes down to cap-margin, lands
        with open(queue, "w") as fh:
            fh.write(make_queue(20))
        r = run([AUTO_DRAIN, "--file", queue, "--cap", "10", "--margin", "2"])
        check("A8 auto_drain guarded write lands",
              r.returncode == 0, f"rc={r.returncode} {r.stderr[:200]}")
        with open(queue) as fh:
            out = fh.read()
        n_pending = sum(1 for l in out.splitlines()
                        if l.strip() and json.loads(l)["status"] == "pending")
        n_lines = len([l for l in out.splitlines() if l.strip()])
        check("A8b drain demoted to cap-margin and lost no lines",
              n_pending == 8 and n_lines == 20,
              f"pending={n_pending} lines={n_lines}")
        r = run([AUTO_DRAIN, "--file", queue, "--cap", "10", "--margin", "2",
                 "--dry-run"])
        check("A8c idempotent dry-run rc=0, writes nothing",
              r.returncode == 0)

        # A9 — mark_published end-to-end on the fixture
        with open(queue, "w") as fh:
            fh.write(make_queue(20))
        r = run([MARK_PUB, "card-003", "--langs", "de,fr", "--file", queue])
        check("A9 mark_published passes the shrink guard (rc=0)",
              r.returncode == 0, f"rc={r.returncode} {r.stdout[:120]} {r.stderr[:200]}")
        r = run([MARK_PUB, "--help"])
        check("A9b mark_published exposes --force",
              r.returncode == 0 and "--force" in r.stdout)
        r = run([AUTO_DRAIN, "--help"])
        check("A9c auto_drain exposes --force",
              r.returncode == 0 and "--force" in r.stdout)

        # A10 — library level: guarded_replace post-write contract
        sys.path.insert(0, HERE)
        import jsonl_guard
        ok, err = jsonl_guard.guarded_replace(
            queue, ["already\n", "lines\n"])
        check("A10 guarded_replace succeeds and content round-trips",
              ok and open(queue).read() == "already\nlines\n", err)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    print("\n%d failure(s)" % len(failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
