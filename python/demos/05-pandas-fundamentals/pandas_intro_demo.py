from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"

# --- Part 1: DataFrame and Series ---
df = pd.read_csv(DATA_PATH)
print(f"df is a {type(df).__name__}")
print(df.head(3))

value_series = df["value"]
print(f"\ndf['value'] is a {type(value_series).__name__}")

# --- Part 2: indexing and selection ---
print("\nFirst row (iloc, position-based):")
print(df.iloc[0])

print("\nBUY trades only (loc, condition-based):")
print(df.loc[df["side"] == "BUY", ["trade_id", "instrument", "value"]].head())

# --- Part 3: groupby, compared to Module 3's manual loop ---
print("\nTotal value by instrument (pandas):")
print(df.groupby("instrument")["value"].sum())

print("\nTotal BUY value by instrument (filter, then groupby):")
print(df[df["side"] == "BUY"].groupby("instrument")["value"].sum())
