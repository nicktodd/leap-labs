"""Lab 12: ETL pipeline — extract, transform, load for messy-trades-raw.csv."""

from pathlib import Path
import pandas as pd

BASE = Path(r"C:\Users\zackt\Documents\leap-sprint4\shared")

ASSET_CLASS_MAP = {
    "equity": "Equity",
    "bond": "Bond",
    "etf": "ETF",
    "crypto": "Crypto",
    "Equity": "Equity",
    "Bond": "Bond",
    "ETF": "ETF",
    "Crypto": "Crypto",
}


def extract() -> pd.DataFrame:
    """Read shared/messy-trades-raw.csv and return the raw DataFrame unchanged."""
    return pd.read_csv(BASE / "messy-trades-raw.csv")


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all cleaning steps from Module 6 and return the cleaned DataFrame."""
    df = df.copy()

    # Drop the row with missing quantity — cannot be reconstructed without the unit count.
    df = df.dropna(subset=["quantity"])

    # Recompute the missing value as quantity * price — both columns present, so derivable.
    missing_val = df["value"].isna()
    df.loc[missing_val, "value"] = df.loc[missing_val, "quantity"] * df.loc[missing_val, "price"]

    # Backfill missing client_name from another row with the same client_id.
    name_lookup = (
        df.dropna(subset=["client_name"])
        .drop_duplicates(subset=["client_id"])
        .set_index("client_id")["client_name"]
    )
    missing_name = df["client_name"].isna()
    df.loc[missing_name, "client_name"] = df.loc[missing_name, "client_id"].map(name_lookup)

    # Parse trade_date using format="mixed" with dayfirst=True to handle the DD/MM/YYYY row.
    df["trade_date"] = pd.to_datetime(df["trade_date"], format="mixed", dayfirst=True)

    # Normalise asset_class via explicit canonical mapping — avoids .capitalize() turning ETF→Etf.
    df["asset_class"] = df["asset_class"].map(ASSET_CLASS_MAP)

    # Drop the exact duplicate row (T0006 appears twice).
    df = df.drop_duplicates()

    return df


def load(df: pd.DataFrame, out_path: Path) -> Path:
    """Write df to out_path as a CSV and return the path."""
    df.to_csv(out_path, index=False)
    return out_path


if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    out_path = Path(__file__).resolve().parent / "clean_trades_loaded.csv"
    load(clean, out_path)
    print(f"Extracted {len(raw)} raw rows, transformed to {len(clean)} clean rows")
    print(f"Loaded to {out_path}")
