from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2] / "shared"
trades = pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])
advisors = pd.read_csv(BASE / "advisors.csv")

# 1. groupby with multiple aggregations
print("Value by client: count, sum, mean")
by_client = trades.groupby("client_name")["value"].agg(["count", "sum", "mean"]).round(2)
print(by_client)

# 2. pivot_table
print("\nTotal value by instrument and side:")
pivot = trades.pivot_table(
    index="instrument", columns="side", values="value", aggfunc="sum", fill_value=0
)
print(pivot)

# 3. merge
merged = trades.merge(advisors, on="advisor", how="left")
print("\nTotal value by team:")
by_team = merged.groupby("team")["value"].sum()
print(by_team)

# 4. resample
by_week = trades.set_index("trade_date")["value"].resample("W").sum()
print("\nTotal value by week:")
print(by_week)

# 5. Takeaways
# - Alice Chen has the highest total value (38,092.40) of any client, across 3 trades.
# - ETH and US10Y are the only two instruments with zero SELL value in this book
#   (both entirely BUY); every other instrument has trades on both sides.
# - The Growth team (J. Okafor + S. Rahman) accounts for 188,237.60 of value, more than
#   13x the Income team's 13,822.05 — almost entirely a headcount effect (2 advisors vs. 1).
# - Week 1 (up to 2026-01-11) saw 122,204.85 in value, well ahead of week 2's 79,854.80 —
#   trading activity front-loaded in this two-week book.
