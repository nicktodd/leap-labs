from trade_math import trade_value, classify_trade

trades = [
    {"trade_id": "T0001", "quantity": 120, "price": 185.32},
    {"trade_id": "T0002", "quantity": 60, "price": 402.11},
    {"trade_id": "T0003", "quantity": "N/A", "price": 98.75},  # malformed, on purpose
    {"trade_id": "T0004", "quantity": 300, "price": 84.22},
    {"trade_id": "T0005", "quantity": 8, "price": 241.20},
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

# Keyword argument form, with a higher threshold for a VIP client's book
vip_value = trade_value(500, 200.00)
print(f"\nVIP check: {classify_trade(vip_value, threshold=50000)} (value {vip_value:,.2f})")
