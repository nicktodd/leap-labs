import string
from pathlib import Path

import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

df = pd.read_csv(SHARED / "transactions.csv")

# Case-insensitive search across two patterns with a regular expression alternation.
# case=False avoids lower-casing the column first; the result is a boolean mask.
coffee_mask = df["merchant"].str.contains("coffee|pret", case=False, regex=True)
coffee = df[coffee_mask]
print(f"Coffee-shop transactions (Costa Coffee or Pret A Manger): {len(coffee)}")
print(coffee["merchant"].value_counts())

# .str.title() capitalises the first letter after ANY non-letter, including an
# apostrophe, and lower-cases everything else. That damages several merchant names.
merchants = pd.Series(sorted(df["merchant"].unique()))
titled = merchants.str.title()
changed = pd.DataFrame({"original": merchants, "str.title()": titled})[merchants != titled]
print("\nMerchant names that .str.title() changes:")
print(changed.to_string(index=False))

# string.capwords splits on whitespace only, so the apostrophe is safe, but it still
# lower-cases acronyms (ASOS -> Asos, TfL -> Tfl). Clean data should be left alone;
# if casing must be normalised, use an explicit mapping of canonical names.
print("\nstring.capwords on the same names:")
print(pd.DataFrame({"original": merchants, "capwords": merchants.map(string.capwords)})
      [merchants != merchants.map(string.capwords)].to_string(index=False))
