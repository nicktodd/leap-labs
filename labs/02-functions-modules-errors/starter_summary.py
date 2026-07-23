"""Process a list of trades, catching type errors and business-rule violations separately."""

from starter_math import InvalidTradeError, safe_trade_value, classify_trade

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
        value = safe_trade_value(trade)
    except (TypeError, ValueError) as e:
        print(f"{trade['trade_id']}: SKIPPED — wrong type for quantity/price: {e}")
    except InvalidTradeError as e:
        print(f"{trade['trade_id']}: SKIPPED — business-rule violation: {e}")
    else:
        # Only runs on success; accumulate running total here, not inside try
        label = classify_trade(value)
        total += value
        print(f"{trade['trade_id']}: {label} trade worth {value:,.2f}")
    finally:
        # Always runs, regardless of success or failure
        print(f"  processed {trade['trade_id']}")

print(f"\nTotal value processed: {total:,.2f}")
