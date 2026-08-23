package com.neueda.leap.sprint7;

import java.io.BufferedReader;
import java.io.FileReader;

// KATA: this compiles and runs. It also fails the Sprint7 Strict Gate.
// Run the SonarQube analysis first to see the REAL findings before fixing
// anything - the point of this lab is reading a tool's report and acting
// on it, not guessing what might be wrong.
public class SettlementReporter {

    public static void main(String[] args) throws Exception {
        String out = "";
        BufferedReader br = new BufferedReader(new FileReader(args[0]));
        String line = br.readLine(); // header
        while ((line = br.readLine()) != null) {
            String[] cols = line.split(",");
            out = out + cols[0] + "," + cols[1] + "\n";
        }
        System.out.println(out);
    }
}
