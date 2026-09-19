# Module 13 Lab — Cyber Challenge: Mission Day

## Mission Brief

*(Read as if from a client, at the start of the day.)*

> PaySprint's Merchant Portal, the internal service merchants use to view and request payouts,
> was flagged by an external security audit last week. The audit didn't share full details,
> only that "multiple issues, several of them serious, were found across access control,
> configuration, dependencies, and process design." Legal and Compliance want a full
> remediation plan, and evidence of fixes, by end of day. You'll present your findings and
> your approach to a non-technical stakeholder this afternoon.

You will not be told in advance how many vulnerabilities exist or where. Finding them is part
of the challenge.

## Objectives

By the end of today you will have:

- Applied Agile ceremonies to a real, time-boxed delivery challenge: kick-off, standup, review,
  retro
- Applied OWASP knowledge (Module 09) and Secure Code Warrior practice (Module 10) to identify
  and fix vulnerabilities in a codebase you haven't seen before
- Submitted your work via Git with proper branching and commit hygiene (Module 03)
- Presented a technical solution and your secure coding approach to a non-specialist audience

## Setup

- The [`starter/`](starter) codebase for this mission: PaySprint's Merchant Portal
- A team repository, with your agreed branching strategy from Sprint 1 Module 12
- Jenkins access, if your team wants to wire up a pipeline as part of the fix (not required,
  but a nice stretch goal given Module 08's skills)
- GitHub Copilot Chat

## Running the day

### Kick-off

Read the mission brief together as a team. Agree who's looking where.

### Sprint Planning (lite)

Skim the whole codebase first, don't dive into fixing the first thing you spot. As a team,
agree a one-sentence sprint goal for the day (Module 02), and a rough allocation of who
investigates which area.

### Diagnose and fix

For every vulnerability you find:

1. Identify the OWASP Top 10 (2025) category
2. Explain the real-world risk in plain English
3. Fix it, using Copilot critically (Module 11), not blindly
4. Commit the fix via a proper branch and PR (Module 03), reviewed by a teammate (Module 04)

### Standup

Join the scheduled cohort standup: three questions, keep it under 15 minutes total.

### Prepare your presentation

Prepare a 5-minute presentation for a **non-specialist audience**. Cover:

- What you found (in plain English, not jargon)
- Why it mattered (the real-world risk, not the technical mechanism)
- How you fixed it (the approach, not a line-by-line code read-through)

### Review

Present to the group.

### Retro

Run a Start / Stop / Continue retro (Module 02) covering the whole sprint, not just today.
Bring your notes to Module 14.

## Acceptance criteria

- All vulnerabilities you found are documented: category, risk, and fix, one entry each.
- Every fix is committed via a proper Git branch and PR, reviewed by a teammate.
- Your 5-minute presentation is ready and rehearsed, and avoids unexplained jargon.
- You have Start / Stop / Continue notes from your retro, ready for Module 14.

There is no published answer key for this exercise, ask your trainer for feedback on your
findings and fixes directly.
