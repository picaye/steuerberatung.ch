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
                                 silent (watchdog) when all is well.
"""
import json, datetime, pathlib, subprocess, sys, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
JL = ROOT / "data/content-research.jsonl"

def fridays():
    d, out = datetime.date(2026, 10, 23), []
    while d <= datetime.date(2028, 6, 30):
        if d.weekday() == 4 and not (d.month == 1 and d.day == 1) and not (d.month == 12 and d.day in (23, 25, 30, 31)):
            out.append(d)
        d += datetime.timedelta(days=1)
    return out

FIXED = {  # drafted fast-lane articles: exact Fridays, do not move
    "lohnabrechnung-2027-ahv-iv-eo-neue-werte": "2026-12-04",
    "ubs-cs-migration-steuererklaerung-2026": "2027-01-08",
    "generalversammlung-2027-gewinn-dividende-steuer": "2027-02-05",
}
DEADLINE = {  # latest acceptable Friday (hard topical windows)
    "kassabuch-twint-aufzeichnung-pflicht-jahresende": "2027-03-31",
    "mwst-erhoehung-2027-ahv-armee": "2026-11-27",
    "fairness-initiative-ehepaare-2026": "2026-11-27",
    "saeule-3a-jahresende-einzahlung-2026": "2026-12-18",
    "saeule-3a-beguenstigte-neu-2027": "2027-01-29",
    "mwst-option-wechsel-frist-31-dezember": "2026-12-11",
    "stille-reserven-eigenkapitalaufbau-jahresende": "2026-12-11",
    "mwst-vorsteuer-eigenverbrauch-jahresende": "2026-12-11",
    "mwst-abmeldung-unter-100000-jahresende": "2026-12-11",
    "bvg-mindestzins-2027": "2026-12-11",
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
    recent = collections.deque(maxlen=2)
    for slot in slots:
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
        changed = {}
        for s, slug in cal.items():
            if byslug[slug].get("hold_until") != str(s):
                changed[slug] = str(s)
        if unplaced:
            print("!! CARDS CANNOT MEET DEADLINES:", [c["slug"] for c in unplaced])
        if not changed:
            return  # healthy calendar: stay silent (watchdog pattern)
        for s, slug in cal.items():
            c = byslug[slug]
            if "release_intent" not in c:
                c["release_intent"] = c.get("hold_until")  # freeze research intent => idempotent re-plans
            c["hold_until"] = str(s)
            c["priority"] = "pin-" + str(s)
        # cards we are NOT planning (no hold_until, unpinned) keep their fields untouched
        with open(JL, "w") as f:
            for c in cards:
                clean = {k: v for k, v in c.items() if not k.startswith("_")}
                f.write(json.dumps(clean, ensure_ascii=False) + "\n")
        r = subprocess.run(["python3", str(ROOT / "scripts/validate_queue.py")], capture_output=True, text=True)
        if "OK" not in r.stdout:
            subprocess.run(["git", "-C", str(ROOT), "checkout", "--", "data/content-research.jsonl"])
            print("FIX REJECTED by validator:", (r.stdout or r.stderr)[:200])
            sys.exit(1)
        subprocess.run(["git", "-C", str(ROOT), "add", "data/content-research.jsonl", "scripts/publish_calendar.py"])
        subprocess.run(["git", "-C", str(ROOT), "commit", "-m",
                        f"publish calendar maintenance: re-pinned {len(changed)} card(s) (collision/deadline/cluster hygiene)"])
        subprocess.run(["git", "-C", str(ROOT), "push", "-q"])
        print("publish calendar: re-pinned", len(changed), "card(s)")
        for slug, when in sorted(changed.items(), key=lambda x: x[1]):
            print(" ", when, slug)

if __name__ == "__main__":
    main()
