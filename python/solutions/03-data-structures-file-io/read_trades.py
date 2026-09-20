import csv
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"

trades = []
with open(DATA_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        trades.append(row)

value_by_client = {}
advisors = set()

for trade in trades:
    client = trade["client_name"]
    value = float(trade["value"])
    value_by_client[client] = value_by_client.get(client, 0.0) + value
    advisors.add(trade["advisor"])

print("Distinct advisors:", sorted(advisors))
print()

summary_path = Path(__file__).resolve().parent / "client_summary.txt"
with open(summary_path, "w", encoding="utf-8") as f:
    for client, total in sorted(value_by_client.items()):
        line = f"{client}: {total:,.2f}"
        print(line)
        f.write(line + "\n")

print(f"\nSummary written to {summary_path.name}")
