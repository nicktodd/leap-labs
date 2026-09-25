"""Extension 1: answer three questions with set operations instead of nested loops."""

import csv
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / "shared"

with open(SHARED / "transactions.csv", newline="", encoding="utf-8") as f:
    transactions = list(csv.DictReader(f))

all_customers = {t["customer_id"] for t in transactions}

# One set per channel. Each set answers "who has ever used this channel?"
online = {t["customer_id"] for t in transactions if t["channel"] == "Online"}
in_store = {t["customer_id"] for t in transactions if t["channel"] == "In-store"}

# 1. Intersection (&): customers in BOTH sets.
both = online & in_store
print(f"Used both Online and In-store ({len(both)}): {sorted(both)}")
# The customers that are NOT in the intersection are worth a look too.
print(f"  ...and not both ({len(all_customers - both)}): {sorted(all_customers - both)}")

# 2. Difference (-): every customer, minus those with at least one decline.
declined = {t["customer_id"] for t in transactions if t["status"] == "DECLINED"}
never_declined = all_customers - declined
print(f"Customers with a decline ({len(declined)}): {sorted(declined)}")
print(f"Customers with no declined transactions ({len(never_declined)}): {sorted(never_declined)}")

# 3. Merchants used by exactly one customer: a dict of sets, then filter on the set size.
customers_by_merchant: dict[str, set[str]] = {}
for t in transactions:
    customers_by_merchant.setdefault(t["merchant"], set()).add(t["customer_id"])
single_customer = {m: c for m, c in customers_by_merchant.items() if len(c) == 1}
print(f"Merchants used by exactly one customer: {single_customer}")

# Sets have no order, so every print above goes through sorted() to make the output
# repeatable from one run to the next.
