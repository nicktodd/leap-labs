# Module 12 Lab — Model Answer (Instructor Reference)

## Warm-up answers

```text
99.5% SLO: error budget = 0.5% of 43,200 = 216 minutes
99.95% SLO: error budget = 0.05% of 43,200 = 21.6 minutes
```

Halving the allowed failure rate (0.5% to 0.05%, a factor of 10 in this case, "one extra nine")
shrinks the budget by the same factor, from 216 minutes down to 21.6 minutes. Worth delegates
seeing this arithmetic directly: reliability targets don't cost linearly more as they tighten,
they cost punishingly more.

## 1. Error budget

```text
Total minutes in 30 days = 30 x 24 x 60 = 43,200 minutes
SLO = 99.9% availability
Error budget = 0.1% of 43,200 = 43.2 minutes
```

## 2. Actual downtime

Summing every day's downtime in `sli-data.md`:

```text
0.5 + 1.0 + 0.5 + 2.0 + 0.5 + 1.0 + 0.5 + 35.0 + 0.5 + 1.0 + 0.5 + 2.0 + 0.5 + 6.0 = 51.5 minutes
```

(All days not listed had 0 minutes of downtime.)

## 3. Breached or not?

**Breached.** 51.5 minutes actual vs 43.2 minutes budgeted, an overage of **8.3 minutes**, or
about **19% over budget**.

## 4. Diagnose the pattern

The single 35-minute incident on Day 17 (bad deploy, missing production config) accounts for
**68%** of the month's total downtime, and on its own is already close to the entire monthly
budget (35.0 out of 43.2 minutes). Without that one incident, total downtime would have been
16.5 minutes, comfortably within budget. This is a materially different situation from "the
service is generally flaky", it's "one specific, identifiable failure mode dominates."

## 5. Recommendation (example)

**Pause the next feature release and prioritise reliability work, specifically targeted at the
Day 17 failure mode, not broad reliability work in general.**

Reasoning to present to a Product Owner: the budget has been breached, so per the team's own
SLO commitment, reliability work takes priority this cycle, that's the agreed mechanism, not a
judgement call the team is making up on the spot. Critically, because one incident dominates,
the fix is likely to be narrow and fast (e.g., a deployment safeguard that validates required
config exists before a rollout completes) rather than an open-ended reliability initiative,
this is a scoped, short piece of work, not a reason to abandon the roadmap for a month.

## What to check as an instructor

- The error budget and total downtime arithmetic are both correct (43.2 minutes; 51.5 minutes).
- Teams correctly conclude the budget was breached, not "close but fine."
- Teams engage with the *pattern*, not just the total, the strongest answers identify that the
  single incident is the real story, and shape their recommendation around fixing that specific
  cause rather than vague "be more careful" reliability work.
- The recommendation is framed in terms a Product Owner would find persuasive (ties back to
  Module 01's Product Owner role), not just "the maths says stop."
