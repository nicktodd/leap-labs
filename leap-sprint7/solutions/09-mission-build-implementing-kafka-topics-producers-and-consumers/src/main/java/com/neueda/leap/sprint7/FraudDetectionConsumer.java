package com.neueda.leap.sprint7;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

// Fixed: key.deserializer must match what the producer actually wrote.
// OrderService publishes with a StringSerializer key (accountId, e.g.
// "ACC-001") - IntegerDeserializer can never parse that, because it isn't
// a number at all, let alone a 4-byte one.
public class FraudDetectionConsumer {

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
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
                    System.out.printf("Fraud check: account=%-8s partition=%d offset=%d  %s%n",
                            record.key(), record.partition(), record.offset(), record.value());
                    received++;
                }
            }
            System.out.println("FraudDetectionConsumer finished - received " + received + " events.");
        }
    }
}
