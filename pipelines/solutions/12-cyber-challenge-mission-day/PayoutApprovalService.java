package com.neueda.leap.merchantportal;

public class PayoutApprovalService {

    private PayoutRepository payoutRepository;

    public PayoutApprovalService(PayoutRepository payoutRepository) {
        this.payoutRepository = payoutRepository;
    }

    // VULNERABILITY (A06): the original design had no concept of segregation
    // of duties, whoever requested a payout was also allowed to approve it
    // themselves. This is a design flaw: no amount of careful coding of
    // *this* method fixes it, the approval workflow itself needs a rule
    // that the approver cannot be the requester.
    //
    // FIX (A06): this is a design fix, not just a code fix, enforce
    // segregation of duties: the approver can never be the same person who
    // requested the payout. No implementation detail elsewhere can patch
    // around a design that doesn't have this rule.
    public void approve(Long payoutId, Long approvingUserId) {
        PayoutRequest payout = payoutRepository.findById(payoutId)
                .orElseThrow(() -> new RuntimeException("Payout not found"));

        if (payout.getRequestedByUserId().equals(approvingUserId)) {
            throw new IllegalStateException(
                    "A payout cannot be approved by the same user who requested it");
        }

        payout.setApprovalStatus("APPROVED");
        payout.setApprovedByUserId(approvingUserId);
        payoutRepository.save(payout);
    }
}
