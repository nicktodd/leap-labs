package com.neueda.leap.mission.stream;

import java.util.ArrayList;
import java.util.List;

// A deliberately simplified, in-memory stand-in for a Kafka topic - no
// Kafka installed yet (that's Module 5). The goal here is the CONCEPTS:
// topic, partition, offset, and how a partition key affects ordering -
// made concrete without any new infrastructure to install first.
public class PartitionedTopicSimulator {

    record TradeEvent(String ticker, String type, double quantity, double price) {}

    // A TOPIC is a named stream of events - here, "trade-events". It's made
    // up of a fixed number of PARTITIONS, each an independent, ORDERED,
    // append-only log. Kafka guarantees order WITHIN a partition, never
    // across partitions.
    static class Topic {
        private final String name;
        private final List<List<TradeEvent>> partitions;

        Topic(String name, int partitionCount) {
            this.name = name;
            this.partitions = new ArrayList<>();
            for (int i = 0; i < partitionCount; i++) {
                partitions.add(new ArrayList<>());
            }
        }

        // The PRODUCER doesn't choose a partition directly - it supplies a
        // KEY (here, the ticker), and the same key ALWAYS hashes to the same
        // partition. That's what guarantees every AAPL event, in order,
        // lands in the same partition as every other AAPL event.
        void produce(TradeEvent event) {
            int partition = Math.floorMod(event.ticker().hashCode(), partitions.size());
            List<TradeEvent> log = partitions.get(partition);
            int offset = log.size(); // OFFSET: this event's position within ITS partition
            log.add(event);
            System.out.printf("[PRODUCE] topic=%s partition=%d offset=%d  key=%-7s %s %s%n",
                    name, partition, offset, event.ticker(), event.type(), event.quantity());
        }

        // A CONSUMER reads a partition sequentially from an offset it
        // tracks itself - Kafka remembers nothing about "has this consumer
        // seen this message" on the server side beyond the offset.
        void consumePartition(int partition) {
            System.out.println("[CONSUME] partition " + partition + " (offsets 0.."
                    + (partitions.get(partition).size() - 1) + "):");
            int offset = 0;
            for (TradeEvent event : partitions.get(partition)) {
                System.out.printf("  offset=%d  %s %s %.2f @ %.2f%n",
                        offset++, event.ticker(), event.type(), event.quantity(), event.price());
            }
        }

        int partitionCount() {
            return partitions.size();
        }
    }

    public static void main(String[] args) {
        Topic tradeEvents = new Topic("trade-events", 3);

        System.out.println("== Producing 8 trade events across a 3-partition topic ==");
        tradeEvents.produce(new TradeEvent("AAPL", "BUY", 100, 150.25));
        tradeEvents.produce(new TradeEvent("VOD.L", "BUY", 500, 89.40));
        tradeEvents.produce(new TradeEvent("AAPL", "SELL", 30, 151.00));
        tradeEvents.produce(new TradeEvent("GILT10", "BUY", 2000, 101.50));
        tradeEvents.produce(new TradeEvent("VOD.L", "SELL", 200, 89.55));
        tradeEvents.produce(new TradeEvent("AAPL", "BUY", 75, 149.80));
        tradeEvents.produce(new TradeEvent("CORPB1", "BUY", 1000, 98.75));
        tradeEvents.produce(new TradeEvent("VOD.L", "BUY", 150, 89.60));

        System.out.println();
        System.out.println("== Consuming each partition, in isolation ==");
        for (int p = 0; p < tradeEvents.partitionCount(); p++) {
            tradeEvents.consumePartition(p);
        }

        System.out.println();
        System.out.println("Notice: every AAPL event landed in the SAME partition, in the exact");
        System.out.println("order they were produced (BUY, SELL, BUY) - order is guaranteed PER KEY,");
        System.out.println("within a partition. There is no single, total order across partitions.");
    }
}
