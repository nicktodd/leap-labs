package com.neueda.leap.sprint5;

public class DerivativeInstrument extends Instrument {

    private static final double FEE_RATE = 0.02;

    public DerivativeInstrument(String ticker) {
        super(ticker);
    }

    @Override
    public double calculateFee(double tradeValue) {
        return tradeValue * FEE_RATE;
    }
}
