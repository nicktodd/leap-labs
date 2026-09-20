# Module 11 Demo Guide - Deployment Automation: Scripting the Full Pipeline

**Duration:** 55 minutes
**Prerequisite:** Module 6's ECR repository, Module 7's cluster and execution role, Module 9's
task definition history, all still in place.

## Part 0: What's Being Automated (5 min)

Every module since Module 6 has run the same sequence of commands by hand: build an image, push
it to ECR, register a task definition, deploy it. A pipeline runs that same sequence
automatically, triggered by a commit landing on the main branch. This module uses **Jenkins**,
one of the most widely deployed CI/CD tools in real organisations (the firm included, per the
mission brief) - but the sequence itself (build, push, deploy, verify) is the same regardless of
which tool runs it.

## Part 0b: Recap - What a Jenkins Pipeline Actually Is (10 min)

The Pipelines week introduced Jenkins and CI/CD fundamentals - worth a proper recap here, since that was
close to three months ago:

- A **pipeline** is an automated sequence of **stages** (commonly Build, Test, Archive, and -
  from here on - Deploy) that runs every time code changes. If an early stage fails, later stages
  don't run at all: a broken Build stage means Test and Deploy never get a chance to run against
  broken code.
- **Continuous Integration** means every change is automatically built and tested. **Continuous
  Delivery** extends that with an artefact ready to deploy at any time. **Continuous Deployment**
  goes one step further and deploys automatically with no manual approval step - this module's
  pipeline is a continuous deployment pipeline: a merge to `main` deploys, with nothing else
  needed.
- Jenkins itself distinguishes a **freestyle job** (build steps configured by hand through the
  Jenkins UI, no code) from a **Pipeline job**, defined by a `Jenkinsfile` checked into the
  repository alongside the application code - the same file everyone on the team can read,
  review, and change through a normal pull request, rather than a UI configuration only visible
  to whoever has Jenkins access. This module uses a Pipeline job throughout.
- The Jenkins dashboard shows a job's build history (blue/green for passed, red for failed); each
  build has its own **Console Output**, the real, complete log of everything that build actually
  ran - the first place to look when a stage fails.

Today's Jenkinsfile follows exactly that shape - `pipeline { agent { ... } stages { stage('Build
and Push') { ... } stage('Deploy') { ... } } }` - the only things genuinely new since the
Pipelines week are what happens *inside* those stages: real AWS CLI calls instead of the Maven/JUnit steps from
the Pipelines week's Java-focused examples.

## Part 1: Authenticating Without Stored Credentials - the Instance Profile (12 min)

A pipeline needs AWS credentials, and the worst way to provide them is a long-lived access key
pasted into Jenkins' own credentials store - it doesn't expire on its own, and if that Jenkins
server is ever compromised, so is the key. Jenkins running on an EC2 instance has a better
option: an **instance profile**, an IAM role attached directly to the instance. AWS's SDKs and
CLI pick up temporary, automatically-rotated credentials from the instance's own metadata service
with no configuration at all - nothing is typed into Jenkins, nothing is stored as a Jenkins
credential.

Two AWS resources make this work. First, an IAM role trusted by EC2 itself:

```bash
aws iam create-role --role-name leap-jenkins-deploy-role \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{
    "Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},
    "Action":"sts:AssumeRole"}]}'
```

Second, an instance profile wrapping that role, which is what actually gets attached to the EC2
instance running Jenkins:

```bash
aws iam create-instance-profile --instance-profile-name leap-jenkins-deploy-profile
aws iam add-role-to-instance-profile --instance-profile-name leap-jenkins-deploy-profile \
  --role-name leap-jenkins-deploy-role
```

The role's own permissions are scoped tightly: push to one named ECR repository, register task
definitions and update one named ECS service, and `iam:PassRole` on the execution role only -
verified directly:

```bash
aws iam get-role-policy --role-name leap-jenkins-deploy-role \
  --policy-name leap-jenkins-deploy-policy --query 'PolicyDocument.Statement[].Sid'
["ECRAuth", "ECRPush", "ECSDeploy", "PassExecutionRoleOnly"]
```

## Part 2: The Build and Push Stage (10 min)

Every step the Jenkinsfile's `Build and Push` stage runs, executed directly to confirm each one
works - no `aws configure` step anywhere, since the instance profile handles authentication:

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker build -t <account>.dkr.ecr.us-east-1.amazonaws.com/leap-mission-service:<sha> .
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/leap-mission-service:<sha>
```

Output: a digest from ECR, confirming the push succeeded - the same push confirmation Module 6
first introduced.

## Part 3: The Render and Deploy Stages (12 min)

The pipeline's `Deploy` stage does two things: build a new task definition, then point the ECS
service at it. Building the task definition always starts from the **current live** definition,
never a checked-in JSON file or a previously-registered copy:

```bash
aws ecs describe-task-definition --task-definition leap-mission-service \
  --query taskDefinition > current-taskdef.json
python3 render_taskdef.py current-taskdef.json <account>.dkr.ecr.us-east-1.amazonaws.com/leap-mission-service:<sha> \
  > new-taskdef.json
aws ecs register-task-definition --cli-input-json file://new-taskdef.json
```

`render_taskdef.py` strips the fields `describe-task-definition` returns that
`register-task-definition` doesn't accept (revision number, ARNs, status), swaps in the new
image, and leaves everything else - ports, log configuration, execution role - exactly as the
live definition already has it. Starting from the live definition this way means the pipeline
never has to keep its own separate copy of the task definition in sync with whatever's actually
running.

```bash
aws ecs update-service --cluster leap-mission-cluster --service leap-mission-service \
  --task-definition <new-taskdef-arn> --force-new-deployment
aws ecs wait services-stable --cluster leap-mission-cluster --services leap-mission-service
```

Wired into the Jenkinsfile, these are exactly the shell commands inside a `Deploy` stage,
sitting alongside the `Build and Push` stage from Part 2 in the same pipeline:

```groovy
stage('Deploy') {
  steps { sh '''
    aws ecs describe-task-definition --task-definition leap-mission-service \
      --query taskDefinition > current-taskdef.json
    python3 render_taskdef.py current-taskdef.json \
      $ECR_REGISTRY/$REPO:$TAG > new-taskdef.json
    aws ecs register-task-definition --cli-input-json file://new-taskdef.json \
      --query taskDefinition.taskDefinitionArn --output text > new-taskdef-arn.txt

    aws ecs update-service --cluster $ECS_CLUSTER --service $ECS_SERVICE \
      --task-definition $(cat new-taskdef-arn.txt) --force-new-deployment
    aws ecs wait services-stable --cluster $ECS_CLUSTER --services $ECS_SERVICE
  ''' }
}
```

Jenkins runs a pipeline's stages in order - `Deploy` only starts once `Build and Push` has
completed successfully, the same fail-fast behaviour the Pipelines week's CI/CD fundamentals covered.

## Part 3b: Acceptance Tests - Checking the Deployment Actually Works (10 min)

`Deploy` confirms a task reached `RUNNING`. It says nothing about whether the application
actually works for a user - that's a different kind of check, and the Angular week's Module 20 already
built exactly the tool for it: a Playwright suite (`login.spec.ts`) testing the mission-ui
frontend end to end - logging in, an invalid-password error, the redirect to `/login` when
logged out, and logout itself.

That suite becomes an **Acceptance Tests** stage, running after `Deploy`, unchanged except for
one thing: the Angular week's Module 20's `playwright.config.ts` hardcodes `baseURL: 'http://localhost:4200'` for
local development. Before it can run against a deployed environment, that needs to read an
environment variable instead, with the local default kept as a fallback for anyone still running
it by hand:

```typescript
use: { baseURL: process.env.BASE_URL || 'http://localhost:4200' },
```

The stage itself:

```groovy
stage('Acceptance Tests') {
  steps { sh '''
    cd mission-ui
    npm ci
    npx playwright install --with-deps chromium
    BASE_URL=$DEPLOYED_URL npx playwright test
  ''' }
}
```

The exact same spec file from the Angular week, now verifying the real deployed frontend and its real
auth-service instead of a local dev server. A pipeline that stops at "the task is `RUNNING`" is
checking infrastructure, not the feature a user actually cares about - a merge only counts as a
successful deployment once the acceptance tests pass too.

## Part 4: Verified - the Deployed Revision Runs (8 min)

```bash
aws ecs run-task --cluster leap-mission-cluster --task-definition leap-mission-service:5 \
  --launch-type FARGATE --network-configuration '...'
```

CloudWatch logs confirm a Spring Boot startup from the freshly built, freshly pushed image - the
same verification discipline every earlier module has used, applied to a task definition a
pipeline produced rather than a human typing commands by hand.

## Key Message

A deployment pipeline isn't a new set of concepts - it's the same pipeline shape the Pipelines week
introduced (stages, triggered automatically, failing fast when something's wrong), running the
same build/push/register/verify sequence this week has run by hand since Module 6, and
authenticating without ever storing a credential in the tool running it. Jenkins' instance
profile and other CI/CD tools' equivalent mechanisms all solve the same underlying problem - a
pipeline needs temporary, non-stored AWS credentials - in whichever way fits that tool.

## Transition to the Lab

Candidates set up their own instance profile and scoped role, write their own Jenkinsfile, and
run each of its steps directly to confirm the pipeline they've written actually works before ever
trusting it to run unattended.
