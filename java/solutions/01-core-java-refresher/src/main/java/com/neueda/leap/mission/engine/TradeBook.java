package com.neueda.leap.mission.engine;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class TradeBook {

    private final List<Trade> trades;

    public TradeBook(List<Trade> trades) {
        this.trades = trades;
    }

    public double totalValue() {
        double total = 0.0;
        for (Trade trade : trades) {
            total += trade.getValue();
        }
        return total;
    }

    public Map<String, Double> valueByInstrument() {
        Map<String, Double> byInstrument = new HashMap<>();
        for (Trade trade : trades) {
            String key = trade.getInstrument();
            double existing = byInstrument.getOrDefault(key, 0.0);
            byInstrument.put(key, existing + trade.getValue());
        }
        return byInstrument;
    }

    public Set<String> distinctClients() {
        Set<String> clients = new HashSet<>();
        for (Trade trade : trades) {
            clients.add(trade.getClientName());
        }
        return clients;
    }
}
