package com.neueda.leap.mission.stream;

import java.io.BufferedReader;
import java.io.FileReader;

// This is Module 1's TradeReportGenerator bug, reproduced in miniature: bad
// rows are caught and silently skipped. No count, no reason, no evidence
// anything was ever wrong.
public class SilentDropLoader {

    public static void main(String[] args) throws Exception {
        int loaded = 0;
        try (BufferedReader br = new BufferedReader(new FileReader("src/main/resources/trades.csv"))) {
            br.readLine(); // header
            String line;
            while ((line = br.readLine()) != null) {
                try {
                    String[] cols = line.split(",");
                    String accountId = cols[0];
                    String ticker = cols[1];
                    double quantity = Double.parseDouble(cols[2]);
                    double price = Double.parseDouble(cols[3]);
                    if (accountId.isBlank() || ticker.isBlank() || quantity <= 0) {
                        throw new IllegalArgumentException("bad row");
                    }
                    loaded++;
                } catch (Exception e) {
                    // skip bad row - just like Module 1's starter codebase
                }
            }
        }
        System.out.println("Loaded " + loaded + " trades.");
        System.out.println("(No record of how many rows were skipped, or why.)");
    }
}
