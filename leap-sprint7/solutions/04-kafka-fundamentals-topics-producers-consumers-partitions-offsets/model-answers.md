# Module 4 — Model Answers

## Part A — Match the Terms

1. **Topic** — `trade-events`, the single named stream every trade gets published to.
2. **Producer** — the trading platform's order-processing code, publishing one event per executed
   trade.
3. **Consumer** — any one of Settlement, the risk dashboard, or the compliance audit log, reading
   from the topic.
4. **Consumer group** — three separate groups, one per system (Settlement's group, the risk
   dashboard's group, compliance's group) — each group gets its own complete copy of every event,
   tracked independently. (Within a single system that scales out to multiple instances, those
   instances would form one consumer group sharing the work — but the three *systems* here are
   three separate groups, each needing the full stream.)
5. **Partition** — one of several independent, ordered logs the `trade-events` topic is split
   into, so multiple consumer instances can read in parallel.
6. **Offset** — a trade event's position within its specific partition — meaningless on its own,
   only meaningful as "position 47 in partition 2."

## Part B — Partition Key

1. **Account ID satisfies Settlement's requirement.** Settlement needs each account's trades in
   the order they happened — using account ID as the key guarantees every trade for account
   `A123` lands in the same partition, in production order, satisfying exactly that requirement.

2. **Yes — account ID itself is that key**, as long as there are meaningfully many distinct
   account IDs relative to the partition count. "Same key → same partition" doesn't mean "one key
   per partition" — many different account IDs will hash into each partition (as seen in the
   demo, where AAPL and VOD.L happened to share partition 1), spreading load across all
   partitions while still preserving order *per account*. The key doesn't need to be unique per
   partition to achieve parallelism; it needs to be the thing whose *internal* order matters.

3. **No genuine problem for either.** The risk dashboard only needs order *within an account*
   (same requirement as Settlement, satisfied by the same key), and the compliance log doesn't
   care about ordering at all — so a key chosen for Settlement's benefit doesn't cost either
   consumer anything. This is worth stating explicitly: the SAME topic, SAME partitioning, can
   correctly serve consumers with different (or looser) ordering needs, as long as it satisfies
   the *strictest* one.

## Part C — Offsets in Practice

1. **Settlement needs its own committed offset for partition 2 (specifically, that it had fully
   processed offset 47) stored somewhere durable** — Kafka's consumer offset tracking (or an
   equivalent Settlement manages itself) — *before* the crash, not reconstructed from memory
   after.

2. **Two failure modes, precisely**:
   - **Reprocessing**: if Settlement resumes from an offset earlier than 48 (say, restarting from
     offset 40 because that's the last point it durably recorded), it will process trades 40-47
     a second time — a real risk for a settlement system if those trades get double-counted.
   - **Skipping**: if Settlement resumes from an offset later than 48 (assuming it had gotten
     further than it actually had), any trades between its true last-processed point and its
     assumed resume point are silently never processed at all — a settlement gap with no error
     raised anywhere.

   Both are real, distinct failure modes with opposite consequences (double-processing vs
   data loss) — which is exactly why *when* and *how often* a consumer commits its offset is a
   deliberate design decision, not an afterthought. (Module 8's data-quality content picks this
   up directly.)
