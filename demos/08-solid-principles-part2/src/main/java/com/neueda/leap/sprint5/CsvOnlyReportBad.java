package com.neueda.leap.sprint5;

import java.util.List;

// This class only ever needs CSV output - but because it implements FatReportable,
// it's forced to provide toConsole() and toPdf() too. There's no sensible
// implementation for either, so both are stubbed out with an exception. Any code
// that calls toPdf() on what LOOKS like a fully-featured FatReportable will crash
// at runtime, for no reason a caller could have anticipated from the type alone.
public class CsvOnlyReportBad implements FatReportable {

    @Override
    public String toCsv(List<Order> orders) {
        StringBuilder csv = new StringBuilder("clientId,fee\n");
        for (Order order : orders) {
            csv.append(order.getClientId()).append(",").append(order.calculateFee()).append("\n");
        }
        return csv.toString();
    }

    @Override
    public String toConsole(List<Order> orders) {
        throw new UnsupportedOperationException("CsvOnlyReportBad does not support console output");
    }

    @Override
    public String toPdf(List<Order> orders) {
        throw new UnsupportedOperationException("CsvOnlyReportBad does not support PDF output");
    }
}
