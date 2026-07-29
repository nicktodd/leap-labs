# Lab 11 — Deployment Automation: Scripting the Full Pipeline

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. Module 6's
ECR repository and Module 7's cluster and execution role should already be in place.

## Task

### Part 1: Trust without secrets

1. Create an IAM OIDC identity provider trusting `token.actions.githubusercontent.com`.
2. Create an IAM role GitHub Actions can assume via that provider, with a trust policy scoped to
   one specific repository and branch — not a wildcard.
3. Attach a permissions policy to that role scoped to exactly what a deploy needs: pushing to
   your one ECR repository, registering task definitions, updating your one ECS service, and
   `iam:PassRole` on your execution role only.

### Part 2: Write the workflow

4. Write a GitHub Actions workflow (`.github/workflows/deploy.yml`) that builds an image on every
   push to `main`, pushes it to ECR tagged with the commit SHA, and deploys it to your ECS
   service using `role-to-assume` (not stored access keys) to authenticate.

### Part 3: Prove it before you trust it

5. Before relying on the workflow actually running correctly, execute each of its steps directly
   from your own machine — login, build, push, register a task definition, run a task — the same
   way this module's demo did. If a step fails, fix the underlying command first; a workflow
   wrapping a broken command is still broken.
6. Specifically check: does your task definition come from the **current live** definition (only
   the image swapped), or from a **local copy** that might be stale? What could a stale local
   copy carry forward that would only fail once deployed?

## Verify

Compare your work against `solutions/11-.../model-answers.md`. Your OIDC role's trust policy
should be scoped to your specific repository, its permissions policy should name specific
resources rather than `"*"` wherever practical, and each pipeline step should succeed when run
directly.

## Cleanup

The OIDC provider and IAM role cost nothing to keep. Leave them in place.

## A Question Worth Sitting With

This lab's workflow authenticates using `role-to-assume` and a short-lived OIDC token instead of
a stored AWS access key in a GitHub secret. If the AWS access key approach were used instead,
what would have to happen for that credential to stop working after, say, a member of the team
leaves? Compare that to how the OIDC approach handles the same situation.
