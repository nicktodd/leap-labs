"""Read trades.csv with csv.DictReader and produce a per-client value summary."""

import csv
from pathlib import Path

DATA_PATH = Path(r"C:\Users\zackt\Documents\fidelity-leap-sprint4\shared\trades.csv")
OUTPUT_PATH = Path(__file__).parent / "client_summary.txt"

# 1. Read all rows into a list of dicts using csv.DictReader
with open(DATA_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# 2. Build per-client total value dict (values from DictReader are strings — convert to float)
client_totals: dict[str, float] = {}
for row in rows:
    name = row["client_name"]
    client_totals[name] = client_totals.get(name, 0.0) + float(row["value"])

# 3. Build a set of distinct advisor names
advisors: set[str] = {row["advisor"] for row in rows}

# 4. Print per-client summary (sorted alphabetically by client_name)
print("Per-client total trade value:")
for client in sorted(client_totals):
    print(f"  {client}: {client_totals[client]:,.2f}")

print(f"\nDistinct advisors ({len(advisors)}): {sorted(advisors)}")

# 5. Write the same summary to client_summary.txt using a with block
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write("Per-client total trade value:\n")
    for client in sorted(client_totals):
        f.write(f"  {client}: {client_totals[client]:,.2f}\n")
    f.write(f"\nDistinct advisors ({len(advisors)}): {sorted(advisors)}\n")

print(f"\nSummary written to {OUTPUT_PATH}")
