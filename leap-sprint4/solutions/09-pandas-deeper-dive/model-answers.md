# Module 9 Lab — Model Answer Notes

See `deeper_dive.py`. Verified output against `shared/trades.csv` and `shared/advisors.csv`.

Key points to check in a delegate pair's solution:

- **`.agg(["count", "sum", "mean"])` is one call, not three separate `groupby` calls** chained
  together — the whole point of Module 9's first section is discovering this exists.
- **`fill_value=0` is present on the `pivot_table` call.** Without it, `ETH`/`SELL` and
  `US10Y`/`SELL` (genuinely zero trades) would show as `NaN`, which is both visually confusing
  and would break any further arithmetic on the pivoted table.
- **The merge uses `how="left"`** (or, since every advisor here does have a matching row, `how`
  barely matters for this dataset — but delegates should still state which they used and why,
  since a stray advisor name typo would silently drop rows under `how="inner"`).
- **Every takeaway must cite an actual number from the delegate's own output**, not a generic
  statement — "the Growth team has more value" is not a takeaway; "the Growth team has
  188,237.60 vs. Income's 13,822.05" is.
- **Pair-work check**: ask each partner, independently, to explain one of the four sections they
  did *not* type — if either can't, the "swap driver" instruction wasn't followed in spirit.
