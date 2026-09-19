package com.neueda.leap.sprint5;

// Kata A: mission-brief.md requirement 6 - every order processed, accepted or
// rejected (and why), plus the fee for each accepted order. Format exactly:
//   Settlement Report
//   <clientId> <ticker>: ACCEPTED, fee $<fee>
//   <clientId> <ticker>: REJECTED - <reason>
//   ... one line per order, in the order recorded ...
//   Total fees: $<sum of all accepted fees>
public class SettlementReport {

    public void recordAccepted(String clientId, String ticker, double fee) {
        throw new UnsupportedOperationException("TODO: implement recordAccepted");
    }

    public void recordRejected(String clientId, String ticker, String reason) {
        throw new UnsupportedOperationException("TODO: implement recordRejected");
    }

    public String render() {
        throw new UnsupportedOperationException("TODO: implement render");
    }
}
