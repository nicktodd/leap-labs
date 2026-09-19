# Lab 1 — Cloud Engineering Foundations & the Deployment Plan

## Setup

No laptop setup needed. Work in pairs, on paper or a whiteboard. Have Sprint 6-9's
architecture in front of you if you want to check specifics (`mission-service`'s
`application.yml`, `sprint8-auth-service`'s `main.ts`, `mission-ui`'s `environment.ts`).

## Task

The mission's current architecture has five pieces:

- `mission-ui` — Angular, built with `ng build`, currently served by the Angular dev server
- `mission-service` — Spring Boot, currently run with `java -jar`
- `sprint8-auth-service` — NestJS, currently run with `node dist/main.js`
- Postgres — currently a Docker container (`sprint6-postgres`)
- Kafka — currently a Docker container, publishing trade events from `mission-service`
  (Sprint 7)

### Part 1: Map each piece

For each of the five pieces above, decide and write down:

1. Does it move to AWS this sprint, or stay local? (One of the five has a deliberately
   different answer from the other four — figure out which, and why, before checking the
   model answer.)
2. If it moves, which AWS service hosts it? Use only the six services from today's demo (S3,
   CloudFront, ECR, ECS, RDS, Secrets Manager) — if you think a piece needs a seventh service,
   write down which one and why, but know that's outside this sprint's scope.
3. What has to be true about the network for that AWS service to reach the pieces it needs to
   talk to? (You don't need Module 3's detail yet — just note where you expect a "public" vs
   "private" decision matters.)

### Part 2: Trace one request

Draw the full path of a single "submit an order" request, from the browser to Postgres and
back, through your Part 1 answers. Label every hop with the AWS service (or "local") handling
it, and mark which hops cross the public internet versus staying inside AWS's private network.

### Part 3: Where secrets live

The mission currently has two real secrets: the JWT signing secret (currently a hardcoded
fallback string, shared across services) and the database password (currently plaintext in a
local `.env` file / `application.yml`). Where should each one live after this sprint, and why
is "hardcoded in the container image" the wrong answer even though it would technically work?

## Verify

Compare your three answers against `solutions/01-.../model-answers.md` — you're not expected
to match every word, but you should be able to defend any place your answer differs.

## A Question Worth Sitting With

If you were deploying your own Sprint 10 capstone extension instead of the baseline mission,
would your answers to Part 1 change? Most extensions add a new component (a notification
service, a reporting job, a websocket feed) — where would it fit in this same six-service
list, and does it change anything about the network diagram from Part 2?
