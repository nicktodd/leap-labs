package com.neueda.leap.sprint5;

public class ConsoleReportWriter implements ReportWriter {
    @Override
    public void write(String line) {
        System.out.println(line);
    }
}
