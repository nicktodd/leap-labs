package com.neueda.leap.sprint5;

public class TradeClassifier {

    public static final double LARGE_THRESHOLD = 20000.0;

    public String classifySize(Trade trade) {
        if (trade.getValue() > LARGE_THRESHOLD) {
            return "LARGE";
        }
        return "NORMAL";
    }

    public String classifySide(Trade trade) {
        String side = trade.getSide();
        if ("BUY".equalsIgnoreCase(side)) {
            return "BUY";
        } else if ("SELL".equalsIgnoreCase(side)) {
            return "SELL";
        } else {
            return "UNKNOWN";
        }
    }
}
