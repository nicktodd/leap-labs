from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, PercentFormatter, StrMethodFormatter

SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

BLUE = "#2a78d6"
ORANGE = "#eb6834"
GBP_TICKS = StrMethodFormatter("£{x:,.0f}")

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)


def style_axes(ax, title, xlabel, ylabel, grid_axis="y"):
    """Apply the house style to one Axes, so every chart in the dashboard looks the same.

    grid_axis is the value axis: "y" for vertical bars and lines, "x" for horizontal bars.
    Grid lines along a category axis add clutter without helping anyone read a value.
    """
    ax.set_title(title, fontsize=11, loc="left")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)  # remove the box: less ink, same data
    ax.grid(axis=grid_axis, color="0.9", linewidth=0.8)
    ax.set_axisbelow(True)  # grid lines behind the bars and lines, not over them


# Each panel function draws onto an Axes it is given, instead of creating its own figure.
# That is what lets the same code fill one cell of a grid.
def panel_categories(ax):
    totals = txns.groupby("merchant_category")["amount_gbp"].sum().sort_values()
    bars = ax.barh(totals.index, totals.values, color=BLUE)
    ax.bar_label(bars, labels=[f"£{v:,.0f}" for v in totals.values], padding=2, fontsize=8)
    ax.set_xlim(0, totals.max() * 1.2)
    ax.xaxis.set_major_formatter(GBP_TICKS)
    style_axes(ax, "Electronics and Travel carry most spend", "Total spend (GBP)", "", grid_axis="x")


def panel_daily(ax):
    daily = txns.set_index("txn_timestamp")["amount_gbp"].resample("D").sum()
    ax.plot(daily.index, daily.values, color=BLUE, marker="o", markersize=3, label="Daily")
    ax.plot(daily.index, daily.rolling(7).mean(), color=ORANGE, linewidth=2.5,
            label="7-day mean")
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(GBP_TICKS)
    ax.legend(fontsize=8)
    ax.tick_params(axis="x", labelrotation=30)
    style_axes(ax, "Daily spend with 7-day rolling mean", "Date", "Spend (GBP)")


def panel_declines(ax):
    rate = (txns["status"] == "DECLINED").groupby(txns["channel"]).mean().sort_values(ascending=False)
    bars = ax.bar(rate.index, rate.values, color=BLUE)
    ax.bar_label(bars, labels=[f"{r:.1%}" for r in rate.values], padding=2, fontsize=8)
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    style_axes(ax, "Online is declined most often", "Channel", "Decline rate")


def panel_hours(ax):
    counts = txns["txn_timestamp"].dt.hour.value_counts().reindex(range(24), fill_value=0)
    ax.bar(counts.index, counts.values, color=BLUE)
    ax.set_xticks(range(0, 24, 3))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # counts are whole numbers
    style_axes(ax, "Transactions by hour of day", "Hour", "Number of transactions")


fig, axes = plt.subplots(2, 2, figsize=(13, 8))
panel_categories(axes[0, 0])
panel_daily(axes[0, 1])
panel_declines(axes[1, 0])
panel_hours(axes[1, 1])
fig.suptitle("PaySprint card payments, 2 Feb - 1 Mar 2026 (all amounts in GBP)", fontsize=14)
fig.tight_layout()
fig.savefig(OUT / "dashboard.png", dpi=120)
plt.close(fig)
print("saved output/dashboard.png (4 panels)")
