# Module 1 — Model Answers

There's no single correct set of three concerns — the point is specificity and a real cost, not
matching this list exactly. These are representative, genuine findings.

## Representative Concern 1 — Silently Swallowed Errors

**Where:** `catch (Exception e) { // skip bad row }` inside `doIt()`.

**Cost:** Any malformed row — a missing field, a corrupted number — disappears with zero trace.
No log, no count, no distinction between "this row was intentionally filtered" and "this row
crashed the parser." In a real settlement pipeline, this is a silent, undetectable data-loss bug.
The only reason it's visible at all in this lab is that someone was told to compare row counts.

## Representative Concern 2 — One Method, Six Jobs

**Where:** `doIt()` does file I/O, CSV parsing, fee calculation, aggregation into shared state,
report formatting, and a second file write — all in roughly 40 lines, all in one method.

**Cost:** There's no way to test fee calculation without also running file I/O. There's no way to
change how the report is formatted without touching the code that also does the calculation. Any
future change to any one responsibility risks breaking an unrelated one, because none of them are
isolated from each other.

## Representative Concern 3 — Duplicated, Hardcoded Fee Logic

**Where:** `val * 0.001` for equities, `val * 0.0005` for bonds and everything else — the rate
appears as a bare literal, not a named constant, and the "everything else" branch quietly reuses
the bond rate for fund trades with no comment explaining whether that's intentional.

**Cost:** If the equity fee rate changes, someone has to know to find this exact line (there's no
single place it's defined). And the fund/bond rate collision is genuinely ambiguous — a future
reader can't tell if fund trades using the bond rate is a deliberate business rule or a bug nobody
noticed, because nothing in the code states an intent either way.

## Other Legitimate Findings

- Two static mutable `Map` fields (`tot`, `f`) as global accumulation state — calling `doIt()`
  twice in the same JVM run silently accumulates totals across both calls, since nothing resets
  them.
- Variable names (`d`, `x`, `tr`, `f`, `p`) that require reading the whole method to understand,
  rather than being self-explanatory at the point of use.
- String concatenation (`out = out + ...`) inside a loop for building the report — not a
  correctness bug at this data volume, but a real performance cost that scales badly.
- Zero tests anywhere in the project — every one of the above findings had to be discovered by
  reading the code and running it manually, because nothing verifies behaviour automatically.

## The Row-Count Question

`trades.csv` has 12 data rows. The program reports "Processed 10 trades." The two missing rows
are the ones with a blank quantity (`VOD.L`) and a non-numeric price (`BARC.L`) — both caught and
silently discarded by the empty `catch` block. Most pairs do **not** notice this without being
told to check — which is itself the point: a bug this quiet doesn't announce itself.

## Framing for Discussion

None of these findings make this "bad code" in a judgmental sense — they make it **expensive**:
expensive to extend safely (Concern 2), expensive to trust (Concern 1), expensive to reason about
correctly (Concern 3). That reframing — cost, not blame — is what Modules 10-13 build on for the
rest of the sprint.
