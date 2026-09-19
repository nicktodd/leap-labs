# Module 14 — Model Answers

`dashboard.py` in this folder is the completed, verified implementation.

## Part A & B — Verified real output, before and after new trades

**Before** producing more live trades:

```
-- Total quantity, by source --
batch (settled, end-of-day)        3650.0
stream (live, last few minutes)    7920.0

-- Pending settlement, by account --
ACC-003    5000.0
ACC-002     950.0
ACC-001   -1680.0
```

**After** running `OrderService` again (4 more events produced):

```
-- Total quantity, by source --
batch (settled, end-of-day)         3650.0
stream (live, last few minutes)    10560.0

-- Pending settlement, by account --
ACC-003    7000.0
ACC-002    1450.0
ACC-001   -1540.0
```

**Batch total: identical, both runs — 3650.0.** Nothing was loaded into the warehouse between
runs, so it couldn't change, and it didn't. **Stream total and every account's pending figure:
changed**, tracking exactly the new trades produced. This is the proof, not an assertion: the
same two-line diff (rerun the loader vs. rerun the producer) would move ONE of these numbers,
never both — because they measure genuinely different things.

## `compute_pending_settlement()`, explained

```python
def compute_pending_settlement(df: pd.DataFrame) -> pd.Series:
    by_account_source = (
        df.groupby(["account_id", "source"])["quantity"].sum().unstack(fill_value=0)
    )
    stream_col = next(c for c in by_account_source.columns if c.startswith("stream"))
    batch_col = next(c for c in by_account_source.columns if c.startswith("batch"))
    pending = by_account_source[stream_col] - by_account_source[batch_col]
    return pending.sort_values(ascending=False)
```

Same `groupby().unstack()` pattern `compute_insights()` already used for tickers — applied to
`account_id` instead. `next(c for c in ... if c.startswith(...))` finds the right column by
prefix rather than hardcoding the full source string, so the function doesn't break if the exact
wording of a source label changes later.

## Part C — model answer

**1. What happens as the topic grows to a year of history?** `extract_stream()`'s runtime grows
linearly with the TOTAL number of events ever produced to `trade-events` — because
`auto_offset_reset="earliest"` combined with a brand-new `group_id` every run means every single
run re-reads the entire topic from the beginning, not just "what's new." A topic with a year of
history would make every dashboard run progressively, permanently slower, even though the
dashboard only actually cares about the last few minutes.

**2. A concrete fix**: filter by event timestamp instead of reading everything. Kafka consumers
support `offsets_for_times()` — given a target timestamp (e.g. "10 minutes ago"), it returns the
offset to start reading from in each partition, without walking every earlier record. Replacing
`auto_offset_reset="earliest"` with an explicit `seek()` to the offset returned by
`offsets_for_times()` for "10 minutes ago" keeps the "always show the full RECENT picture"
property while making runtime bounded by recent volume, not total history.

## Talking points

- The "pending" values aren't meant to be a precise settlement figure — quantity is summed
  regardless of BUY/SELL side in this simplified model, which is a real limitation worth naming
  explicitly if a learner asks. The exercise's actual point is proving cross-source computation
  works and changes correctly on rerun, not building production-accurate P&L.
- This module is a genuine capstone: `extract_batch()` depends on Module 7's idempotent loader
  having run at least once; `extract_stream()` depends on Module 9's `OrderService` having
  published to a real topic. Nothing here works without earlier modules' work being real and
  correct — which is exactly the point of a mission build.
