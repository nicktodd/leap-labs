package com.neueda.leap.merchantportal;

public class PaymentStatusEvent {
    private Long payoutId;
    private String status;

    public Long getPayoutId() { return payoutId; }
    public String getStatus() { return status; }
}
