# Module 9 Lab — Pair Exercise: One-Page EDA Summary

## Objectives

By the end of this lab you will have:

- Used `groupby` with multiple aggregations in one call
- Used `pivot_table` to reshape a summary into a wide, cross-tabulated table
- Used `merge` to combine `shared/trades.csv` with a new reference table
- Used `resample` to summarise the mission dataset over time

## Setup

- `pip install pandas`
- `shared/trades.csv` and `shared/advisors.csv` (repo root)
- Pair up with a partner for this exercise

## Task

Starter file: `starter_deeper_dive.py`, in `labs/09-pandas-deeper-dive/`.

Working with your partner, produce a single script that prints a "one-page" EDA summary of the
mission dataset, covering:

1. **groupby** — total, count, and mean `value` per `client_name`, in one `.agg([...])` call.
2. **pivot_table** — total `value`, rows = `instrument`, columns = `side`, filled with `0` where
   there's no matching data (not `NaN`).
3. **merge** — join `trades.csv` with `shared/advisors.csv` on `advisor`, then show total `value`
   per `team`.
4. **resample** — parse `trade_date` properly, set it as the index, and show total `value` per
   week.
5. A closing block of **3-5 one-line takeaways**, as comments, written by you and your partner
   together — each takeaway must reference a specific number from your output above, not a
   general statement.

## Pairing notes

- Decide together who drives (types) for which of the four sections — swap at least once.
- Before writing the takeaways, both of you should independently look at the output and note
  what stands out, then compare notes before writing the final three to five lines together.

## Acceptance criteria

- The script runs with `python starter_deeper_dive.py` and produces no errors.
- All four techniques (groupby, pivot_table, merge, resample) are present and correct.
- The pivot table has no `NaN` values — every cell is a real number.
- The merge correctly brings in `team` for every trade (no missing teams).
- 3-5 takeaways are written as comments, each citing a specific number from the output.
