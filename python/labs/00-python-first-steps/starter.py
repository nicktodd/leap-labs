# Module 1 Lab (Part 1) - Foundational Python Practice
#
# No libraries, no imports. Work through the TODOs in order - each one builds on
# the last. If you already know Python, skim this and move straight to Part 2
# (starter_payments.py) - this lab is here so nobody is left behind, not to slow
# you down if you don't need it.


# TODO 1: Getting started
# Declare three variables: my_name (a string, your own name), my_favourite_number
# (an int), and learning_python (a bool, set to True). Print a single message using
# an f-string that includes all three, e.g.
#   "Ada is learning Python. Favourite number: 7. True."


# TODO 2: One trade, by hand
# Declare four variables describing a single trade: trade_id (str, e.g. "T0001"),
# quantity (int), price (float), and side (str, "BUY" or "SELL").
# Print each variable together with its type, using type(x).__name__, e.g.
#   "trade_id: T0001 (str)"


# TODO 3: Arithmetic
# Using the quantity and price from TODO 2, compute the trade's value
# (quantity * price) and print it as a plain number, then again formatted to
# 2 decimal places using an f-string (value:.2f).


# TODO 4: Classify it
# Write an if/elif/else chain that prints "small trade" if quantity is under 50,
# "medium trade" if quantity is under 200, and "large trade" otherwise. Run your
# code with a few different quantity values (change TODO 2's quantity and rerun)
# to check all three branches actually work.


# TODO 5: A list of quantities
# Create a list called quantities containing five different int values of your
# choosing. Then:
#   a) print the first and last item using indexing (quantities[0], quantities[-1])
#   b) use a for loop to print each quantity on its own line
#   c) use the accumulator pattern (a running total, updated inside the loop) to
#      compute and print the sum of all five - without using the built-in sum()


# TODO 6: One trade, as a dict
# Rebuild the single trade from TODO 2 as a dictionary called trade, with keys
# "id", "qty", "price", and "side". Then:
#   a) print trade["id"] and trade["price"]
#   b) use trade.get("commission", 0.0) to show that a missing key returns the
#      default instead of raising an error


# TODO 7: A list of trades (bridge to Part 2)
# Create a list called trades containing THREE dicts, each shaped like TODO 6's
# trade (keys "id", "qty", "price", "side"). Then write a for loop that prints,
# for each trade, a line like:
#   "T0001: BUY 120 @ 185.32 = 22238.40"
# (id, side, qty, price, and qty*price, all from the same dict, using an f-string)
#
# This is exactly the shape starter_payments.py (Part 2 of this module's lab)
# starts from - a list of dicts - so once this works, you're ready for it.
