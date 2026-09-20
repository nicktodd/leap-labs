package com.neueda.leap.mission.stream;

import java.time.LocalTime;

// REQUEST-DRIVEN: OrderService knows exactly who it needs to talk to, calls
// each one directly, and BLOCKS waiting for a response before moving on.
// Tight coupling: OrderService has a compile-time dependency on PricingService,
// RiskService, and ConfirmationService. Add a fourth thing that needs to know
// about a new order, and OrderService itself has to change.
public class RequestDrivenExample {

    static void log(String msg) {
        System.out.println("[" + LocalTime.now() + "] " + msg);
    }

    static double getPrice(String ticker) throws InterruptedException {
        log("  -> calling PricingService.getPrice(" + ticker + ")...");
        Thread.sleep(400); // simulate a real network call
        log("  <- PricingService responded");
        return 150.25;
    }

    static boolean checkRisk(String ticker, double quantity) throws InterruptedException {
        log("  -> calling RiskService.checkRisk(...)...");
        Thread.sleep(400);
        log("  <- RiskService responded");
        return true;
    }

    static void sendConfirmation(String ticker) throws InterruptedException {
        log("  -> calling ConfirmationService.send(...)...");
        Thread.sleep(400);
        log("  <- ConfirmationService responded");
    }

    public static void main(String[] args) throws InterruptedException {
        log("OrderService: placing order for AAPL");
        double price = getPrice("AAPL");
        boolean ok = checkRisk("AAPL", 100);
        sendConfirmation("AAPL");
        log("OrderService: order placement complete (price=" + price + ", riskOk=" + ok + ")");
        log("Notice: OrderService waited for ALL THREE calls, in order, one at a time.");
    }
}
