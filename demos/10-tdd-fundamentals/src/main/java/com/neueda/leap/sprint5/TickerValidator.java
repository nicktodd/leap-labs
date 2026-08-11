package com.neueda.leap.sprint5;

// This is the END STATE of a live TDD session - see demo-guide.md for the six
// red-green-refactor cycles that actually built it, one test at a time. Reading
// only this file skips the entire point of the demo.
public class TickerValidator {

    private static final int MAX_BASE_LENGTH = 5;
    private static final String LONDON_SUFFIX = ".L";

    public boolean isValid(String ticker) {
        if (ticker == null || ticker.isEmpty()) {
            return false;
        }

        String base = ticker.endsWith(LONDON_SUFFIX)
                ? ticker.substring(0, ticker.length() - LONDON_SUFFIX.length())
                : ticker;

        if (base.isEmpty() || base.length() > MAX_BASE_LENGTH) {
            return false;
        }

        for (char c : base.toCharArray()) {
            if (!Character.isUpperCase(c) || !Character.isLetter(c)) {
                return false;
            }
        }
        return true;
    }
}
