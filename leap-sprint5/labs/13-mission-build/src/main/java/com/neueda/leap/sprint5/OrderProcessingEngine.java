package com.neueda.leap.sprint5;

import java.util.List;
import java.util.Map;

// Kata B: the orchestrator. For each order: look up the client and their
// holding for that ticker, build an OrderRequest, validate it. If valid:
// calculate the fee (via the order's own Instrument), apply the order to the
// holding (via HoldingUpdater), adjust the portfolio's total value (+tradeValue
// for a buy, -tradeValue for a sell), and record it as accepted. If invalid,
// record it as rejected with the validator's reason - and change NOTHING else.
public class OrderProcessingEngine {

    public OrderProcessingEngine(Map<String, Client> clients, OrderValidator validator,
                                  HoldingUpdater holdingUpdater) {
        throw new UnsupportedOperationException("TODO: implement constructor");
    }

    public SettlementReport process(List<IncomingOrder> orders) {
        throw new UnsupportedOperationException("TODO: implement process");
    }
}
