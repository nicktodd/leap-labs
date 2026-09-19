package com.neueda.leap.paysprint;

public class Transaction {
    private Long id;
    private String merchantName;
    private double amount;

    public Transaction(Long id, String merchantName, double amount) {
        this.id = id;
        this.merchantName = merchantName;
        this.amount = amount;
    }

    public Long getId() { return id; }
    public String getMerchantName() { return merchantName; }
    public double getAmount() { return amount; }
}
