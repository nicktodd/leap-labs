# Sprint 8 — Project Friday Guidance

## Context

This week's teaching covers identity, access management and zero trust, JavaScript and
TypeScript fundamentals, Node.js, NestJS, DTOs and validation in NestJS, secure DB access and
password hashing, and JWT issuing and validation.

This week's deliverable is real authentication: BR-01 needs registration and secure sign-in,
BR-02 needs a client restricted to their own data, and BR-03 needs a session that's time-limited
and revocable. Whatever your team did about authentication in Sprint 6, left it open, stubbed
something, or built it for real, this is the week it either arrives properly or gets revisited
with what you now know.

## The trap to avoid

- Zero trust is this week's framing for a reason. Once this service is real, what should every
  other part of your platform stop assuming, that it was previously trusting by default or
  taking on faith?
- BR-02 and section 9.3 need more than "does this token exist": a client may act on their own
  data and never anyone else's, and internal access should be limited to what a role genuinely
  needs. What does your service actually check to guarantee that, and where does the check live?
- BR-03 needs a session that's revocable, not just time-limited. If a credential is compromised
  right now, what would your team actually have to do to shut that session down before it
  expires on its own? If the honest answer is "wait for it to expire," that's worth surfacing as
  a risk, not quietly accepting.
- This week's teaching covers password hashing properly, argon2 and bcrypt-style algorithms
  rather than a fast general-purpose hash. Apply it here, and make the cost or parameter choice
  deliberately, written down, not a default copied from the first tutorial you find.
- A password, and anything that could reconstruct one, should never reach a log. That's not
  really a design decision, it's a line not to cross, worth checking for directly rather than
  assuming your logging is fine.

## Suggested Friday session

- Design the auth flow as a team before anyone writes a controller: what's issued at login, what
  a refresh looks like, what a token actually needs to carry to answer BR-02.
- Work through the zero trust and revocation questions above and agree your answers.
- Plan the move from wherever you left authentication in Sprint 6 to where it needs to be now,
  and what has to change elsewhere in your platform for that to be clean rather than messy.
- Decide and document your password hashing choice and its parameters.
- Refine the backlog against anything this week's work has surfaced about account state or
  access.

## What to present to the class

- A walkthrough of your auth flow and the identity decisions behind it.
- How you moved from wherever authentication stood after Sprint 6 to where it is now, and any
  risk in that move.
- How you're guaranteeing BR-02, that a client can only ever reach their own data.
- An updated backlog.
