package com.neueda.leap.sprint5;

// The one place instrument TYPE names (as they appear in an incoming order file)
// get turned into actual Instrument objects. Module 7's OCP still holds here -
// adding a new instrument type means adding one case here and one new class, not
// touching OrderValidator, HoldingUpdater, or OrderProcessingEngine.
public class InstrumentFactory {

    public Instrument create(String type, String ticker) {
        return switch (type) {
            case "EQUITY" -> new EquityInstrument(ticker);
            case "BOND" -> new BondInstrument(ticker);
            case "FUND" -> new FundInstrument(ticker);
            default -> throw new IllegalArgumentException("unknown instrument type: " + type);
        };
    }
}
