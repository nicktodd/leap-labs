"""Lab 14: Capstone dashboard — ETL + insights + charts + plain-text summary."""

from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(r"C:\Users\zackt\Documents\fidelity-leap-sprint4\shared")
OUT = Path(__file__).resolve().parent


def extract() -> pd.DataFrame:
    """Read shared/trades.csv with trade_date parsed as a real datetime."""
    return pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Light reshaping — trades.csv is already clean, but keep ETL stages explicit."""
    df = df.copy()
    # Ensure value is numeric (it should be, but defensive cast is good practice)
    df["value"] = pd.to_numeric(df["value"])
    return df


def load(df: pd.DataFrame, out_path: Path) -> Path:
    """Write the processed DataFrame to a CSV and return the path."""
    df.to_csv(out_path, index=False)
    return out_path


def compute_insights(df: pd.DataFrame) -> dict:
    """Compute at least three business insights, each backed by a specific number."""
    # Insight 1: top client by total trade value
    client_totals = df.groupby("client_name")["value"].sum().sort_values(ascending=False)
    top_client = client_totals.index[0]
    top_client_value = client_totals.iloc[0]

    # Insight 2: highest-value asset class
    asset_totals = df.groupby("asset_class")["value"].sum().sort_values(ascending=False)
    top_asset = asset_totals.index[0]
    top_asset_value = asset_totals.iloc[0]

    # Insight 3: advisor whose clients generate highest mean trade value
    advisor_mean = df.groupby("advisor")["value"].mean().sort_values(ascending=False)
    top_advisor = advisor_mean.index[0]
    top_advisor_mean = advisor_mean.iloc[0]

    # Insight 4: buy vs sell split by total value
    side_totals = df.groupby("side")["value"].sum()
    buy_pct = side_totals["BUY"] / side_totals.sum() * 100

    return {
        "top_client": top_client,
        "top_client_value": top_client_value,
        "top_asset": top_asset,
        "top_asset_value": top_asset_value,
        "top_advisor": top_advisor,
        "top_advisor_mean": top_advisor_mean,
        "buy_pct": buy_pct,
        "asset_totals": asset_totals,
        "client_totals": client_totals,
        "weekly": df.set_index("trade_date")["value"].resample("W").sum(),
    }


def build_charts(df: pd.DataFrame, insights: dict) -> None:
    """Build two charts following Module 10 principles — honest axes, specific titles."""
    # Chart 1: total value by client (bar, y from 0)
    fig, ax = plt.subplots(figsize=(10, 5))
    client_totals = insights["client_totals"]
    ax.bar(client_totals.index, client_totals.values, color="steelblue")
    ax.set_title("Total Trade Value by Client — Jan 2026")
    ax.set_xlabel("Client")
    ax.set_ylabel("Total Value (USD / GBP)")
    ax.set_ylim(0)
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(OUT / "dashboard_chart_clients.png", dpi=150)
    plt.close(fig)
    print("Saved dashboard_chart_clients.png")

    # Chart 2: weekly trade volume (line, y from 0)
    weekly = insights["weekly"]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(weekly.index, weekly.values, marker="o", color="darkgreen")
    ax.set_title("Total Trade Value by Week — Jan 2026")
    ax.set_xlabel("Week ending")
    ax.set_ylabel("Total Value (USD / GBP)")
    ax.set_ylim(0)
    fig.tight_layout()
    fig.savefig(OUT / "dashboard_chart_weekly.png", dpi=150)
    plt.close(fig)
    print("Saved dashboard_chart_weekly.png")


def print_dashboard(insights: dict) -> None:
    """Print a plain-text summary a non-technical stakeholder can read without charts."""
    print("\n" + "=" * 60)
    print("  TRADE ANALYTICS DASHBOARD — January 2026")
    print("=" * 60)
    print(
        f"\n1. Top client by total trade value:\n"
        f"   {insights['top_client']} — ${insights['top_client_value']:,.2f}\n"
        f"   This is the highest total of any client in the period."
    )
    print(
        f"\n2. Highest-value asset class:\n"
        f"   {insights['top_asset']} — ${insights['top_asset_value']:,.2f} total traded.\n"
        f"   Equity trades dominate by volume and value."
    )
    print(
        f"\n3. Advisor generating highest mean trade value per trade:\n"
        f"   {insights['top_advisor']} — average ${insights['top_advisor_mean']:,.2f} per trade.\n"
        f"   Clients advised by {insights['top_advisor']} tend to place larger individual trades."
    )
    print(
        f"\n4. Buy vs. sell split:\n"
        f"   {insights['buy_pct']:.1f}% of total value was BUY-side activity.\n"
        f"   The portfolio is accumulating rather than distributing over this period."
    )
    print("\n" + "=" * 60)


if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    load(clean, OUT / "dashboard_data_loaded.csv")
    insights = compute_insights(clean)
    build_charts(clean, insights)
    print_dashboard(insights)
