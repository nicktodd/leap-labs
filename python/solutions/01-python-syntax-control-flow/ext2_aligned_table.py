# Extension 2: an aligned table using f-string format specifications.

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

RATES_TO_GBP = {"GBP": 1.00, "EUR": 0.85, "USD": 0.79}

# <  left-aligns, > right-aligns, the number is the column width,
# , adds thousands separators and .2f fixes two decimal places.
header = f"{'txn_id':<6} {'merchant':<15} {'channel':<11} {'status':<8} {'amount_gbp':>10}"
print(header)
print("-" * len(header))
total = 0.0
for txn in transactions:
    rate = RATES_TO_GBP.get(txn["currency"])
    if rate is None:
        print(f"{txn['txn_id']:<6} {txn['merchant']:<15} {'unsupported currency ' + txn['currency']}")
        continue
    amount_gbp = txn["amount"] * rate
    total += amount_gbp
    print(f"{txn['txn_id']:<6} {txn['merchant']:<15} {txn['channel']:<11} "
          f"{txn['status']:<8} {amount_gbp:>10,.2f}")
print("-" * len(header))
print(f"{'Total (approved and declined)':<44} {total:>10,.2f}")
