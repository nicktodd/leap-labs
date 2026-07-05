from trade_math import trade_value, classify_trade, InvalidTradeError, safe_trade_value

trades = [
    {"trade_id": "T0001", "quantity": 120, "price": 185.32},
    {"trade_id": "T0002", "quantity": "N/A", "price": 402.11},  # wrong type
    {"trade_id": "T0003", "quantity": -5, "price": 98.75},       # fails validation
    {"trade_id": "T0004", "quantity": 300, "price": 84.22},
    {"trade_id": "T0005", "quantity": 8, "price": 241.20},
]

total = 0.0

for trade in trades:
    try:
        value = trade_value(trade["quantity"], trade["price"])
    except (TypeError, ValueError) as e:
        print(f"Skipping {trade['trade_id']}: bad data type ({e})")
        continue
    except InvalidTradeError as e:
        print(f"Skipping {trade['trade_id']}: {e}")
        continue
    else:
        total += value
        print(f"{trade['trade_id']}: {classify_trade(value)} trade worth {value:,.2f}")
    finally:
        print(f"  processed {trade['trade_id']}")

print(f"\nTotal value processed: {total:,.2f}")

# Keyword argument form, with a higher threshold for a VIP client's book
vip_value = trade_value(500, 200.00)
print(f"\nVIP check: {classify_trade(vip_value, threshold=50000)} (value {vip_value:,.2f})")

# safe_trade_value re-raises with the trade_id folded into the message
try:
    safe_trade_value({"trade_id": "T0099", "quantity": -1, "price": 100.0})
except InvalidTradeError as e:
    print(f"\nCaught re-raised error: {e}")
