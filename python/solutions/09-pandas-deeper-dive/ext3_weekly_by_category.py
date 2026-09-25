from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)
spend = txns[txns["status"] == "APPROVED"]

# pd.Grouper does a resample inside a groupby, so time buckets and a category can be grouped
# together in one call. The timestamp stays a column; no set_index is needed.
weekly_long = spend.groupby(
    [pd.Grouper(key="txn_timestamp", freq="W-SUN"), "merchant_category"]
)["amount_gbp"].sum()
print(f"long result: {len(weekly_long)} (week, category) pairs that have spend")

# unstack moves merchant_category from the row index to the columns. Pairs with no spend
# become NaN unless fill_value is given.
weekly = weekly_long.unstack("merchant_category", fill_value=0)
weekly["Total"] = weekly.sum(axis=1)
weekly.index = weekly.index.strftime("w/e %d %b")
print("\nApproved spend (GBP) per week and merchant category:")
print(weekly.round(2).to_string())

# Cross-check against the core task's resample("W-SUN") totals.
check = spend.set_index("txn_timestamp")["amount_gbp"].resample("W-SUN").sum()
assert (abs(weekly["Total"].to_numpy() - check.to_numpy()) < 0.005).all()
print("weekly totals match resample('W-SUN'): True")

print("\nLargest category each week:")
print(weekly.drop(columns="Total").idxmax(axis=1).to_string())
# Travel is the largest category in three of the four weeks and explains most of the rise in
# weekly spend: 2,563.98 in the week ending 22 Feb (including the 2,145.31 fraudulent British
# Airways booking) and 1,202.97 in the final week (K007's flight). Electronics jumps to 1,149.06
# in the final week, which includes K011's 780.00 cloned-card payment. Groceries is the steadiest
# category (176.91 to 395.50 per week).
