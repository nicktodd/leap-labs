package com.neueda.leap.mission.engine;

import java.util.List;

// ISP FIX, one of three segregated interfaces (see also ConsoleReportable). A
// class implements exactly the ones it needs - no forced, unsupported methods.
public interface CsvReportable {
    String toCsv(List<Order> orders);
}
