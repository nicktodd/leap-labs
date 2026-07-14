package com.fidelity.leap.sprint7;

import java.io.BufferedReader;
import java.io.FileReader;
import java.time.LocalDateTime;

// BATCH: a bounded, known-size dataset, processed as a single unit, on a
// schedule (here, whenever this main() is run - in production, a nightly
// cron/Jenkins job). The whole file exists before processing starts, and
// processing has a clear beginning, middle, and end.
public class BatchSettlementJob {

    public static void main(String[] args) throws Exception {
        System.out.println("[" + LocalDateTime.now() + "] Batch job started");

        BufferedReader br = new BufferedReader(new FileReader("src/main/resources/trades.csv"));
        String line = br.readLine(); // header
        int count = 0;
        double totalValue = 0;

        while ((line = br.readLine()) != null) {
            String[] fields = line.split(",");
            double quantity = Double.parseDouble(fields[2]);
            double price = Double.parseDouble(fields[3]);
            totalValue += quantity * price;
            count++;
        }
        br.close();

        System.out.println("[" + LocalDateTime.now() + "] Batch job finished - "
                + count + " trades, total value " + totalValue);
        System.out.println("The whole file was known and available before a single trade was processed.");
    }
}
