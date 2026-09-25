"""Process a batch of raw PaySprint transactions, reporting every failure by reason."""

from payment_utils import (
    InvalidAmountError,
    PaymentError,
    UnsupportedCurrencyError,
    card_fee,
    parse_amount,
    process_transaction,
    to_gbp,
)

# Raw records as they arrive from a card terminal feed: amounts are text, not numbers.
raw_transactions = [
    {"txn_id": "P0001", "merchant": "Tesco", "currency": "GBP", "amount": "78.95"},
    {"txn_id": "P0002", "merchant": "Amazon", "currency": "EUR", "amount": "€143.92"},
    {"txn_id": "P0015", "merchant": "Pret A Manger", "currency": "GBP", "amount": "£5.05"},
    {"txn_id": "P0016", "merchant": "Apple Store", "currency": "USD", "amount": "$1,594.61"},
    {"txn_id": "P0034", "merchant": "Apple Store", "currency": "GBP", "amount": " 293.81 "},
    {"txn_id": "P0048", "merchant": "Uber", "currency": "GBP", "amount": "12.5.0"},
    {"txn_id": "P0057", "merchant": "Airbnb", "currency": "EUR", "amount": None},
    {"txn_id": "P0061", "merchant": "Pret A Manger", "currency": "EUR", "amount": "-5.00"},
    {"txn_id": "P0098", "merchant": "British Airways", "currency": "GBP", "amount": "1,249.00"},
    {"txn_id": "P0999", "merchant": "Uniqlo Ginza", "currency": "JPY", "amount": "4500"},
    {"txn_id": "P0120", "merchant": "Amazon", "amount": "624.51"},   # no currency key
    {"txn_id": "P0134", "merchant": "Costa Coffee", "currency": "GBP", "amount": "£2.91"},
]


def main() -> None:
    """Process raw_transactions, printing each outcome and a failure summary."""
    total_gbp = 0.0
    total_fees = 0.0
    processed = 0
    failures = {"bad format": 0, "unsupported currency": 0, "invalid amount": 0,
                "missing field": 0}

    for txn in raw_transactions:
        txn_id = txn["txn_id"]
        try:
            amount = parse_amount(txn["amount"])
            amount_gbp = to_gbp(amount, txn["currency"])
        except (TypeError, ValueError) as e:
            print(f"Skipping {txn_id}: bad amount format ({e})")
            failures["bad format"] += 1
        except UnsupportedCurrencyError as e:
            print(f"Skipping {txn_id}: {e}")
            failures["unsupported currency"] += 1
        except InvalidAmountError as e:
            print(f"Skipping {txn_id}: {e}")
            failures["invalid amount"] += 1
        except KeyError as e:
            print(f"Skipping {txn_id}: missing field {e}")
            failures["missing field"] += 1
        else:
            # Runs only if the try block raised nothing.
            fee = card_fee(amount_gbp)
            total_gbp += amount_gbp
            total_fees += fee
            print(f"{txn_id}: GBP {amount_gbp:,.2f}, fee GBP {fee:.2f}")
        finally:
            # Runs for every record, success or failure.
            processed += 1

    ok = processed - sum(failures.values())
    print(f"\nProcessed {processed} records: {ok} succeeded")
    print(f"Total GBP {total_gbp:,.2f}, total fees GBP {total_fees:.2f}")
    print(f"Failures by reason: {failures}")

    # Question: why must `except PaymentError` come after its subclasses if it is used in the
    # same try? Answer: except clauses are tested top to bottom and the first match wins. An
    # UnsupportedCurrencyError *is a* PaymentError, so a PaymentError clause placed first would
    # catch it, and the more specific clauses below it would never run.

    # process_transaction wraps any failure in the base class, with the txn_id added.
    try:
        process_transaction(raw_transactions[9])
    except PaymentError as e:
        print(f"\nCaught {type(e).__name__}: {e}")
        print(f"  __cause__ is {type(e.__cause__).__name__}: {e.__cause__}")

    try:
        process_transaction(raw_transactions[10])
    except PaymentError as e:
        print(f"Caught {type(e).__name__}: {e}")
        print(f"  __cause__ is {type(e.__cause__).__name__}: {e.__cause__}")


# The guard lets the extension files import raw_transactions without running main().
if __name__ == "__main__":
    main()
