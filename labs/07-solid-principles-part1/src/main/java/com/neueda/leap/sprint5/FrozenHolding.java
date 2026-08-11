package com.neueda.leap.sprint5;

public class FrozenHolding {

    private final Holding holding;

    public FrozenHolding(Holding holding) {
        this.holding = holding;
    }

    public double getQuantity() {
        return holding.getQuantity();
    }
}
