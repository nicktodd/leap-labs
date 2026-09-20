"""trade_math.py — a small, reusable module of trade calculations.

Keeping this file import-safe (no code runs just from importing it, other than
definitions) is what makes it a well-behaved module: anything meant to run only
when this file is executed directly belongs behind the __main__ guard at the
bottom.
"""


class InvalidTradeError(Exception):
    """Raised when a trade record fails basic validation."""


def trade_value(quantity: float, price: float) -> float:
    """Return quantity * price, after validating both are positive."""
    if quantity <= 0:
        raise InvalidTradeError(f"quantity must be positive, got {quantity}")
    if price <= 0:
        raise InvalidTradeError(f"price must be positive, got {price}")
    return quantity * price


def classify_trade(value: float, threshold: float = 20000) -> str:
    """Return "large" if value exceeds threshold, else "normal"."""
    return "large" if value > threshold else "normal"


def safe_trade_value(trade: dict) -> float:
    """Wrap trade_value, adding the trade_id to any error before re-raising it."""
    try:
        return trade_value(trade["quantity"], trade["price"])
    except InvalidTradeError as e:
        raise InvalidTradeError(f"{trade['trade_id']}: {e}") from e


if __name__ == "__main__":
    # Only runs when this file is executed directly, e.g. `python trade_math.py`,
    # never when another script does `from trade_math import trade_value`.
    print(trade_value(120, 185.32))
    print(classify_trade(22238.40))
