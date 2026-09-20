# Module 8 - Model Answers

`ConfirmationQualityCheck.java` in this folder is the completed, verified implementation.

## Verified output

```
=== Data Quality Report ===
Valid rows:       6
Quarantined rows: 4

  line 5: ,CORPB1,BUY,1000,101.10                  -> missing account_id
  line 6: ACC-002,AAPL,BUY,0,150.25                -> quantity must be positive, was 0.0
  line 7: ACC-004,VOD.L,HOLD,300,45.00             -> side must be BUY or SELL
  line 9: ACC-001,GILT10,BUY,500,xyz               -> price is not a number: 'xyz'
```

Before the TODOs were implemented, this same file reported **10 valid, 0 quarantined** - every
one of these four rows was silently accepted. That's the bug this lab reproduces and fixes.

## Why `validate()` returns a reason String, not a boolean - model answer

A boolean (`isValid(row)`) tells you a row failed. A `String` reason tells you WHY it failed -
and "why" is the only part of that information anyone downstream can actually act on. Settlement
looking at a quarantine report needs to know whether to chase a missing account ID or investigate
a corrupted price feed; those are different follow-up actions, and a boolean throws that
distinction away. The cost of returning a reason instead of a boolean is close to zero (one
`String` field vs one `boolean`), so there's no real trade-off being made here - it's a
better design at no extra cost.

## Talking points

- Each rule returns as soon as it fails (`return "missing account_id"` before checking `side`)
  - a row with multiple problems only reports the first one found. This is a deliberate,
  reasonable simplification for this lab; a stricter validator could collect ALL reasons a row
  failed, at the cost of more code.
- `quantity` is checked with `parseDouble` wrapped in try/catch (validity - is it a number at
  all), THEN checked against `<= 0` (business rule - is it a *sensible* number). Two different
  data quality dimensions, checked in sequence, each with its own specific message.
- Compare this to `SilentDropLoader` from the demo: same four failure conditions exist in this
  lab's data, but a try/catch-and-skip version would report "6 confirmations loaded" with total
  silence about the other four - exactly the Module 1 bug, reproduced with confirmations instead
  of trades.
