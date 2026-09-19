# Module 12 Lab — Error Budget, Ship or Stabilise?

## Key terms, spelled out

- **SLI, Service Level Indicator**: what you actually measure (e.g. % of requests under 200ms)
- **SLO, Service Level Objective**: your internal target for that measurement (e.g. 99.9%)
- **SLA, Service Level Agreement**: a contractual commitment to an external party, usually
  looser than your SLO, with real consequences if missed

## Objectives

By the end of this lab you will have:

- Calculated an error budget from a stated SLO, for two different SLO strictness levels
- Determined whether a fictional service has breached its error budget over the last 30 days
- Decided, with reasoning, whether the team should ship a new feature or focus on reliability
- Presented your reasoning to the group

## Setup

- [`sli-data.md`](sli-data.md) from this lab: 30 days of downtime data for the fictional
  "PaySprint Notifications API," and its stated SLO

## Warm-up: two quick budget calculations

Before the main exercise, calculate the error budget (in minutes) for each of these SLOs, over
a 30-day window (43,200 minutes total):

1. An SLO of **99.5%** availability
2. An SLO of **99.95%** availability

Compare the two: how much does the budget shrink for that extra half a nine of reliability?
This is worth doing by hand once, so the main exercise's numbers feel concrete rather than
abstract.

## Task sheet

Work in your team.

1. **Calculate the error budget**
   The SLO is 99.9% availability over a rolling 30-day window, and the window contains 43,200
   minutes total. Calculate the error budget in minutes: how much downtime is the team allowed
   before breaching their own SLO?

2. **Calculate actual downtime**
   Sum the recorded downtime across all 30 days in `sli-data.md`.

3. **Compare and decide: has the budget been breached?**
   State clearly: is the team within budget, or have they breached it? By how much (in
   minutes, and as a percentage of the budget)?

4. **Diagnose, don't just total up**
   Look at the shape of the data, not just the total. Is the downtime spread evenly across the
   month, or dominated by one or two incidents? Does that change your recommendation?

5. **Recommend: ship the new feature, or focus on reliability?**
   Based on your calculation and your read of the incident pattern, make a clear recommendation
   to the (fictional) team: proceed with the next planned feature release, or pause and
   prioritise reliability work first. Justify it in a way a Product Owner (Module 01) would
   find persuasive, not just "the number says so."

6. **Prepare a two-minute presentation**
   As a team, prepare to present your calculation and recommendation to the group. Include the
   budget, the actual figure, and your reasoning, not just the conclusion.

## Acceptance criteria

- A correct error budget calculation, in minutes.
- A correct total downtime calculation from the provided data.
- A clear breached/not-breached conclusion, with the margin stated.
- A reasoned recommendation that references the *pattern* of incidents, not just the total.
- A short presentation ready to deliver to the group.

If you finish early, discuss: if this had been a single 51.5-minute outage instead of several
smaller ones plus one large one, would your recommendation change? Why or why not?
