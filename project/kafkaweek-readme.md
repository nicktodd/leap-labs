# Kafka Week - Project Friday Guidance

## Context

This week's teaching covers technical debt and refactoring, batch vs. real-time data movement,
event-driven architecture, Kafka fundamentals, designing a Kafka pipeline, batch loading and ETL
patterns, data quality, code quality and quality gates, and DevSecOps.

This week's deliverable is the event backbone: BR-06 already says accepting an order and
executing it are separate steps, execution can fail or be delayed, and the record of intent
can't depend on it succeeding. This week that separation becomes real, connected by messages
rather than one request doing both.

## The trap to avoid

Kafka's fundamental guarantee, which this week's teaching covers, is at-least-once delivery: a
message can arrive more than once, on a rebalance, a crash between a commit and an offset
acknowledgement, or a replay. That's a fact about the tool, not a design decision. The design
decision is what your team does about it, and it's worth treating as the actual point of this
week, not a detail to handle if there's time left:

- What happens the second time whatever consumes these events sees the same message? Not what
  should happen, what does your code actually do, and can you demonstrate it rather than just
  describe it?
- BR-09 required the order status, the cash movement and the position update to succeed or fail
  together back in an earlier week. The same requirement applies here, now from the execution side. What
  makes that true when it's a different part of your system doing the update?
- BR-08 needs a current market quote at the point of execution. Where does that quote come from
  in your design, and what happens when it can't be obtained? You have two options for a market
  data source: a real one online, such as Yahoo Finance, or a fake API your instructors will
  provide, details to follow. Either is fine, but check what its request limits are before you
  design around it, not after you've hit them.
- If your existing data design already has a way of recognising a duplicate or repeated order, this is
  where it gets tested for real. If it doesn't, this is where you'll find out you need one.

## Suggested Friday session

- Design your event flow as a team before writing a producer or consumer: what gets published
  when an order is accepted, what consumes it to execute the order, and what else in your own
  architecture might care about the outcome.
- Walk through the duplicate-delivery question above and agree, concretely, what your consumer
  does the second time, then write a test or a demonstration that proves it.
- This week's characterisation-testing lesson works best applied to code that already has some
  age on it: is there something from earlier worth pinning down with tests before
  you touch it again, now this new pressure is on it?
- Add quality gates to your CI pipeline if you haven't already, and agree what "shifting security
  left" means for this specific service.
- Refine the backlog and risk list against what building this has taught you.

## What to present to the class

- A diagram of your event flow: what's published, by what, and what consumes it.
- What happens when your consumer sees the same message twice, demonstrated, not just described.
- How you're keeping BR-09 true on the execution side.
- A refactor you made and why, or a piece of debt you're deliberately carrying and why.
- An updated backlog and risk list.
