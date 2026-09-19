# Module 09 Lab — Annotated Answers (Instructor Reference)

## 1. Stages, in order

| Stage | Started | What it does |
|---|---|---|
| Checkout | 09:14:02 | Pulls the exact commit that triggered the run from GitHub |
| Build | 09:14:04 | Compiles the code with Maven; fails fast if it doesn't compile |
| Test | 09:14:19 | Runs the automated test suite and records the results |
| Archive | 09:14:25 | Saves and fingerprints the built `.jar` as an artifact |

## 3. Timing

- **Total duration**: 24 seconds (`Finished: SUCCESS, Total time: 24 s`).
- **Longest stage**: Build (09:14:04 to 09:14:19, roughly 15 seconds) — compiling source files
  is the most time-consuming step here; Test and Archive are both quick by comparison.

## 4. What would stop the pipeline?

- If Build had failed to compile, Test would **not** run. Each stage depends on the previous
  one succeeding — there's no point running tests against code that doesn't compile.
- If one test had failed, Jenkins would report the pipeline as failed overall, publish the test
  results showing the failure (via the `junit` step, which records results whether they pass or
  fail), and the Archive stage would **not** run, since the pipeline in this Jenkinsfile stops
  at the first failing stage.

## 5. CI vs CD

- This pipeline is **Continuous Integration**, with the Archive stage laying groundwork for
  delivery: it produces a versioned, fingerprinted artifact ready to hand off, but nothing
  deploys it anywhere automatically, and no human approval step exists yet either.
- To become **Continuous Deployment**, a further stage would need to take the archived artifact
  and deploy it to a live environment automatically, with no manual gate. Getting there safely
  usually requires strong automated test coverage and a rollback strategy, that's why it's
  introduced gradually across the programme rather than on day one.
