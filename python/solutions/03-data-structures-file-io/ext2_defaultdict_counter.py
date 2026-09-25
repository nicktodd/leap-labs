"""Extension 2: the same grouping with collections.defaultdict and Counter."""

import csv
from collections import Counter, defaultdict
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / "shared"

with open(SHARED / "transactions.csv", newline="", encoding="utf-8") as f:
    transactions = list(csv.DictReader(f))

# Core task version: setdefault on a plain dict.
by_customer_setdefault: dict[str, list[dict]] = {}
for t in transactions:
    by_customer_setdefault.setdefault(t["customer_id"], []).append(t)

# defaultdict(list) calls list() to create the missing value on first access, so the
# loop body loses the setdefault call.
by_customer = defaultdict(list)
for t in transactions:
    by_customer[t["customer_id"]].append(t)

# Same keys, same lists in the same order.
print(f"defaultdict matches setdefault: {dict(by_customer) == by_customer_setdefault}")

# The side effect to know about: reading a missing key INSERTS it.
print(f"Keys before lookup: {len(by_customer)}")
print(f"by_customer['K999'] -> {by_customer['K999']}")
print(f"Keys after lookup:  {len(by_customer)}  (K999 is now a key with an empty list)")
del by_customer["K999"]
# Use `key in d` or d.get(key) when you only want to check.

# Counter counts hashable values; most_common(n) returns (value, count) tuples,
# sorted by count descending.
merchant_counts = Counter(t["merchant"] for t in transactions)
print("\nTop 3 merchants by transaction count:")
for merchant, count in merchant_counts.most_common(3):
    print(f"  {merchant:<14} {count:>3}")

# The hand-written equivalent from the core task, for comparison.
manual_counts: dict[str, int] = {}
for t in transactions:
    manual_counts[t["merchant"]] = manual_counts.get(t["merchant"], 0) + 1
manual_top3 = sorted(manual_counts.items(), key=lambda kv: kv[1], reverse=True)[:3]
print(f"Manual dict + sorted gives the same top 3: {manual_top3 == merchant_counts.most_common(3)}")

# A Counter returns 0 for a key it has never seen, where a plain dict raises KeyError.
declined_by_category = Counter(t["merchant_category"] for t in transactions
                               if t["status"] == "DECLINED")
print(f"\nDeclines by category: {dict(declined_by_category)}")
print(f"Declines in Dining (a key the Counter never saw): {declined_by_category['Dining']}")
