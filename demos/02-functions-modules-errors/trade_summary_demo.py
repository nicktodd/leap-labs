from trade_math import trade_value, classify_trade

trades = [
    {"trade_id": "T0001", "quantity": 120, "price": 185.32},
    {"trade_id": "T0002", "quantity": 60, "price": 402.11},
    {"trade_id": "T0003", "quantity": "N/A", "price": 98.75},  # malformed
    {"trade_id": "T0004", "quantity": 300, "price": 84.22},
]

total = 0.0

for trade in trades:
    try:
        value = trade_value(trade["quantity"], trade["price"])
    except TypeError:
        print(f"Skipping malformed trade {trade['trade_id']}: bad quantity/price")
        continue

    total += value
    label = classify_trade(value)
    print(f"{trade['trade_id']}: {label} trade worth {value:,.2f}")

print(f"\nTotal value processed: {total:,.2f}")
