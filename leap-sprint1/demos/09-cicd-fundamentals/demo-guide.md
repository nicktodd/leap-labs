# Demo: Module 09 — CI/CD Fundamentals

**Duration:** 8 minutes
**Prerequisite:** `sample-pipeline-log.txt` open or projected on screen. No hands-on tooling
needed yet, Module 10 covers running Jenkins directly.

## Part 1: The problem CI/CD solves (2 min)

Narration: before CI/CD, "does this work" meant one developer manually building, testing, and
deploying on their own machine, then hoping it behaves the same way for everyone else. Ask the
room: what could go wrong with that? (Collect answers: "works on my machine," forgotten test
runs, inconsistent environments, slow feedback.)

## Part 2: Walking the sample pipeline log (4 min)

Open `sample-pipeline-log.txt` and read through it stage by stage:

- **Checkout**: Jenkins pulls the exact commit that triggered this run
- **Build**: `mvn clean package` compiles the code, fails fast if it doesn't compile
- **Test**: the automated test suite runs, results are recorded whether they pass or fail
- **Archive**: the built artifact (`.jar` file) is saved and fingerprinted for later stages or
  pipelines to use

Narration: point out the timestamps. This whole cycle took 24 seconds. That's the point:
continuous integration means every change gets this same rigorous check, fast enough that
nobody is tempted to skip it.

## Part 3: Continuous integration vs continuous delivery vs continuous deployment (1 min)

Narration, using the terms precisely:

- **Continuous Integration (CI)**: every change is automatically built and tested
- **Continuous Delivery**: every change that passes CI is automatically packaged and ready to
  release, a human still decides when
- **Continuous Deployment**: every change that passes CI goes live automatically, no human gate

Point out our sample pipeline stops at Archive: that's CI, plus the first step toward delivery.
Full deployment automation comes with Docker and later sprints.

## Part 4: Where Jenkins sits (1 min)

Narration: Jenkins is the tool that *runs* this pipeline. It watches for a trigger (commit
pushed, or on a schedule), checks out the code, and executes each stage in order, stopping and
reporting failure the moment something breaks. Module 10 opens Jenkins itself and runs a
pipeline like this one live.

## Key message

CI/CD isn't a specific tool, it's a discipline: every change gets built, tested, and packaged
automatically and consistently. Jenkins is one tool (the one we use this sprint) that
implements that discipline.
