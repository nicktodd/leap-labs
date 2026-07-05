# Demo: Module 1 — Python Fundamentals: Syntax, Data Types & Control Flow

**Duration:** 15 minutes
**Files:** `trade_summary_demo.py`

## Part 1: Variables and basic data types (4 min)

Open `trade_summary_demo.py` and live-run it. Narrate each assignment:

```python
trade_id = "T0001"       # str
quantity = 120            # int
price = 185.32             # float
is_buy = True               # bool
```

Point out Python's dynamic typing: no type is declared, but every value still has one — show
`type(price)` in a REPL to make this concrete.

## Part 2: Control flow (6 min)

Walk through the `if/elif/else` block that classifies a trade's side, and the `for` loop that
iterates over a plain Python list of trade dictionaries. Narrate why a `for` loop over a list of
dicts is the plain-Python equivalent of what pandas will do for us structurally from Module 05
onward — this sets up that comparison deliberately.

Show a `while` loop only briefly (a simple counter) — control flow in data work is dominated by
`for` loops over collections, not `while` loops, and the demo should reflect that emphasis.

## Part 3: Running summary output (5 min)

Run the script end-to-end and show the printed summary: total trade count, total value, and a
per-side (BUY/SELL) breakdown, all computed with plain Python — no libraries.

Narration: this whole demo could be five lines of pandas. That's the point — Module 1 makes you
feel the manual bookkeeping (running totals, manual counters, manual dict lookups) so that when
pandas replaces it in Module 5, the value is obvious, not just asserted.

## Key message

Python's core syntax — variables, types, and control flow — is the same regardless of whether
you ever touch a data library. Everything from here on is built on this foundation.
