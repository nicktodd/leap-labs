# Demo: Python fundamentals, built up step by step. Live-run this section by section -
# each block stands alone and can be typed into the REPL instead if you prefer.
# No libraries: everything here is plain Python.


# --- Comments & print() ---------------------------------------------------
# This is a comment. Python ignores everything after the # on this line.
print("Hello, PaySprint")
print("Trade ID:", "T0001")           # print() can take more than one argument


# --- Whitespace & indentation ----------------------------------------------
if True:
    print("This line is inside the if")
    print("So is this one")
print("This line is NOT inside the if")

# Uncomment the next line to show IndentationError live:
#     print("this breaks - unexpected indent")


# --- Variables ---------------------------------------------------------
trade_id = "T0001"
quantity = 120
price = 185.32
is_buy = True

# Reassignment is allowed, even to a different type:
quantity = "one hundred and twenty"
quantity = 120  # back to an int for the rest of the demo


# --- Data types ----------------------------------------------------------
print(type(trade_id))    # <class 'str'>
print(type(quantity))     # <class 'int'>
print(type(price))         # <class 'float'>
print(type(is_buy))         # <class 'bool'>


# --- Arithmetic operators ---------------------------------------------
total = quantity * price
print(total)              # 22238.4
print(7 // 2)               # 3   (floor division)
print(7 % 2)                  # 1   (remainder)
print(2 ** 8)                    # 256 (power)


# --- Comparison & boolean operators -----------------------------------
print(price == 185.32)     # True
print(price > 100)           # True
is_large_trade = quantity > 100 and price > 100
print(is_large_trade)         # True
print(not is_large_trade)      # False


# --- Strings -------------------------------------------------------------
first = "Ada"
last = "Lovelace"
full_name = first + " " + last
print(full_name)             # Ada Lovelace
print(len(full_name))          # 12

print(trade_id[0])        # T           (indexing)
print(trade_id[1:5])        # 0001        (slicing)
print(trade_id[-1])           # 1           (negative index)

# f-strings - the format most of the rest of this course uses:
print(f"Trade {trade_id} priced at {price:.2f}")

side = "  buy  "
print(side.strip().upper())   # "BUY"


# --- Lists -----------------------------------------------------------------
quantities = [120, 60, 45, 200]
print(quantities[0])          # 120
print(quantities[1:3])          # [60, 45]
quantities.append(75)
print(quantities)                 # [120, 60, 45, 200, 75]
print(200 in quantities)            # True
print(sum(quantities))                # 500


# --- Dictionaries --------------------------------------------------------
trade = {"id": "T0001", "qty": 120, "price": 185.32}
print(trade["id"])           # T0001
print(trade.get("side"))       # None - no error, key doesn't exist
trade["qty"] = 150
print(trade)                     # {'id': 'T0001', 'qty': 150, 'price': 185.32}


# --- Putting it together: a list of dictionaries --------------------------
# This is the shape most real, structured data actually has - a CSV file, an
# API response, a database query result: a list of records, each one a dict.
trades = [
    {"id": "T0001", "qty": 120, "price": 185.32},
    {"id": "T0002", "qty": 60, "price": 402.11},
]
print(trades[0]["id"])          # T0001
print(trades[1]["price"])         # 402.11

for t in trades:
    print(t["id"], t["qty"] * t["price"])


# --- range() ---------------------------------------------------------------
for i in range(5):
    print(i)


# --- The accumulator pattern ------------------------------------------
total = 0
count = 0
for t in trades:
    total += t["qty"] * t["price"]
    count += 1
print(f"Total: {total}, Count: {count}")


# --- Reading an error message on purpose -----------------------------
# Uncomment one line at a time to show these live:
# print("Total: " + 5)      # TypeError: can only concatenate str (not "int") to str
# print(totl)                 # NameError: name 'totl' is not defined
