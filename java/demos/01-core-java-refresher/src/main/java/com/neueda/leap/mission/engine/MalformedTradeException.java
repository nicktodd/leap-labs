package com.neueda.leap.mission.engine;

// A CHECKED exception: extends Exception, not RuntimeException. The compiler forces
// every caller to either catch it or declare "throws MalformedTradeException" -
// a compile-time guarantee that this failure can never be silently ignored.
public class MalformedTradeException extends Exception {

    public MalformedTradeException(String message) {
        super(message);
    }
}
