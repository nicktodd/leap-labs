package com.neueda.leap.mission.stream;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

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
    static String validate(String[] cols) {
        String accountId = cols[0];
        String side = cols[2];
        String quantityStr = cols[3];
        String priceStr = cols[4];

        if (accountId.isBlank()) return "missing account_id";
        if (!side.equals("BUY") && !side.equals("SELL")) return "side must be BUY or SELL";

        double quantity;
        try {
            quantity = Double.parseDouble(quantityStr);
        } catch (NumberFormatException e) {
            return "quantity is not a number: '" + quantityStr + "'";
        }
        if (quantity <= 0) return "quantity must be positive, was " + quantity;

        try {
            Double.parseDouble(priceStr);
        } catch (NumberFormatException e) {
            return "price is not a number: '" + priceStr + "'";
        }

        return null;
    }
}
