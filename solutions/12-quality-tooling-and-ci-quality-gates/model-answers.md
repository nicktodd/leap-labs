# Module 12 — Model Answers

`SettlementReporter.java` in this folder is the completed, verified implementation.

## Part A — The four original issues (verified real SonarQube findings)

```
BLOCKER  java:S2095  line 14  "Use try-with-resources or close this BufferedReader ..."
MAJOR    java:S1854  line 15  "Remove this useless assignment to local variable 'line'."
MINOR    java:S1643  line 18  "Use a StringBuilder instead."
MAJOR    java:S106   line 20  "Replace this use of System.out by a logger."
```

## Part B — The fixes

1. **`try (BufferedReader br = ...)`** — try-with-resources guarantees `close()` is called even
   if an exception is thrown mid-loop, which a bare `new BufferedReader(...)` with no explicit
   close does not.
2. **Renamed the header line's variable and never overwrote it** — the original code assigned
   `br.readLine()` to `line`, then immediately reassigned `line` in the loop condition before
   the header value was ever read. Using a separate name (`header`) for the header row removes
   the dead store.
3. **`StringBuilder` instead of `String out; out = out + ...`** — appends in place rather than
   allocating a new copy of the whole string on every iteration.
4. **`java.util.logging.Logger`** instead of `System.out.println` — the standard, zero-dependency
   logging facility, matching what a real application (not a demo script) should use.

## Part C — The two NEW issues that appeared, and why

After the first round of fixes, rerunning the analysis surfaced two issues that were **not** in
the original four:

```
MAJOR (BUG)  java:S2677  "Use or store the value returned from readLine() instead of
                          throwing it away."
MAJOR        java:S2629  "Invoke method(s) only conditionally."
```

**S2677** appeared because the first fix attempt discarded the header line as a bare statement —
`br.readLine();` with no assignment at all. SonarQube treats an unused return value from
`readLine()` as a genuine reliability concern (a caller ignoring whether a line existed, or was
`null`, at end-of-file). The real fix: assign it to a variable (`String header = br.readLine();`)
even though the value is only used for an optional debug log line.

**S2629** appeared because the first fix logged with `LOGGER.info(out.toString())` directly —
`out.toString()` always runs, building the full string, even when INFO-level logging is disabled
and the result would be thrown away immediately. The fix: guard the call with
`LOGGER.isLoggable(Level.INFO)`, so the (potentially expensive) `toString()` only runs when the
log message will actually be used.

**This is the real lesson of Part C**: fixing a flagged issue is not automatically risk-free —
rerunning the analysis after every change, not just once at the end, is what catches a fix that
traded one problem for a different one.

## Verified final state

```
mvn sonar:sonar -Dsonar.token=... -Dsonar.qualitygate.wait=true
...
QUALITY GATE STATUS: PASSED
BUILD SUCCESS
```

```
bugs: 0
code_smells: 0
vulnerabilities: 0
```

## Talking points

- Every one of these six issues (4 original + 2 introduced) is a genuine SonarQube finding
  against genuinely compiled, running code — none of this was staged or hand-picked from
  documentation.
- The `S1643` StringBuilder finding is identical, independently, to what Module 10's MANUAL smell
  hunt found in `TradeReportGenerator` — good evidence a tool and careful human review converge
  on the same real issues, from different starting points.
- The two BLOCKER-severity `S2095` (unclosed resource) issues in the demo's run against
  `TradeReportGenerator` are real reliability bugs the default "Sonar way" gate let through —
  exactly why Module 12 built a custom gate rather than trusting the default's name alone.
