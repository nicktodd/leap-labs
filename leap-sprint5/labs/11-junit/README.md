# Module 11 Lab — JUnit

## Objectives

By the end of this lab you will have:

- Written a comprehensive JUnit 5 test suite using `@BeforeEach`, `@Nested`, `@ParameterizedTest`,
  `assertThrows`, and `assertAll` — not just `@Test` and `assertEquals`
- Organised tests so the test report itself documents the behaviour being tested

## Setup

- Java 21 and Maven installed
- `RiskLimitChecker.java` (given, don't modify) — fully implemented, your job is to test it
- One example test is already in `RiskLimitCheckerTest.java`, showing the naming and
  `@DisplayName` convention to follow

## The Class Under Test

```java
public boolean canAcceptOrder(double currentPortfolioValue, double orderValue, double riskLimit)
```

- Returns `true` if `currentPortfolioValue + orderValue <= riskLimit`, `false` otherwise
- Throws `IllegalArgumentException` if `orderValue <= 0`
- Throws `IllegalArgumentException` if `riskLimit < 0`

## Task

Build out `RiskLimitCheckerTest.java` to cover the class thoroughly, using **each** of the
following JUnit features at least once:

1. **`@BeforeEach`** — set up a shared `RiskLimitChecker` instance before each test, rather than
   constructing a new one inline in every method.

2. **`@ParameterizedTest` with `@ValueSource`** — test that a *rejected* order (one that would
   push the portfolio over its limit) returns `false` across several different order values.

3. **`@ParameterizedTest` with `@CsvSource`** — test several `(currentPortfolioValue, orderValue,
   riskLimit)` combinations, each paired with its expected `true`/`false` result, including at
   least one exact-boundary case (`currentPortfolioValue + orderValue == riskLimit`).

4. **`assertThrows`** — one test for `orderValue <= 0`, one test for `riskLimit < 0`. Check the
   exception type; optionally check the message.

5. **`assertAll`** — at least one test that groups more than one assertion together (for example,
   asserting both that an exception was thrown AND something about its message, or checking two
   related outcomes of the same call).

6. **`@Nested`** — group your tests into at least two logically distinct nested classes (for
   example, "when the order is valid" vs. "when the input is invalid"), each with a `@DisplayName`
   that reads clearly in a test report.

## Deliverable

A completed `RiskLimitCheckerTest.java`.

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors
- Every feature in the numbered list above is used at least once, correctly
- Every test (and nested class) has a `@DisplayName` that would make sense to someone who has
  never read the code
- No test method is missing an assertion — every test actually checks something

## A note on mocking

You won't use Mockito in this lab — `RiskLimitChecker` takes only primitive parameters, so it has
no collaborators to mock. That's a deliberate, genuine example: not every class needs a mock.
See the demo (`MockitoAndHamcrestDemoTest.java`) for classes that *do* have collaborators worth
isolating.

If you finish early: `OrderExecutor` (copied into this project's demo, originally from Module 8)
depends on both an `Instrument` and a `ReportWriter`. Try rewriting a test for it using
`@Mock`/`when(...).thenReturn(...)`/`verify(...)` instead of the real `BondInstrument` and
`InMemoryReportWriter` — and compare how confident you are that a red test means `OrderExecutor`
itself is broken, versus one of its collaborators.
