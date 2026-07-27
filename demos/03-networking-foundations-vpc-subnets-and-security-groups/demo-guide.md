# Module 3 Demo Guide — Networking Foundations: VPC, Subnets & Security Groups

**Duration:** 50 minutes
**Prerequisite:** Module 2's identity and CLI setup. No new tooling.

## Part 0: What a VPC Actually Is (5 min)

A VPC (Virtual Private Cloud) is itself one of the AWS services from Module 2's "AWS is a
collection of services" framing — its job is to give an account its own private, isolated
network inside AWS, with an IP address range nothing outside it can reach directly. Everything
this module covers — subnets, route tables, security groups — is a way of dividing up and
controlling traffic within that one private network.

Every VPC has a CIDR block (a range of IP addresses, written like `10.42.0.0/16`) — this is the
whole private address space that VPC owns. Nothing about a VPC is public by default; a VPC on
its own, with nothing else configured, cannot reach the internet and cannot be reached from it.

## Part 1: Exploring the Account's Existing VPC (10 min)

Before creating anything, look at what's already here:

```bash
aws ec2 describe-vpcs --profile training --region us-east-1 \
  --query 'Vpcs[].{Id:VpcId,Cidr:CidrBlock,Tags:Tags}'
```

Real output shows one VPC, CIDR `172.31.0.0/16`, tagged with a CloudFormation StackSet name
referencing `AWSControlTowerBP-VPC-ACCOUNT-FACTORY` — this VPC wasn't hand-built; it was
provisioned automatically by AWS Control Tower, the service many organisations (Fidelity
included, per the mission brief) use to standardise how every AWS account in a company is set
up. It has three subnets, one per Availability Zone:

```bash
aws ec2 describe-subnets --profile training --region us-east-1 \
  --query 'Subnets[].{Id:SubnetId,AZ:AvailabilityZone,CIDR:CidrBlock,Public:MapPublicIpOnLaunch}' \
  --output table
```

```
+------------+------------------+-----------------+---------------------------+----------+
|     AZ     |        Id        |      CIDR       |            Id             | Public   |
+------------+------------------+-----------------+---------------------------+----------+
|  us-east-1a| subnet-051d...   |  172.31.64.0/20 |  ...                      |  False   |
|  us-east-1b| subnet-01ed...   |  172.31.32.0/20 |  ...                      |  False   |
|  us-east-1c| subnet-01fd...   |  172.31.80.0/20 |  ...                      |  False   |
+------------+------------------+-----------------+---------------------------+----------+
```

Ask the room to guess: are these public or private subnets? Before answering, define the term
properly — see Part 2.

## Part 2: What Actually Makes a Subnet "Public" (10 min)

A subnet is a slice of a VPC's address range, pinned to exactly one Availability Zone (this is
the AZ-scoping Module 2 flagged as a real, deliberate decision, not an implementation detail).
`MapPublicIpOnLaunch` (whether a launched instance gets a public IP automatically) is *not* what
makes a subnet public — the real test is its route table: a subnet is public if and only if its
route table sends `0.0.0.0/0` (all traffic with no more specific match) to an Internet Gateway.

Check the existing account VPC for an Internet Gateway:

```bash
aws ec2 describe-internet-gateways --profile training --region us-east-1
```

Real output — a genuine, verified surprise: `{"InternetGateways": []}`. This VPC has no
Internet Gateway at all. Checking further confirms no NAT Gateway and no Transit Gateway
attachment either — the only non-local route in any of its route tables points to a VPC
Endpoint for S3. **None of the three subnets shown above are actually public, by the only test
that matters** — and none of them have any path to the general internet whatsoever, despite
looking like a normal three-AZ subnet layout.

This is exactly the kind of Fidelity-specific guardrail the mission brief flags: a real
landing-zone account, provisioned by a central platform team, deliberately locked down in a way
a generic AWS tutorial wouldn't show. Name it directly: **we will not modify this VPC.** It's
owned by a CloudFormation StackSet: hand-editing it fights the automation that manages it, and
in a real organisation, doing this to a landing-zone account is exactly the kind of change that
gets a platform team paged.

## Part 3: Building the Mission's Own VPC (15 min)

Instead, create a small, dedicated VPC for the mission's deployment work — one with a real,
working Internet Gateway, built deliberately rather than inherited:

```bash
aws ec2 create-vpc --cidr-block 10.42.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=leap-mission-vpc}]'
```

A different CIDR range (`10.42.0.0/16` vs the account VPC's `172.31.0.0/16`) avoids any
ambiguity between the two networks. Then, in order:

1. An Internet Gateway, created and attached to the new VPC.
2. Two **public** subnets, one per AZ (`10.42.1.0/24` in `us-east-1a`, `10.42.2.0/24` in
   `us-east-1b`) — `us-east-1` was Module 2's chosen region.
3. Two **private** subnets, one per AZ (`10.42.11.0/24`, `10.42.12.0/24`) — no internet route at
   all, for now. Module 7 onward, ECS tasks and the RDS instance (Module 9) live here.
4. A route table with a `0.0.0.0/0 → Internet Gateway` route, associated with both public
   subnets only.

Verify the public route table for real:

```bash
aws ec2 describe-route-tables --route-table-ids <rtb-id> --profile training --region us-east-1 \
  --query 'RouteTables[0].Routes'
```

```json
[
  {"DestinationCidrBlock": "10.42.0.0/16", "GatewayId": "local", "State": "active"},
  {"DestinationCidrBlock": "0.0.0.0/0", "GatewayId": "igw-...", "State": "active"}
]
```

This time, the definition from Part 2 is genuinely satisfied: `0.0.0.0/0` really does point at
an Internet Gateway. **A VPC, its subnets, an Internet Gateway, and a route table cost nothing**
— unlike a NAT Gateway, an ECS task, or an RDS instance, none of which exist yet, none of these
resources bill by the hour. This VPC is deliberately left in place after this module, rather
than torn down — Module 7 onward reuses it exactly as built here.

## Part 4: Security Groups — Access Control at the Network Level (10 min)

A security group is a stateful virtual firewall attached to a resource (an ECS task, a load
balancer, an RDS instance) — it doesn't route traffic, it decides whether traffic reaching that
resource is allowed at all. Build two, demonstrating a real least-privilege pattern:

```bash
aws ec2 create-security-group --group-name leap-web-sg \
  --description "leap: public web/ALB traffic" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <web-sg-id> \
  --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id <web-sg-id> \
  --protocol tcp --port 443 --cidr 0.0.0.0/0
```

`leap-web-sg` is deliberately open on 80/443 to `0.0.0.0/0` — this is what a public load
balancer's security group is supposed to allow, since anyone on the internet is meant to reach
it (Module 8).

```bash
aws ec2 create-security-group --group-name leap-app-sg \
  --description "leap: mission-service, reachable only from leap-web-sg" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <app-sg-id> \
  --protocol tcp --port 8090 --source-group <web-sg-id>
```

The key difference: `leap-app-sg`'s rule references *another security group*, not a CIDR block.
Verified directly:

```bash
aws ec2 describe-security-groups --group-ids <app-sg-id> \
  --query 'SecurityGroups[0].IpPermissions'
```

```json
[
  {
    "IpProtocol": "tcp", "FromPort": 8090, "ToPort": 8090,
    "UserIdGroupPairs": [{"GroupId": "sg-...web..."}],
    "IpRanges": []
  }
]
```

`IpRanges` is empty; `UserIdGroupPairs` names `leap-web-sg` specifically. This means port 8090
is reachable only from something that has `leap-web-sg` attached — not from any IP address, not
even from inside the VPC, unless it's specifically coming from a resource carrying that other
security group. This is the mechanism Module 8's load balancer and ECS task use directly: the
ALB carries `leap-web-sg`, the mission-service task carries `leap-app-sg`, and the task is
reachable from the ALB and nothing else.

## Key Message

"Public" and "private" are not labels anyone sets directly — they're the *result* of a route
table's configuration, specifically whether `0.0.0.0/0` reaches an Internet Gateway. A subnet
that looks public (has spare IP addresses, sits in a normal-looking VPC) can have no internet
path at all, and the only way to know for certain is to check the route table, not guess from
appearances — exactly what this module's first real surprise demonstrated.

## Transition to the Lab

Candidates explore the account's existing Control Tower VPC read-only, confirm for themselves
that it has no Internet Gateway, and identify which of the mission's leap-mission-vpc subnets
and security groups each of the mission's services will use from Module 7 onward.
