from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # no display needed: every chart is written to a PNG file
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, StrMethodFormatter

SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

BLUE = "#2a78d6"    # main series colour
ORANGE = "#eb6834"  # second series / highlight
GBP_TICKS = "£{x:,.0f}"  # axis tick format: £1,500

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=120)
    plt.close(fig)  # free the memory; scripts that make many figures otherwise warn
    print(f"saved output/{name}")


def plot_category_spend():
    """1. Horizontal bar: category names are long, and horizontal bars keep them readable."""
    totals = txns.groupby("merchant_category")["amount_gbp"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.barh(totals.index, totals.values, color=BLUE)
    # Value labels remove the need to read values off the axis.
    ax.bar_label(bars, labels=[f"£{v:,.0f}" for v in totals.values], padding=3)
    ax.set_xlim(0, totals.max() * 1.15)  # from 0, with room for the largest label
    ax.xaxis.set_major_formatter(StrMethodFormatter(GBP_TICKS))
    ax.set_title("Electronics and Travel carry most card spend (Feb 2026, GBP)")
    ax.set_xlabel("Total spend (GBP)")
    ax.set_ylabel("Merchant category")
    save(fig, "category_spend.png")
    print(f"  largest category: {totals.index[-1]} £{totals.iloc[-1]:,.2f}")


def plot_amount_distribution():
    """2. The same data on a linear and a log scale, side by side."""
    amounts = txns["amount_gbp"]
    fig, (ax_lin, ax_log) = plt.subplots(1, 2, figsize=(11, 4))

    ax_lin.hist(amounts, bins=30, color=BLUE, edgecolor="white")
    ax_lin.set_title("Linear scale: most payments crowd into the first bar")
    ax_lin.set_xlabel("Amount (GBP)")
    ax_lin.set_ylabel("Number of transactions")

    # Equal-width bins on a log axis need log-spaced edges: np.geomspace gives edges with a
    # constant ratio, so each bar is the same width once the axis is logarithmic.
    log_bins = np.geomspace(amounts.min(), amounts.max(), 25)
    ax_log.hist(amounts, bins=log_bins, color=BLUE, edgecolor="white")
    ax_log.set_xscale("log")
    ax_log.xaxis.set_major_formatter(StrMethodFormatter(GBP_TICKS))
    ax_log.set_title("Log scale: the shape of small and large payments")
    ax_log.set_xlabel("Amount (GBP, log scale)")
    ax_log.set_ylabel("Number of transactions")

    fig.suptitle("Card payment amounts are strongly right-skewed")
    save(fig, "amount_distribution.png")
    first_bin = np.histogram(amounts, bins=30)[0][0]
    print(f"  linear histogram: {first_bin} of {len(amounts)} payments fall in the first bin")


def plot_daily_spend():
    """3. Daily spend with a 7-day rolling mean on the same axes."""
    daily = txns.set_index("txn_timestamp")["amount_gbp"].resample("D").sum()
    rolling = daily.rolling(7).mean()  # the first 6 days are NaN: there is no full week yet
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(daily.index, daily.values, color=BLUE, linewidth=1.5, marker="o", markersize=4,
            label="Daily spend")
    ax.plot(rolling.index, rolling.values, color=ORANGE, linewidth=2.5,
            label="7-day rolling mean")
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(StrMethodFormatter(GBP_TICKS))
    ax.set_title("Daily card spend is volatile; the 7-day mean shows the underlying level")
    ax.set_xlabel("Date (Feb - Mar 2026)")
    ax.set_ylabel("Spend (GBP)")
    ax.legend()
    fig.autofmt_xdate()
    save(fig, "daily_spend.png")
    print(f"  {len(daily)} days; highest day {daily.idxmax():%a %d %b} £{daily.max():,.2f}")
    return daily


def plot_decline_rate():
    """4. Decline rate by channel as a percentage, with the group size in each label."""
    stats = (
        txns.assign(declined=txns["status"] == "DECLINED")
        .groupby("channel")["declined"].agg(rate="mean", n="count", declines="sum")
        .sort_values("rate", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(stats.index, stats["rate"], color=BLUE)
    # The count stops a reader over-interpreting a rate built on very few transactions.
    labels = [f"{r:.1%}\n({d} of {n})" for r, d, n in zip(stats["rate"], stats["declines"], stats["n"])]
    ax.bar_label(bars, labels=labels, padding=3)
    ax.set_ylim(0, 1)  # the full 0-100% scale keeps the rates in proportion
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.set_title("Online payments are declined far more often than card-present ones")
    ax.set_xlabel("Channel")
    ax.set_ylabel("Decline rate")
    save(fig, "decline_rate_by_channel.png")
    for channel, rate, n, declines in stats.itertuples():
        print(f"  {channel}: {rate:.1%} ({declines} of {n})")


def plot_misleading():
    """5. MISLEADING ON PURPOSE: raw amounts in three currencies summed and labelled as GBP.

    Flaw: amount is in the transaction's own currency (GBP, EUR or USD). Summing it by country
    adds euros and dollars as if they were pounds, and the axis label claims GBP. The US bar is
    inflated by about 27% (1 / 0.79) and the euro countries by about 18% (1 / 0.85). Every
    number is computed correctly from the data; the unit on the axis is false.
    """
    wrong = txns.groupby("country")["amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(wrong.index, wrong.values, color=ORANGE)
    ax.set_ylim(bottom=0)
    ax.set_title("Card spend by country (GBP)")
    ax.set_xlabel("Country")
    ax.set_ylabel("Total spend (GBP)")  # false: the values are in mixed currencies
    save(fig, "misleading.png")

    right = txns.groupby("country")["amount_gbp"].sum()
    comparison = pd.DataFrame({"chart_shows": wrong, "true_gbp": right}).round(2)
    comparison["overstated_by"] = comparison["chart_shows"] - comparison["true_gbp"]
    print(comparison.sort_values("chart_shows", ascending=False).to_string())


if __name__ == "__main__":
    plot_category_spend()
    plot_amount_distribution()
    plot_daily_spend()
    plot_decline_rate()
    plot_misleading()
