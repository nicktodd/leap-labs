package com.neueda.leap.sprint5;

import java.util.ArrayList;
import java.util.List;

// A second, completely different ReportWriter - useful for tests, where printing
// to the console is awkward to assert on. High-level code that depends on the
// ReportWriter ABSTRACTION can use either one, or a third kind nobody's written
// yet, without a single line of that high-level code changing.
public class InMemoryReportWriter implements ReportWriter {

    private final List<String> lines = new ArrayList<>();

    @Override
    public void write(String line) {
        lines.add(line);
    }

    public List<String> getLines() {
        return lines;
    }
}
