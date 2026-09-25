"""Module 14 capstone starter: PaySprint card payments monthly dashboard.

Pipeline: extract -> transform -> validate -> load -> compute_insights -> build_charts
-> print_dashboard. The source is the MESSY raw export, so transform() has real work to do.

Run from any folder:  python labs/14-sprint4-capstone-wrapup/starter_payments_dashboard.py
"""
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")  # draw charts to files, no window needed
import matplotlib.pyplot as plt  # noqa: E402,F401  (the backend must be chosen first)

SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

PERIOD_START = pd.Timestamp("2026-02-02")
PERIOD_END = pd.Timestamp("2026-03-02")  # exclusive: the month runs to the end of Sun 1 Mar
CONTACTLESS_LIMIT_GBP = 100


def extract():
    """TODO (step 1): read shared/messy-transactions-raw.csv with every column as text
    (dtype=str, keep_default_na=False) and shared/fx_rates.csv. Return (raw, fx)."""
    raise NotImplementedError


def transform(raw, fx):
    """TODO (step 2): clean the raw rows, reusing your Module 6 / Module 12 cleaning.
    Think about the ORDER of the steps: some duplicates only appear after normalisation.
    - strip whitespace, standardise channel spellings, UK -> GB
    - remove duplicates, and record which txn_ids were rejected and why
    - amounts: remove symbols and separators; reject blank / non-numeric amounts
    - timestamps: two formats; reject any that cannot be parsed (do not guess)
    - fill missing merchant_category from the same merchant's other rows
    - add amount_gbp using the FX rates
    - add a held_for_review flag for a contactless payment over CONTACTLESS_LIMIT_GBP
    Return (clean DataFrame, quality) where quality records rows received, rows rejected
    with a reason each, and the transactions held for review."""
    raise NotImplementedError


def validate(df):
    """TODO (step 3): return a list of failed checks as readable strings (an empty list
    means the data is safe to analyse). Check at least: required columns present and not
    null, txn_id unique, channel/country/status only allowed values, every currency has
    an FX rate, amounts positive, every timestamp inside the reporting month."""
    raise NotImplementedError


def load(df, out_path):
    """TODO (step 4): write df to out_path as CSV and return out_path."""
    raise NotImplementedError


def compute_insights(df, quality):
    """TODO (step 5): compute at least three insights in GBP, each backed by a specific
    number, plus the data-quality figures. Decide and document what counts as
    "customer spend" (approved? confirmed fraud? held for review?). Return a dict."""
    raise NotImplementedError


def build_charts(df, insights):
    """TODO (step 6): build at least two charts that support your insights (Module 10:
    honest axes, a title that states the finding, labelled axes with units). Save them
    as PNGs in OUT and return their paths."""
    raise NotImplementedError


def print_dashboard(insights):
    """TODO (step 7): print a plain-text dashboard a non-technical reader can follow
    without opening a chart: the period, the insights with their numbers, and one
    data-quality line (rows received, rejected and why, loaded, held for review)."""
    raise NotImplementedError


if __name__ == "__main__":
    raw_rows, rates = extract()
    clean, quality = transform(raw_rows, rates)

    failures = validate(clean)
    if failures:
        # The gate: nothing is loaded or analysed if any check fails.
        raise SystemExit("Validation failed: " + "; ".join(failures))

    load(clean, OUT / "dashboard_data.csv")
    results = compute_insights(clean, quality)
    build_charts(clean, results)
    print_dashboard(results)
