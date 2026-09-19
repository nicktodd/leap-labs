# Module 7 Demo Guide — Batch Loading in Practice & ETL Patterns

The single most common way a real batch job causes real data damage: it gets rerun. A scheduler
retries a failed job, an operator reruns it manually after an outage, or a pipeline gets
redeployed mid-window — and the same file gets loaded twice.

## Setup

```bash
docker run -d --name sprint7-postgres -e POSTGRES_PASSWORD=leappass \
  -e POSTGRES_DB=sprint7 -p 5434:5432 postgres:16-alpine
```

```bash
mvn compile
mvn dependency:build-classpath -Dmdep.outputFile=cp.txt
```

## Run the Naive Loader Twice

```bash
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.sprint7.NaiveLoader
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.sprint7.NaiveLoader
```

Verified output:

```
--- Run 1 ---
Naive load inserted 5 rows.
Table now contains 5 rows total.
--- Run 2 (same CSV, rerun) ---
Naive load inserted 5 rows.
Table now contains 10 rows total.
```

**Point at it directly**: nothing crashed, nothing errored, no exception was thrown anywhere. The
job "succeeded" twice — and now every settlement is double-counted. This is the classic
batch-loading bug: plain `INSERT` has no memory of what it already loaded.

## Run the Idempotent Loader Twice

```bash
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.sprint7.IdempotentLoader
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.sprint7.IdempotentLoader
```

Verified output:

```
--- Run 1 ---
Idempotent load processed 5 rows (inserted or updated).
Table now contains 5 rows total.
--- Run 2 (same CSV, rerun) ---
Idempotent load processed 5 rows (inserted or updated).
Table now contains 5 rows total.
```

Same CSV, same "processed 5 rows" message both times — but the table stays at 5 rows. The fix:
`settlement_id` is a natural key, and `INSERT ... ON CONFLICT (settlement_id) DO UPDATE` makes
the load **idempotent** — running it any number of times converges on the same end state.

## The Concept, Named

- **Idempotent**: an operation that produces the same result no matter how many times it runs.
  Batch loads MUST be idempotent, because reruns are not an edge case — they're a certainty over
  a job's lifetime (retries, redeploys, manual reruns after an incident).
- **Natural key vs surrogate key**: `settlement_id` already uniquely identifies a settlement in
  the source system — that's what `ON CONFLICT` needs to detect "this row already exists."
  Without a natural key to conflict on, idempotency isn't possible at the database level at all.
- **Full load vs incremental load**: today's demo reloads the whole (small) file every time. A
  real warehouse table with millions of rows can't afford that — Module 8 and the mission build
  pick up incremental/delta loading, which only touches rows that actually changed.

## Transition to the Lab

Learners take a naive, INSERT-only batch loader and convert it to an idempotent one, verifying
the fix the same way this demo did: run it twice, prove the row count doesn't move the second
time.
