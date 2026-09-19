# TODO:
# 1. Define InvalidTradeError(Exception).
# 2. Write trade_value(quantity: float, price: float) -> float, raising InvalidTradeError
#    if quantity or price is not positive.
# 3. Write classify_trade(value: float, threshold: float = 20000) -> str.
# 4. Write safe_trade_value(trade: dict) -> float, which calls trade_value and re-raises
#    InvalidTradeError with the trade_id folded into the message (raise ... from e).
# 5. Add docstrings, and an `if __name__ == "__main__":` block with one example call.
