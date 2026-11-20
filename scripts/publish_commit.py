#!/usr/bin/env python3
"""Canonical commit wrapper for BOTH publish streams (cards t_a0e122fe, t_80f46bde).

Rework t_80f46bde (2026-11-06): the Friday-09:00 publish cron bypassed this
wrapper with raw `git commit` and pushed two uncarded commits (136f31a
"content: <slug> (de/en/fr/it)" and eda011c "build: latest strip, sitemap,
search-index for <slug>"). Root cause: the rule and the wrapper only covered
the 06:30 stream's `content:`/`search-index:` shapes. From now on every
publish-lane commit shape — the 06:30 stream AND the Friday-09:00 stream
(incl. the `build:` regen commit and the slash-lang subject form) — must be
produced here; there is still no free-message path.

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
  * `content --slash-lang` emits the Friday-lane subject form
    "content: <slug> (de/en/fr/it)" (136f31a-style) instead of the
    comma form — both are wrapper-produced and stamped.
  * `build <slug>` stages the Friday regen set (homepage latest strips
    x4, all sitemaps incl. root, the search index) and emits
    "build: latest strip, sitemap, search-index for <slug>" (eda011c-style).
  * `search-index` stages exactly assets/search-index.js.
  * Both refuse to create an empty commit and never push — the host
    flow pushes main + refs/notes after the CI gate passes.
  * Stdlib only; host-side (python3). Skips staging a path git does not
    know about AND that does not exist on disk (a publish that touched
    fewer pages than the default set must still commit).

Completion gate `gate` (t_651281a3, 2026-11-20): the Friday-09:00 run of
cron c431b4839129 stored status=completed / delivery_outcome=delivered
while its entire response was an 86-char command echo — nothing was built,
committed or pushed, the pin (days_until=0) silently slipped and the
human-visible publish slot went empty (live page 404, next auto run a full
week later). A 'delivered' executions row cannot be trusted as publish
proof, so the run now ends with a machine check that no cooperative agent
can pass falsely: if the picker still reports a pick whose pinned slot is
due (days_until <= 0) and no commit touching <slug>.html has landed on
origin/main (root blob absent, or still carrying noindex draft meta), the
gate prints "PUBLISH_SLIP <slug>" and exits 4 — the cron prompt turns a
non-zero gate into a [CRON_FAILURE] delivery, so the false-green shape is
no longer producible end-to-end. The uncooperative-agent residual (an run
that never even runs the gate) is covered by the daily
publish_calendar.py --watchdog (PIN_SLIPPED), t_651281a3 AC2.

Usage (from repo root, publish day, after mark_published.py + the page
build + gen_search_index have written the working tree):
    # 06:30 stream:
    python3 scripts/publish_commit.py content <slug> --langs de,en,fr,it
    python3 scripts/publish_commit.py search-index
    # Friday-09:00 stream (t_80f46bde): slash-lang subject + build regen
    python3 scripts/publish_commit.py content <slug> --slash-lang \
        --files data/audience_map.json scripts/_publish_<date>_<slug>.py
    python3 scripts/publish_commit.py build <slug>
    # run that belongs to a specific card instead of the anchor:
    python3 scripts/publish_commit.py content <slug> --card t_6544e449
    # MANDATORY final step of every publish cron run (t_651281a3):
    python3 scripts/publish_commit.py gate

Exit codes: 0 commit created / gate OK, 1 usage/validation refusal,
2 git error, 4 PUBLISH_SLIP (due pick with nothing landed on origin/main).
"""
from __future__ import annotations

import argparse
import json
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
        "sitemap.xml",
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


def build_paths(slug: str) -> list[str]:
    """File set of the Friday regen commit (eda011c shape): the generated
    homepage latest strips, every sitemap, and the search index. Paths the
    run did not touch are skipped by stage(); --files extends the set."""
    return [
        "index.html",
        "en/index.html",
        "fr/index.html",
        "it/index.html",
        "sitemap.xml",
        "sitemap-de.xml",
        "sitemap-en.xml",
        "sitemap-fr.xml",
        "sitemap-it.xml",
        SEARCH_INDEX_PATH,
    ]


# ---------------------------------------------------------------------------
# Completion gate (t_651281a3): prove the run's artifact actually landed
# ---------------------------------------------------------------------------
GATE_SLIP_EXIT = 4
LANG_MIRRORS = ("en", "fr", "it")


def pick_json(queue: str, calendar: str, today: str | None):
    """Run the picker (same deterministic rules the publish lane used) and
    return its JSON document, or None on failure (message already printed)."""
    picker = REPO / "scripts" / "publish_picker.py"
    cmd = [sys.executable, str(picker), "--queue", queue, "--calendar", calendar]
    if today:
        cmd += ["--today", today]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"gate: publish_picker exited {res.returncode}: "
              f"{res.stderr.strip()[:200]}", file=sys.stderr)
        return None
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError as exc:
        print(f"gate: unparsable picker output: {exc}", file=sys.stderr)
        return None


def resolve_ref(skip_fetch: bool, ref_override: str | None) -> str | None:
    """The pushed truth: origin/main after a fetch (falling back to any
    resolvable candidate). Never trusts the local working tree."""
    if not skip_fetch:
        git("fetch", "--quiet", "origin", "main")
    if ref_override:
        return ref_override
    for cand in ("origin/main", "origin/HEAD", "HEAD"):
        if git("rev-parse", "--verify", "-q", cand).returncode == 0:
            return cand
    return None


def landed_on_ref(ref: str, slug: str) -> tuple[bool, str]:
    """True iff a commit touching <slug>.html is on ref AND the page there
    is published (root blob exists, no mirror still carries noindex draft
    meta). A noindex blob is the drafted fast-lane shape — committed but
    deliberately NOT published, so it must not count as landing."""
    if not git("log", "-1", "--format=%H", ref, "--", f"{slug}.html").stdout.strip():
        return False, f"no commit touching {slug}.html on {ref}"
    r = git("show", f"{ref}:{slug}.html")
    if r.returncode != 0:
        return False, f"{slug}.html absent from {ref} tree"
    if "noindex" in r.stdout:
        return False, f"{slug}.html on {ref} still carries noindex draft meta"
    for lang in LANG_MIRRORS:
        probe = git("show", f"{ref}:{lang}/{slug}.html")
        if probe.returncode == 0 and "noindex" in probe.stdout:
            return False, f"{lang}/{slug}.html on {ref} still carries noindex draft meta"
    return True, "published blob on ref"


def due_pinned(doc: dict) -> list[dict]:
    """Entries the picker says are pinned AND due (days_until <= 0): the AC1
    condition. pick comes first; eligible is scanned too as a safety net,
    de-duplicated by slug."""
    out, seen = [], set()
    for e in [doc.get("pick")] + doc.get("eligible", []):
        if (e and e.get("pinned") and e.get("days_until") is not None
                and e["days_until"] <= 0 and e["slug"] not in seen):
            seen.add(e["slug"])
            out.append(e)
    return out


def gate(args) -> int:
    """AC1 (t_651281a3): a due pinned pick with nothing landed on origin/main
    must exit 4 printing PUBLISH_SLIP <slug>. A run that legitimately
    published nothing (pick null, or nothing due) passes OK."""
    doc = pick_json(args.queue, args.calendar, args.today)
    if doc is None:
        return 2
    due = due_pinned(doc)
    if not due:
        pick = doc.get("pick")
        print("PUBLISH_GATE OK: no due pinned pick "
              f"(pick={pick.get('slug') if pick else None})")
        return 0
    ref = resolve_ref(args.skip_fetch, args.ref)
    if ref is None:
        print("gate: cannot resolve origin/main ref", file=sys.stderr)
        return 2
    rc = 0
    for e in due:
        ok, why = landed_on_ref(ref, e["slug"])
        if ok:
            print(f"PUBLISH_GATE OK: {e['slug']} (slot {e['slot']}) landed on {ref}")
        else:
            print(f"PUBLISH_SLIP {e['slug']} (slot {e['slot']} "
                  f"days_until={e['days_until']}): {why}")
            rc = GATE_SLIP_EXIT
    return rc


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


def content_commit_message(slug: str, langs: list[str], card: str = PUBLISH_CARD,
                           slash_lang: bool = False) -> str:
    """Subject for a content publish.

    slash_lang=True emits the Friday-lane historical form
    "content: <slug> (de/en/fr/it)" (136f31a); the default comma form
    matches the 06:30 stream (f4fa476). Both go through stamped().
    """
    lang_str = ("/" if slash_lang else ",").join(langs) if langs else "de"
    return stamped(f"content: {slug} ({lang_str})", card)


def search_index_commit_message(card: str = PUBLISH_CARD) -> str:
    return stamped("search-index: refresh", card)


def build_commit_message(slug: str, card: str = PUBLISH_CARD) -> str:
    """Friday-lane regen subject (eda011c): latest strips + sitemaps + index."""
    return stamped(f"build: latest strip, sitemap, search-index for {slug}", card)


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
    c.add_argument("--slash-lang", action="store_true",
                   help="Friday-lane subject form '(de/en/fr/it)' instead of '(de,en,fr,it)'")
    c.add_argument("--files", action="append", default=[],
                   help="extra path to stage (repeatable), e.g. the generator script")
    c.add_argument("--card", default=PUBLISH_CARD)

    s = sub.add_parser("search-index", help="commit a search-index refresh")
    s.add_argument("--card", default=PUBLISH_CARD)

    b = sub.add_parser("build", help="commit the Friday regen set (latest strips, sitemaps, search index)")
    b.add_argument("slug")
    b.add_argument("--files", action="append", default=[],
                   help="extra path to stage (repeatable)")
    b.add_argument("--card", default=PUBLISH_CARD)

    g = sub.add_parser("gate", help="MANDATORY run-end completion gate (t_651281a3): "
                                    "PUBLISH_SLIP + exit 4 if a due pinned pick did not "
                                    "land on origin/main")
    g.add_argument("--queue", default=str(REPO / "data" / "content-research.jsonl"))
    g.add_argument("--calendar", default=str(REPO / "scripts" / "publish_calendar.py"))
    g.add_argument("--today", default=None, help="override today (tests/forensics)")
    g.add_argument("--ref", default=None, help="override landing ref (tests/forensics)")
    g.add_argument("--skip-fetch", action="store_true",
                   help="do not fetch origin first (tests/offline)")

    args = ap.parse_args(argv)

    if args.mode == "gate":
        return gate(args)
    if args.mode == "content":
        langs = normalize_langs(args.langs)
        msg = content_commit_message(args.slug, langs, args.card,
                                     slash_lang=args.slash_lang)
        rc = stage(default_content_paths(args.slug, langs) + args.files)
    elif args.mode == "build":
        msg = build_commit_message(args.slug, args.card)
        rc = stage(build_paths(args.slug) + args.files)
    else:
        msg = search_index_commit_message(args.card)
        rc = stage([SEARCH_INDEX_PATH])
    if rc != 0:
        return rc
    return commit(msg)


if __name__ == "__main__":
    sys.exit(main())
