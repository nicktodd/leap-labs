# Module 2 Demo Guide — AWS Account Setup, IAM Basics & CLI Essentials

**Duration:** 40 minutes
**Prerequisite:** AWS CLI v2 installed (`aws --version`). Console and CLI access confirmed per
your instructor's instructions for this cohort.

## Part 0: Who Am I, According to AWS? (5 min)

The first command anyone should run against a new AWS profile, before anything else:

```bash
aws sts get-caller-identity --profile training --region us-east-1
```

Real output:

```json
{
    "UserId": "AIDASFTGYKIZJPPERX6PH",
    "Account": "149465616946",
    "Arn": "arn:aws:iam::149465616946:user/Nicktodd"
}
```

This confirms three things at once: the credentials are valid, which account they belong to,
and which IAM identity is making the call. `aws iam list-account-aliases` confirms the
human-readable account name:

```json
{"AccountAliases": ["watchelmtraining"]}
```

Worth naming: an AWS account is identified by a 12-digit number, not a name — the alias is a
convenience label, nothing more.

## Part 1: What IAM Actually Controls (10 min)

IAM (Identity and Access Management) answers exactly one question for every single AWS API
call: is this identity allowed to do this action, on this resource? Three building blocks:

- **Users** — a long-lived identity, usually a person (or, less ideally, a shared credential)
- **Roles** — a temporary identity anything can assume (an EC2 instance, an ECS task, another
  AWS account) — Module 7 onward, ECS tasks assume a role rather than using a user's credentials
- **Policies** — JSON documents that grant or deny specific actions on specific resources,
  attached to a user, a role, or a group

Show the real policy attached to this training account's user:

```bash
aws iam list-attached-user-policies --user-name Nicktodd --profile training --region us-east-1
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

## Part 2: A Real Least-Privilege Gotcha, Verified Live (15 min)

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
arn:aws:iam::149465616946:user/leap-demo-readonly is not authorized to perform:
s3:ListAllMyBuckets because no identity-based policy allows the s3:ListAllMyBuckets action
```

The policy granted `s3:ListBucket`, which sounds like it should cover this — but
`aws s3api list-buckets` calls a *different* action, `s3:ListAllMyBuckets` (list every bucket
in the account), which the policy never granted. `s3:ListBucket` only covers listing objects
*inside* a bucket you already know the name of:

```bash
aws s3api list-objects-v2 --bucket nick.todd1 --region us-east-1 --max-items 3
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

## Part 3: CLI Profiles, Not Copy-Pasted Keys (10 min)

```bash
aws configure list --profile training
```

```
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                 training           manual    --profile
access_key     ****************LW74 shared-credentials-file
secret_key     ****************utlh shared-credentials-file
    region                us-east-1      config-file    ~/.aws/config
```

`aws configure list` never prints the full secret key — only the last four characters, even
for the profile actually in use. This is deliberate: a screen-shared terminal or a copy-pasted
support message showing full output never leaks a working credential. Every command this sprint
uses `--profile training --region us-east-1` explicitly, rather than relying on whatever
profile happens to be the shell's current default — the same discipline as never hardcoding a
password in source, applied to a terminal session shared with a room of other people running
their own AWS commands.

## Key Message

Every AWS API call is a yes/no answer from IAM, evaluated against the actual named action being
called, not the action's colloquial description. Getting comfortable running `aws sts
get-caller-identity` and `aws iam simulate-principal-policy`-style checks before assuming a
permission exists saves real debugging time for the rest of this sprint, especially once ECS
task roles (Module 7 onward) replace this account's blanket admin access with something
properly scoped.

## Transition to the Lab

Candidates explore the console and CLI on their own AWS access, confirm their identity and
region, and run their first read-only commands against the account.
