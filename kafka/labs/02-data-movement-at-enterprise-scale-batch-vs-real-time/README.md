# Module 2 Lab - Data Movement at Enterprise Scale: Batch vs Real-Time

## Objectives

By the end of this lab you will have:

- Applied the batch vs real-time distinction to real data scenarios, not just definitions
- Practised justifying a data-movement choice against actual consequences (deadlines, failure
  visibility, infrastructure cost) rather than instinct

## Format

A written decision exercise. No code. Individually or in pairs - decide, then compare with
another pair before the group discussion.

## Setup

- Having run `demos/02-.../BatchSettlementJob` and `LivePriceFeedSimulator` first will help, but
  isn't required to start

## Task

For each scenario below, decide: **batch, or real-time?** For each decision, write 2-3 sentences
justifying it against at least one of the concrete consequences from the demo (deadline risk,
failure visibility, infrastructure cost, or how "bounded" the data actually is) - not a general
impression.

### Scenario A - End-of-Day Settlement

Every trade executed during the day needs to be reconciled and reported once the market closes,
in a fixed overnight window before systems reset for the next trading day.

**Your decision and justification:**

### Scenario B - A Live Price Feed

Prices for tracked instruments change continuously throughout the trading day, and the trading
platform's risk calculations need to reflect the current price, not this morning's price.

**Your decision and justification:**

### Scenario C - Monthly Client Statements

Once a month, every client account gets a statement summarising the month's activity and current
holdings, generated and sent out on a fixed date.

**Your decision and justification:**

## Discussion Questions

1. Is there a scenario above where the "obviously correct" answer would change if data volume
   grew 100x? Which one, and why?
2. Name one thing that could go wrong with each of your three choices if it were secretly
   implemented as the *other* pattern (a real-time price feed built as an hourly batch job, or
   end-of-day settlement built as a live stream). Be specific.

## Deliverable

Your three decisions with justifications, and answers to both discussion questions.

## Acceptance criteria

- Each of the three decisions references a specific consequence from the demo, not just "batch
  feels right" or "real-time feels more modern"
- The 100x-volume question identifies a genuine tipping point, not just "yes, everything changes"
- Both failure-mode answers describe a concrete, plausible failure - not a vague "it would be bad"
