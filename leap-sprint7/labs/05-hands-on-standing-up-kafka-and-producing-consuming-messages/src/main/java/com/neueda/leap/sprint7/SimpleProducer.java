package com.neueda.leap.sprint7;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.util.Properties;
import java.util.concurrent.ExecutionException;

// KATA: send 5 settlement events to the "settlement-events" topic on your
// own running Kafka broker (localhost:9092), keyed by account ID.
public class SimpleProducer {

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        // TODO 1: build a Properties object with:
        //   bootstrap.servers = localhost:9092
        //   key.serializer / value.serializer = StringSerializer
        Properties props = new Properties();

        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            String[][] settlements = {
                    {"ACC-001", "SETTLED,AAPL,100"},
                    {"ACC-002", "SETTLED,VOD.L,500"},
                    {"ACC-001", "SETTLED,GILT10,2000"},
                    {"ACC-003", "SETTLED,CORPB1,1000"},
                    {"ACC-002", "SETTLED,AAPL,50"},
            };

            for (String[] settlement : settlements) {
                String accountId = settlement[0];
                String value = settlement[1];

                // TODO 2: build a ProducerRecord for topic "settlement-events",
                // keyed by accountId, with the given value.

                // TODO 3: send it, .get() the result (so the send is confirmed
                // before moving on), and print the partition and offset the
                // broker assigned - same pattern as Module 4's PRODUCE logging.

                throw new UnsupportedOperationException("TODO: implement the send loop");
            }
        }

        System.out.println("Producer finished - all 5 settlement events acknowledged by the broker.");
    }
}
