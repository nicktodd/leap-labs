"""Extension 3: a self_test() built from assert statements.

Each assert states one fact about payment_utils. Module 12 replaces this with pytest,
which finds and runs functions like these automatically and reports every failure.
"""

from payment_utils import (
    InvalidAmountError,
    PaymentError,
    UnsupportedCurrencyError,
    card_fee,
    parse_amount,
    process_transaction,
    to_gbp,
)


def expect_raises(exc_type, func, *args):
    """Call func(*args) and fail unless it raises exc_type (or a subclass)."""
    try:
        func(*args)
    except exc_type:
        return
    raise AssertionError(f"{func.__name__}{args} did not raise {exc_type.__name__}")


def self_test() -> None:
    # Happy paths. Compare floats with a tolerance, never with == after arithmetic.
    assert parse_amount("78.95") == 78.95
    assert parse_amount(" £1,249.00 ") == 1249.0
    assert parse_amount("€85.50") == 85.5
    assert abs(to_gbp(143.92, "EUR") - 122.332) < 1e-9
    assert to_gbp(100.0, "EUR", {"EUR": 0.9}) == 90.0
    assert card_fee(12.50) == 0.20                  # minimum applies
    assert card_fee(1000.0) == 15.0
    assert card_fee(1000.0, rate=0.01) == 10.0

    # Failure paths: the specific exception type is part of the contract.
    expect_raises(TypeError, parse_amount, None)
    expect_raises(ValueError, parse_amount, "12.5.0")
    expect_raises(ValueError, parse_amount, "")
    expect_raises(InvalidAmountError, parse_amount, "-5.00")
    expect_raises(InvalidAmountError, parse_amount, "0")
    expect_raises(UnsupportedCurrencyError, to_gbp, 10.0, "JPY")
    expect_raises(TypeError, card_fee, 10.0, 0.02)   # rate is keyword-only

    # The hierarchy: subclasses are also PaymentErrors.
    expect_raises(PaymentError, parse_amount, "-5.00")
    expect_raises(PaymentError, process_transaction, {"txn_id": "X1", "amount": "5"})

    # process_transaction keeps the original exception as __cause__.
    try:
        process_transaction({"txn_id": "X2", "currency": "JPY", "amount": "5"})
    except PaymentError as e:
        assert str(e).startswith("X2:")
        assert isinstance(e.__cause__, UnsupportedCurrencyError)
    else:
        raise AssertionError("process_transaction accepted JPY")

    # The test for the test: an assertion that should fail does fail.
    try:
        expect_raises(ValueError, parse_amount, "10.00")
    except AssertionError:
        pass
    else:
        raise AssertionError("expect_raises did not detect a missing exception")

    print("self_test: all checks passed")


if __name__ == "__main__":
    self_test()
