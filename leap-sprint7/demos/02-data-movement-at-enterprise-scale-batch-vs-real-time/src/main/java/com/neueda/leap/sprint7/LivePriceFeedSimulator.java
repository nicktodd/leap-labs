package com.neueda.leap.sprint7;

import java.time.LocalDateTime;
import java.util.Random;

// REAL-TIME: an unbounded stream. There is no "whole file" to read - each
// price update arrives independently, whenever the market produces one,
// and gets handled the moment it arrives. There is no natural "end" -
// this would keep running for as long as the market is open.
//
// No Kafka yet - Modules 4-5 introduce the real infrastructure for this.
// This is deliberately the simplest possible version of the IDEA, so the
// batch/real-time contrast is visible before any new tooling gets involved.
public class LivePriceFeedSimulator {

    private static final String[] TICKERS = {"AAPL", "VOD.L", "ULVR.L"};

    public static void main(String[] args) throws InterruptedException {
        System.out.println("[" + LocalDateTime.now() + "] Live feed started - no end in sight");

        Random random = new Random(42);
        for (int i = 0; i < 6; i++) {
            Thread.sleep(800); // a price update arrives whenever it arrives, not on our schedule
            String ticker = TICKERS[random.nextInt(TICKERS.length)];
            double price = 50 + random.nextDouble() * 100;
            System.out.printf("[%s] PRICE UPDATE  %-7s %.2f  (handled immediately, on its own)%n",
                    LocalDateTime.now(), ticker, price);
        }

        System.out.println("[" + LocalDateTime.now() + "] (simulation stopped for the demo - a real feed wouldn't)");
    }
}
