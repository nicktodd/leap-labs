# Demo: Module 3 - Python Data Structures & File I/O

**Duration:** 18 minutes
**Files:** `read_trades_demo.py`

## Part 1: Lists, tuples, dicts, and sets - when to choose which (6 min)

Narrate each structure against the mission dataset:

- **list** - an ordered, changeable sequence: "all twenty trades, in file order." Use when order
  matters and you expect to add/remove items.
- **tuple** - an ordered, unchangeable sequence: `("AAPL", "Equity")` as a fixed pairing. Use when
  the values belong together and shouldn't be accidentally modified.
- **dict** - key-value lookup: `{"trade_id": "T0001", "quantity": 120, ...}`, one dict per trade
  row. Use whenever you need to look something up by name rather than position.
- **set** - an unordered collection of unique values: `{trade["instrument"] for trade in trades}`
  to get the distinct instruments traded, with duplicates automatically removed. Use when you
  care about membership or uniqueness, not order or count.

Show `type()` on each and a quick "can I do `my_list[0] = x`?" vs. "can I do `my_tuple[0] = x`?"
to make the mutability distinction concrete (the tuple assignment raises `TypeError`).

## Part 2: Reading a CSV file with plain Python (6 min)

Open `read_trades_demo.py` and walk through opening `shared/trades.csv` with `csv.DictReader`,
inside a `with open(...) as f:` block.

Narration: `with` guarantees the file is closed even if an error occurs partway through reading
- the same "guaranteed cleanup" idea as Module 2's `finally`, applied specifically to files.
`csv.DictReader` gives you one dict per row, keyed by the header line - no manual splitting on
commas required.

## Part 3: Building a summary structure and writing output (6 min)

Show the demo accumulating a `dict` keyed by instrument, each value a running total - this is
the plain-Python shape of what `groupby` will do in one line from Module 9 onward. Then write
the summary back out to a small text file with `with open(..., "w") as f:`.

Narration: reading and writing files is symmetric - `with open(path) as f` for reading,
`with open(path, "w") as f` for writing - and the `with` block handles closing either way.

## Key message

Choosing the right data structure (list vs. tuple vs. dict vs. set) makes code both correct and
readable. Reading and writing files with `with` is the standard, safe pattern you should default
to every time, not just in demos.
