package com.neueda.leap.sprint5;

// Kata D: interfaces - a capability, not a hierarchy.
// This class represents a flat annual account-servicing charge. It is NOT an
// Instrument (no ticker, not a tradable thing) - it must implement Feeable
// DIRECTLY, with no relationship to the Instrument class at all.
// TODO: implement calculateFee to always return 30.00, regardless of tradeValue
// (the parameter is part of the Feeable contract but isn't used by this fee).
public class AnnualServiceFee implements Feeable {

    @Override
    public double calculateFee(double tradeValue) {
        throw new UnsupportedOperationException("TODO: implement calculateFee");
    }
}
