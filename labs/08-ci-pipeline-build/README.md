# Module 08 Lab — Build a CI Pipeline from Scratch

## Recap: building on Modules 03, 05, and 06

- **Module 03**: PR workflow and branch protection, which can require a CI check to pass
- **Module 05**: pipeline stages conceptually, using a provided log you only had to read
- **Module 06**: a real multi-stage Dockerfile for the team skeleton

Today you write the Jenkinsfile from scratch, and wire up automatic triggering on a PR and on
merge to `main`, the piece that makes Module 03's branch protection meaningful in practice.

## Objectives

By the end of this lab you will have:

- Built a working Jenkins pipeline from scratch
- Understood how to trigger a pipeline on a PR and on a merge to main
- Added a basic automated test step to the pipeline
- Committed the pipeline config to your team repository

## Setup

- The [`starter/`](starter) folder from this lab (the Sprint 1 skeleton, with the multi-stage
  Dockerfile from Module 06 and a placeholder JUnit test, but **no Jenkinsfile**, you're
  writing that yourself)
- Access to the Jenkins instance, with rights to create a new job
- A GitHub repository for this exercise

> **Environment note:** the Jenkins instance for this exercise runs in a private AWS subnet with
> no inbound access from the internet, so GitHub cannot reach it to deliver a webhook. "Automatic
> triggering" in this lab therefore means Jenkins **polling** GitHub on a schedule, not a
> webhook pushing to Jenkins. In a real deployment with a publicly reachable Jenkins (or one
> behind a relay such as a GitHub App with a smee.io/webhook proxy), you'd use webhooks instead,
> since they trigger builds immediately and don't waste API calls on unchanged repositories.

## Task sheet

### Part A — Write the Jenkinsfile

1. Copy `starter/` into a repository and push it.
2. Write a `Jenkinsfile` at the repository root with three stages:
   - **Checkout**: `checkout scm`
   - **Build Image**: `docker build -t team-skeleton:${BUILD_NUMBER} .`
   - **Test**: `mvn -B test`, publishing results with the `junit` step (same pattern as Sprint 1
     Module 10)
3. Commit and push the `Jenkinsfile` using the full PR workflow from Module 03: branch, commit,
   push, open a PR, get it reviewed, merge.

### Part B — Configure automatic triggering

4. In Jenkins, create a **Multibranch Pipeline** job pointing at your repository (not a plain
   Pipeline job, that only builds one branch).
5. Confirm Jenkins discovers `main` and creates a sub-job for it.
6. Since GitHub can't reach this Jenkins instance to deliver a webhook (see the environment note
   above), set up polling instead: open the job, **Configure → Scan Repository Triggers**, tick
   **Periodically if not otherwise run**, and set the interval to **1 minute**, short enough to
   observe within the lab. This makes Jenkins periodically re-scan the repository for new or
   changed branches and PRs, and build anything it finds changed, the polling equivalent of a
   webhook.

### Part C — Prove it triggers automatically

7. Create a new branch, make a small change, push it, and open a PR.
8. Confirm Jenkins automatically discovers the PR and builds it, without you clicking Build Now.
   With polling instead of a webhook, this can take up to the polling interval to appear, so
   give it a minute or two rather than expecting it instantly.
9. Merge the PR to `main`.
10. Confirm Jenkins automatically triggers a separate build for `main` itself (again, allow up
    to the polling interval).
11. Once you've seen both automatic builds happen, turn polling back off: return to **Scan
    Repository Triggers** and untick **Periodically if not otherwise run** (or set it to a much
    longer interval, e.g. daily). A 1-minute poll is fine for demonstrating the concept in this
    lab, but left running it would repeatedly hit GitHub's API and rescan the repository for no
    reason, one of the real reasons teams prefer webhooks over polling in production.

### Part D — Close the loop with branch protection

12. If you have admin rights, configure branch protection on `main` to require this pipeline's
    check to pass before merging (as discussed conceptually in Module 03).
13. If you don't have admin rights, write two or three sentences describing exactly what you'd
    configure, referencing the actual job name Jenkins is reporting as a status check.

## Acceptance criteria

- A `Jenkinsfile` exists in your repository with Checkout, Build Image, and Test stages.
- A Multibranch Pipeline job in Jenkins has discovered your repository's branches and PRs.
- You've demonstrated an automatic build triggered by opening a PR, and a separate automatic
  build triggered by a merge to `main`, without manually clicking Build Now for either.
- You've turned the polling interval back down (or off) after observing both automatic builds.
- You can explain what branch protection rule would make this pipeline's result required before
  merging.

If you finish early, break the placeholder test deliberately (make it assert false), push, and
watch the PR's automatic build go red, this is Module 03's "failing pipeline protects main" made
real, on a pipeline you wrote yourself.
