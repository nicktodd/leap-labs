package com.neueda.leap.sprint5;

public class Order {

    private final String clientId;
    private final Instrument instrument;
    private final double tradeValue;

    public Order(String clientId, Instrument instrument, double tradeValue) {
        this.clientId = clientId;
        this.instrument = instrument;
        this.tradeValue = tradeValue;
    }

    public String getClientId() {
        return clientId;
    }

    public Instrument getInstrument() {
        return instrument;
    }

    public double getTradeValue() {
        return tradeValue;
    }

    public double calculateFee() {
        return instrument.calculateFee(tradeValue);
    }
}
