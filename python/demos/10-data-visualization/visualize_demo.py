from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # no display in this environment; write PNGs instead
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent
trades = pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])


def plot_asset_class_totals():
    totals = trades.groupby("asset_class")["value"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(totals.index, totals.values, color="#1E6FA8")
    ax.set_title("Total Trade Value by Asset Class ($)")
    ax.set_xlabel("Asset Class")
    ax.set_ylabel("Total Value ($)")
    ax.set_ylim(bottom=0)  # a bar chart's length must start at zero, or it lies
    fig.tight_layout()
    fig.savefig(OUT / "asset_class_totals.png")
    plt.close(fig)


def plot_weekly_trend():
    by_week = trades.set_index("trade_date")["value"].resample("W").sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(by_week.index, by_week.values, marker="o", color="#1E6FA8")
    ax.set_title("Total Trade Value by Week ($)")
    ax.set_xlabel("Week Ending")
    ax.set_ylabel("Total Value ($)")
    ax.set_xticks(by_week.index)
    ax.set_xticklabels([d.strftime("%Y-%m-%d") for d in by_week.index])
    fig.tight_layout()
    fig.savefig(OUT / "weekly_trend.png")
    plt.close(fig)


def plot_advisor_totals_misleading():
    totals = trades.groupby("advisor")["value"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(totals.index, totals.values, color="#C0392B")
    ax.set_title("Total Trade Value by Advisor ($) -- MISLEADING")
    ax.set_ylabel("Total Value ($)")
    ax.set_ylim(bottom=13000)  # truncated axis, just below the smallest bar: exaggerates the visual difference
    fig.tight_layout()
    fig.savefig(OUT / "advisor_totals_misleading.png")
    plt.close(fig)
    print("Misleading chart: J. Okafor's bar looks ~10x R. Alvarez's.")
    print(f"Actual values: {dict(totals.round(2))}")


def plot_advisor_totals_honest():
    totals = trades.groupby("advisor")["value"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(totals.index, totals.values, color="#1E6FA8")
    ax.set_title("Total Trade Value by Advisor ($)")
    ax.set_ylabel("Total Value ($)")
    ax.set_ylim(bottom=0)  # honest: length is genuinely proportional to value
    fig.tight_layout()
    fig.savefig(OUT / "advisor_totals_honest.png")
    plt.close(fig)


if __name__ == "__main__":
    plot_asset_class_totals()
    plot_weekly_trend()
    plot_advisor_totals_misleading()
    plot_advisor_totals_honest()
    print("Saved 4 charts to this folder (not committed to git).")
