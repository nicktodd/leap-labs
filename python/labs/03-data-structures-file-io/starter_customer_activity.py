"""Per-customer card activity for February 2026, using only the standard library.

Standard library only: no pandas in this lab.
"""

import csv
import json
from pathlib import Path

# Paths are built from this file's location, so the script works from any folder.
SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

# TODO 1: read SHARED / "fx_rates.csv" with csv.DictReader inside a `with` block and build
#         `rates`, a dict of currency -> float. Print it.
rates: dict[str, float] = {}

# TODO 2: read SHARED / "transactions.csv" with csv.DictReader inside a `with` block into a
#         list of dicts. Add an "amount_gbp" float to each row (amount * rate). Every value
#         from DictReader is a str. Print how many rows you read.
transactions: list[dict] = []

# TODO 3: build txns_by_customer: customer_id -> list of that customer's transaction dicts.
#         Use dict.setdefault(key, []).append(...).
txns_by_customer: dict[str, list[dict]] = {}

# TODO 4: build categories_by_customer: customer_id -> set of merchant_category values.
categories_by_customer: dict[str, set[str]] = {}

# TODO 5: build categories_by_merchant: merchant -> set of merchant_category values, and
#         check that every merchant maps to exactly one category. Print the result.

# TODO 6: build a set of (merchant, merchant_category) tuples and print how many distinct
#         pairs there are. Then show, inside try/except, that a list cannot be a set member.

# TODO 7: build one summary dict per customer with the keys customer_id, customer_name,
#         txn_count, total_gbp (APPROVED only), largest_txn_gbp (largest APPROVED
#         transaction, using max() with key=lambda) and distinct_categories.
#         Sort the list by total_gbp, largest first, with sorted(..., key=...) and print it
#         as an aligned table.
summary_rows: list[dict] = []

# TODO 8: write summary_rows to OUT / "customer_summary.csv" with csv.DictWriter.
#         Open the file with newline="" and write plain numbers (no thousands separators).

# TODO 9: write the DECLINED transactions to OUT / "declined.json" with json.dump(indent=2).
