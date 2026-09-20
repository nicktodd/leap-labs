package com.neueda.leap.mission.stream;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;

// EVENT-DRIVEN: OrderService publishes ONE fact - "an order happened" - and
// moves on immediately. It has no idea who's listening, how many listeners
// there are, or what they do with the event. No Kafka yet (Modules 4-5) -
// this is the simplest possible in-memory version of the IDEA, so the
// contrast with RequestDrivenExample is about the PATTERN, not the tooling.
public class EventDrivenExample {

    record OrderPlacedEvent(String ticker, double quantity) {}

    // A minimal pub/sub bus: publishers and subscribers never reference each
    // other directly. Kafka (Module 4 onward) is a much more capable, durable,
    // distributed version of exactly this idea.
    static class EventBus {
        private final List<Consumer<OrderPlacedEvent>> listeners = new ArrayList<>();
        private final ExecutorService pool = Executors.newFixedThreadPool(3);

        void subscribe(Consumer<OrderPlacedEvent> listener) {
            listeners.add(listener);
        }

        void publish(OrderPlacedEvent event) {
            for (Consumer<OrderPlacedEvent> listener : listeners) {
                pool.submit(() -> listener.accept(event));
            }
        }

        void warmUp() throws Exception {
            // Give the JVM its one-time thread-creation cost BEFORE the timed
            // part of the demo, so "publish() returns immediately" measures
            // the pattern, not JVM startup noise.
            pool.submit(() -> {}).get();
        }

        void shutdown() throws InterruptedException {
            pool.shutdown();
            pool.awaitTermination(5, TimeUnit.SECONDS);
        }
    }

    static long t0;

    static void log(String msg) {
        System.out.printf("[+%4dms] %s%n", System.currentTimeMillis() - t0, msg);
    }

    public static void main(String[] args) throws Exception {
        EventBus bus = new EventBus();

        // Three independent listeners. OrderService (below) will never know
        // any of them exist.
        bus.subscribe(event -> {
            sleep(600);
            log("  [PricingHistoryListener] recorded price context for " + event.ticker());
        });
        bus.subscribe(event -> {
            sleep(900);
            log("  [RiskAuditListener] logged order for compliance review: " + event.ticker());
        });
        bus.subscribe(event -> {
            sleep(300);
            log("  [ConfirmationListener] sent confirmation for " + event.ticker());
        });

        bus.warmUp();
        t0 = System.currentTimeMillis();

        log("OrderService: publishing OrderPlacedEvent(AAPL)");
        bus.publish(new OrderPlacedEvent("AAPL", 100));
        log("OrderService: publish() returned - NOT waiting for any listener");
        log("OrderService: doing other work immediately");

        bus.shutdown();
        log("(all listeners have now finished, for the demo's sake - a real bus would keep running)");
    }

    static void sleep(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
