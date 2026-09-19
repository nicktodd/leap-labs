# Demo: Module 13 — Cyber Challenge, Mission Day

**Duration:** This is a facilitator run-of-show for a full day, not a single demo.
**Prerequisite:** Teams from Sprint 1/2, the `starter/` codebase pushed to a repository each
team has access to, Jenkins access, and a room/slot booked for each team's 5-minute
presentation.

This module has no new technical content to demo. Every skill needed today was taught earlier
in the sprint: Agile ceremonies (Modules 01-02), the PR workflow (Module 03), review etiquette
(Module 04), OWASP recognition (Module 09), Secure Code Warrior practice (Module 10), and
remediation with Copilot (Module 11). Today is where all of it gets used together, under a
realistic time constraint, for the first time.

## Suggested schedule (adapt to your actual day length)

### Kick-off / Mission Briefing (15 min)

Read the mission brief (see the lab README) to every team together, as if you were a client
handing over a real, urgent piece of work. Key framing: "A security audit flagged the Merchant
Portal. You have one day to diagnose it, fix what you find, and be ready to explain your work
to someone non-technical by end of day." Answer clarifying questions, but don't reveal how many
vulnerabilities exist or where, that's the point of the challenge.

### Sprint Planning, lite (10 min)

Each team triages: skim the codebase, agree who's looking where, and set a one-sentence sprint
goal for the day (Module 02 skill, applied for real, under time pressure this time).

### Work Block 1

Teams work. Circulate rather than lecture. If a team is stuck on a specific file, prompt them
back to Module 09's model answers or Module 10's platform, don't just hand them the answer.

### Standup (10 min, roughly at the midpoint of the day)

Run a real standup: three questions, under 15 minutes for the whole cohort or per-team as your
numbers dictate. This is a genuine checkpoint, not a formality, use it to catch a team that's
badly stuck.

### Work Block 2

Teams continue: fixing, committing via the Module 03 PR workflow, and preparing their
5-minute presentation.

### Review: Team Presentations (5 min per team)

Each team presents to a **non-specialist audience** (other teams, or a trainer explicitly
playing a business stakeholder role, not a fellow engineer). The presentation should cover:
what they found, why it mattered in plain English, and how they fixed it, not a line-by-line
code walkthrough.

### Retro (Start / Stop / Continue, whole cohort or per team)

Run the Module 02 format, but pointed at the whole sprint, not just today. This feeds directly
into Module 14's wrap-up.

## Facilitator notes

- **Don't rescue teams too early.** Getting stuck and working through it under time pressure is
  part of the intended experience, this mirrors a real incident far more than a smoothly guided
  exercise would.
- **The six vulnerabilities span categories already covered this sprint** (A01, A02, A03, A06,
  A08, A10), deliberately, so no team should be facing something entirely unfamiliar, only
  unfamiliar *code*.
- **Presentations are the part most teams under-prepare for.** Budget real time for it in the
  schedule, and hold the 5-minute limit firmly, this is itself a practised skill (Module 04's
  communication habits, applied to a non-specialist audience).

## Key message

Nothing here is new. The entire point of Mission Day is proving, under a real time constraint,
that this sprint's separate skills (agile process, Git hygiene, OWASP recognition, secure
remediation, presenting clearly) function together as one coherent way of working, not as
isolated module exercises.
