from pathlib import Path

import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"
RAW_PATH = SHARED / "messy-transactions-raw.csv"
FX_PATH = SHARED / "fx_rates.csv"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

raw = pd.read_csv(RAW_PATH)
df = raw.copy()

# Every fix below needs code AND a one-line comment explaining WHY this fix is right for
# this problem. The reasoning is graded. Decide the order of the steps yourself: the
# README explains why the order matters.

# TODO 1: quantify - nulls per column, distinct raw channel values (use repr() to see
#         whitespace), and the number of exact duplicate rows. Note the dtype of amount.

# TODO 2: amounts - remove currency symbols and thousands separators with
#         .str.replace(regex=True), convert with pd.to_numeric(errors="coerce"), count the
#         rows that became NaN, print them, and drop them (comment: why not fill them?).

# TODO 3: channel - strip + lower, then map every variant to Online / In-store / Contactless.
#         Assert there are exactly 3 distinct values and no NaN.

# TODO 4: country - replace "UK" with "GB" (comment: why do ISO codes matter for joins?).

# TODO 5: merchant - strip leading/trailing whitespace.

# TODO 6: merchant_category - build a merchant -> category lookup from the non-null rows,
#         verify each merchant has exactly one category, then fill the gaps with map + fillna.

# TODO 7: txn_timestamp - parse "%Y-%m-%d %H:%M" and "%d-%b-%Y %H:%M" explicitly with
#         errors="coerce", combine them, print the row(s) that match neither, and reject them.

# TODO 8: duplicates - compare df.duplicated().sum() now with the raw count from step 1.
#         Remove duplicates on the business key txn_id.

# TODO 9: outliers - flag (do not drop) suspicious amounts: an IQR rule within
#         merchant_category on GBP amounts, and the GBP 100 UK contactless limit.
#         Print the flagged rows and write a one-sentence investigation note.

print(f"Final row count: {len(df)}")
