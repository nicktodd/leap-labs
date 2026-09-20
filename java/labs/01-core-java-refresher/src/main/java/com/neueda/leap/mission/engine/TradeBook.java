package com.neueda.leap.mission.engine;

import java.util.List;
import java.util.Map;
import java.util.Set;

// Kata 2: the collections framework.
// TODO: implement all three methods below, using List/Map/Set as appropriate.
public class TradeBook {

    private final List<Trade> trades;

    public TradeBook(List<Trade> trades) {
        this.trades = trades;
    }

    // Sum of every trade's getValue() in this book.
    public double totalValue() {
        throw new UnsupportedOperationException("TODO: implement totalValue");
    }

    // A map of instrument -> total value traded in that instrument.
    public Map<String, Double> valueByInstrument() {
        throw new UnsupportedOperationException("TODO: implement valueByInstrument");
    }

    // The distinct set of client names in this book (no duplicates).
    public Set<String> distinctClients() {
        throw new UnsupportedOperationException("TODO: implement distinctClients");
    }
}
