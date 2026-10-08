# Module 09 Lab - Harden the Mission Model with Keys, Indexes & Constraints

## Objectives

By the end of this lab you will have:

- Reviewed and confirmed primary and foreign keys on every table
- Added indexes where they genuinely help, and explained why elsewhere they wouldn't
- Added NOT NULL, UNIQUE, and CHECK constraints to enforce correctness at the database level
- Closed Module 08's known gap: a table for a client's actual current holdings
- Made sure the schema keeps the history the mission brief asks for
- Used `EXPLAIN ANALYZE` to see an index change a query plan

## Setup

- Module 08's first-draft DDL for the mission model
- Access to a Postgres instance to actually run and test your DDL

## Task sheet

### Part A - Close the gap

1. Add a `client_holdings` table: `client_id` (FK to `clients`), `instrument_id` (FK to
   `instruments`), `quantity`, and `as_of_date`. Decide what the primary key should be, and
   justify your choice.
2. Re-read requirements 1 and 2 in [`shared/mission-brief.md`](../../shared/mission-brief.md):
   the brief needs the **history** of each model portfolio's target composition, and of each
   client's subscriptions, not just the current state. Make your schema keep it:
   - Add `effective_from` (`DATE NOT NULL`) and `effective_to` (`DATE`, `NULL` meaning "still
     current") to `model_portfolio_holdings`, and make `effective_from` part of its primary key,
     so a rebalance closes the old row and inserts a new one instead of overwriting it.
   - Add `ended_date` (`DATE`, `NULL` meaning "current subscription") to
     `client_subscriptions`.
   - Write down, in one sentence each, how you'd query a portfolio's **current** composition, and
     its composition **on a past date**.

   **Check:** you can insert two rows for the same portfolio and instrument with different
   `effective_from` dates without a primary key error.

### Part B - Constraints

3. Add `NOT NULL` to every column that should always have a value (be specific about which,
   and why, for each table).
4. Add a `UNIQUE` constraint on `instruments.ticker`, even though `instrument_id` is already the
   primary key. Explain in one sentence why both are useful.
5. Add a `CHECK` constraint on `model_portfolio_holdings.target_weight_pct` so it can only be
   between 0 and 100.
6. Add a `CHECK` constraint on `client_holdings.quantity` so it can never be negative.
7. Add a `CHECK` constraint so an `effective_to` (or `ended_date`) can't be earlier than the
   date it closes.

### Part C - Indexes

8. Add an index on every foreign key column across your schema (Postgres doesn't create these
   automatically, unlike for primary keys).
9. Identify one column, beyond the foreign keys, that you'd index because it's likely to be
   filtered or joined on often (for example, something used in a common report). Justify your
   choice.
10. Identify one column you would **not** index, and explain why, using what you learned about
   when indexes don't help.

### Part D - Prove it works

11. Run your complete, updated DDL against a real Postgres database.
12. Try to insert a row that violates one of your constraints (e.g. a `target_weight_pct` of
    150), confirm Postgres rejects it, and note the actual error message.

### Part E - Read an execution plan

13. Pick a query that filters on a foreign key column, for example
    `SELECT * FROM client_holdings WHERE instrument_id = 7;`. Run it with `EXPLAIN ANALYZE`
    **before** creating that column's index (drop the index first if you've already added it),
    then create the index and run it again. Note what changes: `Seq Scan` to `Index Scan` (or
    `Bitmap Index Scan`), `Filter` to `Index Cond`, and whether `Rows Removed by Filter`
    disappears. On a table this small Postgres may still choose a sequential scan, if so, run
    `SET enable_seqscan = off;` to see the index plan, then `SET enable_seqscan = on;`
    afterwards, and write one sentence on why the planner preferred the scan.
14. Run `EXPLAIN ANALYZE SELECT * FROM instruments WHERE UPPER(ticker) = 'GLBEQ1';`. Explain
    why the index on `ticker` can't be used, then rewrite the query so it can, and confirm the
    new plan with `EXPLAIN ANALYZE`.

## Acceptance criteria

- `client_holdings` exists, with a justified primary key choice.
- `model_portfolio_holdings` and `client_subscriptions` keep history, as the mission brief
  requires, rather than only the current state.
- Every table has appropriate `NOT NULL`, and the two specified `CHECK` constraints are in
  place and working.
- Every foreign key column has an index.
- You've named one additional column worth indexing and one you'd deliberately leave unindexed,
  both with reasoning.
- You've demonstrated, with a real error message, that at least one constraint actually rejects
  bad data.
- You've compared `EXPLAIN ANALYZE` output before and after adding an index, and rewritten a
  function-wrapped filter so it can use an index.

If you finish early, add a `CHECK` constraint ensuring `client_holdings.as_of_date` can't be in
the future, what's a scenario where that constraint might turn out to be wrong?
