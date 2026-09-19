# Lab 11 — Deployment Automation: Scripting the Full Pipeline

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. Module 6's
ECR repository and Module 7's cluster and execution role should already be in place.

## Task

### Part 1: Trust without stored credentials

1. Create an IAM role trusted by `ec2.amazonaws.com`.
2. Wrap it in an instance profile — the thing that actually gets attached to a Jenkins agent EC2
   instance.
3. Attach a permissions policy to that role scoped to exactly what a deploy needs: pushing to
   your one ECR repository, registering task definitions, updating your one ECS service, and
   `iam:PassRole` on your execution role only.

### Part 2: Write the pipeline

4. Write a Jenkins declarative pipeline (`Jenkinsfile`) with stages that build an image, push it
   to ECR tagged with the commit SHA, and deploy it to your ECS service — with no `aws configure`
   step and no AWS credentials stored in Jenkins anywhere.

### Part 3: Prove it before you trust it

5. Before relying on the pipeline actually running correctly, execute each of its shell steps
   directly from your own machine — login, build, push, register a task definition, run a task —
   the same way this module's demo did. If a step fails, fix the underlying command first; a
   pipeline wrapping a broken command is still broken.
6. Specifically check: does your "render task definition" step come from the **current live**
   task definition (only the image swapped), or from a **checked-in or previously-registered
   copy** that might be stale? What could a stale copy carry forward that would only fail once
   deployed?

## Verify

Compare your work against `solutions/11-.../model-answers.md`. Your instance profile's role
should trust `ec2.amazonaws.com` specifically, its permissions policy should name specific
resources rather than `"*"` wherever practical, and each pipeline step should succeed when run
directly.

## Cleanup

The IAM role and instance profile cost nothing to keep. Leave them in place.

## A Question Worth Sitting With

An instance profile vends temporary credentials only to the specific EC2 instance it's attached
to, automatically rotated, with nothing stored anywhere. If Jenkins instead used a long-lived AWS
access key stored as a Jenkins credential, what would have to happen for that credential to stop
working after, say, that Jenkins server is decommissioned or a team member who set it up leaves?
Compare that to how the instance profile handles the same situation.
