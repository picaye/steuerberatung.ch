#!/usr/bin/env python3
"""test_draft_leak_guards.py — regression tests for the grenzg draft-leak guards.

Guards under test (commit history of scripts/mksitemap.py + scripts/gen_latest.py):
  G1  noindex pages are skipped by mksitemap.py (bced659) AND gen_latest.py (a116adc)
  G2  slugs whose data/content-research.jsonl record is status:pending are
      skipped by BOTH scripts (17c892e) — tracked != published
  G3  untracked working-tree drafts are skipped by BOTH scripts (524483c)

The test builds a throwaway git repo in a temp dir, copies the two scripts
into it, runs them as the publish cron would, and asserts that only the
published page ends up in sitemap.xml and in the homepage LATEST strips.
Exit 0 = every guard holds; exit 1 = a guard leaked (with the failing
assertions listed).

    python3 scripts/test_draft_leak_guards.py

Self-contained: never touches the real repo's sitemap.xml or index.html.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"

ARTICLE_LD = (
    '<script type="application/ld+json">'
    '{"@type":"Article","headline":"%s","description":"test desc",'
    '"datePublished":"%s"}</script>'
)


def page(title: str, date: str, noindex: bool = False) -> str:
    robots = (
        '<meta name="robots" content="noindex, nofollow">\n' if noindex else ""
    )
    return (
        "<!DOCTYPE html>\n<html lang=\"de\">\n<head>\n"
        f'<title>{title}</title>\n{robots}'
        f"{ARTICLE_LD % (title, date)}\n"
        "</head>\n<body>\n<main>\n</main>\n</body>\n</html>\n"
    )


def index_page() -> str:
    return (
        "<!DOCTYPE html>\n<html lang=\"de\">\n<head><title>Home</title></head>\n"
        "<body>\n<main>\n"
        "<!-- LATEST:START -->\n<!-- LATEST:END -->\n"
        "</main>\n</body>\n</html>\n"
    )


def build_fixture(tmp: Path) -> None:
    """A mini site with one published page and three draft variants."""
    (tmp / "scripts").mkdir()
    for name in ("mksitemap.py", "gen_latest.py"):
        shutil.copy2(SCRIPTS / name, tmp / "scripts" / name)

    # published: tracked, indexable, status:published record
    (tmp / "published.html").write_text(page("Published", "2026-10-01"), encoding="utf-8")
    # draft A: tracked + noindex (G1)
    (tmp / "draft-noindex.html").write_text(page("Draft Noindex", "2026-10-05", noindex=True), encoding="utf-8")
    # draft B: tracked, indexable, but content-research status:pending (G2)
    (tmp / "draft-pending.html").write_text(page("Draft Pending", "2026-10-04"), encoding="utf-8")
    # draft C: in the working tree only, never committed (G3)
    (tmp / "draft-untracked.html").write_text(page("Draft Untracked", "2026-10-06"), encoding="utf-8")

    # en/ mirror: same pending slug must be skipped in the language dir too
    (tmp / "en").mkdir()
    (tmp / "en" / "published.html").write_text(page("Published EN", "2026-10-01"), encoding="utf-8")
    (tmp / "en" / "draft-pending.html").write_text(page("Draft Pending EN", "2026-10-04"), encoding="utf-8")

    (tmp / "index.html").write_text(index_page(), encoding="utf-8")
    (tmp / "en" / "index.html").write_text(index_page(), encoding="utf-8")

    (tmp / "data").mkdir()
    (tmp / "data" / "content-research.jsonl").write_text(
        json.dumps({"slug": "published", "status": "published"}) + "\n"
        + json.dumps({"slug": "draft-pending", "status": "pending"}) + "\n"
        + json.dumps({"slug": "draft-noindex", "status": "published"}) + "\n",  # noindex must win independently
        encoding="utf-8",
    )

    g = ["git", "-C", str(tmp)]
    subprocess.run(g + ["init", "-q"], check=True)
    subprocess.run(g + ["config", "user.email", "test@example.com"], check=True)
    subprocess.run(g + ["config", "user.name", "test"], check=True)
    subprocess.run(g + ["add", "scripts", "index.html", "en/index.html",
                        "published.html", "draft-noindex.html", "draft-pending.html",
                        "en/published.html", "en/draft-pending.html"], check=True)
    subprocess.run(g + ["commit", "-qm", "fixture"], check=True)
    # draft-untracked.html deliberately left uncommitted


def run_scripts(tmp: Path) -> tuple[str, str]:
    """Run both generators; return (sitemap.xml, concatenated index strips)."""
    for script in ("mksitemap.py", "gen_latest.py"):
        r = subprocess.run(
            [sys.executable, str(tmp / "scripts" / script)],
            capture_output=True, text=True, timeout=60,
        )
        if r.returncode != 0:
            raise RuntimeError(f"{script} failed rc={r.returncode}\n{r.stderr}")
    sitemap = (tmp / "sitemap.xml").read_text(encoding="utf-8")
    strips = ""
    for idx in (tmp / "index.html", tmp / "en" / "index.html"):
        html = idx.read_text(encoding="utf-8")
        m = re.search(r"<!-- LATEST:START -->.*?<!-- LATEST:END -->", html, re.S)
        strips += (m.group(0) if m else "")
    return sitemap, strips


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="draft-leak-guards-"))
    try:
        build_fixture(tmp)
        sitemap, strips = run_scripts(tmp)

        checks: list[tuple[str, bool]] = []

        def check(name: str, ok: bool) -> None:
            checks.append((name, ok))

        # positive controls: the published page must be present
        check("sitemap contains published.html", "/published.html" in sitemap)
        check("sitemap contains en/published.html", "/en/published.html" in sitemap)
        check("strips link published.html", 'href="published.html"' in strips)

        # G1 noindex
        check("G1 sitemap: no draft-noindex", "draft-noindex" not in sitemap)
        check("G1 strips: no draft-noindex", "draft-noindex" not in strips)
        # G2 status:pending
        check("G2 sitemap: no draft-pending", "draft-pending" not in sitemap)
        check("G2 strips: no draft-pending", "draft-pending" not in strips)
        # G3 untracked
        check("G3 sitemap: no draft-untracked", "draft-untracked" not in sitemap)
        check("G3 strips: no draft-untracked", "draft-untracked" not in strips)

        failed = [n for n, ok in checks if not ok]
        for name, ok in checks:
            print(("PASS  " if ok else "FAIL  ") + name)
        print(f"\n{len(checks) - len(failed)}/{len(checks)} assertions passed")
        if failed:
            print("FAILED GUARDS:")
            for n in failed:
                print("  -", n)
            print(f"\nfixture kept for inspection: {tmp}")
            return 1
        shutil.rmtree(tmp, ignore_errors=True)
        print("ALL DRAFT-LEAK GUARDS HOLD")
        return 0
    finally:
        pass


if __name__ == "__main__":
    sys.exit(main())
