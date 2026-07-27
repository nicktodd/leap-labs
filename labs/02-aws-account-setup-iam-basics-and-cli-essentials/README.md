# Lab 2 — AWS Account Setup, IAM Basics & CLI Essentials

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. Confirm
`aws --version` reports AWS CLI v2 before starting.

## Task

### Part 1: Confirm your identity

1. Run `aws sts get-caller-identity` (with whatever profile flag your instructor's setup
   requires). Record the account number and your IAM ARN.
2. Run `aws iam list-account-aliases`. Does the account have a human-readable alias, and if so,
   what is it?
3. In the console, check the region selector in the top-right corner. Confirm it matches the
   region your CLI commands default to (`aws configure list`). A mismatch here is a common
   source of "my resource doesn't exist" confusion later this sprint — a bucket or cluster
   created in one region is invisible from another.

### Part 2: Explore what your identity can do

4. Run `aws iam list-attached-user-policies --user-name <your-username>`. What policy is
   attached, and what does that policy's name suggest about its scope?
5. In the console, open IAM → Users → your user → the Permissions tab, and open the attached
   policy's JSON. Find the `Action` and `Resource` fields. What do `"Action": "*"` and
   `"Resource": "*"` mean, read literally?

### Part 3: Run your first real commands

6. List the S3 buckets in the account: `aws s3 ls`. (There are several already — this is a
   shared training account; leave anyone else's buckets alone.)
7. List the VPCs in the account: `aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,Cidr:CidrBlock}'
   --output table`. You'll use this VPC directly in Module 3.
8. List the ECS clusters in the account: `aws ecs list-clusters`. Confirm it returns an empty
   list — nothing has been deployed yet.

## Verify

Compare your Part 1 and Part 2 answers against `solutions/02-.../model-answers.md`. For Part 3,
confirm each command returned real output rather than an error — if any command fails, check
your region flag and credentials before assuming AWS itself is the problem.

## A Question Worth Sitting With

The policy attached to your user is almost certainly `AdministratorAccess` — every action, on
every resource. That's a reasonable choice for a shared training account with a fixed group of
trusted people for one week. Name one concrete reason it would be the wrong choice for the
credential a real ECS task uses in production to talk to RDS, and one concrete reason it would
also be the wrong choice for a CI/CD pipeline's deployment credential (Module 11 builds exactly
this kind of pipeline).
