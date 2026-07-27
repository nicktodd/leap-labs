# Lab 3 — Networking Foundations: VPC, Subnets & Security Groups

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. No new
tooling. Your account may already have a default VPC, one provisioned by a landing-zone tool
like AWS Control Tower, or nothing at all — the steps below work regardless of which.

## Task

### Part 1: CIDR notation, worked by hand

1. Without running anything, work out by hand: how many IP addresses does a `/24` CIDR block
   contain? How many does a `/16` contain? Which one is bigger, and why does a *smaller* number
   after the slash mean a *bigger* address range?
2. `10.0.4.0/24` and `10.0.5.0/24` — are these two ranges overlapping, or completely separate?
   Justify your answer from the CIDR notation itself, not a guess.

### Part 2: Explore whatever VPC(s) already exist in your account

3. Run `aws ec2 describe-vpcs`. Do you have any VPCs already? If so, note each one's CIDR block
   and check its tags — was it created by an automation tool (a CloudFormation stack, a
   Control-Tower-style tag), or does it look hand-built?
4. For any VPC you found, list its subnets (`aws ec2 describe-subnets --filters
   Name=vpc-id,Values=<vpc-id>`) and, for each one, check its route table
   (`aws ec2 describe-route-tables --filters Name=association.subnet-id,Values=<subnet-id>`).
   Using only the route table — not the subnet's name, tags, or `MapPublicIpOnLaunch` — decide
   which subnets are genuinely public and which are not.

### Part 3: Build a VPC from scratch, one layer at a time

Build this yourself, matching today's four-layer demo exactly:

5. Create a new VPC with a CIDR block of your choice (avoid clashing with anything from Part 2).
   Confirm it exists with `describe-vpcs` before moving on.
6. Add four subnets: two in one Availability Zone's pair (one meant to be public, one meant to be
   private) and two in a second AZ, following the same public/private split. Use `/24` blocks
   carved from your VPC's range.
7. Create and attach an Internet Gateway to your VPC. Confirm the attachment with
   `describe-internet-gateways` before moving on — don't assume the attach command alone proves
   it worked.
8. Create a route table with a `0.0.0.0/0 → <your Internet Gateway>` route, and associate it with
   only the two subnets you intend to be public. Leave the other two subnets on the VPC's default
   route table (local-only, no internet path).
9. Verify, using only route tables (the same test as Part 2), that exactly two of your four
   subnets are genuinely public and two are genuinely private.

### Part 4: Security groups

10. Create two security groups in your new VPC: one open on port 80 to `0.0.0.0/0`, and a second
    that allows a port of your choice only from the first security group (not from a CIDR).
11. Run `describe-security-groups` on the second one and confirm its rule's `IpRanges` is empty
    and `UserIdGroupPairs` references the first security group's ID.
12. If you were adding a third security group for a database, which of your two existing groups
    should be allowed to reach it, and why should the answer definitely not be "the one open to
    `0.0.0.0/0`"?

## Verify

Compare your Part 1 and Part 4 reasoning against `solutions/03-.../model-answers.md`. For Parts
2 and 3, there's no single expected answer — what matters is that your conclusions are drawn
from the actual route tables you queried, not an assumption about what a subnet "should" be.

## A Question Worth Sitting With

Imagine a subnet in your account has `MapPublicIpOnLaunch: true` but, when you check its route
table, `0.0.0.0/0` has no route to an Internet Gateway at all. Is that subnet public or private?
What would go wrong if you trusted `MapPublicIpOnLaunch` instead of checking the route table
directly, and placed something sensitive there believing it was private?
