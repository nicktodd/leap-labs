# Module 2 Lab — Batch vs Real-Time: Answers

## Scenario A — End-of-Day Settlement

**Decision: Batch**

Settlement is a bounded, time-boxed operation — all trades from the day's session exist by
market close, and the reconciliation window is fixed (overnight before systems reset). Using
batch here avoids the infrastructure cost of maintaining a live stream for an operation that
only runs once per day. The demo's BatchSettlementJob shows that a batch job with a clear
deadline is a natural fit: if it fails, you know immediately (the overnight window closes without
a confirmation), and retrying a batch job against an immutable snapshot of the day's trades is
straightforward. A streaming implementation would carry continuous infrastructure cost for a
problem that is inherently periodic.

## Scenario B — A Live Price Feed

**Decision: Real-time**

Prices change continuously and the risk calculations that consume them need the current price,
not a snapshot from an earlier batch. The demo's LivePriceFeedSimulator shows that a batch job
updating prices on even a short interval (say, every minute) would produce risk calculations
based on stale prices during high-volatility moments — a concrete failure mode. The data is not
bounded in the way settlement data is: there is no "end of the price feed" until the market
closes, so a batch window does not map naturally onto the problem.

## Scenario C — Monthly Client Statements

**Decision: Batch**

Monthly statements are generated once per month on a fixed date from a complete, bounded dataset
(the month's activity). Batch is the natural fit: the data is finite and known at generation
time, and the deadline is a calendar date rather than a latency requirement. The failure
visibility argument from the demo applies cleanly: if the batch job fails, you know before
statements are sent, and you can rerun it. A streaming implementation would add continuous cost
and complexity for a report that only needs to be correct once per month.

## Discussion Questions

### 1. Would 100x data volume change any answer?

Scenario C (monthly statements) is the one most likely to tip. At 100x account volume, a single
batch job generating every statement sequentially on a fixed date might not complete within the
acceptable overnight window. The tipping point would be whether the batch job can still finish
within its deadline — if not, the architecture would need to change (parallelise the batch job,
or shift to event-driven generation triggered per account on a rolling basis throughout the day
before the statement date). The other two scenarios are less sensitive: settlement is already a
time-bounded overnight job (and 100x trade volume would push toward parallelisation within the
batch, not a shift to real-time), and the price feed is already real-time.

### 2. Failure modes if built the wrong way

**Scenario A built as a live stream (wrong pattern):**
Settlement data would be processed as trades arrive throughout the day, creating partial
positions that change with every event. A downstream system reading the settlement state mid-day
would see an incomplete, changing snapshot and might act on it (triggering premature settlement
messages, incorrect margin calls). The natural audit checkpoint — "as of market close, the
settlement is complete and stable" — disappears.

**Scenario B built as an hourly batch job (wrong pattern):**
Risk calculations between batch runs would use prices that are up to 59 minutes stale. During a
market event (a flash crash, an earnings surprise), the trading platform would be making
risk decisions based on prices from before the event. A position that should trigger a margin
call at the current price would appear safe at the hour-old price — a concrete, measurable
financial risk.

**Scenario C built as a live stream (wrong pattern):**
Statements would be generated continuously as events arrive, meaning every trade would trigger
a new version of the client's statement. Clients would receive dozens or hundreds of statement
emails per month (or the system would need complex deduplication logic to suppress them), and
the final statement at month-end would need to be distinguished from the intermediate ones —
replicating the same bounded-batch logic that batch was designed to provide natively.
