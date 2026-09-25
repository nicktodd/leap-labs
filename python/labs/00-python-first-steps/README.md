# Module 1 Lab (Part 1) - Foundational Python Practice

## Who this is for

If you've never written Python before, or it's been a long time, start here. If you're already
comfortable with variables, types, lists, and dictionaries, skip straight to **Part 2**
(`starter_payments.py`, in `../01-python-syntax-control-flow/`) - this lab won't teach you
anything new.

There's no shame either way. Some of the room will fly through this in ten minutes; others will
want the full session. Both are fine - the point of the course is what you can build by the end
of the week, not how fast you get through page one.

## Objectives

By the end of this lab you will have:

- Declared variables of each basic type and printed them with their types
- Done arithmetic and formatted a number with an f-string
- Written an if/elif/else chain with three branches
- Built and looped over a list, using the accumulator pattern by hand
- Built a dictionary, read from it, and used `.get()` with a default
- Built a small list of dictionaries and looped over it - the exact shape Part 2 starts from

## Setup

- Python 3.11+ installed and on your PATH
- No libraries and no imports: plain Python only
- Starter file: `starter.py`, in `labs/00-python-first-steps/`
- Run it with `python starter.py` as you go - run it after every TODO, not just at the end

## Task

Work through the seven TODOs in `starter.py`, in order. Each one is a few lines - run the script
after each one and check the output makes sense before moving to the next. Don't use `sum()`,
`max()`, or any built-in you haven't been shown yet - TODO 5c specifically asks you to add the
numbers up by hand, because that's the pattern (`total = 0`, then `total += ...` inside a loop)
you'll use constantly from here on, including once pandas takes over most of this work for you
in Module 5.

## Acceptance criteria

- The script runs with `python starter.py` and produces no errors.
- TODO 1 prints a single message naming your name, favourite number, and the bool.
- TODO 2 prints all four variables, each with its correct type name (`str`, `int`, `float`, `str`
  for `side`).
- TODO 3 prints the trade's value twice: once unformatted, once as `{value:.2f}`.
- TODO 4 correctly classifies at least two different `quantity` values you test it with.
- TODO 5 prints the first and last item, all five items on their own lines, and a correct sum
  computed without `sum()`.
- TODO 6 prints `trade["id"]` and `trade["price"]`, and shows `.get()` returning a default for a
  key that doesn't exist.
- TODO 7 prints one formatted line per trade, for three trades, using an f-string.

## What next

Once this all runs cleanly, move on to **Part 2**: `../01-python-syntax-control-flow/starter_payments.py`
and its own `README.md` - a longer, more realistic lab using the same ideas against a bigger,
messier dataset.
