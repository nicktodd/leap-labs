# Lab 08 — Blocked: Jenkins Required

## Status

BLOCKED. This lab requires:
- A running Jenkins instance (Multibranch Pipeline plugin installed)
- A GitHub repository with webhook access pointed at the Jenkins instance
- Rights to create a Jenkins job

None of these are available in the local environment. The Jenkinsfile deliverable has been
written and committed to this folder — it is syntactically complete and follows the three-stage
spec (Checkout, Build Image, Test with JUnit publishing).

## What would need to happen to unblock

1. Install Jenkins (Docker: `docker run -p 8080:8080 jenkins/jenkins:lts`) or use a
   team-provisioned instance.
2. Create a Multibranch Pipeline job pointing at the team GitHub repository.
3. Install the GitHub webhook plugin and configure the webhook URL in GitHub
   (`http://<jenkins-host>/github-webhook/`).
4. Push the Jenkinsfile on a branch, open a PR, and confirm Jenkins discovers and builds it
   automatically.

## Branch protection note (Part D)

Once the pipeline is running, branch protection on `main` would be configured to require the
Jenkins Multibranch Pipeline status check to pass before merging. The exact check name would
be `sprint2-team-project/main` (or the PR branch name) as reported by Jenkins in the GitHub
Checks UI.
