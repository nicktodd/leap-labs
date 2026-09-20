package com.neueda.leap.mission.engine;

// A class that is NOT an Instrument in any sense - it represents a flat annual
// account-keeping fee, not a tradable thing. It has nothing in common with
// Instrument's hierarchy (no ticker, no trade-related state at all), but it still
// needs to "calculate a fee" - so it implements Feeable directly, with no
// inheritance from Instrument whatsoever. This is exactly why interfaces exist
// alongside abstract classes: a shared CAPABILITY across otherwise-unrelated
// classes, not a shared IS-A relationship.
public class AccountMaintenanceCharge implements Feeable {

    private final String accountId;

    public AccountMaintenanceCharge(String accountId) {
        this.accountId = accountId;
    }

    public String getAccountId() {
        return accountId;
    }

    @Override
    public double calculateFee(double tradeValue) {
        // tradeValue is ignored - this fee doesn't depend on any trade at all,
        // it's a flat annual charge. The parameter still has to be there because
        // the interface's method signature requires it.
        return 25.00;
    }
}
