# Module 2 Lab — Functions, Modules & Error Handling

## Objectives

By the end of this lab you will have:

- Written and called functions, including one with a default keyword argument
- Split code across two files using `import`
- Added `try`/`except` error handling for malformed records
- Refactored a working script without changing its behaviour for well-formed input

## Setup

- Python 3.11+, no external libraries
- Starter files: `starter_math.py` (empty module for your functions) and
  `starter_summary.py` (the script to refactor, containing Module 1's inline logic plus one
  deliberately malformed trade record)

## Task

1. In `starter_math.py`, write two functions:
   - `trade_value(quantity, price)` — returns `quantity * price`
   - `classify_trade(value, threshold=20000)` — returns `"large"` if `value > threshold`,
     otherwise `"normal"`
2. In `starter_summary.py`, `import` both functions from `starter_math` and use them in place of
   the inline calculation and inline threshold check.
3. Wrap the value calculation in a `try`/`except TypeError` block so a malformed trade record
   (where `quantity` is a string like `"N/A"`) is skipped with a clear message, instead of
   crashing the whole script.
4. Confirm the running total and per-trade output still match what Module 1's version produced,
   for every well-formed trade.

## Acceptance criteria

- `starter_math.py` and `starter_summary.py` both run, with `starter_summary.py` importing from
  `starter_math.py`.
- The malformed trade record is skipped with a printed message, not a crash.
- `classify_trade` is called at least once using the keyword form with a non-default threshold
  (for example `classify_trade(value, threshold=50000)`), to show you understand keyword
  arguments, not just positional ones.
- No bare `except:` — catch `TypeError` specifically.
