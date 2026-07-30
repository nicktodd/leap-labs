# Sprint 11 Instructor Guide — Cloud & Deployment + Final Showcase

This is the sprint-wide companion to the per-module `demos/<module>/demo-guide.md` files, which
remain the primary teaching script for each session — read this first for the week's shape,
setup, and the things worth knowing across more than one module; read each module's own
demo-guide for the actual talking points and commands.

## Before Monday

- **AWS access**: confirm with your own organisation how this cohort will get console/CLI access
  before Module 2 — the labs deliberately say "access the AWS console as per your instructor's
  instructions" rather than assuming a specific method, since that decision sits outside this
  repo. Everything in this guide and in `demos/` was authored and verified against a `training`
  CLI profile in `us-east-1`; your cohort's account will differ in account ID, and very likely in
  any pre-existing resources (a default VPC, Control-Tower-provisioned resources) — the labs are
  written to be account-agnostic for exactly this reason.
- **Region and naming**: everything in this sprint's real, verified examples uses `us-east-1` and
  a `leap-` prefix on named resources. If your cohort's account uses a different region or has a
  naming convention already in place, the concepts transfer directly but the exact resource names
  in demo-guides won't match what you'll actually see — say so explicitly rather than let
  candidates think something's wrong.
- **A Fidelity platform engineering SME session** happens before Module 1, per the mission brief —
  this sprint teaches generic AWS principles; that session teaches how Fidelity actually does it.
  Confirm that session is scheduled before committing to the Module 1 start time below.
- **Prior-sprint dependencies**: Sprint 6's mission-service Dockerfile, Sprint 8's auth-service,
  and Sprint 9's `mission-ui` build are used unchanged throughout — confirm candidates still have
  working local checkouts of all three before Module 6.

## The Week at a Glance

| Day | Modules | Runtime | Theme |
|---|---|---|---|
| 1 | 1, 2, 3 | 45 + 45 + 50 = 140 min | Foundations: the deployment plan, IAM/CLI, networking |
| 2 | 4, 5, 6 | 50 + 50 + 45 = 145 min | Frontend on S3/CloudFront, containerising the backend |
| 3 | 7, 8 | 50 + 60 = 110 min | ECS: task definitions, then a real deployed service |
| 4 | 9, 10 | 55 + 55 = 110 min | Data/secrets, observability/cost |
| 5 | 11, 12 | 55 + 50 = 105 min | Pipeline automation, capstone application, wrap-up |
| — | Friday | — | Final Showcase (breaks from the weekly cadence entirely) |

Each module's own demo-guide breaks its runtime into timed `Part 0…N` sections — the table above
is for planning the week, not the session.

## Cost and Teardown Discipline

Every module that provisions a billed resource (RDS, NAT Gateway, ALB, interface endpoints) tears
it down again in its own demo-guide and lab, immediately after verification — this is
deliberate, not an oversight, and worth stating explicitly to candidates: a training account
accumulates real cost if resources are left running past their module, and the discipline of
tearing down what you verified is itself part of what this sprint teaches. What's left running
persistently across the whole sprint is free or near-free: the VPC and subnets (Module 3), the
ECS cluster and execution role (Module 7), the ECR repositories (Module 6), the S3 gateway
endpoint and Jenkins instance profile (Modules 8 and 11), and the CloudWatch dashboard/alarm/
budget (Module 10). Module 12 opens with a live audit confirming exactly this — worth running
yourself before the week starts, so you know what a clean baseline account actually looks like.

If you're running this sprint for a second cohort against the same account, re-run Module 12's
audit commands first — resources from a previous cohort's incomplete cleanup are the most likely
source of unexpected cost or naming collisions.

## Threads That Run Across Multiple Modules

A handful of ideas get introduced once and then referenced again later — worth knowing where each
one recurs, so a candidate's question in Module 9 about something from Module 3 doesn't catch you
off guard:

- **The route-table test for public/private** (Module 3) is the same reasoning later applied to
  "is this task definition correct" (Module 7), "is this the actual bill" (Module 10) — check
  the real thing directly, not a name, tag, or assumption.
- **Least-privilege IAM** (Module 2's restricted S3 user) recurs in every execution role and
  instance profile from Module 7 onward — each one scoped to exactly what it needs, never a
  wildcard where a specific resource ARN will do.
- **NAT Gateway vs. PrivateLink** (Module 3 introduces both conceptually; Module 8 builds
  PrivateLink for real, with the explicit condition — no external API calls — under which it's
  sufficient; Module 10's real Cost Explorer data ties actual spend back to that choice).
- **Task definitions must come from the current live definition, not a stale copy** (Module 11) —
  this is a real, general pipeline-authoring risk, not specific to Jenkins or to this mission.
- **Sprint 9's Playwright suite** (`login.spec.ts`) reappears in Module 11 as an Acceptance Tests
  pipeline stage — candidates who struggled with Sprint 9 Module 16 may need a quick pointer back
  to that spec file's structure.

## Module-by-Module Notes

Durations and full talking points live in each module's own `demos/<module>/demo-guide.md`. This
section is only what's easy to miss on a first read.

**Module 1–2 — Foundations, IAM/CLI.** No AWS resources persist from these modules. Module 2's
"what does `s3:ListBucket` actually cover" gotcha is a genuine, common confusion — worth letting
candidates predict the answer before revealing it.

**Module 3 — Networking.** The four-layer build-up (VPC → subnets → IGW → route tables) is
deliberately live-built, not shown finished — resist the urge to skip ahead to the completed
diagram. The NAT Gateway and PrivateLink slides are conceptual only in this module; don't
provision either here, Module 8 does that for real.

**Module 4–5 — S3/CloudFront.** Module 4's bucket is public; Module 5's is fully private, fronted
by CloudFront with Origin Access Control. Both buckets are billed while they exist (minimal, but
real) — both are deleted at the end of their own module.

**Module 6 — ECR.** The buildx attestation-manifest finding (extra untagged image entries after a
plain `docker build`) is genuinely easy to mistake for a mistake — it isn't one; the lifecycle
policy in this module's demo cleans it up as a matter of course, not as a fix for an error.

**Module 7 — ECS task definitions.** Runs entirely with `run-task` in a public subnet — no
service, no load balancer yet. If a candidate's image was built on Apple Silicon, expect the
CPU-architecture mismatch this module's demo walks through; it's common, not rare.

**Module 8 — Deploying the backend.** Uses PrivateLink, not a NAT Gateway — if you're recalling
an earlier run of this sprint that used NAT Gateway, that was superseded; PrivateLink is correct
for this workload's actual needs (no external API calls) and is the version verified live. The
ALB health check accepting both `200` and `401` is deliberate, not a workaround to gloss over —
`/actuator/health` is genuinely guarded by Spring Security.

**Module 9 — RDS/Secrets Manager.** `--manage-master-user-password` is the star of this module —
make sure candidates see the real `SecretArn` AWS generates, not just told it happens. The
Parameter Store comparison (cost vs. rotation) is worth a real show of hands: who'd choose which,
and why.

**Module 10 — Observability/cost.** Deliberately provisions nothing new — it queries data the
sprint has already generated. If you're running this sprint back-to-back with limited real
historical data (e.g. a compressed schedule), the CloudWatch Logs Insights query and Cost
Explorer numbers will be thinner than this repo's own worked examples; the commands and reasoning
still hold, just with less to show.

**Module 11 — Pipeline automation (Jenkins).** No live Jenkins instance is required for this
module — every pipeline step is verified directly via CLI, and the Jenkinsfile is provided as
`.example` reference material. If your cohort does have a shared Jenkins instance available, this
module is a natural place to actually wire the instance-profile pattern up for real.

**Module 12 — Capstone application + wrap-up.** This is the pivot from "the shared baseline
mission" to "your own project" — expect this module's pacing to vary more than any other, since
candidates' Sprint 10 extensions differ widely in whether they need a new ECR repo/task
definition or fit inside the existing service. Budget extra floating time here rather than a
fixed 50 minutes if the cohort's capstones are architecturally diverse.

## Friday: The Final Showcase

Per the mission brief, Friday breaks from the weekly cadence entirely — no guest speaker, no
Weekly Knowledge Check. Panel Q&A should specifically probe the two threads Module 12 asked
candidates to prepare: a **named, specific** example of a Copilot suggestion that needed
correcting (not "I used Copilot"), and a **named, specific** real risk their pipeline automation
caught or prevented (not "I set up a pipeline"). Candidates who can only answer in general terms
on either thread haven't yet internalised the discipline this sprint has been building since
Module 1 — worth flagging in feedback even if the deployment itself works.

The day closes with a Group Retro covering the full 11-sprint programme, not just this week — see
the top-level `README.md`'s note on this for logistics.
