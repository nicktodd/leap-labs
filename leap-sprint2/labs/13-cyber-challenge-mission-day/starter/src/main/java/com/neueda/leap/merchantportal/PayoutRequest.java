package com.neueda.leap.merchantportal;

public class PayoutRequest {
    private Long id;
    private Long merchantId;
    private Long requestedByUserId;
    private String approvalStatus; // PENDING, APPROVED, REJECTED
    private Long approvedByUserId;
    private double amount;

    public PayoutRequest(Long id, Long merchantId, Long requestedByUserId, double amount) {
        this.id = id;
        this.merchantId = merchantId;
        this.requestedByUserId = requestedByUserId;
        this.amount = amount;
        this.approvalStatus = "PENDING";
    }

    public Long getId() { return id; }
    public Long getMerchantId() { return merchantId; }
    public Long getRequestedByUserId() { return requestedByUserId; }
    public String getApprovalStatus() { return approvalStatus; }
    public void setApprovalStatus(String s) { this.approvalStatus = s; }
    public Long getApprovedByUserId() { return approvedByUserId; }
    public void setApprovedByUserId(Long id) { this.approvedByUserId = id; }
    public double getAmount() { return amount; }
}
