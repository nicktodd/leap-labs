# TODO: import from starter_math, then refactor the loop below to:
# - catch (TypeError, ValueError) together for a wrong-type quantity/price
# - catch InvalidTradeError separately for a business-rule failure
# - use else to accumulate the running total only on success
# - use finally to print a "processed <trade_id>" line unconditionally

trades = [
    {"trade_id": "T0001", "quantity": 120, "price": 185.32},
    {"trade_id": "T0002", "quantity": "N/A", "price": 402.11},  # wrong type
    {"trade_id": "T0003", "quantity": -5, "price": 98.75},       # fails validation
    {"trade_id": "T0004", "quantity": 300, "price": 84.22},
    {"trade_id": "T0005", "quantity": 8, "price": 241.20},
]

total = 0.0

for trade in trades:
    value = trade["quantity"] * trade["price"]  # will crash on T0002/T0003 as-is
    total += value
    label = "large" if value > 20000 else "normal"
    print(f"{trade['trade_id']}: {label} trade worth {value:,.2f}")

print(f"\nTotal value processed: {total:,.2f}")
