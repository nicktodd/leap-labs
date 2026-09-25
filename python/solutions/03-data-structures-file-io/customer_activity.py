"""Per-customer card activity for February 2026, using only the standard library."""

import csv
import json
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

# --- 1. FX rates: a dict is the natural shape for "look up a rate by currency" ---
rates = {}
with open(SHARED / "fx_rates.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        rates[row["currency"]] = float(row["rate_to_gbp"])   # CSV values are always str
print(f"FX rates: {rates}")

# --- 2. Transactions: a list keeps file order; each row is a dict keyed by header ---
transactions = []
with open(SHARED / "transactions.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        # Keep full precision here and round only for output, so totals are not
        # distorted by rounding every row first.
        row["amount_gbp"] = float(row["amount"]) * rates[row["currency"]]
        transactions.append(row)
print(f"Read {len(transactions)} transactions")

# --- 3. Dict of lists: every transaction for each customer ---
txns_by_customer: dict[str, list[dict]] = {}
for txn in transactions:
    # setdefault returns the existing list, or inserts [] and returns that
    txns_by_customer.setdefault(txn["customer_id"], []).append(txn)
print(f"Customers with transactions: {len(txns_by_customer)}")

# --- 4. Dict of sets: the distinct categories each customer spends in ---
categories_by_customer: dict[str, set[str]] = {}
for txn in transactions:
    categories_by_customer.setdefault(txn["customer_id"], set()).add(txn["merchant_category"])

# --- 5. Consistency check: each merchant should belong to exactly one category ---
categories_by_merchant: dict[str, set[str]] = {}
for txn in transactions:
    categories_by_merchant.setdefault(txn["merchant"], set()).add(txn["merchant_category"])
inconsistent = {m: cats for m, cats in categories_by_merchant.items() if len(cats) != 1}
if inconsistent:
    print(f"Merchants with more than one category: {inconsistent}")
else:
    print(f"All {len(categories_by_merchant)} merchants map to exactly one category")

# --- 6. Tuples as set members: a (merchant, category) pair is a fixed, hashable value ---
merchant_category_pairs = {(t["merchant"], t["merchant_category"]) for t in transactions}
print(f"Distinct (merchant, category) pairs: {len(merchant_category_pairs)}")
# A list cannot go in a set: it is mutable, so it has no stable hash.
try:
    {["Tesco", "Groceries"]}
except TypeError as e:
    print(f"A list cannot be a set member: {e}")

# --- 7. One summary row per customer ---
summary_rows = []
for customer_id, txns in txns_by_customer.items():
    approved = [t for t in txns if t["status"] == "APPROVED"]
    largest = max(approved, key=lambda t: t["amount_gbp"])   # compare by GBP amount
    summary_rows.append({
        "customer_id": customer_id,
        "customer_name": txns[0]["customer_name"],
        "txn_count": len(txns),
        "total_gbp": round(sum(t["amount_gbp"] for t in approved), 2),
        "largest_txn_gbp": round(largest["amount_gbp"], 2),
        "distinct_categories": len(categories_by_customer[customer_id]),
    })
summary_rows = sorted(summary_rows, key=lambda r: r["total_gbp"], reverse=True)

print(f"\n{'id':<5} {'customer':<16} {'txns':>4} {'total_gbp':>10} {'largest':>9} {'cats':>4}")
for r in summary_rows:
    print(f"{r['customer_id']:<5} {r['customer_name']:<16} {r['txn_count']:>4} "
          f"{r['total_gbp']:>10,.2f} {r['largest_txn_gbp']:>9,.2f} {r['distinct_categories']:>4}")

# --- 8. CSV output: plain numbers, so the file can be read back as numbers ---
summary_path = OUT / "customer_summary.csv"
with open(summary_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
    writer.writeheader()
    writer.writerows(summary_rows)
print(f"\nWrote {len(summary_rows)} rows to {summary_path.relative_to(OUT.parent)}")

# --- 9. JSON output: the declined transactions, as a list of dicts ---
# {**t, ...} copies each dict and overrides one key, so the in-memory rows are unchanged.
declined = [{**t, "amount_gbp": round(t["amount_gbp"], 2)}
            for t in transactions if t["status"] == "DECLINED"]
declined_path = OUT / "declined.json"
with open(declined_path, "w", encoding="utf-8") as f:
    json.dump(declined, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(declined)} declined transactions to {declined_path.relative_to(OUT.parent)}")
