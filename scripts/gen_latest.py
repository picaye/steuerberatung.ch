#!/usr/bin/env python3
"""gen_latest.py — regenerate the "latest articles" strip on all four homepages.

Scans each language's article pages (root = DE, en/ fr/ it/), reads the
JSON-LD `headline`, `description` and `datePublished` (fallback dateModified)
from every Article node, sorts by date, takes the top N (default 5) and
rewrites the marked block inside each index.html.

Zero manual maintenance: the article's own metadata is the single source of
truth. Run after publishing a new article (the publish cron does this):

    python3 scripts/gen_latest.py            # rewrite all 4 homepages
    python3 scripts/gen_latest.py --dry-run  # print what would change

The block lives between the markers:
    <!-- LATEST:START --> ... <!-- LATEST:END -->
which gen_latest.py creates automatically in an index.html if missing (the
section heading is localised and also managed by this script).
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK_START = "<!-- LATEST:START -->"
MARK_END = "<!-- LATEST:END -->"

# Localised strings for the generated block (site voice: Sie/vouvoiement/Lei/EN).
L10N = {
    "de": {
        "heading": "Aktuelle Artikel",
        "sub": "Frisch veröffentlicht – das Neueste aus dem Ratgeber.",
        "new": "Neu",
        "cta": "Zum Artikel →",
        "aria": "Aktuelle Artikel",
    },
    "en": {
        "heading": "Latest articles",
        "sub": "Freshly published – the newest from our guides.",
        "new": "New",
        "cta": "Read the article →",
        "aria": "Latest articles",
    },
    "fr": {
        "heading": "Articles récents",
        "sub": "Publiés récemment – les nouveautés de nos guides.",
        "new": "Nouveau",
        "cta": "Lire l’article →",
        "aria": "Articles récents",
    },
    "it": {
        "heading": "Articoli recenti",
        "sub": "Di recente pubblicazione – le novità dalle nostre guide.",
        "new": "Nuovo",
        "cta": "Leggi l’articolo →",
        "aria": "Articoli recenti",
    },
}

ARTICLE_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
DATE_RE = re.compile(r'"date(?:Published|Modified)":\s*"(\d{4}-\d{2}-\d{2})"')


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def article_meta(path: Path) -> dict | None:
    """Return {slug, headline, desc, date} for an Article page, else None."""
    html = path.read_text(encoding="utf-8")
    best: dict | None = None
    for blob in ARTICLE_RE.findall(html):
        try:
            nodes = json.loads(blob)
        except json.JSONDecodeError:
            continue
        if isinstance(nodes, dict):
            nodes = [nodes]
        for node in nodes:
            if not isinstance(node, dict) or node.get("@type") not in (
                "Article",
                "NewsArticle",
                "BlogPosting",
            ):
                continue
            date = node.get("datePublished") or node.get("dateModified") or ""
            m = re.match(r"(\d{4}-\d{2}-\d{2})", str(date))
            if not m:
                continue
            headline = node.get("headline") or ""
            if not headline:
                continue
            desc = node.get("description") or ""
            cand = {
                "slug": path.name,
                "headline": headline,
                "desc": desc,
                "date": m.group(1),
            }
            if best is None or cand["date"] > best["date"]:
                best = cand
    if best is None:  # fallback: raw regex anywhere in the head (JSON-LD quirk)
        m = DATE_RE.search(html[:6000])
        t = re.search(r"<title>(.*?)</title>", html)
        if m and t:
            best = {
                "slug": path.name,
                "headline": t.group(1).split(" | ")[0],
                "desc": "",
                "date": m.group(1),
            }
    return best


def collect(lang: str) -> list[dict]:
    base = ROOT if lang == "de" else ROOT / lang
    out = []
    for p in sorted(base.glob("*.html")):
        meta = article_meta(p)
        if meta:
            out.append(meta)
    # newest first; stable tiebreak by slug
    out.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    return out


def render(lang: str, articles: list[dict], today: datetime.date) -> str:
    t = L10N[lang]
    lines = [MARK_START]
    lines.append('<section class="section latest-section" aria-label="%s">' % t["aria"])
    lines.append("<div class=\"container\">")
    lines.append("<h2>%s</h2>" % esc(t["heading"]))
    lines.append('<p class="muted">%s</p>' % esc(t["sub"]))
    lines.append('<ol class="latest-list">')
    for i, a in enumerate(articles):
        try:
            d = datetime.date.fromisoformat(a["date"])
        except ValueError:  # defensive: never ship a raw/garbage date
            d = today
        date_lbl = d.strftime("%d.%m.%Y" if lang == "de" else "%d %b %Y")
        is_new = (today - d).days <= 14
        item_cls = ' class="featured"' if i == 0 else ""
        lines.append("<li%s>" % item_cls)
        lines.append("<article>")
        lines.append('<div class="latest-meta"><time datetime="%s">%s</time>%s</div>' % (
            a["date"],
            esc(date_lbl),
            ('<span class="latest-new">%s</span>' % esc(t["new"])) if is_new else "",
        ))
        lines.append("<h3><a href=\"%s\">%s</a></h3>" % (a["slug"], esc(a["headline"])))
        if a["desc"]:
            lines.append("<p>%s</p>" % esc(a["desc"]))
        lines.append('<a class="latest-cta" href="%s">%s</a>' % (a["slug"], esc(t["cta"])))
        lines.append("</article>")
        lines.append("</li>")
    lines.append("</ol>")
    lines.append("</div>")
    lines.append("</section>")
    lines.append(MARK_END)
    return "\n".join(lines)


def inject(index: Path, block: str) -> bool:
    html = index.read_text(encoding="utf-8")
    if MARK_START in html and MARK_END in html:
        new = re.sub(
            re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
            lambda _: block,
            html,
            count=1,
            flags=re.S,
        )
    else:
        # insert the block right before the closing </main>
        if "</main>" not in html:
            print(f"ERROR: {index} has no markers and no </main> — skipping", file=sys.stderr)
            return False
        new = html.replace("</main>", block + "\n</main>", 1)
    if new == html:
        return False
    index.write_text(new, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--today", default=None, help="ISO date override for the 'New' badge")
    args = ap.parse_args()
    today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()

    changed = 0
    for lang in ("de", "en", "fr", "it"):
        arts = collect(lang)[: args.count]
        if not arts:
            print(f"WARN: {lang}: no dated articles found", file=sys.stderr)
            continue
        block = render(lang, arts, today)
        index = ROOT / "index.html" if lang == "de" else ROOT / lang / "index.html"
        if args.dry_run:
            print(f"--- {lang} ({len(arts)} articles): " + ", ".join(a["slug"] for a in arts))
            continue
        if inject(index, block):
            print(f"{lang}: rewrote latest block ({len(arts)} articles)")
            changed += 1
        else:
            print(f"{lang}: no change")
    return 0


if __name__ == "__main__":
    sys.exit(main())
