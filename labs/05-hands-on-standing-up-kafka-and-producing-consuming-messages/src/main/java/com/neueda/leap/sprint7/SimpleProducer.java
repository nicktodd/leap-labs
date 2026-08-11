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
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

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

                ProducerRecord<String, String> record =
                        new ProducerRecord<>("settlement-events", accountId, value);

                RecordMetadata metadata = producer.send(record).get();
                System.out.printf("Sent: key=%s partition=%d offset=%d value=%s%n",
                        accountId, metadata.partition(), metadata.offset(), value);
            }
        }

        System.out.println("Producer finished - all 5 settlement events acknowledged by the broker.");
    }
}
