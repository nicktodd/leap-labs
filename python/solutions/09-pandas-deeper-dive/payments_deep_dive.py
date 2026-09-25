from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
customers = pd.read_csv(SHARED / "customers.csv")
fx = pd.read_csv(SHARED / "fx_rates.csv")

print(f"transactions: {len(txns)} rows, customers: {len(customers)} rows, fx rates: {len(fx)} rows")

# --- 1. FX merge ---
# validate="many_to_one" makes pandas raise MergeError if a currency appears more than once in
# fx_rates.csv. Without it, a duplicated rate row (for example two EUR rates from different
# days) would silently duplicate every EUR transaction and inflate every total.
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)
assert len(txns) == 140, "the FX merge must not change the row count"
assert txns["rate_to_gbp"].notna().all(), "every currency needs a rate"
print(f"\n1. FX merge: {len(txns)} rows, total amount_gbp = {txns['amount_gbp'].sum():,.2f}")

# --- 2. Customer merge ---
cust_cols = customers.drop(columns="customer_name")  # txns already has customer_name
merged = txns.merge(cust_cols, on="customer_id", how="left", indicator=True,
                    validate="many_to_one")
print("\n2. Customer merge (how='left', indicator=True):")
print(merged["_merge"].value_counts().to_string())
orphans = merged[merged["_merge"] == "left_only"]
print(f"orphan rows: {len(orphans)}, customers: {orphans['customer_id'].unique().tolist()} "
      f"({orphans['customer_name'].iloc[0]}), amount_gbp = {orphans['amount_gbp'].sum():,.2f}")
inner_rows = len(txns.merge(cust_cols, on="customer_id", how="inner", validate="many_to_one"))
print(f"row count: inner join = {inner_rows}, left join = {len(merged)}")
merged["segment"] = merged["segment"].fillna("Unknown")
# Keep the left join. The 10 K012 rows are genuine transactions; the customer is missing from
# customers.csv because the reference data lags behind. An inner join would silently drop
# them, understating the month's total by 479.02 GBP and hiding a data-quality issue that the
# reference-data team needs to fix. Labelling the segment "Unknown" keeps them visible.

# --- 3. Named aggregation per segment (all transactions) ---
merged["declined"] = merged["status"] == "DECLINED"
by_segment = merged.groupby("segment").agg(
    txn_count=("txn_id", "count"),
    customers=("customer_id", "nunique"),
    total_gbp=("amount_gbp", "sum"),
    avg_gbp=("amount_gbp", "mean"),
    decline_rate=("declined", "mean"),
    fraud_count=("is_fraud", "sum"),
).sort_values("total_gbp", ascending=False)
print("\n3. Summary by segment (all transactions):")
print(by_segment.round({"total_gbp": 2, "avg_gbp": 2, "decline_rate": 3}))

# From here on, "spend" means APPROVED transactions only: a declined payment moves no money.
spend = merged[merged["status"] == "APPROVED"]
print(f"\napproved transactions: {len(spend)}, approved spend: {spend['amount_gbp'].sum():,.2f} GBP")

# --- 4. pivot_table ---
pivot = spend.pivot_table(index="merchant_category", columns="channel", values="amount_gbp",
                          aggfunc="sum", fill_value=0, margins=True, margins_name="Total")
print("\n4. Approved spend (GBP) by merchant category and channel:")
print(pivot.round(2))
margin_total = pivot.loc["Total", "Total"]
print(f"margin total {margin_total:,.2f} equals approved spend: "
      f"{abs(margin_total - spend['amount_gbp'].sum()) < 0.005}")
# The zero cells (for example Retail/In-store) mean no approved transactions at all, not
# transactions that summed to 0: fill_value=0 replaces NaN for display and arithmetic.

# --- 5. Time series ---
by_time = spend.set_index("txn_timestamp").sort_index()
daily = by_time["amount_gbp"].resample("D").sum()
print(f"\n5. Daily spend: {len(daily)} days, {(daily == 0).sum()} days with zero spend")
# resample("D") creates one row per calendar day, and a day with no transactions would appear
# with a sum of 0. groupby(dt.date) would leave such a day out, and a rolling mean over it
# would then span more than 7 calendar days. In this month every day has approved spend.
rolling_7d = daily.rolling(7).mean()  # the first 6 days are NaN: fewer than 7 values
daily_view = pd.DataFrame({"daily_gbp": daily, "rolling_7d_gbp": rolling_7d}).round(2)
print(daily_view.tail(10))

weekly = by_time["amount_gbp"].resample("W-SUN").agg(["sum", "count"])
weekly.columns = ["spend_gbp", "txn_count"]
print("\nWeekly approved spend (weeks end on Sunday):")
print(weekly.round(2))
top_week = weekly["spend_gbp"].idxmax()
print(f"highest week ends {top_week:%a %d %b %Y}: {weekly.loc[top_week, 'spend_gbp']:,.2f} GBP")

# Payday effect: compare all transaction attempts per day before and from Fri 27 Feb.
payday = pd.Timestamp("2026-02-27")
daily_all = merged.set_index("txn_timestamp").sort_index()["txn_id"].resample("D").count()
daily_spend_count = by_time["txn_id"].resample("D").count()
for label, mask in [("before payday", daily_all.index < payday),
                    ("from payday", daily_all.index >= payday)]:
    print(f"{label:>14}: {daily_all[mask].mean():.2f} transactions/day, "
          f"{daily_spend_count[mask].mean():.2f} approved/day, "
          f"{daily[mask].mean():,.2f} GBP approved spend/day")

# --- 6. Takeaways (written with a partner) ---
# - K012's 10 transactions (479.02 GBP) have no customer record: 7.1% of rows would vanish with
#   an inner join, so the left join and an "Unknown" segment are kept.
# - Standard customers carry 9 of the 12 fraud cases and the highest decline rate (0.152),
#   against 0.000 for Business.
# - Online is 8,333.80 of the 11,471.55 GBP approved spend (72.6%), and Travel alone is
#   4,704.40, all of it Online.
# - The highest week is the one ending Sun 1 Mar (3,978.87 GBP, 36 approved transactions),
#   which contains payday; from Fri 27 Feb attempts rise from 4.76 to 7.00 per day.
# - Weekly spend includes approved fraud: the week ending 22 Feb (3,720.33) contains the
#   2,145.31 fraudulent flight (P0094), and 1 Mar's 1,147.88 includes the 780.00 cloned-card
#   payment (K011), so spend totals alone overstate both the mid-month peak and the payday bump.
