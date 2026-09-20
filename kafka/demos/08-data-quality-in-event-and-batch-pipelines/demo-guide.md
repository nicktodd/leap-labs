# Module 8 Demo Guide - Data Quality in Event & Batch Pipelines

Module 1 introduced `TradeReportGenerator` - the starter codebase's `catch (Exception e) {}`
silently dropped 2 of 12 rows with no trace. Today's demo reproduces that exact bug in
miniature, then fixes it properly.

## Run the Silent-Drop Version

```bash
mvn compile
java -cp target/classes com.neueda.leap.mission.stream.SilentDropLoader
```

Verified output:

```
Loaded 6 trades.
(No record of how many rows were skipped, or why.)
```

**Point at it directly**: the same 10-row CSV has 4 bad rows in it. This loader reports success
- "Loaded 6 trades" - with zero indication that 4 rows never made it in. This is Module 1's bug,
exactly: a catch block with nothing in it destroys the evidence a problem ever existed.

## Run the Quarantine Version

```bash
java -cp target/classes com.neueda.leap.mission.stream.QuarantineLoader
```

Verified output:

```
=== Data Quality Report ===
Valid rows:       6
Quarantined rows: 4

  line 4: ,GILT10,2000,98.50                       -> missing account_id
  line 6: ACC-002,AAPL,-50,150.25                  -> quantity must be positive, was -50.0
  line 7: ACC-004,,300,45.00                       -> missing ticker
  line 9: ACC-001,GILT10,abc,98.50                 -> quantity is not a number: 'abc'
```

Same input file, same 6 valid rows loaded - but now every bad row is counted, kept, and labelled
with the SPECIFIC rule it broke. Nothing was silently thrown away.

## The Concept, Named

- **Validate, don't just try/catch**: `SilentDropLoader` treats "this row is bad" as an
  *exception* - something unexpected that gets caught and forgotten. `QuarantineLoader` treats
  it as an *expected outcome* - a named rule that a row can fail, checked explicitly, every time.
- **Quarantine, not delete**: a bad row isn't a row you throw away - it's a row someone
  (Settlement, in a real system) needs to see and fix. Deleting it silently is a worse failure
  mode than crashing loudly.
- **Data quality dimensions**, made concrete by today's four failures:
  - **Completeness** - `missing account_id`, `missing ticker`
  - **Validity** - `quantity is not a number`
  - **Plausibility / business-rule validity** - `quantity must be positive`

## Batch vs Event: the Same Problem, Different Visibility

- In a **batch** load (today's demo), a bad row sits in a file you can inspect after the fact -
  quarantine and reporting are straightforward because everything is already in front of you.
- In an **event** pipeline (Kafka, Modules 4-6), a bad event is one message among a continuous
  stream - there's no "end of file" moment to generate a report at. The same quality checks have
  to run per-event, in real time, with quarantined events routed somewhere (a dead-letter topic)
  rather than a report printed at the end.
- The RULES are identical either way - completeness, validity, business plausibility. Only WHEN
  and WHERE the check happens changes.

## Transition to the Lab

Learners take a silent-drop loader (same shape as `SilentDropLoader`) and convert it into a
quarantine loader - writing the specific validation rules themselves, and proving the fix by
reading the quarantine report, not by trusting a "success" message.
