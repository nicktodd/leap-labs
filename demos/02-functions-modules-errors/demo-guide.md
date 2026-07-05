# Demo: Module 2 — Functions, Modules & Error Handling

**Duration:** 15 minutes
**Files:** `trade_math.py`, `trade_summary_demo.py`

## Part 1: Extracting a function (4 min)

Show `trade_math.py`'s `trade_value(quantity, price)` function. Narration: Module 1's inline
`quantity * price` calculation, repeated on every loop iteration, is exactly the kind of logic
that deserves a name — once it has a name, it can be tested, reused, and reasoned about on its
own.

Show default and keyword arguments with `classify_trade(value, threshold=20000)`, and call it
both positionally and with the keyword form (`classify_trade(value, threshold=50000)`) to make
the difference concrete.

## Part 2: Splitting code across modules (4 min)

Show `trade_summary_demo.py` importing from `trade_math.py`:

```python
from trade_math import trade_value, classify_trade
```

Narration: a "module" in Python is just a `.py` file; `import` is how one file uses code defined
in another. This is the same underlying idea as Sprint 1's Java classes and Sprint 3's SQL
schemas — logic namespaced and reused rather than copy-pasted.

## Part 3: Error handling with try/except (7 min)

Introduce a deliberately malformed trade record (a `quantity` that's the string `"N/A"` instead
of a number) and run the script without error handling first — let it crash, and narrate the
traceback line by line.

Then wrap the calculation in `try/except`:

```python
try:
    value = trade_value(trade["quantity"], trade["price"])
except TypeError:
    print(f"Skipping malformed trade {trade['trade_id']}: bad quantity/price")
    continue
```

Narration: `except TypeError` catches *only* the error we anticipated. Emphasise: never write a
bare `except:` — it hides bugs you didn't anticipate, not just the ones you did.

## Key message

Functions turn repeated logic into a single, testable unit. Modules let that logic be reused
across files. `try/except` lets a program keep working when one record is bad, instead of the
whole run crashing on it.
