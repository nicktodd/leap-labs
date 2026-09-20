# Module 9 - Model Answers

`FraudDetectionConsumer.java` in this folder is the completed, verified implementation.

## The error, as it actually appeared

```
Exception in thread "main" org.apache.kafka.common.errors.RecordDeserializationException:
Error deserializing KEY for partition trade-events-1 at offset 0. If needed, please seek
past the record to continue consumption.
...
Caused by: org.apache.kafka.common.errors.SerializationException:
Size of data received by IntegerDeserializer is not 4
	at org.apache.kafka.common.serialization.IntegerDeserializer.deserialize(...)
```

## Root cause, in one sentence

The consumer was configured with `key.deserializer = IntegerDeserializer`, but `OrderService`
publishes keys as account IDs (`"ACC-001"`) using a `StringSerializer` - the bytes on the topic
were never a 4-byte integer, so deserialization fails the moment the consumer tries to read them.

## The fix

Change `key.deserializer` from `IntegerDeserializer` to `StringDeserializer`, matching
`SettlementConsumer`'s (and the producer's) configuration exactly.

## Verified output after the fix

```
FraudDetectionConsumer polling for up to 10 seconds...
Fraud check: account=ACC-001  partition=1 offset=0  AAPL,BUY,100
Fraud check: account=ACC-001  partition=1 offset=1  AAPL,SELL,40
Fraud check: account=ACC-003  partition=1 offset=2  GILT10,BUY,2000
Fraud check: account=ACC-002  partition=0 offset=0  VOD.L,BUY,500
FraudDetectionConsumer finished - received 4 events.
```

## Talking points

- **"Size of data received by IntegerDeserializer is not 4"** is a genuinely confusing message
  to a first-time reader - it doesn't say "wrong deserializer" or name the actual key value. This
  is a good example of why reading the `Caused by:` chain matters more than the top-level
  exception name (`RecordDeserializationException` alone tells you almost nothing).
- If a team asked GenAI to explain this: a plausible but WRONG answer is "the message is
  corrupted" or "the topic has mixed data types" - technically not false, but it skips past the
  actual, checkable cause (a config mismatch between this consumer and the producer). The
  verification step in Part B - comparing against `SettlementConsumer`'s config - is what catches
  a shallow explanation before it gets accepted.
- The deserializer must match what the PRODUCER wrote, not what "seems right" for the data's
  logical type. Account IDs happen to often look numeric-adjacent (`ACC-001`) but they were never
  serialized as integers - the fix is about matching the actual bytes on the wire, not about
  picking the deserializer that looks most correct in isolation.
