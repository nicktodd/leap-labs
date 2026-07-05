# Module 3 Lab — Model Answer Notes

See `read_trades.py`. Key points to check:

- **`value` must be converted with `float()` before summing.** `csv.DictReader` returns every
  field as a string; forgetting the conversion produces string concatenation instead of a sum
  (or a `TypeError` if `+=` is used on a running float total) — a good diagnostic for whether the
  "everything from a CSV is a string" point actually landed.
- **The path is computed from `Path(__file__).resolve().parents[2]`**, not a hardcoded absolute
  path or a bare `"shared/trades.csv"` — the latter only works if the script happens to be run
  from the repo root. Using `__file__` makes the script location-independent.
- **A `set`, not a `list`, for distinct advisors.** Using a list and manually checking
  `if advisor not in advisors` before appending works but is exactly the kind of manual
  bookkeeping a `set` exists to remove.
- **Both the read and the write use `with`.** A missing `with` on the write (a bare
  `f = open(...)` without a matching `f.close()`) is a common miss to watch for.
