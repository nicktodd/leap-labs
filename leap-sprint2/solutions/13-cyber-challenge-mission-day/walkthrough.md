# Module 13 Mission Day — Instructor Walkthrough

No answer key is published to delegates for this exercise, the diagnosis is the point. These
notes are for facilitators giving feedback during and after the day.

## The six vulnerabilities

| # | File | OWASP 2025 Category | Risk |
|---|---|---|---|
| 1 | `MerchantController.java` | A01: Broken Access Control | Any merchant can view any other merchant's payout details (IDOR) |
| 2 | `application.properties` | A02: Security Misconfiguration | All actuator endpoints exposed (incl. env dump), full stack traces returned to clients |
| 3 | `pom.xml` (`log4j-core:2.14.1`) | A03: Software Supply Chain Failures | Log4Shell, CVE-2021-44228, critical unauthenticated RCE |
| 4 | `PayoutApprovalService.java` | A06: Insecure Design | No segregation of duties, requester can approve their own payout |
| 5 | `WebhookController.java` | A08: Software or Data Integrity Failures | Incoming webhook payloads trusted with no signature verification |
| 6 | `BatchPayoutJob.java` | A10: Mishandling of Exceptional Conditions | Failed transfers marked PAID anyway, risking double-payment or silent loss on retry |

See the fixed files in this folder. Note: `WebhookController.java`'s fix references an
`HmacUtil` helper that isn't included, it's illustrative of the *approach* (verify a signature
over the raw body before trusting the payload), not a drop-in compilable class. If a team
implements this fully, that's commendable and worth calling out specifically.

## Grading the presentations

Use this rubric, adapted from Module 04's review checklist, applied to a presentation instead
of code:

- **Plain English**: could someone with no engineering background follow the explanation of
  what was wrong and why it mattered?
- **Risk framed correctly**: does the team correctly connect each finding to a real-world
  consequence (money, data exposure, fraud), not just "this is bad practice"?
- **Fix explained at the right altitude**: approach and reasoning, not a line-by-line code
  read-through (a common failure mode under time pressure, teams default to showing code because
  it's what they just did, redirect them if they drift into it)
- **Time discipline**: five minutes, held firmly, this is itself a practised skill

## Common gaps to watch for

- Teams that fix #4 (insecure design) with a code-only patch but can't articulate *why* it's a
  design issue rather than a bug, prompt them back to Module 09's model answer distinction.
- Teams that miss #3 entirely (a dependency version, not obviously "code"), this is a good
  moment to reinforce that Module 05's Security Scan pipeline stage exists precisely to catch
  this class of finding automatically, rather than relying on someone spotting it by eye.
- Teams that fix #6 by wrapping the retry logic instead of fixing the status-recording bug
  itself, the actual root cause is that PAID no longer reliably means "money was sent."

## Retro follow-through

Whatever came out of each team's Start/Stop/Continue retro should be referenced directly in
Module 14's wrap-up, treat it as live input, not a formality that happened and is now over.
