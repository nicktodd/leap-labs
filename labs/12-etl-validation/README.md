# Module 12 Lab — ETL Concepts & Data Validation

## Objectives

By the end of this lab you will have:

- Structured a small pipeline as extract, transform, and load stages
- Written a pytest suite that validates a dataset's schema and value ranges
- Used GenAI to interpret an unfamiliar failing-test error, then written the fix yourself

## Setup

- `pip install pandas pytest`
- `shared/messy-trades-raw.csv` (repo root)
- GitHub Copilot Chat available for Part 3

## Task

Starter files: `starter_etl_pipeline.py` and `starter_test_trades.py`, in
`labs/12-etl-validation/`.

### Part 1: Structure the pipeline

In `starter_etl_pipeline.py`, complete three functions:

- `extract()` — read `shared/messy-trades-raw.csv`
- `transform(df)` — apply Module 6's cleaning steps (drop the row with missing quantity,
  recompute the missing value, backfill the missing client_name, parse the ambiguous date,
  normalise asset_class casing without breaking `ETF`, drop the exact duplicate)
- `load(df, out_path)` — write the cleaned result to a CSV

### Part 2: Validate with pytest

In `starter_test_trades.py`, write a pytest suite (using a `clean_trades` fixture that calls
`transform(extract())`) with tests for:

1. No missing `trade_id` values
2. `quantity` is always positive
3. `value` is never negative
4. `asset_class` only contains `Equity`, `Bond`, `ETF`, or `Crypto`
5. No duplicate `trade_id` values

Run `pytest starter_test_trades.py -v` and confirm all five pass against your `transform()`.

### Part 3: Interpret an unfamiliar error, then fix it yourself

Add one more test, deliberately without `.all()`:

```python
def test_asset_class_valid_no_all(clean_trades):
    valid = {"Equity", "Bond", "ETF", "Crypto"}
    assert clean_trades["asset_class"].isin(valid)
```

Run it and read the error. If you don't immediately recognise it, paste the error message into
Copilot Chat and ask it to explain what's going wrong — then, **without copying a suggested fix
verbatim**, write the correct one-line fix yourself and explain in a comment why it was needed.

## Acceptance criteria

- `extract`, `transform`, and `load` are each a separate, named function — not one long script.
- All five validation tests pass against your `transform()` output.
- The deliberately broken test is present, run, and its error message is visible in your terminal
  history or a comment — not silently deleted once you understood it.
- The fix is written by you, with a comment explaining what `.isin(...)` returns and why `.all()`
  is needed to use it in an `assert`.
