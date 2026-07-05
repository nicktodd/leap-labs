# Module 4 Lab — Model Answer Notes

See `compliance_checker.py`. Verified output against `shared/trades.csv`:

- **LARGE** (value > 20,000): T0001, T0002, T0006, T0008, T0016
- **HIGH_VOLUME** (Equity BUY, quantity > 150): T0016 only — this is the trade the
  `asset_class == "Equity"` restriction exists for: without it, the Bond trades (quantities of
  2,000-5,000) would incorrectly dominate the flag.
- **HIGH_FREQUENCY** (>= 3 trades): Alice Chen, Ben Whitfield, Chidi Nwosu

Against `shared/messy-trades-raw.csv`: T0004 (blank `value`) and T0005 (blank `quantity`) are
skipped with a warning; the duplicate T0006 row is **not** deduplicated (the brief doesn't ask
for that — flagging it twice is correct per the rules as written, not a bug); the extreme outlier
T0021 (quantity 99,999) correctly flags both `LARGE` and `HIGH_VOLUME`.

Key points to check in a delegate's solution:

- **`read_trades()` converts `quantity` and `value` inside the `try`, before appending the row.**
  A common mistake is appending the raw string row first and converting later, which either
  crashes downstream or silently includes unconverted rows.
- **The `HIGH_VOLUME` rule checks `asset_class == "Equity"` first.** Delegates who skip this
  restriction will see Bond trades dominate the flag and should notice something's off — this is
  a deliberate check on whether they're testing against realistic output, not just "does it run."
- **`find_frequent_clients` counts *all* trades for a client**, not just flagged ones — a
  reasonable but incorrect reading is to only count a client's `LARGE`/`HIGH_VOLUME` trades.
- **The report and console output come from the same `write_report()` call**, not two separately
  maintained pieces of code that could drift apart.
- **`argparse` defaults match the table in the brief exactly** — a delegate who hardcodes values
  instead of wiring up `argparse` properly should be sent back to fix it; the CLI interface is
  part of the acceptance criteria, not a nice-to-have.
