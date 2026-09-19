# Model Answers — SOLID Principles Part 2

## Kata A (ISP): why not just implement both interfaces "to be safe"?

It would compile fine to have `CsvSettlementReport implements CsvReportable, ConsoleReportable`
and give `toConsole()` a real implementation too. The kata specifically asks for only
`CsvReportable` because the exercise is about a *design habit*: implement what the class actually
needs right now, not what it might conceivably need later. Adding `ConsoleReportable` "just in
case" is the same instinct that produces fat interfaces in the first place — it starts small and
reasonable, and grows every time someone adds "just one more" capability nobody's using yet.

## Kata B (DIP): what the reflection test is actually checking, and why it matters

`OrderExecutorTest.constructorDependsOnTheReportWriterAbstraction` checks the constructor's
*declared parameter type*, not runtime behaviour — it would fail even if you passed in a
`ConsoleReportWriter` correctly, if the constructor signature itself said
`OrderExecutor(ConsoleReportWriter writer)` instead of `OrderExecutor(ReportWriter writer)`. That
distinction is the whole principle: DIP isn't about which object you happen to pass at runtime,
it's about what the class's own signature *permits* you to pass. A constructor typed to the
concrete class can never accept `InMemoryReportWriter` — the compiler would refuse it, regardless
of how the object behaves.

## A question worth asking about your own mission design

Look back at your Module 4 `mission-model.mmd`. Does `OrderExecutor` (or whatever you called it)
depend on `Portfolio` as a concrete class, or would it make more sense for it to depend on some
abstraction over "a thing I can query and update holdings on"? There's a real, defensible case
for *not* introducing that abstraction yet — YAGNI cuts both ways, and Module 12's mission build
is where this decision gets made for real, not hypothetically.
