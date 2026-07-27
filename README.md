# LEAP Program — Sprint 11 Lab Exercises

This repository contains the hands-on lab exercises accompanying **Sprint 11: Cloud &
Deployment + Final Showcase**, week 11 of the LEAP graduate programme.

## Prerequisites

- An AWS account with console and CLI access — confirm with your instructor how access is
  provided for this cohort before Module 2
- AWS CLI v2, installed and ready to authenticate (`aws --version`)
- Docker, for Module 6 onward (building and pushing the mission's container images)
- A working checkout of Sprint 6/7's mission service (Spring Boot), Sprint 8's
  `sprint8-auth-service` (NestJS), and Sprint 9's `mission-ui` (Angular) — this sprint deploys
  all three, unchanged, to AWS
- Your Sprint 10 capstone project, if you want to apply this sprint's deployment steps to it as
  well as the baseline mission — several labs suggest this as a stretch step, not a requirement
- GitHub Copilot Chat (continuing as a learning aid)

## Coming from Sprint 10

Sprint 10 was a project week — you extended the mission with a feature of your own. Sprint 11
doesn't touch that work directly; it teaches you how to put the mission (and, if you choose,
your own extension) on AWS, reachable by a real URL instead of `localhost`. See
`shared/mission-brief.md`.

Before Module 1, a Fidelity platform engineering SME runs a session on Fidelity's own AWS
environment — its guardrails, approved service catalogue, and security baselines. This sprint
teaches generic AWS principles; that session teaches how Fidelity actually does it.

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`, following the same
pattern as every previous sprint.

- `demos/<module>/` — instructor-led demo assets and guides
- `labs/<module>/` — your starter files and the task README for that module
- `solutions/<module>/` — reference solutions (try the lab first!)

Unlike prior sprints, most of this sprint's "solution" is a set of real AWS resources rather
than source code — model answers describe verified CLI/console output and the exact commands
used, since the underlying infrastructure is torn down after each module's lab.

## Getting started

1. Clone this repository.
2. `cd` into a module's `labs/<module>/` folder and check that module's README for setup.
3. Work through the modules in order, starting with `labs/01-.../README.md`.

## Modules

| # | Module | Lab |
|---|---|---|
| 1 | Cloud Engineering Foundations & the Deployment Plan | _coming soon_ |
| 2 | AWS Account Setup, IAM Basics & CLI Essentials | _coming soon_ |
| 3 | Networking Foundations: VPC, Subnets & Security Groups | _coming soon_ |
| 4 | S3 Fundamentals & Deploying the Frontend | _coming soon_ |
| 5 | CloudFront: CDN Fundamentals & Fronting the Frontend | _coming soon_ |
| 6 | Containerising for the Cloud: From Docker to ECR | _coming soon_ |
| 7 | Introduction to ECS: Clusters, Task Definitions & Services | _coming soon_ |
| 8 | Deploying the Backend to ECS | _coming soon_ |
| 9 | Managed Data & Secrets: RDS & Secrets Manager | _coming soon_ |
| 10 | Observability & Cost Awareness | _coming soon_ |
| 11 | Deployment Automation: Scripting the Full Pipeline | _coming soon_ |
| 12 | Final Capstone Preparations & Sprint 11 Wrap-up | _coming soon_ |

## Friday: Final Showcase

Friday breaks from the usual weekly cadence — there's no guest speaker or Weekly Knowledge
Check. The whole day is the Final Showcase: live demos to Fidelity leaders, instructors, and
peers, covering the trading platform, your chosen Sprint 10 extension, your design decisions,
Copilot usage, and code quality story, followed by panel Q&A. The day closes with a Group Retro
reflecting on the full 11-sprint programme, not just this week.

## Support

Ask your trainer or Scrum team lead during class, or raise a question in the cohort's usual
support channel.
