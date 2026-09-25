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

# --- 1. Quantify the damage before changing anything ---
# Measuring first gives a baseline to reconcile against at the end.
print(f"Raw rows: {len(df)}")
print("\nNulls per column (non-zero only):")
nulls = df.isna().sum()
print(nulls[nulls > 0])
print(f"\nDistinct raw channel values ({df['channel'].nunique()}):")
print(df["channel"].map(repr).value_counts())
print(f"\nExact duplicate rows in the raw file: {df.duplicated().sum()}")
# amount was read as str, not float, because some values contain symbols or text.
print(f"amount dtype as read: {df['amount'].dtype}")

# --- 2. Amounts: strip symbols and separators, then convert ---
# Currency symbols and thousands separators are formatting, not data: removing them
# recovers the number, and the currency column already records which currency it is.
cleaned_text = df["amount"].str.replace(r"[£€$,\s]", "", regex=True)
df["amount"] = pd.to_numeric(cleaned_text, errors="coerce")
bad_amount = df["amount"].isna()
print(f"\nRows whose amount could not be parsed: {bad_amount.sum()}")
print(raw.loc[bad_amount, ["txn_id", "merchant", "amount"]])
# A blank or "TBC" amount has no source to recover it from (no quantity * price as in
# the trades data), and inventing a value would corrupt every total -> drop these rows.
df = df[~bad_amount].copy()

# --- 3. Channel: normalise case and whitespace, then map to canonical values ---
# .str.title() would give "In-Store" and cannot join "instore" to "In-store"; an explicit
# mapping states every accepted variant and turns anything unexpected into NaN.
CHANNEL_CANONICAL = {
    "online": "Online",
    "in-store": "In-store",
    "instore": "In-store",
    "in store": "In-store",
    "contactless": "Contactless",
}
df["channel"] = df["channel"].str.strip().str.lower().map(CHANNEL_CANONICAL)
assert df["channel"].notna().all(), "unmapped channel variant found"
assert df["channel"].nunique() == 3, df["channel"].unique()
print(f"\nChannel values after mapping: {sorted(df['channel'].unique())}")

# --- 4. Country: UK -> GB ---
# ISO 3166 codes are what reference data (customers.csv home_country) and payment
# networks use; "UK" would fail to match "GB" in any join or country comparison.
uk_rows = (df["country"] == "UK").sum()
df["country"] = df["country"].replace({"UK": "GB"})
print(f"Replaced UK with GB on {uk_rows} rows; countries now: {sorted(df['country'].unique())}")

# --- 5. Merchant whitespace ---
# " TfL " and "TfL" are the same merchant; untrimmed names split groupbys and lookups.
padded = (df["merchant"] != df["merchant"].str.strip()).sum()
df["merchant"] = df["merchant"].str.strip()
print(f"Stripped whitespace from {padded} merchant names")

# --- 6. Missing merchant_category: recover from the same merchant's other rows ---
# This must run AFTER step 5, otherwise " Amazon" and "Amazon" are different keys.
known = df.dropna(subset=["merchant_category"])
categories_per_merchant = known.groupby("merchant")["merchant_category"].nunique()
# Safe only because each merchant maps to exactly one category; verify it, not assume it.
assert (categories_per_merchant == 1).all(), categories_per_merchant[categories_per_merchant > 1]
merchant_to_category = known.groupby("merchant")["merchant_category"].first()
missing_cat = df["merchant_category"].isna()
df["merchant_category"] = df["merchant_category"].fillna(df["merchant"].map(merchant_to_category))
print(f"\nFilled merchant_category on {missing_cat.sum()} rows:")
print(df.loc[missing_cat, ["txn_id", "merchant", "merchant_category"]])

# --- 7. Timestamps: two explicit formats, invalid dates become NaT ---
# Both formats are unambiguous, so parse each explicitly rather than letting pandas
# guess; a value that matches neither format becomes NaT instead of a guessed date.
iso = pd.to_datetime(df["txn_timestamp"], format="%Y-%m-%d %H:%M", errors="coerce")
dmy = pd.to_datetime(df["txn_timestamp"], format="%d-%b-%Y %H:%M", errors="coerce")
print(f"\nTimestamps in YYYY-MM-DD format: {iso.notna().sum()}, in DD-Mon-YYYY format: {dmy.notna().sum()}")
df["txn_timestamp"] = iso.fillna(dmy)
bad_date = df["txn_timestamp"].isna()
print("Rows with an unparseable timestamp:")
print(raw.loc[df.index[bad_date], ["txn_id", "txn_timestamp", "merchant", "amount"]])
# 2026-02-29 does not exist (2026 is not a leap year). 28 Feb and 1 Mar are both
# plausible, so choosing one would be a guess -> reject the row and query the source.
df = df[~bad_date].copy()

# --- 8. Duplicates: only detectable in full after normalisation ---
# On the raw file only P0095 was an exact duplicate. P0102's second copy differed only
# in formatting (" Amazon", "ONLINE"), so it becomes an exact duplicate now.
print(f"\nExact duplicates now (after normalisation): {df.duplicated().sum()}")
dup_ids = df.loc[df.duplicated(subset=["txn_id"]), "txn_id"].tolist()
print(f"Duplicate txn_ids: {dup_ids}")
# txn_id is the business key: one transaction, one row. Keep the first copy.
df = df.drop_duplicates(subset=["txn_id"], keep="first")

# --- 9. Outlier: flag, do not drop ---
# Compare like with like: convert to GBP (mixing currencies would distort the IQR),
# and use a per-category fence, because a normal Travel spend is not a normal Dining spend.
rates = pd.read_csv(FX_PATH).set_index("currency")["rate_to_gbp"]
amount_gbp = df["amount"] * df["currency"].map(rates)
by_cat = amount_gbp.groupby(df["merchant_category"])
q1 = by_cat.transform(lambda s: s.quantile(0.25))
q3 = by_cat.transform(lambda s: s.quantile(0.75))
iqr_flag = amount_gbp > q3 + 1.5 * (q3 - q1)
# Business rule: the UK contactless limit is GBP 100, so a larger contactless payment
# in GB cannot have been authorised as contactless.
limit_flag = (df["channel"] == "Contactless") & (df["country"] == "GB") & (amount_gbp > 100)
review = df.assign(amount_gbp=amount_gbp.round(2), iqr_flag=iqr_flag, contactless_limit=limit_flag)
review = review[iqr_flag | limit_flag]
print(f"\nRows flagged by the per-category IQR rule: {iqr_flag.sum()}; "
      f"by the contactless-limit rule: {limit_flag.sum()}; by both: {(iqr_flag & limit_flag).sum()}")
print(review[["txn_id", "merchant", "merchant_category", "channel", "amount_gbp",
              "iqr_flag", "contactless_limit"]].to_string(index=False))
# The IQR rule alone produces candidates, not verdicts: Dishoom meals sit in a Dining
# category dominated by coffee, and Trainline fares in a Transport category dominated
# by TfL, so they are statistically unusual but commercially normal. Only P0141 breaks
# both the statistical rule and the business rule.
# Investigation note: P0141 (Pret A Manger, 1,850.00 GBP contactless) is most likely 18.50
# keyed without the decimal point; confirm the authorised amount with the acquirer's
# settlement record for that transaction before correcting it.

# --- Acceptance checks ---
assert len(df) == 138, len(df)
assert set(df["channel"]) == {"Online", "In-store", "Contactless"}
assert not (df["country"] == "UK").any()
assert df["amount"].dtype == "float64"
assert pd.api.types.is_datetime64_any_dtype(df["txn_timestamp"])
assert df["merchant_category"].isna().sum() == 0
assert "P0141" in set(df["txn_id"])

print(f"\nFinal clean rows: {len(df)} (raw {len(raw)} - 2 bad amounts - 1 invalid date - 2 duplicates)")
print(df.dtypes)
df.to_csv(OUT / "clean_transactions.csv", index=False)
print(f"\nWrote {OUT / 'clean_transactions.csv'}")
