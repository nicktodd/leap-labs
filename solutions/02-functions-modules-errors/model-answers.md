# Module 2 Lab — Model Answer Notes

See `trade_math.py` and `trade_summary.py`. Key points to check:

- **Two files, one `import`.** `trade_summary.py` imports `trade_value` and `classify_trade`
  from `trade_math` — delegates sometimes redefine the functions in both files instead of
  actually importing, which defeats the point of the exercise.
- **`except TypeError`, not a bare `except:`.** A bare `except` would also silently swallow
  genuine bugs (e.g. a typo'd dictionary key), not just the malformed-quantity case it's meant to
  catch.
- **The keyword-argument form is demonstrated separately** (the "VIP check"), not forced
  awkwardly into the main loop — showing the concept clearly matters more than cramming it in.
- **Behaviour for well-formed trades is unchanged** from Module 1's version — refactoring should
  never change output for the cases that already worked.
