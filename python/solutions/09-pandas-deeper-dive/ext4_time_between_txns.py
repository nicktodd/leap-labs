from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])

# diff() within each customer: the time since that customer's previous transaction.
# Sort first: diff works on row order, not on timestamps.
txns = txns.sort_values(["customer_id", "txn_timestamp"])
txns["gap"] = txns.groupby("customer_id")["txn_timestamp"].diff()
txns["gap_min"] = txns["gap"].dt.total_seconds() / 60

print(f"first transaction per customer has no gap: {txns['gap'].isna().sum()} NaT values")
print("\nShortest gaps between a customer's consecutive transactions:")
cols = ["customer_id", "txn_id", "txn_timestamp", "merchant", "channel", "currency", "amount",
        "status", "is_fraud", "gap_min"]
print(txns.nsmallest(6, "gap_min")[cols].to_string(index=False))

print("\nK009 on 12 Feb:")
k009 = txns[(txns["customer_id"] == "K009") & (txns["txn_timestamp"].dt.day == 12)]
print(k009[cols].to_string(index=False))
# Two of the three shortest gaps in the month belong to K009's card-testing burst on 12 Feb:
# 1.50 GBP at 01:33, 1.00 GBP 22 minutes later, then a 1,281.98 USD Apple Store attempt
# 15 minutes after that (declined). All three are Online, in the early hours. The gap alone
# does not separate fraud from normal behaviour: the other 15-minute gap (K002, P0011, an
# ASOS order at 17:39) is legitimate. A short gap combined with tiny amounts, the hour and the
# channel is what identifies card testing.
