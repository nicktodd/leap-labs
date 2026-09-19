# Module 11 Demo Guide — JUnit

Open `JUnitFeaturesDemoTest.java` and run it first, then walk through it top to bottom.

```bash
mvn test
```

Expect: 14 tests run, 1 skipped, 0 failures. Point out the skipped count before diving in — it's
deliberate, not a problem (see `@Disabled` at the bottom).

## `@BeforeEach` — Fresh State, Every Test

Every lab this sprint has created its test objects inline, inside each test method. `setUp()`
here does it once, and JUnit re-runs it before *every single test method* — each test gets its
own fresh `Holding`, with zero risk of one test's leftover state leaking into another. Ask: what
would happen if `holding` were created once, outside any method, and shared across tests? (Answer:
tests could pass or fail depending on execution order — exactly the kind of flaky, order-dependent
test suite `@BeforeEach` prevents.)

## `assertThrows` — the Formal Way

Point out `adjustBelowZeroThrows()`. Every previous lab that tested for an exception did it with a
manual `try { ... fail(...); } catch (X e) { ... }`, or relied on the test framework failing loudly
if an exception propagated up uncaught. `assertThrows` is shorter, and — this is the important
part — it **fails the test if no exception is thrown at all**, which is easy to get wrong with a
hand-rolled `try/catch` (an empty catch block with nothing after it will silently let the test
pass even if the code never threw).

## `assertAll` — Grouped Assertions

Run `bondReportsTickerAndFeeTogether()` and deliberately break it (e.g., temporarily change
`BondInstrument`'s flat fee) to show **both** failures reported together, not just the first one
JUnit happens to reach. Contrast with what a chain of three separate `assertEquals` calls would
show: only the first failure, hiding the second until the first is fixed and the test is re-run.

## `@ParameterizedTest` — One Test Body, Many Inputs

`bondFeeIsAlwaysFive` and `equityFeeIsOnePercentOfTradeValue` replace what would otherwise be
four or five near-identical copy-pasted test methods. Point out the difference between
`@ValueSource` (one input per run) and `@CsvSource` (an input *and* its expected output, paired).
Ask: when would you reach for one over the other? (`@ValueSource` when the assertion logic is the
same for every input; `@CsvSource` when each input has a different expected result.)

## `@Nested` — Structure the Test Report Itself

`WhenHoldingIsAtZero` groups two tests under a name that reads like a sentence:
"JUnitFeaturesDemoTest > when the holding is at exactly zero > any negative adjustment throws."
This is documentation, generated for free from the test structure — nobody has to keep a separate
spec document in sync with what's actually tested.

## `@Disabled` — Skipping With Intent on Record

The last test is deliberately skipped, with a reason. Contrast with commenting a test out or
deleting it: both lose the fact that the test was *intended* to exist, and why it currently
doesn't run. `@Disabled` keeps that information visible in the test report itself.

## Points to Make Explicitly

- **None of this changes what you were already doing conceptually** — it's the same "write a
  test, make an assertion" pattern from every earlier module, with better tools for organising
  and expressing it.
- **`@DisplayName` matters more than it looks like it should.** A test report full of
  `bondFeeIsAlwaysFive` is fine; a test report full of "a bond's fee is always exactly $5,
  regardless of trade value" is something a non-technical stakeholder could actually read.

## Part Two: Mocking and Isolation (`MockitoAndHamcrestDemoTest`)

This is the part of the module that takes people longest to get comfortable with — slow down
here, and expect to spend as much time on this file as on everything above it combined.

### Start With the Problem, Not the Tool

Before touching Mockito, ask the group to look at Module 8's `OrderExecutor` tests (the ones
using a real `BondInstrument` and a real `InMemoryReportWriter`) and answer honestly: **if one of
those tests goes red, which class is actually broken?** They can't tell without investigating —
the test exercises `OrderExecutor`'s coordination logic *and* `BondInstrument`'s real fee formula
*and* `InMemoryReportWriter`'s real storage, all in one go. A bug in any of the three produces
the same symptom: a red test with `OrderExecutor`'s name on it.

This is the entire justification for mocking, and it has to land before any Mockito syntax does:
**a unit test should test one unit.** `OrderExecutor`'s actual job is small — ask its
`Instrument` for a fee, ask its `ReportWriter` to write a line — and testing that job properly
means controlling what its collaborators do, not trusting their real implementations to behave
correctly too.

### `@Mock` and `@ExtendWith(MockitoExtension.class)`

Point out the two fields at the top of the class and the class-level annotation. `@Mock` creates
a fake `Instrument` and a fake `ReportWriter` — objects of the right type that do nothing at all
by default, and remember every call made to them. `MockitoExtension` is what actually processes
the `@Mock` annotations before each test runs (functionally similar to `@BeforeEach`, but for
mock creation specifically).

### Stubbing: `when(...).thenReturn(...)`

Walk through `executorUsesWhateverFeeTheInstrumentReturns()`. Read it as a sentence: "when
`calculateFee` is called with `1000.0`, then return `42.0`." Stress that **42.0 is not a real fee
any instrument would compute** — that's deliberate. The test doesn't care what a real fee formula
looks like; it only cares whether `OrderExecutor` correctly uses whatever its collaborator gives
it back.

Show `stubbingWithAnArgumentMatcher` next — `anyDouble()` stubs a response for *any* argument,
for tests where the exact input genuinely doesn't matter to what's being checked.

### `verify()`: Proving a Call Actually Happened

This is the concept most people find hardest, because it's a new *shape* of assertion — not
"does this value equal that value," but "did this interaction with a collaborator actually
happen." Run through all three `Verifying` tests:

- `verify(mockWriter).write("C001: $42.0")` — proves `OrderExecutor` talked to its writer, with
  exactly the right line
- `verify(mockInstrument, times(1)).calculateFee(500.0)` — proves it happened, and exactly once
  (not zero times, not twice)
- `verifyNoInteractions(mockWriter)` — proves a mock was **never touched at all**, useful for
  proving a branch that shouldn't reach a collaborator genuinely doesn't

Ask: what would `verify(mockWriter, times(2)).write(anyString())` mean, and when might it fail
in a way that reveals a real bug (e.g., a loop accidentally writing the same line twice)?

### `ArgumentCaptor`: When `verify()` Isn't Precise Enough

`verify(mockWriter).write("C001: $42.0")` requires an exact string match. Sometimes you want to
capture what was actually passed and inspect it more flexibly — show
`capturesTheLineWrittenForDetailedInspection`, and point out the two-step shape: capture first,
then assert on `captor.getValue()` separately.

### Mocks vs. Hand-Rolled Fakes — Bring Back Module 8

Run the `MocksVersusHandRolledFakes` tests side by side. `InMemoryReportWriter` was a perfectly
good, deliberately-written test double — but it only replaced *one* of `OrderExecutor`'s two
collaborators. The test still depends on `BondInstrument`'s real fee formula being correct. The
mock-based version replaces *both*, and returns `999.0` — a number no real instrument would ever
produce — specifically to prove the test result cannot possibly depend on real instrument logic
at all.

**Say explicitly: neither approach is "wrong."** A hand-rolled fake is often the right call when
a collaborator is simple and stable (`InMemoryReportWriter` will likely never need to change).
Mockito earns its complexity when there are many collaborators, or when their real behaviour is
exactly what you need to control per-test.

## Part Three: Hamcrest Matchers

Run the three `HamcrestMatchers` tests. The core pitch: `assertThat(value, matcher)` reads closer
to the requirement it's checking than `assertEquals(expected, actual)` does, and matchers
**compose** — `allOf(greaterThan(0.0), lessThan(100.0))` in one readable line, where a plain
JUnit equivalent needs two separate assertions or a hand-written boolean expression with no
useful failure message if it's wrong.

Point out `containsString`, `hasSize`, and `hasItem` specifically — these read almost like plain
English, which matters more than it seems for a test suite other people will read later.

## Points to Make Explicitly (Mocking and Hamcrest)

- **Not every class needs mocks.** `RiskLimitChecker` (this module's lab) takes only primitives —
  there's nothing to mock, and that's fine. Mocking earns its place specifically when a class has
  collaborators whose real behaviour would otherwise leak into the test.
- **A test full of mocks that never calls `verify()` on any of them is a smell.** If you stub a
  collaborator but never check it was actually used correctly, you're only testing "did this not
  crash," not "did this coordinate correctly."
- **Hamcrest and JUnit's own assertions aren't competitors — use whichever reads more clearly for
  a given check.** `assertEquals` is perfectly fine for a simple equality check; reach for
  Hamcrest when composing conditions or asserting on strings/collections.

## Transition to the Lab

Learners write a comprehensive test suite from scratch for a given, already-implemented class
(`RiskLimitChecker`) — using `@BeforeEach`, `@Nested`, `@ParameterizedTest`, `assertThrows`, and
`assertAll` deliberately, not just `@Test` and `assertEquals` as in earlier modules.

**`RiskLimitChecker` takes only primitive parameters — it has no collaborators, so there's
nothing to mock.** Mention this explicitly rather than letting it go unaddressed: it's a genuine
example of a class that doesn't need mocking, not an oversight in the lab design. Point out that
`OrderExecutor` and `OrderProcessingEngine` (Modules 8, 12, and 13) are exactly the kind of
classes where mocking would apply if their existing tests were rewritten for true isolation — a
good optional exercise for anyone who finishes early.
