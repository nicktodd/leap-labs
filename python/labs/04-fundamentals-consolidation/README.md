# Module 4 Lab - Extended Exercise: Card Fraud Screening Tool

This is a bigger exercise than Modules 1-3: a small command-line tool, not a single script.
Budget more time for it than for earlier labs. It draws on everything from this week so far
(control flow, functions, data structures, file I/O and error handling), applied together
rather than one at a time.

## Scenario

PaySprint's fraud team confirms fraud cases by hand after customers complain. It wants a first
automated screen: a command-line tool that reads a month of card transactions, applies four
simple rules, and writes a report the team can read in the morning. Because the team already
knows which February transactions were fraud, the report must also say how well the rules did:
how many flags were right, how many were false alarms, and which fraud cases got through.

## Objectives

By the end of this lab you will have:

- Built a command-line tool with `argparse`, with defaults and typed options, instead of a
  script with hardcoded values
- Applied several independent business rules, including one that needs reference data from a
  second file and one that needs a count per customer per day
- Parsed timestamps with `datetime.strptime` and used the parsed value (hour, date)
- Handled malformed records without crashing, using what you learned in Module 2
- Written a report to a file and to the console from one function
- Measured your rules against known outcomes, and found where they fail
- Explained every function you wrote to a partner, and reviewed theirs in return

## Setup

- Python 3.11+, no external libraries (`argparse`, `csv`, `datetime` and `pathlib` are in the
  standard library)
- Starter file: `starter_fraud_screen.py`, in `labs/04-fundamentals-consolidation/`. Save your
  finished tool as `fraud_screen.py`.
- Run it from any folder: `python fraud_screen.py` uses the defaults below;
  `python fraud_screen.py --help` lists the options.

## The data

- `shared/transactions.csv`: 140 card transactions, 2 Feb to 1 Mar 2026. Columns used here:
  `txn_id`, `txn_timestamp` (`YYYY-MM-DD HH:MM`), `customer_id`, `merchant`, `channel`
  (`Online`, `In-store`, `Contactless`), `country` (ISO (International Organization for
  Standardization) country code), `currency` (GBP, EUR (euro) or USD (US dollar)), `amount` and `is_fraud` (1 if the fraud team
  confirmed the transaction as fraud, else 0).
- `shared/customers.csv`: one row per customer, including `home_country`.
- `shared/fx_rates.csv`: FX (foreign exchange) rates to GBP (pounds sterling).
  `amount_gbp = amount * rate_to_gbp`.
- `shared/messy-transactions-raw.csv`: a raw export of the same month with formatting problems.
  Use it to test your error handling, not as your main input.

## The brief

Build `fraud_screen.py`, a command-line tool that reads a transactions CSV, flags transactions
and customer-days against four rules, evaluates the rules against `is_fraud`, and writes a
report.

### Command-line interface

| Argument | Default | Meaning |
|---|---|---|
| `--input` | `shared/transactions.csv` | transactions CSV to screen |
| `--customers` | `shared/customers.csv` | customer reference data |
| `--fx` | `shared/fx_rates.csv` | FX rates to GBP |
| `--report` | `output/fraud_report.txt` | report file, in an `output/` folder next to the script |
| `--high-value` | `500` | GBP amount above which a transaction is `HIGH_VALUE` |
| `--velocity` | `3` | transactions on one calendar day at or above which a customer-day is flagged `VELOCITY` |

Build the default paths from `Path(__file__)` so the tool works from any folder.

### Rules

1. **HIGH_VALUE**: `amount_gbp > high_value`.
2. **FOREIGN**: the transaction `country` differs from the customer's `home_country` in
   `customers.csv`. Compare with the customer's home country, not with `GB`: some customers live
   in France or Ireland. A customer who is missing from `customers.csv` gets the flag
   `UNKNOWN_CUSTOMER` instead, and the tool must not crash.
3. **NIGHT_ONLINE**: `channel == "Online"` and the hour is 00:00 to 04:59.
4. **VELOCITY**: per customer per calendar day, the number of transactions is `>= velocity`.
   This is a flag on a customer-day, not on a transaction: report each qualifying customer-day
   once, with its count.

A transaction can have several flags. Parse `txn_timestamp` with
`datetime.strptime(text, "%Y-%m-%d %H:%M")`.

### Handling malformed records

Skip a row, print a warning naming its `txn_id` and the reason, and continue, when:

- `amount` cannot be converted with `float()`
- `txn_timestamp` is not in the expected format (or is not a real date)
- `currency` has no rate in the FX file

The tool must never crash on bad input. Do not repair values in this version: that is
Extension 2.

### The report

Write a plain-text report to the `--report` path and print the same text to the console, both
from one function. It contains:

- The number of transactions processed and the number skipped, with each skipped `txn_id` and
  its reason
- Every flagged transaction on one line: `txn_id`, customer, timestamp, merchant, GBP amount and
  its flags
- Every `VELOCITY` customer-day on one line: customer, date and count
- A rule evaluation using `is_fraud`, for the transaction flags (HIGH_VALUE, FOREIGN,
  UNKNOWN_CUSTOMER, NIGHT_ONLINE): how many flagged transactions are fraud, how many are false
  alarms, and how many fraud transactions have no flag (list their `txn_id`s)

## Suggested structure

You decide the function breakdown, but a `fraud_screen.py` with one large function will be
hard for your partner to review. The starter suggests:

- `load_rates(path)`, `load_customers(path)`: small readers that return lookup dicts (Module 3)
- `parse_row(row, rates)`: converts one row, raising `ValueError` with a reason if it is bad
- `read_transactions(path, rates)`: returns `(transactions, skipped)`, catching the
  `ValueError` from `parse_row` (Module 2)
- `check_high_value`, `check_foreign`, `check_night_online`: one rule each
- `build_flags(...)`, `find_velocity(...)`, `evaluate(...)`
- `build_report(...)` returning a list of lines, and `write_report(path, lines)`
- `build_parser()` and `main()`, guarded by `if __name__ == "__main__":`

The demo's `flag_clients()` counted per customer with one dict. `find_velocity` needs a count
per customer per day: think about what the dict key should be.

## Using GenAI on this lab

GitHub Copilot Chat remains a learning aid, with the same rules as every earlier week: it is
fine to ask it to explain an error, suggest a cleaner way to write something, or check for
missed edge cases. It is not fine to ask it to write the tool for you and submit code you cannot
explain. Your partner review (below) asks you to walk through your own functions: code you
cannot explain does not pass, whether or not it runs.

A useful prompt for this lab: paste your `check_foreign` function and ask *"What inputs would
make this function crash or return the wrong answer?"*. Then decide for yourself which of the
answers apply to this data.

## Pairing step

Once your tool runs cleanly against both CSV files:

1. Pair up with a partner.
2. Walk them through your `parse_row()` and `read_transactions()` functions and your
   malformed-row handling.
3. Swap: have them run your tool against both files and compare their report with yours for
   `shared/transactions.csv`. The flags should match exactly: the rules are not a matter of
   opinion.
4. Note anywhere your reports disagree, and work out which of you has a bug.
5. Together, look at the false alarms. Pick two and write one sentence each on why the rule
   fired and what extra information would have cleared the transaction.

## Acceptance criteria

- `python fraud_screen.py` runs with the default arguments against `shared/transactions.csv`,
  with no errors, and writes `output/fraud_report.txt`.
- Against `shared/transactions.csv`: 140 processed, 0 skipped, 33 flagged transactions, and 5
  `VELOCITY` customer-days (K002 on 4 Feb, K004 on 17 Feb, K008 on 1 Mar, K009 on 12 Feb with 4
  transactions, K011 on 1 Mar).
- P0016 is flagged `HIGH_VALUE, FOREIGN, NIGHT_ONLINE`. K003's EUR spend in France is not
  flagged `FOREIGN`. Every K012 transaction is flagged `UNKNOWN_CUSTOMER` (10 of them).
- Rule evaluation: 12 of the 33 flagged transactions are fraud, 21 are false alarms, and no
  fraud transaction is left without a flag.
- Against `shared/messy-transactions-raw.csv` the tool does not crash, and skips 23 rows with a
  warning naming each `txn_id` (amounts such as `£123.09` and `TBC`, timestamps such as
  `04-Feb-2026 17:39`, and the impossible date `2026-02-29 09:35`).
- The report file and the console output are identical, because one function produces both.
- Changing `--high-value` or `--velocity` on the command line changes the result without editing
  the code.
- You can explain every function in your solution to a partner, unprompted.

## Extension exercises

1. **JSON report.** Add `--format text|json` (default `text`). With `json`, write the same
   content as a JSON file with `json.dump(..., indent=2)`. Done when the file loads back with
   `json.load` and contains the processed count, the skipped rows, the flagged transactions with
   their flags, the velocity customer-days and the evaluation. You will need to decide what to do
   with `datetime` values and with a dict whose keys are tuples: `json.dump` accepts neither.
2. **Tolerant parsing.** Accept the `DD-Mon-YYYY HH:MM` timestamp format (`%d-%b-%Y %H:%M`) as
   well as the standard one, and parse amounts with currency symbols and thousands separators by
   reusing `parse_amount` from your Module 2 `payment_utils.py` (copy the module next to your
   tool and import it). Done when you can show how many fewer rows are skipped on
   `shared/messy-transactions-raw.csv`, which rows are still skipped and why, and which new
   false alarms appear now that more rows get through (look at the `country` column).
3. **Risk score.** Give each transaction a score equal to its number of flags, counting
   `VELOCITY` when the transaction falls on a flagged customer-day. Add `--min-score` (default
   2) and list the transactions at or above it, highest score first, then largest GBP amount.
   Done when you also print, for each score, how many transactions have that score and how many
   of them are fraud, and can say which minimum score you would recommend.
4. **Threshold sweep.** For `HIGH_VALUE` thresholds of 250, 500, 750 and 1,000, print one row
   per threshold with: transactions flagged, fraud caught, false alarms and fraud missed (with
   the missed `txn_id`s). Do it for the HIGH_VALUE rule on its own and for all the transaction
   rules together. Done when you can explain the trade-off the table shows. Module 13 gives these
   quantities their names (precision and recall).
