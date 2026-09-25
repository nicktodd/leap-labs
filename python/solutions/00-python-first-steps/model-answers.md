# Module 1 Lab (Part 1) - Model Answer Notes

See `first_steps.py` for the full solution.

## Verified results

Output of `python first_steps.py` (with `my_name = "Ada"`, `quantity = 120`):

- TODO 1: `Ada is learning Python. Favourite number: 7. True.`
- TODO 2: all four fields printed with their correct type names (`str`, `int`, `float`, `str`).
- TODO 3: `22238.399999999998` (unformatted), then `22238.40` (formatted to 2dp).
- TODO 4: `medium trade` (120 is under 200, not under 50).
- TODO 5: first item `120`, last item `80`, all five printed on their own lines, sum `505`.
- TODO 6: `T0001`, `185.32`, then `0.0` for the missing `"commission"` key.
- TODO 7: three formatted lines, one per trade, each showing the correct `qty * price`.

## Key points to check in a delegate's solution

- **TODO 1's f-string embeds all three variables in one `print()`**, not three separate prints -
  the point is practising the `f"...{x}..."` shape, not just printing values.
- **TODO 3's unformatted total will show extra decimal places** (`22238.399999999998`, not
  `22238.4`) - this is normal floating-point behaviour, not a mistake. It's worth naming
  explicitly if a delegate asks why, since it's the first time they'll have seen it: `.2f`
  formatting in the very next line is the fix, not a bug to chase.
- **TODO 4 should be tested with more than one `quantity` value.** A delegate who only ever runs
  it with the original 120 hasn't actually verified the `small` or `large` branches exist and
  work - ask them to change the value and rerun, twice, before moving on.
- **TODO 5c must not use `sum()`.** The point of this task is the accumulator pattern itself
  (`total = 0`, then `total += q` inside the loop) - it's used everywhere from here on,
  including inside pandas once Module 5 replaces manual loops like this one.
- **TODO 6's `.get("commission", 0.0)` must return `0.0`, not raise a `KeyError`.** A delegate
  who writes `trade["commission"]` instead will hit exactly the error `.get()` with a default is
  there to avoid - worth pointing out explicitly if it comes up.
- **TODO 7's dicts should be built directly with all four keys**, not built as TODO 6's `trade`
  three times with a name change - the point is practising the literal `{...}` shape inside a
  list, since that's exactly what `starter_payments.py` (Part 2) starts from.

## Where this leads

Every idea in this lab - variables, types, arithmetic, `if`/`elif`/`else`, a list with an
accumulator, a dict, and finally a list of dicts - reappears immediately in Part 2
(`starter_payments.py`), just applied to a bigger, messier, real dataset instead of five
invented numbers. A delegate who's genuinely comfortable with TODO 7 by the end of this lab
should find Part 2's first task (reading fields off `transactions[0]`) unsurprising.
