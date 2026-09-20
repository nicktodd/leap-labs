# Module 1 Lab - Python Fundamentals: Syntax, Data Types & Control Flow

## Objectives

By the end of this lab you will have:

- Used core Python data types (`str`, `int`, `float`, `bool`) correctly
- Used `if`/`elif`/`else` and a `for` loop to process a collection of records
- Written and run a short Python script from the command line
- Produced simple summary output from a list of trade records

## Setup

- Python 3.11+ installed and on your PATH
- No libraries required - plain Python only

## Task

Starter file: `starter_trades.py`. It contains a plain Python list of trade record dictionaries
(same shape as the demo). Write a script that:

1. Iterates over the trades list.
2. For each trade, computes `value = quantity * price`.
3. Flags any trade where `value` is greater than 20,000 as a "large trade" (print a message
   naming the trade).
4. Prints an overall summary: total number of trades, total value across all trades, and the
   count of BUY trades vs. SELL trades.

## Acceptance criteria

- The script runs with `python your_script.py` and produces no errors.
- Every trade over 20,000 in value is flagged individually.
- The final summary correctly reports total trade count, total value, and the BUY/SELL split.
- Only core Python syntax is used (no `import pandas` or similar) - that comparison comes in
  Module 5.
