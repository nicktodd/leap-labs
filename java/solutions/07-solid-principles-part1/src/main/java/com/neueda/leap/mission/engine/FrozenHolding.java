package com.neueda.leap.mission.engine;

public class FrozenHolding {

    private final Holding holding;

    public FrozenHolding(Holding holding) {
        this.holding = holding;
    }

    public double getQuantity() {
        return holding.getQuantity();
    }
}
