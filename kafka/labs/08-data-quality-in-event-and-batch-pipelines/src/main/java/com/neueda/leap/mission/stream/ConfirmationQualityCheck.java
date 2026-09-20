package com.neueda.leap.mission.stream;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

// KATA: this loader compiles and runs, but validate() always returns null -
// every row is treated as valid, even the four bad ones. Implement the
// validation rules so the quarantine report actually catches them.
public class ConfirmationQualityCheck {

    record QuarantinedRow(int lineNumber, String rawLine, String reason) {}

    public static void main(String[] args) throws Exception {
        List<String[]> valid = new ArrayList<>();
        List<QuarantinedRow> quarantined = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader("src/main/resources/confirmations.csv"))) {
            br.readLine(); // header
            String line;
            int lineNumber = 1;
            while ((line = br.readLine()) != null) {
                lineNumber++;
                String[] cols = line.split(",", -1);
                String reason = validate(cols);
                if (reason == null) {
                    valid.add(cols);
                } else {
                    quarantined.add(new QuarantinedRow(lineNumber, line, reason));
                }
            }
        }

        System.out.println("=== Data Quality Report ===");
        System.out.println("Valid rows:       " + valid.size());
        System.out.println("Quarantined rows: " + quarantined.size());
        System.out.println();
        for (QuarantinedRow q : quarantined) {
            System.out.printf("  line %d: %-40s -> %s%n", q.lineNumber(), q.rawLine(), q.reason());
        }
    }

    // Columns: account_id, ticker, side, quantity, price
    //
    // TODO 1: return "missing account_id" if account_id is blank.
    // TODO 2: return "side must be BUY or SELL" if side is anything else.
    // TODO 3: return "quantity must be positive, was <value>" if quantity
    //         parses but is <= 0.
    // TODO 4: return "price is not a number: '<value>'" if price does not
    //         parse as a number (catch NumberFormatException).
    //
    // Return null if the row passes every rule.
    static String validate(String[] cols) {
        String accountId = cols[0];
        String ticker = cols[1];
        String side = cols[2];
        String quantityStr = cols[3];
        String priceStr = cols[4];

        return null;
    }
}
