#!/usr/bin/env python3
"""Generate assets/locations.js from the official ESTV location dataset.

Source: scripts/fixtures/estv_raw_factors_2026.json (fetched by
fetch_estv_fixtures.py from the ESTV API). Re-run each January after
refreshing the fixtures. The browser calculator uses this list for
municipality autocomplete; the proxy /api/tax/locations is the online
fallback for names not in the static list.
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "scripts", "fixtures", "estv_raw_factors_2026.json")
OUT = os.path.join(BASE, "assets", "locations.js")

data = json.load(open(SRC))["response"]
out, seen = [], set()
for x in data:
    loc = x["Location"]
    ident = loc["TaxLocationID"]
    if ident in seen:
        continue
    seen.add(ident)
    out.append({"id": ident, "city": loc["City"],
                "zip": loc.get("ZipCode", ""), "canton": loc["Canton"]})
out.sort(key=lambda e: (e["canton"], e["zip"] or "9999", e["city"]))

header = ("// Generated from the official ESTV location dataset (2026) by "
          "scripts/gen_locations.py - do not edit by hand.\n")
with open(OUT, "w") as f:
    f.write(header)
    f.write("window.TAX_LOCATIONS = ")
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";\n")
print(f"wrote {len(out)} locations to {OUT} ({os.path.getsize(OUT)} bytes)")
