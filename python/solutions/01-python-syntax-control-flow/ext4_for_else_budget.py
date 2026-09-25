# Extension 4: the budget loop as a for loop with break and a for ... else clause.

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


def check_budget(budget_gbp):
    """Walk approved, supported-currency transactions in order until the budget breaks."""
    cumulative = 0.0
    fitted = 0
    for txn in transactions:
        rate = RATES_TO_GBP.get(txn["currency"])
        if txn["status"] != "APPROVED" or rate is None:
            continue
        amount_gbp = txn["amount"] * rate
        if cumulative + amount_gbp > budget_gbp:
            print(f"Budget GBP {budget_gbp:,.2f}: {fitted} fitted (GBP {cumulative:,.2f}); "
                  f"{txn['txn_id']} (GBP {amount_gbp:,.2f}) breached it")
            break
        cumulative += amount_gbp
        fitted += 1
    else:
        # A for loop's else runs only if the loop finished without hitting break.
        print(f"Budget GBP {budget_gbp:,.2f}: never exceeded; all {fitted} approved "
              f"transactions fit (GBP {cumulative:,.2f})")


check_budget(200.00)    # same answer as the while loop in payments.py
check_budget(5000.00)   # large enough that break never runs, so else fires
