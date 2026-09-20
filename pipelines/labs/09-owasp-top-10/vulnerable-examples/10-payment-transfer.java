// PaySprint Mobile - TransferService.java (excerpt)

public class TransferService {

    public TransferResult transfer(Account from, Account to, BigDecimal amount) {
        try {
            ledger.debit(from, amount);
            ledger.credit(to, amount);
            notificationService.sendConfirmation(from, to, amount);
        } catch (LedgerException e) {
            // If crediting the destination account fails after the debit
            // already succeeded, this catch block just logs a warning and
            // reports success anyway, the money has left "from" but never
            // arrived at "to".
            log.warn("Transfer had an issue, continuing anyway: " + e.getMessage());
        }

        return TransferResult.success();
    }
}
