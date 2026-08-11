package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;
import java.util.Collection;

import static org.junit.jupiter.api.Assertions.*;

class GoodClientRegistryTest {

    @Test
    void doesNotExtendAnyCollectionType() {
        // Composition, not inheritance: GoodClientRegistry's only ancestor should
        // be Object - it must not "is-a" any List/Collection type.
        Class<?> superclass = GoodClientRegistry.class.getSuperclass();
        assertEquals(Object.class, superclass,
                "GoodClientRegistry must not extend a collection type - use composition instead");
        assertFalse(Collection.class.isAssignableFrom(GoodClientRegistry.class),
                "GoodClientRegistry must not implement Collection either");
    }

    @Test
    void addsAndFindsAClient() {
        GoodClientRegistry registry = new GoodClientRegistry();
        registry.addClient("C001");
        assertTrue(registry.contains("C001"));
        assertEquals(1, registry.size());
    }

    @Test
    void rejectsADuplicateClientId() {
        GoodClientRegistry registry = new GoodClientRegistry();
        registry.addClient("C001");
        assertThrows(IllegalArgumentException.class, () -> registry.addClient("C001"));
        assertEquals(1, registry.size());
    }
}
