# Demo: Module 2 — Functions, Modules & Error Handling

**Duration:** 22 minutes
**Files:** `trade_math.py`, `trade_summary_demo.py`

## Part 1: Extracting a function, with type hints (4 min)

Show `trade_math.py`'s `trade_value(quantity: float, price: float) -> float`. Narration:
Module 1's inline `quantity * price` calculation, repeated on every loop iteration, deserves a
name. The `: float` and `-> float` annotations are type hints — Python doesn't enforce them at
runtime, but your editor and teammates read them as documentation, and tools like `mypy` can
check them. In data work, where a silently-wrong type (a string where a number was expected) is
one of the most common bugs, type hints earn their keep.

Show default and keyword arguments with `classify_trade(value, threshold=20000)`, calling it
both positionally and with the keyword form.

## Part 2: Writing a well-behaved module (3 min)

Point out three things that make `trade_math.py` a good module, not just a file with functions
in it:

- A module docstring at the top explaining its purpose
- Each function has its own docstring
- An `if __name__ == "__main__":` guard at the bottom — code inside it only runs when the file
  is executed directly (`python trade_math.py`), never when another file does
  `from trade_math import trade_value`

Run `python trade_math.py` directly to show the guard's code executing, then show
`trade_summary_demo.py` importing the same file without that code running.

## Part 3: Raising your own exceptions (5 min)

Show the `InvalidTradeError(Exception)` class in `trade_math.py` — a custom exception is just a
class that inherits from `Exception` (or a more specific built-in exception). `trade_value` now
validates its inputs and `raise`s `InvalidTradeError` with a clear message when they're invalid.

Narration: built-in exceptions like `TypeError` tell you *what kind* of mistake happened at the
Python level; custom exceptions let you say what's wrong in terms of *your own domain* — "a
negative quantity isn't a valid trade" is a business rule, not a Python type error.

## Part 4: Multiple except blocks, else, and finally (6 min)

Walk through the loop in `trade_summary_demo.py`:

```python
try:
    value = trade_value(trade["quantity"], trade["price"])
except (TypeError, ValueError) as e:
    print(f"Skipping {trade['trade_id']}: bad data type ({e})")
    continue
except InvalidTradeError as e:
    print(f"Skipping {trade['trade_id']}: {e}")
    continue
else:
    total += value
    print(f"{trade['trade_id']}: {classify_trade(value)} trade worth {value:,.2f}")
finally:
    print(f"  processed {trade['trade_id']}")
```

Narration, one clause at a time:

- **Multiple `except` blocks** let you react differently to different failure kinds — a wrong
  data type is a different problem from a business-rule violation, and the message should say so.
- **A combined `except (TypeError, ValueError) as e`** catches either type with one block, when
  the handling is genuinely the same either way.
- **`else`** runs only when the `try` block succeeded with no exception — it keeps "what happens
  on success" visibly separate from "what happens on failure."
- **`finally`** always runs, success or failure — the right place for cleanup that must happen
  regardless (closing a file, releasing a lock; here, just a processed-marker for clarity).

## Part 5: Re-raising with more context (4 min)

Show `safe_trade_value()`:

```python
def safe_trade_value(trade: dict) -> float:
    try:
        return trade_value(trade["quantity"], trade["price"])
    except InvalidTradeError as e:
        raise InvalidTradeError(f"{trade['trade_id']}: {e}") from e
```

Narration: sometimes the right response to an exception isn't to swallow it, it's to add context
and let it keep propagating — `raise ... from e` preserves the original error as the visible
cause while adding the detail (here, which trade_id failed) that the inner function didn't have.

## Key message

Exceptions aren't just "the program crashed" — they're a structured way to say exactly what went
wrong, react differently to different problems, and guarantee cleanup happens regardless. Custom
exceptions let that structure speak your domain's language, not just Python's.
