#!/usr/bin/env python3
"""Regenerate static/er-weapons-db.js from static/EldenRingWeapons.csv"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
CSV  = ROOT / "static" / "EldenRingWeapons.csv"
OUT  = ROOT / "static" / "er-weapons-db.js"

weapons = []
with open(CSV, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        weapons.append({
            "id":       int(row["id"]),
            "name":     row["name"],
            "image":    row["image"],
            "category": row["category"],
            "skill":    row["skill"],
            "passive":  row["passive effect"],
            "weight":   row["weight"],
        })

OUT.write_text(
    "// Elden Ring weapon database — auto-generated from EldenRingWeapons.csv\n"
    "// To regenerate: python3 scripts/build-weapons-db.py\n"
    f"const ER_WEAPONS = {json.dumps(weapons, indent=2)};\n",
    encoding="utf-8",
)

print(f"Written {len(weapons)} weapons → {OUT.relative_to(ROOT)}")
