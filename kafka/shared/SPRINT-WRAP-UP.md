# This Week's Wrap-up

## What This Sprint Built

**Mission A - Real-Time.** The trading platform's `OrderService` (Module 9) publishes a trade
event to Kafka (topics, partitions, and keys designed in Modules 4-6) every time an order is
accepted, fully decoupled from whoever consumes it.

**Mission B - Honesty.** `shared/starter-codebase`'s `TradeReportGenerator` went from a single
neglected file (Module 1) to a smell-hunted (Module 10), characterisation-tested and safely
refactored (Module 11), SonarQube-gated (Module 12), and security-scanned (Module 13) codebase -
the same file, module by module, genuinely improved and provably behaviour-preserving at every
step.

**Where they met.** Module 14's dashboard reads from BOTH: a Postgres warehouse table Module 7's
idempotent batch loader populates, and the live Kafka topic Mission A built - proving, with two
numbers that behave differently on rerun, that batch and stream answer genuinely different
questions.

## Self-Assessment: Can You Explain These, Specifically?

Not "did you attend the session" - can you give a concrete, specific answer for each:

1. Why does `INSERT ... ON CONFLICT` make a batch load safe to rerun, and what specifically
   breaks without it? (Module 7)
2. Why did the "Sonar way" quality gate PASS on a codebase with 2 BLOCKER bugs? What changed to
   make the same analysis genuinely FAIL? (Module 12)
3. Why did fixing `NotificationService.java`'s hardcoded credentials NOT remove them from the
   repository? What's the one action that actually neutralizes a leaked secret? (Module 13)
4. In Module 14's dashboard, which number stayed identical across two runs, which one changed,
   and why does that difference matter?

If any of these only get a vague answer ("it's about testing" / "it's a security thing"), that's
worth another look at the relevant demo guide before Friday.

## Friday

- **Guest speaker**
- **Weekly knowledge check (MCQ)**
- **Group retrospective** - what went well this sprint, what was genuinely hard, what you'd want
  explained differently next time
- The Secure Code Warrior Hackathon runs as its own standalone timed session, separate from this
  cadence

## What to Bring to the Retro

One specific moment from this sprint where a tool or test caught something you wouldn't have
caught by reading the code alone (Module 10's scanner, Module 12's SonarQube run, Module 13's
gitleaks scan are all real candidates) - and one moment where a real, verified run surprised you
(a number you expected to be different, an error you didn't anticipate).
