# Assessment

**Note on this file - the touchpoint schedule needs a real decision, not just relabeling:**
the four touchpoints below are pinned to "After Sprint N" content milestones from the old
curriculum order. Mapped to what each touchpoint actually needs *ready*, not just to the old
number, the picture is:

- **TP1** needs the data model done → that's still the Data week (week 2), unchanged.
- **TP2** needs the domain engine, REST API, and event backbone done → that's still after the
  Kafka week (week 8), unchanged.
- **TP3** needs *both* authentication and the trading UI working together → this is the one
  that breaks. Old order had Node (auth, then Sprint 8) finish before Angular (UI, then Sprint
  9), so "after Sprint 9" had both ready. New order has Angular at week 5 and Node at week 6 -
  the UI now finishes *before* auth does. "After Angular week" alone would mean assessing UI +
  auth integration before auth exists. The natural new trigger is **after Node week (week 6)**,
  not after Angular week - but that's a scheduling decision for whoever owns this rubric, not
  something I've changed below.
- **TP4** needs everything done, at the end → still the Cloud week (week 10), unchanged.

The table, area breakdowns, and "Bring to TPn" headers below still say "After Sprint 3/7/9" and
"End of Sprint 11" - I've left the *timing* exactly as it was pending that decision, and only
fixed content references elsewhere in the document (e.g. "the Sprint 4 ETL pipeline" → "the
Python week ETL pipeline") where they don't affect scheduling.

Your team's project work is assessed as a team, at four points across the
programme, for a single running score out of 100. There is no pass mark. The
score is a measure of how far the platform and the way you are building it have
come, and it exists so that the feedback at each review is concrete rather than
an impression.

This document is the whole rubric. Nothing is assessed that is not described
here, and the marks against each item tell you where we think the value is.

## How it works

Assessment happens at four touchpoints, each tied to a point where there is
something coherent to look at rather than work in flight.

| Touchpoint | When | What comes into scope | Marks | Running total |
|---|---|---|---:|---:|
| **TP1** | After Sprint 3 | Backlog and stories, how the team is running itself, the first data model and its access patterns, the customer engagement | 18 | 18 |
| **TP2** | After Sprint 7 | The reporting and ETL work from Sprint 4, the domain engine, the REST API, the event backbone, atomic execution and duplicate handling | 40 | 58 |
| **TP3** | After Sprint 9 | Authentication and security, the trading UI, the order lifecycle working end to end through the real UI against real services | 26 | 84 |
| **TP4** | End of Sprint 11 | Deployment, the finished quality and test picture, the gap-closing work and any BR-18 capability, the showcase | 16 | 100 |

### The score is additive, and the touchpoints are not deadlines

Each touchpoint releases its own marks. It does not re-score everything from the
start: TP1 is marked out of 18, TP2 adds up to 40 more, and so on, up to 100.

Marks you do not earn at their touchpoint are not lost. If an area is still thin
at TP2 but solid by TP3, those marks are picked up at TP3, at full value. The
touchpoint is when the work is first looked for, and when feedback on it is most
useful to you, not a gate that closes. Marks already earned are not taken back
either; the continuity checks below are their own small line items, not a
re-marking of what came before.

We will still encourage you to meet each touchpoint on time. Scoping work to
land by a fixed review date is a large part of what this project is teaching,
and a team that consistently turns up ready is building a real delivery skill.
Treat the dates as an external constraint the way you would on a real
engagement. But arriving late costs nothing in the score itself.

Every touchpoint after the first also carries a small **continuity check** on
the areas already assessed. By TP2 the schema has more weeks
built on it, and the question is whether the design still hangs together as a
whole, whether the changes made along the way were deliberate and recorded, and
whether anything regressed in correctness. Adjusting the earlier design is
expected. Leaving the design record behind, or breaking something that used to
work, is not. Those marks are noted in each area below.

### You are assessed against your own design, and it is expected to change

There is no central set of contracts, no prescribed architecture, and no
reference schema. What you are held to is the design record you maintain: your
own architecture, API contracts, event definitions, schema, decision log and
risk list, read against the business requirements specification.

That design is expected to change, and changing it is not a cost here. The
candidate architecture pitched at kickoff is made with the least knowledge the
team will ever have of the problem, so large parts of it turning out wrong is
the normal outcome, not a failure. The same is true of the first schema, the
first API shape and the first backlog.

What is assessed is not whether the design held still, but whether it evolved
well: each significant change was a decision the team made on purpose, recorded
with its reason, and reconciled with the rest of the design and the
documentation. A team that spotted a modelling mistake early on, changed it
deliberately later and can explain why scores better here than a team
whose schema never changed because it was never tested. The faults are
unrecorded drift, where the running system and the design record have quietly
diverged and nobody chose it, and a correctness regression that later work
introduced and no one caught.

### The contribution record

The score is a team score. It is not split between members.

Alongside it, keep a `contributions.md` in your repository with one short block
per week: for each member, what they led, what they paired on, and what they
reviewed, plus a line on anything that slipped and where it went. At each
touchpoint the instructor checks it against your commit history and your board.

Its purpose is to make sure the work rotated, which the reviews test directly by
asking any member to walk a part of the platform they did not build. If a
member cannot speak to any of the work, that is a conversation with your
instructor, not a deduction from the team's score.

### The customer's input

The instructor who acted as your customer sends your assessing instructor a
short note after each interview: whether you prepared, whether you led the
meeting, whether you confirmed what you heard, and whether you followed up on
the answers that were left vague. That note is evidence that feeds the Delivery
marks. It is not a separate score.

### Score bands

The number is reported with a band, so it means something without a pass line.

| Band | Range | Reads as |
|---|---|---|
| Developing | 0–39 | The pieces exist in part; the platform does not yet hold together, or the team is not yet running as one |
| Functional | 40–59 | The core works and is being built deliberately; known gaps in correctness, rigour or process |
| Solid | 60–74 | The platform does what the requirements ask, the design decisions are defensible, the design has been adjusted deliberately as the team learned more, and the team can explain its own work |
| Strong | 75–89 | Correct where it is hard to be correct, tested where it matters, honest about its own limits, and evolving on purpose rather than by accident |
| Exceptional | 90–100 | The platform and the process would stand up outside the programme, with the difficult properties designed in rather than hoped for |

---

# The assessed areas

Ten areas, 100 marks. Each table shows the marks available at each touchpoint.
An `R` in the notes means the marks at that touchpoint are a regression check on
work first assessed earlier.

## 1. Delivery and agile process - 16 marks

How the team runs itself as a delivery team, assessed a little at every
touchpoint rather than in one block.

| What is assessed | TP1 | TP2 | TP3 | TP4 |
|---|---:|---:|---:|---:|
| Backlog traceable to the spec and to the customer conversation, with stories that carry acceptance criteria rather than restated requirement titles | 3 | 1 | 1 | 1 |
| Decision log and risk list are current and record real decisions and real risks, not a template filled in once | 2 | 1 | 1 | 1 |
| The weekly class check-in is honest: it surfaces problems, shows the backlog and risks moving, and a member who did not present can answer for the team | 1 | 1 | 1 | 1 |
| The contribution record is maintained per sprint and matches the history and the board | 1 | – | – | – |
| **Subtotal** | **7** | **3** | **3** | **3** |

## 2. Data, storage and analytics - 13 marks

| What is assessed | TP1 | TP2 | TP3 | TP4 |
|---|---:|---:|---:|---:|
| The data model covers the domain the platform needs (accounts, instruments, orders, positions, cash, the permanent record), is normalised, and any deliberate denormalisation is recorded with its reason | 3 | – | – | – |
| Access patterns are worked out capability by capability (order processing, positions and cash, the audit trail, reporting), and each storage decision is tied to the requirement that drove it | 3 | – | – | – |
| Integrity is enforced by the database rather than hoped for in code: keys, constraints, and a way to reject a duplicated order | 2 | – | – | – |
| The historical and reporting design for BR-16 is described: how it is populated, how it is queried, how it behaves as it grows | 1 | – | – | – |
| The data model still hangs together after the domain, the API and the executor have been built on it; changes since TP1 were deliberate and are recorded, and the design record matches what is running (`R`) | – | 2 | – | – |
| The ETL pipeline is separated into extract, transform and load, is repeatable, and handles a malformed input rather than wrapping the run in a bare `try` | – | 1 | – | – |
| Three business insights are each stated as a claim a non-technical reader can act on, and the reporting path does not compete with live trading | – | 1 | – | – |
| **Subtotal** | **9** | **4** | **–** | **–** |

## 3. Domain and business rules - 13 marks

| What is assessed | TP1 | TP2 | TP3 | TP4 |
|---|---:|---:|---:|---:|
| Entities, enumerations and the order lifecycle match the team's own model, and the terminal states are chosen on purpose rather than falling out of the first code written | – | 3 | – | – |
| The BR-05 checks and the BR-06 "recorded as a commitment before execution" rule are implemented as an explicit, ordered sequence, in the domain and not in a caller | – | 3 | – | – |
| The domain has no database, HTTP or framework dependency, and can answer "is this order allowed?" in isolation | – | 2 | – | – |
| Money is represented with a type that survives many small operations, and the choice is defended | – | 1 | – | – |
| Tests were written before the implementation, evidenced in the commit history, and they assert behaviour rather than only running green | – | 2 | – | – |
| The domain still serves its callers cleanly now that the executor uses it from the execution side; any changes made to accommodate that were deliberate and recorded (`R`) | – | – | 1 | – |
| The domain is coherent across the finished platform, its evolution since TP2 is recorded, and every member can walk it as it stands now (`R`) | – | – | – | 1 |
| **Subtotal** | **–** | **11** | **1** | **1** |

## 4. API and services - 13 marks

| What is assessed | TP1 | TP2 | TP3 | TP4 |
|---|---:|---:|---:|---:|
| A running service exposes the team's own published contract, and the contract is coherent: a consistent response shape and a consistent error shape across every operation | – | 3 | – | – |
| Layering holds: no persistence in a controller, no HTTP or framework type in the domain, and no business rule that belongs in the domain living in a service | – | 2 | – | – |
| Persistence uses parameterised statements throughout | – | 1 | – | – |
| Order placement is atomic per BR-09: the order record, the cash movement and the holding change commit together or not at all, and something concrete enforces that rather than a hope that it is so | – | 3 | – | – |
| Concurrent orders against one account cannot both spend the same cash, demonstrated, with the losing one failing cleanly | – | 1 | – | – |
| The service builds and runs as a container in the team's own environment, reproducibly | – | 1 | – | – |
| The API serves authentication and the UI cleanly; where the contract changed to meet them, the contract and its consumers were updated together (`R`) | – | – | 1 | – |
| The API serves its current contract in the deployed platform, and the contract document matches what is deployed (`R`) | – | – | – | 1 |
| **Subtotal** | **–** | **11** | **1** | **1** |

## 5. Events and asynchronous execution - 8 marks

| What is assessed | TP1 | TP2 | TP3 | TP4 |
|---|---:|---:|---:|---:|
| Accepting an order and executing it are genuinely separate, connected by messages, and the record of intent does not depend on execution succeeding | – | 2 | – | – |
| The consumer is idempotent: replaying the same message does not double-debit an account, demonstrated on demand rather than described | – | 3 | – | – |
| The execution side keeps BR-09 true: order status, cash and position update in one transaction | – | 2 | – | – |
| The market-data source and its request limits are understood, the design stays inside them, and the key never reaches the browser | – | 1 | – | – |
| **Subtotal** | **–** | **8** | **–** | **–** |

## 6. Authentication and security - 8 marks

| What is assessed | TP1 | TP2 | TP3 | TP4 |
|---|---:|---:|---:|---:|
| Registration and secure sign-in work end to end (BR-01), and whatever stood in for authentication earlier has been replaced or revisited deliberately | – | – | 2 | – |
| A client can reach only their own positions, cash and history (BR-02, section 9.3), and the check lives somewhere a caller cannot bypass | – | – | 2 | – |
| The session is time-limited and revocable (BR-03); if it is only time-limited, that gap is recorded as a risk rather than left silent | – | – | 1 | – |
| Passwords are hashed with argon2 or bcrypt at a deliberate cost, never logged, and no secret is in the repository | – | – | 2 | – |
| Adopting the auth service elsewhere in the platform is a configuration change, not a code change | – | – | 1 | – |
| **Subtotal** | **–** | **–** | **8** | **–** |

## 7. Trading UI and the end-to-end experience - 9 marks

| What is assessed | TP1 | TP2 | TP3 | TP4 |
|---|---:|---:|---:|---:|
| The required views exist (sign-in, holdings and cash, order ticket, blotter, per BR-10, BR-11, BR-13) and work for the Joanna persona without a guide | – | – | 2 | – |
| Sign-in runs against the real auth service, route guards block unauthenticated access, and the token is attached to the platform's own services and to nothing else | – | – | 2 | – |
| An order that is accepted but not yet filled reads as still working, not as broken (section 9.2) | – | – | 2 | – |
| Every error the back end can return reaches the screen as something a non-technical client can act on | – | – | 1 | – |
| No API key or secret is present in the built bundle | – | – | 1 | – |
| The UI works correctly served from the deployed origin; any changes needed for that (origin configuration, base href) are deliberate and recorded (`R`) | – | – | – | 1 |
| **Subtotal** | **–** | **–** | **8** | **1** |

## 8. Quality and testing - 7 marks

| What is assessed | TP1 | TP2 | TP3 | TP4 |
|---|---:|---:|---:|---:|
| Tests exist at the level that matches the risk (unit for rules, integration for wiring), and characterisation tests were put around older code before it was changed | – | 2 | – | – |
| The test coverage reaches the full path: something proves sign-in and placing an order work end to end, each journey standing on its own | – | – | 2 | – |
| A CI pipeline runs the tests and a quality gate on every change | – | – | 1 | – |
| Coverage across the finished platform is meaningful (tests assert outcomes, not just execution), and the gate is green without findings waved through | – | – | – | 2 |
| **Subtotal** | **–** | **2** | **3** | **2** |

## 9. Deployment and operations - 7 marks

| What is assessed | TP1 | TP2 | TP3 | TP4 |
|---|---:|---:|---:|---:|
| The front end is reachable at a real URL over HTTPS | – | – | – | 1 |
| The static origin is private and only the CDN reads it; a public bucket does not satisfy this | – | – | – | 2 |
| Deployment is one repeatable command covering build, upload and invalidation, and running it twice leaves the same result as running it once | – | – | – | 2 |
| The deploying credential is scoped to only what it needs, no long-lived key is in the repository, and teardown responsibilities are confirmed and recorded | – | – | – | 1 |
| The back end accepts requests from the deployed origin by a considered rule, not "allow everything" | – | – | – | 1 |
| **Subtotal** | **–** | **–** | **–** | **7** |

## 10. Defence and showcase - 6 marks

The part no artefact can show: whether the team owns what it built.

| What is assessed | TP1 | TP2 | TP3 | TP4 |
|---|---:|---:|---:|---:|
| Every member can walk the backlog and the data model unaided, and the team can say what the customer did not tell them that they still need | 2 | – | – | – |
| The team can trace one order from the request through the topic to the committed rows and the published event, and defend the order in which the rules are evaluated | – | 1 | – | – |
| Every member can walk any part of the back end and the UI unaided, including parts they did not build, and the team can show the order lifecycle live against real services | – | – | 2 | – |
| The showcase covers the platform end to end, what the kickoff architecture got wrong and how the design responded as the team learned more, two or three decisions the team would defend and what it rejected, the BR-18 capability if built, and where AI helped and where it did not | – | – | – | 1 |
| **Subtotal** | **2** | **1** | **2** | **1** |

---

# The reviews

Each touchpoint is a conversation with your instructor against a running system,
not a submission read in isolation. Satisfying the countable items is necessary
and it is not sufficient: whether a rule has quietly moved into the wrong layer,
whether an index is justified or merely present, whether an error message is one
a trader could act on, whether your team can explain any of it, are read rather
than searched for. A green test suite is the floor.

Where your design has moved since the last touchpoint, come ready to walk that
change: what you learned, what you decided, and where it is recorded. That is a
normal part of the conversation, not something to explain away.

## Bring to TP1 (after Sprint 3)

The backlog walked against the spec, with three items traced back to either a
business requirement or a sentence the customer said. The risk list. The ER
diagram and your migrations applied against an empty database. Your six most
important queries and why each index earns its place. The design note on the
historical and reporting data. A statement that inserts the same order twice
under one idempotency key and is refused by the database. `contributions.md`.
Your answer to "why is the model this way and not the other way" for the
decision you argued about longest.

## Bring to TP2 (after Sprint 7)

The running stack. One order traced from the HTTP request, through your domain,
onto your topic, consumed by your executor, to the committed rows and the
published event. Every operation in your contract answering with the shape your
contract states. Each failure your domain defines produced on demand in your
error shape. A missing and a tampered token on a protected route. Several
concurrent orders against one account, with the cash reconciled against the
order history afterwards. The duplicate message replayed live, moving no money
the second time. Your `git log` showing tests arriving before implementation.
The three business insights and the numbers behind one of them traced to the
rows they came from. Your answer to what happens when two customers spend the
same money at the same moment.

## Bring to TP3 (after Sprint 9)

The auth service, the trade API and the UI all running together. Sign-in from a
clean browser against the real auth service. A guarded route hit without a
session so the redirect can be watched. A recording of the requests one
signed-in page makes, showing where the bearer token went and where it did not.
Each error code rendered as a sentence a trader can act on. An order placed
through the UI and left sitting unfilled, and the screen bringing it up to date.
The built bundle searched in front of the panel for a key and a secret. Your
answer to how a compromised session would actually be shut down before it
expires.

## Bring to TP4 (end of Sprint 11)

The deployed application reached over HTTPS at its real URL. Both of the
origin bucket's own endpoints refusing a direct request. The deploy script run
twice. The JavaScript the deployed page serves, searched for secrets. The
scoped deployment policy. Your decision log for the deployment. The risk list
from every earlier week with an honest status on each open item. And the
showcase itself: the platform end to end, the architecture's journey from the
kickoff pitch, the decisions you would defend, the BR-18 capability if you built
it, and where AI earned its place across the programme and where it did not.
