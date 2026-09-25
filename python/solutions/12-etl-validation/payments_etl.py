"""Module 12 lab solution: an extract-transform-load pipeline for the raw card transactions.

Run:        python payments_etl.py
Test:       cd solutions/12-etl-validation && python -m pytest -v
"""
from pathlib import Path

import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"
RAW_PATH = SHARED / "messy-transactions-raw.csv"
FX_PATH = SHARED / "fx_rates.csv"
OUT = Path(__file__).resolve().parent / "output"

CHANNEL_CANONICAL = {"online": "Online", "instore": "In-store", "contactless": "Contactless"}
TIMESTAMP_FORMATS = ["%Y-%m-%d %H:%M", "%d-%b-%Y %H:%M"]
CONTACTLESS_LIMIT_GBP = 100
TEXT_COLUMNS = ["txn_id", "customer_id", "customer_name", "merchant", "merchant_category",
                "channel", "country", "currency", "status"]


# --- Extract -------------------------------------------------------------------------------

def extract(path=RAW_PATH):
    """Read the raw file exactly as it is: every column as a string, blanks kept as "".

    Extract should not interpret types. With default settings pandas would silently turn
    "" into NaN and guess a dtype per column, so a value like "TBC" or "£1,249.00" would
    either force the whole column to text or be lost before any rule has looked at it.
    Keeping the raw strings means every conversion happens in transform, where it is
    tested, and every rejected row can be written out as it originally arrived.
    """
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def read_fx(path=FX_PATH):
    return pd.read_csv(path)


# --- Transform: small, individually testable steps ----------------------------------------

def clean_amount(series):
    """'£1,249.00' -> 1249.0. Anything that is still not a number afterwards -> NaN."""
    stripped = series.str.strip().str.replace(r"[£$€,]", "", regex=True)
    return pd.to_numeric(stripped, errors="coerce")


def normalise_channel(series):
    """Map spelling variants ('ONLINE', ' Contactless', 'instore', 'In Store') to the three
    canonical values. Case, surrounding spaces, inner spaces and hyphens are ignored.
    An unrecognised channel becomes NaN rather than being guessed."""
    key = series.str.strip().str.lower().str.replace(r"[\s\-]", "", regex=True)
    return key.map(CHANNEL_CANONICAL)


def normalise_country(series):
    """ISO 3166 codes: upper case, and 'UK' is not an ISO code (Great Britain is 'GB')."""
    return series.str.strip().str.upper().replace({"UK": "GB"})


def parse_timestamps(series):
    """Parse the two formats in the file. Each format is tried explicitly, so nothing is
    guessed; a value that matches neither (including the impossible 2026-02-29) -> NaT."""
    result = pd.to_datetime(series, format=TIMESTAMP_FORMATS[0], errors="coerce")
    for fmt in TIMESTAMP_FORMATS[1:]:
        result = result.fillna(pd.to_datetime(series, format=fmt, errors="coerce"))
    return result


def fill_categories(df):
    """Fill a blank merchant_category from the category the same merchant has elsewhere.
    Must run after merchant names are stripped, or ' Tesco ' will not match 'Tesco'."""
    df = df.copy()
    known = df[df["merchant_category"] != ""]
    category_by_merchant = known.groupby("merchant")["merchant_category"].agg(lambda s: s.mode().iloc[0])
    blank = df["merchant_category"] == ""
    df.loc[blank, "merchant_category"] = df.loc[blank, "merchant"].map(category_by_merchant)
    return df


def add_amount_gbp(df, fx):
    """amount_gbp = amount * rate_to_gbp, rounded to pence. Unknown currency -> NaN."""
    df = df.copy()
    rates = df["currency"].map(fx.set_index("currency")["rate_to_gbp"])
    df["amount_gbp"] = (df["amount"] * rates).round(2)
    return df


def transform(raw, fx):
    """Return (clean, rejects). Rejected rows keep their raw values plus a reject_reason."""
    df = raw.copy()
    reject_index, reject_reason = [], []

    def reject(mask, reason):
        nonlocal df
        reject_index.extend(df.index[mask])
        reject_reason.extend([reason] * int(mask.sum()))
        df = df[~mask]

    # 1. Normalise text first. P0102's second copy differs only by ' Amazon' and 'ONLINE',
    #    so it is only recognisable as a duplicate after this step: order matters.
    for col in TEXT_COLUMNS:
        df[col] = df[col].str.strip()
    df["channel"] = normalise_channel(df["channel"])
    df["country"] = normalise_country(df["country"])

    # 2. Duplicates: whole-row duplicates after normalisation (P0095, P0102). Rows that
    #    shared a txn_id but differed in content would survive here and be caught by the
    #    txn_id uniqueness test, which is the right outcome: they need a human decision.
    reject(df.duplicated(keep="first"), "duplicate")

    # 3. Amounts: symbols and separators are recoverable; blank and 'TBC' are not.
    df["amount"] = clean_amount(df["amount"])
    reject(df["amount"].isna(), "bad amount")

    # 4. Timestamps: two valid formats; 2026-02-29 does not exist, so reject, do not guess.
    df["txn_timestamp"] = parse_timestamps(df["txn_timestamp"])
    reject(df["txn_timestamp"].isna(), "invalid timestamp")

    # 5. Recoverable gaps and derived columns.
    df = fill_categories(df)
    df["distance_from_home_km"] = df["distance_from_home_km"].astype(float)
    df["is_fraud"] = df["is_fraud"].astype(int)
    df = add_amount_gbp(df, fx)

    # 6. Flag, do not delete: a contactless payment above the UK contactless limit is
    #    implausible (P0141, Pret A Manger 1850.00 is most likely 18.50 mis-keyed).
    df["needs_review"] = (df["channel"] == "Contactless") & (df["amount_gbp"] > CONTACTLESS_LIMIT_GBP)

    clean = df.reset_index(drop=True)
    rejects = raw.loc[reject_index].assign(reject_reason=reject_reason).reset_index(drop=True)
    return clean, rejects


# --- Load ----------------------------------------------------------------------------------

def load(clean, rejects, out_dir=OUT):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    clean_path = out_dir / "clean_transactions.csv"
    rejects_path = out_dir / "rejected_transactions.csv"
    # Same timestamp format as shared/transactions.csv, so downstream readers see one format.
    clean.to_csv(clean_path, index=False, date_format="%Y-%m-%d %H:%M")
    rejects.to_csv(rejects_path, index=False)
    return clean_path, rejects_path


def run_pipeline(raw_path=RAW_PATH, out_dir=OUT):
    raw = extract(raw_path)
    clean, rejects = transform(raw, read_fx())
    paths = load(clean, rejects, out_dir)
    return raw, clean, rejects, paths


if __name__ == "__main__":
    raw, clean, rejects, (clean_path, rejects_path) = run_pipeline()
    print(f"Extracted {len(raw)} raw rows -> {len(clean)} clean rows + {len(rejects)} rejected rows")
    print("\nRejected rows:")
    print(rejects[["txn_id", "txn_timestamp", "amount", "reject_reason"]].to_string(index=False))
    print("\nFlagged for review (kept in the clean output):")
    print(clean.loc[clean["needs_review"], ["txn_id", "merchant", "channel", "amount_gbp"]].to_string(index=False))
    print(f"\nChannels: {clean['channel'].value_counts().to_dict()}")
    print(f"Countries: {clean['country'].value_counts().to_dict()}")
    print(f"Total amount_gbp: {clean['amount_gbp'].sum()!r}")
    print(f"\nWrote {clean_path.name} and {rejects_path.name} to {clean_path.parent}")
