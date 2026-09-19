package com.neueda.leap.sprint5;

// One parsed row from the day's order file (mission-brief.md requirement 2).
// Deliberately a plain data holder - parsing is OrderBatchReader's job,
// validation is OrderValidator's job, this class does neither.
public class IncomingOrder {

    private final String clientId;
    private final Instrument instrument;
    private final double quantity;
    private final double price;
    private final boolean buy;

    public IncomingOrder(String clientId, Instrument instrument, double quantity, double price, boolean buy) {
        this.clientId = clientId;
        this.instrument = instrument;
        this.quantity = quantity;
        this.price = price;
        this.buy = buy;
    }

    public String getClientId() {
        return clientId;
    }

    public Instrument getInstrument() {
        return instrument;
    }

    public double getQuantity() {
        return quantity;
    }

    public double getPrice() {
        return price;
    }

    public boolean isBuy() {
        return buy;
    }
}
