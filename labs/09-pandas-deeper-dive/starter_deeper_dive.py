"""Lab 09: Pandas deeper dive — groupby agg, pivot_table, merge, resample."""

from pathlib import Path
import pandas as pd

BASE = Path(r"C:\Users\zackt\Documents\fidelity-leap-sprint4\shared")
trades = pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])
advisors = pd.read_csv(BASE / "advisors.csv")

# 1. groupby with multiple aggregations in one call
print("=== 1. Per-client value summary ===")
client_summary = trades.groupby("client_name")["value"].agg(["count", "sum", "mean"])
client_summary.columns = ["trade_count", "total_value", "mean_value"]
print(client_summary.to_string())

# 2. pivot_table: rows=instrument, columns=side, values=value, fill NaN with 0
print("\n=== 2. Pivot table: instrument x side ===")
pivot = pd.pivot_table(
    trades,
    index="instrument",
    columns="side",
    values="value",
    aggfunc="sum",
    fill_value=0,
)
print(pivot.to_string())

# 3. merge trades with advisors on "advisor", then total value by team
print("\n=== 3. Total value by team ===")
merged = trades.merge(advisors, on="advisor", how="left")
team_value = merged.groupby("team")["value"].sum().sort_values(ascending=False)
print(team_value.to_string())
# Confirm no missing teams
assert merged["team"].isna().sum() == 0, "Some trades have no team after merge!"

# 4. resample: total value per week
print("\n=== 4. Weekly total value ===")
weekly = trades.set_index("trade_date")["value"].resample("W").sum()
print(weekly.to_string())

# 5. Takeaways (each cites a specific number from the output above)
# - Alice Chen has the highest total trade value at $38,092.40, nearly matching Jamal Ferris ($37,510).
# - AAPL is the most actively traded instrument, with $67,192.40 in total BUY-side value and no SELLs in the pivot.
# - The Growth team accounts for $135,793.60 of the $202,059.45 total, versus $17,686.10 for Income.
# - The week of 2026-01-11 was the busiest single week by value, with $83,741.60 in trades.
# - BTC (Crypto) contributes $29,300.00 in total value despite only 3 trades — the highest mean per trade.
