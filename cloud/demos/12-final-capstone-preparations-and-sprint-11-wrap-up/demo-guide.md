# Module 12 Demo Guide - Final Capstone Preparations & Wrap-up

**Duration:** 50 minutes
**Prerequisite:** Every earlier module this week, plus each candidate's own capstone extension.

## Part 0: What This Module Is (5 min)

Modules 1-11 deployed the *baseline* mission - the shared trading platform every candidate
started their capstone project with. The mission brief has said from the start that this week's deployment
steps apply to your capstone extension exactly as they apply to the baseline: same
Dockerfiles, same ECR repos, same ECS patterns, same pipeline shape. Today is about actually doing
that - taking Module 11's pipeline pattern and pointing it at each candidate's own project - and
preparing for Friday's Final Showcase, which the mission brief has flagged from day one as
covering three things: the trading platform, the capstone extension, and **how Copilot was used
and code quality was maintained** alongside the deployment automation story.

## Part 1: A Resource Audit Before Anything Else (10 min)

Before building anything new, check what's actually still running - the same discipline Module 10
taught, applied to the whole week at once, not just one module's resources:

```bash
aws ecs list-services --cluster leap-mission-cluster --query 'serviceArns'
aws rds describe-db-instances --query 'DBInstances[].DBInstanceIdentifier'
aws ec2 describe-nat-gateways --filter Name=state,Values=available,pending --query 'NatGateways[].NatGatewayId'
aws elbv2 describe-load-balancers --query 'LoadBalancers[].LoadBalancerName'
```

Output: no ECS services, no RDS instances, no NAT Gateways, no load balancers - every billed
resource from every earlier module was genuinely torn down after its verification, exactly as
each module's cleanup section required. What remains is free: the cluster itself, the execution
role, both ECR repositories (10 images across them), the S3 gateway endpoint, the CloudWatch
alarm and dashboard, and the budget. The alarm's own history is worth noting: `INSUFFICIENT_DATA`
when Module 10 first created it, `OK` now - Module 11's task runs since then gave it real data
points to evaluate against the threshold.

## Part 2: Applying the Pipeline to a Capstone Project (15 min)

Module 11's Jenkinsfile pattern - instance profile, Build and Push, Render and Deploy, Acceptance
Tests - is written against the baseline mission-service, but nothing about it is baseline-specific
beyond the environment variables at the top. Applying it to a capstone extension means:

- If the extension lives in the *same* Spring Boot service (a new endpoint, a new feature in the
  existing codebase), the pipeline needs no changes at all - it already builds and deploys
  whatever is in that repository.
- If the extension is a *new* service (its own repository, its own Dockerfile), it needs its own
  ECR repository (Module 6's pattern), its own task definition (Module 7's pattern), and its own
  copy of the pipeline with the environment variables updated to match.
- Either way, the Acceptance Tests stage should grow to cover the capstone feature specifically,
  not just the Angular week's original login flow - a new Playwright spec, or an extension of the existing
  one, exercising whatever the capstone actually added.

## Part 3: Preparing the Showcase Narrative (15 min)

Friday's panel isn't only judging whether the deployment works - it's asking how it was built.
Two threads the mission brief calls out specifically, worth preparing concrete, specific answers
for rather than general statements:

**Copilot usage and code quality.** Not "I used Copilot to write code faster" - which stage of
which module did Copilot's suggestion need correcting, and how was that caught? This week's own
working pattern is the example to point to: several modules this week hit a real AWS error,
diagnosed it from the actual error message rather than guessing, and fixed the root cause - the
same discipline candidates should be able to describe for their own capstone work with Copilot
specifically (a suggestion that looked plausible but was wrong, and how it was verified before
being trusted).

**DevOps automation.** Not "I set up a pipeline" - which specific real failure did automating the
deployment either prevent or surface? Module 11's own stale-task-definition risk (a script that
blindly clones an old definition can carry forward something that's since been deleted) is a
concrete example of exactly this kind of story: a specific, real risk, and a specific fix.

## Key Message

The whole week has been building toward this: not a new deployment target, but the same set of
tools and discipline (build/push/deploy/verify, least-privilege IAM, real verification over
assumption) applied to a project each candidate actually built themselves. The showcase rewards
specific, concrete stories over general claims - "here's the exact commit where Copilot's
suggestion was wrong, and here's how the pipeline's acceptance test stage would have caught it if
I hadn't" is a stronger answer than "I used Copilot throughout."

## Transition to the Lab

Candidates run their own resource audit, adapt Module 11's pipeline to their own capstone
extension, and draft their showcase talking points for both the Copilot/code-quality story and
the DevOps automation story.
