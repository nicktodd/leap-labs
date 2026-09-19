# Demo: Module 1 — Core Java Refresher

**Duration:** 20 minutes
**Files:** `TradeDemo.java`, `Trade.java`, `MalformedTradeException.java`
**Prerequisite:** Java 21 and Maven installed

This module is called a "refresher," but don't assume it — treat it as a translation guide from
the Python you spent all of Sprint 4 in. Every section below is framed as "here's the Python idea
you already know, here's its Java form."

## Part 0: Why Java looks so different, in one sentence (2 min)

Narration: Python is dynamically typed (a variable's type is checked at runtime, if at all) and
uses indentation to mark blocks. Java is statically typed (every variable's type is declared and
checked by the compiler, before the program ever runs) and uses braces `{}` and semicolons to
mark statements and blocks. Neither is "better," they're different trade-offs: Java catches a
whole class of mistakes before you run anything; Python lets you move faster with less ceremony.

## Part 1: Types and control flow (5 min)

Show the top of `TradeDemo.java`. Narrate each declaration against its Python equivalent:

```java
String tradeId = "T0001";   // Python: tradeId = "T0001"   (str)
double quantity = 120;       // Python: quantity = 120       (float)
boolean isBuy = true;         // Python: isBuy = True          (bool, capital T in Python!)
```

Point out: `String`, `double`, `boolean` are the *declared type* — once declared, that variable
can never hold a different type. Try (verbally, don't actually break the demo) assigning
`quantity = "not a number"` — Python would allow it silently; Java refuses to even compile it.

Show the `if`/`else` block — same logic as Python's `if`/`else`, but note the required
parentheses around the condition and the braces instead of indentation.

## Part 2: The collections framework (7 min)

The big three, mapped directly:

| Python | Java |
|---|---|
| `list` | `List` (usually `ArrayList`) |
| `dict` | `Map` (usually `HashMap`) |
| `set` | `Set` (usually `HashSet`) |

```java
List<Trade> trades = new ArrayList<>();
```

Narration: `List<Trade>` is a **generic** type — "a list that only ever holds `Trade` objects."
Python's `list` can silently mix types (`[1, "two", 3.0]`); Java's compiler won't let a `List<Trade>`
hold anything else, ever. This is caught at compile time, not discovered later at runtime.

Show the `for (Trade trade : trades)` loop — narrate it as identical in spirit to Python's
`for trade in trades:`.

Show building `Map<String, Double> valueByInstrument` with `getOrDefault(key, 0.0)` — this is
*exactly* Module 3's Python pattern (`totals.get(key, 0.0) + value`), just spelled differently.
Point out this manual accumulation is also exactly what Module 9's `groupby` replaced in pandas —
the underlying idea (partition, then accumulate) is the same in every language.

## Part 3: Checked vs. unchecked exceptions (6 min)

Narration: Python doesn't distinguish exception types at the language level — `try`/`except` can
catch anything, and nothing forces you to catch anything. Java has two categories:

- **Unchecked** (`extends RuntimeException`) — the compiler does not require you to handle it.
  `NumberFormatException` from `Double.parseDouble("not-a-number")` is unchecked; if nothing
  catches it, the program crashes, the same as an uncaught Python exception.
- **Checked** (`extends Exception`, not `RuntimeException`) — the compiler *requires* every
  caller to either catch it or declare `throws SomeException` on their own method. This category
  has no Python equivalent — Python's exceptions are all effectively "unchecked" from the
  compiler's perspective, since Python doesn't check any of this before running.

Show `MalformedTradeException extends Exception` and `parseTradeLine(...) throws
MalformedTradeException` — narrate that the `throws` clause is not optional decoration, the code
won't compile without it, given the method body can throw that checked exception.

## Key message

Almost everything you did with Python's dynamic typing, lists/dicts/sets, and `try`/`except` has
a direct Java equivalent — the concepts transfer, only the syntax and the compiler's strictness
change. The one genuinely new idea is checked exceptions: a category of error the compiler
forces you to acknowledge, which Python has no equivalent of at all.
