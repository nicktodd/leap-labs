package com.neueda.leap.sprint5;

// Equities: a flat 0.1% commission.
public class EquityInstrument extends Instrument {

    private static final double FEE_RATE = 0.001;

    public EquityInstrument(String ticker) {
        super(ticker);
    }

    @Override
    public double calculateFee(double tradeValue) {
        return tradeValue * FEE_RATE;
    }
}
