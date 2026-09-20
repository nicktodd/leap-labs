package com.neueda.leap;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class GreeterTest {

    @Test
    void greetIncludesName() {
        Greeter greeter = new Greeter();
        assertEquals("Good day, Priya", greeter.greet("Priya"));
    }
}
