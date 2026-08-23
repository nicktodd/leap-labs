package com.neueda.leap.sprint5;

import java.util.List;
import java.util.Map;
import java.util.Set;

// Kata 2: the collections framework.
// TODO: implement all three methods below, using List/Map/Set as appropriate.
// This is the same shape as Sprint 4 Module 3's plain-Python trade summary -
// same logic, Java's collection types instead of list/dict/set.
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
