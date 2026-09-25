import time
from pathlib import Path

import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

base = pd.read_csv(SHARED / "transactions.csv")
rates = pd.read_csv(SHARED / "fx_rates.csv").set_index("currency")["rate_to_gbp"]
rate_dict = rates.to_dict()


def gbp_iterrows(df):
    # iterrows builds a new Series object for every row, then Python code runs per row.
    values = []
    for _, row in df.iterrows():
        values.append(row["amount"] * rate_dict[row["currency"]])
    return pd.Series(values, index=df.index)


def gbp_vectorised(df):
    # One lookup and one multiplication over whole columns, executed in compiled code.
    return df["amount"] * df["currency"].map(rates)


for copies in (1, 100):
    df = pd.concat([base] * copies, ignore_index=True)

    start = time.perf_counter()
    loop_result = gbp_iterrows(df)
    loop_secs = time.perf_counter() - start

    start = time.perf_counter()
    vec_result = gbp_vectorised(df)
    vec_secs = time.perf_counter() - start

    assert (loop_result - vec_result).abs().max() < 1e-9  # same answer both ways
    print(f"{len(df):>6} rows: iterrows {loop_secs * 1000:8.2f} ms, "
          f"vectorised {vec_secs * 1000:6.2f} ms, ratio {loop_secs / vec_secs:6.0f}x")

# Explanation: the loop pays Python-level overhead (creating a Series per row, dict
# lookups, appends) for every row, so its cost grows row by row. The vectorised version
# makes a handful of calls that each process the whole column in NumPy's compiled code.
# At 140 rows both are fast enough (roughly 10x apart); the gap widens as data grows
# (a few hundred times at 14,000 rows). Exact timings vary by machine and run.
