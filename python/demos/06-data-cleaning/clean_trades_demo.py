from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "messy-trades-raw.csv"

df = pd.read_csv(DATA_PATH)

# --- Part 1: quantify the damage ---
print("Missing values per column:")
print(df.isna().sum()[df.isna().sum() > 0])
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# --- Part 2: missing values, three different decisions ---

# quantity missing (T0005): can't be safely reconstructed -> drop the row
before = len(df)
df = df[df["quantity"].notna()].copy()
print(f"\nDropped {before - len(df)} row(s) with missing quantity (can't be reconstructed)")

# value missing (T0004): derivable from quantity * price -> recompute
df["quantity"] = df["quantity"].astype(float)
missing_value = df["value"].isna()
df.loc[missing_value, "value"] = df.loc[missing_value, "quantity"] * df.loc[missing_value, "price"]
print(f"Recomputed value for {missing_value.sum()} row(s) from quantity * price")

# client_name missing (T0010): backfill from another row sharing client_id
missing_name = df["client_name"].isna().sum()
df["client_name"] = df.groupby("client_id")["client_name"].transform("first")
print(f"Backfilled client_name for {missing_name} row(s) using a matching client_id")

# --- Part 3: data types, including dates ---
# 05/01/2026 is ambiguous on its own; T0002 sits between T0001 (2026-01-05) and
# T0003 (2026-01-06), so it must be day-first: 2026-01-05, not 1 May.
df["trade_date"] = pd.to_datetime(df["trade_date"], format="mixed", dayfirst=True)
print(f"\ntrade_date dtype after parsing: {df['trade_date'].dtype}")

# .str.capitalize() alone would turn "ETF" into "Etf" — it doesn't know ETF is an
# acronym, only that it should upper-case the first letter and lower-case the rest.
# A canonical mapping avoids introducing a new inconsistency while fixing the old one.
ASSET_CLASS_CANONICAL = {"equity": "Equity", "bond": "Bond", "etf": "ETF", "crypto": "Crypto"}
df["asset_class"] = df["asset_class"].str.lower().map(ASSET_CLASS_CANONICAL)
print(f"Distinct asset classes after normalising case: {sorted(df['asset_class'].unique())}")

# --- Part 4: duplicates and outliers ---
before = len(df)
df = df.drop_duplicates()
print(f"\nDropped {before - len(df)} exact duplicate row(s)")

equity_quantities = df.loc[df["asset_class"] == "Equity", "quantity"]
q3 = equity_quantities.quantile(0.75)
outliers = df[(df["asset_class"] == "Equity") & (df["quantity"] > q3 * 5)]
print(f"\nFlagged {len(outliers)} outlier(s) for review (not auto-removed):")
print(outliers[["trade_id", "instrument", "quantity"]])

print(f"\nFinal clean row count: {len(df)}")
