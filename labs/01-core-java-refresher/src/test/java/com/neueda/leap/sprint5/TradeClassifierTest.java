package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class TradeClassifierTest {

    private final TradeClassifier classifier = new TradeClassifier();

    @Test
    void classifiesAValueAboveThresholdAsLarge() {
        Trade trade = new Trade("T0001", "Alice Chen", "AAPL", 120, 185.32, "BUY");
        assertEquals("LARGE", classifier.classifySize(trade));
    }

    @Test
    void classifiesAValueAtOrBelowThresholdAsNormal() {
        Trade trade = new Trade("T0002", "Ben Whitfield", "MSFT", 10, 100.0, "BUY");
        assertEquals("NORMAL", classifier.classifySize(trade));
    }

    @Test
    void classifiesABuySide() {
        Trade trade = new Trade("T0003", "Alice Chen", "AAPL", 40, 186.10, "BUY");
        assertEquals("BUY", classifier.classifySide(trade));
    }

    @Test
    void classifiesASellSide() {
        Trade trade = new Trade("T0004", "Alice Chen", "AAPL", 40, 186.10, "SELL");
        assertEquals("SELL", classifier.classifySide(trade));
    }

    @Test
    void classifiesAnUnrecognisedSideAsUnknown() {
        Trade trade = new Trade("T0005", "Alice Chen", "AAPL", 40, 186.10, "TRANSFER");
        assertEquals("UNKNOWN", classifier.classifySide(trade));
    }
}
