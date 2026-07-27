# Lab 3 — Networking Foundations: VPC, Subnets & Security Groups

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. No new
tooling — this lab is entirely exploration and CLI commands against resources your instructor
has already provisioned (`leap-mission-vpc`) or that already exist in the account.

## Task

### Part 1: Explore the account's existing VPC

1. Run `aws ec2 describe-vpcs` and find the VPC that is **not** `leap-mission-vpc`. Look at its
   tags — what does the CloudFormation StackSet name in its tags tell you about how it was
   created?
2. List that VPC's subnets with `aws ec2 describe-subnets --filters
   Name=vpc-id,Values=<vpc-id>`. How many are there, and which Availability Zone is each one in?
3. Before running anything else, write down your own definition: what specifically makes a
   subnet "public," as opposed to just having spare IP addresses or looking normal?
4. Run `aws ec2 describe-internet-gateways` and check whether one is attached to this VPC. Based
   on your Part 1.3 definition, are any of this VPC's subnets actually public?

### Part 2: Explore the mission's own VPC

5. Find `leap-mission-vpc` with `aws ec2 describe-vpcs --filters Name=tag:Name,Values=leap-mission-vpc`.
   What CIDR block does it use, and how does that compare to the account's existing VPC from
   Part 1?
6. List its subnets. You should find four: two tagged `leap-public-*`, two tagged
   `leap-private-*`. For each one, check its associated route table
   (`aws ec2 describe-route-tables --filters Name=association.subnet-id,Values=<subnet-id>`) and
   confirm for yourself, from the routes, which two are genuinely public and which two are not.
7. Which of the mission's services (from Module 1's architecture map) belongs in a public
   subnet, and which belong in a private one? Justify each answer — don't just guess based on
   the name.

### Part 3: Security groups

8. Find `leap-web-sg` and `leap-app-sg` in the mission's VPC
   (`aws ec2 describe-security-groups --filters Name=vpc-id,Values=<mission-vpc-id>`).
9. For each one, run `aws ec2 describe-security-groups --group-ids <id> --query
   'SecurityGroups[0].IpPermissions'` and compare the two. One references a CIDR block; the
   other references a security group ID. What's the practical difference in what each one
   actually allows?
10. If a third security group existed for the mission's database (Module 9 builds this for
    real), which of `leap-web-sg` or `leap-app-sg` should be allowed to reach it directly, and
    why should the answer definitely not be "anything in `leap-web-sg`"?

## Verify

Compare your answers against `solutions/03-.../model-answers.md`. For the route table checks in
Part 2, make sure your conclusion is based on the actual routes returned, not an assumption from
the subnet's name or tag.

## A Question Worth Sitting With

The account's existing Control Tower VPC has real, valid-looking subnets across three
Availability Zones, with spare IP addresses available in each — everything a subnet "should"
have, except a path to the internet. If you only checked `MapPublicIpOnLaunch` and never checked
the route table, what wrong conclusion would you have reached, and what real deployment mistake
could that wrong conclusion lead to later this sprint?
