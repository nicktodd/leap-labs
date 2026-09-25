"""Extension 1: exceptions that carry data (txn_id, reason) as well as a message.

The core solution had to parse the reason back out of which except clause fired. Here the
exception carries it, so a single `except PaymentError` can build the whole summary.
"""

from process_payments import raw_transactions   # reuse the same 12 records

DEFAULT_RATES = {"GBP": 1.00, "EUR": 0.85, "USD": 0.79}


class PaymentError(Exception):
    """Base payment failure, carrying the txn_id and a short machine-friendly reason."""

    def __init__(self, message: str, *, txn_id: str | None = None,
                 reason: str = "payment error"):
        super().__init__(message)   # keeps str(e) and the traceback text working
        self.txn_id = txn_id
        self.reason = reason


class InvalidAmountError(PaymentError):
    """Amount parsed but is not a valid payment amount."""


class UnsupportedCurrencyError(PaymentError):
    """No FX rate for the currency."""


def parse_amount(text: str) -> float:
    """Same rules as payment_utils.parse_amount."""
    if not isinstance(text, str):
        raise TypeError(f"amount must be a str, got {type(text).__name__}")
    cleaned = text.strip()
    if cleaned and cleaned[0] in "£€$":
        cleaned = cleaned[1:]
    amount = float(cleaned.replace(",", ""))
    if amount <= 0:
        raise InvalidAmountError(f"amount must be positive, got {amount}",
                                 reason="invalid amount")
    return amount


def to_gbp(amount: float, currency: str, rates: dict[str, float] | None = None) -> float:
    """Same rules as payment_utils.to_gbp."""
    if rates is None:
        rates = DEFAULT_RATES
    if currency not in rates:
        raise UnsupportedCurrencyError(f"no FX rate for {currency}",
                                       reason="unsupported currency")
    return amount * rates[currency]


def process_transaction(txn: dict) -> float:
    """Return the GBP amount, or raise PaymentError with txn_id and reason set."""
    txn_id = txn.get("txn_id", "<no txn_id>")
    try:
        return to_gbp(parse_amount(txn["amount"]), txn["currency"])
    except KeyError as e:
        raise PaymentError(f"{txn_id}: missing field {e}", txn_id=txn_id,
                           reason="missing field") from e
    except (TypeError, ValueError) as e:
        raise PaymentError(f"{txn_id}: bad amount format ({e})", txn_id=txn_id,
                           reason="bad format") from e
    except PaymentError as e:
        # Keep the specific subclass's reason; add the txn_id the inner code lacked.
        raise PaymentError(f"{txn_id}: {e}", txn_id=txn_id, reason=e.reason) from e


if __name__ == "__main__":
    failures: dict[str, list[str]] = {}
    total_gbp = 0.0
    for txn in raw_transactions:
        try:
            total_gbp += process_transaction(txn)
        except PaymentError as e:
            # One handler: the exception object tells us everything we need.
            failures.setdefault(e.reason, []).append(e.txn_id)
    print(f"Total GBP {total_gbp:,.2f}")
    for reason, txn_ids in failures.items():
        print(f"  {reason}: {len(txn_ids)} ({', '.join(txn_ids)})")
