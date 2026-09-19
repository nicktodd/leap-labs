package com.neueda.leap.sprint5;

// Funds: a flat $2 fee, regardless of trade size - a genuinely different fee
// structure to EquityInstrument's percentage-based one. Each subclass owns its own
// rule; nothing about that rule lives in the shared Instrument base.
public class FundInstrument extends Instrument {

    private static final double FLAT_FEE = 2.00;

    public FundInstrument(String ticker) {
        super(ticker);
    }

    @Override
    public double calculateFee(double tradeValue) {
        return FLAT_FEE;
    }
}
