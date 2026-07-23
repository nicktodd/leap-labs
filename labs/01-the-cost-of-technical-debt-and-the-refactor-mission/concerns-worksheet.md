# Technical Debt Review — `TradeReportGenerator.java`

**Reviewers:** Sprint 7 Lab 1

## Concern 1

**Where:** Variable names throughout `doIt()` — `tot`, `f`, `tkr`, `typ`, `q`, `pr`, `val`, `x`, `p`, `br`, `out`

**What's the concrete cost or risk?**
A developer joining the team must hold the entire method in working memory to understand what any
variable means. `f` is fees, `tot` is totals by ticker, `x` is the parsed CSV row — none of
this is readable without decoding the abbreviations first. The concrete cost: every future change
to this method carries a higher risk of introducing a bug because the reviewer cannot quickly
verify intent. A code review of "is this change correct?" becomes "let me first decode what every
variable is."

## Concern 2

**Where:** Static mutable fields `tot`, `f`, and `c` at the class level (lines 8-10)

**What's the concrete cost or risk?**
`doIt()` accumulates into shared static state rather than local variables. Running the program
twice in the same JVM without explicitly resetting those fields (as the characterisation test
has to do manually) would silently double-count trades. Any future caller — a scheduler running
the report multiple times, a test suite running tests in sequence — gets wrong numbers with no
error or warning. The concrete cost: correctness depends on a hidden invariant (the JVM must be
fresh) that is not expressed anywhere in the code.

## Concern 3

**Where:** The `catch (Exception e) { // skip bad row }` block in `doIt()` (lines 39-41)

**What's the concrete cost or risk?**
Bad rows are silently discarded. The program reports "Processed 10 trades" against a 12-row CSV,
but the two malformed rows disappear without any indication of why or which rows they were.
Operationally, this means a data quality problem looks like a clean run. If the CSV feed changes
format, or a bug is introduced in parsing, the program will silently produce an incomplete report
and no alarm will fire. The concrete cost: debugging a discrepancy between the CSV row count and
the processed count requires reading the source code, not reading a log.

## The Row-Count Question

`trades.csv` row count (excluding header): **12**

Program's own reported count: **10**

Do they match? **No.** Two rows are malformed — one has a blank quantity field and one has a
non-numeric price — so `Double.parseDouble()` throws on each, and the catch block silently
discards them. The program processes 10 of 12 rows and gives no indication 2 were dropped.

## In One Sentence Each

What would make this codebase expensive to **extend**?
Single-letter variable names and the absence of any method decomposition mean any change to
`doIt()` requires re-reading the entire method to understand what each line does before
writing a single new line.

What would make this codebase expensive to **trust**?
Static mutable state and silent exception-swallowing mean you cannot tell, from a run's output
alone, whether the numbers are correct or whether rows were silently dropped.
