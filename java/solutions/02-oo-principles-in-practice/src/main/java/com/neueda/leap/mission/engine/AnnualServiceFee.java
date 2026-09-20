package com.neueda.leap.mission.engine;

public class AnnualServiceFee implements Feeable {

    private static final double FLAT_FEE = 30.00;

    @Override
    public double calculateFee(double tradeValue) {
        return FLAT_FEE;
    }
}
