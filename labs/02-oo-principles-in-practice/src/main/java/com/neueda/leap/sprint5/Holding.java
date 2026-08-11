package com.neueda.leap.sprint5;

public class Holding {

    private double quantity;

    public Holding(double initialQuantity) {
        if (initialQuantity < 0) {
            throw new IllegalArgumentException("Initial quantity cannot be negative: " + initialQuantity);
        }
        this.quantity = initialQuantity;
    }

    public double getQuantity() {
        return quantity;
    }

    public void adjust(double delta) {
        double result = quantity + delta;
        if (result < 0) {
            throw new IllegalArgumentException("Adjustment would result in negative quantity: " + result);
        }
        quantity = result;
    }
}
