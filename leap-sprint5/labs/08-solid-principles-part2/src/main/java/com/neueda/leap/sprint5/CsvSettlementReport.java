package com.neueda.leap.sprint5;

import java.util.List;

// Kata A (ISP): implement CsvReportable ONLY - don't implement ConsoleReportable
// too, even though it might feel natural to "future proof" it. Format exactly:
//   clientId,fee
//   <clientId>,<fee>
//   ... one line per order ...
// (a trailing newline after the last order line is fine)
public class CsvSettlementReport implements CsvReportable {

    @Override
    public String toCsv(List<Order> orders) {
        throw new UnsupportedOperationException("TODO: implement toCsv");
    }
}
