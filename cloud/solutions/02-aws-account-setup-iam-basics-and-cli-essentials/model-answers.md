# Lab 2 Model Answers

## Verified Output

Run for real, against the training AWS account (account number and username shown here are
illustrative examples, not the real values, to keep this document safe to share outside the
training environment):

- `aws ec2 describe-availability-zones --region us-east-1`: five AZs (`us-east-1a` through
  `us-east-1e`), all `available`.
- `aws sts get-caller-identity`: an account number and an IAM ARN of the form
  `arn:aws:iam::<account-id>:user/<username>`.
- `aws configure list`: active profile, active region, and both keys masked to their last four
  characters only.
- `aws iam list-attached-user-policies`: one attached policy, `AdministratorAccess`
  (`arn:aws:iam::aws:policy/AdministratorAccess`).
- `aws ec2 describe-vpcs`: one VPC, non-default, CIDR `172.31.0.0/16` - this is the VPC Module
  3 explores in detail.
- `aws ecs list-clusters`: `{"clusterArns": []}` - confirmed empty before any deployment work
  begins.

## Part 1: What Is AWS, and Where Does It Run?

AWS is better described as a collection of independent services than as one product because
each service - S3, EC2, RDS, and the several hundred others - does one specific job, is called
through its own API, and has its own separately-controlled set of permissions. There's no single
"AWS" action; there's `s3:GetObject`, `ec2:RunInstances`, `rds:CreateDBInstance`, each a
distinct, separately-grantable capability belonging to a distinct service.

Switching the console's region selector changes every resource list shown - an S3 bucket, VPC,
or ECS cluster visible in one region simply doesn't appear when a different region is selected,
even though it's the same account. This isn't a permissions issue; the resource genuinely lives
in only one region (with the exception of a handful of account-wide services like IAM).

AWS splits each region into several Availability Zones rather than building one large data
centre per region because a single data centre can lose power, lose network connectivity, or
suffer a hardware failure - concentrating everything in one building means that one failure
takes down the entire region. Multiple, physically separate AZs mean a failure in one doesn't
affect the others, while still being close enough to each other for low-latency connections
between them.

A region is a geographic area; an Availability Zone is one of those several physically separate
data centres within that region, each with independent power and networking. A database cares
about which AZ specifically because RDS's Multi-AZ option (Module 9) keeps a live standby copy
in a *second*, physically separate AZ - if the primary AZ has a power or network outage, the
standby in the other AZ is unaffected and can take over. Two resources in the same region but
different AZs are still close enough for low-latency replication between them.

## Part 2 & 3: Console and CLI Identity

The account number is the account's real, permanent identifier - an account alias (if set) is a
display convenience that can be changed or removed without affecting anything else; scripts and
IAM policies should never rely on an alias, only account numbers or ARNs. Region mismatch
between the console's selector and the CLI's default is worth checking explicitly, because
several services this week uses are region-scoped and will appear to "not exist" if you're
looking in the wrong region rather than because the resource wasn't created.

## Part 4: IAM's Building Blocks and Policy Scope

Of IAM's four building blocks, **only the policy actually contains any permissions**. A user, a
group, and a role are all just different ways of attaching a policy to something: a policy
attached to a user affects only that user; a policy attached to a group affects every current
and future member of that group; a role has no permanent credentials of its own at all -
something else (an ECS task, an EC2 instance) assumes it temporarily and inherits whatever
policies are attached to it for the duration.

`AdministratorAccess`'s name accurately describes its scope: full access to every AWS service
and action, on every resource in the account, with one narrow, deliberate exception (it cannot
modify AWS's own root-account billing settings). Reading the policy JSON directly:
`"Action": "*"` means "every action this policy statement could possibly apply to," and
`"Resource": "*"` means "every resource in the account, of every type" - read literally, this
single two-field statement is the entire policy; there's no further narrowing anywhere else in
the document.

If your user belongs to a group, that group may carry its own attached policies, separate from
anything attached to the user directly - a user's total effective permissions are the union of
everything attached to it directly *and* everything attached to every group it belongs to, not
just whichever one you happened to check first.

## The Reflection Question

**Why `AdministratorAccess` is the wrong choice for an ECS task's production credential**: a
task role scoped to admin means any bug, dependency vulnerability, or successful exploit in
`mission-service` itself - a single vulnerable library, one bad input-validation gap - grants an
attacker the same power as a full account administrator, not just access to the one RDS
database and the few other resources that task actually needs. Module 7's task roles are scoped
narrowly for exactly this reason: the blast radius of a compromised container should be limited
to what that container legitimately needs.

**Why it's also wrong for a CI/CD deployment credential**: a pipeline credential with admin
access means a single leaked secret (checked into a public repo by mistake, exposed in a build
log, or extracted from a compromised CI runner) is a full account takeover, not "an attacker can
redeploy the frontend." Module 11's deployment scripts should use a credential scoped to exactly
the handful of actions a deploy needs - pushing to a specific ECR repository, updating a
specific ECS service, syncing a specific S3 bucket, invalidating a specific CloudFront
distribution - nothing else.
