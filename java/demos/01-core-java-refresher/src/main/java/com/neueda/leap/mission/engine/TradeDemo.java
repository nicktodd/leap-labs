package com.neueda.leap.mission.engine;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class TradeDemo {

    public static void main(String[] args) {

        // --- Part 1: types and control flow ---
        // Java is statically typed: every variable's type is declared and checked
        // by the compiler, before the program ever runs.
        String tradeId = "T0001";
        double quantity = 120;
        int wholeShares = 120;        // int is 32-bit; use long for a bigger range
        boolean isBuy = true;

        System.out.println(tradeId + ": quantity=" + quantity + " isBuy=" + isBuy);

        // if/else: braces mark each block, and the condition needs parentheses
        double value = 22238.40;
        String size;
        if (value > 20000) {
            size = "LARGE";
        } else {
            size = "NORMAL";
        }
        System.out.println("Size: " + size);

        // --- Part 2: the collections framework ---
        // The big three: List (typically ArrayList), Map (typically HashMap),
        // and Set (typically HashSet).
        // Java's collections are all GENERIC: List<Trade> means "a list that only
        // ever holds Trade objects" - the compiler enforces this at compile time.
        List<Trade> trades = new ArrayList<>();
        trades.add(new Trade("T0001", "Alice Chen", "AAPL", 120, 185.32, "BUY"));
        trades.add(new Trade("T0002", "Ben Whitfield", "MSFT", 60, 402.11, "BUY"));
        trades.add(new Trade("T0003", "Alice Chen", "AAPL", 40, 186.10, "SELL"));

        double totalValue = 0.0;
        for (Trade trade : trades) {
            totalValue += trade.getValue();
        }
        System.out.println("Total value: " + totalValue);

        // Building a summary Map: look up the running total for a key, defaulting
        // to 0.0 if it isn't there yet, then write the updated total back.
        Map<String, Double> valueByInstrument = new HashMap<>();
        for (Trade trade : trades) {
            String key = trade.getInstrument();
            double existing = valueByInstrument.getOrDefault(key, 0.0);
            valueByInstrument.put(key, existing + trade.getValue());
        }
        System.out.println("Value by instrument: " + valueByInstrument);

        // Set: holds only distinct values
        Set<String> distinctClients = new HashSet<>();
        for (Trade trade : trades) {
            distinctClients.add(trade.getClientName());
        }
        System.out.println("Distinct clients: " + distinctClients);

        // --- Part 3: checked vs unchecked exceptions ---

        // Unchecked (RuntimeException): the compiler does NOT force you to handle
        // this. Java throws it, and if nothing catches it, the program crashes.
        try {
            double parsed = Double.parseDouble("not-a-number");
        } catch (NumberFormatException e) {
            System.out.println("Caught unchecked exception: " + e.getMessage());
        }

        // Checked (extends Exception, not RuntimeException): the compiler REQUIRES
        // every caller to either catch it or declare "throws" - this forces a
        // conscious decision about how to handle a foreseeable failure.
        try {
            Trade badTrade = parseTradeLine("T0099,Unknown,???,-5,0.00,BUY");
        } catch (MalformedTradeException e) {
            System.out.println("Caught checked exception: " + e.getMessage());
        }
    }

    // "throws MalformedTradeException" in the method signature is what makes this
    // a checked exception - every caller must acknowledge it, at compile time.
    private static Trade parseTradeLine(String line) throws MalformedTradeException {
        String[] parts = line.split(",");
        double quantity = Double.parseDouble(parts[3]);
        if (quantity <= 0) {
            throw new MalformedTradeException("quantity must be positive, got " + quantity);
        }
        return new Trade(parts[0], parts[1], parts[2], quantity,
                Double.parseDouble(parts[4]), parts[5]);
    }
}
