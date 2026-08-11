package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.fail;

class FrozenHoldingTest {

    @Test
    void doesNotExtendHolding() {
        assertFalse(Holding.class.isAssignableFrom(FrozenHolding.class),
                "FrozenHolding must not extend Holding - use composition instead");
    }

    @Test
    void reportsTheWrappedQuantity() {
        FrozenHolding frozen = new FrozenHolding(new Holding(250));

        assertEquals(250.0, frozen.getQuantity(), 0.0001);
    }

    @Test
    void hasNoAdjustMethod() {
        try {
            Method m = FrozenHolding.class.getMethod("adjust", double.class);
            fail("FrozenHolding must not expose " + m);
        } catch (NoSuchMethodException expected) {
            // correct - a frozen holding should not offer adjust() at all
        }
    }
}
