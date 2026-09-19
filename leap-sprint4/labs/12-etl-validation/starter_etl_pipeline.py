from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2] / "shared"


def extract():
    """TODO: read shared/messy-trades-raw.csv and return it unchanged."""
    raise NotImplementedError


def transform(df):
    """TODO: apply Module 6's cleaning steps: drop the row with missing quantity,
    recompute the missing value, backfill the missing client_name, parse the
    ambiguous date, normalise asset_class casing (without breaking ETF), and drop
    the exact duplicate row."""
    raise NotImplementedError


def load(df, out_path):
    """TODO: write df to out_path as a CSV, and return out_path."""
    raise NotImplementedError


if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    out_path = Path(__file__).resolve().parent / "clean_trades_loaded.csv"
    load(clean, out_path)
    print(f"Extracted {len(raw)} raw rows, transformed to {len(clean)} clean rows")
