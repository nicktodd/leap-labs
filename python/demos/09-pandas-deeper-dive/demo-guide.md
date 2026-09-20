# Demo: Module 9 - pandas Deeper Dive: Groupby, Pivot, Merge & Time Series

**Duration:** 22 minutes
**Files:** `pandas_deeper_dive_demo.py`
**Data:** `shared/trades.csv` and a new reference table, `shared/advisors.csv`

## Part 1: groupby with multiple aggregations (5 min)

Module 5 used `groupby(...)["col"].sum()` - a single aggregation. Show
`.agg(["count", "sum", "mean"])` instead, computing all three per advisor in one call.

Narration: `.agg([...])` with a list runs several aggregations on the same column at once; `.agg`
also accepts a dict (`{"value": "sum", "quantity": "mean"}`) to aggregate different columns
differently - worth showing both forms exist, even briefly.

## Part 2: pivot_table - reshaping, not just summarising (6 min)

Show `trades.pivot_table(index="asset_class", columns="side", values="value", aggfunc="sum",
fill_value=0)`. Narration: `groupby` produces a long, tidy result; `pivot_table` reshapes that
same kind of summary into a wide, cross-tabulated table - asset class down the rows, side across
the columns. Point out `fill_value=0`: without it, the Bond/SELL cell (which has zero matching
rows) would be `NaN`, not `0` - a real gotcha worth calling out explicitly.

Connect back to Module 7's `crosstab`: `crosstab` counts rows; `pivot_table` aggregates a value
column. Same shape of table, different question being answered.

## Part 3: merge - bringing in a second table (6 min)

Introduce `shared/advisors.csv`, a small reference table (advisor, team, years of experience).
Show `trades.merge(advisors, on="advisor", how="left")`.

Narration: this is the same underlying idea as the Data week's SQL joins, expressed in pandas - `on`
is the join key, `how="left"` keeps every trade even if (hypothetically) an advisor had no
matching reference row. Group the merged result by `team` to show a business question - "which
team's book is larger?" - that's impossible to answer from `trades.csv` alone, only becomes
answerable once the two tables are combined.

## Part 4: time series basics (5 min)

Parse `trade_date` with `parse_dates=["trade_date"]` on load, then `set_index("trade_date")`.
Show `.resample("W")["value"].sum()` - a weekly total.

Narration: `resample` is groupby for time - instead of grouping by a category column, it groups
by a time bucket (day, week, month). This is the same underlying operation as `groupby`, applied
along a datetime index instead of a categorical one.

## Key message

Four separate operations, one underlying idea: reduce many rows to a meaningful summary, at
whatever granularity the question needs - one category (`groupby`), two dimensions at once
(`pivot_table`), across two tables (`merge`), or across time (`resample`).
