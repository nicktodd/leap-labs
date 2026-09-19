# Demo: Module 12 — SRE Principles Introduction

**Duration:** 18 minutes
**Prerequisite:** none. Conceptual, with two worked calculations.

## Part 1: What SRE is, and how it relates to DevOps (3 min)

Narration: Site Reliability Engineering (SRE) treats operating software as an engineering
problem, not a separate "ops" function bolted on afterwards. The same rigour applied to writing
code (measurement, automation, iteration) gets applied to keeping it running reliably. In
practice, this means the team that builds a feature shares real accountability for how it
behaves in production, not just for shipping it.

Relate this back to Module 05's DevOps content: DevOps is the cultural shift (shared ownership,
breaking down the dev/ops divide). SRE is a concrete, measurable way of *implementing* that
culture, with specific practices: SLIs, SLOs, error budgets, and toil reduction, which is
exactly what the rest of this module covers. Where DevOps says "everyone owns reliability," SRE
says "here is precisely how much reliability we owe, and how we'll know if we're behind."

## Part 2: SLI, SLO, SLA, spelled out (4 min)

Narration, pointing at the diagram, and write all three acronyms out in full on the board, not
just the letters: these three terms get used interchangeably in casual conversation, but they
mean genuinely different things, and mixing them up leads to real confusion about who owes what
to whom.

- **SLI, Service Level Indicator**: what you actually *measure*. A raw number, not a target.
  Example: "percentage of requests that succeeded in under 200ms, over the last hour."
- **SLO, Service Level Objective**: the internal *target* for that measurement. Example: "99.9%
  of requests succeed in under 200ms, measured over a rolling 30-day window." This is a promise
  the team makes to itself.
- **SLA, Service Level Agreement**: a *contractual* commitment, usually to an external party
  (a customer, a regulator, another team), usually **looser** than the internal SLO, with real
  consequences (service credits, penalties, breach of contract) if missed.

Ask the room: why would a team deliberately set their SLO tighter than their SLA? Answer: so
that if things start slipping, the team notices and acts *before* they're at risk of breaching
an actual contractual commitment. The SLO is an early-warning threshold; the SLA is the real
deadline.

## Part 3: The Four Golden Signals (2 min)

Narration: when deciding *what* to measure as an SLI in the first place, Google's SRE book
popularised four categories worth monitoring for almost any service, known as the **Four Golden
Signals**:

- **Latency**: how long requests take
- **Traffic**: how much demand the service is under
- **Errors**: the rate of requests that fail
- **Saturation**: how "full" the service is (CPU, memory, connection pools, etc.)

Point out: most useful SLIs are built from one of these four, if you're not sure what to
measure for a new service, start here.

## Part 4: The error budget, worked twice (6 min)

Narration: if the SLO is 99.9% availability over 30 days, the **error budget** is the remaining
0.1%, the amount of unreliability the team is explicitly allowed before they've broken their own
promise.

**Worked example 1, a simple case:**

```text
30 days = 43,200 minutes total
SLO: 99.9% availability
Error budget = 0.1% of 43,200 minutes = 43.2 minutes of allowed downtime
```

**Worked example 2, a stricter SLO:**

```text
SLO: 99.99% availability (one extra nine)
Error budget = 0.01% of 43,200 minutes = 4.32 minutes of allowed downtime
```

Narration: point out how dramatically the budget shrinks for each additional "nine" of
reliability, this is why teams don't reach for 99.99% or 99.999% casually, each extra nine costs
disproportionately more engineering effort to hold.

Narration continued: this reframes "reliability" from a vague aspiration into a number a team
can actually manage against. If the budget isn't spent, the team has room to take some risk,
ship faster, try something new. If it's already spent (or overspent), the team's priority
shifts to reliability work until they're back in budget. This is the mechanism that balances
feature delivery against reliability, not a values statement, a number.

## Part 5: Toil, in more depth (3 min)

Narration: toil is manual, repetitive, automatable operational work that scales linearly with
service growth and provides no lasting engineering value. Concrete examples worth naming:

- Manually restarting a service every time it wedges, instead of fixing why it wedges
- Manually running the same diagnostic steps for every alert, instead of scripting them
- Manually granting the same category of access request, instead of self-service automation

Narration: SRE teams often explicitly cap how much of their time can go to toil (a common
guideline is no more than 50%), specifically so there's always guaranteed time left for the
engineering work that would prevent the next incident, not just react to it. Toil left
unchecked tends to grow to fill all available time, since it's always more urgent-feeling than
long-term prevention work.

## Key message

SLIs, SLOs, and error budgets turn "is this reliable enough" from a feeling into a number a team
can calculate, track, and make real trade-off decisions against, exactly what today's lab
practises. Reducing toil is what protects the time needed to act on those decisions.
