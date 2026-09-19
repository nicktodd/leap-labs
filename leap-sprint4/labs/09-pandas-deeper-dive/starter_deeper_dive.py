from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2] / "shared"
trades = pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])
advisors = pd.read_csv(BASE / "advisors.csv")

# TODO:
# 1. groupby("client_name")["value"].agg(["count", "sum", "mean"])
# 2. pivot_table: index=instrument, columns=side, values=value, aggfunc=sum, fill_value=0
# 3. merge trades with advisors on "advisor", then total value by team
# 4. set_index("trade_date") and resample("W")["value"].sum()
# 5. 3-5 one-line takeaways as comments, each citing a specific number above
