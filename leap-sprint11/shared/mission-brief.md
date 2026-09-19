# Sprint 11 Mission: Putting the Trading Platform on AWS

Since Sprint 9, the mission has been a fully working application — a real Angular front end
(`mission-ui`), a real Spring Boot mission service, and a real NestJS auth service, all
talking to a real Postgres database — but only reachable on `localhost`. Sprint 10 was a
project week: candidates extended the mission with a feature of their own choosing. Nobody
outside this room has ever been able to actually reach it.

Sprint 11 puts the mission on AWS. By Friday's Final Showcase, `mission-ui` is served from S3
through CloudFront, the mission service and auth service run as containerised tasks on ECS,
and the database is a managed RDS instance — reachable from a real URL, by anyone, not just
from a laptop with the right services running locally.

## What Changes, and What Doesn't

**Doesn't change:**
- The mission service's business logic, persistence layer, and `SecurityConfig` (Sprint 5/6/7)
- The auth service's login/register/refresh contract (Sprint 8)
- `mission-ui`'s components, services, routing, and tests (Sprint 9) — the same Angular build
  artifact that ran on `localhost:4200` is what gets uploaded to S3
- Any Sprint 10 capstone extension a candidate built — the deployment steps this sprint teaches
  apply to it exactly as they apply to the baseline mission

**Changes:**
- `mission-ui`'s build output moves from a dev server on a laptop to an S3 bucket served
  through CloudFront
- The mission service and auth service move from `java -jar` / `node dist/main.js` on a laptop
  to containerised ECS Fargate tasks, built from the same Dockerfiles Sprint 6 and Sprint 8
  already wrote
- Postgres moves from a local Docker container to a managed RDS instance
- Hardcoded local secrets (the JWT signing secret, database credentials) move to Secrets
  Manager, retrieved at runtime rather than read from a local `.env` file or `application.yml`

## Why a Networking Module Comes Before ECS and RDS

Nothing in Sprints 1-10 required understanding a VPC, a subnet, or a security group — every
service ran on `localhost`, where networking is invisible. ECS tasks and RDS instances don't
have that luxury: they need a network to sit in, with a real, deliberate decision about which
subnets are public (reachable from the internet) and which are private (reachable only from
inside the VPC). Module 3 teaches just enough networking for Modules 7-9 to make sense — not a
full networking course.

## Why This Sprint Was Rebuilt Around ECS, Not Just S3/CloudFront

An earlier version of this sprint covered S3 and CloudFront for the Angular frontend in depth,
but gave the containerised backend only "awareness — no hands-on" treatment: a brief mention of
Lambda, ECR, and Secrets Manager, with nothing actually deployed. Since the mission's backend
services are containerised and need somewhere to actually run, ECS is a proper hands-on block
(Modules 7-8) in this version, with ECR (Module 6), RDS, and Secrets Manager (Module 9) taught
as applied deployment steps rather than overview slides.

## A Note on the Firm's Own AWS Environment

This sprint is taught against generic AWS principles, using a training AWS account. The firm
operates its own AWS implementation, with its own guardrails, approved service catalogue, and
security baselines that will differ from what's taught here in real, specific ways. A platform
engineering SME session from the firm happens before Module 1 to brief candidates on the
firm-specific version of everything this sprint covers, ECS included — this sprint's labs
teach the underlying AWS concepts; the SME session teaches how the firm actually does it.

## Non-Goals

No changes to any service's business logic, contract, or test suite. No multi-region,
auto-scaling, or blue/green deployment strategy — this sprint gets one working copy of the
mission running in one region, reachable by a real URL, which is itself a large enough goal for
four days. Cost and teardown discipline matter throughout: every module that provisions AWS
resources tears them down once verified, both to control cost and because a Fargate task or an
RDS instance left running over a weekend is a real, avoidable expense.
