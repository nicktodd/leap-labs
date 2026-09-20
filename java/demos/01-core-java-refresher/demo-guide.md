# Demo: Module 1 - Core Java Refresher

**Duration:** 20 minutes
**Files:** `TradeDemo.java`, `Trade.java`, `MalformedTradeException.java`
**Prerequisite:** Java 21 and Maven installed

This module is called a "refresher," but don't assume it - treat it as a grounding pass over the
language fundamentals everything else this week builds on. Every section below pairs a core
concept with the line of code that demonstrates it.

## Part 0: Why Java's strictness pays off, in one sentence (2 min)

Narration: Java is statically typed - every variable's type is declared and checked by the
compiler, before the program ever runs - and uses braces `{}` and semicolons to mark statements
and blocks. That strictness is a deliberate trade-off: it catches a whole class of mistakes
before you ever run the program, at the cost of a little more ceremony up front.

## Part 1: Types and control flow (5 min)

Show the top of `TradeDemo.java`. Narrate each declaration:

```java
String tradeId = "T0001";
double quantity = 120;
boolean isBuy = true;
```

Point out: `String`, `double`, `boolean` are the *declared type* - once declared, that variable
can never hold a different type. Try (verbally, don't actually break the demo) assigning
`quantity = "not a number"` - Java refuses to even compile it.

Show the `if`/`else` block, noting the required parentheses around the condition and the braces
that mark each block.

## Part 2: The collections framework (7 min)

The big three:

| Interface | Typical implementation |
|---|---|
| `List` | `ArrayList` |
| `Map` | `HashMap` |
| `Set` | `HashSet` |

```java
List<Trade> trades = new ArrayList<>();
```

Narration: `List<Trade>` is a **generic** type - "a list that only ever holds `Trade` objects."
The compiler won't let a `List<Trade>` hold anything else, ever. This is caught at compile time,
not discovered later at runtime.

Show the `for (Trade trade : trades)` loop.

Show building `Map<String, Double> valueByInstrument` with `getOrDefault(key, 0.0)` - narrate the
pattern: look up the running total for a key, defaulting to `0.0` if it isn't there yet, then
write the updated total back. This "partition, then accumulate" shape recurs constantly whenever
you're summarising a collection by some grouping key.

## Part 3: Checked vs. unchecked exceptions (6 min)

Narration: Java has two categories of exception:

- **Unchecked** (`extends RuntimeException`) - the compiler does not require you to handle it.
  `NumberFormatException` from `Double.parseDouble("not-a-number")` is unchecked; if nothing
  catches it, the program crashes.
- **Checked** (`extends Exception`, not `RuntimeException`) - the compiler *requires* every
  caller to either catch it or declare `throws SomeException` on their own method. This forces a
  developer to consciously decide how to handle a foreseeable failure, rather than letting it
  crash the program by accident.

Show `MalformedTradeException extends Exception` and `parseTradeLine(...) throws
MalformedTradeException` - narrate that the `throws` clause is not optional decoration, the code
won't compile without it, given the method body can throw that checked exception.

## Key message

Java's type system and collections framework give you compile-time guarantees that catch entire
classes of bugs before the program ever runs. The one genuinely new idea today is checked
exceptions: a category of error the compiler forces you to acknowledge, right there in the
method signature.
