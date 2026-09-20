package com.neueda.leap.mission.engine;

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
