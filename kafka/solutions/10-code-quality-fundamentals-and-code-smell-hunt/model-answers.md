# Module 10 - Model Answers

`CodeSmellScanner.java` in this folder is the completed, verified implementation of Part A.

## Part A - Verified output

```
-- Duplicated literals --
  "0.0005" appears 2 times -> extract to a named constant
```

`0.001` (the EQUITY rate) appears once and is correctly NOT flagged - duplication is specifically
about a value appearing more than once, not about magic numbers in general (that's the separate,
broader check the demo's scanner already had).

## Part B - Manual Smell Hunt

### 1. String concatenation in a loop

`out = out + tkr + "," + ...` runs once per row. `String` is immutable in Java - every `+`
doesn't append to the existing string, it allocates an entirely NEW string containing a copy of
everything so far, plus the new piece. For 10 rows this is invisible. For 10 million rows, the
total work done is proportional to the SQUARE of the row count (each concatenation copies
everything before it) - a `StringBuilder` would do the same job in work proportional to the row
count itself. This is a genuine, measurable performance smell, not a style preference - it just
happens to be invisible at small scale, which is exactly why it survives in real code for years.

### 2. Single Responsibility, named specifically

`doIt()`'s distinct jobs:
- **Parsing** a CSV line into typed fields - changes if the file format changes
- **Fee calculation** - changes if a fee rate or a new trade type is added
- **Aggregation** (running totals per ticker) - changes if the aggregation logic changes (e.g.
  aggregate per account instead of per ticker)
- **Reporting** (building the `out` string, writing `report.csv`) - changes if the report format
  or destination changes
- A fifth, easy to miss: **error handling policy** (silently skip bad rows) - changes if the
  business decides bad rows should instead be quarantined (Module 8's exact concern)

Five independent reasons for this one method to change, each unrelated to the others. Change any
one, and you're editing (and re-testing, if tests existed) all five at once.

### 3. A test you cannot write today

You cannot write a unit test for "given an EQUITY trade of value X, the fee is X * 0.001" without
ALSO reading a file from disk, because fee calculation is inline inside the loop that reads
`BufferedReader`. There's no method boundary around "just the fee logic" to call in isolation -
testing it means testing file I/O, parsing, aggregation, and reporting all at once, or not
testing it at all. This is the concrete, structural reason "just add a test" isn't actually
simple advice here - and it's exactly what Module 11's characterisation-tests-before-refactoring
approach is designed to work around.

## Talking points

- The lab's duplicated-literal finding (`0.0005` shared by BOND and the fallback branch) is a
  real, live risk: if a new trade type is added and someone copies the fallback branch as a
  starting point, they inherit a rate that was never actually chosen for that type - it just
  happened to be nearby.
- All of Part B's findings feed directly into Module 11: SRP violations become the seams a safe
  refactor extracts along; the untestable fee logic becomes the first thing a characterisation
  test has to work around before extraction is safe.
