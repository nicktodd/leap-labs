"""Lab 10: Data visualization — bar, line, scatter, and one misleading chart."""

from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(r"C:\Users\zackt\Documents\fidelity-leap-sprint4\shared")
OUT = Path(__file__).resolve().parent
trades = pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])

# 1. Bar chart: total value by asset_class
asset_totals = trades.groupby("asset_class")["value"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(asset_totals.index, asset_totals.values, color="steelblue")
ax.set_title("Total Trade Value by Asset Class (Jan 2026)")
ax.set_xlabel("Asset Class")
ax.set_ylabel("Total Value (USD/GBP)")
ax.set_ylim(0, asset_totals.max() * 1.15)
fig.tight_layout()
fig.savefig(OUT / "chart_asset_class.png", dpi=150)
plt.close(fig)
print("Saved chart_asset_class.png")

# 2. Line chart: total value by week
weekly = trades.set_index("trade_date")["value"].resample("W").sum()
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(weekly.index, weekly.values, marker="o", color="darkgreen")
ax.set_title("Total Trade Value by Week (Jan 2026)")
ax.set_xlabel("Week ending")
ax.set_ylabel("Total Value (USD/GBP)")
ax.set_ylim(0)
fig.tight_layout()
fig.savefig(OUT / "chart_weekly_trend.png", dpi=150)
plt.close(fig)
print("Saved chart_weekly_trend.png")

# 3. Scatter plot: quantity vs value, Equity trades only
equity = trades[trades["asset_class"] == "Equity"]
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(equity["quantity"], equity["value"], alpha=0.7, color="darkorange")
ax.set_title("Equity Trades: Quantity vs. Value (Jan 2026)")
ax.set_xlabel("Quantity (shares)")
ax.set_ylabel("Trade Value (USD)")
fig.tight_layout()
fig.savefig(OUT / "chart_quantity_vs_value.png", dpi=150)
plt.close(fig)
print("Saved chart_quantity_vs_value.png")

# 4. Misleading chart: truncated y-axis on the asset-class bar chart.
# FLAW: the y-axis starts at 60,000 instead of 0, which makes Equity look roughly 10x larger
# than Bond when the actual ratio is about 6x — an honest axis would start at 0.
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(asset_totals.index, asset_totals.values, color="steelblue")
ax.set_title("Total Trade Value by Asset Class (MISLEADING — truncated y-axis)")
ax.set_xlabel("Asset Class")
ax.set_ylabel("Total Value (USD/GBP)")
ax.set_ylim(60000, asset_totals.max() * 1.05)  # deliberate truncation to exaggerate differences
fig.tight_layout()
fig.savefig(OUT / "chart_misleading.png", dpi=150)
plt.close(fig)
print("Saved chart_misleading.png")
