# Module 04 Lab - Walkthrough (Instructor Reference)

```bash
git switch -c feature/docker-skeleton

# copy starter/ files in, edit Main.java's <team-name> placeholder

mvn clean package
docker build -t team-skeleton .
docker run --rm team-skeleton
# Hello world from Sprint Squad's project skeleton

git add Dockerfile pom.xml src
git commit -m "Add containerised hello world skeleton"
git push -u origin feature/docker-skeleton

# merge according to the team's Foundations week's Module 9 strategy, e.g. for trunk-based:
git switch main
git merge feature/docker-skeleton
git push
```

## Adding the Jenkinsfile (Part E)

```bash
git switch -c feature/jenkins-skeleton
# add Jenkinsfile (see solutions/04-containerising-skeleton/Jenkinsfile) at repo root
git add Jenkinsfile
git commit -m "Add Jenkinsfile to build and smoke-test the skeleton"
git push -u origin feature/jenkins-skeleton

git switch main
git merge feature/jenkins-skeleton
git push
```

Create the Jenkins Pipeline job pointing at the team repository (`Jenkinsfile` at the root, same
pattern as Module 02), then **Build Now**. Expected result: all three stages (Checkout, Build
Image, Smoke Test) green, with the Smoke Test stage's console output showing the team's hello
world message.

## What to check as an instructor

- The Dockerfile is single-stage and minimal, matching Module 03's pattern (base image,
  `WORKDIR`, `COPY`, `ENTRYPOINT`). A multi-stage build isn't wrong, but isn't required at this
  stage either.
- The merge into `main` actually followed whatever the team documented in the Foundations
  week's Module 9, not just
  "whatever was quickest." Ask a team member to explain the step they took and why.
- A second team member, working from a clean `git pull`, can reproduce the exact same
  `docker build` and `docker run` result. This confirms the skeleton isn't accidentally relying
  on something local to one person's machine (a stray file, a cached layer, a locally installed
  tool not captured anywhere in the repo).
- The Jenkins job runs from the `Jenkinsfile` on `main`, not a local copy pasted into the job
  configuration, that's the whole point of a Pipeline job over a freestyle one (Module 02).
- All three stages go green, and the Smoke Test stage's console output shows the team's actual
  hello world message, not just "the container started."
