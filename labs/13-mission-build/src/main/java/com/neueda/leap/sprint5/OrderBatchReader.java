package com.neueda.leap.sprint5;

import java.util.ArrayList;
import java.util.List;

// mission-brief.md requirement 2: "orders arrive in a batch... from an upstream
// system (for this sprint: a CSV/text file)". One line = one order:
//   clientId,ticker,instrumentType,quantity,price,side
// e.g. C001,AAPL,EQUITY,100,150.00,BUY
public class OrderBatchReader {

    private final InstrumentFactory instrumentFactory;

    public OrderBatchReader(InstrumentFactory instrumentFactory) {
        this.instrumentFactory = instrumentFactory;
    }

    public List<IncomingOrder> readAll(List<String> lines) {
        List<IncomingOrder> orders = new ArrayList<>();
        for (String line : lines) {
            if (line.isBlank()) {
                continue;
            }
            String[] parts = line.split(",");
            String clientId = parts[0].trim();
            String ticker = parts[1].trim();
            Instrument instrument = instrumentFactory.create(parts[2].trim(), ticker);
            double quantity = Double.parseDouble(parts[3].trim());
            double price = Double.parseDouble(parts[4].trim());
            boolean buy = parts[5].trim().equalsIgnoreCase("BUY");
            orders.add(new IncomingOrder(clientId, instrument, quantity, price, buy));
        }
        return orders;
    }
}
