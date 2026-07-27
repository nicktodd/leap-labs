# Lab 3 Model Answers

## Verified Output

Run for real, against the training AWS account (resource IDs shown here are the real,
non-sensitive identifiers this account actually returned — unlike an account number or IAM
username, a VPC/subnet/security-group ID reveals nothing about who owns the account and is safe
to record as-is):

- The account's existing VPC (`vpc-0030f5799ebc2bbee`, CIDR `172.31.0.0/16`) is tagged with a
  CloudFormation StackSet name referencing `AWSControlTowerBP-VPC-ACCOUNT-FACTORY-V1` — it was
  provisioned automatically when this account was created, as part of AWS Control Tower's
  standard account setup, not hand-built.
- That VPC has three subnets, one per AZ (`us-east-1a`, `us-east-1b`, `us-east-1c`), each with
  `MapPublicIpOnLaunch: false`.
- `aws ec2 describe-internet-gateways` for that VPC returns an empty list. Further checks
  (`describe-nat-gateways`, `describe-transit-gateway-attachments`) also return empty — the
  VPC's only non-local route, on every subnet, points to a Gateway VPC Endpoint for S3, not to
  general internet access.
- `leap-mission-vpc` (CIDR `10.42.0.0/16`) has four subnets: two public (`10.42.1.0/24`,
  `10.42.2.0/24`, one per AZ), two private (`10.42.11.0/24`, `10.42.12.0/24`, one per AZ).
- The public subnets' route table has a real `0.0.0.0/0 → igw-...` route, confirmed by
  `describe-route-tables`.
- `leap-app-sg`'s inbound rule on port 8090 has an empty `IpRanges` and a populated
  `UserIdGroupPairs` referencing `leap-web-sg`'s ID directly — not a CIDR block at all.

## Part 1: What Makes a Subnet Public

The CloudFormation StackSet tag means this VPC was created by automation as part of a
standardised account template (AWS Control Tower's "Account Factory") — every new account in an
organisation using Control Tower gets an identical VPC baseline, not something an individual
engineer designed for this specific account.

The correct definition: a subnet is public if and only if its route table sends `0.0.0.0/0` to
an Internet Gateway. `MapPublicIpOnLaunch` only controls whether an instance launched into that
subnet is automatically assigned a public IP address — it has no effect on whether traffic can
actually reach that IP, and a `true` value on a subnet with no Internet Gateway route is
meaningless. By the correct test, **none of the account's existing VPC's three subnets are
public** — none of them have any path to the general internet at all, public IP or not.

## Part 2: The Mission's VPC

`leap-mission-vpc` uses `10.42.0.0/16`, a deliberately different range from the account's
existing `172.31.0.0/16` VPC, so the two networks can never be ambiguous with each other even if
they were ever connected (they are not, in this sprint). The two `leap-public-*` subnets have a
route table with a real `0.0.0.0/0 → igw-...` entry; the two `leap-private-*` subnets' route
tables have only the automatic local route, no internet path at all — genuinely private, by the
same test applied in Part 1.

Of the mission's services: the Application Load Balancer (Module 8) belongs in the public
subnets — it's the one thing meant to be reachable from the internet. The mission-service and
auth-service ECS tasks, and the RDS instance (Module 9), belong in the private subnets — none of
them should be reachable directly from the internet; they're reached only via the load balancer,
which is itself inside the VPC.

## Part 3: Security Groups

`leap-web-sg` allows inbound traffic on 80/443 from `0.0.0.0/0` — any IP address on the
internet, which is correct for a public load balancer's security group. `leap-app-sg` allows
inbound traffic on 8090 only from anything carrying `leap-web-sg` — not from any IP address,
including IPs inside the same VPC that don't have `leap-web-sg` attached. The practical
difference: a CIDR-based rule is a fixed, static allowlist of addresses; a security-group-based
rule dynamically covers whatever resources have that other group attached, now or in the future,
without ever needing to know or update an IP address.

**Only `leap-app-sg` should be allowed to reach a future database security group directly** —
`leap-web-sg` (the load balancer) has no legitimate reason to talk to Postgres at all; it only
ever talks to the mission-service task. Allowing `leap-web-sg` direct database access would mean
the load balancer's security group — the one thing directly exposed to the internet — has a path
straight to the database, defeating the entire point of putting the database in a private subnet
behind an application tier in the first place.

## The Reflection Question

Checking only `MapPublicIpOnLaunch` would have concluded the account's existing VPC's subnets
were private (since it's `false` on all three) — which happens to be the right conclusion here,
but for the wrong reason, and only by coincidence. The real risk is the opposite case: a subnet
with `MapPublicIpOnLaunch: true` but no Internet Gateway route looks "public" by that one
attribute while genuinely having no internet path, and a subnet with `MapPublicIpOnLaunch:
false` but a real `0.0.0.0/0` route to an Internet Gateway is genuinely reachable from the
internet by anything given an explicit public IP, despite "looking" private. Trusting the wrong
signal could lead directly to a real deployment mistake later this sprint: assuming a subnet is
safely private and placing RDS or an ECS task's only network interface there, when the route
table actually gives it a live path to the internet.
