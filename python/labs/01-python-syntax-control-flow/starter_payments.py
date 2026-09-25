# Starter: plain Python card-transaction records. No imports, no libraries.
#
# Each record is a dict. `amount` is in the transaction's own currency (see `currency`).
# Twelve records are copied from shared/transactions.csv. P0999 is an extra record added
# for this lab: it is in JPY (Japanese yen), a currency PaySprint does not support yet.

transactions = [
    {"txn_id": "P0001", "customer_name": "Farah Siddiqui", "merchant": "Tesco",
     "channel": "Online", "currency": "GBP", "amount": 78.95, "status": "APPROVED"},
    {"txn_id": "P0003", "customer_name": "Eilidh Murray", "merchant": "TfL",
     "channel": "Contactless", "currency": "GBP", "amount": 4.63, "status": "APPROVED"},
    {"txn_id": "P0015", "customer_name": "Julia Novak", "merchant": "Pret A Manger",
     "channel": "Contactless", "currency": "GBP", "amount": 5.05, "status": "APPROVED"},
    {"txn_id": "P0016", "customer_name": "Ben Carter", "merchant": "Apple Store",
     "channel": "Online", "currency": "USD", "amount": 1594.61, "status": "DECLINED"},
    {"txn_id": "P0020", "customer_name": "Kofi Asante", "merchant": "Sainsbury's",
     "channel": "In-store", "currency": "GBP", "amount": 57.70, "status": "APPROVED"},
    {"txn_id": "P0026", "customer_name": "Chloe Dubois", "merchant": "TfL",
     "channel": "Contactless", "currency": "EUR", "amount": 6.30, "status": "APPROVED"},
    {"txn_id": "P0999", "customer_name": "Lena Fischer", "merchant": "Uniqlo Ginza",
     "channel": "In-store", "currency": "JPY", "amount": 4500.0, "status": "APPROVED"},
    {"txn_id": "P0034", "customer_name": "Ibrahim Yusuf", "merchant": "Apple Store",
     "channel": "In-store", "currency": "GBP", "amount": 293.81, "status": "APPROVED"},
    {"txn_id": "P0037", "customer_name": "Kofi Asante", "merchant": "Shell",
     "channel": "Contactless", "currency": "GBP", "amount": 72.40, "status": "DECLINED"},
    {"txn_id": "P0043", "customer_name": "Ibrahim Yusuf", "merchant": "Amazon",
     "channel": "Online", "currency": "GBP", "amount": 1.50, "status": "APPROVED"},
    {"txn_id": "P0044", "customer_name": "Ibrahim Yusuf", "merchant": "Amazon",
     "channel": "Online", "currency": "GBP", "amount": 1.00, "status": "APPROVED"},
    {"txn_id": "P0057", "customer_name": "Daniel Price", "merchant": "Airbnb",
     "channel": "Online", "currency": "EUR", "amount": 767.51, "status": "APPROVED"},
    {"txn_id": "P0100", "customer_name": "George Mensah", "merchant": "British Airways",
     "channel": "Online", "currency": "USD", "amount": 1522.75, "status": "APPROVED"},
]

# FX (foreign exchange) rates to GBP. Use these three values in an if/elif/else chain in
# Task 2 (a dict lookup is Extension 1):
#   GBP 1.00    EUR 0.85    USD 0.79

BUDGET_GBP = 200.00

# TODO 1: print each field of the first transaction with its type name, and a computed
#         bool `is_approved`.

# TODO 2-5: one `for` loop over `transactions` that:
#   - converts `amount` to GBP with an if/elif/else chain on `currency`; for any other
#     currency print a warning naming the txn_id and `continue`
#   - classifies the GBP amount as "micro" (< 10), "standard" (< 250) or "high"
#   - prints one line per transaction
#   - accumulates the approved GBP total, the declined count, and one counter per channel
#   - tracks the largest approved transaction without using max()

# TODO 6: a `while` loop over the approved transactions, in list order, that stops as soon
#         as cumulative GBP spend exceeds BUDGET_GBP. Report how many fitted and which
#         txn_id breached the budget.
