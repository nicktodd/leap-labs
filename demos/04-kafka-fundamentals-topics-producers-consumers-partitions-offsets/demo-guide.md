# Module 4 Demo Guide — Kafka Fundamentals: Topics, Producers, Consumers, Partitions, Offsets

No Kafka installed yet — that's Module 5. Today is entirely about the vocabulary, made concrete
with a deliberately simplified in-memory stand-in before any real infrastructure enters the
picture.

## Run It

```bash
mvn compile
java -cp target/classes com.fidelity.leap.sprint7.PartitionedTopicSimulator
```

## Walk Through Each Term, Against Real Output

- **Topic**: `"trade-events"` — a named stream. One topic, many events over time.
- **Producer**: `produce(event)` — appends one event. In real Kafka this is a client library call
  over the network; here it's a method call, same idea.
- **Partition**: the topic was created with 3. Point at the output — events land in partition 0,
  1, or 2. **This is the concept most learners haven't met before**: a topic isn't one log, it's
  several independent logs.
- **Offset**: the number next to each event, within its own partition — `partition=1 offset=0`,
  `partition=1 offset=1`, and so on. An offset only means something *relative to its partition* —
  "offset 2" exists independently in partition 0, 1, and 2, referring to three different events.
- **Consumer**: `consumePartition(p)` — reads a partition's log sequentially, tracking its own
  position (offset). Kafka's server doesn't track "has this consumer read this yet" — the consumer
  does, which is why offsets matter so much.

## The Partition Key: Where the Real Insight Is

Point at the `produce` method: `Math.floorMod(event.ticker().hashCode(), partitions.size())`. The
**key** (here, the ticker) determines the partition — not randomly, not round-robin, but a
deterministic hash. Every `AAPL` event, no matter when it's produced, lands in the exact same
partition as every other `AAPL` event.

**Now point at the actual output**: `AAPL`'s three events appear in partition 1, in the exact
order they were produced — BUY, SELL, BUY. That ordering guarantee is real, and it's the entire
reason partition keys exist: **if downstream consumers need to process a ticker's events in the
order they happened (and for trade events, they do), the key has to be the ticker.**

## The Trade-off, Named Honestly

Ask the group: **is there a single, total order across the whole topic?** Point at the output
again — `CORPB1` (partition 0) and `GILT10` (partition 2) were produced *after* several `AAPL` and
`VOD.L` events, but nothing in the log tells you that relative ordering once you're looking at
partition 0 or 2 in isolation. **Kafka trades total ordering for parallelism**: more partitions
means more consumers can work in parallel, but only events sharing a key are ordered relative to
each other. This is the trade-off Module 6 asks learners to design around directly.

## Transition to the Lab

A guided worksheet: map each Kafka term just covered to a concrete piece of a real trade-event
scenario, before writing a single line of Kafka code (that starts in Module 5).
