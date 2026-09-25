"""Extension 2: the processing loop with logging instead of print."""

import logging

from payment_utils import PaymentError, card_fee, process_transaction
from process_payments import raw_transactions

# One call configures the root logger: minimum level and line format.
logging.basicConfig(level=logging.INFO, format="%(levelname)-7s %(message)s")
log = logging.getLogger("payments")

total_gbp = 0.0
skipped = 0
for txn in raw_transactions:
    try:
        amount_gbp = process_transaction(txn)
    except PaymentError as e:
        # %-style arguments: the message is only built if this level is enabled.
        log.warning("skipped %s [cause: %s]", e, type(e.__cause__).__name__)
        skipped += 1
    else:
        total_gbp += amount_gbp
        log.info("processed %s: GBP %.2f, fee GBP %.2f",
                 txn["txn_id"], amount_gbp, card_fee(amount_gbp))

log.info("done: total GBP %.2f, %d skipped", total_gbp, skipped)

# Raising the level hides the INFO lines without touching any of the calls above.
log.setLevel(logging.WARNING)
log.info("this line is not shown")
log.warning("WARNING and above are still shown after setLevel(logging.WARNING)")
