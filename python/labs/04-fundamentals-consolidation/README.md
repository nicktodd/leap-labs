# Module 4 Lab - Extended Exercise: Trade Compliance Checker

This is a bigger exercise than Modules 1-3: a small command-line tool, not a single script.
Budget more time for it than earlier labs - it deliberately draws on everything from this week
so far (control flow, functions, data structures, file I/O, and error handling), applied
together rather than one at a time.

## Objectives

By the end of this lab you will have:

- Built a command-line tool using `argparse`, not just a script with hardcoded values
- Applied multiple independent business rules to the mission dataset
- Handled malformed records without crashing, using what you learned in Module 2
- Written a clear report to a file, in addition to console output
- Explained every function you wrote to a partner, and reviewed theirs in return

## Setup

- Python 3.11+, no external libraries - `argparse` and `csv` are both in the standard library
- Starter file: `starter_compliance_checker.py`, in `labs/04-fundamentals-consolidation/`
- Data: `shared/trades.csv` (clean) and `shared/messy-trades-raw.csv` (deliberately dirty - used
  to test your error handling, not as your primary input)

## The brief

Build `compliance_checker.py`, a command-line tool that reads a trades CSV and flags trades or
clients against three independent business rules, then writes a report.

### Command-line interface

```bash
python compliance_checker.py --input ../../shared/trades.csv --report report.txt
```

Use `argparse` to support these arguments:

| Argument | Default | Meaning |
|---|---|---|
| `--input` | `shared/trades.csv` | path to the trades CSV to check |
| `--report` | `report.txt` | path to write the report to |
| `--large-threshold` | `20000` | trade value above which a trade is flagged `LARGE` |
| `--high-volume-threshold` | `150` | quantity above which an **Equity** BUY is flagged `HIGH_VOLUME` |
| `--frequency-threshold` | `3` | trade count at or above which a client is flagged `HIGH_FREQUENCY` |

### Business rules

1. **LARGE** - any trade where `value > large_threshold`.
2. **HIGH_VOLUME** - any trade where `asset_class == "Equity"`, `side == "BUY"`, and
   `quantity > high_volume_threshold`. (Bond and Crypto quantities are on a different scale to
   equities - don't apply this rule to them.)
3. **HIGH_FREQUENCY** - any client whose total trade count in the file is
   `>= frequency_threshold`. This is a per-client flag, not a per-trade one: report it once per
   qualifying client, listing their trade count.

### Handling malformed records

Run your tool against `shared/messy-trades-raw.csv` as well as the clean file. It contains rows
with a missing `quantity`, a missing `value`, and a duplicated row. Your tool must skip any row
where `quantity` or `value` can't be converted to a number, print a warning naming the
`trade_id`, and continue processing the rest of the file - it must never crash on bad input.

### The report

Write a plain-text report (`--report` path) containing:

- A count of trades processed, and a count of trades skipped as malformed
- Every `LARGE` and `HIGH_VOLUME` trade, one line each, naming the `trade_id` and the flag(s)
  that applied (a trade can have both)
- Every `HIGH_FREQUENCY` client, one line each, naming the client and their trade count

Print the same summary to the console.

## Suggested structure

You decide the function breakdown, but a `compliance_checker.py` with only one giant function
will be hard for your partner to review. As a guide, aim for functions along these lines:

- `read_trades(path)` - reads the CSV, returns a list of dicts, skipping and warning on malformed
  rows (this is exactly Module 3's file-reading pattern, plus Module 2's error handling)
- `check_large(trade, threshold)`, `check_high_volume(trade, threshold)` - return `True`/`False`
- `count_by_client(trades)` - returns a dict of `client_name -> count` (Module 3's dict-building
  pattern)
- `write_report(path, trades, flags_by_trade, frequent_clients, skipped_count)`
- `main()` - parses arguments and calls the above, guarded by `if __name__ == "__main__":`

## Using GenAI on this lab

GitHub Copilot Chat remains a learning aid, same rules as every earlier week: fine to ask it to
explain an error, suggest a cleaner way to write something, or sanity-check for missed edge
cases; not fine to ask it to write the tool for you and submit code you can't explain. Your
partner review (below) will ask you to walk through your own functions - code you can't explain
doesn't pass, regardless of whether it runs.

## Pairing step

Once your tool runs cleanly against both CSV files:

1. Pair up with a partner.
2. Walk them through your `read_trades()` function and your malformed-row handling, specifically.
3. Swap: have them run your tool against both files and compare their report output to yours for
   `shared/trades.csv` (the flags should match exactly - the rules aren't a matter of opinion).
4. Note anywhere your reports disagree, and work out which of you has a bug.

## Acceptance criteria

- `python compliance_checker.py` runs against `shared/trades.csv` with default arguments, with no
  errors, and produces a report matching the business rules above.
- The same command against `shared/messy-trades-raw.csv` skips malformed rows with a printed
  warning naming the `trade_id`, and does not crash.
- All three business rules are implemented as described, including the asset-class restriction
  on `HIGH_VOLUME`.
- The report file and console output agree with each other.
- You can explain every function in your solution to a partner, unprompted.
