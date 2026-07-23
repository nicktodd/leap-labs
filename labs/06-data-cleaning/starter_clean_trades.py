"""Lab 06: Data cleaning — handle messy-trades-raw.csv."""

from pathlib import Path
import pandas as pd

DATA_PATH = Path(r"C:\Users\zackt\Documents\fidelity-leap-sprint4\shared\messy-trades-raw.csv")

df = pd.read_csv(DATA_PATH)
print(f"Starting row count: {len(df)}")

# 1. Drop the row with missing quantity — it cannot be reconstructed without the unit count.
df = df.dropna(subset=["quantity"])

# 2. Recompute the missing value as quantity * price — we have both components so we can
#    derive it rather than discarding a valid trade.
missing_val_mask = df["value"].isna()
df.loc[missing_val_mask, "value"] = df.loc[missing_val_mask, "quantity"] * df.loc[missing_val_mask, "price"]

# 3. Backfill the missing client_name from another row with the same client_id —
#    C007 appears with a name elsewhere so we can look it up rather than drop or guess.
client_name_lookup = (
    df.dropna(subset=["client_name"])
    .drop_duplicates(subset=["client_id"])
    .set_index("client_id")["client_name"]
)
missing_name_mask = df["client_name"].isna()
df.loc[missing_name_mask, "client_name"] = df.loc[missing_name_mask, "client_id"].map(client_name_lookup)

# 4. Parse trade_date correctly, resolving the ambiguous DD/MM/YYYY row.
#    T0002 has date "05/01/2026". Looking at the surrounding trade_id sequence:
#    T0001 is 2026-01-05 and T0003 is 2026-01-06, so T0002 must also be 2026-01-05 (Jan 5).
#    The format is DD/MM/YYYY (day-first), not MM/DD/YYYY.
df["trade_date"] = pd.to_datetime(df["trade_date"], format="mixed", dayfirst=True)

# 5. Normalise asset_class casing using a canonical mapping — a generic .str.capitalize()
#    would produce "Etf" instead of "ETF", so we map each known variant explicitly.
ASSET_CLASS_MAP = {
    "equity": "Equity",
    "bond": "Bond",
    "etf": "ETF",
    "crypto": "Crypto",
    "Equity": "Equity",
    "Bond": "Bond",
    "ETF": "ETF",
    "Crypto": "Crypto",
}
df["asset_class"] = df["asset_class"].map(ASSET_CLASS_MAP)
print(f"Distinct asset_class values after normalisation: {df['asset_class'].unique()}")

# 6. Drop exact duplicate rows — T0006 appears twice; keep the first occurrence.
df = df.drop_duplicates()

# 7. Flag the quantity outlier — T0021 (Kwame Osei, AAPL Equity BUY, qty=99999) is orders of
#    magnitude larger than any other Equity trade (next highest is 200). Print but don't drop it.
#    Investigation note: I would contact the advisor (R. Alvarez) and the client to confirm the
#    order size; a 99,999-share equity ticket could be a data-entry error (extra 9) or a fat-finger,
#    and comparing with the client's historical order sizes and account balance would confirm or
#    rule it out.
equity_df = df[df["asset_class"] == "Equity"]
qty_mean = equity_df["quantity"].mean()
qty_std = equity_df["quantity"].std()
outlier_mask = (df["asset_class"] == "Equity") & (df["quantity"] > qty_mean + 3 * qty_std)
outliers = df[outlier_mask]
if not outliers.empty:
    print("\nQuantity outlier(s) flagged (not dropped):")
    print(outliers[["trade_id", "client_name", "instrument", "quantity", "value"]].to_string(index=False))

print(f"\nFinal row count: {len(df)}")
assert len(df) == 20, f"Expected 20 rows, got {len(df)}"
