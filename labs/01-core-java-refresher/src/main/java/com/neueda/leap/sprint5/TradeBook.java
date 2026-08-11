package com.neueda.leap.sprint5;

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
        double total = 0;
        for (Trade trade : trades) {
            total += trade.getValue();
        }
        return total;
    }

    public Map<String, Double> valueByInstrument() {
        Map<String, Double> map = new HashMap<>();
        for (Trade trade : trades) {
            String instrument = trade.getInstrument();
            map.put(instrument, map.getOrDefault(instrument, 0.0) + trade.getValue());
        }
        return map;
    }

    public Set<String> distinctClients() {
        Set<String> clients = new HashSet<>();
        for (Trade trade : trades) {
            clients.add(trade.getClientName());
        }
        return clients;
    }
}
