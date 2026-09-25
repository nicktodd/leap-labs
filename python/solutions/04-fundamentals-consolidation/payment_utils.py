"""payment_utils.py - parsing, conversion and fee rules for PaySprint card payments.

Importing this module defines names only; the examples at the bottom run only when the
file is executed directly (python payment_utils.py).
"""

# Default FX (foreign exchange) rates to GBP. Module 3 reads these from shared/fx_rates.csv.
DEFAULT_RATES = {"GBP": 1.00, "EUR": 0.85, "USD": 0.79}

CURRENCY_SYMBOLS = "£€$"


class PaymentError(Exception):
    """Base class for every payment rule failure. Catch this to catch them all."""


class InvalidAmountError(PaymentError):
    """Raised when an amount parses as a number but is not a valid payment amount."""


class UnsupportedCurrencyError(PaymentError):
    """Raised when there is no FX rate for a transaction's currency."""


def parse_amount(text: str) -> float:
    """Turn raw amount text such as " £1,249.00 " into a positive float.

    Raises TypeError if text is not a str (e.g. None), ValueError if the cleaned text is
    not a number, and InvalidAmountError if the number is zero or negative.
    """
    # Type hints are not enforced at runtime, so check explicitly. Without this,
    # None would fail later with a less helpful AttributeError on .strip().
    if not isinstance(text, str):
        raise TypeError(f"amount must be a str, got {type(text).__name__}")
    cleaned = text.strip()
    if cleaned and cleaned[0] in CURRENCY_SYMBOLS:
        cleaned = cleaned[1:]
    cleaned = cleaned.replace(",", "")
    amount = float(cleaned)   # raises ValueError for text like "12.5.0" or ""
    if amount <= 0:
        raise InvalidAmountError(f"amount must be positive, got {amount}")
    return amount


def to_gbp(amount: float, currency: str, rates: dict[str, float] | None = None) -> float:
    """Convert amount in currency to GBP, using DEFAULT_RATES unless rates is given.

    The default is None, not {} or DEFAULT_RATES: a mutable default is created once, when
    the function is defined, and shared by every call, so any change made to it inside the
    function would leak into later calls.
    """
    if rates is None:
        rates = DEFAULT_RATES
    if currency not in rates:
        raise UnsupportedCurrencyError(f"no FX rate for {currency}")
    return amount * rates[currency]


def card_fee(amount_gbp: float, *, rate: float = 0.015, minimum: float = 0.20) -> float:
    """Return the processing fee in GBP: rate * amount, but never less than minimum.

    rate and minimum are keyword-only (everything after the bare *), so a call site must
    say card_fee(10.0, rate=0.02); card_fee(10.0, 0.02) is a TypeError. Two float
    arguments passed by position are too easy to swap.
    """
    return max(round(amount_gbp * rate, 2), minimum)


def process_transaction(txn: dict) -> float:
    """Return the GBP amount of a raw transaction dict, or raise PaymentError.

    A missing field, a badly formatted amount or a payment rule failure is re-raised as a
    PaymentError that names the txn_id, with the original exception kept as __cause__.
    Callers therefore only need to catch PaymentError.
    """
    txn_id = txn.get("txn_id", "<no txn_id>")
    try:
        amount = parse_amount(txn["amount"])
        return to_gbp(amount, txn["currency"])
    except KeyError as e:
        raise PaymentError(f"{txn_id}: missing field {e}") from e
    except (TypeError, ValueError) as e:
        raise PaymentError(f"{txn_id}: bad amount format ({e})") from e
    except PaymentError as e:
        raise PaymentError(f"{txn_id}: {e}") from e


if __name__ == "__main__":
    print(parse_amount(" £1,249.00 "))                   # 1249.0
    print(to_gbp(100.0, "EUR"))                           # 85.0
    print(to_gbp(100.0, "EUR", {"EUR": 0.90}))            # 90.0, custom rates
    print(card_fee(12.50))                                # 0.2, the minimum applies
    print(card_fee(1000.0, rate=0.01))                    # 10.0
    # Prints 122.33199999999998: binary floating-point noise (Extension 4 fixes this).
    print(process_transaction({"txn_id": "P0002", "currency": "EUR", "amount": "€143.92"}))
