# Module 5 Lab — Pandas Fundamentals: DataFrames & Series

## Objectives

By the end of this lab you will have:

- Loaded `shared/trades.csv` into a pandas DataFrame
- Used `.iloc`, `.loc`, and boolean indexing to select and filter rows
- Used `groupby` to reproduce Module 3's manual per-client summary
- Compared the plain-Python approach (Module 3) with the pandas approach, directly

## Setup

- `pip install pandas`
- `shared/trades.csv` (repo root)

## Task

Starter file: `starter_pandas_intro.py`, in `labs/05-pandas-fundamentals/`.

1. Load `shared/trades.csv` into a DataFrame with `pd.read_csv()`.
2. Using `.loc` and boolean indexing, select only the SELL trades, keeping just the `trade_id`,
   `client_name`, and `value` columns.
3. Reproduce Module 3's per-client value summary using `groupby("client_name")["value"].sum()`.
   Compare the result to your Module 3 output (or the reference solution) for
   `shared/trades.csv` — the numbers must match exactly.
4. Reproduce Module 3's distinct-advisor set using `df["advisor"].unique()`.
5. Print, in one final block: the number of lines your Module 3 solution needed for the
   per-client summary loop, versus the number of lines the pandas `groupby` line needed. Comment
   in your script on what pandas is doing "underneath" that manual loop.

## Acceptance criteria

- The script runs with `python starter_pandas_intro.py` and produces no errors.
- The SELL-only selection uses `.loc` with a boolean condition, not manual iteration.
- The `groupby` per-client totals match Module 3's totals for every client, exactly.
- A short comment in the script explains, in your own words, what `groupby("client_name")["value"].sum()`
  is doing in terms of Module 3's manual dict-accumulation loop.
