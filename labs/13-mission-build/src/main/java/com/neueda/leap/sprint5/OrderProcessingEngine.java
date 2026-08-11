package com.neueda.leap.sprint5;

import java.util.List;
import java.util.Map;

public class OrderProcessingEngine {

    private final Map<String, Client> clients;
    private final OrderValidator validator;
    private final HoldingUpdater holdingUpdater;

    public OrderProcessingEngine(Map<String, Client> clients, OrderValidator validator,
                                  HoldingUpdater holdingUpdater) {
        this.clients = clients;
        this.validator = validator;
        this.holdingUpdater = holdingUpdater;
    }

    public SettlementReport process(List<IncomingOrder> orders) {
        SettlementReport report = new SettlementReport();

        for (IncomingOrder order : orders) {
            Client client = clients.get(order.getClientId());
            Portfolio portfolio = client.getPortfolio();
            Holding holding = portfolio.getHolding(order.getInstrument().getTicker());

            OrderRequest request = new OrderRequest(order.getQuantity(), order.getPrice(), order.isBuy());
            ValidationResult result = validator.validate(request, holding.getQuantity(),
                    portfolio.getTotalValue(), client.getRiskLimit());

            if (result.isValid()) {
                double fee = order.getInstrument().calculateFee(request.tradeValue());
                holdingUpdater.applyOrder(holding, order.isBuy(), order.getQuantity());
                double delta = order.isBuy() ? request.tradeValue() : -request.tradeValue();
                portfolio.adjustTotalValue(delta);
                report.recordAccepted(order.getClientId(), order.getInstrument().getTicker(), fee);
            } else {
                report.recordRejected(order.getClientId(), order.getInstrument().getTicker(), result.getReason());
            }
        }

        return report;
    }
}
