# Module 3 Lab — Python Data Structures & File I/O

## Objectives

By the end of this lab you will have:

- Chosen the right data structure (list, tuple, dict, or set) for a given piece of data
- Read `shared/trades.csv` using plain Python and `csv.DictReader` (no pandas)
- Computed a summary using a dict keyed by instrument
- Written the summary to a text file

## Setup

- Python 3.11+, no external libraries — this is plain Python, the same dataset pandas takes
  over from Module 5 onward
- `shared/trades.csv` (repo root) is the file you'll read

## Task

Starter file: `starter_read_trades.py`, in `labs/03-data-structures-file-io/`.

1. Open `shared/trades.csv` with `csv.DictReader` inside a `with open(...) as f:` block, and
   collect all rows into a list of dicts.
2. Build a `dict` keyed by `client_name`, where each value is the running total `value` for that
   client (remember: values from `csv.DictReader` are always strings — convert `value` to
   `float` before summing).
3. Build a `set` of the distinct `advisor` names that appear in the data.
4. Print, for each client (sorted alphabetically), their total trade value.
5. Write the same per-client summary to a text file, `client_summary.txt`, in the same folder as
   your script.

## Acceptance criteria

- The script runs with `python starter_read_trades.py` and produces no errors.
- Every client in `shared/trades.csv` appears exactly once in both the printed output and
  `client_summary.txt`, with a correctly summed total.
- The distinct advisor set is printed and contains no duplicates.
- The file is opened using `with`, both for reading and for writing — no unguarded `open()` calls.
