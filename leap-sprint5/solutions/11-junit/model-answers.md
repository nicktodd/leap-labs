# Model Answers — JUnit

## Why `@CsvSource` includes an exact-boundary case

`"1000, 1000, 2000, true"` tests `currentPortfolioValue + orderValue == riskLimit` exactly. This
is the single most important row in that table — an off-by-one error in `canAcceptOrder` (using
`<` instead of `<=`) would pass every other row and fail silently on real client accounts sitting
precisely at their limit. The row immediately after it (`1000, 1000.01, 2000, false`) exists for
the same reason, checked from the other side.

## Why two `@Nested` classes, not one flat list

`WhenInputIsInvalid` and `WhenOrderIsAtTheBoundary` group tests by *what's being tested*, not by
*which JUnit feature is being demonstrated*. A test report organised this way reads as
documentation of `RiskLimitChecker`'s actual behaviour — a colleague could learn what the class
does just from the `@DisplayName`s, without opening the source file. Grouping instead by "here are
my `@ParameterizedTest`s, here are my `assertThrows` tests" would document the test suite's
*technique*, which is far less useful to a future reader trying to understand the business rule.

## Why `assertAll` in `zeroOrNegativeOrderValueThrows`

Both assertions are about the same exception, so if one fails, seeing whether the other also
failed is genuinely useful diagnostic information in a single test run — rather than fixing one,
re-running, and only then discovering the second problem.

## The connection to Module 3's validation requirements

`RiskLimitChecker` is a stand-in for exactly the kind of validation logic Module 3's mission
brief describes (requirement 3: "a buy order cannot be accepted if it would take the client's
total portfolio value over their risk limit"). The thorough test suite built here is direct
preparation for Module 12, where this same class of logic gets built into the actual mission
project — test-first, the way Module 10 practised.
