# Demo: Module 08 - CI Pipeline Build Lab

**Duration:** 12 minutes
**Prerequisite:** The `starter/` project from this lab pushed to a GitHub repository. Access to
your local Jenkins (in Docker, on `http://localhost:8080`) with rights to create a job, and the
GitHub Branch Source and GitHub plugins installed. Admin rights on the GitHub repository (to add a
webhook), and Node.js installed (for `npx smee-client`). Start a smee.io channel before the
session so the URL is ready to paste.

## Part 1: Recap, quickly (2 min)

Narration: Module 05 covered pipeline stages conceptually, using a provided log you only had to
read. Module 06 gave you a real multi-stage Dockerfile. Today you write the Jenkinsfile from
scratch yourself, and, for the first time this programme, wire up *automatic* triggering, not
just clicking Build Now.

## Part 2: A job that only builds one branch isn't enough (2 min)

Narration: every Jenkins job so far (Module 02, this week's Module 05) has been a
single Pipeline job pointed at one branch, built manually or on a single webhook. The
Foundations week's Module 6's whole workflow depends on the pipeline running on *every* PR, and again on merge to main. A
single-branch job can't do that on its own.

Show, on the diagram, the difference between a plain **Pipeline job** and a **Multibranch
Pipeline job**: a Multibranch Pipeline auto-discovers every branch and every open PR in a
repository (via the GitHub Branch Source plugin) and builds each one independently, whenever it
changes.

## Part 3: Writing the Jenkinsfile from scratch (4 min)

```groovy
pipeline {
    agent any
    tools {
        maven 'Maven3'
    }
    triggers {
        githubPush()
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build -t team-skeleton:${BUILD_NUMBER} .'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn -B test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }
    }
}
```

Narration: three stages, nothing here is new syntax, this is Module 05's shape (Checkout,
Build, Test) applied to the multi-stage Dockerfile from Module 06. `${BUILD_NUMBER}` tags each
image uniquely, a small habit worth normalising early. `githubPush()` is the Jenkinsfile
equivalent of ticking **GitHub hook trigger for GITScm polling**: build when GitHub says so.

## Part 4: Configuring the Multibranch Pipeline job (3 min)

In Jenkins: **New Item > Multibranch Pipeline**, point it at the GitHub repository, and confirm
it discovers `main` plus any open branches/PRs, each getting its own sub-job automatically.

Then the webhook. Jenkins is on `localhost`, which GitHub can't reach, so relay it through
smee.io:

```bash
npx smee-client --url https://smee.io/<channel> --target http://localhost:8080/github-webhook/
```

On GitHub: **Settings > Webhooks > Add webhook**, payload URL = the smee.io channel URL,
content type `application/json`, events **Pushes** and **Pull requests**. Show the `ping`
arriving in three places: the smee.io tab, the smee-client terminal, and a green tick under
**Recent Deliveries**. Point out the trailing `/github-webhook/` on the target, it's the most
common mistake.

## Part 5: Prove the triggers work (1 min)

Push a small change on a feature branch and open a PR, watch Jenkins pick it up automatically.
Merge to `main`, watch a separate build trigger for `main` itself.

## Key message

The pipeline stages themselves (Checkout, Build, Test) are things you already know how to
write. What's new today is making the pipeline run *automatically*, on every PR and on every
merge to main, which is what actually makes the Foundations week's Module 6 branch protection meaningful in
practice, not just in theory.
