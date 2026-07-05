import csv
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"

# --- Part 1: data structures, quickly ---
instruments_list = ["AAPL", "MSFT", "AAPL"]              # list: ordered, can change
instrument_asset = ("AAPL", "Equity")                      # tuple: ordered, can't change
first_trade = {"trade_id": "T0001", "quantity": 120}         # dict: lookup by key
distinct_instruments_demo = {"AAPL", "MSFT", "AAPL"}          # set: duplicates removed

print("List:", instruments_list)
print("Tuple:", instrument_asset)
print("Dict:", first_trade)
print("Set (duplicates removed):", distinct_instruments_demo)

try:
    instrument_asset[0] = "MSFT"
except TypeError as e:
    print(f"Tuples can't be modified: {e}")

# --- Part 2: read the mission dataset with csv.DictReader ---
trades = []
with open(DATA_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        trades.append(row)

print(f"\nRead {len(trades)} trades from {DATA_PATH.name}")

# --- Part 3: build a summary dict keyed by instrument, write it to a file ---
value_by_instrument = {}
for trade in trades:
    instrument = trade["instrument"]
    value = float(trade["value"])
    value_by_instrument[instrument] = value_by_instrument.get(instrument, 0.0) + value

distinct_instruments = set(value_by_instrument.keys())
print(f"Distinct instruments traded: {sorted(distinct_instruments)}")

summary_path = Path(__file__).resolve().parent / "instrument_summary.txt"
with open(summary_path, "w", encoding="utf-8") as f:
    for instrument, total in sorted(value_by_instrument.items()):
        line = f"{instrument}: {total:,.2f}"
        print(line)
        f.write(line + "\n")

print(f"\nSummary written to {summary_path.name}")
