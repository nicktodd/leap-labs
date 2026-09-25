from pathlib import Path

import pandas as pd

from ext2_pipe_functions import RAW_PATH, clean

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)


def quality_profile(df):
    """One column of the report: row count, nulls per column, distinct key values."""
    profile = {"rows": len(df)}
    for col in df.columns.drop("needs_review", errors="ignore"):
        profile[f"nulls: {col}"] = int(df[col].isna().sum())
    profile["distinct channel values"] = df["channel"].nunique()
    profile["distinct country values"] = df["country"].nunique()
    profile["exact duplicate rows"] = int(df.duplicated().sum())
    profile["duplicate txn_ids"] = int(df["txn_id"].duplicated().sum())
    return pd.Series(profile)


raw = pd.read_csv(RAW_PATH)
clean_df = clean(raw)

report = pd.DataFrame({"before": quality_profile(raw), "after": quality_profile(clean_df)})
report["change"] = report["after"] - report["before"]
print(report.to_string())

print("\nDistinct values, before -> after:")
for col in ("channel", "country"):
    print(f"  {col}: {sorted(raw[col].map(repr).unique())}")
    print(f"  {' ' * len(col)}  -> {sorted(clean_df[col].unique())}")

report.to_csv(OUT / "quality_report.csv")
print(f"\nWrote {OUT / 'quality_report.csv'}")
