# Module 2 Lab - Model Answer Notes

See `trade_math.py` and `trade_summary.py`. Key points to check:

- **`InvalidTradeError` inherits from `Exception`**, not from a built-in like `ValueError`
  unless there's a reason to - a plain custom class is the right default for a new domain rule.
- **`except (TypeError, ValueError) as e` is one block, not two.** Delegates sometimes write two
  separate `except` blocks with identical bodies instead of combining the tuple - functionally
  fine, but the combined form communicates "these are handled the same way" more clearly.
- **`else` accumulates the total, `finally` prints the processed-marker.** A common mix-up is
  putting the total-accumulation inside `finally` instead of `else` - that would add to the total
  even for a trade that failed validation, silently corrupting the running total.
- **`safe_trade_value` uses `raise ... from e`**, not a bare `raise InvalidTradeError(...)` - the
  `from e` preserves the original exception as the visible cause in the traceback, which matters
  when debugging a chain of re-raises.
- **`starter_math.py`'s `__main__` guard only prints when run directly.** Importing it from
  `trade_summary.py` should produce no output of its own - if it does, the guard is missing or
  misplaced.
- Type hints (`quantity: float`, `-> float`) are not enforced at runtime - a delegate correctly
  passing `quantity="N/A"` despite the hint is expected and is exactly what the `except
  (TypeError, ValueError)` block is there to catch.
