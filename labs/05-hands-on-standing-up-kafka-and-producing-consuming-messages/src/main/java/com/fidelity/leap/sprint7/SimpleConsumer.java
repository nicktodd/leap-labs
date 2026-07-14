package com.fidelity.leap.sprint7;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

// KATA: consume the 5 settlement events SimpleProducer wrote, and print each
// one's partition, offset, key, and value.
public class SimpleConsumer {

    public static void main(String[] args) {
        // TODO 1: build a Properties object with:
        //   bootstrap.servers = localhost:9092
        //   key.deserializer / value.deserializer = StringDeserializer
        //   group.id = settlement-events-lab-consumer
        //   auto.offset.reset = earliest
        Properties props = new Properties();

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            // TODO 2: subscribe to the "settlement-events" topic.

            System.out.println("Consumer polling for up to 10 seconds...");
            long deadline = System.currentTimeMillis() + 10_000;
            int received = 0;
            while (System.currentTimeMillis() < deadline) {
                // TODO 3: poll for records (Duration.ofMillis(500) is a
                // reasonable timeout), and for each record received, print its
                // partition, offset, key, and value, and increment `received`.

                if (received >= 5) break; // this lab only produced 5 events
            }
            System.out.println("Consumer finished - received " + received + " events.");
        }
    }
}
