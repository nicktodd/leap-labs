from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2] / "shared"
trades = pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])
advisors = pd.read_csv(BASE / "advisors.csv")

# --- Part 1: groupby with multiple aggregations ---
print("Value by advisor: count, sum, and mean in one call")
print(trades.groupby("advisor")["value"].agg(["count", "sum", "mean"]).round(2))

# --- Part 2: pivot_table ---
print("\nTotal value by asset class and side (a wide, cross-tabulated summary):")
pivot = trades.pivot_table(
    index="asset_class", columns="side", values="value", aggfunc="sum", fill_value=0
)
print(pivot)

# --- Part 3: merge ---
print("\nAdvisors reference table:")
print(advisors)

merged = trades.merge(advisors, on="advisor", how="left")
print("\nTotal value by team (only answerable once trades and advisors are combined):")
print(merged.groupby("team")["value"].sum())

# --- Part 4: time series basics ---
by_date = trades.set_index("trade_date")
print("\nWeekly total value (resample is groupby, for time):")
print(by_date["value"].resample("W").sum())
