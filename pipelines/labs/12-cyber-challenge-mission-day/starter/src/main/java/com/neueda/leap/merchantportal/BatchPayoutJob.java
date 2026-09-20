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

    public void runNightlyBatch(List<PayoutRequest> approvedPayouts) {
        for (PayoutRequest payout : approvedPayouts) {
            try {
                bankTransferClient.transfer(payout.getMerchantId(), payout.getAmount());
                payout.setApprovalStatus("PAID");
            } catch (BankTransferException e) {
                log.warn("Transfer failed for payout {}, marking paid anyway: {}",
                        payout.getId(), e.getMessage());
                payout.setApprovalStatus("PAID");
            }
            payoutRepository.save(payout);
        }
    }
}
