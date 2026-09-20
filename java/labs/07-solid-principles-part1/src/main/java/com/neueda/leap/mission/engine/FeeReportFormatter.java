package com.neueda.leap.mission.engine;

import java.util.List;

// Kata A.2 (SRP): one job only - turn orders plus a pre-calculated total into a
// report string. Format exactly:
//   Settlement Report
//   <clientId>: $<fee>
//   ... one line per order ...
//   Total fees: $<total>
// (no trailing newline after the total line)
public class FeeReportFormatter {

    public String format(List<Order> orders, double total) {
        throw new UnsupportedOperationException("TODO: implement format");
    }
}
