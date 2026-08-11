package com.neueda.leap.sprint5;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@DisplayName("OrderProcessingEngine")
class OrderProcessingEngineTest {

    private Map<String, Client> clients;
    private OrderProcessingEngine engine;

    @BeforeEach
    void setUp() {
        clients = new HashMap<>();
        clients.put("C001", new Client("C001", 20000));
        clients.put("C002", new Client("C002", 5000));
        engine = new OrderProcessingEngine(clients, new OrderValidator(), new HoldingUpdater());
    }

    private List<IncomingOrder> read(String... lines) {
        return new OrderBatchReader(new InstrumentFactory()).readAll(List.of(lines));
    }

    @Nested
    @DisplayName("when an order is accepted")
    class WhenAccepted {

        @Test
        @DisplayName("records it in the report with its fee")
        void recordsAcceptedOrderWithFee() {
            SettlementReport report = engine.process(read("C001,AAPL,EQUITY,100,150.00,BUY"));

            assertTrue(report.render().contains("C001 AAPL: ACCEPTED, fee $15.0"));
        }

        @Test
        @DisplayName("updates the client's holding")
        void updatesHolding() {
            engine.process(read("C001,AAPL,EQUITY,100,150.00,BUY"));

            assertEquals(100.0, clients.get("C001").getPortfolio().getHolding("AAPL").getQuantity(), 0.0001);
        }

        @Test
        @DisplayName("updates the portfolio's total value")
        void updatesPortfolioValue() {
            engine.process(read("C001,AAPL,EQUITY,100,150.00,BUY"));

            assertEquals(15000.0, clients.get("C001").getPortfolio().getTotalValue(), 0.0001);
        }

        @Test
        @DisplayName("a subsequent sell decreases the holding correctly")
        void sellDecreasesHolding() {
            engine.process(read(
                    "C001,AAPL,EQUITY,100,150.00,BUY",
                    "C001,AAPL,EQUITY,20,150.00,SELL"
            ));

            assertEquals(80.0, clients.get("C001").getPortfolio().getHolding("AAPL").getQuantity(), 0.0001);
        }
    }

    @Nested
    @DisplayName("when an order is rejected")
    class WhenRejected {

        @Test
        @DisplayName("records it in the report with the reason, and charges no fee")
        void recordsRejectedOrderWithReason() {
            SettlementReport report = engine.process(read("C002,VWRL,FUND,1000,10.00,BUY"));

            assertTrue(report.render().contains("C002 VWRL: REJECTED - would exceed the client's risk limit"));
            assertTrue(report.render().contains("Total fees: $0.0"));
        }

        @Test
        @DisplayName("does not change the client's portfolio")
        void doesNotChangePortfolio() {
            engine.process(read("C002,VWRL,FUND,1000,10.00,BUY"));

            assertEquals(0.0, clients.get("C002").getPortfolio().getTotalValue(), 0.0001);
            assertEquals(0.0, clients.get("C002").getPortfolio().getHolding("VWRL").getQuantity(), 0.0001);
        }
    }

    @Test
    @DisplayName("processes a mixed batch, computing the correct total fees")
    void processesAMixedBatch() {
        SettlementReport report = engine.process(read(
                "C001,AAPL,EQUITY,100,150.00,BUY",
                "C001,VOD.L,BOND,50,10.00,BUY",
                "C002,VWRL,FUND,1000,10.00,BUY"
        ));

        assertTrue(report.render().contains("Total fees: $20.0"));
    }
}
