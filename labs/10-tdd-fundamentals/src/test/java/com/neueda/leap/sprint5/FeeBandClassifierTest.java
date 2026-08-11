package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FeeBandClassifierTest {

    private final FeeBandClassifier classifier = new FeeBandClassifier();

    @Test
    void classifiesLowValueTradeAsStandard() {
        assertEquals("STANDARD", classifier.classify(1000));
    }

    @Test
    void classifiesHighValueTradeAsInstitutional() {
        assertEquals("INSTITUTIONAL", classifier.classify(60000));
    }

    @Test
    void classifiesMidValueTradeAsPremium() {
        assertEquals("PREMIUM", classifier.classify(10000));
    }

    @Test
    void classifiesLowerPremiumBoundaryAsPremium() {
        assertEquals("PREMIUM", classifier.classify(5000));
    }

    @Test
    void classifiesLowerInstitutionalBoundaryAsInstitutional() {
        assertEquals("INSTITUTIONAL", classifier.classify(50000));
    }
}
