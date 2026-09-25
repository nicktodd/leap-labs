# Module 3 Lab - Python Data Structures & File I/O

## Scenario

PaySprint's customer-service team wants a one-page view of each cardholder's February activity:
how many transactions, how much approved spend in GBP (pounds sterling), their largest purchase
and how many kinds of merchant they use. The fraud team separately wants the declined
transactions as a JSON (JavaScript Object Notation) file it can load into its case tool. Both
must be built with the Python standard library only, reading the FX (foreign exchange) rates
from a file rather than hardcoding them.

## Objectives

By the end of this lab you will have:

- Read two CSV (comma-separated values) files with `csv.DictReader`, and turned one of them
  into a lookup dict
- Built nested structures: a dict of lists and a dict of sets, using `dict.setdefault`
- Used a set of tuples, and explained why a tuple can be a set member and a list cannot
- Used `max()` and `sorted()` with a `key=lambda` to pick and order records by a computed value
- Written a CSV file with `csv.DictWriter` and a JSON file with `json.dump`, using `with` for
  every file handle

## Setup

- Python 3.11+, no external libraries (`csv`, `json` and `pathlib` are in the standard library)
- Starter file: `starter_customer_activity.py`, in `labs/03-data-structures-file-io/`
- Run it with `python starter_customer_activity.py` from any folder: paths are built from
  `Path(__file__)`, and output files go into an `output/` folder next to the script

## The data

- `shared/fx_rates.csv`: `currency, rate_to_gbp` (GBP 1.00, EUR (euro) 0.85, USD (US dollar) 0.79).
  `amount_gbp = amount * rate_to_gbp`.
- `shared/transactions.csv`: 140 card transactions, 2 Feb to 1 Mar 2026. The columns you need
  are `txn_id`, `customer_id`, `customer_name`, `merchant`, `merchant_category`, `channel`,
  `currency`, `amount` and `status` (`APPROVED` or `DECLINED`).
- `shared/customers.csv` (Extension 3 only): one row per customer with `credit_limit_gbp`.

Every value that `csv.DictReader` returns is a `str`, including `amount` and `rate_to_gbp`.

## Task

1. **FX rates as a dict.** Read `fx_rates.csv` with `csv.DictReader` inside a `with` block and
   build `rates`, a dict of currency to `float`. Print it.
2. **Transactions as a list of dicts.** Read `transactions.csv` the same way. Add an
   `amount_gbp` key (a `float`) to each row using `rates`, and append the row to a list. Keep full
   precision: round only when you display or write a value. Print the number of rows.
3. **Dict of lists.** Build `txns_by_customer: dict[str, list[dict]]` mapping each
   `customer_id` to the list of that customer's transactions, using
   `txns_by_customer.setdefault(customer_id, []).append(txn)`. Print the number of customers.
4. **Dict of sets.** Build `categories_by_customer: dict[str, set[str]]` mapping each
   `customer_id` to the set of `merchant_category` values they have spent in.
5. **Consistency check.** Build a dict of sets mapping each `merchant` to the categories it
   appears under. Every merchant should map to exactly one category. Print either the
   inconsistent merchants or a confirmation that includes the number of merchants.
6. **Tuples in a set.** Build a set of `(merchant, merchant_category)` tuples and print how many
   distinct pairs there are. Then try to put a list `["Tesco", "Groceries"]` into a set inside
   `try`/`except TypeError` and print the error message. In a comment, explain the difference.
7. **Per-customer summary.** For each customer build a dict with the keys `customer_id`,
   `customer_name`, `txn_count` (all transactions), `total_gbp` (APPROVED transactions only,
   rounded to 2 decimal places), `largest_txn_gbp` (the largest APPROVED transaction in GBP,
   found with `max(..., key=lambda t: ...)`) and `distinct_categories` (the size of the set from
   Task 4). Sort the rows by `total_gbp`, largest first, with `sorted(..., key=..., reverse=True)`
   and print them as an aligned table.
8. **CSV output.** Write the summary rows to `output/customer_summary.csv` with `csv.DictWriter`
   (header row plus one row per customer). Open the file with `newline=""` and write plain
   numbers, not display-formatted text such as `2,632.04`.
9. **JSON output.** Write every DECLINED transaction (all its fields, with `amount_gbp` rounded
   to 2 decimal places) to `output/declined.json` with `json.dump(..., indent=2)`.

The demo accumulated one running total per key. Here the values in your dicts are themselves
collections, and the sort and the maximum use a value you compute, not a field from the file.

## Acceptance criteria

- The script runs from any folder with no errors and uses `with` for every file it opens.
- `rates` prints as `{'GBP': 1.0, 'EUR': 0.85, 'USD': 0.79}` (floats, not strings).
- 140 transactions, 12 customers, all 18 merchants map to exactly one category, 18 distinct
  (merchant, category) pairs.
- The first rows of your table: K006 Farah Siddiqui (11 transactions, GBP 2,632.04, largest
  2,145.31, 5 categories), then K004 Daniel Price (19, GBP 2,002.88, largest 652.38, 7). The last
  row is K005 Eilidh Murray (GBP 164.98).
- The approved totals of all 12 customers add up to GBP 11,471.55.
- `output/customer_summary.csv` has a header and 12 rows, and its `total_gbp` column contains
  values such as `2632.04` (no commas).
- `output/declined.json` is a JSON list of 13 objects, the first being P0016.

## Extension exercises

1. **Set operations.** Using one set of customer IDs per question and the operators `&` and `-`,
   print: the customers who have used both the Online and the In-store channel (intersection);
   the customers with no declined transactions (all customers minus those with a decline); and
   the merchants used by exactly one customer. Done when each answer is a sorted list produced
   by a set expression, with no nested loops.
2. **`defaultdict` and `Counter`.** Rewrite the Task 3 grouping with
   `collections.defaultdict(list)` and confirm it gives the same dict. Show what happens to a
   `defaultdict` when you read a key that is not there. Use `Counter` to print the top 3 merchants
   by transaction count with `most_common(3)`. Done when you can state one situation where the
   plain dict with `setdefault` is the safer choice.
3. **Join to reference data.** Read `shared/customers.csv` into a dict keyed by `customer_id`.
   For each customer, print approved February spend as a percentage of `credit_limit_gbp`,
   sorted highest first. One customer in the transactions is missing from `customers.csv`: use
   `.get()` so the script reports that customer with a warning instead of raising `KeyError`.
   Done when the table has 11 rows plus one warning line.
4. **Round trip.** Read `output/customer_summary.csv` back with `csv.DictReader`, convert the
   values and check that every customer's `txn_count` and `total_gbp` match the in-memory summary
   rows, and that the grand totals agree. Then write the totals with `f"{x:,.2f}"` to a second
   CSV file, read it back and show what `float()` does with the result. Done when you can explain
   in a comment why a CSV file meant for another program should hold plain numbers.
