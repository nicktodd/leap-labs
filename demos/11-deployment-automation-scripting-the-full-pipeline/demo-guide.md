# Module 11 Demo Guide — Deployment Automation: Scripting the Full Pipeline

**Duration:** 55 minutes
**Prerequisite:** Module 6's ECR repository, Module 7's cluster and execution role, Module 9's
task definition history, all still in place.

## Part 0: What's Being Automated (5 min)

Every module since Module 6 has run the same sequence of commands by hand: build an image, push
it to ECR, register a task definition, deploy it. A real pipeline runs that same sequence
automatically, triggered by a commit landing on the main branch. This module uses **Jenkins**,
one of the most widely deployed CI/CD tools in real organisations (Fidelity included, per the
mission brief) — but the sequence itself (build, push, deploy, verify) is the same regardless of
which tool runs it.

## Part 1: Authenticating Without Stored Credentials — the Instance Profile (15 min)

A pipeline needs AWS credentials, and the worst way to provide them is a long-lived access key
pasted into Jenkins' own credentials store — it doesn't expire on its own, and if that Jenkins
server is ever compromised, so is the key. Jenkins running on an EC2 instance has a better
option: an **instance profile**, an IAM role attached directly to the instance. AWS's SDKs and
CLI pick up temporary, automatically-rotated credentials from the instance's own metadata service
with no configuration at all — nothing is typed into Jenkins, nothing is stored as a Jenkins
credential.

Two real AWS resources make this work. First, an IAM role trusted by EC2 itself:

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
definitions and update one named ECS service, and `iam:PassRole` on the execution role only —
verified directly:

```bash
aws iam get-role-policy --role-name leap-jenkins-deploy-role \
  --policy-name leap-jenkins-deploy-policy --query 'PolicyDocument.Statement[].Sid'
["ECRAuth", "ECRPush", "ECSDeploy", "PassExecutionRoleOnly"]
```

## Part 2: The Pipeline's Steps, Run Directly (15 min)

Every step the Jenkinsfile (`Jenkinsfile.example`) would run, executed directly to confirm each
one actually works — exactly what the instance-profile credentials on a Jenkins agent would do,
with no `aws configure` step anywhere:

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker build -t <account>.dkr.ecr.us-east-1.amazonaws.com/leap-mission-service:<sha> .
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/leap-mission-service:<sha>
```

Real output: a genuine digest from ECR, confirming the push succeeded.

## Part 3: A Real Failure — Cloning a Stale Task Definition (10 min)

The first deploy attempt copied the *previous* task definition (Module 9's revision 3) and only
swapped its image — the same shortcut it's tempting to script directly into a Jenkinsfile's shell
steps. Running it produced a real failure:

```
ResourceInitializationError: unable to pull secrets or registry auth ...
AccessDeniedException: ... is not authorized to perform: secretsmanager:GetSecretValue
on resource: arn:...secretsmanager:...rds!db-...
```

Revision 3 referenced Module 9's RDS secret — which was deleted, along with the execution role's
permission to read it, when Module 9 was torn down. Cloning an old revision cloned that stale
reference too. This is exactly why the pipeline's "Render Task Definition" stage
(`render_taskdef.py.example`) starts from `aws ecs describe-task-definition` on the **current
live** task definition and only swaps the image field — never a checked-in JSON file or a
previously-registered copy that might be out of date, or worse, reference something that no
longer exists.

The fix: build a clean task definition from the current live one and register that instead:

```bash
aws ecs register-task-definition --cli-input-json file://taskdef-clean.json
# revision 5, referencing the newly-pushed image
```

## Part 4: Verified — the New Revision Actually Runs (8 min)

```bash
aws ecs run-task --cluster leap-mission-cluster --task-definition leap-mission-service:5 \
  --launch-type FARGATE --network-configuration '...'
```

Real CloudWatch logs confirm a genuine Spring Boot startup from the freshly built, freshly pushed
image — the same verification discipline every earlier module has used, applied to a task
definition a pipeline produced rather than a human typing commands by hand.

## Key Message

A deployment pipeline isn't a new set of concepts — it's the same build/push/register/verify
sequence this sprint has run by hand since Module 6, made to run automatically and authenticate
without ever storing a credential in the tool running it. Jenkins' instance profile and GitHub
Actions' OIDC solve the same underlying problem (a pipeline needs temporary, non-stored AWS
credentials) in the way that fits each tool. The one genuinely new risk automation introduces is
exactly what today's real failure demonstrated: a script that blindly clones the last task
definition can silently carry forward something that's since been deleted. Building from the
current live definition avoids it, regardless of which CI/CD tool is doing the building.

## Transition to the Lab

Candidates set up their own instance profile and scoped role, write their own Jenkinsfile, and
run each of its steps directly to confirm the pipeline they've written actually works before ever
trusting it to run unattended.
