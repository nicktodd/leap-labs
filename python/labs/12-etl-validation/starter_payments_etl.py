"""Module 12 lab starter: an extract-transform-load pipeline for the raw card transactions.

Run:   python starter_payments_etl.py
Each function raises NotImplementedError until you complete it. Complete them in order, and
test each small transform function (Part 2) as soon as it is written.
"""
from pathlib import Path

import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"
RAW_PATH = SHARED / "messy-transactions-raw.csv"
FX_PATH = SHARED / "fx_rates.csv"
OUT = Path(__file__).resolve().parent / "output"

# Every raw channel variant should map to one of these three values after normalising.
CHANNEL_CANONICAL = {"online": "Online", "instore": "In-store", "contactless": "Contactless"}
TIMESTAMP_FORMATS = ["%Y-%m-%d %H:%M", "%d-%b-%Y %H:%M"]
CONTACTLESS_LIMIT_GBP = 100


# --- Extract -------------------------------------------------------------------------------

def extract(path=RAW_PATH):
    """Read the raw file with every column as a string and blanks kept as "".

    TODO: use pd.read_csv with dtype=str and keep_default_na=False.
    TODO: in this docstring, explain why the extract stage should not interpret types.
    """
    raise NotImplementedError


def read_fx(path=FX_PATH):
    return pd.read_csv(path)


# --- Transform: small functions, each one testable on its own -----------------------------

def clean_amount(series):
    """TODO: '£1,249.00' -> 1249.0 and '€85.50' -> 85.5. Anything that is still not a number
    after removing symbols and separators (blank, 'TBC') -> NaN."""
    raise NotImplementedError


def normalise_channel(series):
    """TODO: map every spelling variant to Online / In-store / Contactless. An unrecognised
    value must become NaN, not a guess."""
    raise NotImplementedError


def normalise_country(series):
    """TODO: upper-case ISO country codes; 'UK' -> 'GB'."""
    raise NotImplementedError


def parse_timestamps(series):
    """TODO: parse both TIMESTAMP_FORMATS explicitly; a value matching neither -> NaT."""
    raise NotImplementedError


def fill_categories(df):
    """TODO: fill a blank merchant_category from the category the same merchant has on other
    rows. Return a new DataFrame; do not modify the one passed in."""
    raise NotImplementedError


def add_amount_gbp(df, fx):
    """TODO: add amount_gbp = amount * rate_to_gbp, rounded to 2 decimal places."""
    raise NotImplementedError


def transform(raw, fx):
    """Return (clean, rejects).

    TODO:
    - strip text columns, normalise channel and country
    - reject duplicates (think about the order: when can P0102's second copy be detected?)
    - clean amounts; reject rows whose amount is NaN with reason "bad amount"
    - parse timestamps; reject NaT rows with reason "invalid timestamp"
    - fill categories, convert distance_from_home_km to float and is_fraud to int, add amount_gbp
    - add a needs_review column: Contactless payments above CONTACTLESS_LIMIT_GBP (flag, do
      not delete)
    - rejects: the rejected rows with their RAW values plus a reject_reason column
    """
    raise NotImplementedError


# --- Load ----------------------------------------------------------------------------------

def load(clean, rejects, out_dir=OUT):
    """TODO: create out_dir if needed, write clean_transactions.csv and
    rejected_transactions.csv into it (no index), and return the two paths."""
    raise NotImplementedError


def run_pipeline(raw_path=RAW_PATH, out_dir=OUT):
    raw = extract(raw_path)
    clean, rejects = transform(raw, read_fx())
    paths = load(clean, rejects, out_dir)
    return raw, clean, rejects, paths


if __name__ == "__main__":
    raw, clean, rejects, (clean_path, rejects_path) = run_pipeline()
    print(f"Extracted {len(raw)} raw rows -> {len(clean)} clean rows + {len(rejects)} rejected rows")
    # TODO: print the rejected rows with their reasons, the rows flagged for review, the
    # channel counts and the total amount_gbp.
