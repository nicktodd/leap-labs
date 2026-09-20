trades = [
    {"trade_id": "T0001", "side": "BUY", "quantity": 120, "price": 185.32},
    {"trade_id": "T0002", "side": "BUY", "quantity": 60, "price": 402.11},
    {"trade_id": "T0003", "side": "SELL", "quantity": 5000, "price": 98.75},
    {"trade_id": "T0004", "side": "SELL", "quantity": 40, "price": 186.10},
    {"trade_id": "T0005", "side": "BUY", "quantity": 25, "price": 141.87},
    {"trade_id": "T0006", "side": "BUY", "quantity": 300, "price": 84.22},
    {"trade_id": "T0007", "side": "SELL", "quantity": 20, "price": 404.55},
    {"trade_id": "T0008", "side": "BUY", "quantity": 0.5, "price": 42000.00},
]

LARGE_TRADE_THRESHOLD = 20000

total_count = 0
total_value = 0.0
buy_count = 0
sell_count = 0

for trade in trades:
    value = trade["quantity"] * trade["price"]
    total_count += 1
    total_value += value

    if value > LARGE_TRADE_THRESHOLD:
        print(f"Large trade: {trade['trade_id']} ({trade['side']}) worth {value:,.2f}")

    if trade["side"] == "BUY":
        buy_count += 1
    elif trade["side"] == "SELL":
        sell_count += 1

print("\n--- Summary ---")
print(f"Total trades: {total_count}")
print(f"Total value: {total_value:,.2f}")
print(f"BUY trades:  {buy_count}")
print(f"SELL trades: {sell_count}")
