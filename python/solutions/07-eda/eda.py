from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

print(f"Shape: {df.shape}")
print("\ndescribe() on numeric columns:")
print(df[["quantity", "price", "value"]].describe())

# Anomaly: value is stored in the trade's own currency, not a common one. Summing or
# averaging value across currencies without converting first mixes USD and GBP amounts
# as if they were the same unit — a genuine anomaly worth flagging, not just splitting by.
print("\nTrade count and mean value by currency (not directly comparable across currencies):")
print(df.groupby("currency")["value"].agg(["count", "mean"]))

print("\nTotal value by client (highest total value):")
by_client_value = df.groupby("client_name")["value"].sum().sort_values(ascending=False)
print(by_client_value.head(3))

print("\nTrade count by client (highest trade count):")
by_client_count = df.groupby("client_name")["value"].count().sort_values(ascending=False)
print(by_client_count.head(3))

print("\nTotal value by equity instrument:")
equity = df[df["asset_class"] == "Equity"]
print(equity.groupby("instrument")["value"].sum().sort_values(ascending=False))

# Pattern: Equity trades (11 of 20) outnumber every other asset class combined (9 of 20).
# Anomaly: value mixes USD and GBP without conversion (see currency segmentation above) —
#          any total or mean across the whole book is only meaningful within one currency.
# Hypothesis: clients served by J. Okafor (the advisor with the most trades) have a higher
#             mean trade value than clients served by the other two advisors — checkable
#             directly with df.groupby("advisor")["value"].mean(), and properly testable
#             with Module 8's statistical tools rather than eyeballing the means.
print("\nHypothesis check (mean value by advisor):")
print(df.groupby("advisor")["value"].mean().sort_values(ascending=False))
