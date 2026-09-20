package com.neueda.leap.mission.engine;

// Kata B (DIP): depend on the ReportWriter ABSTRACTION, supplied through the
// constructor - do not construct a ConsoleReportWriter (or any other concrete
// writer) inside this class.
public class OrderExecutor {

    public OrderExecutor(ReportWriter writer) {
        throw new UnsupportedOperationException("TODO: implement constructor");
    }

    public double execute(Order order) {
        throw new UnsupportedOperationException("TODO: implement execute");
    }
}
