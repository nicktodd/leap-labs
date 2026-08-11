# Module 13 — Model Answers & Notes

## Part 1 — The Completed Script

See `integration-test.sh` in this folder for the full working version. The key patterns:

**The `set -e` retry-loop gotcha** — a bare `curl ... && break` inside a `for` loop, under
`set -e`, kills the entire script the first time `curl` fails (which it will, repeatedly, while a
container is still starting). This is exactly the bug that surfaced while building the demo for
this module. Wrapping it as `if curl ...; then break; fi` avoids the trap, because an `if`
condition's exit status is never treated as the script's own failure.

**Token extraction without extra tooling**:
```bash
TOKEN=$(echo "$LOGIN_RESPONSE" | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')
```
A minimal `sed` pattern rather than reaching for `jq` (which may not be installed everywhere) or a
scripting language — appropriate for a small, single-field extraction in a shell script.

## Part 2 — Sample Wrap-up Answers

**1. A REST design decision, traced.** A reasonable answer: Module 4's `POST /orders` design
(learner's own resource naming) generally survived into Module 11's
`POST /accounts/{accountId}/orders` — but the exact shape was forced to change once persistence
(Module 7) entered the picture: an order needs to be scoped to an *account*, not just submitted
in isolation, because `AccountMapper` needs to know which holdings row to read and write. That
requirement wasn't visible from Module 4's REST principles alone — it only became obvious once
real data entered the picture in Module 7.

**2. Was Sprint 5's logic really unchanged?** Yes — literally, byte-for-byte, other than the
package declaration (`com.neueda.leap.sprint5` → `com.neueda.leap.sprint6.domain`) and one
added comment. `OrderValidator.java`, `HoldingUpdater.java`, and the `Instrument` hierarchy in
Module 11's `domain/` package are the exact classes from Sprint 5, Module 13. The mission brief's
claim held up under direct inspection, not just as a stated intention.

**3. The portfolio-valuation simplification, justified.** Model 11 used
`currentQuantity * dto.price()` as a stand-in for a client's true portfolio value, because
building real market-price lookups would need a live pricing feed this sprint never scoped. The
honest justification: it's *documented*, in both code comments and the demo guide, as a known
simplification with a clear reason — not silently passed off as correct. A shortcut becomes a
problem when it's hidden; naming it explicitly (as Module 11 did) is what separates a reasonable
training-sprint trade-off from technical debt nobody flagged.

## What This Module Actually Proved

Three services (Postgres, the Node auth stub, the Spring Boot mission service), built across
three different modules by three different teaching threads (data, security, application logic),
running as three independent containers, communicating only through the exact contracts each
prior module established — a shared secret, a Docker network, a JDBC URL. Nothing about this
integration required changing code written in an earlier module. That's the actual test this
module runs: not just "does the code work," but "did the modules' seams hold."
