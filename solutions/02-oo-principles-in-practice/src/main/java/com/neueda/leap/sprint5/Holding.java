package com.neueda.leap.sprint5;

public class Holding {

    private double quantity;

    public Holding(double initialQuantity) {
        if (initialQuantity < 0) {
            throw new IllegalArgumentException("initial quantity cannot be negative");
        }
        this.quantity = initialQuantity;
    }

    public double getQuantity() {
        return quantity;
    }

    public void adjust(double delta) {
        double newQuantity = quantity + delta;
        if (newQuantity < 0) {
            throw new IllegalArgumentException(
                    "adjustment would make quantity negative: " + quantity + " + " + delta);
        }
        quantity = newQuantity;
    }
}
