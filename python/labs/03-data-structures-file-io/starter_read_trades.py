import csv
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"

# TODO:
# 1. Read DATA_PATH with csv.DictReader inside a `with` block, collect rows into a list.
# 2. Build a dict keyed by client_name, summing `value` (convert to float) per client.
# 3. Build a set of distinct advisor names.
# 4. Print each client's total, sorted alphabetically by client_name.
# 5. Write the same summary to client_summary.txt (same folder as this script), using `with`.
