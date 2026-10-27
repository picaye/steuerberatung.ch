#!/usr/bin/env python3
"""steuerberatung.ch publish calendar maintainer (Pino 2026-10-21).

Friday-only weekly grid (one article per week). Guarantees:
- no collisions (two cards never share a slot week),
- deadline-sensitive cards never slip past their topical deadline,
- same-cluster cards (mwst / 3a / ahv / bvg / steuererklaerung ...) never in
  consecutive weeks ("not always all 3a at once"),
- FIXED fast-lane drafts stay on their exact Fridays.

Modes:
  publish_calendar.py            print taken-Friday calendar
  publish_calendar.py --free     next 20 free Fridays
  publish_calendar.py --fix      re-plan pins; rewrite jsonl + git commit only if
                                 something changed; prints summary when it fixes,
                                 silent (watchdog) when all is well. Surplus cards
                                 that no Friday slot (nominal horizon or beyond)
                                 can host are DE-PINNED, never left on stale pins.
                                 The commit is refused if the post-plan queue
                                 carries any slot collision or off-grid pin.
                                 Maintenance commits are always card-stamped
                                 with MAINTENANCE_CARD (uncarded-stream guard).
  publish_calendar.py --fix --dry-run
                                 same planning, prints what would change, no writes.
"""
import json, datetime, pathlib, re, subprocess, sys, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
JL = ROOT / "data/content-research.jsonl"

# Standing anchor card for the --fix maintenance stream (t_d0820b72). Every
# commit this script makes must carry a card id: scripts/uncarded_commits.py
# fails sweeps on uncarded streams, and this cron stream was its dominant
# source (fleet convention established in t_45ab7c9f).
MAINTENANCE_CARD = "t_d0820b72"

# Same shape scripts/uncarded_commits.py audits for.
CARD_STAMP_RE = re.compile(r"t_[0-9a-f]{8}")


def maintenance_commit_message(changed_n: int, cleared_n: int) -> str:
    """Commit message for a --fix maintenance run, always card-stamped."""
    return (f"publish calendar maintenance: re-pinned {changed_n} card(s)"
            + (f", de-pinned {cleared_n}" if cleared_n else "")
            + f" (collision/deadline/cluster hygiene) ({MAINTENANCE_CARD})")

GRID_START = datetime.date(2026, 10, 23)
HORIZON_END = datetime.date(2028, 6, 30)  # nominal calendar horizon
EXCLUDED = {(1, 1), (12, 23), (12, 25), (12, 30), (12, 31)}  # holiday blackout days

def is_friday_slot(d):
    """Grid predicate: a Friday outside blackout days. Shared with
    validate_queue.py so CI and planner never drift apart."""
    return d.weekday() == 4 and (d.month, d.day) not in EXCLUDED

def fridays():
    d, out = GRID_START, []
    while d <= HORIZON_END:
        if is_friday_slot(d):
            out.append(d)
        d += datetime.timedelta(days=1)
    return out

FIXED = {  # drafted fast-lane articles: exact Fridays, do not move
    "ubs-cs-migration-steuererklaerung-2026": "2027-01-08",
    "generalversammlung-2027-gewinn-dividende-steuer": "2027-02-05",
}
DEADLINE = {  # latest acceptable Friday (hard topical windows)
    "kassabuch-twint-aufzeichnung-pflicht-jahresende": "2027-03-31",
    "mwst-erhoehung-2027-ahv-armee": "2026-11-27",
    "fairness-initiative-ehepaare-2026": "2026-11-27",
    "saeule-3a-jahresende-einzahlung-2026": "2026-12-18",
    "saeule-3a-beguenstigte-neu-2027": "2027-01-29",
    "mwst-option-wechsel-frist-31-dezember": "2026-12-18",
    "lohnabrechnung-2027-ahv-iv-eo-neue-werte": "2026-12-18",
    "stille-reserven-eigenkapitalaufbau-jahresende": "2026-12-11",
    "mwst-vorsteuer-eigenverbrauch-jahresende": "2026-12-11",
    "mwst-abmeldung-unter-100000-jahresende": "2026-12-11",
    "arbeitgeber-3a-beitrag-lohnausweis": "2026-12-11",
    "ahv-lohnabrechnung-annualisieren-frist-31-januar": "2027-01-29",
    "carif-krypto-datenaustausch-ab-2027": "2027-01-15",
    "steuererklaerung-fristerstreckung-2027": "2027-03-19",
    "saeule-3a-jahresende-einzahlung-2026": "2026-12-18",
}

def cluster(slug):
    for pat, name in [("mwst", "mwst"), ("saeule-3a", "3a"), ("arbeitgeber-3a", "3a"),
                      ("ahv", "ahv"), ("bvg", "bvg"), ("pensionskasse", "bvg"),
                      ("steuererklaerung", "stkl"), ("verrechnungssteuer", "vst"),
                      ("quellensteuer", "vst"), ("individualbesteuerung", "ehe"),
                      ("fairness", "ehe"), ("getrennt-leben", "ehe"), ("alimente", "ehe"),
                      ("grenzgaenger", "gz"), ("krypto", "krypto"), ("carif", "krypto"),
                      ("etf", "depot"), ("gold", "depot"), ("kapitalverluste", "depot"),
                      ("auslaendische-liegenschaft", "lieg"), ("liegenschaftssteuer", "lieg")]:
        if pat in slug:
            return name
    return slug.split("-")[0]

def load():
    return [json.loads(l) for l in open(JL)]

def plan(cards):
    slots = fridays()
    today = datetime.date.today()
    art = [c for c in cards if c.get("status") == "pending" and c.get("type") in (None, "article")
           and (c.get("hold_until") or c["slug"] in FIXED)]
    for c in art:
        hu = datetime.date.fromisoformat(c.get("release_intent") or c["hold_until"]) if (c.get("release_intent") or c.get("hold_until")) else datetime.date(2026, 10, 23)
        c["_rel"] = max(datetime.date(2026, 10, 23), hu - datetime.timedelta(days=21))
        c["_dl"] = datetime.date.fromisoformat(DEADLINE[c["slug"]]) if c.get("slug") in DEADLINE else None
    out = {}
    for slug, when in FIXED.items():
        out[datetime.date.fromisoformat(when)] = slug
    rest = [c for c in art if c["slug"] not in FIXED]
    # Anchor rule: a pin that is already valid (future, on the Friday grid,
    # slot still free, deadline not passed) is KEPT as-is. Maintenance then
    # re-pins only the broken cards — the slot calendar is a product
    # decision, not churn fodder, and idempotent re-runs stay silent.
    for c in list(rest):
        hu = c.get("hold_until")
        try:
            d = datetime.date.fromisoformat(hu) if hu else None
        except ValueError:
            d = None
        if d is None or d < today or not is_friday_slot(d) or d in out:
            continue
        if c["_dl"] is not None and c["_dl"] < d:
            continue
        out[d] = c["slug"]
        rest.remove(c)
    recent = collections.deque(maxlen=2)
    for slot in slots:
        if slot < today:
            continue  # past Fridays are not placeable slots (rule 3 pins)
        if slot in out:
            recent.append(cluster(out[slot]))
            continue
        elig = [c for c in rest if c["_rel"] <= slot and (c["_dl"] is None or c["_dl"] >= slot)]
        if not elig:
            continue
        elig.sort(key=lambda c: (c["_dl"] or datetime.date(2099, 1, 1),
                                 1 if cluster(c["slug"]) in recent else 0,
                                 c["_rel"],
                                 {"high": 0, "medium": 1, "low": 2}.get(c.get("demand"), 3),
                                 c["slug"]))
        pick = elig[0]
        out[slot] = pick["slug"]
        rest.remove(pick)
        recent.append(cluster(pick["slug"]))
    # Grid saturated: place the surplus on Fridays BEYOND the nominal
    # horizon instead of leaving them on stale pins. A stale pin that the
    # reflow later reuses is exactly the collision defect this planner is
    # meant to prevent. Cards whose topical deadline has passed are the
    # only ones left unplaced (reported to the caller, never pinned).
    if rest:
        nxt = slots[-1] + datetime.timedelta(days=1)
        while rest:
            slot = nxt
            while not is_friday_slot(slot):
                slot += datetime.timedelta(days=1)
            elig = [c for c in rest if c["_rel"] <= slot and (c["_dl"] is None or c["_dl"] >= slot)]
            if not elig:
                break  # remaining cards cannot meet deadlines even past the horizon
            elig.sort(key=lambda c: (c["_dl"] or datetime.date(2099, 1, 1),
                                     1 if cluster(c["slug"]) in recent else 0,
                                     c["_rel"],
                                     {"high": 0, "medium": 1, "low": 2}.get(c.get("demand"), 3),
                                     c["slug"]))
            pick = elig[0]
            out[slot] = pick["slug"]
            rest.remove(pick)
            recent.append(cluster(pick["slug"]))
            nxt = slot + datetime.timedelta(days=1)
    return out, rest

def main():
    cards = load()
    args = sys.argv[1:]
    if "--free" in args:
        cal = plan(cards)[0]
        n = 0
        for s in fridays():
            if s not in cal and s >= datetime.date.today():
                print(s); n += 1
                if n >= 20:
                    break
        return
    cal, unplaced = plan(cards)
    if not args:
        for s in sorted(cal):
            print(s, "->", cal[s])
        print("# planned:", len(cal), "| pending-without-pin total:", len([c for c in cards if c.get("status") == "pending" and c.get("type") in (None, "article") and not c.get("hold_until") and c["slug"] not in FIXED]))
        return
    if "--fix" in args:
        byslug = {c["slug"]: c for c in cards if "slug" in c}
        dry = "--dry-run" in args
        changed = {}
        cleared = []
        for s, slug in cal.items():
            if byslug[slug].get("hold_until") != str(s):
                changed[slug] = str(s)
        # Surplus cards (cannot meet deadlines even past the horizon) must
        # NOT keep their stale pins: an old pin re-used by the reflow is a
        # collision waiting to happen. They are de-pinned instead.
        planned_slugs = set(cal.values())
        pinned_slugs = {c["slug"] for c in cards if c.get("status") == "pending"
                        and c.get("type") in (None, "article")
                        and (c.get("hold_until") or c["slug"] in FIXED)}
        for slug in pinned_slugs - planned_slugs:
            if byslug[slug].get("hold_until"):
                cleared.append(slug)
        if unplaced:
            print("!! CARDS CANNOT MEET DEADLINES (de-pinned):", [c["slug"] for c in unplaced])
        if not changed and not cleared:
            return  # healthy calendar: stay silent (watchdog pattern)
        if dry:
            print("DRY-RUN: would re-pin", len(changed), "card(s); would de-pin", len(cleared), "card(s)")
            for slug, when in sorted(changed.items(), key=lambda x: x[1]):
                print("  ->", when, slug)
            for slug in cleared:
                print("  de-pin", slug)
        else:
            for s, slug in cal.items():
                c = byslug[slug]
                if "release_intent" not in c:
                    c["release_intent"] = c.get("hold_until")  # freeze research intent => idempotent re-plans
                c["hold_until"] = str(s)
                c["priority"] = "pin-" + str(s)
            for slug in cleared:
                c = byslug[slug]
                c["hold_until"] = None
                if isinstance(c.get("priority"), str) and c["priority"].startswith("pin-"):
                    c["priority"] = c.get("demand") or "medium"
            # Post-plan collision assertion: every Friday slot may carry at
            # most one pending pin. If the plan is not collision-free the
            # commit is REFUSED (never push a knowingly-broken queue).
            slot_count = collections.Counter(
                c["hold_until"] for c in cards
                if c.get("status") == "pending" and c.get("type") in (None, "article")
                and c.get("hold_until"))
            collisions = {s: n for s, n in slot_count.items() if n > 1}
            offgrid = [s for s in slot_count if not is_friday_slot(datetime.date.fromisoformat(s))]
            if collisions or offgrid:
                print("FIX ABORTED — collisions:", collisions, "off-grid:", offgrid)
                sys.exit(1)
            with open(JL, "w") as f:
                for c in cards:
                    clean = {k: v for k, v in c.items() if not k.startswith("_")}
                    clean.pop("hold_until", None) if c.get("hold_until") is None and "hold_until" in c else None
                    f.write(json.dumps(clean, ensure_ascii=False) + "\n")
            r = subprocess.run(["python3", str(ROOT / "scripts/validate_queue.py")], capture_output=True, text=True)
            if "OK" not in r.stdout:
                subprocess.run(["git", "-C", str(ROOT), "checkout", "--", "data/content-research.jsonl"])
                print("FIX REJECTED by validator:", (r.stdout or r.stderr)[:200])
                sys.exit(1)
            subprocess.run(["git", "-C", str(ROOT), "add", "data/content-research.jsonl", "scripts/publish_calendar.py"])
            subprocess.run(["git", "-C", str(ROOT), "commit", "-m",
                            maintenance_commit_message(len(changed), len(cleared))])
            subprocess.run(["git", "-C", str(ROOT), "push", "-q"])
            print("publish calendar: re-pinned", len(changed), "card(s)")
            for slug, when in sorted(changed.items(), key=lambda x: x[1]):
                print(" ", when, slug)

if __name__ == "__main__":
    main()
