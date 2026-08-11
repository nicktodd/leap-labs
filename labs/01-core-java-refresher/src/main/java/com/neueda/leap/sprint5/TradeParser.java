package com.neueda.leap.sprint5;

public class TradeParser {

    public Trade parse(String line) throws MalformedTradeException {
        String[] parts = line.split(",");
        String tradeId = parts[0].trim();
        String clientName = parts[1].trim();
        String instrument = parts[2].trim();
        double quantity = Double.parseDouble(parts[3].trim());
        double price = Double.parseDouble(parts[4].trim());
        String side = parts[5].trim();

        if (quantity <= 0) {
            throw new MalformedTradeException("quantity must be positive, got: " + quantity);
        }
        if (price <= 0) {
            throw new MalformedTradeException("price must be positive, got: " + price);
        }

        return new Trade(tradeId, clientName, instrument, quantity, price, side);
    }
}
