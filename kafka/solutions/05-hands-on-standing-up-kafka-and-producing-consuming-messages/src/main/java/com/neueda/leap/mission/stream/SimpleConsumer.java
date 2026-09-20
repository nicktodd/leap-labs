package com.neueda.leap.mission.stream;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

public class SimpleConsumer {

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("group.id", "settlement-events-lab-consumer");
        props.put("auto.offset.reset", "earliest");

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(List.of("settlement-events"));

            System.out.println("Consumer polling for up to 10 seconds...");
            long deadline = System.currentTimeMillis() + 10_000;
            int received = 0;
            while (System.currentTimeMillis() < deadline) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(500));
                for (ConsumerRecord<String, String> record : records) {
                    System.out.printf("Received partition=%d offset=%d key=%-8s value=%s%n",
                            record.partition(), record.offset(), record.key(), record.value());
                    received++;
                }
                if (received >= 5) break;
            }
            System.out.println("Consumer finished - received " + received + " events.");
        }
    }
}
