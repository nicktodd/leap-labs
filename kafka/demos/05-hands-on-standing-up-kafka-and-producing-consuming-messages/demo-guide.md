# Module 5 Demo Guide - Hands-on: Standing Up Kafka & Producing/Consuming Messages

Module 4's concepts, against a real broker for the first time. Same vocabulary - topic,
partition, offset, producer, consumer - now backed by real infrastructure instead of an in-memory
stand-in.

## Stand Up Kafka

```bash
docker run -d --name kafka-missionstream -p 9092:9092 apache/kafka:latest
```

The official `apache/kafka` image runs in **KRaft mode** - no separate ZooKeeper container
needed, unlike older Kafka setups the group may have seen referenced elsewhere. One container,
one broker, ready on `localhost:9092`.

## Create the Topic

```bash
docker exec kafka-missionstream /opt/kafka/bin/kafka-topics.sh --create \
  --topic trade-events --bootstrap-server localhost:9092 \
  --partitions 3 --replication-factor 1

docker exec kafka-missionstream /opt/kafka/bin/kafka-topics.sh --describe \
  --topic trade-events --bootstrap-server localhost:9092
```

Point at the `--describe` output: three partitions, each with a leader - this is Module 4's
"anatomy of a topic" diagram, as a real, running thing instead of a picture.

## Run the Producer

```bash
mvn compile
mvn dependency:build-classpath -Dmdep.outputFile=cp.txt
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.mission.stream.SimpleProducer
```

Point at the output: `partition=0 offset=0`, `partition=1 offset=0`, and so on - **the broker
assigned these**, not our own code (contrast directly with Module 4's `Math.floorMod` running
locally). `producer.send(record).get()` blocks until the broker acknowledges the write - worth
naming explicitly as a design choice (fire-and-forget vs waiting for acknowledgment is a real,
consequential setting in a production producer).

## Run the Consumer

```bash
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.mission.stream.SimpleConsumer
```

**Compare the output directly against Module 4's prediction**: AAPL's events (partition 0,
offsets 0 then 1) arrive in production order - BUY, then SELL. VOD.L's events (partition 1,
offsets 0 then 1) arrive in production order too. The ordering guarantee from Module 4 isn't a
theory anymore - it just happened, against a real broker, in this room.

## `group.id`: Point at It Directly

```java
props.put("group.id", "trade-events-demo-consumer");
```

Run the consumer a second time immediately. **Nothing new arrives** (the deadline hits with 0
events) - because this consumer group has already committed past offset 2 in partition 0 and
offset 1 in partition 1. Change `group.id` to something new and rerun: **all 5 events arrive
again**, from the beginning. This is Module 4's "who tracks the offset" question, answered
concretely: the broker tracks each consumer group's committed offset, and a new group starts with
no history at all.

## Transition to the Lab

Learners stand up their own Kafka container, create their own topic, and write their own minimal
producer/consumer pair - verified the same way this demo was: real broker, real partition
assignment, real ordering.
