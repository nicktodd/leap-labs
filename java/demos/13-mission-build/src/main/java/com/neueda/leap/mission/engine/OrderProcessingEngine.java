package com.neueda.leap.mission.engine;

import java.util.List;
import java.util.Map;

// The orchestrator - and notice how little of it is NEW logic. Every real
// decision (is this order valid? how do I apply it? what's the fee?) is
// delegated to a class built in an earlier module. This class's only job is
// coordinating them in the right order, which is exactly the "OrderExecutor"
// role sketched all the way back in Module 3's worksheet.
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
            String ticker = order.getInstrument().getTicker();
            Portfolio portfolio = client.getPortfolio();
            Holding holding = portfolio.getHolding(ticker);

            OrderRequest request = new OrderRequest(order.getQuantity(), order.getPrice(), order.isBuy());
            ValidationResult result = validator.validate(
                    request, holding.getQuantity(), portfolio.getTotalValue(), client.getRiskLimit());

            if (result.isValid()) {
                double fee = order.getInstrument().calculateFee(request.tradeValue());
                holdingUpdater.applyOrder(holding, order.isBuy(), order.getQuantity());
                portfolio.adjustTotalValue(order.isBuy() ? request.tradeValue() : -request.tradeValue());
                report.recordAccepted(order.getClientId(), ticker, fee);
            } else {
                report.recordRejected(order.getClientId(), ticker, result.getReason());
            }
        }

        return report;
    }
}
