# Module 5 - Model Answers

`SimpleProducer.java` and `SimpleConsumer.java` in this folder are the completed, verified
implementations.

## Verified output

Run against a real `apache/kafka:latest` broker in KRaft mode, topic `settlement-events`
(3 partitions):

```
--- PRODUCER ---
Sent key=ACC-001  value=SETTLED,AAPL,100    -> partition=1 offset=0
Sent key=ACC-002  value=SETTLED,VOD.L,500   -> partition=0 offset=0
Sent key=ACC-001  value=SETTLED,GILT10,2000 -> partition=1 offset=1
Sent key=ACC-003  value=SETTLED,CORPB1,1000 -> partition=1 offset=2
Sent key=ACC-002  value=SETTLED,AAPL,50     -> partition=0 offset=1
Producer finished - all 5 settlement events acknowledged by the broker.

--- CONSUMER ---
Consumer polling for up to 10 seconds...
Received partition=1 offset=0 key=ACC-001  value=SETTLED,AAPL,100
Received partition=1 offset=1 key=ACC-001  value=SETTLED,GILT10,2000
Received partition=1 offset=2 key=ACC-003  value=SETTLED,CORPB1,1000
Received partition=0 offset=0 key=ACC-002  value=SETTLED,VOD.L,500
Received partition=0 offset=1 key=ACC-002  value=SETTLED,AAPL,50
Consumer finished - received 5 events.
```

## Talking points

- **ACC-001's two events land in partition 1, at offsets 0 and 1** - production order preserved,
  exactly as Module 4's worksheet predicted for a key-based partition assignment.
- **ACC-002's two events land in partition 0, at offsets 0 and 1** - same guarantee, different
  partition, because the key hashed differently.
- **ACC-003 shares partition 1 with ACC-001** but that's fine - the ordering guarantee is *per
  key*, not per partition. ACC-003's single event doesn't need to be ordered relative to
  ACC-001's; it just happens to share space with them.
- The producer's `.get()` call is what makes `partition=` / `offset=` available to print at all -
  without waiting for the broker's acknowledgment, that metadata wouldn't exist yet on the
  client side.
- If the lab's stub is run before Part A/B are implemented, both throw immediately (a
  `ConfigException` for missing serializer/deserializer config) rather than silently doing
  nothing - the kata is designed to fail loud, not quiet.
