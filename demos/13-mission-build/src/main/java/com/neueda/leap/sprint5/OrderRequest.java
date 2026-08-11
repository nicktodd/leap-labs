package com.neueda.leap.sprint5;

// A slightly richer stand-in for an incoming order than Modules 7-9's Order class -
// it carries quantity and price separately, because Module 3's validation rules
// (see shared/mission-brief.md) need both independently, not just a combined
// trade value.
public class OrderRequest {

    private final double quantity;
    private final double price;
    private final boolean buy;

    public OrderRequest(double quantity, double price, boolean buy) {
        this.quantity = quantity;
        this.price = price;
        this.buy = buy;
    }

    public double getQuantity() {
        return quantity;
    }

    public double getPrice() {
        return price;
    }

    public boolean isBuy() {
        return buy;
    }

    public double tradeValue() {
        return quantity * price;
    }
}
