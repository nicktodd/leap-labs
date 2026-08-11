package com.neueda.leap.sprint7;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.util.Properties;
import java.util.concurrent.ExecutionException;

// A REAL producer, against a REAL Kafka broker - no more in-memory
// stand-ins (Module 4). Same concepts, real infrastructure: a topic,
// a partition key (the ticker), and a broker that assigns the partition
// and offset - not our own code, this time.
public class SimpleProducer {

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            String[][] trades = {
                    {"AAPL", "BUY,100,150.25"},
                    {"VOD.L", "BUY,500,89.40"},
                    {"AAPL", "SELL,30,151.00"},
                    {"GILT10", "BUY,2000,101.50"},
                    {"VOD.L", "SELL,200,89.55"},
            };

            for (String[] trade : trades) {
                String ticker = trade[0];
                String value = trade[1];
                ProducerRecord<String, String> record =
                        new ProducerRecord<>("trade-events", ticker, value);

                // .get() blocks until the broker acknowledges the write -
                // fine for this demo, where seeing real confirmation
                // matters more than throughput.
                RecordMetadata metadata = producer.send(record).get();
                System.out.printf("Sent key=%-7s value=%-16s -> partition=%d offset=%d%n",
                        ticker, value, metadata.partition(), metadata.offset());
            }
        }

        System.out.println("Producer finished - all 5 trade events acknowledged by the broker.");
    }
}
