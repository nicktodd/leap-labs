package com.neueda.leap.sprint5;

// Kata B (OCP): a new instrument type, with a flat 2% fee. Add this WITHOUT
// changing Instrument.java, Feeable.java, Order.java, or any existing instrument
// class - that's the whole point of the exercise.
public class DerivativeInstrument extends Instrument {

    public DerivativeInstrument(String ticker) {
        super(ticker);
    }

    @Override
    public double calculateFee(double tradeValue) {
        throw new UnsupportedOperationException("TODO: implement calculateFee");
    }
}
