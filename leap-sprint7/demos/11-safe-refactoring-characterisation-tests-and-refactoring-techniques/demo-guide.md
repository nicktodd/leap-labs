# Module 11 Demo Guide — Safe Refactoring: Characterisation Tests & Refactoring Techniques

Module 10 produced a written smell report on `shared/starter-codebase`. Today, that report
becomes an actual, safe change to the real code — "safe" meaning provably behaviour-preserving,
not just "looks fine to me."

## Step 1: Write the Safety Net BEFORE Touching Anything

```bash
cd shared/starter-codebase
mvn test
```

Look at `src/test/java/.../TradeReportGeneratorCharacterisationTest.java` before running it.

**This is a characterisation test, not a unit test in the usual sense.** It doesn't assert what
`doIt()` SHOULD do — it records, verbatim, what `doIt()` ACTUALLY does today, including its bug:

```java
assertTrue(output.contains("Processed 10 trades"),
        "expected exactly 10 of the 12 rows to be processed");
```

12 rows go in, 2 are malformed, `doIt()` silently drops both — and the test locks that in
deliberately. **This is not this refactor's job to fix.** Module 8 already built an entire
module around fixing exactly this bug, on a different codebase. Mixing "refactor the structure"
with "fix the behaviour" in the same change is how refactors turn into rewrites nobody can
review — the discipline here is real, not academic.

Run it:

```bash
mvn test
```

Verified: `Tests run: 1, Failures: 0`. This one green test is now the safety net for everything
that follows — any change that breaks it means the refactor changed observable behaviour, which
is exactly what a safe refactor is not allowed to do.

## Step 2: Perform ONE Small, Named Refactoring Step

Module 10's scanner flagged `0.0005` as a duplicated literal — used for BOND's fee rate AND the
fallback rate, by coincidence rather than design. Today's refactor fixes exactly that finding,
and nothing else.

**Before:**
```java
if (typ.equals("EQUITY")) {
    fee = val * 0.001;
} else if (typ.equals("BOND")) {
    fee = val * 0.0005;
} else {
    fee = val * 0.0005;
}
```

**After** — `FeeCalculator.java`, a new class:
```java
static final double EQUITY_FEE_RATE = 0.001;
static final double OTHER_FEE_RATE = 0.0005; // covers BOND and any other trade type

public static double calculateFee(String tradeType, double tradeValue) {
    double rate = tradeType.equals("EQUITY") ? EQUITY_FEE_RATE : OTHER_FEE_RATE;
    return tradeValue * rate;
}
```

`doIt()` now calls `FeeCalculator.calculateFee(typ, val)` — one line, replacing eight.

**Two named techniques, both textbook Fowler refactorings, walked through mechanically:**

- **Extract Method.** Take a self-contained block of code, give it a name, move it to its own
  method, and replace the original block with a call to that method. Mechanically, three things
  happened here:
  1. The `if/else if/else` block (8 lines) was copied into a new method, `calculateFee`, on a
     new class, `FeeCalculator`.
  2. Inside that new method, `typ` and `val` (the local variables the old block read) became
     parameters — `tradeType` and `tradeValue` — because the new method has no access to
     `doIt()`'s local variables anymore.
  3. Back in `doIt()`, the original 8 lines were deleted and replaced with one line:
     `double fee = FeeCalculator.calculateFee(typ, val);`
  Nothing about WHAT gets computed changed — only WHERE the computation lives, and what it's
  called.

- **Introduce Named Constant.** Take a literal value whose meaning isn't obvious from reading it
  (`0.001`, `0.0005`) and replace it with a named constant (`EQUITY_FEE_RATE`,
  `OTHER_FEE_RATE`) declared once, near the top of the class. Every place that used to write the
  literal now references the name instead. The compiled behaviour is identical — `0.001` and
  `EQUITY_FEE_RATE` are the same value at runtime — but a reader no longer has to already know
  the business rule to understand the code.

**Why do these two together, in one step, rather than as two separate refactors?** Because they
target the SAME finding from Module 10 (the duplicated `0.0005` literal) and they reinforce each
other: extracting the method gives the constants somewhere sensible to live (as `static final`
fields on `FeeCalculator`, not floating loose inside `doIt()`), and naming the constants makes
the newly-extracted method self-documenting instead of just "shorter."

Note what did NOT change: `doIt()` still reads the file the same way, still accumulates into
the same static maps, still writes the same report. Only the fee calculation moved.

## Step 3: Prove Nothing Broke

```bash
mvn test
```

Verified: still `Tests run: 1, Failures: 0`. Same characterisation test, unchanged, still green
— proof the refactor is behaviour-preserving, not just "probably fine."

## Step 4: The New Test That Wasn't Possible Before

Module 10's lab asked: *why can't you unit test the fee logic today?* Because it was inline,
inside a loop, inside a method that also does file I/O. Now it can be tested directly:

```java
@Test
void equityTradesAreChargedTheEquityRate() {
    double fee = FeeCalculator.calculateFee("EQUITY", 10_000);
    assertEquals(10.0, fee, 0.0001);
}
```

Run the full suite:

```bash
mvn test
```

Verified: `Tests run: 4, Failures: 0` — the original characterisation test, plus three new,
fast, isolated tests for `FeeCalculator` that need no file, no static state, and run in
milliseconds.

## Step 5: A Further Refactor — Extract Interface + Replace Conditional with Polymorphism

`FeeCalculator` is a genuine improvement, but it still has an `if/else` (now a ternary) deciding
between two behaviours based on a `String`. That's a smell in its own right — every time a new
trade type needs its own rate, someone has to find and edit this exact method. Two more named
techniques address that directly. This step is **optional and not required by the lab** — it's
here to show what refactoring further, past the first obvious step, actually looks like.

**Extract Interface.** Name the CAPABILITY the conditional is really choosing between, as an
interface:

```java
public interface FeeRule {
    double feeFor(double tradeValue);
}
```

`FeeRule` doesn't say HOW a fee is calculated — only that anything implementing it can, given a
trade value, produce a fee. This is the same idea as an interface anywhere else in this course
(compare to how `OrderRepository` let `OrderService`, in Sprint 6, not care whether it was
talking to a real database or a mock) — code that depends on the interface doesn't need to know
which implementation it's actually using.

Two implementations, one per fee rule:

```java
public class EquityFeeRule implements FeeRule {
    static final double RATE = 0.001;
    public double feeFor(double tradeValue) { return tradeValue * RATE; }
}

public class OtherFeeRule implements FeeRule {
    static final double RATE = 0.0005;
    public double feeFor(double tradeValue) { return tradeValue * RATE; }
}
```

**Replace Conditional with Polymorphism.** Instead of one method asking "which type is this?"
with an `if`/ternary, a lookup picks the right `FeeRule` object, and that OBJECT decides its own
fee — no conditional logic left at all:

```java
public class FeeRuleCalculator {
    private static final Map<String, FeeRule> RULES = Map.of("EQUITY", new EquityFeeRule());
    private static final FeeRule DEFAULT_RULE = new OtherFeeRule();

    public static double calculateFee(String tradeType, double tradeValue) {
        FeeRule rule = RULES.getOrDefault(tradeType, DEFAULT_RULE);
        return rule.feeFor(tradeValue);
    }
}
```

**Point at exactly what changed and why it matters**: there is no `if`, `else`, or `?:` anywhere
in `FeeRuleCalculator`. Adding a new trade type with its own rate — say, `FUND` at a third rate
— means writing one new class (`FundFeeRule`) and adding one new map entry. It does NOT mean
finding and editing an existing method's conditional logic, which is exactly the kind of change
that risks breaking an unrelated branch by accident in a method nobody fully remembers anymore.

**Prove it's equivalent, not just similar:**

```java
@Test
void matchesFeeCalculatorForEquityTrades() {
    assertEquals(FeeCalculator.calculateFee("EQUITY", 10_000),
            FeeRuleCalculator.calculateFee("EQUITY", 10_000), 0.0001);
}
```

Run the suite:

```bash
mvn test
```

Verified: `Tests run: 7, Failures: 0` — the characterisation test, `FeeCalculator`'s 3 tests, and
3 new parity tests proving `FeeRuleCalculator` produces IDENTICAL output to `FeeCalculator` for
every trade type in the real data. Two different internal designs, one proven-identical result —
this is what "behaviour-preserving" looks like when comparing two refactors of the same logic to
EACH OTHER, not just each one to the untouched original.

**Is this worth it, for THIS codebase, right now?** Genuinely debatable, and worth putting to the
room: `FeeRuleCalculator` is more code (5 files vs. 1) to express the same two rates. The payoff
— adding a new fee rule without touching existing logic — only matters if new trade types are
actually expected to arrive often. Refactoring toward more flexibility has a cost, and applying
it where the flexibility isn't needed is itself a smell (over-engineering). This is a genuinely
open question, not a "more design patterns are always better" lesson.

## The Concept, Named

- **Characterisation test**: describes current behaviour, bugs included, written BEFORE
  refactoring — the opposite of a spec, and not something you'd normally keep forever (once the
  code is genuinely well-tested, ordinary unit tests replace it).
- **Refactoring, precisely defined**: a change to the code's internal structure that does NOT
  change its observable behaviour. If behaviour changes, it isn't a refactor — it's a rewrite,
  and it needs different scrutiny (new tests for the new behaviour, not a green characterisation
  test as proof).
- **Small, named steps**: Extract Method, Introduce Named Constant, Extract Interface, Replace
  Conditional with Polymorphism — not "clean up the fee logic" as one vague, unreviewable
  change. Each step has a name someone else would recognize from a refactoring catalogue
  (Fowler's *Refactoring* is the canonical one).
- **More refactoring isn't automatically better**: `FeeRuleCalculator` is objectively more
  flexible than `FeeCalculator` — and objectively more code, for a benefit that only pays off if
  new trade types actually show up. Knowing when to STOP refactoring is as much a skill as
  knowing the techniques.

## Transition to the Lab

Learners perform a SECOND, different refactoring step on the same codebase — protected by the
same characterisation test, adding their own new unit test for the piece they extract.
