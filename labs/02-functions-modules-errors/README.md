# Module 2 Lab — Functions, Modules & Error Handling

## Objectives

By the end of this lab you will have:

- Written and called functions with type hints, including one with a default keyword argument
- Written a well-behaved module: docstrings and an `if __name__ == "__main__":` guard
- Defined and raised a custom exception for a business-rule validation failure
- Handled multiple exception types with separate `except` blocks, a combined `except (...)`, and
  `else`/`finally`
- Re-raised an exception with extra context using `raise ... from e`

## Setup

- Python 3.11+, no external libraries
- Starter files: `starter_math.py` (module to complete) and `starter_summary.py` (script to
  refactor), containing several deliberately malformed trade records

## Task

1. In `starter_math.py`:
   - Define `InvalidTradeError(Exception)`, a custom exception class.
   - Write `trade_value(quantity: float, price: float) -> float`, which `raise`s
     `InvalidTradeError` if `quantity` or `price` is not positive, otherwise returns
     `quantity * price`.
   - Write `classify_trade(value: float, threshold: float = 20000) -> str`.
   - Write `safe_trade_value(trade: dict) -> float`, which calls `trade_value` and, if it raises
     `InvalidTradeError`, re-raises it with the trade's `trade_id` folded into the message
     (`raise InvalidTradeError(...) from e`).
   - Add a module docstring, a docstring on each function, and an `if __name__ == "__main__":`
     block that prints one example call.
2. In `starter_summary.py`, import from `starter_math` and refactor the loop to:
   - Catch `(TypeError, ValueError)` together for a wrong-type quantity/price.
   - Catch `InvalidTradeError` separately for a business-rule failure (e.g. negative quantity).
   - Use `else` to accumulate the running total only on success.
   - Use `finally` to print a "processed `<trade_id>`" line unconditionally.

## Acceptance criteria

- `starter_math.py` runs standalone (`python starter_math.py`) and produces output only from its
  `__main__` guard.
- `starter_summary.py` imports from `starter_math.py` and runs without crashing on any of the
  provided malformed trades.
- Each malformed trade is caught by the correct `except` block (wrong type vs. business-rule
  violation) with a message that says which.
- `else` and `finally` are both used, each for the purpose described above, not interchangeably.
- No bare `except:` anywhere.
