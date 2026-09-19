package com.neueda.leap.sprint5;

// A CHECKED exception: extends Exception, not RuntimeException. The compiler forces
// every caller to either catch it or declare "throws MalformedTradeException" -
// there's no Python equivalent of this compile-time enforcement; Python's
// try/except only catches at runtime, whatever you choose to catch.
public class MalformedTradeException extends Exception {

    public MalformedTradeException(String message) {
        super(message);
    }
}
