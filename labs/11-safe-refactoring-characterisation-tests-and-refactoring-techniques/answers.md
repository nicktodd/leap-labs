# Module 11 Lab — Part C Answer

## Why `recordTrade()` Still Cannot Be Tested in Full Isolation

Unlike `FeeCalculator`, which takes its inputs as parameters and returns its output as a return
value, `recordTrade()` reads and writes the static fields `tot`, `f`, and `c` on
`TradeReportGenerator` directly. These fields are not passed in, and the result is not returned
— the method reaches out to shared mutable state that lives outside its own scope.

This means:

1. **Setup cost in every test:** Any test calling `recordTrade()` must manually reset `tot`, `f`,
   and `c` before it runs, otherwise a previous test's state bleeds in and the assertions become
   meaningless.

2. **No concurrency safety:** Two tests running `recordTrade()` at the same time would corrupt
   each other's state through the shared static fields — the fields are not thread-local.

3. **No true isolation:** `recordTrade()` cannot be given controlled inputs and have its output
   inspected without going through the class-level state. You can observe the result only by
   reading `tot.get(ticker)` and `f.get(ticker)` after the call — which is reading shared state,
   not a return value.

Extract Method moved the *code* into a named method with a clear name and a clear place in the
class. It did NOT remove the problem: the dependency on static mutable state (`tot`, `f`, `c`)
is still there. Removing that would require a different refactoring step — extracting the state
into instance variables (making `TradeReportGenerator` instantiable) or passing the maps in as
parameters — neither of which Extract Method alone performs.
