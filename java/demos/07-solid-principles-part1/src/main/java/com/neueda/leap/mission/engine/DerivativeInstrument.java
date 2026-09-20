package com.neueda.leap.mission.engine;

// OCP IN ACTION. The business just asked for a new instrument type, with its own
// fee rule (a flat 2%). Notice what did NOT need to change to support this:
// Instrument.java, Feeable.java, Order.java, FeeAggregator.java,
// FeeReportFormatter.java - none of them were touched. The system is "closed for
// modification" (nothing existing changed) but "open for extension" (a whole new
// instrument type just slotted in) - that's the O in SOLID.
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
