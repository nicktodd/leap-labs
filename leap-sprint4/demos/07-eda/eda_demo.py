from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

# --- Part 2: shape and summary statistics ---
print(f"Shape: {df.shape}")
print("\ndescribe() on numeric columns:")
print(df[["quantity", "price", "value"]].describe())

# --- Part 3: segmenting ---
print("\nTrade count by asset class:")
print(df["asset_class"].value_counts())

print("\nTrade count by asset class, as a proportion of the book:")
print(df["asset_class"].value_counts(normalize=True).round(2))

print("\nTrade count by advisor:")
print(df["advisor"].value_counts())

# crosstab: a two-way segmentation, asset class against side, in one table
print("\nAsset class by side (crosstab):")
print(pd.crosstab(df["asset_class"], df["side"]))

# a first glance at correlation between numeric columns — Module 8 covers what this
# actually means and how to interpret it properly; here it's just another thing to notice
print("\nCorrelation between numeric columns (a first glance, not a conclusion):")
print(df[["quantity", "price", "value"]].corr(numeric_only=True).round(2))

# --- Part 4: a segment-level comparison, and a hypothesis ---
print("\nValue by side (BUY vs SELL):")
print(df.groupby("side")["value"].agg(["count", "mean", "sum"]))

print(
    "\nHypothesis: BUY trades are, on average, larger in value than SELL trades "
    "in this book. Module 8 covers the statistical tools to test this properly — "
    "this module only surfaces it as a pattern worth checking."
)
