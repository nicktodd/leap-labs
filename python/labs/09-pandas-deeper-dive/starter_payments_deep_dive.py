from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
customers = pd.read_csv(SHARED / "customers.csv")
fx = pd.read_csv(SHARED / "fx_rates.csv")

print(f"transactions: {len(txns)} rows, customers: {len(customers)} rows, fx rates: {len(fx)} rows")

# TODO 1 - FX merge
# - Merge fx onto txns on "currency" with validate="many_to_one", then add
#   amount_gbp = amount * rate_to_gbp (rounded to 2 decimal places).
# - Check the row count is unchanged and no rate is missing.
# - Comment: what does validate="many_to_one" protect against?

# TODO 2 - Customer merge
# - Merge customers with how="left" and indicator=True (drop customers' customer_name first,
#   since txns already has one).
# - Print the _merge counts, and the orphan rows (left_only): which customer, how many rows,
#   how much GBP?
# - Compare the row count of an inner join with the left join.
# - Fill the missing segment with "Unknown".
# - Comment: which join do you keep for the summary, and why?

# TODO 3 - Named aggregation per segment (all transactions, including declined)
# - One groupby("segment").agg(...) call producing: txn_count, customers (nunique),
#   total_gbp, avg_gbp, decline_rate (mean of a boolean column), fraud_count.

# From here on, "spend" means APPROVED transactions only: a declined payment moves no money.

# TODO 4 - pivot_table
# - rows merchant_category, columns channel, values amount_gbp, aggfunc "sum", fill_value=0,
#   margins=True (margins_name="Total").
# - Check the bottom-right margin equals the total approved spend.

# TODO 5 - Time series
# - Daily spend: set_index("txn_timestamp") and resample("D").sum(). How many days are there,
#   and how many have zero spend?
# - A 7-day rolling mean of the daily spend.
# - Weekly totals with resample("W-SUN"): spend and transaction count.
# - Compare transactions per day before and from payday (Fri 27 Feb 2026).

# TODO 6 - Takeaways (with your partner)
# 3-5 one-line takeaways as comments, each citing a specific number from your output.
