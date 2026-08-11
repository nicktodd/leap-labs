package com.neueda.leap.sprint5;

import java.util.ArrayList;
import java.util.List;

// mission-brief.md requirement 6: every order processed today, accepted or
// rejected (and why), plus the fee charged for each accepted order.
public class SettlementReport {

    private final List<String> lines = new ArrayList<>();
    private double totalFees;

    public void recordAccepted(String clientId, String ticker, double fee) {
        lines.add(clientId + " " + ticker + ": ACCEPTED, fee $" + fee);
        totalFees += fee;
    }

    public void recordRejected(String clientId, String ticker, String reason) {
        lines.add(clientId + " " + ticker + ": REJECTED - " + reason);
    }

    public String render() {
        StringBuilder report = new StringBuilder("Settlement Report\n");
        for (String line : lines) {
            report.append(line).append("\n");
        }
        report.append("Total fees: $").append(totalFees);
        return report.toString();
    }
}
