package com.neueda.leap.sprint5;

import java.util.List;

// The other half of the ISP fix - kept separate from CsvReportable so a class
// that only needs one of the two never has to know the other exists.
public interface ConsoleReportable {
    String toConsole(List<Order> orders);
}
