package com.neueda.leap.mission.stream;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.function.Function;

// Demo: the SAME six trade events, produced with two different partition key
// strategies, to make the design consequence of a key choice visible before
// any code gets written in Module 9.
public class PartitionKeyChoice {

    record TradeEvent(String eventId, String accountId, String ticker, String side) {}

    static List<List<TradeEvent>> produceWithKey(List<TradeEvent> events, int partitionCount,
                                                  Function<TradeEvent, String> keyFn) {
        List<List<TradeEvent>> partitions = new ArrayList<>();
        for (int i = 0; i < partitionCount; i++) partitions.add(new ArrayList<>());
        for (TradeEvent event : events) {
            String key = keyFn.apply(event);
            int partition = Math.floorMod(key.hashCode(), partitionCount);
            partitions.get(partition).add(event);
        }
        return partitions;
    }

    static void printPartitions(List<List<TradeEvent>> partitions) {
        for (int i = 0; i < partitions.size(); i++) {
            StringBuilder sb = new StringBuilder("  partition " + i + ": ");
            for (TradeEvent e : partitions.get(i)) {
                sb.append(e.accountId()).append("/").append(e.side()).append("  ");
            }
            System.out.println(sb.toString().isBlank() ? "  partition " + i + ": (empty)" : sb);
        }
    }

    public static void main(String[] args) {
        // ACC-001 buys AAPL then sells it. Settlement MUST see BUY before SELL.
        List<TradeEvent> events = List.of(
                new TradeEvent(UUID.randomUUID().toString(), "ACC-001", "AAPL", "BUY"),
                new TradeEvent(UUID.randomUUID().toString(), "ACC-002", "VOD.L", "BUY"),
                new TradeEvent(UUID.randomUUID().toString(), "ACC-001", "AAPL", "SELL"),
                new TradeEvent(UUID.randomUUID().toString(), "ACC-003", "GILT10", "BUY"),
                new TradeEvent(UUID.randomUUID().toString(), "ACC-002", "VOD.L", "SELL"),
                new TradeEvent(UUID.randomUUID().toString(), "ACC-001", "AAPL", "BUY")
        );

        System.out.println("=== Option A: partition key = eventId (unique per event) ===");
        List<List<TradeEvent>> byEventId = produceWithKey(events, 3, TradeEvent::eventId);
        printPartitions(byEventId);
        System.out.println("ACC-001's three events are scattered across different partitions.");
        System.out.println("A consumer reading one partition at a time CANNOT tell BUY happened");
        System.out.println("before SELL - each partition only knows its own slice.");

        System.out.println();
        System.out.println("=== Option B: partition key = accountId ===");
        List<List<TradeEvent>> byAccountId = produceWithKey(events, 3, TradeEvent::accountId);
        printPartitions(byAccountId);
        System.out.println("ACC-001's three events land in the SAME partition, in production");
        System.out.println("order: BUY, SELL, BUY. Settlement's ordering requirement is satisfied");
        System.out.println("by the key choice alone - no code in the consumer has to fix this up.");
    }
}
