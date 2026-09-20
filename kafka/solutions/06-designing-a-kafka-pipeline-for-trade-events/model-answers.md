# Module 6 - Model Answers

## Part A - Topic Design

1. **One topic.** All four systems need the same underlying data - every executed trade - just
   with different ordering/completeness requirements, not different content. Kafka topics are
   cheap for consumers to share: each of the four systems gets its own consumer group reading the
   whole topic independently, so one topic doesn't mean one system, or contention between them.
   Multiple topics would only be justified if the systems needed genuinely different data (e.g. a
   topic of raw trades vs a topic of pre-aggregated daily summaries) - not the case here.

2. **`trade-events`** - one clear, descriptive name; matches the naming style already used in
   Modules 4 and 5.

## Part B - Partition Key

1. **Account ID.** Settlement, the risk dashboard, and fraud detection all need one thing in
   common: a given account's own trades, in order. Account ID as the key guarantees every trade
   for `ACC-001` lands in the same partition, in production order - satisfying all three at once,
   with a single key choice.

2. **`eventId` would scatter every account's trades randomly across partitions** - exactly what
   the demo showed: ACC-001's BUY, SELL, BUY split across partitions 0 and 2, with no way for a
   consumer reading one partition to know what happened in another. It maximizes spread (good for
   raw parallelism) at the cost of the one property every consumer here actually needs: per-account
   order. A unique key is the right choice when NO consumer needs order - that's compliance, but
   compliance shares the topic with three systems that DO need it.

3. **No conflict in this scenario.** Every requirement above is "per-account order," at different
   strictness (Settlement/risk/fraud need it; compliance doesn't care). A key satisfying the
   strictest shared requirement (account ID) costs nothing to the systems with looser needs - this
   is the same principle from Module 4's worksheet, now applied to the real pipeline.

## Part C - Partition Count & Consumer Groups

1. **Start with a modest number (e.g. 6-12), not "as many as possible."** The real trade-off:
   more partitions means more consumer instances CAN work in parallel (within a consumer group),
   but each partition is also a unit of "how the broker tracks work" - too many, with too few
   consumers actually using them, adds overhead for no benefit. Partition count should roughly
   match expected consumer parallelism, not be maximized blindly, and CANNOT be safely decreased
   later without breaking the account-ID-to-partition mapping (rehashing changes which partition
   an account lands in).

2. **Four consumer groups - one per system** (Settlement, risk dashboard, compliance, fraud
   detection). Each is a genuinely separate downstream system needing the complete stream,
   tracked independently - exactly the "one group per system" pattern from Module 4's worksheet,
   now with a fourth system added.

3. **No - partition count and consumer group design control ordering and parallelism, not
   latency.** Fraud detection's "within a few seconds" requirement is about how often/promptly
   its consumer polls and processes, and how quickly a trade is produced and acknowledged - not
   about how many partitions exist. A single-partition topic with a fast-polling consumer can meet
   a latency target; a 50-partition topic with a consumer that only polls once a minute cannot.
   This is worth flagging explicitly: partitioning is a design lever, not a substitute for actually
   checking that a consumer runs often enough.
