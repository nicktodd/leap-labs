# Module 09 — CI/CD Pipeline Analysis

## Stages in order

1. **Checkout** — 09:14:02 — cloned the repository and checked out commit a7e9c31
2. **Build** — 09:14:04 — ran `mvn -B clean package`, compiled 4 source files, produced the jar in 14s
3. **Test** — 09:14:19 — ran `mvn -B test`, 6 tests ran, 6 passed, 0 failures
4. **Archive** — 09:14:25 — archived `target/sprint1-demo-app-0.1.0.jar` with fingerprinting

## Timing

- Total pipeline duration: **24 seconds**
- Longest stage: **Build** (approx 14s) — Maven downloads/resolves dependencies and compiles, which is inherently slower than running tests against already-compiled code

## What would stop the pipeline?

- If Build had failed to compile, the Test stage would NOT have run — Jenkins executes stages sequentially and stops on failure by default
- If one test had failed, Jenkins would mark the build as FAILED/UNSTABLE and the Archive stage would NOT run (no artifact to archive from a broken build)

## CI vs CD

This is **Continuous Integration** — code is automatically built, tested, and the artifact archived on every push, but there is no automated deployment step. To become Continuous Deployment, a Deploy stage would need to be added after Archive that automatically pushes the jar/container to a live environment without manual approval.
