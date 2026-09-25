# Demo: Module 1 - Python Fundamentals: Syntax, Data Types & Control Flow

**Duration:** 30-40 minutes (flexible - see the note below)
**Files:** `fundamentals_demo.py` (new foundational material), `trade_summary_demo.py` (the
capstone, unchanged)

**A note on pacing:** this module's slide deck now runs to 35 slides, deliberately more than
any one cohort will need. If your group already has some Python (or strong experience in
another language), skim or skip the early sections - comments/print, indentation, the REPL,
variables - and start from wherever the room's actual knowledge runs out. If your group is
genuinely new to Python, plan the fuller 40 minutes and don't rush the foundational sections;
the rest of the week depends on this module landing properly, and a for loop over a list of
dicts is genuinely opaque to someone who has never met a list or a dict on their own.

## Part 1: The Absolute Basics (8-10 min, skip for an experienced cohort)

Open `fundamentals_demo.py` and live-run it section by section (or retype each block into a
`python3` REPL - showing the REPL itself, once, is worth doing even if you then switch to
running the file).

- **Comments & print()**: `#` comments, `print()` with multiple arguments.
- **Indentation**: run the `if True:` block, then show `IndentationError` live by uncommenting
  the broken line - a real, and very common, beginner error is worth ten minutes of description.
- **Variables**: assignment, naming (snake_case), and that reassignment is allowed - even to a
  different type. Contrast explicitly with any language in the room that requires a type
  declaration.

Key message: none of this is exciting on its own, but every later module - pandas, Node,
Angular's TypeScript - assumes this is automatic. Ten minutes here saves confusion for weeks.

## Part 2: Types & Operators (6-8 min)

Continue through `fundamentals_demo.py`'s data-types and operator sections:

- `type(x)` on each of the four basics: str, int, float, bool.
- Arithmetic operators, including `//` and `%` - these trip people up; show `7 // 2` and
  `7 % 2` side by side and ask the room to predict each before revealing.
- Comparison operators and `and`/`or`/`not` - emphasise `==` vs `=` explicitly, it's the most
  common early typo.

## Part 3: Strings (5-6 min)

- Concatenation with `+`, and why `"Trade " + 1` fails (TypeError) - a good moment to show an
  error on purpose, before Part 6 makes it the explicit topic.
- Indexing and slicing - the same `[start:end]` shape that lists use later, worth flagging
  explicitly as something to remember.
- f-strings - narrate that this is the formatting style the rest of the course uses
  throughout, not just today.
- One or two string methods (`.strip()`, `.upper()`) - enough to show that methods exist and
  return a new value, not a full tour.

## Part 4: Lists & Dictionaries (6-8 min)

This is the section the original version of this module skipped straight past - take the time.

- Lists: creation, indexing, `.append()`, `in`. Keep it concrete: a list of quantities, not an
  abstract example.
- Dictionaries: creation, key access, `.get()` with a default. Make the point explicitly that
  `.get()` doesn't raise an error when a key is missing - this matters later for messy real data.
- **Lists of dictionaries** - the payoff slide. Build the `trades` list live, on screen, from
  the individual list and dict pieces just shown, so the room sees it assembled rather than
  appearing fully formed. This is the shape (CSV rows, API responses, database results) they'll
  meet constantly from here on.

## Part 5: Control Flow (6-8 min)

Walk through `if`/`elif`/`else`, then `for` loops - **in this order**: over a plain list of
numbers first (`for q in quantities:`), then `range()`, then over the `trades` list of dicts
built in Part 4. Narrate the accumulator pattern explicitly (`total = 0`, then `total += ...`
inside the loop) - name it as a pattern, because it recurs constantly, including in pandas from
Module 5 onward.

Show a `while` loop only briefly (a simple counter) - control flow in data work is dominated by
`for` loops over collections, not `while` loops, and the demo should reflect that emphasis.

## Part 6: Reading Errors (3-4 min)

Uncomment the two error lines at the bottom of `fundamentals_demo.py` one at a time.
Deliberately slow down here: read the traceback aloud, point at the error TYPE
(TypeError/NameError) and the message, and connect it back to what caused it. This is a skill,
not an afterthought - a beginner who can read `TypeError: can only concatenate str (not "int")
to str` and know what to do next will spend far less time stuck than one who just re-runs the
code hoping it fixes itself.

## Part 7: The Capstone - Running Summary Output (5 min)

Switch to `trade_summary_demo.py` and run it end-to-end. This is deliberately the same shape as
Part 4's `trades` example, just larger and wired into real control flow: total trade count,
total value, and a per-side (BUY/SELL) breakdown, computed with plain Python - no libraries.

Narration: this whole script could be five lines of pandas. That's the point - Module 1 makes
you feel the manual bookkeeping (running totals, manual counters, manual dict lookups) so that
when pandas replaces it in Module 5, the value is obvious, not just asserted.

## Key message

Python's core syntax - variables, types, operators, strings, lists, dictionaries, and control
flow - is the same regardless of whether you ever touch a data library. Everything from here on
is built on this foundation, and it's worth getting solid before moving on.
