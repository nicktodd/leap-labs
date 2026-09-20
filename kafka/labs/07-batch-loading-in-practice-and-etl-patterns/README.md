# Module 7 Lab - Batch Loading in Practice & ETL Patterns

## Objectives

By the end of this lab you will have:

- Reproduced a real batch-loading bug (a rerun silently doubling data)
- Fixed it by making the load idempotent, and proven the fix the same way the bug was proven

## Setup

Reuse the demo's Postgres container, or start your own:

```bash
docker run -d --name missionstream-postgres -e POSTGRES_PASSWORD=leappass \
  -e POSTGRES_DB=missionstream -p 5434:5432 postgres:16-alpine
```

```bash
mvn compile
mvn dependency:build-classpath -Dmdep.outputFile=cp.txt
```

## Task

### Part A - Reproduce the Bug

Run `ConfirmationLoader` twice against `confirmations.csv`:

```bash
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.mission.stream.ConfirmationLoader
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.mission.stream.ConfirmationLoader
```

Confirm what you see: does the row count double on the second run? This is the bug you're
about to fix - see it happen before changing anything.

### Part B - Fix It

Reset the table (`DROP TABLE trade_confirmations;` via `docker exec missionstream-postgres psql -U
postgres -d missionstream -c "DROP TABLE trade_confirmations;"`), then complete the two TODOs in
`ConfirmationLoader.java`:

1. Add a `PRIMARY KEY` constraint on `confirmation_id` in the `CREATE TABLE` statement.
2. Change the `INSERT` into an `INSERT ... ON CONFLICT (confirmation_id) DO UPDATE SET ...` so
   reruns update existing rows instead of adding new ones.

### Part C - Prove the Fix

Run the fixed loader twice, the same way you did in Part A. The row count must NOT change on the
second run.

## Deliverable

A working, idempotent `ConfirmationLoader`, with both the before (duplicating) and after (stable)
behavior observed directly - not assumed.

## Acceptance criteria

- Table has a primary key on `confirmation_id`
- Load uses `ON CONFLICT ... DO UPDATE`, not a plain `INSERT`
- Running the loader twice in a row leaves the row count unchanged after the fix
- You can explain, in one sentence, why the original version was NOT idempotent
