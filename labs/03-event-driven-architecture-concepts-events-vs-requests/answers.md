# Module 3 Lab — Events vs Requests: Answers

## Scenario A — End-of-Day Settlement

**Decision: Event**

The trading platform does not need an answer from the settlement system before it can proceed —
it is only announcing that a set of trades occurred today. Settlement can process the notification
asynchronously, within its own overnight window, without holding up the trading platform.
Building this as a request would couple the trading platform's ability to close the day to
the settlement system's availability and response time — a dependency that serves no business
purpose since the trading platform does not act on the settlement result in real time.

## Scenario B — A Live Price Feed

**Decision: Event**

The price feed is a continuous announcement — "the price of AAPL is now 152.30" — not a
question that expects a reply. The trading platform's risk engine consumes these announcements
and updates its internal state, but it does not need to wait for a confirmation from the feed
before processing the next price update. Building this as a request would require the feed to
wait for every consumer to acknowledge each price before publishing the next one, which is
both unnecessary and a bottleneck in high-frequency price movement.

## Scenario C — Monthly Client Statements

**Decision: Event**

Statement generation is triggered by a calendar event ("the month has ended") rather than by
a question that needs an answer. The system generating statements does not need to know whether
any downstream system (email delivery, client portal) has processed the statement before it
moves on — it announces "statement for ACC-001 is ready" and each consumer handles it
independently. A request-driven design would block statement generation until every consumer
acknowledged receipt, which adds unnecessary coupling and latency.

## Discussion Questions

### 1. Do batch/real-time and event/request ever point in genuinely different directions?

Scenario A demonstrates this clearly: End-of-Day Settlement is **batch** (Module 2) AND
**event** (Module 3). It runs once per day on a bounded dataset (batch), AND the trading
platform does not wait for a response from the settlement system (event). These are independent
axes: batch vs real-time describes *when* data moves and *how much* of it moves at once; event
vs request describes *whether the sender needs a response before it can proceed*. A batch job
can publish an event when it finishes, and a real-time stream can use a request-response pattern
to retrieve missing reference data. The two axes correlate in common patterns (real-time feeds
are usually event-driven; interactive UIs are usually request-driven) but they are not the same
question.

### 2. What breaks if one scenario is built the wrong way on this axis?

**Scenario B (price feed) built as a request (wrong pattern):**
Every consumer needing a price would have to ask the feed "what is the current price of AAPL?"
and wait for a response. At scale, with thousands of instruments and hundreds of consumers,
this becomes a query bottleneck: the feed must handle a firehose of inbound requests rather than
broadcasting a single outgoing event. More critically, there is a race condition: by the time
a consumer receives the response to its request, the price may have changed again. The feed's
own publish rate would be gated on how quickly consumers poll it — which is precisely the
staleness problem real-time streaming was chosen to avoid.

### 3. Can a consumer that genuinely needs an answer still be built on top of an event-driven system?

Yes — two patterns work. The first is a **reply-to pattern**: the consumer publishes a request
event to a topic, including its own consumer group ID or a correlation ID and a reply-to topic
name; the feed (or a request-handling service) consumes the request event and publishes the
answer to the reply-to topic; the consumer reads from the reply-to topic. This preserves
decoupling while enabling request-response semantics over Kafka.

The second is a **separate request-driven lookup alongside the event stream**: the consumer
subscribes to the price event stream for low-latency updates and also maintains a reference
data service it can query synchronously when it needs a confirmed current value (e.g. at trade
execution time). The event stream handles continuous updates; the request-response path handles
the cases where a definitive answer is required before proceeding. This is common in trading
systems where risk calculations use stream-updated prices but order execution validates against
a authoritative price service.
