# Module 3 Lab - Event-Driven Architecture Concepts: Events vs Requests

## Objectives

By the end of this lab you will have:

- Applied the event-driven vs request-driven distinction to real scenarios
- Recognised that "batch vs real-time" (Module 2) and "event vs request" (today) are two
  different questions, even though they often correlate

## Format

A written decision exercise, revisiting Module 2's scenarios. No code. Individually or in pairs.

## Setup

- Having run `demos/03-.../RequestDrivenExample` and `EventDrivenExample` first will help
- Your Module 2 answers, if you kept them - you'll be comparing today's decisions against them

## Task

For each of Module 2's three scenarios, decide: **event, or request?** Justify in 2-3 sentences,
specifically addressing: does the caller need an answer before it can proceed, or is it only
announcing that something happened?

### Scenario A - End-of-Day Settlement

**Your decision and justification:**

### Scenario B - A Live Price Feed

**Your decision and justification:**

### Scenario C - Monthly Client Statements

**Your decision and justification:**

## Discussion Questions

1. **Compare today's answers to Module 2's batch/real-time answers.** Is there a scenario where
   the batch-vs-real-time answer and the event-vs-request answer point in genuinely different
   directions? What does that tell you about the two axes being independent questions?
2. Pick one scenario and describe what would break if it were built the wrong way on this axis -
   a request built as an event, or an event built as a request. Be specific about the failure, not
   just "it would be worse."
3. In a live price feed, could a consumer that genuinely needs an *answer* (not just a
   notification) still be built on top of an event-driven system? How?

## Deliverable

Your three decisions with justifications, and answers to all three discussion questions.

## Acceptance criteria

- Each decision explicitly addresses whether the caller needs a response before proceeding
- Discussion question 1 identifies whether the two axes actually diverge for any scenario, with
  reasoning, not just a restated conclusion
- Discussion question 3's answer describes a genuine mechanism (e.g. a reply-to pattern, or a
  separate request-driven lookup alongside the event stream), not "it can't be done"
