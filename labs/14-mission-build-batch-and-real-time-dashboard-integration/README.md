# Module 14 Lab — Mission Build: Batch + Real-Time Dashboard Integration

## Objectives

By the end of this lab you will have:

- Implemented a genuine cross-source insight that neither the batch nor the stream extract
  alone could answer
- Reasoned through a real scaling trade-off in the "fresh group.id every run" design decision

## Setup

Both data sources need to already exist — reuse the demo's:

```bash
docker start sprint7-postgres kafka-sprint7
pip install -r requirements.txt
```

## Task

### Part A — `compute_pending_settlement()`

Run the lab as-is:

```bash
python dashboard.py
```

It fails with `NotImplementedError` — that's the starting point, not a bug.

Implement `compute_pending_settlement(df)`. For each `account_id`, compute:

- `stream_quantity` — total quantity for that account, `source` starting with `"stream"`
- `batch_quantity` — total quantity for that account, `source` starting with `"batch"`
- `pending` = `stream_quantity - batch_quantity`

Return a `pandas.Series` indexed by `account_id`, sorted descending by `pending` (largest first).

Run it again — it should now print a "Pending settlement" section without errors.

### Part B — Prove the Behavior Is Real

1. Note the current `pending` values.
2. Produce more live trade events (reuse Module 9's `OrderService`, same accounts).
3. Rerun the dashboard. Confirm: the `batch_quantity` side of the calculation is unchanged,
   the `stream_quantity` side increased, and `pending` grew accordingly for the accounts
   involved.

### Part C — The Scaling Question

The demo guide flagged this as a real design trade-off: `extract_stream()` reads from the
beginning of the topic every single run (a fresh `group.id` each time). Answer, in writing:

1. What happens to this dashboard's runtime as the `trade-events` topic grows to contain a
   year of history?
2. Propose ONE concrete change to `extract_stream()` that would fix this, without losing the
   "always show the full recent picture" property the demo guide argued for. (Hint: "recent"
   doesn't have to mean "everything ever produced.")

## Deliverable

- A working `compute_pending_settlement()`, verified against a real rerun with new live trades
- Written answers to Part C

## Sprint 7 Wrap-up

This is the sprint's last technical module — see `shared/SPRINT-WRAP-UP.md` for the retrospective
prompt and Friday's assessment format.

## Acceptance criteria

- `python dashboard.py` runs without error and prints non-empty pending settlement figures
- Rerunning after producing new trade events shows `pending` values that changed only for
  affected accounts, and only on the stream side
- Part C's answer names the actual mechanism (unbounded read growing linearly with topic size)
  and proposes a concrete, specific fix (e.g. filtering by event timestamp, or seeking to a
  bounded offset) — not just "make it faster"
