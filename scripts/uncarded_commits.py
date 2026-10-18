#!/usr/bin/env python3
"""Audit origin/main for commits that carry no kanban card id (t_6884615a).

Convention (AGENTS.md / CLAUDE.md): every commit pushed to main must
reference its kanban card id -- ``t_`` + 8 hex chars -- in the commit
message. GitHub issue refs alone ("Pino #10") do NOT count.

A commit also counts as carded when a git note on it (default ref
``refs/notes/commits``) carries the card id; that is the retroactive
annotation channel for commits pushed before the convention existed, so
history never has to be rewritten.

Host-side, stdlib only. Reads the local clone; performs no network I/O --
fetch origin/main (and the notes ref, e.g.
``git fetch origin refs/notes/*:refs/notes/*``) before running.

Usage:
    python3 scripts/uncarded_commits.py [--repo PATH] [--ref origin/main]
                                        [-n 20] [--notes-ref commits]

Output: one line per commit -- short sha, the card id(s) found and where
(message or note), or UNCARDED. Exit code 0 if every checked commit is
carded, 1 if any is uncarded (so it can gate a host-side push flow).
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

CARD_RE = re.compile(r"\bt_[0-9a-f]{8}\b")


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )


def card_refs(text):
    return sorted(set(CARD_RE.findall(text or "")))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--repo",
        default=None,
        help="repo path (default: the repo containing this script)",
    )
    ap.add_argument("--ref", default="origin/main", help="branch/ref to audit")
    ap.add_argument(
        "-n",
        "--count",
        type=int,
        default=20,
        help="how many recent commits to check (default 20)",
    )
    ap.add_argument(
        "--notes-ref",
        default="commits",
        help="git notes ref consulted when the message has no card id "
        "(default: commits -> refs/notes/commits)",
    )
    args = ap.parse_args()

    repo = Path(args.repo) if args.repo else Path(__file__).resolve().parents[1]

    probe = git(repo, "rev-parse", "--verify", "--quiet", args.ref)
    if probe.returncode != 0:
        print(f"error: ref {args.ref!r} not found in {repo} (fetch first)", file=sys.stderr)
        return 2

    listing = git(repo, "log", f"-n{args.count}", "--format=%H%x00%s", args.ref)
    if listing.returncode != 0:
        print(f"error: git log failed: {listing.stderr.strip()}", file=sys.stderr)
        return 2

    entries = []
    for line in listing.stdout.splitlines():
        if not line.strip():
            continue
        sha, subject = line.split("\x00", 1)
        entries.append((sha, subject))

    uncarded = []
    for sha, subject in entries:
        msg = git(repo, "log", "-1", "--format=%B", sha).stdout
        cards = card_refs(msg)
        source = "message"
        if not cards:
            note = git(repo, "notes", "--ref", args.notes_ref, "show", sha)
            if note.returncode == 0:
                cards = card_refs(note.stdout)
                source = "note"
        short = sha[:7]
        if cards:
            print(f"{short}  carded ({source}): {', '.join(cards)}  | {subject[:72]}")
        else:
            print(f"{short}  UNCARDED  | {subject[:72]}")
            uncarded.append(short)

    print(
        f"\nchecked {len(entries)} commits on {args.ref}: "
        f"{len(entries) - len(uncarded)} carded, {len(uncarded)} uncarded"
        + (f" -> {', '.join(uncarded)}" if uncarded else "")
    )
    return 1 if uncarded else 0


if __name__ == "__main__":
    sys.exit(main())
