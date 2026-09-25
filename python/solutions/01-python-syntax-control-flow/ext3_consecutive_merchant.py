# Extension 3: detect a customer making two consecutive transactions at the same merchant.

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

# The loop only sees one record at a time, so to compare with the previous record we
# carry it across iterations in a variable. It starts as None: the first record has no
# predecessor.
previous = None
repeats = 0
for txn in transactions:
    if (previous is not None
            and txn["customer_name"] == previous["customer_name"]
            and txn["merchant"] == previous["merchant"]):
        repeats += 1
        print(f"{txn['customer_name']}: {previous['txn_id']} and {txn['txn_id']} are "
              f"consecutive transactions at {txn['merchant']} "
              f"({previous['amount']:.2f} then {txn['amount']:.2f} {txn['currency']})")
    previous = txn   # update last, after the comparison

print(f"\nConsecutive repeat pairs found: {repeats}")
