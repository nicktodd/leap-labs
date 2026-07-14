package com.fidelity.leap.sprint7;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SettlementReporter {

    private static final Logger LOGGER = Logger.getLogger(SettlementReporter.class.getName());

    public static void main(String[] args) throws Exception {
        StringBuilder out = new StringBuilder();
        try (BufferedReader br = new BufferedReader(new FileReader(args[0]))) {
            String header = br.readLine();
            String line;
            while ((line = br.readLine()) != null) {
                String[] cols = line.split(",");
                out.append(cols[0]).append(",").append(cols[1]).append("\n");
            }
            LOGGER.fine(() -> "Header row was: " + header);
        }
        if (LOGGER.isLoggable(Level.INFO)) {
            LOGGER.info(out.toString());
        }
    }
}
