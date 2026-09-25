# Module 2 Lab - Model Answer Notes

See `payment_utils.py` and `process_payments.py` for the core solution, and
`ext1_error_attributes.py` to `ext4_decimal_money.py` for the extensions. Run everything from
any folder; the extension files import `raw_transactions` from `process_payments.py`, whose
loop sits behind a `__main__` guard for that reason.

## Verified results

`python payment_utils.py` prints `1249.0`, `85.0`, `90.0`, `0.2`, `10.0` and
`122.33199999999998` (float noise on EUR 143.92, picked up again in Extension 4).

`python process_payments.py`:

- 12 processed, 7 succeeded: P0001, P0002, P0015, P0016, P0034, P0098, P0134.
- Total GBP 3,011.79, total fees GBP 45.45. P0015 (GBP 5.05) and P0134 (GBP 2.91) pay the
  GBP 0.20 minimum fee.
- Failures: `{'bad format': 2, 'unsupported currency': 1, 'invalid amount': 1, 'missing field': 1}`
  - P0048 `'12.5.0'`: `ValueError` from `float()`
  - P0057 `None`: `TypeError` raised by `parse_amount` ("amount must be a str, got NoneType")
  - P0061 `'-5.00'`: `InvalidAmountError` ("amount must be positive, got -5.0")
  - P0999 `JPY`: `UnsupportedCurrencyError`
  - P0120: `KeyError: 'currency'`
- Chaining: `PaymentError: P0999: no FX rate for JPY` with `__cause__` of type
  `UnsupportedCurrencyError`; `PaymentError: P0120: missing field 'currency'` with a `KeyError`
  cause.

## Key points to check in a delegate's solution

- **The hierarchy is real inheritance.** `InvalidAmountError(PaymentError)`, not
  `InvalidAmountError(Exception)`. Test it: `isinstance(InvalidAmountError("x"), PaymentError)`
  must be `True`, otherwise `process_transaction`'s `except PaymentError` misses it.
- **`parse_amount` checks the type first.** Without the `isinstance` check, `None` fails on
  `.strip()` with an `AttributeError`, which none of the `except` clauses catch, so the script
  crashes on P0057.
- **Only one leading symbol is removed, and commas are removed before `float()`.** `"12.5.0"`
  must still reach `float()` and fail there; a delegate who strips all dots "to be safe" turns
  it into `1250`.
- **The mutable default question.** A default value is evaluated once, when `def` runs. With
  `rates={}` every call that omits `rates` shares the same dict object, so any code that writes
  into it (for example caching a rate) changes the default for all later calls. `None` plus
  `if rates is None:` creates a fresh choice per call.
- **Keyword-only arguments.** `card_fee(10.0, 0.02)` raises `TypeError: card_fee() takes 1
  positional argument but 2 were given`. Two adjacent floats are easy to swap; forcing
  `rate=` makes the call site self-describing.
- **`else` accumulates, `finally` counts.** Accumulating in `finally` runs for failed records
  too: `amount_gbp` still holds the previous record's value, so each failure silently adds the
  last good amount again (a `NameError` only if the very first record fails). Counting
  `processed` in `else` would give 7, not 12.
- **The `(TypeError, ValueError)` clause comes first but does not hide the domain errors**,
  because `InvalidAmountError` and `UnsupportedCurrencyError` inherit from `PaymentError`, not
  from `ValueError`. A delegate who makes `InvalidAmountError(ValueError)` will see P0061 counted
  as "bad format": a good discussion point about choosing base classes.
- **`raise ... from e`, and `e.__cause__`.** `from e` sets `__cause__`; the traceback then shows
  both exceptions with "The above exception was the direct cause of the following exception".
- **Ordering answer.** `except` clauses are tested top to bottom and the first match wins. Every
  `UnsupportedCurrencyError` is a `PaymentError`, so a `PaymentError` clause placed first
  catches it and the specific clause becomes unreachable.
- **No output on import.** `from payment_utils import ...` must print nothing.

## Extension notes

**E1 - Exceptions that carry data.** Output: total GBP 3,011.79, then `bad format: 2 (P0048,
P0057)`, `invalid amount: 1 (P0061)`, `unsupported currency: 1 (P0999)`, `missing field: 1
(P0120)`. The `__init__` must call `super().__init__(message)` so `str(e)` still works. Look for
keyword-only `txn_id`/`reason` and for the re-raise keeping the inner error's `reason` rather
than overwriting it with a generic one. The payoff is one `except` clause instead of four.

**E2 - Logging.** Seven `INFO` lines, five `WARNING` lines (for example `WARNING skipped P0048:
bad amount format (could not convert string to float: '12.5.0') [cause: ValueError]`), then
`INFO done: total GBP 3011.79, 5 skipped`. After `log.setLevel(logging.WARNING)` an `info` call
prints nothing. Check that delegates use `%s` arguments (`log.info("processed %s", txn_id)`)
rather than f-strings; both work, but the `%s` form defers formatting until the level check
passes. `basicConfig` only takes effect the first time it is called.

**E3 - Self-test.** Prints `self_test: all checks passed`. Look for: float comparisons using a
tolerance where arithmetic is involved (`to_gbp(143.92, "EUR")` is `122.33199999999998`, not
`122.332`), an `expect_raises` helper (or `try/except/else`) so that "did not raise" is itself
a failure, and at least one check that the helper can fail. A bare `try: ... except: pass` test
proves nothing. `pytest.raises` in Module 12 is the same idea.

**E4 - Decimal.** Verified output: `0.1 + 0.2` is `0.30000000000000004`; 1,000 float additions of
`0.10` give `99.9999999999986`, the `Decimal` version gives `100.00`. EUR 143.92 converts to
`122.33` and USD 1,594.61 to `1259.74`. The fee on GBP 1,249.00 is exactly 18.735: float
`round()` gives `18.73` (the stored float is slightly below 18.735) while `ROUND_HALF_UP` gives
`18.74`. Common pitfall: `Decimal(0.85)` copies the float's binary error
(`0.84999999999999997779...`); build Decimals from strings.
