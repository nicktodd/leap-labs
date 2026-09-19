package com.neueda.leap.sprint5;

public class OrderExecutor {

    private final ReportWriter writer;

    public OrderExecutor(ReportWriter writer) {
        this.writer = writer;
    }

    public double execute(Order order) {
        double fee = order.calculateFee();
        writer.write(order.getClientId() + ": $" + fee);
        return fee;
    }
}
