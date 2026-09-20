from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"

# TODO:
# 1. Load DATA_PATH into a DataFrame.
# 2. Select SELL-only trades (trade_id, client_name, value) using .loc + boolean indexing.
# 3. groupby("client_name")["value"].sum() and compare against your Module 3 totals.
# 4. df["advisor"].unique() for the distinct advisors.
# 5. Print a line-count comparison, and comment on what groupby is doing underneath.
