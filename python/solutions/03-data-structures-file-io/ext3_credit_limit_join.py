"""Extension 3: join transactions to customers.csv with a dict lookup."""

import csv
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / "shared"

with open(SHARED / "fx_rates.csv", newline="", encoding="utf-8") as f:
    rates = {row["currency"]: float(row["rate_to_gbp"]) for row in csv.DictReader(f)}

# The lookup table: customer_id -> the whole customer row. Building it once makes each
# lookup a single dict access instead of a scan of the customer list.
with open(SHARED / "customers.csv", newline="", encoding="utf-8") as f:
    customers = {row["customer_id"]: row for row in csv.DictReader(f)}
print(f"Customers in reference data: {len(customers)}")

approved_gbp: dict[str, float] = {}
with open(SHARED / "transactions.csv", newline="", encoding="utf-8") as f:
    for t in csv.DictReader(f):
        if t["status"] != "APPROVED":
            continue
        amount_gbp = float(t["amount"]) * rates[t["currency"]]
        approved_gbp[t["customer_id"]] = approved_gbp.get(t["customer_id"], 0.0) + amount_gbp

rows = []
missing = []
for customer_id, spend in approved_gbp.items():
    # customers[customer_id] would raise KeyError for K012. .get() returns None instead,
    # so the missing customer is reported rather than stopping the script.
    customer = customers.get(customer_id)
    if customer is None:
        missing.append(customer_id)
        continue
    limit = float(customer["credit_limit_gbp"])
    rows.append((customer_id, customer["customer_name"], spend, limit, spend / limit * 100))

rows.sort(key=lambda r: r[4], reverse=True)
print(f"\n{'id':<5} {'customer':<16} {'spend_gbp':>10} {'limit_gbp':>10} {'used':>6}")
for customer_id, name, spend, limit, pct in rows:
    print(f"{customer_id:<5} {name:<16} {spend:>10,.2f} {limit:>10,.0f} {pct:>5.1f}%")

for customer_id in missing:
    print(f"\nWARNING: {customer_id} has approved spend of GBP {approved_gbp[customer_id]:,.2f} "
          f"but no row in customers.csv; credit limit unknown")
