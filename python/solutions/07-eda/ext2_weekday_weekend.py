from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)

# Aggregate to one row per calendar day first. resample("D") also creates rows for days with
# no transactions (count 0, spend 0), which a plain groupby on the date would leave out.
daily = txns.set_index("txn_timestamp").resample("D").agg(
    {"amount_gbp": "sum", "txn_id": "count"}
).rename(columns={"amount_gbp": "spend_gbp", "txn_id": "txn_count"})
daily["day_type"] = daily.index.dayofweek.map(lambda d: "Weekend" if d >= 5 else "Weekday")

summary = daily.groupby("day_type").agg(
    days=("spend_gbp", "size"),
    mean_daily_spend_gbp=("spend_gbp", "mean"),
    mean_daily_txns=("txn_count", "mean"),
)
print("Per-day averages:")
print(summary.round(2).to_string())

# The misleading alternative: average the individual transactions in each group.
per_txn = txns.groupby(txns["txn_timestamp"].dt.dayofweek >= 5)["amount_gbp"].agg(["count", "mean"])
per_txn.index = per_txn.index.map({False: "Weekday", True: "Weekend"})
print("\nPer-transaction averages (answers a different question):")
print(per_txn.round(2).to_string())

# The question is "is a weekend day busier than a weekday?". There are 20 weekdays and 8
# weekend days in the period, so comparing totals would favour weekdays for no reason, and a
# mean per transaction says how big each payment is, not how much happens on a day. A group
# with fewer but larger payments can have a higher mean per transaction and lower daily spend.
# Aggregating to days first puts both groups on the same unit: one day.
