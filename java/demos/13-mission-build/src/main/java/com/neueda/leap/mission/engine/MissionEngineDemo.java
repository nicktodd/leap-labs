package com.neueda.leap.mission.engine;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MissionEngineDemo {

    public static void main(String[] args) {
        Map<String, Client> clients = new HashMap<>();
        clients.put("C001", new Client("C001", 20000));
        clients.put("C002", new Client("C002", 5000));

        List<String> orderFile = List.of(
                "C001,AAPL,EQUITY,100,150.00,BUY",
                "C001,VOD.L,BOND,50,10.00,BUY",
                "C002,VWRL,FUND,1000,10.00,BUY",   // 1000 * 10 = 10000, over C002's 5000 risk limit
                "C001,AAPL,EQUITY,20,150.00,SELL",
                "C001,MSFT,EQUITY,-5,300.00,BUY"    // invalid quantity
        );

        OrderBatchReader reader = new OrderBatchReader(new InstrumentFactory());
        List<IncomingOrder> orders = reader.readAll(orderFile);

        OrderProcessingEngine engine = new OrderProcessingEngine(
                clients, new OrderValidator(), new HoldingUpdater());

        SettlementReport report = engine.process(orders);

        System.out.println(report.render());
        System.out.println();
        System.out.println("C001's AAPL holding after the batch: "
                + clients.get("C001").getPortfolio().getHolding("AAPL").getQuantity());
    }
}
