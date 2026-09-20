package com.neueda.leap.merchantportal;

public interface BankTransferClient {
    void transfer(Long merchantId, double amount) throws BankTransferException;
}
