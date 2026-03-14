#!/usr/bin/env python3
"""
Generate static/er-aow-db.js from:
  - https://eldenring.fanapis.com/api/ashes?limit=100
  - static/Elden Ring Compatible Ash of War Sheet - Weapons.csv

Run: python3 scripts/build-aow-db.py
"""

import csv
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
WEAPONS_CSV = ROOT / "static" / "Elden Ring Compatible Ash of War Sheet - Weapons.csv"
OUT = ROOT / "static" / "er-aow-db.js"

# ── 1. Fetch all ashes from the API ──────────────────────────────────────────
print("Fetching ashes from API...")
with urllib.request.urlopen("https://eldenring.fanapis.com/api/ashes?limit=100") as r:
    data = json.loads(r.read())

AOW_PREFIXES = ["Ash Of War: ", "Ashes Of War: ", "Ash of War: "]

def strip_prefix(raw):
    for p in AOW_PREFIXES:
        if raw.lower().startswith(p.lower()):
            return raw[len(p):]
    return raw  # e.g. "Through And Through", "Lost Ashes Of War"

ashes = []
for a in data["data"]:
    raw_name = a["name"]
    name = strip_prefix(raw_name)
    ashes.append({
        "id":          a["id"],
        "name":        name,
        "image":       a.get("image") or "",
        "description": (a.get("description") or "").replace("\n", " ").strip(),
        "affinity":    a.get("affinity") or "",
        "skill":       a.get("skill") or name,
    })

ashes.sort(key=lambda a: a["name"])
print(f"  Got {len(ashes)} ashes")

# ── 2. Build weapon→aow map from Weapons.csv (one entry per weapon name) ─────
print("Building weapon→AoW compatibility map...")
weapon_aow = {}   # weapon name (str) → [ash names...]
can_apply   = set()  # weapon names that CAN apply AoW
cannot_apply = set() # weapon names that CANNOT

with open(WEAPONS_CSV, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        wname = row["Weapon Name"].strip()
        if wname in weapon_aow:
            continue  # deduplicate — same aow list for all affinities

        if row["Can Apply Ash of War"].strip().lower() == "yes":
            can_apply.add(wname)
            aow_list = []
            for i in range(1, 57):
                v = (row.get(f"Ash of War {i}") or "").strip()
                if v and v not in aow_list:
                    aow_list.append(v)
            weapon_aow[wname] = aow_list
        else:
            cannot_apply.add(wname)
            weapon_aow[wname] = []

print(f"  Weapons with AoW: {len(can_apply)}, without: {len(cannot_apply)}")

# ── 3. Write JS ───────────────────────────────────────────────────────────────
js = (
    "// Elden Ring Ashes of War database — auto-generated\n"
    "// To regenerate: python3 scripts/build-aow-db.py\n\n"
    f"const ER_ASHES = {json.dumps(ashes, indent=2)};\n\n"
    "// weapon name → array of compatible ash names (empty = cannot apply AoW)\n"
    f"const ER_WEAPON_AOW = {json.dumps(weapon_aow, indent=2)};\n"
)

OUT.write_text(js, encoding="utf-8")
print(f"Written → {OUT.relative_to(ROOT)}  ({OUT.stat().st_size // 1024} KB)")
