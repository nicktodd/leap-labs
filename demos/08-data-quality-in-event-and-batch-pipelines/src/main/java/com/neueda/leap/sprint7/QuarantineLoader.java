package com.neueda.leap.sprint7;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

// The fix: every row is explicitly validated against named rules. Rows that
// fail are QUARANTINED - kept, counted, and labelled with why - not thrown
// away.
public class QuarantineLoader {

    record QuarantinedRow(int lineNumber, String rawLine, String reason) {}

    public static void main(String[] args) throws Exception {
        List<String[]> valid = new ArrayList<>();
        List<QuarantinedRow> quarantined = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader("src/main/resources/trades.csv"))) {
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

    // Returns null if the row is valid, otherwise the specific reason it failed.
    static String validate(String[] cols) {
        if (cols.length < 4) return "wrong number of columns";
        String accountId = cols[0];
        String ticker = cols[1];
        String quantityStr = cols[2];

        if (accountId.isBlank()) return "missing account_id";
        if (ticker.isBlank()) return "missing ticker";

        double quantity;
        try {
            quantity = Double.parseDouble(quantityStr);
        } catch (NumberFormatException e) {
            return "quantity is not a number: '" + quantityStr + "'";
        }
        if (quantity <= 0) return "quantity must be positive, was " + quantity;

        return null;
    }
}
