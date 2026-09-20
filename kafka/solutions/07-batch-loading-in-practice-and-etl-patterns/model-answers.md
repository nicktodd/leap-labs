# Module 7 - Model Answers

`ConfirmationLoader.java` in this folder is the completed, verified implementation.

## Verified output

### Before the fix (Part A) - reproducing the bug

```
--- Run 1 ---
Processed 5 confirmations.
Table now contains 5 rows total.
--- Run 2 (same CSV, rerun) ---
Processed 5 confirmations.
Table now contains 10 rows total.
```

### After the fix (Part C) - proving idempotency

```
--- Run 1 ---
Processed 5 confirmations.
Table now contains 5 rows total.
--- Run 2 (same CSV, rerun) ---
Processed 5 confirmations.
Table now contains 5 rows total.
```

## The two changes

1. **`confirmation_id VARCHAR(20) PRIMARY KEY`** - without a primary (or unique) key on the
   natural identifier, Postgres has no way to detect "this row already exists"; `ON CONFLICT`
   has nothing to target.

2. **`INSERT ... ON CONFLICT (confirmation_id) DO UPDATE SET ...`** - on a fresh
   `confirmation_id`, this behaves exactly like a plain `INSERT`. On a `confirmation_id` that
   already exists, it updates that row's columns instead of adding a duplicate.

## Why the original wasn't idempotent, in one sentence

A plain `INSERT` has no concept of "this data was already loaded" - every execution is treated
as brand new, so running the same file twice produces two copies of every row.

## Talking points

- "Processed 5 confirmations" is printed identically both times, before and after the fix - the
  *loader's own logging* can't tell you whether the load was idempotent; only checking the actual
  row count can. This is worth calling out: a batch job reporting success tells you nothing about
  whether it was SAFE to run.
- This is the same problem Module 5's `group.id` demo touched from the other side: Kafka commits
  offsets so a consumer doesn't reprocess; here, `ON CONFLICT` makes reprocessing harmless even
  when it happens. Two different tools solving the same underlying question - what happens on a
  rerun?
- Module 8 builds on this directly: idempotency prevents duplication, but it doesn't catch a row
  that was wrong to begin with (a negative quantity, a missing account ID) - that's a data
  quality problem, not a reload problem.
