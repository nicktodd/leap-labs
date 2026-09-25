# Extension 1: replace the if/elif/else currency chain with a dict lookup and .get().

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

# The rates now live in data, not in code. Adding CHF is one new entry, not a new elif.
RATES_TO_GBP = {"GBP": 1.00, "EUR": 0.85, "USD": 0.79}

approved_total_gbp = 0.0
for txn in transactions:
    # .get() returns None for a missing key instead of raising KeyError, so the
    # unsupported-currency case becomes an explicit None check.
    rate = RATES_TO_GBP.get(txn["currency"])
    if rate is None:
        print(f"WARNING: {txn['txn_id']} has unsupported currency {txn['currency']}; skipped")
        continue
    amount_gbp = txn["amount"] * rate
    print(f"{txn['txn_id']}: {txn['amount']:,.2f} {txn['currency']} = GBP {amount_gbp:,.2f}")
    if txn["status"] == "APPROVED":
        approved_total_gbp += amount_gbp

print(f"\nApproved total: GBP {approved_total_gbp:,.2f} (matches the if/elif version)")

# Trade-off: RATES_TO_GBP.get(currency, 1.0) would be shorter, but a default of 1.0
# silently treats JPY 4,500 as GBP 4,500. A missing rate is an error to report, so the
# lookup has no default and the None case is handled explicitly.
wrong = transactions[6]["amount"] * RATES_TO_GBP.get(transactions[6]["currency"], 1.0)
print(f"With a 1.0 default, {transactions[6]['txn_id']} would count as GBP {wrong:,.2f}")
