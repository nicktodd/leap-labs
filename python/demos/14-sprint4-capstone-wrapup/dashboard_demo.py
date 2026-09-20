"""A small end-to-end dashboard, pulling together every module of Sprint 4:
Module 12's ETL structure, Module 6's cleaning, Module 7/9's analysis patterns,
and Module 10's honest charting principles.

Data-access note for a non-technical stakeholder: this dashboard reads from a local
file (extract()), not a live API. For a book this size (twenty trades, refreshed once
a day), a daily file is simpler and more reliable than querying an API on every run --
an API only earns its complexity when data changes intraday or only a filtered subset
is needed. If the source ever changes to a live feed, only extract() needs to change;
transform(), load(), and everything downstream stay the same.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent


def extract():
    return pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])


def transform(df):
    # This dataset is already clean (Module 6's messy twin is what needed real cleaning);
    # transform() still exists as its own stage so a future dirtier source slots in here.
    return df


def load(df, out_path):
    df.to_csv(out_path, index=False)
    return out_path


def compute_insights(df):
    asset_share = (df.groupby("asset_class")["value"].sum() / df["value"].sum() * 100).round(1)
    top_asset_class = asset_share.idxmax()

    mean_by_advisor = df.groupby("advisor")["value"].mean().round(2)
    top_advisor = mean_by_advisor.idxmax()
    bottom_advisor = mean_by_advisor.idxmin()
    ratio = round(mean_by_advisor[top_advisor] / mean_by_advisor[bottom_advisor], 1)

    weekly = df.set_index("trade_date")["value"].resample("W").sum()

    return {
        "asset_share": asset_share,
        "top_asset_class": top_asset_class,
        "mean_by_advisor": mean_by_advisor,
        "top_advisor": top_advisor,
        "bottom_advisor": bottom_advisor,
        "advisor_ratio": ratio,
        "weekly": weekly,
    }


def build_charts(df, insights):
    totals = df.groupby("asset_class")["value"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(totals.index, totals.values, color="#1E6FA8")
    ax.set_title("Total Trade Value by Asset Class ($)")
    ax.set_ylabel("Total Value ($)")
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    fig.savefig(OUT / "dashboard_asset_class.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(insights["weekly"].index, insights["weekly"].values, marker="o", color="#1E6FA8")
    ax.set_title("Total Trade Value by Week ($)")
    ax.set_ylabel("Total Value ($)")
    ax.set_xticks(insights["weekly"].index)
    ax.set_xticklabels([d.strftime("%Y-%m-%d") for d in insights["weekly"].index])
    fig.tight_layout()
    fig.savefig(OUT / "dashboard_weekly_trend.png")
    plt.close(fig)


def print_dashboard(insights):
    print("=== Mission Dataset: Weekly Analytics Dashboard ===\n")
    print(f"1. {insights['top_asset_class']} accounts for "
          f"{insights['asset_share'][insights['top_asset_class']]}% of total trade value.")
    print(f"2. {insights['top_advisor']}'s average trade "
          f"(${insights['mean_by_advisor'][insights['top_advisor']]:,.2f}) is "
          f"{insights['advisor_ratio']}x {insights['bottom_advisor']}'s "
          f"(${insights['mean_by_advisor'][insights['bottom_advisor']]:,.2f}).")
    week1, week2 = insights["weekly"].iloc[0], insights["weekly"].iloc[1]
    print(f"3. Week 1 trading value (${week1:,.2f}) outpaced week 2 (${week2:,.2f}).")
    print("\nCharts saved: dashboard_asset_class.png, dashboard_weekly_trend.png")


if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    load(clean, OUT / "dashboard_data_loaded.csv")
    insights = compute_insights(clean)
    build_charts(clean, insights)
    print_dashboard(insights)
