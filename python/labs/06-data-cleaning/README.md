# Module 6 Lab - Data Cleaning & Preparation

## Objectives

By the end of this lab you will have:

- Identified and handled missing values, choosing a different strategy per column based on what's
  actually knowable
- Parsed an ambiguous date format correctly, using context rather than a guess
- Normalised inconsistent casing without introducing a new inconsistency
- Removed an exact duplicate row
- Flagged (not silently removed) a statistical outlier, with documented reasoning

## Setup

- `pip install pandas`
- `shared/messy-trades-raw.csv` (repo root) - the same trades as `shared/trades.csv`,
  deliberately dirtied

## Task

Starter file: `starter_clean_trades.py`, in `labs/06-data-cleaning/`.

For **each** issue below, write the cleaning code **and** a one-line comment explaining your
reasoning - the reasoning is graded as part of this lab, not just the resulting numbers.

1. **Missing `quantity`** (one row) - cannot be safely reconstructed. Drop the row.
2. **Missing `value`** (one row) - can be recomputed as `quantity * price`. Recompute it, don't
   drop the row.
3. **Missing `client_name`** (one row) - the same `client_id` appears on another row that does
   have a name. Backfill it from that row.
4. **Ambiguous date format** - one row's `trade_date` is in `DD/MM/YYYY` format, not
   `YYYY-MM-DD` like the rest. Work out which day it actually is using the surrounding
   `trade_id` sequence (don't just assume day-first or month-first), then parse the whole column
   to a proper datetime dtype.
5. **Inconsistent casing in `asset_class`** - normalise it. Check your fix doesn't turn `"ETF"`
   into `"Etf"` (a generic `.str.capitalize()` will do exactly that) - use a small canonical
   mapping instead.
6. **An exact duplicate row** - find it with `.duplicated()`, then remove it.
7. **A quantity outlier** - one Equity trade has a quantity far outside the range of every other
   Equity trade. Flag it (print it, don't delete it) and write one sentence in your script's
   comments on what you'd do next to investigate it (who would you ask, what would confirm or
   rule out a data-entry error?).

## Acceptance criteria

- The script runs with `python starter_clean_trades.py` and produces no errors.
- The final cleaned DataFrame has 20 rows (22 in the file, minus 1 dropped for missing
  quantity and 1 exact duplicate removed).
- Every one of the seven issues above is handled, each with a one-line comment explaining the
  reasoning, not just the code.
- `asset_class` has exactly four distinct values after cleaning: `Equity`, `Bond`, `ETF`, `Crypto`
  - check this explicitly by printing `df["asset_class"].unique()`.
- The outlier is printed, not dropped, along with your one-sentence investigation note.
