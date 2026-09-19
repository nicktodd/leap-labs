# Demo: Module 10 — Introduction to Jenkins

**Duration:** 12 minutes
**Prerequisite:** Access to the Sprint 1 Jenkins instance. A Pipeline job called
`sprint1-demo-app` already created, pointing at a repository containing the
[`starter/`](../../labs/10-jenkins-intro/starter) project from this module's lab (this is the
**broken** version, used deliberately for this demo).

## Part 1: Navigating the Jenkins UI (3 min)

- **Dashboard**: the list of all jobs, with status icons (blue/green ball = last build passed,
  red = failed)
- Click into `sprint1-demo-app`: the **job page** shows build history down the left, a
  **Build Now** button, and a summary of the last build
- Click a build number (e.g. `#4`): the **build page** shows the stage view, duration, and a
  link to **Console Output**

Narration: everything here mirrors what you saw in Module 09's sample log, just inside the
Jenkins web UI instead of a plain text file.

## Part 2: Jobs vs pipelines (2 min)

Narration: a **job** is Jenkins's general term for something it can run and track history for.
A **freestyle job** is configured entirely through the UI: a fixed list of build steps, no
code. A **Pipeline job** is defined by a `Jenkinsfile`, checked into the repository alongside
the code it builds. That's what we're using this sprint, and what you saw the syntax of in
Module 05 and Module 09.

## Part 3: Running the job and reading the result (3 min)

Click **Build Now**. Once it starts, open the build and watch the **stage view** update live,
then open **Console Output**.

Narration: this job is deliberately broken. Scroll to the Test stage output and find:

```text
ERROR: No test report files were found. Configuration error?
```

Ask the room: what does this error actually mean? Most people haven't seen it before, that's
exactly the point.

## Part 4: Using GenAI to interpret the error (3 min)

Select the error text and the relevant Jenkinsfile stage in the editor, and ask Copilot Chat:

```text
This Jenkins pipeline fails at the Test stage with "No test report files were found.
Configuration error?" Here is the Test stage from the Jenkinsfile. What does this error
mean, and what's the most likely cause?
```

Narration: read the explanation aloud. It should point out that the `junit` step's glob
pattern doesn't match where Maven Surefire actually writes its XML reports
(`target/surefire-reports/*.xml` by default, not `target/test-reports/*.xml`). Critique it the
same way as Module 05: does this match what we'd expect, and is there a way to confirm it (for
example, checking the actual folder structure under `target/` after a local `mvn test` run)?

## Part 5: Fixing and re-running (1 min)

Edit the `Jenkinsfile`, correct the glob to `target/surefire-reports/*.xml`, commit, push, and
click **Build Now** again. Show the build going green.

## Key message

Reading a Jenkins failure starts in exactly the same place every time: open Console Output,
find where it stopped, and read the error. GenAI is a fast way to turn an unfamiliar error
message into a plausible explanation, but you still confirm it before trusting it, exactly the
habit built in Module 05.
