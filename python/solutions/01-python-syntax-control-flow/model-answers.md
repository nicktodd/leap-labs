# Module 1 Lab - Model Answer Notes

See `trade_summary.py` for the full solution. Key points to check when reviewing a delegate's
attempt:

- **Threshold comparison uses the computed `value`, not `quantity` or `price` alone.** A common
  mistake is flagging on `price > 20000` instead of `quantity * price > 20000`.
- **Running totals are accumulated inside the loop**, not recomputed afterwards with a second
  pass - this is the "manual bookkeeping" habit Module 5's pandas equivalent (`df[...].sum()`)
  replaces.
- **BUY/SELL counts use `elif`, not two independent `if` statements** - defensive coding for a
  side value that might one day be something else (e.g. a future `SHORT` side).
- T0008's quantity (`0.5`) is deliberately a float, not an int, since fractional units (crypto)
  are realistic in this domain - this previews why Module 3's data-structure choices need to
  tolerate mixed numeric types.
