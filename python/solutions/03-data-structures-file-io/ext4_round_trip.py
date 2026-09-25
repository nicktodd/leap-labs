"""Extension 4: read output/customer_summary.csv back and check it against memory."""

import csv
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"

# Run the core script and keep its variables. This writes output/customer_summary.csv
# and gives us summary_rows, the in-memory values the file was written from.
print("Running customer_activity.py ...")
core = runpy.run_path(str(HERE / "customer_activity.py"))
in_memory = {r["customer_id"]: r for r in core["summary_rows"]}
print("... done\n")

# Read the file back. Every value comes back as a str, so convert before comparing.
with open(OUT / "customer_summary.csv", newline="", encoding="utf-8") as f:
    from_file = {row["customer_id"]: row for row in csv.DictReader(f)}

mismatches = []
for customer_id, row in from_file.items():
    expected = in_memory[customer_id]
    if (float(row["total_gbp"]) != expected["total_gbp"]
            or int(row["txn_count"]) != expected["txn_count"]):
        mismatches.append(customer_id)

file_total = sum(float(row["total_gbp"]) for row in from_file.values())
memory_total = sum(r["total_gbp"] for r in in_memory.values())
print(f"Rows in file: {len(from_file)}, rows in memory: {len(in_memory)}")
print(f"Grand total from file:   {file_total:,.2f}")
print(f"Grand total from memory: {memory_total:,.2f}")
print(f"Per-customer mismatches: {mismatches or 'none'}")

# Why the core script writes plain numbers: write the same rows with display formatting
# and try to read them back.
formatted_path = OUT / "customer_summary_formatted.csv"
with open(formatted_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["customer_id", "total_gbp"])
    for r in core["summary_rows"]:
        writer.writerow([r["customer_id"], f"{r['total_gbp']:,.2f}"])

with open(formatted_path, newline="", encoding="utf-8") as f:
    first = next(csv.DictReader(f))
print(f"\nFormatted file, first row: {first}")
try:
    float(first["total_gbp"])
except ValueError as e:
    # The thousands separator makes the text unreadable as a number. The csv module
    # quotes the field, so the file is still valid CSV, but every consumer now has to
    # strip commas (and must know which locale's separators were used).
    print(f"float() on the formatted value fails: {e}")
