#!/usr/bin/env python3
"""Size guard for data/content-research.jsonl (incident t_2ed95a27, 2026-11-11).

The queue file was truncated to 0 bytes twice in one morning when an
agent-side scratch script opened it with open(path, "w") — which truncates
ON OPEN — and then crashed (NameError) before writing anything back. Every
downstream sweep/cron metric (PINS, DUE) silently reads 0 from an empty
queue and the only rescue is git.

Two sanctioned modes:

  1. Library — used by auto_drain.py / mark_published.py:
        from jsonl_guard import shrink_rejected, guarded_replace
     * shrink_rejected(before_lines, after_lines, force, min_ratio=0.5)
       -> (bool, msg): True if the write would leave fewer than
       min_ratio * the current NON-EMPTY line count and --force is absent.
       The original file is never touched in that case.
     * guarded_replace(path, lines): temp + fsync + os.replace + post-write
       verification; on any mismatch the original bytes are restored and
       the call fails. A crash mid-write can therefore never truncate the
       real file.

  2. Wrapper CLI — REQUIRED for any agent-side rewrite of the queue
     (hand-editing the file or writing it from a scratch script bypasses
     every guard):
        python3 scripts/jsonl_guard.py --candidate /tmp/new.jsonl \
            [--file data/content-research.jsonl] [--force] [--dry-run]
     Checks the shrink floor, runs scripts/validate_queue.py against the
     candidate, then atomically replaces. Exit codes: 0 ok, 1 guard reject,
     2 usage/target error.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_QUEUE = os.path.join(REPO, "data", "content-research.jsonl")
VALIDATOR = os.path.join(REPO, "scripts", "validate_queue.py")
MIN_RATIO = 0.5
MIN_PROTECTED_BASE = 10  # below this many lines a shrink is plausible editing


def nonempty(lines):
    return sum(1 for l in lines if l.strip())


def shrink_rejected(lines_before, lines_after, force=False,
                    min_ratio=MIN_RATIO):
    """(bool, msg) — bool True means the write must NOT land."""
    before, after = nonempty(lines_before), nonempty(lines_after)
    if force:
        return False, f"size-guard: --force given ({before} -> {after} lines), allowed"
    if before < MIN_PROTECTED_BASE:
        return False, ""
    floor = math.ceil(before * min_ratio)
    if after < floor:
        return True, (f"size-guard: REFUSING to leave the file with {after} "
                      f"non-empty lines; floor is {floor} "
                      f"({int(min_ratio * 100)}% of current {before}). "
                      "Pass --force only if the shrink is intentional.")
    return False, ""


def _read_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, "rb") as fh:
        raw = fh.read()
    return raw.decode("utf-8").splitlines(keepends=True)


def guarded_replace(path, lines, encoding="utf-8"):
    """Atomic replace with post-write verification + in-memory restore.

    Returns (True, "") on success, (False, msg) on failure (original intact).
    """
    original_bytes = b""
    if os.path.exists(path):
        with open(path, "rb") as fh:
            original_bytes = fh.read()
    data = "".join(lines)
    if data and not data.endswith("\n"):
        data += "\n"
    payload = data.encode(encoding)
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".jsonguard_",
                               suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(payload)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except OSError as exc:
        if os.path.exists(tmp):
            os.unlink(tmp)
        if os.path.exists(path) and open(path, "rb").read() != original_bytes:
            with open(path, "wb") as fh:
                fh.write(original_bytes)
        return False, f"size-guard: write failed ({exc}); original restored"
    # post-write verification: on-disk content must equal what we wrote
    with open(path, "rb") as fh:
        now = fh.read()
    if now != payload:
        with open(path, "wb") as fh:
            fh.write(original_bytes)
        return False, ("size-guard: post-write verification mismatch; "
                       "original restored")
    return True, ""


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Size guard for the publish queue (see module docstring)",
        epilog="Agent-side rewrites of the publish queue MUST go through "
               "this wrapper or the guarded sanctioned scripts.")
    ap.add_argument("--candidate", required=True,
                    help="path to the fully-rewritten queue file to install")
    ap.add_argument("--file", default=DEFAULT_QUEUE,
                    help=f"target queue (default: {DEFAULT_QUEUE})")
    ap.add_argument("--force", action="store_true",
                    help="allow a >50%% shrink of the current file")
    ap.add_argument("--dry-run", action="store_true",
                    help="run all checks, write nothing")
    args = ap.parse_args(argv)

    try:
        before = _read_lines(args.file)
        after = _read_lines(args.candidate)
    except FileNotFoundError as exc:
        print(f"size-guard: cannot read target/candidate: {exc}",
              file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"size-guard: cannot read target/candidate: {exc}",
              file=sys.stderr)
        return 2

    rejected, msg = shrink_rejected(before, after, force=args.force)
    if msg:
        print(msg, file=sys.stderr)
    if rejected:
        return 1
    if not nonempty(after) and not args.force:
        print("size-guard: candidate is empty — refusing (use --force to "
              "acknowledge)", file=sys.stderr)
        return 1

    # every candidate line must be valid JSON before anything lands
    for i, line in enumerate(after, 1):
        if not line.strip():
            continue
        try:
            json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"size-guard: candidate line {i} is not valid JSON "
                  f"({exc}); refusing", file=sys.stderr)
            return 1

    res = subprocess.run([sys.executable, VALIDATOR, "--file",
                          args.candidate], capture_output=True, text=True)
    if res.returncode != 0:
        print((res.stdout + res.stderr).strip(), file=sys.stderr)
        print("size-guard: validate_queue rejected the candidate; target "
              "untouched", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"size-guard: dry-run OK ({nonempty(before)} -> "
              f"{nonempty(after)} lines); nothing written", file=sys.stderr)
        return 0

    ok, err = guarded_replace(args.file, after)
    if not ok:
        print(err, file=sys.stderr)
        return 1
    print(f"size-guard: replaced {args.file} ({nonempty(before)} -> "
          f"{nonempty(after)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
