#!/usr/bin/env python3
"""Canonical commit wrapper for the 06:30 publish stream (card t_a0e122fe).

Why this exists: t_d0820b72 card-stamped ONLY the maintenance stream
(publish_calendar.py MAINTENANCE_CARD), and its QA handoff named the
content/search-index commits an ownerless "other lane". Live probe
sweep-378 confirmed the gap: the 2026-10-30 publish push added e6a4672
("content: mwst-erhoehung-2027-ahv-armee (de/en/fr/it)") and cad7eb3
("search-index: refresh") to origin/main with no (t_xxxxxxxx) stamp,
taking scripts/uncarded_commits.py from 1 uncarded (sweep 376) to 3.
Every future publish run would grow that stream — violating the fleet
stamp convention (t_45ab7c9f: every commit on main carries its card id,
either t_+8hex in the message or a retroactive note on
refs/notes/commits). From now on the publish step commits ONLY through
this script; like mark_published.py for the queue flip, it has no
free-message path, so an un-stamped publish commit is not producible.

Standing-anchor pattern (t_fcff6abc): the publish stream is produced by
the cron run itself, not by one specific ticket, so — exactly like the
research cron — every message carries the standing anchor card id
PUBLISH_CARD unless the run explicitly belongs to another card
(--card t_xxxxxxxx). This mirrors the retroactive annotations already
on refs/notes/commits ("standing cron anchor card ... per t_45ab7c9f").

Guarantees:
  * stamped() refuses any message that does not END with "(t_<8hex>)"
    using the same regex scripts/uncarded_commits.py audits with.
  * `content` stages the standard publish file set for a slug (article
    mirrors, index/ratgeber pages, sitemaps, the queue flip) plus any
    extra --files (e.g. the one-off generator script under scripts/).
  * `search-index` stages exactly assets/search-index.js.
  * Both refuse to create an empty commit and never push — the host
    flow pushes main + refs/notes after the CI gate passes.
  * Stdlib only; host-side (python3). Skips staging a path git does not
    know about AND that does not exist on disk (a publish that touched
    fewer pages than the default set must still commit).

Usage (from repo root, publish day, after mark_published.py + the page
build + gen_search_index have written the working tree):
    python3 scripts/publish_commit.py content <slug> --langs de,en,fr,it
    python3 scripts/publish_commit.py search-index
    # run that belongs to a specific card instead of the anchor:
    python3 scripts/publish_commit.py content <slug> --card t_6544e449

Exit codes: 0 commit created, 1 usage/validation refusal, 2 git error.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Standing anchor card for the publish stream (same convention the research
# cron and its retroactive notes use; see module docstring / t_45ab7c9f).
PUBLISH_CARD = "t_fcff6abc"

# MUST stay byte-identical in semantics to scripts/uncarded_commits.py
# CARD_RE — a message accepted here must be recognised as carded there.
CARD_RE = re.compile(r"\bt_[0-9a-f]{8}\b")

SEARCH_INDEX_PATH = "assets/search-index.js"


def default_content_paths(slug: str, langs: list[str]) -> list[str]:
    """The standard file set a `content:` publish commit touches.

    Derived from the real shape of e6a4672 (2026-10-30 publish): article
    mirrors (root = de), per-language index + ratgeber mirrors, the four
    sitemaps and the queue flip. Extra files (generator script,
    audience_map) are passed via --files by the run that produced them.
    """
    paths = [
        f"{slug}.html",
        "index.html",
        "ratgeber.html",
        "sitemap-de.xml",
        "sitemap-en.xml",
        "sitemap-fr.xml",
        "sitemap-it.xml",
        "data/content-research.jsonl",
    ]
    for lang in langs:
        if lang == "de":
            continue  # de is the root mirror
        paths += [
            f"{lang}/{slug}.html",
            f"{lang}/index.html",
            f"{lang}/ratgeber.html",
        ]
    return paths


def normalize_langs(value: str | list) -> list[str]:
    if isinstance(value, list):
        items = value
    else:
        items = re.split(r"[,\s]+", value.strip())
    seen, out = set(), []
    for it in items:
        it = it.strip().lower()
        if it and it not in seen:
            seen.add(it)
            out.append(it)
    return out


def stamped(message: str, card: str) -> str:
    """Return `message` ending in the card stamp, or refuse (exit 1).

    There is deliberately no way to reach git commit without passing
    through here with a valid card id.
    """
    if not CARD_RE.fullmatch(card):
        print(f"refusing: card id {card!r} is not t_+8hex", file=sys.stderr)
        sys.exit(1)
    msg = message.rstrip()
    if not msg:
        print("refusing: empty commit message", file=sys.stderr)
        sys.exit(1)
    if msg.endswith(f"({card})"):
        return msg
    return f"{msg} ({card})"


def content_commit_message(slug: str, langs: list[str], card: str = PUBLISH_CARD) -> str:
    lang_str = ",".join(langs) if langs else "de"
    return stamped(f"content: {slug} ({lang_str})", card)


def search_index_commit_message(card: str = PUBLISH_CARD) -> str:
    return stamped("search-index: refresh", card)


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)


def stage(paths: list[str]) -> int:
    """git add every path that exists or is already tracked. Return staged count."""
    tracked = set(
        git("ls-files").stdout.splitlines()
    )
    addable = [p for p in paths if (REPO / p).exists() or p in tracked]
    missing = [p for p in paths if p not in addable]
    for m in missing:
        print(f"note: skipping path not present/tracked: {m}")
    if not addable:
        print("refusing: none of the target paths exist — nothing to stage", file=sys.stderr)
        return 1
    res = git("add", "--", *addable)
    if res.returncode != 0:
        print(f"git add failed: {res.stderr.strip()}", file=sys.stderr)
        return 2
    staged = git("diff", "--cached", "--name-only").stdout.splitlines()
    if not staged:
        print("refusing: nothing changed — no empty commit", file=sys.stderr)
        return 1
    for line in staged:
        print(f"staged: {line}")
    return 0


def commit(message: str) -> int:
    res = git("commit", "-m", message)
    if res.returncode != 0:
        print(f"git commit failed: {res.stderr.strip() or res.stdout.strip()}", file=sys.stderr)
        return 2
    print(f"committed: {message}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="mode", required=True)

    c = sub.add_parser("content", help="commit a published article set")
    c.add_argument("slug")
    c.add_argument("--langs", default="de,en,fr,it")
    c.add_argument("--files", action="append", default=[],
                   help="extra path to stage (repeatable), e.g. the generator script")
    c.add_argument("--card", default=PUBLISH_CARD)

    s = sub.add_parser("search-index", help="commit a search-index refresh")
    s.add_argument("--card", default=PUBLISH_CARD)

    args = ap.parse_args(argv)

    if args.mode == "content":
        langs = normalize_langs(args.langs)
        msg = content_commit_message(args.slug, langs, args.card)
        rc = stage(default_content_paths(args.slug, langs) + args.files)
    else:
        msg = search_index_commit_message(args.card)
        rc = stage([SEARCH_INDEX_PATH])
    if rc != 0:
        return rc
    return commit(msg)


if __name__ == "__main__":
    sys.exit(main())
