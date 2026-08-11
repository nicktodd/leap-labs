package com.neueda.leap.sprint5;

import java.util.ArrayList;
import java.util.List;

public class SettlementReport {

    private final List<String> lines = new ArrayList<>();
    private double totalFees = 0;

    public void recordAccepted(String clientId, String ticker, double fee) {
        lines.add(clientId + " " + ticker + ": ACCEPTED, fee $" + fee);
        totalFees += fee;
    }

    public void recordRejected(String clientId, String ticker, String reason) {
        lines.add(clientId + " " + ticker + ": REJECTED - " + reason);
    }

    public String render() {
        StringBuilder sb = new StringBuilder("Settlement Report\n");
        for (String line : lines) {
            sb.append(line).append("\n");
        }
        sb.append("Total fees: $").append(totalFees);
        return sb.toString();
    }
}
