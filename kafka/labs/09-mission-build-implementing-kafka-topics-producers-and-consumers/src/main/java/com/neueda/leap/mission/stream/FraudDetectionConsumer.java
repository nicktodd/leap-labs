package com.neueda.leap.mission.stream;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

// KATA: this is Module 6's fourth consumer group - fraud detection - reading
// the SAME trade-events topic the demo's OrderService already published to.
//
// It was written by copying SettlementConsumer and changing the group.id -
// but it does not run. Run it, read the real stack trace, and fix it.
// Consider asking GenAI to explain the error - but verify its explanation
// against the actual Kafka client docs before trusting it (the Java week's
// critical-evaluation habit, applied here).
public class FraudDetectionConsumer {

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.IntegerDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("group.id", "fraud-detection-service");
        props.put("auto.offset.reset", "earliest");

        try (KafkaConsumer<Integer, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(List.of("trade-events"));

            System.out.println("FraudDetectionConsumer polling for up to 10 seconds...");
            long deadline = System.currentTimeMillis() + 10_000;
            int received = 0;
            while (System.currentTimeMillis() < deadline) {
                ConsumerRecords<Integer, String> records = consumer.poll(Duration.ofMillis(500));
                for (ConsumerRecord<Integer, String> record : records) {
                    System.out.printf("Fraud check: account=%s partition=%d offset=%d  %s%n",
                            record.key(), record.partition(), record.offset(), record.value());
                    received++;
                }
            }
            System.out.println("FraudDetectionConsumer finished - received " + received + " events.");
        }
    }
}
