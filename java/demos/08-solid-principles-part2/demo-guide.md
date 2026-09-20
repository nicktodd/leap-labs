# Module 8 Demo Guide - SOLID Principles Part 2 (I, D)

Run `SolidDemoPart2.java` end to end first, then walk back through it section by section.

```bash
mvn package
java -cp target/classes com.neueda.leap.mission.engine.SolidDemoPart2
```

## I - Interface Segregation Principle

`FatReportable` bundles three unrelated output formats into one interface. `CsvOnlyReportBad`
only ever needs CSV, but has to implement `toConsole()` and `toPdf()` anyway - both stubbed with
an exception. Run the demo and watch `toPdf()` crash on what the type system claims is a "full"
`FatReportable`. Ask the group: **how would a caller know, just from the type, that calling
`toPdf()` is unsafe?** They can't - that's the actual cost of a fat interface, not just
"inconvenience for the implementer."

Contrast with `CsvSettlementReport implements CsvReportable`: it's not that this class "chose"
not to support PDF - `toPdf()` doesn't exist on it at all. The compiler removes the mistake,
rather than the mistake being caught (or not) at runtime.

Tie back explicitly: this is the same shape of fix as Module 6's `flawed-design.mmd` and Module
7's `BadReportGenerator` - a class forced to do too much, but this time the "too much" is imposed
from outside, by an interface, not chosen by the class itself.

## D - Dependency Inversion Principle

`BadOrderExecutor` constructs its own `ConsoleReportWriter` inside itself. Ask: **how would you
unit test `BadOrderExecutor.execute()` without it actually printing to the console?** There's no
clean way - the dependency is baked in.

`OrderExecutor` takes a `ReportWriter` through its constructor instead. Run the demo and show the
exact same class working with two completely different writers - `InMemoryReportWriter` (for
testing, no console output at all) and `ConsoleReportWriter` (for real use) - with zero changes
to `OrderExecutor` itself between the two.

**The name is the confusing part - spend time on it.** "Dependency Inversion" doesn't mean
"inject dependencies" (that's a mechanism, not the principle). It means: high-level policy
(`OrderExecutor`, which decides *what* to do) should not depend on low-level detail
(`ConsoleReportWriter`, which decides *how* output actually happens). Instead, both depend on an
abstraction (`ReportWriter`) that neither one owns. The dependency *direction* is inverted from
what you'd naturally write: instead of high-level code reaching down into detail, detail reaches
up to satisfy an interface the high-level code defines.

## Points to Make Explicitly

- **ISP and DIP are often the two hardest of the five to spot**, because SRP/OCP/LSP violations
  usually show up as "this one file does something obviously wrong." ISP and DIP violations show
  up as friction - a stubbed method here, an untestable class there - that's easy to shrug off as
  normal, rather than recognising as a design smell with a name.
- **`InMemoryReportWriter` isn't a demo trick - it's the actual reason DIP matters for testing.**
  Every JUnit test written this sprint that doesn't hit a real database, file, or console is
  benefiting from this exact pattern, whether or not it was called out explicitly.

## Transition to the Lab

Learners implement `CsvSettlementReport` (ISP) and `OrderExecutor` (DIP) themselves, with the
bad versions (`FatReportable`/`CsvOnlyReportBad`, `BadOrderExecutor`) available in the demo
project as reference, not as files to modify.
