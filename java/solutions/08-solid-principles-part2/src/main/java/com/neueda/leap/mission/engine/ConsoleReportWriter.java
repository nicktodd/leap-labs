package com.neueda.leap.mission.engine;

public class ConsoleReportWriter implements ReportWriter {
    @Override
    public void write(String line) {
        System.out.println(line);
    }
}
