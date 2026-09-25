from pathlib import Path

import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"
RAW_PATH = SHARED / "messy-transactions-raw.csv"
FX_PATH = SHARED / "fx_rates.csv"

CHANNEL_CANONICAL = {
    "online": "Online",
    "in-store": "In-store",
    "instore": "In-store",
    "in store": "In-store",
    "contactless": "Contactless",
}


# Each step takes a DataFrame and returns a new one, so steps can be chained with .pipe(),
# tested one at a time, and reordered deliberately. .assign() returns a copy, so the
# input DataFrame is never modified in place.

def parse_amount(df):
    # Symbols and separators are formatting; blank and "TBC" become NaN for a later decision.
    text = df["amount"].str.replace(r"[£€$,\s]", "", regex=True)
    return df.assign(amount=pd.to_numeric(text, errors="coerce"))


def drop_bad_amounts(df):
    # No source exists to reconstruct a missing amount, so these rows cannot be kept.
    return df[df["amount"].notna()]


def normalise_channel(df):
    # Explicit mapping of every accepted variant; anything else becomes NaN and fails the check.
    channel = df["channel"].str.strip().str.lower().map(CHANNEL_CANONICAL)
    assert channel.notna().all(), "unmapped channel variant found"
    return df.assign(channel=channel)


def fix_country(df):
    # ISO 3166 code GB, to match reference data in joins.
    return df.assign(country=df["country"].replace({"UK": "GB"}))


def strip_merchant(df):
    # Padded names would split groupbys and break the category lookup below.
    return df.assign(merchant=df["merchant"].str.strip())


def fill_category(df):
    # Safe because each merchant has exactly one category elsewhere in the file (checked).
    known = df.dropna(subset=["merchant_category"])
    assert (known.groupby("merchant")["merchant_category"].nunique() == 1).all()
    lookup = known.groupby("merchant")["merchant_category"].first()
    return df.assign(merchant_category=df["merchant_category"].fillna(df["merchant"].map(lookup)))


def parse_timestamp(df):
    # Two explicit formats; anything else (2026-02-29) becomes NaT rather than a guess.
    iso = pd.to_datetime(df["txn_timestamp"], format="%Y-%m-%d %H:%M", errors="coerce")
    dmy = pd.to_datetime(df["txn_timestamp"], format="%d-%b-%Y %H:%M", errors="coerce")
    return df.assign(txn_timestamp=iso.fillna(dmy))


def drop_bad_dates(df):
    # An impossible date cannot be corrected without guessing: reject it.
    return df[df["txn_timestamp"].notna()]


def dedupe(df):
    # Runs after normalisation, so formatting-only copies (P0102) are caught too.
    return df.drop_duplicates(subset=["txn_id"], keep="first")


def flag_outliers(df):
    # Flag, never drop: per-category IQR fence in GBP, plus the GBP 100 UK contactless limit.
    rates = pd.read_csv(FX_PATH).set_index("currency")["rate_to_gbp"]
    gbp = df["amount"] * df["currency"].map(rates)
    grouped = gbp.groupby(df["merchant_category"])
    q1 = grouped.transform(lambda s: s.quantile(0.25))
    q3 = grouped.transform(lambda s: s.quantile(0.75))
    iqr_flag = gbp > q3 + 1.5 * (q3 - q1)
    limit_flag = (df["channel"] == "Contactless") & (df["country"] == "GB") & (gbp > 100)
    return df.assign(needs_review=iqr_flag & limit_flag)


def normalise(raw):
    """Every fix that changes values but removes no rows."""
    return (
        raw.pipe(parse_amount)
        .pipe(normalise_channel)
        .pipe(fix_country)
        .pipe(strip_merchant)
        .pipe(fill_category)
        .pipe(parse_timestamp)
    )


def clean(raw):
    """The full pipeline: normalise, then reject, then deduplicate, then flag."""
    return (
        raw.pipe(normalise)
        .pipe(drop_bad_amounts)
        .pipe(drop_bad_dates)
        .pipe(dedupe)
        .pipe(flag_outliers)
    )


if __name__ == "__main__":
    raw = pd.read_csv(RAW_PATH)
    clean_df = clean(raw)
    print(f"Raw rows: {len(raw)}, clean rows: {len(clean_df)}")
    print(f"Channels: {sorted(clean_df['channel'].unique())}")
    print(f"Rows needing review: {clean_df.loc[clean_df['needs_review'], 'txn_id'].tolist()}")

    # The order matters: deduplicating before normalising misses P0102.
    wrong_order = raw.drop_duplicates().pipe(normalise).pipe(drop_bad_amounts).pipe(drop_bad_dates)
    print(f"If exact-duplicate removal runs first, on raw data: {len(wrong_order)} rows "
          f"(txn_id P0102 appears {int((wrong_order['txn_id'] == 'P0102').sum())} times)")
    assert len(clean_df) == 138
