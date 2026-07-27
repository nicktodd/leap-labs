# Lab 2 Model Answers

## Verified Output

Run for real, against the training AWS account:

- `aws sts get-caller-identity`: `Account: 149465616946`, `Arn:
  arn:aws:iam::149465616946:user/Nicktodd`.
- `aws iam list-account-aliases`: `watchelmtraining`.
- `aws iam list-attached-user-policies --user-name Nicktodd`: one attached policy,
  `AdministratorAccess` (`arn:aws:iam::aws:policy/AdministratorAccess`).
- `aws ec2 describe-vpcs`: one VPC, non-default, CIDR `172.31.0.0/16` — this is the VPC Module
  3 explores in detail.
- `aws ecs list-clusters`: `{"clusterArns": []}` — confirmed empty before any deployment work
  begins.

## Part 1: Identity

The account number (`149465616946`) is the account's real, permanent identifier — the alias
(`watchelmtraining`) is a display convenience that can be changed or removed without affecting
anything else; scripts and IAM policies should never rely on the alias, only the account number
or ARNs. Region mismatch between the console's selector and the CLI's default is worth checking
explicitly here because several services in this sprint (S3 buckets are global-ish but bucket
*contents* and most other services are region-scoped) will appear to "not exist" if you're
looking in the wrong region rather than because the resource wasn't created.

## Part 2: Policy Scope

`AdministratorAccess`'s name accurately describes its scope: full access to every AWS service
and action, on every resource in the account, with one narrow, deliberate exception (it cannot
modify AWS's own root-account billing settings). Reading the policy JSON directly:
`"Action": "*"` means "every action this policy statement could possibly apply to," and
`"Resource": "*"` means "every resource in the account, of every type" — read literally, this
single two-field statement is the entire policy; there's no further narrowing anywhere else in
the document.

## The Reflection Question

**Why `AdministratorAccess` is the wrong choice for an ECS task's production credential**: a
task role scoped to admin means any bug, dependency vulnerability, or successful exploit in
`mission-service` itself — a single vulnerable library, one bad input-validation gap — grants an
attacker the same power as a full account administrator, not just access to the one RDS
database and the few other resources that task actually needs. Module 7's task roles are scoped
narrowly for exactly this reason: the blast radius of a compromised container should be limited
to what that container legitimately needs.

**Why it's also wrong for a CI/CD deployment credential**: a pipeline credential with admin
access means a single leaked secret (checked into a public repo by mistake, exposed in a build
log, or extracted from a compromised CI runner) is a full account takeover, not "an attacker can
redeploy the frontend." Module 11's deployment scripts should use a credential scoped to exactly
the handful of actions a deploy needs — pushing to a specific ECR repository, updating a
specific ECS service, syncing a specific S3 bucket, invalidating a specific CloudFront
distribution — nothing else.
