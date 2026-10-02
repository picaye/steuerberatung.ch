#!/usr/bin/env python3
"""Backfill the 'Verwandte Artikel' block into the 18 root DE articles.

Idempotent and re-runnable: the block lives between
<!-- RELATED:START --> / <!-- RELATED:END --> markers just before </main>;
a re-run replaces the existing block in place. Root DE only — no en/fr/it
fan-out (per gh:picaye/steuerberatung.ch#1 scope).

Usage: python3 scripts/backfill_related.py [--check]
  --check: report what would change, write nothing.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import article_template as at  # noqa: E402

RELATED_RE = re.compile(
    re.escape(at.RELATED_START) + r".*?" + re.escape(at.RELATED_END), re.S)


def articles():
    return sorted(
        f for f in os.listdir(at.BASE)
        if f.endswith(".html")
        and '"@type": "Article"' in open(os.path.join(at.BASE, f), encoding="utf-8").read())


def main():
    check = "--check" in sys.argv
    m = at.load_related_map()
    slugs = articles()

    # --- validate the map before touching anything ---
    problems = []
    for s in slugs:
        rel = m.get(s)
        if rel is None:
            problems.append(f"{s}: missing from related_map.json")
            continue
        if len(rel) != 3:
            problems.append(f"{s}: {len(rel)} related links (want 3)")
        if s in rel:
            problems.append(f"{s}: self-link")
        for r in rel:
            if not os.path.exists(os.path.join(at.BASE, r)):
                problems.append(f"{s}: related target does not exist: {r}")
    for s in m:
        if s not in slugs:
            problems.append(f"related_map has stale key (not a DE article): {s}")
    if problems:
        print("MAP PROBLEMS:")
        for p in problems:
            print(" -", p)
        sys.exit(1)

    changed = 0
    for s in slugs:
        path = os.path.join(at.BASE, s)
        doc = open(path, encoding="utf-8").read()
        block = at.render_related("de", m[s])
        if RELATED_RE.search(doc):
            new = RELATED_RE.sub(lambda _: block, doc, count=1)
        else:
            if "</main>" not in doc:
                print(f"{s}: no </main> — skipped")
                continue
            new = doc.replace("</main>", block + "\n</main>", 1)
        if new != doc:
            changed += 1
            print(("would update: " if check else "updated: ") + s)
            if not check:
                open(path, "w", encoding="utf-8").write(new)
        else:
            print("already current:" if check else "unchanged:   ", s)
    print(f"{changed}/{len(slugs)} pages {'would change' if check else 'changed'}")


if __name__ == "__main__":
    main()
