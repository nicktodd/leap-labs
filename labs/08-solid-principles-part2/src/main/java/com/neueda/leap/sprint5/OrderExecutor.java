package com.neueda.leap.sprint5;

// Kata B (DIP): depend on the ReportWriter ABSTRACTION, supplied through the
// constructor - do not construct a ConsoleReportWriter (or any other concrete
// writer) inside this class.
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
