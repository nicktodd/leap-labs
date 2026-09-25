from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
fx = pd.read_csv(SHARED / "fx_rates.csv")

# --- 1. Derived columns ---
# amount is in three different currencies, so every money comparison below uses amount_gbp.
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)
txns["hour"] = txns["txn_timestamp"].dt.hour
txns["weekday"] = txns["txn_timestamp"].dt.day_name()
print(f"Loaded {len(txns)} transactions, "
      f"{txns['txn_timestamp'].min():%d %b %Y} to {txns['txn_timestamp'].max():%d %b %Y}")

# --- 2. Distribution of amount_gbp ---
print("\n2. amount_gbp distribution")
print(txns["amount_gbp"].describe(percentiles=[0.5, 0.9, 0.99]).round(2).to_string())
# The mean (129.18) is more than three times the median (39.75): a long right tail. Half of
# all payments are under GBP 40, but a few large Electronics/Travel payments (max 2,145.31)
# pull the mean up. The 99th percentile (1,300.61) is more than four times the 90th (295.33),
# so the tail is a handful of rows. The standard deviation (291.75) is larger than the mean,
# another sign of skew. "Typical payment" should be reported as the median for this data.

# --- 3. Spend by merchant category ---
by_category = (
    txns.groupby("merchant_category")["amount_gbp"]
    .agg(txn_count="count", total_gbp="sum")
    .sort_values("total_gbp", ascending=False)
)
by_category["share_pct"] = (by_category["total_gbp"] / by_category["total_gbp"].sum() * 100).round(1)
print("\n3. Spend by merchant category (GBP)")
print(by_category.round(2).to_string())
# Count and value tell different stories: Transport (37) and Groceries (26) are the most
# frequent categories but hold under 15% of spend between them, while Electronics (9) and
# Travel (6) are rare but carry 62.9% of the money.

# --- 4. Decline rate by channel ---
# The mean of a boolean column is the share of True values, so groupby().mean() on it gives a
# rate directly.
txns["declined"] = txns["status"] == "DECLINED"
decline_by_channel = txns.groupby("channel")["declined"].agg(txns="count", declines="sum", rate="mean")
print("\n4. Decline rate by channel")
print(decline_by_channel.round(3).to_string())
print("\nStatus share within each channel (crosstab, normalize='index'):")
print(pd.crosstab(txns["channel"], txns["status"], normalize="index").round(3).to_string())
# normalize="index" makes each row sum to 1, so rows of different sizes are comparable.
# Online: 11 of 71 declined (15.5%); Contactless 1 of 45 (2.2%); In-store 1 of 24 (4.2%).
# The card-present counts are very small, which matters when Module 8 tests this.

# --- 5. Hour bands ---
# pd.cut bins are right-inclusive by default, so edges -1, 5, 11, 17, 23 give 0-5, 6-11,
# 12-17 and 18-23.
txns["hour_band"] = pd.cut(
    txns["hour"],
    bins=[-1, 5, 11, 17, 23],
    labels=["Night 00-05", "Morning 06-11", "Afternoon 12-17", "Evening 18-23"],
)
by_band = txns.groupby("hour_band", observed=True).agg(
    txn_count=("txn_id", "count"),
    decline_rate=("declined", "mean"),
    fraud_rate=("is_fraud", "mean"),
)
print("\n5. Hour bands")
print(by_band.round(3).to_string())
# All 10 Night transactions are confirmed fraud and 6 of them were declined. No declines and
# no fraud happen in the Morning band. Ten rows is a small group, so this is a pattern to
# investigate, not a rule.

# --- 6. The currency anomaly ---
raw_total = txns["amount"].sum()
gbp_total = txns["amount_gbp"].sum()
print("\n6. Currency anomaly")
print(f"sum of raw amount:  {raw_total:,.2f}  (mixes GBP, EUR and USD)")
print(f"sum of amount_gbp:  {gbp_total:,.2f}")
print(f"overstatement:      {raw_total - gbp_total:,.2f}")
by_currency = txns.groupby("currency").agg(
    txn_count=("amount", "count"), raw_amount=("amount", "sum"), amount_gbp=("amount_gbp", "sum")
)
by_currency["difference"] = by_currency["raw_amount"] - by_currency["amount_gbp"]
print(by_currency.round(2).to_string())
# Summing amount treats EUR 100 and USD 100 as GBP 100. The GBP rows are unaffected; the whole
# overstatement (2,677.76) comes from the EUR and USD rows, and the 8 USD rows alone account
# for 1,924.13 of it. Any total built from amount is wrong.

# --- 7. Findings ---
# Pattern: the Night band (00:00-05:59) holds 10 of 140 transactions, and all 10 are confirmed
#   fraud; 6 of them were declined.
# Anomaly: summing the raw amount column gives 20,762.64, overstating February spend by
#   GBP 2,677.76 because it adds EUR and USD amounts as if they were GBP.
# Hypothesis: Online transactions are declined more often than card-present (In-store and
#   Contactless) transactions, and the difference is larger than chance would explain.
#   Checkable in Module 8 with a chi-square test of independence on channel x declined.
