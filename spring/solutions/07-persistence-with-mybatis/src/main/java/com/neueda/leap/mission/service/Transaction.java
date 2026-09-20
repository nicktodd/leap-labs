package com.neueda.leap.mission.service;

import java.math.BigDecimal;
import java.time.LocalDate;

// Given - result-mapping class for Kata B.
public class Transaction {
    private int transactionId;
    private String ticker;
    private String txnType;
    private BigDecimal quantity;
    private BigDecimal price;
    private LocalDate txnDate;

    public int getTransactionId() {
        return transactionId;
    }

    public void setTransactionId(int transactionId) {
        this.transactionId = transactionId;
    }

    public String getTicker() {
        return ticker;
    }

    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    public String getTxnType() {
        return txnType;
    }

    public void setTxnType(String txnType) {
        this.txnType = txnType;
    }

    public BigDecimal getQuantity() {
        return quantity;
    }

    public void setQuantity(BigDecimal quantity) {
        this.quantity = quantity;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public LocalDate getTxnDate() {
        return txnDate;
    }

    public void setTxnDate(LocalDate txnDate) {
        this.txnDate = txnDate;
    }
}
