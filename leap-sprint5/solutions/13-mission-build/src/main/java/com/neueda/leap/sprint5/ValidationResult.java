package com.neueda.leap.sprint5;

// A small value type, built via TDD alongside OrderValidator itself (see
// demo-guide.md, Cycle 1). Mission-brief requirement 4 says a rejected order
// needs a REASON, not just a boolean - this exists to carry that.
public class ValidationResult {

    private final boolean valid;
    private final String reason;

    private ValidationResult(boolean valid, String reason) {
        this.valid = valid;
        this.reason = reason;
    }

    public static ValidationResult valid() {
        return new ValidationResult(true, null);
    }

    public static ValidationResult invalid(String reason) {
        return new ValidationResult(false, reason);
    }

    public boolean isValid() {
        return valid;
    }

    public String getReason() {
        return reason;
    }
}
