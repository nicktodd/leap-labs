package com.neueda.leap.sprint5;

import java.util.List;

// ISP VIOLATION. One interface, three unrelated output formats bundled together.
// Any class that implements this - even one that only ever needs to produce a
// CSV file - is FORCED to also provide toConsole() and toPdf(), whether or not
// they make sense for it. See CsvOnlyReportBad.java for what that forces the
// implementer to do.
public interface FatReportable {
    String toConsole(List<Order> orders);
    String toCsv(List<Order> orders);
    String toPdf(List<Order> orders);
}
