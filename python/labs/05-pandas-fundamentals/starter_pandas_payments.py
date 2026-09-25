from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SHARED = ROOT / "shared"
TXN_PATH = SHARED / "transactions.csv"
FX_PATH = SHARED / "fx_rates.csv"
# Your Module 3 output, if you have it (optional: step 7 must work without it).
MODULE3_SUMMARY = ROOT / "labs" / "03-data-structures-file-io" / "output" / "customer_summary.csv"

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

# TODO 1: read TXN_PATH with parse_dates=["txn_timestamp"]. Print the shape, the dtypes,
#         and call .info(). Check that txn_timestamp is a datetime dtype, not str.

# TODO 2: positional selection with .iloc:
#         - rows at positions 10 to 14 inclusive
#         - the last 3 rows
#         - the first 5 rows and the first 4 columns, in one .iloc call

# TODO 3: label selection with .loc:
#         - by_id = df.set_index("txn_id")
#         - the single transaction "P0042"
#         - the label range "P0010" to "P0015", columns merchant and amount.
#           Print how many rows it returns and comment on why.

# TODO 4: boolean filters:
#         - declined Online transactions (two conditions combined with &)
#         - non-GBP transactions, using .isin()
#         - the declined Online filter again, written with .query(); confirm it matches

# TODO 5: read FX_PATH, turn it into a Series indexed by currency, and add an amount_gbp
#         column using .map() on df["currency"]. No loops.

# TODO 6: the 5 largest transactions by amount_gbp (nlargest), then sort the whole
#         DataFrame by customer_id ascending and amount_gbp descending.

# TODO 7: per-customer summary with groupby + agg:
#         txn_count (all rows) and total_gbp (APPROVED rows only), one row per customer.
#         Compare it with the Module 3 plain-Python numbers: implement module3_summary()
#         below, and compare money with a tolerance, not ==.


def module3_summary():
    """Return {customer_id: (txn_count, total_gbp)} using csv.DictReader and dicts only."""
    raise NotImplementedError


# TODO 8: write a comment block mapping each pandas operation you used to the
#         Module 3 loop it replaces.
