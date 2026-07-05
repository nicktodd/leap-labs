# Demo: core Python syntax, data types, and control flow, applied to a handful of
# in-memory trade records. No libraries: this is deliberately manual bookkeeping.

trades = [
    {"trade_id": "T0001", "side": "BUY", "quantity": 120, "price": 185.32},
    {"trade_id": "T0002", "side": "BUY", "quantity": 60, "price": 402.11},
    {"trade_id": "T0003", "side": "SELL", "quantity": 40, "price": 186.10},
    {"trade_id": "T0004", "side": "BUY", "quantity": 25, "price": 141.87},
    {"trade_id": "T0005", "side": "SELL", "quantity": 20, "price": 404.55},
]

# Basic data types
trade_id = trades[0]["trade_id"]   # str
quantity = trades[0]["quantity"]    # int
price = trades[0]["price"]           # float
is_buy = trades[0]["side"] == "BUY"   # bool

print(f"First trade {trade_id}: quantity={quantity} ({type(quantity).__name__}), "
      f"price={price} ({type(price).__name__}), is_buy={is_buy}")

# Control flow: classify and total, one trade at a time
total_count = 0
total_value = 0.0
buy_value = 0.0
sell_value = 0.0

for trade in trades:
    value = trade["quantity"] * trade["price"]
    total_count += 1
    total_value += value

    if trade["side"] == "BUY":
        buy_value += value
    elif trade["side"] == "SELL":
        sell_value += value
    else:
        print(f"Unrecognised side for {trade['trade_id']}: {trade['side']}")

print(f"\nTotal trades: {total_count}")
print(f"Total value: {total_value:,.2f}")
print(f"BUY value:  {buy_value:,.2f}")
print(f"SELL value: {sell_value:,.2f}")

# A while loop, briefly, for completeness
i = 0
while i < len(trades):
    i += 1
print(f"\nCounted {i} trades with a while loop, same answer as the for loop above.")
