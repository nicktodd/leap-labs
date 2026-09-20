from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "messy-trades-raw.csv"

df = pd.read_csv(DATA_PATH)

# 1. quantity missing: no safe way to reconstruct a trade's quantity -> drop the row
df = df[df["quantity"].notna()].copy()
df["quantity"] = df["quantity"].astype(float)

# 2. value missing: derivable from quantity * price -> recompute rather than drop
missing_value = df["value"].isna()
df.loc[missing_value, "value"] = df.loc[missing_value, "quantity"] * df.loc[missing_value, "price"]

# 3. client_name missing: same client_id appears elsewhere with a name -> backfill
df["client_name"] = df.groupby("client_id")["client_name"].transform("first")

# 4. ambiguous date (05/01/2026): T0002 sits between T0001 (2026-01-05) and
#    T0003 (2026-01-06) by trade_id order, so it must be day-first: 2026-01-05, not 1 May.
df["trade_date"] = pd.to_datetime(df["trade_date"], format="mixed", dayfirst=True)

# 5. asset_class casing: a plain .str.capitalize() would turn "ETF" into "Etf" (it treats
#    ETF as a normal word, not an acronym) -> use an explicit canonical mapping instead.
ASSET_CLASS_CANONICAL = {"equity": "Equity", "bond": "Bond", "etf": "ETF", "crypto": "Crypto"}
df["asset_class"] = df["asset_class"].str.lower().map(ASSET_CLASS_CANONICAL)

# 6. exact duplicate row (T0006 appears twice, identically) -> safe to drop outright
df = df.drop_duplicates()

# 7. quantity outlier: T0021's quantity (99,999) is far outside every other Equity
#    trade's range. Flag it for review rather than dropping it — it could be a genuine
#    institutional block trade, or a fat-finger error (a missing decimal point:
#    999.99?). Next step: check the original order ticket with the trading desk before
#    deciding whether to correct or keep it.
equity_quantities = df.loc[df["asset_class"] == "Equity", "quantity"]
q3 = equity_quantities.quantile(0.75)
outliers = df[(df["asset_class"] == "Equity") & (df["quantity"] > q3 * 5)]

print("Distinct asset classes:", sorted(df["asset_class"].unique()))
print(f"\nFinal row count: {len(df)}")
print("\nFlagged outlier(s) for review:")
print(outliers[["trade_id", "instrument", "quantity"]])
