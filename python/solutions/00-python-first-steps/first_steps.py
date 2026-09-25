# Module 1 Lab (Part 1) - Model Solution

# TODO 1: Getting started
my_name = "Ada"
my_favourite_number = 7
learning_python = True
print(f"{my_name} is learning Python. Favourite number: {my_favourite_number}. {learning_python}.")


# TODO 2: One trade, by hand
trade_id = "T0001"
quantity = 120
price = 185.32
side = "BUY"

print(f"trade_id: {trade_id} ({type(trade_id).__name__})")
print(f"quantity: {quantity} ({type(quantity).__name__})")
print(f"price: {price} ({type(price).__name__})")
print(f"side: {side} ({type(side).__name__})")


# TODO 3: Arithmetic
value = quantity * price
print(value)
print(f"{value:.2f}")


# TODO 4: Classify it
if quantity < 50:
    print("small trade")
elif quantity < 200:
    print("medium trade")
else:
    print("large trade")


# TODO 5: A list of quantities
quantities = [120, 60, 45, 200, 80]

print(quantities[0])
print(quantities[-1])

for q in quantities:
    print(q)

total = 0
for q in quantities:
    total += q
print(total)


# TODO 6: One trade, as a dict
trade = {"id": trade_id, "qty": quantity, "price": price, "side": side}

print(trade["id"])
print(trade["price"])
print(trade.get("commission", 0.0))


# TODO 7: A list of trades (bridge to Part 2)
trades = [
    {"id": "T0001", "qty": 120, "price": 185.32, "side": "BUY"},
    {"id": "T0002", "qty": 60, "price": 402.11, "side": "BUY"},
    {"id": "T0003", "qty": 40, "price": 186.10, "side": "SELL"},
]

for t in trades:
    t_value = t["qty"] * t["price"]
    print(f"{t['id']}: {t['side']} {t['qty']} @ {t['price']} = {t_value:.2f}")
