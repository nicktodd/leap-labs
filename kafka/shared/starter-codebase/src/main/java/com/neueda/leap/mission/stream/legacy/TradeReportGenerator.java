package com.neueda.leap.mission.stream.legacy;

import java.io.*;
import java.util.*;

public class TradeReportGenerator {

    static Map<String, Double> tot = new HashMap<>();
    static Map<String, Double> f = new HashMap<>();
    static int c = 0;

    public static void main(String[] args) throws Exception {
        String p = args.length > 0 ? args[0] : "src/main/resources/trades.csv";
        doIt(p);
    }

    public static void doIt(String p) throws Exception {
        BufferedReader br = new BufferedReader(new FileReader(p));
        String line = br.readLine(); // header
        String out = "TICKER,QTY,VALUE,FEE\n";
        while ((line = br.readLine()) != null) {
            try {
                String[] x = line.split(",");
                String tkr = x[0];
                String typ = x[1];
                double q = Double.parseDouble(x[2]);
                double pr = Double.parseDouble(x[3]);
                double val = q * pr;
                double fee = FeeCalculator.calculateFee(typ, val);
                if (tot.containsKey(tkr)) {
                    tot.put(tkr, tot.get(tkr) + val);
                    f.put(tkr, f.get(tkr) + fee);
                } else {
                    tot.put(tkr, val);
                    f.put(tkr, fee);
                }
                c++;
                out = out + tkr + "," + q + "," + val + "," + fee + "\n";
            } catch (Exception e) {
                // skip bad row
            }
        }
        br.close();

        System.out.println("Processed " + c + " trades");
        for (String k : tot.keySet()) {
            System.out.println(k + " total=" + tot.get(k) + " fee=" + f.get(k));
        }

        FileWriter fw = new FileWriter("report.csv");
        fw.write(out);
        fw.close();
    }
}
