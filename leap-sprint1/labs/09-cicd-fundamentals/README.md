# Module 09 Lab — CI/CD Fundamentals

## Objectives

By the end of this lab you will have:

- Traced a sample pipeline run stage by stage
- Identified what happens, and why, at each stage
- Distinguished continuous integration from continuous delivery and continuous deployment

## Setup

- [`sample-pipeline-log.txt`](../../demos/09-cicd-fundamentals/sample-pipeline-log.txt) from the
  demo

## Task sheet

1. **Identify the stages**
   - Read through `sample-pipeline-log.txt`.
   - List the stages in the order they ran, and the timestamp each one started.

2. **What happened in each stage?**
   - For each stage, write one sentence describing what it actually did.
   - For the Test stage specifically, note how many tests ran and how many passed.

3. **Timing**
   - What was the total pipeline duration?
   - Which stage took the longest? Why might that be, given what each stage does?

4. **What would stop the pipeline?**
   - If the Build stage had failed to compile, would the Test stage still have run? Why?
   - If one test had failed in the Test stage, what do you think Jenkins would report, and
     would the Archive stage still run?

5. **CI vs CD**
   - This pipeline stops after Archive. Is that Continuous Integration, Continuous Delivery, or
     Continuous Deployment? Justify your answer in one sentence.
   - What would need to change for this to become Continuous Deployment?

## Acceptance criteria

- You have a written list of all four stages, in order, with one sentence each on what happens.
- You can state the total pipeline duration and identify the longest stage.
- Your CI vs CD answer correctly identifies this pipeline as CI (with delivery groundwork via
  the Archive stage) and explains what deployment automation would add.

If you finish early, sketch (on paper or in your notes) what you'd expect the log to look like
if the Test stage had failed, based on what you already know about how the stages depend on
each other.
