# Module 10 Demo Guide - Code Quality Fundamentals & Code Smell Hunt

Module 1 asked learners to look at `TradeReportGenerator` and write down what concerned them,
in their own words, with no formal vocabulary required. Today gives that reaction a vocabulary -
and, more importantly, a way to MEASURE it, not just feel it.

## What "Code Quality" Actually Means

"Code quality" is vague on its own. Today breaks it into five concrete, checkable properties,
each with a real example already sitting in `TradeReportGenerator.java`:

| Property | Question it answers | Where it shows up today |
|---|---|---|
| **Method length** | Is this method doing one job, or several? | `doIt()` is 44 lines |
| **Cyclomatic complexity** | How many distinct paths through this code need testing? | `doIt()` has ~7 |
| **Mutable state** | Can this code be called twice safely? | 3 static fields |
| **Exception handling** | Does a failure get seen, or hidden? | 1 empty catch block |
| **Naming & magic numbers** | Does the code explain itself? | `q`, `pr`, `0.001` |

None of these are opinions. Each one is something you can point at, count, and show someone else
- which is exactly why tools like SonarQube (Module 12) can check for them automatically.

## Run the Scanner

```bash
mvn compile
java -cp target/classes com.neueda.leap.mission.stream.CodeSmellScanner
```

By default it scans `TradeReportGenerator.java` directly - no arguments needed if you're running
from this module's folder.

## Verified Output, Walked Through

```
-- Method length & complexity --
  public static void doIt(String p) throws Exception {
    length: 44 lines | parameters: 1 | approx. cyclomatic complexity: 7
    -> LONG METHOD: over 30 lines is a strong signal it's doing more than one job
    -> HIGH COMPLEXITY: 7 decision points means 7 distinct paths through this method
```

**Point at this directly**: `doIt()` reads a file, parses each line, calculates a fee, decides
between three fee rates, accumulates two running totals, counts trades, builds a report string,
prints a summary, AND writes a file - eight distinct responsibilities in one method. Length and
complexity aren't the smell themselves; they're the SYMPTOM. The smell is "this method has more
than one reason to change" (the Single Responsibility Principle, named explicitly).

```
-- Mutable static state --
  3 mutable static field(s) found:
    static Map<String, Double> tot = new HashMap<>();
    static Map<String, Double> f = new HashMap<>();
    static int c = 0;
  -> calling doIt() twice in the same run would accumulate, not reset.
```

This is worth proving, not just asserting: ask the room what `doIt()` would print if called
twice in a row with the same file. (It would double every total - `tot` and `f` never get
cleared.) Static mutable state doesn't just look messy; it's a real, demonstrable bug waiting for
the day someone calls this method more than once.

```
-- Swallowed exceptions --
  line 46: } catch (Exception e) {
    -> catch block has no code - any exception here is silently discarded
```

Direct callback to Module 8: this IS the bug that module built an entire demo around. Same file,
same line, now caught by a tool instead of by reading the code by eye.

```
-- Magic numbers --
  3 unexplained decimal literal(s), 2 distinct value(s): [0.001, 0.0005]
```

`0.001` and `0.0005` are fee rates - but nothing in the code says so. A reader has to already
know the business rule to recognize what these numbers mean. A named constant
(`EQUITY_FEE_RATE = 0.001`) makes the comment unnecessary, because the name IS the explanation.

```
-- Unclear naming (1-2 character identifiers) --
  4 short local variable name(s): [c, p, q, pr]
```

`c` (trade count), `p` (file path), `q` (quantity), `pr` (price) - every one of these compiles
identically to a full word. The computer doesn't care. The next developer does.

## The Concept, Named

- **Code smell**: not a bug - the code runs correctly - but a signal that the design will make
  future changes harder or riskier than they need to be.
- **Single Responsibility Principle**: a method/class should have one reason to change. `doIt()`
  has at least four (parsing, fee calculation, aggregation, reporting).
- **DRY (Don't Repeat Yourself)**: not obviously violated in this small file, but worth
  mentioning as the smell-detector's blind spot - duplication needs a human eye or a dedicated
  tool (Module 12), not this scanner.
- **These are measurements, not a checklist to blindly satisfy** - a 44-line method isn't
  automatically wrong; it's a strong SIGNAL worth investigating. Module 11 is where these
  findings turn into an actual, safe refactor.

## Transition to the Lab

Learners run the same scanner (or extend it) against a different piece of the starter codebase,
or manually hunt for smells the scanner doesn't catch - then write up findings the same
structured way: named smell, specific location, why it matters.
