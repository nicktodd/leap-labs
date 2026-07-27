# Module 2 Demo Guide — AWS Account Setup, IAM Basics & CLI Essentials

**Duration:** 45 minutes
**Prerequisite:** AWS CLI v2 installed (`aws --version`). Console and CLI access confirmed per
your instructor's instructions for this cohort.

## Part 0: Regions and Availability Zones (8 min)

Before touching the console or the CLI, establish where things actually run. An AWS Region is
a physical location — a cluster of data centres in one geographic area (`us-east-1`, Northern
Virginia; `eu-west-1`, Ireland). Every resource this sprint creates belongs to exactly one
region unless it's explicitly global (IAM users, for example, are account-wide, not
region-scoped; S3 buckets, ECS clusters, and RDS instances are not).

Each region is made up of multiple, physically separate Availability Zones (AZs) — independent
data centres with their own power and networking, close enough for low-latency connections
between them, far enough apart that one AZ's outage doesn't take down another:

```bash
aws ec2 describe-availability-zones --region us-east-1 \
  --query 'AvailabilityZones[].{Name:ZoneName,State:State}' --output table
```

```
-----------------------------
| DescribeAvailabilityZones |
+-------------+-------------+
|    Name     |    State    |
+-------------+-------------+
|  us-east-1a |  available  |
|  us-east-1b |  available  |
|  us-east-1c |  available  |
|  us-east-1d |  available  |
|  us-east-1e |  available  |
```

This matters directly for Module 3 onward: a subnet lives in exactly one AZ, and RDS's Multi-AZ
option (Module 9) works by keeping a standby database in a *second* AZ specifically so one data
centre going down doesn't take the database with it. "Which region" and "which AZ" are two
different questions this sprint asks repeatedly, not interchangeable ideas.

## Part 1: Accessing AWS via the Console (7 min)

The AWS Management Console is a web UI at `https://console.aws.amazon.com` — sign in, and the
region selector in the top-right corner controls which region's resources the console currently
shows. Walk through it live:

- Signing in (however this cohort's access is provisioned — see your instructor's setup notes)
- The region selector, and what changes when it's switched (a different region shows
  completely different resources — an S3 bucket created in `us-east-1` is invisible from the
  `eu-west-1` view, even in the same account)
- The search bar at the top, for jumping directly to a service (faster than the left-hand
  service menu once you know roughly what you're looking for)

The console is good for exploring, for reading a resource's full configuration, and for the
first few times through a workflow. Everything this sprint automates from Module 11 onward uses
the CLI instead, because a console click can't be scripted or repeated identically twice.

## Part 2: Accessing AWS via the CLI (10 min)

The AWS CLI talks to the same API the console does, from a terminal. The first command to run
against any new profile, before anything else:

```bash
aws sts get-caller-identity --profile training --region us-east-1
```

Illustrative output (account numbers and usernames below are examples, not this account's real
values):

```json
{
    "UserId": "AIDAEXAMPLE123456789",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/alex.morgan"
}
```

This confirms three things at once: the credentials are valid, which account they belong to,
and which IAM identity is making the call.

```bash
aws configure list --profile training
```

```
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                 training           manual    --profile
access_key     ****************ABCD shared-credentials-file
secret_key     ****************WXYZ shared-credentials-file
    region                us-east-1      config-file    ~/.aws/config
```

`aws configure list` never prints the full secret key — only the last four characters, even for
the profile actually in use. This is deliberate: a screen-shared terminal or a copy-pasted
support message showing full output never leaks a working credential. Every command this sprint
uses `--profile training --region us-east-1` explicitly, rather than relying on whatever profile
happens to be the shell's current default — the same discipline as never hardcoding a password
in source, applied to a terminal session shared with a room of other people running their own
AWS commands.

## Part 3: What IAM Actually Controls (8 min)

IAM (Identity and Access Management) answers exactly one question for every single AWS API
call: is this identity allowed to do this action, on this resource? Three building blocks:

- **Users** — a long-lived identity, usually a person (or, less ideally, a shared credential)
- **Roles** — a temporary identity anything can assume (an EC2 instance, an ECS task, another
  AWS account) — Module 7 onward, ECS tasks assume a role rather than using a user's credentials
- **Policies** — JSON documents that grant or deny specific actions on specific resources,
  attached to a user, a role, or a group

Show the policy attached to this training account's user:

```bash
aws iam list-attached-user-policies --user-name alex.morgan --profile training --region us-east-1
```

```json
{
    "AttachedPolicies": [
        {"PolicyName": "AdministratorAccess", "PolicyArn": "arn:aws:iam::aws:policy/AdministratorAccess"}
    ]
}
```

Name this directly: `AdministratorAccess` grants every action on every resource — appropriate
for a shared training account where the alternative is fighting permissions errors all week,
completely inappropriate for a real production deployment credential. This sprint's later ECS
task roles (Module 7 onward) are scoped to exactly what each task needs, not admin.

## Part 4: A Real Least-Privilege Gotcha, Verified Live (12 min)

Rather than describe least privilege abstractly, this demo creates a genuinely restricted IAM
user with a narrow policy, uses it directly, and tears it down immediately afterward.

```bash
aws iam create-user --user-name leap-demo-readonly --profile training --region us-east-1
```

Attach an inline policy granting only `s3:GetObject` and `s3:ListBucket`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {"Effect": "Allow", "Action": ["s3:GetObject", "s3:ListBucket"], "Resource": "*"}
  ]
}
```

```bash
aws iam put-user-policy --user-name leap-demo-readonly --policy-name leap-s3-readonly \
  --policy-document file://leap-s3-readonly.json --profile training --region us-east-1
aws iam create-access-key --user-name leap-demo-readonly --profile training --region us-east-1
```

Using the new user's own credentials directly (not the training profile):

```bash
aws s3api list-buckets --region us-east-1
```

Real output — a genuine, verified surprise:

```
An error occurred (AccessDenied) when calling the ListBuckets operation: User:
arn:aws:iam::123456789012:user/leap-demo-readonly is not authorized to perform:
s3:ListAllMyBuckets because no identity-based policy allows the s3:ListAllMyBuckets action
```

The policy granted `s3:ListBucket`, which sounds like it should cover this — but
`aws s3api list-buckets` calls a *different* action, `s3:ListAllMyBuckets` (list every bucket
in the account), which the policy never granted. `s3:ListBucket` only covers listing objects
*inside* a bucket you already know the name of:

```bash
aws s3api list-objects-v2 --bucket some-existing-bucket --region us-east-1 --max-items 3
```

This succeeds and returns real object keys. The gap between "sounds like listing" and "the
actual IAM action name" is the single most common real-world IAM debugging trap — a policy
that looks obviously correct on read-through, but fails on one specific call because AWS split
what looks like one capability into two separate, separately-grantable actions.

Tear down immediately after the demo:

```bash
aws iam delete-access-key --user-name leap-demo-readonly --access-key-id <AccessKeyId> \
  --profile training --region us-east-1
aws iam delete-user-policy --user-name leap-demo-readonly --policy-name leap-s3-readonly \
  --profile training --region us-east-1
aws iam delete-user --user-name leap-demo-readonly --profile training --region us-east-1
```

## Key Message

Every AWS API call is a yes/no answer from IAM, evaluated against the actual named action being
called, not the action's colloquial description. Getting comfortable confirming identity,
region, and permissions before assuming something exists or is allowed saves real debugging
time for the rest of this sprint, especially once ECS task roles (Module 7 onward) replace this
account's blanket admin access with something properly scoped.

## Transition to the Lab

Candidates explore the console and CLI on their own AWS access, confirm their identity, region,
and Availability Zones, and run their first read-only commands against the account.
