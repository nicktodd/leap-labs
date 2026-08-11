package com.neueda.leap.sprint5;

import java.util.List;

// ISP FIX, one of three segregated interfaces (see also ConsoleReportable). A
// class implements exactly the ones it needs - no forced, unsupported methods.
public interface CsvReportable {
    String toCsv(List<Order> orders);
}
