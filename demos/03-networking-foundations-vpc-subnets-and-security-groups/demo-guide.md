# Module 3 Demo Guide — Networking Foundations: VPC, Subnets & Security Groups

**Duration:** 50 minutes
**Prerequisite:** Module 2's identity and CLI setup. No new tooling.

**A note on accounts:** this guide's real, verified command output comes from exploring one
particular AWS account during preparation. Your own account will very likely look different —
it might have a default VPC, a Control-Tower-provisioned one, or no VPC at all yet. Don't expect
candidates to see the exact resources shown here; the concepts and the commands to check them
are what carries over, not the specific IDs or CIDR blocks.

## Part 0: What a VPC Actually Is (5 min)

A VPC (Virtual Private Cloud) is itself one of the AWS services from Module 2's "AWS is a
collection of services" framing — its job is to give an account its own private, isolated
network inside AWS, with an IP address range nothing outside it can reach directly. Everything
this module covers — subnets, route tables, security groups — is a way of dividing up and
controlling traffic within that one private network.

Nothing about a VPC is public by default; a VPC on its own, with nothing else configured, cannot
reach the internet and cannot be reached from it.

## Part 1: CIDR Notation, Properly Explained (10 min)

Every VPC and every subnet is defined by a CIDR block (Classless Inter-Domain Routing) — don't
assume this notation is already familiar; walk through it explicitly before using it again.

An IPv4 address is four numbers 0-255, written like `10.42.1.7`. A CIDR block adds a slash and a
number — `10.42.0.0/16` — where the number after the slash says how many of the address's 32
bits are fixed (the "network" part) and how many are free to vary (the "host" part):

- `/16` fixes the first 16 bits (`10.42`), leaving 16 bits free — `2^16 = 65,536` possible
  addresses, from `10.42.0.0` to `10.42.255.255`
- `/24` fixes the first 24 bits (`10.42.1`), leaving 8 bits free — `2^8 = 256` possible
  addresses, from `10.42.1.0` to `10.42.1.255`
- A smaller number after the slash means a *bigger* range (fewer fixed bits, more free bits) — a
  common point of confusion worth naming directly

This is exactly how a VPC and its subnets relate: a VPC might be given a `/16` (65,536
addresses), and each subnet carved out of it takes a smaller slice — a `/24` (256 addresses) is
a common subnet size, small enough that several can fit inside one `/16` VPC with room to spare.
AWS reserves five addresses in every subnet for its own use (the network address, the router,
DNS, future use, and the broadcast address), so a `/24` subnet actually has 251 usable addresses,
not 256 — worth mentioning so nobody is surprised later by a subnet that looks "one address
short."

## Part 2: Building Up a VPC, One Layer at a Time (20 min)

Rather than jump to a finished diagram, build it live, one layer at a time, on the whiteboard or
in slides — this is deliberately the same order the slide deck presents it in.

**Layer 1 — the VPC alone.** One box: an example VPC, `10.0.0.0/16`. On its own it has no
subnets, no route to anywhere, and nothing inside it can talk to anything outside it.

**Layer 2 — subnets, each pinned to one Availability Zone.** Add four boxes inside the VPC: two
public, two private, one of each per AZ (Module 2 covered why AZ choice matters). Each subnet is
a smaller CIDR carved from the VPC's range — for example `10.0.1.0/24` and `10.0.2.0/24` for the
two public subnets, `10.0.11.0/24` and `10.0.12.0/24` for the two private ones. At this point,
*none* of the four subnets can reach the internet yet — adding a subnet doesn't add internet
access on its own, a common assumption worth correcting directly.

**Layer 3 — an Internet Gateway.** Add one box outside the VPC boundary, attached to it. An
Internet Gateway is what makes any traffic to/from the public internet possible at all for this
VPC — but attaching one doesn't automatically make any subnet public either. It only creates the
*possibility* of a route.

**Layer 4 — route tables.** This is the layer that actually decides public versus private. Add
a route table associated with the two public subnets, containing two routes: the VPC's own CIDR
routed `local` (automatic, always present), and `0.0.0.0/0` (everything else) routed to the
Internet Gateway. The two private subnets get their own route table with only the `local` route
— no path out at all.

Land this explicitly, now that all four layers are on the board: **a subnet is public if and
only if its route table sends `0.0.0.0/0` to an Internet Gateway.** Nothing else — not its name,
not a "public" tag, not whether an instance in it gets a public IP automatically
(`MapPublicIpOnLaunch`, which only controls IP assignment, not reachability) — makes a subnet
actually public.

## Part 3: A Real, Verified Example of the Definition Mattering (10 min)

During preparation for this course, exploring one AWS account's pre-existing VPC (provisioned
automatically by AWS Control Tower, a service many organisations — Fidelity included, per the
mission brief — use to standardise every new account's setup) turned up a genuine surprise worth
sharing as a real example, even though your own account will likely look different:

```bash
aws ec2 describe-internet-gateways --region <your-region>
```

```json
{"InternetGateways": []}
```

That account's VPC had three subnets across three AZs, all looking perfectly normal — spare IP
addresses, real CIDR blocks — but **no Internet Gateway at all**, anywhere in the account.
Checking further found no NAT Gateway and no Transit Gateway attachment either; the only
non-local route on any subnet pointed at a VPC Endpoint for S3, not general internet access. By
the correct test from Part 2, none of those three subnets were actually public, regardless of
how normal they looked.

The lesson generalises regardless of what your own account contains: **always check the route
table directly** — never assume "public" or "private" from a subnet's name, its tags, or
`MapPublicIpOnLaunch` alone.

## Part 4: Security Groups — Access Control at the Network Level (10 min)

Route tables decide whether traffic *can* reach a subnet at all. A security group is a second,
independent layer on top of that: a stateful virtual firewall attached to a specific resource (an
ECS task, a load balancer, an RDS instance) — it doesn't route traffic, it decides whether
traffic reaching that resource is allowed through.

Build two, demonstrating a real least-privilege pattern, in an example VPC:

```bash
aws ec2 create-security-group --group-name example-web-sg \
  --description "public web/ALB traffic" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <web-sg-id> \
  --protocol tcp --port 80 --cidr 0.0.0.0/0
```

`example-web-sg` is deliberately open on port 80 to `0.0.0.0/0` — correct for a public load
balancer, since anyone on the internet is meant to reach it.

```bash
aws ec2 create-security-group --group-name example-app-sg \
  --description "app tier, reachable only from example-web-sg" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <app-sg-id> \
  --protocol tcp --port 8090 --source-group <web-sg-id>
```

The key difference: `example-app-sg`'s rule references *another security group*, not a CIDR
block. Verified directly:

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

`IpRanges` is empty; `UserIdGroupPairs` names `example-web-sg` specifically. Port 8090 is
reachable only from something that has `example-web-sg` attached — not from any IP address, not
even from inside the VPC, unless it's specifically coming from a resource carrying that other
security group. This is the mechanism Module 8's load balancer and ECS task use directly.

## Key Message

"Public" and "private" are not labels anyone sets directly — they're the *result* of a route
table's configuration, specifically whether `0.0.0.0/0` reaches an Internet Gateway. Building a
VPC up layer by layer — CIDR block, then subnets, then an Internet Gateway, then route tables —
makes visible exactly which layer that decision actually lives in.

## Transition to the Lab

Candidates explore whatever VPC already exists in their own account (if any), using the
route-table test rather than any other signal, then build a small VPC of their own from scratch,
one layer at a time, matching today's build-up.
