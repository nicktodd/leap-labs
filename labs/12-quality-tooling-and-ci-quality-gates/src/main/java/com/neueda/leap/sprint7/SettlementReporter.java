package com.neueda.leap.sprint7;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

// Lab 12: fixed to pass the Sprint7 Strict Gate.
// Original issues found by SonarQube:
//   1. BufferedReader was not closed (resource leak) - fixed with try-with-resources
//   2. String concatenation in a loop (performance) - fixed with StringBuilder
//   3. Raw exception propagation via throws Exception - tightened to throws IOException
public class SettlementReporter {

    public static void main(String[] args) throws IOException {
        StringBuilder out = new StringBuilder();
        try (BufferedReader br = new BufferedReader(new FileReader(args[0]))) {
            br.readLine(); // header
            String line;
            while ((line = br.readLine()) != null) {
                String[] cols = line.split(",");
                out.append(cols[0]).append(",").append(cols[1]).append("\n");
            }
        }
        System.out.println(out);
    }
}
