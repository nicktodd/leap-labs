from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
fx = pd.read_csv(SHARED / "fx_rates.csv")

print(f"Loaded {len(txns)} transactions")

# TODO 1 - Derived columns
# - Merge fx onto txns by currency and add amount_gbp = amount * rate_to_gbp (2 decimal places).
# - Add hour (0-23) and weekday (e.g. "Monday") from txn_timestamp using the .dt accessor.

# TODO 2 - Distribution of amount_gbp
# - Print amount_gbp.describe(percentiles=[0.5, 0.9, 0.99]).
# - Comment: compare the mean with the median (the 50% row). What does the gap tell you,
#   and which one would you report as the "typical payment"?

# TODO 3 - Spend by merchant category
# - One table with txn_count, total_gbp and share_pct (share of total GBP spend, %) per
#   merchant_category, sorted by total_gbp descending.
# - Comment: which categories are frequent, and which carry the money?

# TODO 4 - Decline rate by channel
# - Add a boolean column declined (status == "DECLINED").
# - Decline rate per channel with groupby("channel")["declined"].mean() (also show count and sum).
# - The same view with pd.crosstab(channel, status, normalize="index").

# TODO 5 - Hour bands
# - Use pd.cut on hour to make hour_band: Night 00-05, Morning 06-11, Afternoon 12-17,
#   Evening 18-23. Check your bin edges: pd.cut bins include the right edge by default.
# - Per band: transaction count, decline rate and fraud rate (is_fraud).

# TODO 6 - The currency anomaly
# - Print amount.sum() and amount_gbp.sum() and the difference.
# - Break the difference down by currency. Which rows cause it?

# TODO 7 - Findings (comments, one sentence each, with numbers from your output)
# Pattern:
# Anomaly:
# Hypothesis (checkable, and name the Module 8 test that would check it):
