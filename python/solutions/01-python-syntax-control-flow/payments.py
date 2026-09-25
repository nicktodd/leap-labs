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

BUDGET_GBP = 200.00

# --- Task 1: data types, and a computed bool ---
first = transactions[0]
print("First transaction:")
print(f"  txn_id   = {first['txn_id']!r:<18} {type(first['txn_id']).__name__}")
print(f"  merchant = {first['merchant']!r:<18} {type(first['merchant']).__name__}")
print(f"  currency = {first['currency']!r:<18} {type(first['currency']).__name__}")
print(f"  amount   = {first['amount']!r:<18} {type(first['amount']).__name__}")
is_approved = first["status"] == "APPROVED"   # a comparison evaluates to a bool
print(f"  is_approved = {is_approved} ({type(is_approved).__name__})")

# --- Tasks 2-5: one pass over the list, doing all the bookkeeping by hand ---
approved_total_gbp = 0.0
declined_count = 0
online_count = 0
contactless_count = 0
instore_count = 0
largest_txn_id = None
largest_gbp = 0.0
approved = []          # approved records, in list order, for Task 6

print("\nTransactions:")
for txn in transactions:
    currency = txn["currency"]

    # Task 2: currency conversion. The else branch catches anything unexpected.
    if currency == "GBP":
        rate = 1.00
    elif currency == "EUR":
        rate = 0.85
    elif currency == "USD":
        rate = 0.79
    else:
        print(f"  WARNING: {txn['txn_id']} has unsupported currency {currency}; skipped")
        continue   # nothing below this line runs for this record
    amount_gbp = txn["amount"] * rate
    txn["amount_gbp"] = amount_gbp   # keep it on the record for Task 6

    # Task 3: amount band. Order matters: the first true condition wins, so each
    # branch only needs to test its upper bound.
    if amount_gbp < 10:
        band = "micro"
    elif amount_gbp < 250:
        band = "standard"
    else:
        band = "high"
    print(f"  {txn['txn_id']} {txn['merchant']} ({txn['channel']}, {txn['status']}): "
          f"GBP {amount_gbp:,.2f} [{band}]")

    # Task 4: running totals and counters
    if txn["status"] == "APPROVED":
        approved_total_gbp += amount_gbp
        approved.append(txn)
        # Task 5: largest approved so far, compared one record at a time
        if largest_txn_id is None or amount_gbp > largest_gbp:
            largest_txn_id = txn["txn_id"]
            largest_gbp = amount_gbp
    else:
        declined_count += 1

    if txn["channel"] == "Online":
        online_count += 1
    elif txn["channel"] == "Contactless":
        contactless_count += 1
    elif txn["channel"] == "In-store":
        instore_count += 1
    else:
        print(f"  WARNING: {txn['txn_id']} has unknown channel {txn['channel']}")

print("\n--- Summary ---")
print(f"Approved total: GBP {approved_total_gbp:,.2f}")
print(f"Declined transactions: {declined_count}")
print(f"Online: {online_count}, Contactless: {contactless_count}, In-store: {instore_count}")
print(f"Largest approved: {largest_txn_id} (GBP {largest_gbp:,.2f})")

# --- Task 6: a while loop whose stopping point is not known in advance ---
# A for loop visits every item. Here we want to stop at the first transaction that
# pushes cumulative spend over the budget, and we cannot know in advance which one
# that will be, so the loop condition carries the stopping rule.
cumulative = 0.0
i = 0
while i < len(approved) and cumulative + approved[i]["amount_gbp"] <= BUDGET_GBP:
    cumulative += approved[i]["amount_gbp"]
    i += 1

print(f"\nBudget GBP {BUDGET_GBP:,.2f}: {i} approved transactions fit "
      f"(GBP {cumulative:,.2f})")
if i < len(approved):
    breach = approved[i]
    print(f"{breach['txn_id']} (GBP {breach['amount_gbp']:,.2f}) would take spend to "
          f"GBP {cumulative + breach['amount_gbp']:,.2f}, breaching the budget")
else:
    print("The budget was never exceeded")
