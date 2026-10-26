#!/usr/bin/env python3
"""Canonical record-writer for publishing a queue card (card t_52601755).

Why this exists: publishes hand-edited data/content-research.jsonl inline,
and the 2026-10-23 publish wrote "langs": "de,en,fr,it" — a comma-joined
string — onto fairness-initiative-ehepaare-2026 while every other published
record carries a JSON list. validate_queue.py now rejects non-list langs
(Rule 6), so from now on the publish step marks cards ONLY through this
script, which cannot produce the broken shape.

Guarantees:
  * langs is always emitted as a JSON list of 2-letter codes ("de,en,fr,it"
    input is split for you; duplicates removed, order preserved).
  * exactly one line of the queue changes; anything else aborts the write.
  * the candidate file must pass scripts/validate_queue.py before it
    replaces the original (atomic replace).
  * serialization matches the queue convention: json.dumps(...,
    ensure_ascii=False), one record per line.

Usage (from repo root, on publish day, alongside building the pages):
    python3 scripts/mark_published.py <slug> --langs de,en,fr,it
    # override the stamp date if re-running for an earlier publish:
    python3 scripts/mark_published.py <slug> --langs de,en,fr,it --published-date 2026-10-23

Exit codes: 0 written, 1 usage/validation failure, 2 file/format error.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_QUEUE = str(REPO / "data" / "content-research.jsonl")
VALIDATOR = str(REPO / "scripts" / "validate_queue.py")


def normalize_langs(value: str | list) -> list[str]:
    """Coerce any plausible langs input into an ordered, deduped list."""
    if isinstance(value, list):
        parts = [str(v) for v in value]
    else:
        parts = str(value).replace(";", ",").split(",")
    out: list[str] = []
    for p in parts:
        code = p.strip().lower()
        if not code:
            continue
        if len(code) != 2 or not code.isalpha():
            raise ValueError(f"not a 2-letter language code: {p!r}")
        if code not in out:
            out.append(code)
    if not out:
        raise ValueError("langs resolved to an empty list")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("slug", help="queue card slug to mark published")
    ap.add_argument("--langs", required=True,
                    help='published language set, e.g. "de,en,fr,it" '
                         '(always written as a JSON list)')
    ap.add_argument("--published-date", default=None,
                    help="YYYY-MM-DD stamp (default: today)")
    ap.add_argument("--file", default=DEFAULT_QUEUE)
    args = ap.parse_args(argv)

    try:
        langs = normalize_langs(args.langs)
    except ValueError as exc:
        print(f"mark_published: bad langs: {exc}", file=sys.stderr)
        return 1

    if args.published_date:
        try:
            dt.date.fromisoformat(args.published_date)
        except ValueError:
            print("mark_published: --published-date must be YYYY-MM-DD",
                  file=sys.stderr)
            return 1
        stamp = args.published_date
    else:
        stamp = dt.date.today().isoformat()

    path = Path(args.file)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"mark_published: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    hits = []
    for idx, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"mark_published: {path} line {idx + 1} is not valid JSON: {exc}",
                  file=sys.stderr)
            return 2
        if isinstance(rec, dict) and rec.get("slug") == args.slug and rec.get("status"):
            hits.append((idx, rec))

    if len(hits) != 1:
        print(f"mark_published: expected exactly 1 card with slug {args.slug!r}, "
              f"found {len(hits)} — aborting", file=sys.stderr)
        return 1
    idx, rec = hits[0]
    if rec.get("status") == "published":
        print(f"mark_published: {args.slug} is already "
              f"published_date={rec.get('published_date', rec.get('published_at'))!r} "
              f"langs={rec.get('langs')!r} — nothing to do", file=sys.stderr)
        return 1

    rec["status"] = "published"
    rec["published_date"] = stamp
    rec["langs"] = langs  # list, always — this is the whole point of the script

    new_line = json.dumps(rec, ensure_ascii=False)
    old_lines = list(lines)
    lines[idx] = new_line
    changed = [i + 1 for i in range(len(lines)) if lines[i] != old_lines[i]]
    if changed != [idx + 1] or len(lines) != len(old_lines):
        print(f"mark_published: sanity check failed — would change lines {changed}; "
              "aborting", file=sys.stderr)
        return 1

    # Write a temp sibling, validate it, then atomically replace.
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".mark_pub_",
                               suffix=".jsonl")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + ("\n" if any(l.strip() for l in old_lines) else ""))
        res = subprocess.run([sys.executable, VALIDATOR, "--file", tmp],
                             capture_output=True, text=True)
        if res.returncode != 0:
            print((res.stdout + res.stderr).strip(), file=sys.stderr)
            print("mark_published: validator rejected the candidate file; "
                  "original untouched", file=sys.stderr)
            return 1
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

    print(f"mark_published: line {idx + 1} {args.slug} -> "
          f"status=published published_date={stamp} langs={langs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
