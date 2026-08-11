# Module 1 Lab — Model Answer Notes

See `src/main/java/com/neueda/leap/sprint5/`. Verified: `mvn test` passes all 12 tests with
0 failures, 0 errors.

Key points to check in a delegate's solution:

- **`classifySide` uses `equalsIgnoreCase`, not `==` or `.equals()` on a possibly-null/differently
  cased string.** A delegate coming straight from Python sometimes reaches for `==` on strings out
  of habit — in Java, `==` compares object references, not content, and would silently produce
  wrong results here. This is one of the sharpest early Python-to-Java gotchas worth flagging in
  review even if a delegate's tests happen to pass by luck.
- **`valueByInstrument` uses `getOrDefault(key, 0.0)`**, not a manual `containsKey` check — both
  work, but `getOrDefault` is the idiomatic Java equivalent of Python's `dict.get(key, 0.0)`,
  and delegates who already saw that pattern in Sprint 4 should recognise it here.
- **`TradeParser.parse` must NOT wrap `Double.parseDouble` in a try/catch that swallows
  `NumberFormatException`.** A delegate who catches it "to be safe" and returns `null` or a
  default value has broken the acceptance criteria — the unchecked exception must be allowed to
  propagate, exactly the same as an uncaught Python exception would.
- **The checked exception is thrown only after both values parse successfully** — quantity and
  price are validated for positivity only once they're confirmed to be real numbers, not before.
