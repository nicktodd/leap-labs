from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"

df = pd.read_csv(DATA_PATH)

# SELL-only trades, via .loc + boolean indexing
sell_trades = df.loc[df["side"] == "SELL", ["trade_id", "client_name", "value"]]
print("SELL trades:")
print(sell_trades)

# groupby reproduces Module 3's manual per-client dict-accumulation loop:
# `for trade in trades: value_by_client[client] = value_by_client.get(client, 0.0) + value`
# becomes one line, because groupby already knows how to partition rows by a column
# and .sum() already knows how to accumulate a numeric Series within each partition.
totals_by_client = df.groupby("client_name")["value"].sum()
print("\nTotal value by client:")
print(totals_by_client)

distinct_advisors = df["advisor"].unique()
print(f"\nDistinct advisors: {sorted(distinct_advisors)}")

print("\nModule 3's manual loop: roughly 6 lines (open file, loop, get/add, print loop)")
print("Module 5's pandas line: 1 line (df.groupby('client_name')['value'].sum())")
