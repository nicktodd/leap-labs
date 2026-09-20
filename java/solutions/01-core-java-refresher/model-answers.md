# Module 1 Lab - Model Answer Notes

See `src/main/java/com/neueda/leap/mission/engine/`. Verified: `mvn test` passes all 12 tests with
0 failures, 0 errors.

Key points to check in a delegate's solution:

- **`classifySide` uses `equalsIgnoreCase`, not `==` or `.equals()` on a possibly-null/differently
  cased string.** In Java, `==` compares object references, not content, and would silently
  produce wrong results here. This is one of the sharpest early Java gotchas worth flagging in
  review even if a delegate's tests happen to pass by luck.
- **`valueByInstrument` uses `getOrDefault(key, 0.0)`**, not a manual `containsKey` check - both
  work, but `getOrDefault` is the idiomatic way to accumulate into a `Map` without a separate
  existence check.
- **`TradeParser.parse` must NOT wrap `Double.parseDouble` in a try/catch that swallows
  `NumberFormatException`.** A delegate who catches it "to be safe" and returns `null` or a
  default value has broken the acceptance criteria - the unchecked exception must be allowed to
  propagate.
- **The checked exception is thrown only after both values parse successfully** - quantity and
  price are validated for positivity only once they're confirmed to be real numbers, not before.
