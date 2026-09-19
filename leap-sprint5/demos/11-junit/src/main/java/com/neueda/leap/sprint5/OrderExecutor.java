package com.neueda.leap.sprint5;

// DIP FIX. OrderExecutor now depends on the ReportWriter ABSTRACTION, supplied
// through its constructor, not on any specific implementation it builds itself.
// The high-level policy (calculate a fee, report it) no longer knows or cares
// whether that report ends up on the console, in memory, or somewhere not
// invented yet - that decision is made once, at the point where an OrderExecutor
// is constructed, not baked into the class.
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
