package com.neueda.leap.mission.engine;

// Kata 3: checked vs unchecked exceptions.
// Line format: tradeId,clientName,instrument,quantity,price,side
public class TradeParser {

    // TODO: parse `line` into a Trade.
    // - Let Double.parseDouble's NumberFormatException (unchecked) propagate
    //   unhandled if quantity or price isn't a valid number - do NOT catch it here.
    // - If quantity is parsed successfully but is <= 0, throw a checked
    //   MalformedTradeException with a message naming the bad value.
    // - If price is parsed successfully but is <= 0, throw a checked
    //   MalformedTradeException with a message naming the bad value.
    public Trade parse(String line) throws MalformedTradeException {
        throw new UnsupportedOperationException("TODO: implement parse");
    }
}
