package com.neueda.leap.sprint5;

// DIP VIOLATION. OrderExecutor is "high-level" policy - it decides WHAT to do
// (calculate a fee, write a line about it). ConsoleReportWriter is "low-level"
// detail - it decides HOW output actually happens. Here, the high-level class
// directly constructs the low-level one, so it can never be pointed at any other
// kind of writer - not for testing, not for a future CSV or file destination -
// without editing BadOrderExecutor itself.
public class BadOrderExecutor {

    private final ConsoleReportWriter writer = new ConsoleReportWriter();

    public double execute(Order order) {
        double fee = order.calculateFee();
        writer.write(order.getClientId() + ": $" + fee);
        return fee;
    }
}
