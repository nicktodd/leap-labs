package com.neueda.leap.sprint7;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

// KATA: this is Module 6's fourth consumer group - fraud detection - reading
// the SAME trade-events topic the demo's OrderService already published to.
//
// Root-cause explanation (Part B): The original used IntegerDeserializer for
// the key, but the producer keyed events by account ID (a String), so the
// key bytes cannot be deserialized as an Integer - this causes a
// SerializationException at runtime. The fix is to use StringDeserializer
// for the key, matching how the producer serialized it.
public class FraudDetectionConsumer {

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        // FIX: was IntegerDeserializer - the producer uses String keys (account IDs),
        // so this must be StringDeserializer to avoid SerializationException.
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("group.id", "fraud-detection-service");
        props.put("auto.offset.reset", "earliest");

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(List.of("trade-events"));

            System.out.println("FraudDetectionConsumer polling for up to 10 seconds...");
            long deadline = System.currentTimeMillis() + 10_000;
            int received = 0;
            while (System.currentTimeMillis() < deadline) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(500));
                for (ConsumerRecord<String, String> record : records) {
                    System.out.printf("Fraud check: account=%s partition=%d offset=%d  %s%n",
                            record.key(), record.partition(), record.offset(), record.value());
                    received++;
                }
            }
            System.out.println("FraudDetectionConsumer finished - received " + received + " events.");
        }
    }
}
