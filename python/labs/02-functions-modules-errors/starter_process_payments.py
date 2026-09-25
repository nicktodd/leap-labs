"""Process a batch of raw PaySprint transactions.

Run this file as it is first: the naive loop at the bottom crashes on the first bad record.
Read the traceback, then replace the loop as described in the lab README.
"""

# TODO: import what you need from starter_payment_utils.

# Raw records as they arrive from a card terminal feed: amounts are text, not numbers.
raw_transactions = [
    {"txn_id": "P0001", "merchant": "Tesco", "currency": "GBP", "amount": "78.95"},
    {"txn_id": "P0002", "merchant": "Amazon", "currency": "EUR", "amount": "€143.92"},
    {"txn_id": "P0015", "merchant": "Pret A Manger", "currency": "GBP", "amount": "£5.05"},
    {"txn_id": "P0016", "merchant": "Apple Store", "currency": "USD", "amount": "$1,594.61"},
    {"txn_id": "P0034", "merchant": "Apple Store", "currency": "GBP", "amount": " 293.81 "},
    {"txn_id": "P0048", "merchant": "Uber", "currency": "GBP", "amount": "12.5.0"},
    {"txn_id": "P0057", "merchant": "Airbnb", "currency": "EUR", "amount": None},
    {"txn_id": "P0061", "merchant": "Pret A Manger", "currency": "EUR", "amount": "-5.00"},
    {"txn_id": "P0098", "merchant": "British Airways", "currency": "GBP", "amount": "1,249.00"},
    {"txn_id": "P0999", "merchant": "Uniqlo Ginza", "currency": "JPY", "amount": "4500"},
    {"txn_id": "P0120", "merchant": "Amazon", "amount": "624.51"},   # no currency key
    {"txn_id": "P0134", "merchant": "Costa Coffee", "currency": "GBP", "amount": "£2.91"},
]

RATES = {"GBP": 1.00, "EUR": 0.85, "USD": 0.79}

# Naive version: assumes every record is clean. It is expected to crash.
total_gbp = 0.0
for txn in raw_transactions:
    amount_gbp = float(txn["amount"]) * RATES[txn["currency"]]
    total_gbp += amount_gbp
    print(f"{txn['txn_id']}: GBP {amount_gbp:,.2f}")
print(f"Total GBP {total_gbp:,.2f}")

# TODO: replace the naive loop with a try/except/else/finally version (see README Task 2).
# TODO: call process_transaction on a bad record, catch PaymentError, print e and e.__cause__.
