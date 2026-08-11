"""Lab 05: Pandas fundamentals — DataFrames, selection, and groupby."""

from pathlib import Path
import pandas as pd

DATA_PATH = Path(r"C:\Users\zackt\Documents\leap-sprint4\shared\trades.csv")

# 1. Load into a DataFrame
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} rows.\n")

# 2. Select SELL-only trades using .loc + boolean indexing
sell_trades = df.loc[df["side"] == "SELL", ["trade_id", "client_name", "value"]]
print("SELL-only trades:")
print(sell_trades.to_string(index=False))

# 3. Per-client value summary using groupby — replaces Module 3's manual dict loop
client_totals = df.groupby("client_name")["value"].sum().sort_index()
print("\nPer-client total value (groupby):")
print(client_totals.to_string())

# Comment: groupby("client_name")["value"].sum() is doing exactly what Module 3's
# manual loop did: it groups all rows that share the same client_name together,
# then for each group sums the value column — equivalent to iterating rows and
# accumulating client_totals[name] += float(row["value"]), but expressed in one
# vectorised pandas operation instead of ~5 lines of explicit Python.

# 4. Distinct advisors using unique()
advisors = df["advisor"].unique()
print(f"\nDistinct advisors: {sorted(advisors)}")

# 5. Line count comparison
print("\n--- Comparison ---")
print("Module 3 per-client summary loop: ~5 lines (for row in rows: ... accumulate dict)")
print("Pandas groupby line: 1 line")
print("pandas is grouping all rows by client_name and summing value in one vectorised call,")
print("equivalent to the manual dict-accumulation loop but faster and with far less code.")
