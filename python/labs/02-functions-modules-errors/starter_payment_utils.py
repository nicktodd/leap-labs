"""TODO: replace this line with a module docstring describing the module.

Complete this module, then import from it in starter_process_payments.py with
`from starter_payment_utils import ...`. (The model answer calls it payment_utils.py.)
"""

# Default FX (foreign exchange) rates to GBP.
DEFAULT_RATES = {"GBP": 1.00, "EUR": 0.85, "USD": 0.79}

# TODO 1: define the exception hierarchy:
#   PaymentError(Exception)
#   InvalidAmountError(PaymentError)
#   UnsupportedCurrencyError(PaymentError)
# Each needs only a docstring.


def parse_amount(text: str) -> float:
    """TODO 2: turn raw text such as " £1,249.00 " into a positive float.

    - raise TypeError yourself if text is not a str (None must not reach .strip())
    - strip whitespace, one leading £, € or $, and thousands separators
    - let float() raise ValueError for text that is still not a number
    - raise InvalidAmountError if the result is zero or negative
    """
    raise NotImplementedError


def to_gbp(amount: float, currency: str, rates: dict[str, float] | None = None) -> float:
    """TODO 3: return amount converted to GBP.

    Use DEFAULT_RATES when rates is None. Raise UnsupportedCurrencyError when the currency
    has no rate. Answer in a comment: why is the default None and not rates={}?
    """
    raise NotImplementedError


def card_fee(amount_gbp: float, *, rate: float = 0.015, minimum: float = 0.20) -> float:
    """TODO 4: return the fee, rate * amount_gbp rounded to 2 dp, but at least minimum.

    Note the bare * in the signature: what does it force callers to do?
    """
    raise NotImplementedError


def process_transaction(txn: dict) -> float:
    """TODO 5: return the GBP amount for a raw transaction dict.

    Call parse_amount and to_gbp. Convert a KeyError, a TypeError or ValueError from a bad
    amount, or any PaymentError subclass into a PaymentError whose message starts with the
    txn_id, using `raise ... from e`. Callers then only need `except PaymentError`.
    """
    raise NotImplementedError


# TODO 6: add an `if __name__ == "__main__":` block with one example call per function.
