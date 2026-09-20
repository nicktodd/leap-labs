# Lab 3 Model Answers

## Part 1: CIDR Notation

A `/24` fixes the first 24 bits of the address, leaving 8 bits free: `2^8 = 256` addresses. A
`/16` fixes only the first 16 bits, leaving 16 bits free: `2^16 = 65,536` addresses. The `/16`
range is bigger, because *fewer* fixed bits means *more* possible combinations in the free bits
- the number after the slash counts fixed bits, not the size of the range, which is why a
smaller number produces a larger range. (In practice, subtract 5 reserved addresses from any
AWS subnet's usable count - a `/24` subnet has 251 usable addresses, not 256.)

`10.0.4.0/24` covers `10.0.4.0` through `10.0.4.255`; `10.0.5.0/24` covers `10.0.5.0` through
`10.0.5.255`. These are completely separate, non-overlapping ranges - the third number (`4` vs
`5`) is part of each range's fixed network portion, so the two blocks share no addresses at all.

## Part 2 & 3: Verified Output (Illustrative)

The exact resources found here depend entirely on your own account - there is no single correct
answer to compare against. As a real, verified example from one account explored during course
preparation, worth checking your own findings against the same *method*, not the same result:

- That account had one pre-existing VPC (CIDR `172.31.0.0/16`), tagged with a CloudFormation
  StackSet name referencing an AWS Control Tower account-factory template - provisioned
  automatically when the account was created, not hand-built.
- It had three subnets, one per Availability Zone, all with `MapPublicIpOnLaunch: false`.
- `aws ec2 describe-internet-gateways` for that VPC returned an empty list - no Internet Gateway
  anywhere in the account. Further checks found no NAT Gateway and no Transit Gateway attachment
  either; the only non-local route on any subnet pointed at a Gateway VPC Endpoint for S3.
- **By the correct test (a `0.0.0.0/0` route to an Internet Gateway), none of that account's
  three subnets were actually public** - despite having spare IP addresses and looking like a
  normal three-AZ layout.

Whatever your own account contains, the method is the same: read the route table directly for
each subnet, and judge "public" or "private" from that alone.

For the hand-built VPC in Part 3, a correctly-built version should show: two subnets whose
associated route table contains a `0.0.0.0/0` route pointing at your Internet Gateway (genuinely
public), and two subnets on the VPC's default route table with only the automatic `local` route
(genuinely private, no internet path at all).

## Part 4: Security Groups

A security group rule with a populated `IpRanges` field is a fixed, static allowlist of IP
addresses. A rule with a populated `UserIdGroupPairs` field and empty `IpRanges` instead
dynamically covers whatever resources currently have that *other* security group attached - the
rule doesn't name any IP address at all, so it automatically covers new resources that get the
referenced group attached later, without ever needing an update.

**Only the second security group (the one restricted to the first group, not the one open to
`0.0.0.0/0`) should be allowed to reach a database's security group.** The group open on port 80
to `0.0.0.0/0` represents the one thing directly exposed to the internet - allowing it a direct
path to the database would mean anyone on the internet is one hop away from the data tier,
defeating the entire purpose of putting a database behind an application tier and a private
subnet in the first place.

## Part 5: A Private Subnet That Still Needs Out

A NAT Gateway, added to a *public* subnet (it needs its own route to the internet via the
Internet Gateway to work at all), with its own Elastic IP. The change goes on the **private**
route table, not the public one: add a `0.0.0.0/0 -> <NAT Gateway>` route alongside the existing
`local` route. The public route table is untouched - it already reaches the internet directly via
the Internet Gateway, and public subnets have no need for a NAT Gateway. This is exactly the
route table change Module 8 makes live, immediately before deploying an ECS service into these
same private subnets.

**NAT Gateway vs PrivateLink:** a NAT Gateway gives a private subnet a path to the internet in
general - ECR included, but so is anything else out there, and the traffic genuinely travels the
internet path even between two AWS services in the same region. PrivateLink (VPC Interface
Endpoints) gives a direct, private connection to one specific AWS service over AWS's own
network, with no internet route involved - narrower, since it only covers whichever services you
provision an endpoint for, but tighter, since nothing travels the public internet at all. A
private subnet that only ever needs to reach ECR and CloudWatch Logs could use PrivateLink alone
and never need a NAT Gateway; a private subnet that also needs to call an external third-party
API would still need one, or need PrivateLink for the AWS-service traffic and a NAT Gateway for
everything else. Which is cheaper depends on the number of endpoints required versus the data
volume moved - covered properly in Module 10.

## The Reflection Question

A subnet with `MapPublicIpOnLaunch: true` but no `0.0.0.0/0` route to an Internet Gateway is
**private**, by the only test that actually matters - `MapPublicIpOnLaunch` only controls
whether AWS *assigns* a public IP address automatically to something launched there; it says
nothing about whether traffic can actually reach that address, because without an Internet
Gateway route, nothing outside the VPC can route to it regardless of what IP it has.

Trusting `MapPublicIpOnLaunch` instead of the route table is dangerous in the *opposite*
direction from what it looks like at first: a subnet that "looks public" (flag set to true) but
has no real route is merely wasted effort, not a security problem. The genuinely dangerous case
is the reverse - a subnet with `MapPublicIpOnLaunch: false` (looking reassuringly private) that
*does* have a real `0.0.0.0/0 → Internet Gateway` route in its table is actually reachable from
the internet by anything given an explicit public IP, despite every surface signal suggesting
otherwise. Placing a database or an internal service there while believing it was private, based
on the flag alone, would leave it genuinely exposed.
