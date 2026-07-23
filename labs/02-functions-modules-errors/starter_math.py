"""Trade math utilities: validation, value calculation, and classification.

This module provides functions for computing and classifying trade values,
with custom error handling for invalid trade inputs.
"""


class InvalidTradeError(Exception):
    """Raised when a trade violates a business rule (e.g. non-positive quantity or price)."""


def trade_value(quantity: float, price: float) -> float:
    """Return quantity * price, raising InvalidTradeError if either is not positive.

    Args:
        quantity: Number of units traded.
        price: Price per unit.

    Returns:
        The total trade value as a float.

    Raises:
        InvalidTradeError: If quantity or price is not strictly positive.
    """
    if quantity <= 0 or price <= 0:
        raise InvalidTradeError(
            f"quantity and price must both be positive (got quantity={quantity}, price={price})"
        )
    return quantity * price


def classify_trade(value: float, threshold: float = 20000) -> str:
    """Return 'LARGE' if value exceeds threshold, otherwise 'normal'.

    Args:
        value: The trade value to classify.
        threshold: The cut-off above which a trade is considered LARGE (default 20000).

    Returns:
        'LARGE' or 'normal'.
    """
    return "LARGE" if value > threshold else "normal"


def safe_trade_value(trade: dict) -> float:
    """Compute trade value for a trade dict, re-raising with trade_id on failure.

    Args:
        trade: A dict with at least 'trade_id', 'quantity', and 'price' keys.

    Returns:
        The computed trade value.

    Raises:
        InvalidTradeError: Re-raised with the trade_id folded into the message.
    """
    try:
        return trade_value(trade["quantity"], trade["price"])
    except InvalidTradeError as e:
        raise InvalidTradeError(
            f"Trade {trade['trade_id']}: {e}"
        ) from e


if __name__ == "__main__":
    example = {"trade_id": "T0001", "quantity": 120, "price": 185.32}
    val = safe_trade_value(example)
    label = classify_trade(val)
    print(f"{example['trade_id']}: {label} trade worth {val:,.2f}")
