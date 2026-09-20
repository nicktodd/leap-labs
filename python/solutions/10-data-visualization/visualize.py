from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent
trades = pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])

# 1. Bar chart: total value by asset class
totals = trades.groupby("asset_class")["value"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(totals.index, totals.values, color="#1E6FA8")
ax.set_title("Total Trade Value by Asset Class ($)")
ax.set_xlabel("Asset Class")
ax.set_ylabel("Total Value ($)")
ax.set_ylim(bottom=0)
fig.tight_layout()
fig.savefig(OUT / "chart_asset_class.png")
plt.close(fig)

# 2. Line chart: total value by week
by_week = trades.set_index("trade_date")["value"].resample("W").sum()
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(by_week.index, by_week.values, marker="o", color="#1E6FA8")
ax.set_title("Total Trade Value by Week ($)")
ax.set_xlabel("Week Ending")
ax.set_ylabel("Total Value ($)")
ax.set_xticks(by_week.index)
ax.set_xticklabels([d.strftime("%Y-%m-%d") for d in by_week.index])
fig.tight_layout()
fig.savefig(OUT / "chart_weekly_trend.png")
plt.close(fig)

# 3. Scatter plot: quantity vs value, Equity only
equity = trades[trades["asset_class"] == "Equity"]
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(equity["quantity"], equity["value"], color="#1E6FA8")
ax.set_title("Equity Trades: Quantity vs. Value")
ax.set_xlabel("Quantity")
ax.set_ylabel("Value ($)")
fig.tight_layout()
fig.savefig(OUT / "chart_quantity_vs_value.png")
plt.close(fig)

# 4. Misleading chart: y-axis truncated just below the smallest bar, exaggerating
#    the visual difference between advisors even though the underlying numbers
#    (115,569 vs. 72,669 vs. 13,822) are already genuinely different.
by_advisor = trades.groupby("advisor")["value"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(by_advisor.index, by_advisor.values, color="#C0392B")
ax.set_title("Total Trade Value by Advisor ($) -- misleading: truncated y-axis")
ax.set_ylabel("Total Value ($)")
ax.set_ylim(bottom=13000)
fig.tight_layout()
fig.savefig(OUT / "chart_misleading.png")
plt.close(fig)

print("Saved 4 charts to this folder (not committed to git).")
