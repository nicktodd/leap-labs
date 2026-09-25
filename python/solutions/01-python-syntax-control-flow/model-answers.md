# Module 1 Lab - Model Answer Notes

See `payments.py` for the core solution and `ext1_currency_lookup.py` to
`ext4_for_else_budget.py` for the extensions.

## Verified results

Output of `python payments.py`:

- First transaction: `txn_id`, `merchant` and `currency` are `str`, `amount` is `float`,
  `is_approved = True (bool)`.
- P0999 prints `WARNING: P0999 has unsupported currency JPY; skipped` and nothing else.
- Bands: micro P0003, P0015, P0026, P0043, P0044; standard P0001, P0020, P0037; high P0016
  (GBP 1,259.74), P0034, P0057 (GBP 652.38), P0100 (GBP 1,202.97).
- Approved total GBP 2,303.35; declined 2 (P0016, P0037); Online 6, Contactless 4, In-store 2.
- Largest approved: P0100, GBP 1,202.97. (P0016 is larger at GBP 1,259.74 but DECLINED.)
- Budget GBP 200.00: 5 approved transactions fit (GBP 151.68); P0034 (GBP 293.81) would take
  spend to GBP 445.50.

## Key points to check in a delegate's solution

- **The `continue` comes before any accumulation.** If the currency check happens after the
  counters are incremented, P0999 is counted as an In-store transaction (In-store 3 instead of 2).
- **The band chain tests upper bounds in ascending order.** `if amount_gbp < 10 ... elif
  amount_gbp < 250` works because the first true branch wins. Writing
  `elif amount_gbp >= 10 and amount_gbp < 250` is correct but redundant; testing `< 250` first
  would put every micro transaction in `standard`.
- **Bands and the largest transaction use the GBP amount, not `amount`.** Using the raw amount
  makes P0016 (USD 1,594.61) and P0100 (USD 1,522.75) look larger than they are, and would rank
  a EUR amount against a GBP amount as if they were the same unit.
- **The largest-so-far check handles the first record.** Either start from `None` and test for
  it, or start from `0.0`. Starting from the first transaction's amount without checking its
  status is a subtle bug: P0001 is approved here, but that is luck.
- **The largest approved is P0100, not P0016.** A delegate who reports P0016 has not filtered
  on status.
- **The `while` loop's condition carries the stopping rule** and it also guards the index
  (`i < len(approved)`), so the loop cannot run off the end of the list if the budget is never
  reached. A `while True` with `break` is acceptable if the index guard is present.
- **`is_approved` is computed with `==`**, not written as the literal `True`.

## Extension notes

**E1 - Dict lookup.** Output matches the core run (approved total GBP 2,303.35). The point to
look for is the comment on the trade-off: `.get(currency, 1.0)` would quietly treat JPY 4,500 as
GBP 4,500.00, which the extension prints to make the risk visible. A dict makes the rates data
(easy to extend, easy to load from a file in Module 3), while the `if` chain makes them code.
Delegates who use `RATES_TO_GBP[currency]` without a membership check get a `KeyError` on P0999,
which previews Module 2.

**E2 - Aligned table.** Header and rows use the same widths. Amounts are right-aligned with
`>10,.2f`, so `1,259.74` and `4.63` line up on the decimal point. P0999 shows a short
"unsupported currency JPY" note in place of its amount. The table total is GBP 3,635.49 because
it includes declined transactions; delegates should label such a total clearly.

**E3 - Consecutive repeats.** One pair: Ibrahim Yusuf, P0043 then P0044 at Amazon (GBP 1.50 then
GBP 1.00). These are the card-testing transactions in the full dataset: a fraudster confirms a
stolen card works with tiny payments before a large attempt (P0045 in `shared/transactions.csv`).
Check that `previous = txn` is the last statement in the loop body; updating it before the
comparison compares each record with itself. A delegate may reasonably ask whether "consecutive"
should mean the same customer's previous transaction anywhere in the list; that needs a dict
keyed by customer, which is Module 3.

**E4 - `for ... else`.** GBP 200 gives the same answer as Task 6 (5 fitted, GBP 151.68, P0034
breaches). GBP 5,000 runs the `else` branch: all 10 approved transactions fit, GBP 2,303.35.
The common misunderstanding is that `else` runs when the loop body's `if` is false; it runs when
the loop ends without `break`. The solution wraps the loop in a function so it can be called
twice; a delegate who duplicates the loop is fine at this stage (functions are Module 2).
