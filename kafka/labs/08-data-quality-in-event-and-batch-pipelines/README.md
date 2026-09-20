# Module 8 Lab - Data Quality in Event & Batch Pipelines

## Objectives

By the end of this lab you will have:

- Written explicit validation rules covering completeness and validity, instead of relying on
  try/catch to hide bad data
- Proven the fix by reading a quarantine report, not by trusting a "success" message

## Setup

```bash
mvn compile
```

## The Bug, As Given

Run `ConfirmationQualityCheck` as-is:

```bash
java -cp target/classes com.neueda.leap.mission.stream.ConfirmationQualityCheck
```

It reports **10 valid rows, 0 quarantined** - but `confirmations.csv` has four genuinely bad
rows in it (a missing account ID, an invalid side, a zero quantity, and a non-numeric price).
`validate()` always returns `null`, so nothing is ever caught. This is deliberate: confirm the
bug is real before fixing it.

## Task

Complete the four TODOs inside `validate()` in `ConfirmationQualityCheck.java`:

1. Missing `account_id` → return `"missing account_id"`.
2. `side` is anything other than `BUY` or `SELL` → return `"side must be BUY or SELL"`.
3. `quantity` parses but is `<= 0` → return `"quantity must be positive, was <value>"`.
4. `price` does not parse as a number → return `"price is not a number: '<value>'"`.

Return `null` if a row passes every rule.

## Deliverable

A `ConfirmationQualityCheck` that reports exactly 6 valid rows and 4 quarantined rows, each
quarantined row labelled with the specific rule it broke.

## Acceptance criteria

- Valid count is 6, quarantined count is 4
- Every quarantined row's reason names the actual rule broken, not a generic message
- You can explain, in one sentence, why `validate()` returning a reason STRING is a better design
  than `validate()` returning a boolean
