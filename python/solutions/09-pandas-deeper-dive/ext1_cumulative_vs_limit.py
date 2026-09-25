from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
customers = pd.read_csv(SHARED / "customers.csv")
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)

# Only approved payments use up the credit limit. An inner join is deliberate here: K012 has no
# credit_limit_gbp, so there is nothing to compare against.
spend = (txns[txns["status"] == "APPROVED"]
         .merge(customers[["customer_id", "credit_limit_gbp"]], on="customer_id", how="inner",
                validate="many_to_one")
         .sort_values(["customer_id", "txn_timestamp"]))  # cumsum must run in time order

spend["cum_gbp"] = spend.groupby("customer_id")["amount_gbp"].cumsum()
spend["pct_of_limit"] = spend["cum_gbp"] / spend["credit_limit_gbp"]

month_end = spend.groupby("customer_id").agg(
    credit_limit_gbp=("credit_limit_gbp", "first"),
    month_spend_gbp=("cum_gbp", "last"),
    pct_of_limit=("pct_of_limit", "last"),
)
print("Approved spend against credit limit at month end:")
print(month_end.sort_values("pct_of_limit", ascending=False)
      .round({"month_spend_gbp": 2, "pct_of_limit": 3}))

# After inspecting the month-end table: most customers use under 20% of their limit in a month,
# so 25% separates the few heavy users from the rest.
THRESHOLD = 0.25
crossed = spend[spend["pct_of_limit"] >= THRESHOLD]
first_cross = crossed.groupby("customer_id").head(1)  # first row per customer, in time order
print(f"\nFirst transaction where cumulative approved spend reaches {THRESHOLD:.0%} of the limit:")
print(first_cross[["customer_id", "txn_id", "txn_timestamp", "merchant", "amount_gbp",
                   "cum_gbp", "credit_limit_gbp", "pct_of_limit", "is_fraud"]]
      .round({"pct_of_limit": 3}).to_string(index=False))

# Share of each crossing customer's month that is approved fraud.
fraud_spend = spend[spend["is_fraud"] == 1].groupby("customer_id")["amount_gbp"].sum()
for cid in first_cross["customer_id"]:
    fraud_gbp = fraud_spend.get(cid, 0.0)
    clean = month_end.loc[cid, "month_spend_gbp"] - fraud_gbp
    print(f"{cid}: approved fraud {fraud_gbp:,.2f} GBP; without it the month ends at "
          f"{clean / month_end.loc[cid, 'credit_limit_gbp']:.1%} of the limit")
# Three customers cross 25%, all with low limits (1,500 to 3,000 GBP). K002 and K009 get there
# with their own spending. K011's crossing payment (P0098, 418.67, British Airways) is genuine,
# but its running total already contains the 412.54 ASOS fraud from 14 Feb (P0054); without
# its two approved fraud payments K011 would end the month at 22.4%, below the threshold.
# Approved fraud consumes genuine credit, which is one reason to monitor limit usage.
