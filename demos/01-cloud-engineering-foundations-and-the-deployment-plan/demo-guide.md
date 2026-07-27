# Module 1 Demo Guide — Cloud Engineering Foundations & the Deployment Plan

**Duration:** 45 minutes
**Prerequisite:** None — this module is deliberately code-free. Bring the mission's
architecture from Sprints 6-9 to the whiteboard, not a laptop.

## Part 0: What Actually Changes Moving to the Cloud (10 min)

Every service the mission depends on already runs, right now, on someone's laptop:
`mission-service` on `:8090`, `sprint8-auth-service` on `:3000`, Postgres in a Docker
container on `:5433`, `mission-ui` on the Angular dev server at `:4200`. All of it works.
None of it is reachable by anyone who isn't sitting at that laptop.

"Moving to the cloud" doesn't mean rewriting any of that. It means three things, and only
three things:

1. **Somewhere that isn't a laptop runs the code** — a laptop being asleep, closed, or
   disconnected from a coffee-shop network is not an acceptable reason for a real
   application to go down.
2. **A real, stable address reaches it** — not `localhost`, not an IP that changes every time
   someone reconnects to Wi-Fi.
3. **Someone other than the one person who built it can operate it** — restart it, see its
   logs, know when it's unhealthy, without SSH-ing into a specific laptop.

Nothing about *what the mission service does* changes. `OrderController`, the JWT validation,
the MyBatis mappers — all of Sprint 6's actual code ships unmodified. This sprint changes
*where it runs*, not *what it is*.

## Part 1: The Small Set of Services That Handle Most of the Work (10 min)

AWS has several hundred services. The mission needs six, and this sprint teaches exactly
those six, nothing more:

| Service | What it replaces from "the laptop" |
|---|---|
| **S3** | The folder `ng build` writes static files into |
| **CloudFront** | Nothing — this is new; there was no CDN in front of `localhost:4200` |
| **ECR** | The local Docker image cache (`docker images`) |
| **ECS (Fargate)** | `java -jar mission-service.jar` / `node dist/main.js`, running forever |
| **RDS** | The `sprint6-postgres` Docker container |
| **Secrets Manager** | The hardcoded `JWT_SECRET` fallback string and `.env` files |

Worth naming directly: this list is deliberately short. A real platform team's AWS footprint
is much larger (Lambda, SQS, DynamoDB, API Gateway, dozens more) — this sprint teaches the
six services this specific mission actually needs, not a tour of the AWS console.

## Part 2: Tracing One Request Through the Deployed Architecture (15 min)

Draw this on the whiteboard, live, narrating each hop:

```
Browser
  |
  v
CloudFront (edge, cached, TLS)
  |
  v
S3 (mission-ui's static build - HTML/CSS/JS only, nothing runs here)
  |
  | (browser then calls the API directly, not through CloudFront/S3)
  v
Application Load Balancer
  |
  v
ECS Fargate task (mission-service container, in a private subnet)
  |
  v
RDS (Postgres, in a private subnet, unreachable from the internet)
```

Two things worth pausing on, both real gotchas the lab will ask candidates to reason about
directly:

- **S3 never executes anything.** `mission-ui`'s Angular build is HTML/CSS/JS that runs in
  the *visitor's* browser — S3 just serves the files, the same as `ng build`'s output folder
  did locally. The mission service, by contrast, is a JVM process that has to actually run
  somewhere continuously — that's what ECS is for. Confusing "static files that run in the
  browser" with "a server process that has to keep running" is the single most common
  mistake candidates make when first sketching this diagram.
- **RDS sits in a private subnet, unreachable from the browser or the internet at all** — only
  the mission service's ECS task, inside the same VPC, can reach it. The browser never talks
  to Postgres directly, exactly as it doesn't today (it goes through the mission service).

## Part 3: What Stays Local — and Why That's a Real Decision, Not a Gap (10 min)

Kafka (Sprint 7) is the one piece of the mission's architecture that deliberately does **not**
move to AWS this sprint. AWS has a managed Kafka service (MSK), but it's genuinely expensive
to run correctly (multiple broker nodes, minimum cluster sizing) and non-trivial to configure
well in four days alongside ECS, RDS, and CloudFront. The deployment plan's honest answer is:
Kafka stays on Docker Compose, locally, as a deliberate scope decision — not because nobody
thought about it.

This is the point of the lab: given the mission's full architecture, decide *and justify*
what moves and what doesn't, rather than assuming everything automatically goes to the cloud
because "that's what this sprint is about."

## Key Message

Every AWS service this sprint teaches exists to do one job the mission's architecture already
needs done — nothing is being learned for its own sake. Before writing a single `aws` CLI
command, know what's moving, where, and why; the rest of the sprint is executing this plan.

## Transition to the Lab

In pairs, candidates map every piece of the mission's real architecture — `mission-ui`,
`mission-service`, `sprint8-auth-service`, Postgres, Kafka — to where it lives in AWS (or
stays local), and justify each decision the same way today's demo justified Kafka staying
local.
