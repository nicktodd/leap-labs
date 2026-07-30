# Lab 12 — Final Capstone Preparations & Sprint 11 Wrap-up

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. Every
earlier module's resources (cluster, ECR repos, execution role, dashboard, alarm, budget) should
still be in place; billed resources (RDS, ECS services, NAT/ALB) should already be torn down.

## Task

### Part 1: Audit your own account

1. Run the same audit commands this module's demo used (`ecs list-services`,
   `rds describe-db-instances`, `describe-nat-gateways`, `describe-load-balancers`). Confirm
   nothing billed is running that shouldn't be. If something is, tear it down now, before
   moving on.
2. Check your CloudWatch alarm's current state and history. Has it moved from
   `INSUFFICIENT_DATA` to something else since Module 10? What changed to cause that?

### Part 2: Apply the pipeline to your capstone

3. Identify whether your Sprint 10 capstone extension lives in the existing mission-service
   codebase, or as its own separate service.
4. If it's a separate service: create its own ECR repository and task definition, following
   Module 6 and Module 7's patterns exactly.
5. Adapt Module 11's Jenkinsfile (or your own equivalent) to build, push, and deploy your
   capstone extension specifically — updating the environment variables at the top, not
   rewriting the pipeline's shape.
6. Extend the Acceptance Tests stage with at least one Playwright check that exercises your
   capstone feature specifically, not just Sprint 9's original login flow.

### Part 3: Prepare your showcase narrative

7. Write down one specific example of a Copilot suggestion during your own work (this sprint or
   Sprint 10) that needed correcting — what was wrong with it, and how did you catch it before
   trusting it?
8. Write down one specific example of something your pipeline automation either prevented or
   caught that manual deployment steps might have missed.

## Verify

Compare your resource audit against `solutions/12-.../model-answers.md`'s expected clean state.
For Parts 2 and 3, there's no single correct answer — what matters is that your pipeline actually
runs against your own capstone code, and that your showcase notes are specific and concrete
rather than general statements.

## Cleanup

Nothing new and billed was created this module. Leave everything as it is for Friday.

## A Question Worth Sitting With

The mission brief says this sprint's deployment steps "apply to a Sprint 10 capstone extension
exactly as they apply to the baseline mission." Was that true for your own extension, or did you
find one place where it genuinely wasn't — something about your specific feature that needed a
real decision the baseline mission never had to make?
