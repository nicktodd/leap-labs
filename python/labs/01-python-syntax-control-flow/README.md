# Module 1 Lab - Python Fundamentals: Syntax, Data Types & Control Flow

## Scenario

PaySprint runs a card-payments business alongside its trading platform. Before any tooling is
built, the payments team wants a plain-Python script that walks through a small sample of card
transactions, converts each one to GBP (pounds sterling), sorts it into an amount band and
produces a short summary. One record in the sample is in a currency PaySprint does not support
yet, and the script must deal with it without stopping.

## Objectives

By the end of this lab you will have:

- Inspected core Python data types (`str`, `float`, `bool`) and computed a `bool` from a comparison
- Written `if`/`elif`/`else` chains where the order of the conditions matters
- Used `continue` to skip a record inside a `for` loop
- Accumulated totals, counters and a running maximum by hand, without built-in helpers
- Used a `while` loop for a stopping condition that is not known before the loop starts

## Setup

- Python 3.11+ installed and on your PATH
- No libraries and no imports: plain Python only
- Starter file: `starter_payments.py`, in `labs/01-python-syntax-control-flow/`
- Run it with `python starter_payments.py`

## The data

The starter file contains a list called `transactions`: 13 dicts, 12 copied from
`shared/transactions.csv` plus one extra record (P0999, in JPY, Japanese yen). Each dict has:

| Key | Type | Meaning |
|---|---|---|
| `txn_id` | str | transaction identifier, e.g. `P0001` |
| `customer_name` | str | cardholder |
| `merchant` | str | where the card was used |
| `channel` | str | `Online`, `Contactless` or `In-store` |
| `currency` | str | currency of `amount`: `GBP`, `EUR`, `USD` (and one `JPY`) |
| `amount` | float | amount in `currency` |
| `status` | str | `APPROVED` or `DECLINED` |

FX (foreign exchange) rates to GBP: GBP 1.00, EUR 0.85, USD 0.79. `amount_gbp = amount * rate`.

## Task

Write your code in the starter file (or a copy of it). Do not use `max()`, `sum()`, dicts of
counters or any imports: the point of this lab is to do the bookkeeping yourself.

1. **Types.** For the first transaction, print `txn_id`, `merchant`, `currency` and `amount`
   together with the name of each value's type (`type(x).__name__`). Then compute
   `is_approved = <comparison of status with "APPROVED">` and print it with its type.
2. **Currency conversion.** Loop over `transactions` with a `for` loop. Convert `amount` to GBP
   with an `if`/`elif`/`else` chain on `currency`. In the `else` branch, print a warning that
   names the `txn_id` and the currency, then `continue` to the next record.
3. **Amount band.** In the same loop, classify the GBP amount with `if`/`elif`/`else`:
   `"micro"` if under 10, `"standard"` if under 250, otherwise `"high"`. Print one line per
   transaction showing `txn_id`, merchant, channel, status, GBP amount (2 decimal places) and band.
4. **Totals and counters.** Still in the same loop, accumulate: the total GBP value of APPROVED
   transactions, the number of DECLINED transactions, and a count per channel using three
   separate counter variables (dicts arrive in Module 3). Print them after the loop.
5. **Largest approved.** Track the largest APPROVED transaction (its `txn_id` and GBP amount)
   by comparing each record with the largest seen so far. Print it after the loop.
6. **Budget check with `while`.** A customer-service tool needs to know how many approved
   transactions, taken in list order, fit inside a GBP 200 budget. Write a `while` loop that
   adds approved GBP amounts until the next one would take cumulative spend over
   `BUDGET_GBP`, then stops. Print how many transactions fitted, the cumulative spend, and the
   `txn_id` that would have breached the budget. Hint: during Task 4, append each approved
   record (with its GBP amount stored on it) to a list, then loop over that list.

   The demo used `while` with a simple counter, which a `for` loop does better. Here the loop
   stops at a point you cannot know before it starts, which is the case `while` is for.

## Acceptance criteria

- The script runs with `python starter_payments.py` and produces no errors.
- P0999 produces exactly one warning line and does not appear in any total or count.
- Your summary matches these values: approved total GBP 2,303.35; 2 declined; Online 6,
  Contactless 4, In-store 2; largest approved P0100 at GBP 1,202.97.
- Five transactions are `micro`, three `standard`, four `high`.
- The budget check reports that 5 approved transactions fit (GBP 151.68) and that P0034
  breaches the GBP 200 budget.
- Each `if`/`elif` chain is ordered so that each branch only tests its upper bound.
- No imports, no `max()`, no `sum()`.

## Extension exercises

1. **Dict lookup for rates.** Replace the currency `if`/`elif`/`else` chain with a dict
   `RATES_TO_GBP` and `.get()`. P0999 must still be skipped with a warning. Done when your
   approved total is unchanged and you have written a comment explaining why
   `RATES_TO_GBP.get(currency, 1.0)` would be a bug.
2. **Aligned table.** Print the transactions as a table with fixed-width columns using format
   specifications, for example `f"{txn_id:<6} {merchant:<15} {amount_gbp:>10,.2f}"`. Done when
   the amounts line up on the decimal point, including the four-digit ones.
3. **Consecutive repeats.** Detect any customer whose transaction is immediately followed, in
   the list, by another transaction from the same customer at the same merchant. Keep the
   previous record in a variable across loop iterations. Done when you print the customer, both
   `txn_id`s and both amounts. Look at what you find: why might a fraud analyst care about it?
4. **`for` with `break` and `else`.** Rewrite the budget check as a `for` loop that uses `break`
   when the budget is exceeded, with a `for ... else` clause that prints a message when the
   budget is never exceeded. Run it with GBP 200 (same answer as Task 6) and with a budget large
   enough that the `else` branch runs.
