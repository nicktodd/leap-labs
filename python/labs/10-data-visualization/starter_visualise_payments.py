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

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)


def save(fig, name):
    """Save a figure into output/ and close it. Call this at the end of every plot function."""
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=120)
    plt.close(fig)
    print(f"saved output/{name}")


def plot_category_spend():
    # TODO 1 - Horizontal bar chart of total amount_gbp by merchant_category -> category_spend.png
    # - Sort so the largest bar is at the top (barh draws the first row at the bottom).
    # - Value labels on the bars with ax.bar_label(bars, labels=[...]).
    # - x-axis starts at 0; leave room on the right for the largest label.
    # - A title that states the finding, and labelled axes with units.
    raise NotImplementedError


def plot_amount_distribution():
    # TODO 2 - One figure, two histograms side by side (plt.subplots(1, 2)) -> amount_distribution.png
    # - Left: amount_gbp with ordinary bins on a linear x-axis.
    # - Right: the same data with log-spaced bins (np.geomspace) and ax.set_xscale("log").
    # - Each panel's title says what that panel shows.
    raise NotImplementedError


def plot_daily_spend():
    # TODO 3 - Line chart of daily spend -> daily_spend.png
    # - Daily totals with resample("D") on txn_timestamp.
    # - A 7-day rolling mean (.rolling(7).mean()) on the same axes.
    # - A legend, y-axis from 0, labelled axes, readable dates (fig.autofmt_xdate()).
    raise NotImplementedError


def plot_decline_rate():
    # TODO 4 - Bar chart of decline rate by channel -> decline_rate_by_channel.png
    # - y-axis from 0% to 100% (ax.set_ylim(0, 1) with PercentFormatter(xmax=1)).
    # - Each bar label shows the rate and the counts, e.g. "15.5%\n(11 of 71)".
    raise NotImplementedError


def plot_misleading():
    # TODO 5 - A deliberately misleading chart -> misleading.png
    # - Not a truncated axis (the demo covered that). See the README for options.
    # - A comment (or docstring) naming the specific flaw, and print the numbers that show it.
    raise NotImplementedError


if __name__ == "__main__":
    plot_category_spend()
    plot_amount_distribution()
    plot_daily_spend()
    plot_decline_rate()
    plot_misleading()
