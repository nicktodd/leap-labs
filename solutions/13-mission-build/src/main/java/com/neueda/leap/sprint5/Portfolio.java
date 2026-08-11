package com.neueda.leap.sprint5;

import java.util.HashMap;
import java.util.Map;

// New this module - but built from pieces you already know. Holds one Holding
// per ticker (composition, exactly like Module 4's class diagram), and a running
// total value used directly by OrderValidator's risk-limit check.
public class Portfolio {

    private final Map<String, Holding> holdings = new HashMap<>();
    private double totalValue;

    public Holding getHolding(String ticker) {
        return holdings.computeIfAbsent(ticker, t -> new Holding(0));
    }

    public double getTotalValue() {
        return totalValue;
    }

    public void adjustTotalValue(double delta) {
        totalValue += delta;
    }
}
