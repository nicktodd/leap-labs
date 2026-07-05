# TODO: import trade_value and classify_trade from starter_math, then refactor the loop
# below to use them, and add try/except handling for the malformed trade.

trades = [
    {"trade_id": "T0001", "quantity": 120, "price": 185.32},
    {"trade_id": "T0002", "quantity": 60, "price": 402.11},
    {"trade_id": "T0003", "quantity": "N/A", "price": 98.75},  # malformed, on purpose
    {"trade_id": "T0004", "quantity": 300, "price": 84.22},
    {"trade_id": "T0005", "quantity": 8, "price": 241.20},
]

total = 0.0

for trade in trades:
    value = trade["quantity"] * trade["price"]  # will crash on T0003 as-is
    total += value
    label = "large" if value > 20000 else "normal"
    print(f"{trade['trade_id']}: {label} trade worth {value:,.2f}")

print(f"\nTotal value processed: {total:,.2f}")
