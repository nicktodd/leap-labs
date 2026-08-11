package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;

import static org.junit.jupiter.api.Assertions.*;

class HoldingTest {

    @Test
    void everyFieldOnHoldingIsPrivate() {
        // Encapsulation, verified automatically: no field on this class may be
        // public. This is exactly what "make the invariant impossible to bypass"
        // means in practice - not just a style preference.
        for (Field field : Holding.class.getDeclaredFields()) {
            assertFalse(Modifier.isPublic(field.getModifiers()),
                    "Field '" + field.getName() + "' must not be public");
        }
    }

    @Test
    void constructorAcceptsAValidInitialQuantity() {
        Holding holding = new Holding(100);
        assertEquals(100, holding.getQuantity(), 0.001);
    }

    @Test
    void constructorRejectsANegativeInitialQuantity() {
        assertThrows(IllegalArgumentException.class, () -> new Holding(-1));
    }

    @Test
    void adjustAppliesAValidDelta() {
        Holding holding = new Holding(100);
        holding.adjust(-30);
        assertEquals(70, holding.getQuantity(), 0.001);
    }

    @Test
    void adjustRejectsADeltaThatWouldGoNegative() {
        Holding holding = new Holding(50);
        assertThrows(IllegalArgumentException.class, () -> holding.adjust(-1000));
        // State must be unchanged after a rejected adjustment
        assertEquals(50, holding.getQuantity(), 0.001);
    }
}
