package com.neueda.leap.paysprint;

public class Account {
    private Long id;
    private Long ownerId;
    private String iban;
    private double balance;

    public Account(Long id, Long ownerId, String iban, double balance) {
        this.id = id;
        this.ownerId = ownerId;
        this.iban = iban;
        this.balance = balance;
    }

    public Long getId() { return id; }
    public Long getOwnerId() { return ownerId; }
    public String getIban() { return iban; }
    public double getBalance() { return balance; }
}
