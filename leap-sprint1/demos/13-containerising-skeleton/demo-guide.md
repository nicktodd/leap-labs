# Demo: Module 13 — Containerising the Project Skeleton

**Duration:** 12 minutes
**Prerequisite:** A team repository already set up with a branching strategy (Module 12). Docker
Desktop running, and access to the Sprint 1 Jenkins instance. No new commands beyond Modules 07,
10, and 11.

## Part 1: Framing the task (1 min)

Narration: like Module 12, there's nothing new to learn here technically. This is Module 11's
Dockerfile skills, Module 07's branching skills, and Module 10's Jenkinsfile syntax, applied
together, on the team repository you just created.

## Part 2: Branch, add the skeleton (3 min)

Using whatever branch naming the team agreed in Module 12 (or a sensible default like
`feature/docker-skeleton` if their strategy doesn't specify one):

```bash
git switch -c feature/docker-skeleton
```

Add a minimal "hello world" app, a Dockerfile, and build it:

```dockerfile
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY target/team-skeleton-0.1.0.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

```bash
mvn clean package
docker build -t team-skeleton .
docker run --rm team-skeleton
```

Narration: `--rm` here instead of `-d`, this app just prints a message and exits, there's
nothing to leave running or inspect afterwards, unlike Module 11's app.

## Part 3: Commit and merge via the team's strategy (3 min)

```bash
git add Dockerfile pom.xml src
git commit -m "Add containerised hello world skeleton"
git push -u origin feature/docker-skeleton
```

Narration: this is exactly the moment the team's Module 12 decision matters. If they chose
trunk-based, merge straight back to `main` quickly. If they chose something with a review step,
have a teammate look at the branch first. Either way, the mechanics are identical to Module 07.

```bash
git switch main
git merge feature/docker-skeleton
git push
```

## Part 4: Confirm everyone can reproduce it (1 min)

Have a second team member pull `main`, build the image, and run it themselves.

Narration: the point isn't just "it builds on my machine", it's confirming the whole team can
reproduce the same containerised skeleton from a clean checkout. That's the property CI (coming
properly in a later sprint) will eventually verify automatically.

## Part 5: A simple Jenkinsfile for the skeleton (3 min)

Narration: the skeleton is committed and reproducible by hand. The last step is letting Jenkins
do that reproduction check automatically, the same discipline from Module 09, now applied to the
team's own repository for the first time.

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build -t team-skeleton .'
            }
        }
        stage('Smoke Test') {
            steps {
                sh 'docker run --rm team-skeleton'
            }
        }
    }
}
```

Create a Jenkins Pipeline job pointing at the team repository, commit the `Jenkinsfile` to
`main` via the team's branching strategy (exactly like Part 3), then click **Build Now** and
show all three stages going green.

## Key message

A working, committed, containerised skeleton is the last piece needed before the team starts
building on top of it, and a Jenkins job that rebuilds and smoke-tests it automatically is what
turns "it worked when we checked" into something the team can trust on every future change.
Everything from here on in the programme builds on this same repo, same strategy, same
container pattern, same pipeline.
