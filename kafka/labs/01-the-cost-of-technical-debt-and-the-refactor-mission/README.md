# Module 1 Lab - The Cost of Technical Debt & the Refactor Mission

## Objectives

By the end of this lab you will have:

- Reviewed a real, working codebase honestly, without immediately trying to fix it
- Named specific, concrete costs of technical debt - not a general impression of "messy code"
- Read this week's mission brief and understood what the refactor mission actually asks for

## Format

This is a **review, not a coding kata**. Work in pairs. Do not change any code in
`shared/starter-codebase` - it's reused, in its current state, by Modules 10-13.

## Setup

- Java 21 and Maven installed
- Run the codebase first, so you're reviewing something you've actually seen work:

  ```bash
  cd shared/starter-codebase
  mvn compile
  java -cp target/classes com.neueda.leap.mission.stream.legacy.TradeReportGenerator
  ```
- Read `shared/mission-brief.md`

## Task

Read `TradeReportGenerator.java` with your partner. Using `concerns-worksheet-template.md`, write
down the **first three things that concern you** - in the order you actually noticed them, not
reordered by importance afterwards. For each one:

- Name the specific line(s) or pattern, not a vague feeling
- Explain the concrete cost: what could go wrong, or what would be expensive, because of this
- Resist the urge to write "and here's how I'd fix it" - that's not today's job

Then answer, as a pair:

- **Compare `trades.csv`'s row count to the program's own "Processed N trades" output.** Are they
  the same? If not, where did the difference go, and would you have noticed without being told to
  check?
- **In one sentence each**: what would make this codebase expensive to extend, and what would
  make it expensive to trust?

## Deliverable

Your completed `concerns-worksheet-template.md`.

## Acceptance criteria

- Exactly three concerns listed, each naming a specific location or pattern in the code
- Each concern states a concrete cost or risk, not just "this looks bad"
- The row-count question is answered correctly, with the actual cause identified
- No code in `shared/starter-codebase` has been modified
