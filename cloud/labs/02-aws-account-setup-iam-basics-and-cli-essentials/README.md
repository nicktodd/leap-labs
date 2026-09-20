# Lab 2 - AWS Account Setup, IAM Basics & CLI Essentials

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. Confirm
`aws --version` reports AWS CLI v2 before starting.

## Task

### Part 1: What is AWS, and where does it run?

1. In your own words: why is AWS better described as "a collection of independent services"
   than as one product? Name three services from today's demo and the one job each does.
2. In the console, note the region shown in the top-right selector. Switch it to a different
   region and observe what happens to the resource lists you were just looking at.
3. Before running anything, write down: why does AWS split a region into multiple Availability
   Zones, rather than one big data centre per region?
4. Run `aws ec2 describe-availability-zones --region <your-region>
   --query 'AvailabilityZones[].{Name:ZoneName,State:State}' --output table`. How many AZs does
   this region have, and are they all `available`?
5. In your own words: what's the difference between "which region" and "which Availability
   Zone," and why would a database care about the second one specifically (you'll meet this
   again directly in Module 9)?

### Part 2: Explore the console

6. Sign in to the AWS console. Find the search bar at the top and use it to jump directly to
   the S3, EC2, and IAM services, rather than using the left-hand menu.
7. Open the IAM service and find your own user. Note its ARN.

### Part 3: Confirm CLI access

8. Run `aws sts get-caller-identity`. Record the account number and your IAM ARN, and confirm
   they match what the console showed in Part 2.
9. Run `aws configure list`. Confirm it shows your active profile and region, and that the
   access key and secret key are both masked to their last four characters only.
10. Confirm the CLI's default region matches the console's region selector from Part 1 - a
    mismatch here is a common source of "my resource doesn't exist" confusion later this week.

### Part 4: Explore what your identity can do

11. IAM has four building blocks: users, groups, roles, and policies. In your own words, what
    is the *only* one of the four that actually contains any permissions - and what do the
    other three do instead?
12. Run `aws iam list-attached-user-policies --user-name <your-username>`. What policy is
    attached, and what does that policy's name suggest about its scope?
13. In the console, open IAM → Users → your user → the Permissions tab, and open the attached
    policy's JSON. Find the `Action` and `Resource` fields. What do `"Action": "*"` and
    `"Resource": "*"` mean, read literally?
14. Still in the console, check whether your user belongs to any IAM Groups. If it does, does
    the group have any policies attached, separately from the ones attached to your user
    directly?

### Part 5: Run your first real commands

15. List the S3 buckets in the account: `aws s3 ls`. (There are several already - this is a
    shared training account; leave anyone else's buckets alone.)
16. List the VPCs in the account: `aws ec2 describe-vpcs --query
    'Vpcs[].{Id:VpcId,Cidr:CidrBlock}' --output table`. You'll use this VPC directly in Module 3.
17. List the ECS clusters in the account: `aws ecs list-clusters`. Confirm it returns an empty
    list - nothing has been deployed yet.

## Verify

Compare your Part 1, 3, and 4 answers against `solutions/02-.../model-answers.md`. For Part 5,
confirm each command returned real output rather than an error - if any command fails, check
your region flag and credentials before assuming AWS itself is the problem.

## A Question Worth Sitting With

The policy attached to your user is almost certainly `AdministratorAccess` - every action, on
every resource. That's a reasonable choice for a shared training account with a fixed group of
trusted people for one week. Name one concrete reason it would be the wrong choice for the
credential a real ECS task uses in production to talk to RDS, and one concrete reason it would
also be the wrong choice for a CI/CD pipeline's deployment credential (Module 11 builds exactly
this kind of pipeline).
