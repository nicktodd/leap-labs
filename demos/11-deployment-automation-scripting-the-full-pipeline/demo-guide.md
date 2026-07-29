# Module 11 Demo Guide — Deployment Automation: Scripting the Full Pipeline

**Duration:** 55 minutes
**Prerequisite:** Module 6's ECR repository, Module 7's cluster and execution role, Module 9's
task definition history, all still in place.

## Part 0: What's Being Automated (5 min)

Every module since Module 6 has run the same sequence of commands by hand: build an image, push
it to ECR, register a task definition, run or deploy it. A real pipeline runs that same sequence
automatically, triggered by a `git push` — GitHub Actions is this module's choice of tool, but the
sequence itself (build, push, deploy, verify) is the same regardless of which CI/CD product runs
it.

## Part 1: Authenticating Without Secrets — OIDC (15 min)

A pipeline needs AWS credentials, and the worst way to provide them is a long-lived access key
pasted into a repository secret — it doesn't expire on its own, and if it leaks, it's valid until
someone notices and rotates it. GitHub Actions supports **OpenID Connect (OIDC)** instead: GitHub
issues each workflow run a short-lived, cryptographically signed token, and AWS is configured to
trust that token directly — no stored AWS credentials anywhere in GitHub at all.

Two real AWS resources make this work. First, an OIDC identity provider, telling AWS to trust
tokens issued by GitHub:

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 1c58a3a8518e8759bf075b76b750d4f2df264fcd
```

Second, an IAM role GitHub Actions assumes, with a trust policy scoped to one specific repository
and branch — not "any GitHub Actions run anywhere":

```json
{
  "Effect": "Allow",
  "Principal": {"Federated": "arn:aws:iam::<account-id>:oidc-provider/token.actions.githubusercontent.com"},
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {"token.actions.githubusercontent.com:aud": "sts.amazonaws.com"},
    "StringLike": {"token.actions.githubusercontent.com:sub": "repo:<org>/leap-sprint11:ref:refs/heads/main"}
  }
}
```

The role's own permissions are scoped just as tightly: push to one named ECR repository, register
task definitions and update one named ECS service, and `iam:PassRole` on the execution role
only — verified directly:

```bash
aws iam get-role-policy --role-name leap-github-actions-deploy-role \
  --policy-name leap-github-actions-deploy-policy --query 'PolicyDocument.Statement[].Sid'
["ECRAuth", "ECRPush", "ECSDeploy", "PassExecutionRoleOnly"]
```

## Part 2: The Pipeline's Steps, Run Directly (15 min)

Every step the workflow (`deploy.yml.example`) would run, executed directly to confirm each one
actually works:

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker build -t <account>.dkr.ecr.us-east-1.amazonaws.com/leap-mission-service:<sha>-ci .
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/leap-mission-service:<sha>-ci
```

Real output: a genuine digest from ECR, confirming the push succeeded.

## Part 3: A Real Failure — Cloning a Stale Task Definition (10 min)

The first deploy attempt copied the *previous* task definition (Module 9's revision 3) and only
swapped its image — the same shortcut it's tempting to script. Running it produced a real
failure:

```
ResourceInitializationError: unable to pull secrets or registry auth ...
AccessDeniedException: ... is not authorized to perform: secretsmanager:GetSecretValue
on resource: arn:aws:secretsmanager:...rds!db-...
```

Revision 3 referenced Module 9's RDS secret — which was deleted, along with the execution role's
permission to read it, when Module 9 was torn down. Cloning an old revision cloned that stale
reference too. This is exactly why the workflow example uses
`aws-actions/amazon-ecs-render-task-definition`, which starts from the **current live** task
definition and only swaps the image field — not a local copy that might be out of date, or worse,
reference something that no longer exists.

The fix: build a clean task definition from the base template (image, ports, log configuration —
no stale `secrets` block) and register that instead:

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
sequence this sprint has run by hand since Module 6, made to run automatically and
authenticate without ever storing a credential. The one genuinely new risk automation
introduces is exactly what today's real failure demonstrated: a script that blindly clones the
last task definition can silently carry forward something that's since been deleted. Building
from the current live definition, or a clean template, avoids it.

## Transition to the Lab

Candidates set up their own OIDC provider and scoped role, write their own workflow file, and run
each of its steps directly to confirm the pipeline they've written actually works before ever
trusting it to run unattended.
