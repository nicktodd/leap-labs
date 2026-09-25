from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

BLUE = "#2a78d6"
PAYDAY = pd.Timestamp("2026-02-27")  # Friday 27 February

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)

daily = txns.set_index("txn_timestamp").resample("D").agg(
    {"amount_gbp": "sum", "txn_id": "count"}
).rename(columns={"amount_gbp": "spend_gbp", "txn_id": "txn_count"})

before = daily.loc[daily.index < PAYDAY, "txn_count"]
after = daily.loc[daily.index >= PAYDAY, "txn_count"]
print(f"mean transactions per day before payday: {before.mean():.2f} ({len(before)} days)")
print(f"mean transactions per day from payday:   {after.mean():.2f} ({len(after)} days)")
peak_day = daily["spend_gbp"].idxmax()
peak_txn = txns.loc[txns["txn_timestamp"].dt.normalize() == peak_day].nlargest(1, "amount_gbp").iloc[0]
print(f"highest spend day: {peak_day:%a %d %b} £{daily['spend_gbp'].max():,.2f}; "
      f"largest payment {peak_txn['txn_id']} £{peak_txn['amount_gbp']:,.2f} "
      f"(is_fraud = {peak_txn['is_fraud']})")

# The payday bump shows in the NUMBER of transactions, not in GBP spend: spend is dominated by
# a few large payments (several of them fraud), which hide a change in everyday activity.
# Two panels that share the date axis let both stories be annotated without a second y-axis.
fig, (ax_spend, ax_count) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

ax_spend.plot(daily.index, daily["spend_gbp"], color=BLUE, marker="o", markersize=4)
ax_spend.set_ylim(0, daily["spend_gbp"].max() * 1.2)
ax_spend.yaxis.set_major_formatter(StrMethodFormatter("£{x:,.0f}"))
ax_spend.set_title("Daily spend (GBP): the peaks are single large payments")
ax_spend.set_ylabel("Spend (GBP)")
ax_spend.annotate(
    f"{peak_txn['txn_id']}: one £{peak_txn['amount_gbp']:,.0f} payment, confirmed fraud",
    xy=(peak_day, daily["spend_gbp"].max()),
    xytext=(pd.Timestamp("2026-02-04"), daily["spend_gbp"].max() * 1.05),
    arrowprops={"arrowstyle": "->", "color": "0.3"}, va="center",
)

ax_count.plot(daily.index, daily["txn_count"], color=BLUE, marker="o", markersize=4)
ax_count.set_ylim(0, daily["txn_count"].max() + 2)
ax_count.axvspan(PAYDAY - pd.Timedelta(hours=12), daily.index.max() + pd.Timedelta(hours=12),
                 color="0.92", zorder=0)
ax_count.annotate(
    f"Payday (Fri 27 Feb): {after.mean():.1f} transactions a day,\nup from {before.mean():.1f}",
    xy=(PAYDAY, daily.loc[PAYDAY, "txn_count"]),
    xytext=(pd.Timestamp("2026-02-15"), daily["txn_count"].max() + 1),
    arrowprops={"arrowstyle": "->", "color": "0.3"}, va="center",
)
ax_count.set_title("Transactions per day: the payday bump")
ax_count.set_ylabel("Number of transactions")
ax_count.set_xlabel("Date (Feb - Mar 2026)")
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(OUT / "daily_payday_annotated.png", dpi=120)
plt.close(fig)
print("saved output/daily_payday_annotated.png")
