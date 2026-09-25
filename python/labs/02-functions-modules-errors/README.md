# Module 2 Lab - Functions, Modules & Error Handling

## Scenario

PaySprint's card terminals send transactions as raw text. Amounts arrive with currency symbols
and thousands separators, some are malformed, one record is in a currency PaySprint cannot
price, and one has lost its `currency` field. The current processing loop crashes on the first
bad record. Your job is to build a small, reusable `payment_utils` module with its own exception
hierarchy, and a processing script that handles every failure, counts it by reason and carries
on.

## Objectives

By the end of this lab you will have:

- Written functions with type hints and docstrings, including an optional parameter defaulting
  to `None` and keyword-only parameters
- Written a well-behaved module with a module docstring and an `if __name__ == "__main__":` guard
- Defined an exception hierarchy (a base class and two subclasses) and raised each where a
  business rule fails
- Raised a built-in exception (`TypeError`) yourself when an argument has the wrong type
- Ordered several `except` clauses correctly, and used `else` and `finally` for their intended
  purposes
- Converted low-level exceptions into a domain exception with `raise ... from e`, and inspected
  `__cause__`

## Setup

- Python 3.11+, no external libraries
- Starter files in `labs/02-functions-modules-errors/`:
  - `starter_payment_utils.py`: the module to complete (stubs raise `NotImplementedError`)
  - `starter_process_payments.py`: the processing script, with 12 raw records and a naive loop
- Run `python starter_process_payments.py` before changing anything. It crashes with a
  `ValueError` on P0002 (`'€143.92'`). Read the traceback: which line failed, and why?

## The data

`raw_transactions` in `starter_process_payments.py` holds 12 dicts with `txn_id`, `merchant`,
`currency` and `amount`. Every `amount` is a string (or `None`), exactly as it would arrive from
a text feed:

| Kind of value | Examples |
|---|---|
| Clean or recoverable | `"78.95"`, `"€143.92"`, `"$1,594.61"`, `" 293.81 "`, `"1,249.00"` |
| Not a number | `"12.5.0"` (P0048), `None` (P0057) |
| A number, but not a valid payment | `"-5.00"` (P0061) |
| Unsupported currency | `JPY` (P0999) |
| Missing field | P0120 has no `currency` key |

FX (foreign exchange) rates to GBP: GBP 1.00, EUR 0.85, USD 0.79.

## Task

1. **Complete `starter_payment_utils.py`.**
   1. Define `PaymentError(Exception)`, and `InvalidAmountError` and `UnsupportedCurrencyError`,
      both subclasses of `PaymentError`.
   2. `parse_amount(text: str) -> float`: if `text` is not a `str`, raise `TypeError` yourself
      (type hints are not enforced at runtime). Strip whitespace, one leading `£`, `€` or `$`,
      and all commas, then call `float()`, which raises `ValueError` for anything still not a
      number. Raise `InvalidAmountError` if the result is zero or negative.
   3. `to_gbp(amount: float, currency: str, rates: dict[str, float] | None = None) -> float`:
      use `DEFAULT_RATES` when `rates` is `None`; raise `UnsupportedCurrencyError` for a
      currency with no rate. In a comment, explain why `rates={}` as the default would be a bug.
   4. `card_fee(amount_gbp: float, *, rate: float = 0.015, minimum: float = 0.20) -> float`:
      the fee is `rate * amount_gbp` rounded to 2 decimal places, but never less than
      `minimum`. The bare `*` makes `rate` and `minimum` keyword-only. Confirm that
      `card_fee(10.0, 0.02)` raises `TypeError` and write down why that is a good thing.
   5. `process_transaction(txn: dict) -> float`: call `parse_amount` and `to_gbp` and return the
      GBP amount. Convert a `KeyError`, a `TypeError`/`ValueError` from the amount, or any
      `PaymentError` subclass into a `PaymentError` whose message starts with the `txn_id`,
      using `raise PaymentError(...) from e`.
   6. Add a module docstring, a docstring on every function, and an `if __name__ == "__main__":`
      block with one example call per function.
2. **Rewrite the loop in `starter_process_payments.py`.** Import from your module. Inside the
   loop, call `parse_amount` and `to_gbp` directly (not `process_transaction`) in a `try`, with
   these `except` clauses in this order:
   - `(TypeError, ValueError)`: bad amount format
   - `UnsupportedCurrencyError`
   - `InvalidAmountError`
   - `KeyError`: missing field

   Each prints a message naming the `txn_id` and increments a count in a `failures` dict keyed
   by reason. Use `else` to compute the card fee and add to the GBP and fee totals; use
   `finally` to increment a `processed` counter. After the loop, print the processed count, the
   totals and the `failures` dict.
3. **Exception chaining.** Call `process_transaction` on P0999 and on P0120. Catch the base
   `PaymentError` and print the message, the type of `e.__cause__` and `e.__cause__` itself.
4. **Ordering question.** Answer in a comment: if one `try` had both `except PaymentError` and
   `except UnsupportedCurrencyError`, why must the `PaymentError` clause come last?

## Acceptance criteria

- `python starter_payment_utils.py` prints only the output of its `__main__` block, and
  importing the module prints nothing.
- The processing script runs to completion: 12 records processed, 7 succeeded.
- Totals: GBP 3,011.79 processed, fees GBP 45.45. Small amounts (P0015, P0134) are charged the
  GBP 0.20 minimum.
- Failure counts: bad format 2 (P0048, P0057), unsupported currency 1 (P0999), invalid amount 1
  (P0061), missing field 1 (P0120).
- `None` is reported as a `TypeError` raised by `parse_amount`, not as an `AttributeError`.
- The chaining step prints `P0999: no FX rate for JPY` with `__cause__` of type
  `UnsupportedCurrencyError`, and `P0120: missing field 'currency'` with a `KeyError` cause.
- No bare `except:` and no `except Exception:` anywhere.

## Extension exercises

1. **Exceptions that carry data.** Give `PaymentError` an `__init__(self, message, *, txn_id=None,
   reason=...)` that stores `txn_id` and `reason` as attributes (call `super().__init__(message)`).
   Raise every error with its reason, then rebuild the failure summary with a single
   `except PaymentError as e` that uses `e.reason` and `e.txn_id`. Done when the summary lists
   each reason with its count and the `txn_id`s, and matches the core counts.
2. **Logging.** Replace `print` in the processing loop with the `logging` module: `INFO` for each
   processed transaction, `WARNING` for each skipped one, and a format that shows the level and
   the message (`logging.basicConfig(format="%(levelname)-7s %(message)s", ...)`). Done when
   raising the level to `WARNING` hides the `INFO` lines without changing any logging call.
3. **Self-test with `assert`.** Write `self_test()` that checks the happy paths of every function
   and also that specific inputs raise specific exceptions (`None` gives `TypeError`, `"12.5.0"`
   gives `ValueError`, `"-5.00"` gives `InvalidAmountError`, `JPY` gives
   `UnsupportedCurrencyError`, a positional `rate` gives `TypeError`). Done when it prints one
   success line, and fails loudly if you break any rule on purpose. Module 12 replaces this with
   pytest.
4. **Money as `Decimal`.** Show that `0.1 + 0.2 == 0.3` is `False` and what 1,000 additions of
   `0.10` give as a float. Then write `to_gbp_decimal` using `decimal.Decimal` rates built from
   strings, quantised to `Decimal("0.01")` with `ROUND_HALF_UP`. Done when you can show one
   amount where float `round()` and `Decimal` half-up rounding give different pennies (hint: the
   fee on GBP 1,249.00).
