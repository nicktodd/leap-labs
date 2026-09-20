package com.neueda.leap.mission.stream;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.util.List;
import java.util.Properties;

// Stands in for the Spring week's mission service. acceptOrder() is the same
// core logic the mission service already has - what's NEW is the publish()
// call at the end, implementing Module 6's design exactly as specified:
// topic = trade-events, partition key = accountId.
public class OrderService {

    record Order(String accountId, String ticker, String side, double quantity) {}

    private final KafkaProducer<String, String> producer;

    public OrderService(KafkaProducer<String, String> producer) {
        this.producer = producer;
    }

    // The mission service's existing order-acceptance logic (from the Spring week) -
    // unchanged. Validation, persistence, etc. would happen here in the
    // real service. Publishing is an ADDITION, not a rewrite.
    public void acceptOrder(Order order) throws Exception {
        System.out.println("OrderService: order accepted - " + order);
        publishTradeEvent(order);
    }

    // NEW this sprint: every accepted order also publishes a trade event.
    // The mission service does not know or care who (if anyone) consumes it.
    private void publishTradeEvent(Order order) throws Exception {
        String value = String.format("%s,%s,%.0f", order.ticker(), order.side(), order.quantity());
        ProducerRecord<String, String> record =
                new ProducerRecord<>("trade-events", order.accountId(), value);

        RecordMetadata metadata = producer.send(record).get();
        System.out.printf("  -> published to trade-events: partition=%d offset=%d%n",
                metadata.partition(), metadata.offset());
    }

    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            OrderService orderService = new OrderService(producer);

            List<Order> orders = List.of(
                    new Order("ACC-001", "AAPL", "BUY", 100),
                    new Order("ACC-002", "VOD.L", "BUY", 500),
                    new Order("ACC-001", "AAPL", "SELL", 40),
                    new Order("ACC-003", "GILT10", "BUY", 2000)
            );

            for (Order order : orders) {
                orderService.acceptOrder(order);
            }
        }
    }
}
