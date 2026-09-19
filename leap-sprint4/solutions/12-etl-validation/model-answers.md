# Module 12 Lab — Model Answer Notes

See `etl_pipeline.py` and `test_trades.py`. Verified: all 6 tests pass, `transform()` reduces
22 raw rows (21 unique trades, one duplicated) to 20 clean rows, matching Module 6's result
exactly.

Key points to check in a delegate's solution:

- **`extract`, `transform`, and `load` are genuinely separate functions**, each independently
  callable and testable — a delegate who inlines everything into one script under a different
  name has missed the actual point of structuring a pipeline this way.
- **The pytest fixture calls `transform(extract())`**, not a hardcoded/pre-saved clean file — the
  tests must validate the pipeline's actual current output, not a snapshot that could drift out
  of sync with the code.
- **Before fixing the broken test, the delegate should be able to explain, in their own words,
  what `.isin(...)` returns** (a boolean Series, one value per row) and why `assert` can't use it
  directly. A delegate who pastes a GenAI-suggested fix without being able to explain this hasn't
  met the module's actual bar — the acceptance criteria explicitly requires the error message to
  have been read, not just made to go away.
- **The comment explaining the fix should reference `.all()` specifically** ("were all rows
  valid"), not just "this fixes the error" — the reasoning is what's being assessed, same as
  every other module's requirement for justified, not just working, code.
