# Module 10 Lab — Introduction to Jenkins

## Objectives

By the end of this lab you will have:

- Navigated the Jenkins UI: dashboard, job page, build page, console output
- Run an existing pipeline and read its result
- Diagnosed a deliberately broken pipeline stage, using GenAI as a first port of call
- Fixed the break and confirmed the pipeline goes green

## Setup

- Access to the Sprint 1 Jenkins instance
- Maven 3 configured as a tool in Jenkins (**Manage Jenkins > Tools > Maven installations > Add
  Maven**, name it `Maven3`, and let Jenkins install it automatically). This only needs doing
  once per Jenkins instance, ask your trainer if it's already set up. The name must be exactly
  `Maven3` to match the `tools` block in the [`Jenkinsfile`](starter/Jenkinsfile).
- Your own Pipeline job in Jenkins, pointing at your own copy of the
  [`starter/`](starter) project from this lab, pushed to your GitHub repository from Module 08
- GitHub Copilot Chat available in IntelliJ

## Task sheet

### Part A — Run it and find the break

1. Copy `starter/` into your own repository (or a new one), push it to GitHub, and create a
   Jenkins Pipeline job pointing at it. Ask your trainer if you're unsure how to create the job.
2. Click **Build Now** and watch the stage view.
3. Once the build finishes, open **Console Output** and find the error. Note down the exact
   error message and which stage it occurred in.

### Part B — Diagnose with GenAI

4. Open the `Jenkinsfile` in IntelliJ. Select the `Test` stage and, in Copilot Chat, ask it to
   explain the error message you found and suggest the most likely cause. Remember: this is
   still a learning-aid prompt, ask it to explain, not to fix the file for you.
5. Critique the explanation: does it match what you know about how Maven Surefire works? Check
   for yourself by running `mvn test` locally and looking at what actually gets created under
   `target/`.

### Part C — Fix it and confirm

6. Based on your diagnosis, edit the `Jenkinsfile` yourself to fix the broken step.
7. Commit and push the fix.
8. Run the Jenkins job again and confirm it now succeeds. Open Console Output once more and
   confirm the Test stage now reports passing tests, and the Archive stage runs.

## Acceptance criteria

- You can state the exact error message the broken pipeline produced, and which stage it came
  from.
- You have a short written note (a few sentences) on what GenAI told you the error meant, and
  whether you confirmed it was accurate.
- Your fixed pipeline shows a green (successful) build in Jenkins, with the Test stage
  reporting passing tests and the Archive stage completing.

If you finish early, compare your fix with a partner's, did you phrase your Copilot prompt the
same way? Did you get the same explanation?
