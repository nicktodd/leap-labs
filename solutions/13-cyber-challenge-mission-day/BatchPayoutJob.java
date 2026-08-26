package com.neueda.leap.merchantportal;

import java.util.List;

public class BatchPayoutJob {

    private static final org.slf4j.Logger log = org.slf4j.LoggerFactory.getLogger(BatchPayoutJob.class);

    private BankTransferClient bankTransferClient;
    private PayoutRepository payoutRepository;

    public BatchPayoutJob(BankTransferClient bankTransferClient, PayoutRepository payoutRepository) {
        this.bankTransferClient = bankTransferClient;
        this.payoutRepository = payoutRepository;
    }

    // VULNERABILITY (A10): in the original version, if the bank transfer
    // failed partway through the nightly batch, the payout was still marked
    // APPROVED->PAID and the loop moved on to the next merchant. There was no
    // distinction between "this payout was never attempted" and "this payout
    // failed after the money may have already left," so re-running the batch
    // after a failure risked paying some merchants twice, and silently
    // skipping others.
    //
    // FIX (A10): a failed transfer is marked FAILED, not PAID, and the batch
    // continues to the next merchant rather than silently misreporting this
    // one. A separate, idempotent retry process can safely re-attempt only
    // the FAILED payouts later, because their real status is now recorded
    // accurately instead of masked.
    public void runNightlyBatch(List<PayoutRequest> approvedPayouts) {
        for (PayoutRequest payout : approvedPayouts) {
            try {
                bankTransferClient.transfer(payout.getMerchantId(), payout.getAmount());
                payout.setApprovalStatus("PAID");
            } catch (BankTransferException e) {
                log.error("Transfer failed for payout {}, marking FAILED for retry: {}",
                        payout.getId(), e.getMessage());
                payout.setApprovalStatus("FAILED");
            }
            payoutRepository.save(payout);
        }
    }
}
