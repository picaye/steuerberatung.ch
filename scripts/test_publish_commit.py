#!/usr/bin/env python3
"""Regression suite for scripts/publish_commit.py — run: python3 scripts/test_publish_commit.py (CI gate: .github/workflows/pages.yml).

Card t_a0e122fe: the publish stream's content/search-index commits shipped
without card stamps (2026-10-30: e6a4672 + cad7eb3 took uncarded_commits.py
from 1 to 3). t_d0820b72 stamped only the maintenance stream. These checks
lock the two properties that keep the stream carded:

  C1  PUBLISH_CARD is the standing anchor and a valid card id.
  C2  both message builders ALWAYS end in a stamp that
      scripts/uncarded_commits.py would recognise (CARD_RE semantics).
  C3  stamped() cannot be steered into an un-stamped or double-stamped
      message, and rejects malformed card ids.
  C4  the CLI has no free-message path (argparse surface).
  C5  behaviour: a real `content` commit in a throwaway git repo lands
      stamped (t_fcff6abc) and stages the expected file set.
  C6  behaviour: `search-index` commits exactly assets/search-index.js
      stamped, and refuses an empty second run instead of committing.
  C7  behaviour (t_80f46bde): `content --slash-lang` lands the Friday-lane
      subject "content: <slug> (de/en/fr/it) (t_fcff6abc)" — byte-equal to
      136f31a's subject apart from the stamp.
  C8  behaviour (t_80f46bde): `build <slug>` lands "build: latest strip,
      sitemap, search-index for <slug> (t_fcff6abc)" and stages exactly the
      regen set the run touched — byte-equal to eda011c's subject + stamp.

Stdlib only — the check runs the publish-commit path end to end in a temp
repo. git is required (skips with rc 0 when absent, same as the other
suites' tolerance for CI images without git config).
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import publish_commit as pc  # noqa: E402


def _load_uncarded_audit():
    spec = importlib.util.spec_from_file_location(
        "uncarded_commits", str(HERE / "uncarded_commits.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _git(cwd: Path, *args: str) -> str:
    env = {**__import__("os").environ,
           "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    res = subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                         text=True, env=env)
    if res.returncode != 0:
        raise AssertionError(f"git {' '.join(args)}: {res.stderr}")
    return res.stdout


def _make_repo(root: Path) -> Path:
    repo = root / "repo"
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "publish-commit-test")
    # publish_commit anchors REPO at its own file location; install the
    # real script into the throwaway repo so the CLI targets this repo.
    (repo / "scripts").mkdir()
    shutil.copy(HERE / "publish_commit.py", repo / "scripts" / "publish_commit.py")
    return repo


def main() -> int:
    audit = _load_uncarded_audit()
    results: list[tuple[str, str]] = []

    # C1 standing anchor identity
    assert pc.PUBLISH_CARD == "t_fcff6abc", pc.PUBLISH_CARD
    assert audit.CARD_RE.fullmatch(pc.PUBLISH_CARD), \
        "PUBLISH_CARD must be recognised by the uncarded audit"
    results.append(("C1", "PUBLISH_CARD is the t_fcff6abc anchor and matches the audit CARD_RE"))

    # C2 builders always stamp, on every input shape
    msgs = [
        pc.content_commit_message("mwst-erhoehung-2027-ahv-armee", ["de", "en", "fr", "it"]),
        pc.content_commit_message("x", []),
        pc.content_commit_message("y", ["de"], card="t_6544e449"),
        pc.search_index_commit_message(),
        pc.search_index_commit_message(card="t_6544e449"),
        pc.content_commit_message("stille-reserven", ["de", "en", "fr", "it"], slash_lang=True),
        pc.build_commit_message("stille-reserven"),
        pc.build_commit_message("z", card="t_6544e449"),
    ]
    for m in msgs:
        assert re.search(r"\(t_[0-9a-f]{8}\)$", m), m
        assert audit.CARD_RE.search(m), m
    assert msgs[0] == "content: mwst-erhoehung-2027-ahv-armee (de,en,fr,it) (t_fcff6abc)", msgs[0]
    assert msgs[3] == "search-index: refresh (t_fcff6abc)", msgs[3]
    assert msgs[5] == "content: stille-reserven (de/en/fr/it) (t_fcff6abc)", msgs[5]
    assert msgs[6] == "build: latest strip, sitemap, search-index for stille-reserven (t_fcff6abc)", msgs[6]
    results.append(("C2", "content/search-index/build/slash-lang builders all end in an audit-recognised stamp"))

    # C3 stamped() invariants
    assert pc.stamped("foo (t_11111111)", "t_11111111") == "foo (t_11111111)"  # no double stamp
    assert pc.stamped("foo (t_22222222)", "t_11111111") == "foo (t_22222222) (t_11111111)"
    for bad in ("", "   "):
        try:
            pc.stamped(bad, pc.PUBLISH_CARD)
        except SystemExit as e:
            assert e.code == 1, e.code
        else:
            raise AssertionError(f"empty message accepted: {bad!r}")
    for bad_card in ("fcff6abc", "t_fcff6abc1", "t_FCFF6ABC", "T_fcff6abc", "t_fcff6abg"):
        try:
            pc.stamped("msg", bad_card)
        except SystemExit as e:
            assert e.code == 1, e.code
        else:
            raise AssertionError(f"malformed card accepted: {bad_card!r}")
    results.append(("C3", "stamped(): no empty msg, no double stamp, malformed card ids refused"))

    # C4 no free-message surface on the CLI
    src = (HERE / "publish_commit.py").read_text(encoding="utf-8")
    assert not re.search(r'add_argument\(\s*"-{1,2}m(essage)?"', src), \
        "CLI must not expose a raw commit-message option"
    assert re.search(r'git\("commit", "-m", message\)', src), src
    results.append(("C4", "CLI commits only builder-produced messages (no free-message path)"))

    if shutil.which("git") is None:
        for name in ("C5", "C6", "C7", "C8"):
            results.append((name, "skipped: git unavailable"))
    else:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _make_repo(root)
            slug = "mwst-erhoehung-2027-ahv-armee"
            for p in [f"{slug}.html", "index.html", "ratgeber.html",
                      "en/index.html", "en/ratgeber.html", f"en/{slug}.html",
                      "data/content-research.jsonl", "sitemap-de.xml",
                      "sitemap-en.xml", "sitemap-fr.xml", "sitemap-it.xml",
                      "fr/index.html", f"fr/{slug}.html", "fr/ratgeber.html",
                      "it/index.html", f"it/{slug}.html", "it/ratgeber.html",
                      "assets/search-index.js"]:
                f = repo / p
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text("x\n")
            _git(repo, "add", "-A")
            _git(repo, "commit", "-qm", "seed (t_99999999)")
            # mutate the publish set + an unrelated file that must NOT be staged
            (repo / f"{slug}.html").write_text("new page\n")
            (repo / "data/content-research.jsonl").write_text('{"slug": "%s"}\n' % slug)
            (repo / "unrelated.txt").write_text("do not touch\n")
            (repo / "index.html").write_text("new index\n")
            res = subprocess.run(
                [sys.executable, str(repo / "scripts" / "publish_commit.py"),
                 "content", slug, "--langs", "de,en,fr,it"],
                capture_output=True, text=True, cwd=repo)
            assert res.returncode == 0, res.stderr
            msg = _git(repo, "log", "-1", "--format=%s").strip()
            assert msg == f"content: {slug} (de,en,fr,it) (t_fcff6abc)", msg
            files = set(_git(repo, "show", "--name-only", "--format=", "HEAD").split())
            assert files == {f"{slug}.html", "index.html", "data/content-research.jsonl"}, files
            assert (repo / "unrelated.txt").exists()  # untouched, still untracked
            results.append(("C5", "real content commit lands stamped with the exact e6a4672-style subject"))

            # C6 search-index behaviour
            (repo / "assets/search-index.js").write_text("// idx\n")
            res = subprocess.run(
                [sys.executable, str(repo / "scripts" / "publish_commit.py"), "search-index"],
                capture_output=True, text=True, cwd=repo)
            assert res.returncode == 0, res.stderr
            msg = _git(repo, "log", "-1", "--format=%s").strip()
            assert msg == "search-index: refresh (t_fcff6abc)", msg
            files = set(_git(repo, "show", "--name-only", "--format=", "HEAD").split())
            assert files == {"assets/search-index.js"}, files
            count_before = _git(repo, "rev-list", "--count", "HEAD")
            res = subprocess.run(
                [sys.executable, str(repo / "scripts" / "publish_commit.py"), "search-index"],
                capture_output=True, text=True, cwd=repo)
            assert res.returncode == 1 and "empty commit" in res.stderr, res.stderr + res.stdout
            assert _git(repo, "rev-list", "--count", "HEAD") == count_before
            results.append(("C6", "search-index commit scoped to assets/search-index.js; second run refuses empty"))

            # C7 content --slash-lang behaviour (Friday lane, 136f31a shape)
            slug2 = "stille-reserven-eigenkapitalaufbau-jahresende"
            for p in [f"{slug2}.html", "en/ratgeber.html", f"en/{slug2}.html",
                      "fr/ratgeber.html", f"fr/{slug2}.html",
                      "it/index.html", f"it/{slug2}.html", "it/ratgeber.html",
                      "data/audience_map.json", "sitemap.xml",
                      "scripts/_publish_20261106_stille_reserven.py"]:
                f = repo / p
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text("friday\n")
            _git(repo, "add", "-A")
            _git(repo, "commit", "-qm", "seed2 (t_99999998)")
            for p in (f"{slug2}.html", f"en/{slug2}.html", f"fr/{slug2}.html", f"it/{slug2}.html",
                      "data/audience_map.json", "sitemap.xml",
                      "scripts/_publish_20261106_stille_reserven.py"):
                (repo / p).write_text("friday2\n")
            res = subprocess.run(
                [sys.executable, str(repo / "scripts" / "publish_commit.py"),
                 "content", slug2, "--slash-lang",
                 "--files", "data/audience_map.json",
                 "--files", "scripts/_publish_20261106_stille_reserven.py"],
                capture_output=True, text=True, cwd=repo)
            assert res.returncode == 0, res.stderr
            msg = _git(repo, "log", "-1", "--format=%s").strip()
            assert msg == f"content: {slug2} (de/en/fr/it) (t_fcff6abc)", msg
            files = set(_git(repo, "show", "--name-only", "--format=", "HEAD").split())
            for must in (f"{slug2}.html", f"it/{slug2}.html", "sitemap.xml",
                         "data/audience_map.json",
                         "scripts/_publish_20261106_stille_reserven.py"):
                assert must in files, f"missing {must} in {files}"
            results.append(("C7", "content --slash-lang lands the 136f31a-shaped subject, stamped"))

            # C8 build behaviour (Friday regen, eda011c shape)
            for p in ["index.html", "en/index.html", "fr/index.html", "sitemap.xml",
                      "sitemap-de.xml", "sitemap-en.xml", "sitemap-fr.xml", "sitemap-it.xml",
                      "assets/search-index.js"]:
                (repo / p).write_text("regen\n")
            res = subprocess.run(
                [sys.executable, str(repo / "scripts" / "publish_commit.py"),
                 "build", "stille-reserven"],
                capture_output=True, text=True, cwd=repo)
            assert res.returncode == 0, res.stderr
            msg = _git(repo, "log", "-1", "--format=%s").strip()
            assert msg == "build: latest strip, sitemap, search-index for stille-reserven (t_fcff6abc)", msg
            files = set(_git(repo, "show", "--name-only", "--format=", "HEAD").split())
            assert files == {"index.html", "en/index.html", "fr/index.html",
                             "sitemap.xml", "sitemap-de.xml", "sitemap-en.xml",
                             "sitemap-fr.xml", "sitemap-it.xml",
                             "assets/search-index.js"}, files
            results.append(("C8", "build lands the eda011c-shaped subject, stamps it, stages the regen set only"))

    width = max(len(n) for n, _ in results)
    for name, desc in results:
        print(f"{name:<{width}}  PASS  {desc}")
    print(f"\npublish_commit regression suite: {len(results)} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
