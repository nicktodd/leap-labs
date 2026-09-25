from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv")
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)

# Spend is measured on APPROVED transactions only: a declined payment moved no money.
approved = txns[txns["status"] == "APPROVED"]
by_customer = approved.groupby("customer_id")["amount_gbp"].sum().sort_values(ascending=False)

pareto = by_customer.to_frame("spend_gbp")
pareto["cum_share_pct"] = (pareto["spend_gbp"].cumsum() / pareto["spend_gbp"].sum() * 100).round(1)
pareto["rank"] = range(1, len(pareto) + 1)
print("Approved GBP spend by customer, largest first, with cumulative share:")
print(pareto.round(2).to_string())

# "Top 20% of customers" has to be a whole number of customers. Round up so that a small
# customer base still gets at least one customer in the top group.
n_customers = len(pareto)
top_n = -(-n_customers * 20 // 100)  # ceiling division
top_share = pareto["cum_share_pct"].iloc[top_n - 1]
print(f"\n{n_customers} customers; top 20% = top {top_n}: {', '.join(pareto.index[:top_n])}")
print(f"share of approved GBP spend from the top {top_n}: {top_share:.1f}%")
