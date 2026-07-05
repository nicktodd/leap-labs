from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2] / "shared"

ASSET_CLASS_CANONICAL = {"equity": "Equity", "bond": "Bond", "etf": "ETF", "crypto": "Crypto"}


def extract():
    return pd.read_csv(BASE / "messy-trades-raw.csv")


def transform(df):
    df = df[df["quantity"].notna()].copy()
    df["quantity"] = df["quantity"].astype(float)

    missing_value = df["value"].isna()
    df.loc[missing_value, "value"] = df.loc[missing_value, "quantity"] * df.loc[missing_value, "price"]

    df["client_name"] = df.groupby("client_id")["client_name"].transform("first")
    df["trade_date"] = pd.to_datetime(df["trade_date"], format="mixed", dayfirst=True)
    df["asset_class"] = df["asset_class"].str.lower().map(ASSET_CLASS_CANONICAL)
    df = df.drop_duplicates()
    return df


def load(df, out_path):
    df.to_csv(out_path, index=False)
    return out_path


if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    out_path = Path(__file__).resolve().parent / "clean_trades_loaded.csv"
    load(clean, out_path)
    print(f"Extracted {len(raw)} raw rows, transformed to {len(clean)} clean rows")
