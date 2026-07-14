# Module 9 Demo Guide — Mission Build: Implementing Kafka Topics, Producers & Consumers

This is Module 6's design, built. Same topic name, same partition key, same reasoning —
now real code, publishing from something that stands in for the mission service itself.

## Setup

Reuse `kafka-sprint7` (from Module 5), and make sure `trade-events` exists with 3 partitions
(created in Module 5/6):

```bash
docker exec kafka-sprint7 /opt/kafka/bin/kafka-topics.sh --describe \
  --topic trade-events --bootstrap-server localhost:9092
```

```bash
mvn compile
mvn dependency:build-classpath -Dmdep.outputFile=cp.txt
```

## Run the Order Service

```bash
java -cp "target/classes;$(cat cp.txt)" com.fidelity.leap.sprint7.OrderService
```

Verified output:

```
OrderService: order accepted - Order[accountId=ACC-001, ticker=AAPL, side=BUY, quantity=100.0]
  -> published to trade-events: partition=1 offset=0
OrderService: order accepted - Order[accountId=ACC-002, ticker=VOD.L, side=BUY, quantity=500.0]
  -> published to trade-events: partition=0 offset=0
OrderService: order accepted - Order[accountId=ACC-001, ticker=AAPL, side=SELL, quantity=40.0]
  -> published to trade-events: partition=1 offset=1
OrderService: order accepted - Order[accountId=ACC-003, ticker=GILT10, side=BUY, quantity=2000.0]
  -> published to trade-events: partition=1 offset=2
```

**Point at `acceptOrder()` directly**: this is the mission service's existing order-acceptance
logic (Sprint 6), unchanged. `publishTradeEvent()` is the ONLY new thing — a single method call
added at the end. Nothing about how orders are validated or processed changed.

## Run the Settlement Consumer

```bash
java -cp "target/classes;$(cat cp.txt)" com.fidelity.leap.sprint7.SettlementConsumer
```

Verified output:

```
SettlementConsumer polling for up to 10 seconds...
Settlement received: account=ACC-001  partition=1 offset=0  AAPL,BUY,100
Settlement received: account=ACC-001  partition=1 offset=1  AAPL,SELL,40
Settlement received: account=ACC-003  partition=1 offset=2  GILT10,BUY,2000
Settlement received: account=ACC-002  partition=0 offset=0  VOD.L,BUY,500
SettlementConsumer finished - received 4 events.
```

ACC-001's BUY then SELL: partition 1, offsets 0 then 1 — production order, exactly what Module
6's design promised. `SettlementConsumer` never talks to `OrderService` directly — it doesn't
even run in the same process. That's the decoupling this sprint's mission is built around.

## Point at the Decoupling, Explicitly

`OrderService` has no idea `SettlementConsumer` exists. It doesn't import it, call it, or wait
for it. If the risk dashboard, fraud detection, or compliance consumers from Module 6's design
were also running right now, `OrderService` would behave identically — same four `publish()`
calls, same four log lines. Adding a new downstream consumer is a change to that consumer's code,
never to `OrderService`.

## Transition to the Lab

Teams implement the SAME pattern for a consumer they haven't built before — and hit a real,
unfamiliar Kafka error along the way, exactly like production. Interpreting that error
critically (using GenAI as a second opinion, not an oracle) is deliberately part of the exercise.
