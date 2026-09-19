# Module 6 Lab — Model Answer Notes

See `clean_trades.py`. Verified output: 20 final rows, four distinct `asset_class` values
(`Equity`, `Bond`, `ETF`, `Crypto`), one outlier flagged (T0021, quantity 99,999).

Key points to check in a delegate's solution:

- **Three different missing-value strategies, not one rule applied everywhere.** A delegate who
  drops all three rows with missing data, or fills all three with 0/empty string, has missed the
  point — the grading is on the *reasoning* per column, not just a clean `isna().sum()` of zero.
- **The date fix must be justified by the `trade_id` sequence**, not just "I assumed day-first
  because that's more common outside the US." Both are legitimate startingpoints, but the
  *justification* using the surrounding rows is what the lab is actually testing.
- **`asset_class` must end up with `ETF`, not `Etf`.** This is the easiest place to spot a
  delegate who copy-pasted `.str.capitalize()` without checking every distinct output value.
- **The outlier must still be present in the final DataFrame**, just flagged separately — a
  delegate who filters it out entirely (e.g. `df = df[df["quantity"] < q3 * 5]`) has skipped the
  actual point of the exercise, which is judgement over automatic removal.
- **`drop_duplicates()` is called once, on an exact duplicate** — this row happens to be a clean
  case; delegates should notice it wouldn't be this simple for a *near*-duplicate (e.g. the same
  trade with one field slightly different) and say so, even briefly.
