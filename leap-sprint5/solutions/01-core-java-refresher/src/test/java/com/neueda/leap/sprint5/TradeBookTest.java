package com.neueda.leap.sprint5;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;

class TradeBookTest {

    private TradeBook book;

    @BeforeEach
    void setUp() {
        List<Trade> trades = List.of(
                new Trade("T0001", "Alice Chen", "AAPL", 120, 185.32, "BUY"),
                new Trade("T0002", "Ben Whitfield", "MSFT", 60, 402.11, "BUY"),
                new Trade("T0003", "Alice Chen", "AAPL", 40, 186.10, "SELL")
        );
        book = new TradeBook(trades);
    }

    @Test
    void sumsTotalValueAcrossAllTrades() {
        double expected = (120 * 185.32) + (60 * 402.11) + (40 * 186.10);
        assertEquals(expected, book.totalValue(), 0.001);
    }

    @Test
    void sumsValueByInstrument() {
        Map<String, Double> byInstrument = book.valueByInstrument();
        double expectedAapl = (120 * 185.32) + (40 * 186.10);
        double expectedMsft = 60 * 402.11;

        assertEquals(expectedAapl, byInstrument.get("AAPL"), 0.001);
        assertEquals(expectedMsft, byInstrument.get("MSFT"), 0.001);
        assertEquals(2, byInstrument.size());
    }

    @Test
    void findsDistinctClientsWithNoDuplicates() {
        Set<String> clients = book.distinctClients();
        assertEquals(Set.of("Alice Chen", "Ben Whitfield"), clients);
        assertEquals(2, clients.size());
    }
}
