from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv")
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)

# transform("median") returns one value per ROW (the median of that row's customer), aligned
# to the original index, so it can be compared directly with amount_gbp. agg("median") would
# return one value per customer, which needs a merge before it can be compared.
txns["customer_median_gbp"] = txns.groupby("customer_id")["amount_gbp"].transform("median")
txns["ratio_to_median"] = (txns["amount_gbp"] / txns["customer_median_gbp"]).round(1)
flagged = txns[txns["amount_gbp"] > 5 * txns["customer_median_gbp"]]

cols = ["txn_id", "customer_id", "merchant", "channel", "country", "amount_gbp",
        "customer_median_gbp", "ratio_to_median", "status", "is_fraud"]
print(f"Transactions above 5x the customer's median amount_gbp: {len(flagged)}")
print(flagged[cols].to_string(index=False))

caught = flagged["is_fraud"].sum()
total_fraud = txns["is_fraud"].sum()
print(f"\nflagged rows that are fraud: {caught} of {len(flagged)}")
print(f"fraud rows caught:           {caught} of {total_fraud}")
missed = txns[(txns["is_fraud"] == 1) & ~txns.index.isin(flagged.index)]
print("fraud rows not flagged:")
print(missed[cols].to_string(index=False))
