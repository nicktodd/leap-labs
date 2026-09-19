# Module 05 Lab — Trace a Multi-Stage Pipeline Failure

## Recap: where we left off in Sprint 1

- **Module 09 (CI/CD Fundamentals)**: pipeline stages, and CI vs Delivery vs Deployment
- **Module 10 (Introduction to Jenkins)**: navigating Jenkins, and using GenAI as a first port
  of call to interpret an unfamiliar failure

This lab extends both: a longer pipeline with a security gate, and a real reason (Module 03's
branch protection) why a failing stage actually matters.

## Objectives

By the end of this lab you will have:

- Traced a multi-stage Jenkins pipeline run and identified which stage failed
- Read the failure in the console log and explained it in plain English
- Used GenAI as a first port of call to interpret unfamiliar pipeline output, then verified it
- Understood how this connects to branch protection from Module 03

## Setup

- [`sample-pipeline-log.txt`](../../demos/05-devops-cicd-deeper-dive/sample-pipeline-log.txt)
  from the demo
- GitHub Copilot Chat

## Task sheet

1. **Identify the stages**
   List every stage in the pipeline, in order, and mark which ones passed and which one (if
   any) failed. For the `Test` and `Acceptance Test` stages specifically, write one sentence
   each on what each one is actually checking, and how they differ.

2. **Read the failure**
   For the failed stage, copy the exact error line(s) from the log. What tool produced this
   output? What specifically did it flag?

3. **Use GenAI, then verify**
   Ask Copilot Chat to explain the failure in plain English. Then verify at least one specific
   claim from its explanation yourself (for example, look up the CVE mentioned, or read what the
   tool's documentation says a CRITICAL severity finding means).

4. **Explain it in plain English, in your own words**
   Write two or three sentences a non-technical stakeholder could understand: what went wrong,
   and why the pipeline stopped rather than continuing to Deploy.

5. **Connect it to branch protection**
   If this repository's `main` branch requires this pipeline to pass before merging (Module
   03), what would have happened if this change had been merged anyway? Write one sentence.

## Acceptance criteria

- You've correctly identified the failed stage and quoted the specific error.
- You have a written, verified explanation of the failure, not just GenAI's raw output pasted
  in unchanged.
- Your plain-English explanation would make sense to someone who has never seen a Jenkins log
  before.
- You've explicitly connected this failure to what branch protection would have prevented.

If you finish early, look up CVE-2019-12384 for real, was the GenAI explanation of its severity
and impact accurate?
