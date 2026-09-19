package com.neueda.leap.sprint5;

// The same "trade" you worked with in Sprint 4 (shared/trades.csv), now as a Java class
// instead of a pandas row. Fields are private (encapsulation) with public getters -
// Module 2 covers why that matters as a design decision, not just syntax.
public class Trade {

    private final String tradeId;
    private final String clientName;
    private final String instrument;
    private final double quantity;
    private final double price;
    private final String side; // "BUY" or "SELL"

    public Trade(String tradeId, String clientName, String instrument,
                 double quantity, double price, String side) {
        this.tradeId = tradeId;
        this.clientName = clientName;
        this.instrument = instrument;
        this.quantity = quantity;
        this.price = price;
        this.side = side;
    }

    public String getTradeId() {
        return tradeId;
    }

    public String getClientName() {
        return clientName;
    }

    public String getInstrument() {
        return instrument;
    }

    public double getQuantity() {
        return quantity;
    }

    public double getPrice() {
        return price;
    }

    public String getSide() {
        return side;
    }

    public double getValue() {
        return quantity * price;
    }

    @Override
    public String toString() {
        return tradeId + " " + side + " " + instrument + " worth " + getValue();
    }
}
