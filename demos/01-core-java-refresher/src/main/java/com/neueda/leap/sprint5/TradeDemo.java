package com.neueda.leap.sprint5;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class TradeDemo {

    public static void main(String[] args) {

        // --- Part 1: types and control flow ---
        // Python: quantity = 120                 (dynamically typed, inferred at runtime)
        // Java:   double quantity = 120;          (statically typed, checked at compile time)
        String tradeId = "T0001";   // Python str  -> Java String
        double quantity = 120;       // Python float -> Java double
        int wholeShares = 120;        // Python int has no width limit; Java int is 32-bit,
                                        // long is 64-bit if you need a bigger range
        boolean isBuy = true;          // Python True/False -> Java true/false, lowercase

        System.out.println(tradeId + ": quantity=" + quantity + " isBuy=" + isBuy);

        // if/else: same idea as Python, but braces instead of indentation, and the
        // condition needs parentheses
        double value = 22238.40;
        String size;
        if (value > 20000) {
            size = "LARGE";
        } else {
            size = "NORMAL";
        }
        System.out.println("Size: " + size);

        // --- Part 2: the collections framework ---
        // Python list  -> Java List (typically ArrayList)
        // Python dict  -> Java Map (typically HashMap)
        // Python set   -> Java Set (typically HashSet)
        // Java's collections are all GENERIC: List<Trade> means "a list that only
        // ever holds Trade objects" - the compiler enforces this, Python's list can
        // silently mix types.
        List<Trade> trades = new ArrayList<>();
        trades.add(new Trade("T0001", "Alice Chen", "AAPL", 120, 185.32, "BUY"));
        trades.add(new Trade("T0002", "Ben Whitfield", "MSFT", 60, 402.11, "BUY"));
        trades.add(new Trade("T0003", "Alice Chen", "AAPL", 40, 186.10, "SELL"));

        // for-each: same idea as Python's "for trade in trades:"
        double totalValue = 0.0;
        for (Trade trade : trades) {
            totalValue += trade.getValue();
        }
        System.out.println("Total value: " + totalValue);

        // Building a summary Map, the same shape as Module 3's Python dict-accumulation
        // pattern (totals.get(key, 0.0) + value), just with Java's Map API instead
        Map<String, Double> valueByInstrument = new HashMap<>();
        for (Trade trade : trades) {
            String key = trade.getInstrument();
            double existing = valueByInstrument.getOrDefault(key, 0.0);
            valueByInstrument.put(key, existing + trade.getValue());
        }
        System.out.println("Value by instrument: " + valueByInstrument);

        // Set: same idea as Python's set() for distinct values
        Set<String> distinctClients = new HashSet<>();
        for (Trade trade : trades) {
            distinctClients.add(trade.getClientName());
        }
        System.out.println("Distinct clients: " + distinctClients);

        // --- Part 3: checked vs unchecked exceptions ---

        // Unchecked (RuntimeException): the compiler does NOT force you to handle
        // this. Java throws it, and if nothing catches it, the program crashes -
        // the same behaviour as an uncaught Python exception.
        try {
            double parsed = Double.parseDouble("not-a-number");
        } catch (NumberFormatException e) {
            System.out.println("Caught unchecked exception: " + e.getMessage());
        }

        // Checked (extends Exception, not RuntimeException): the compiler REQUIRES
        // every caller to either catch it or declare "throws" - this class of
        // exception simply doesn't exist in Python, where every exception is
        // effectively "unchecked" from the compiler's point of view.
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
