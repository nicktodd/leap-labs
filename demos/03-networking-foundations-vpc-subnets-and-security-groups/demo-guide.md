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

## Part 2b: A Private Subnet That Still Needs to Reach Out (5 min)

Private means no *inbound* route from the internet — it doesn't mean the resources inside can
never talk out at all. An ECS task sitting in one of these private subnets still needs to reach
ECR to pull its own container image: a connection it starts itself, outbound only.

A **NAT Gateway** provides exactly that. It lives in a *public* subnet, with its own Elastic IP,
and the private subnets get a route table entry sending `0.0.0.0/0` to it instead of to the
Internet Gateway directly:

- `local + 0.0.0.0/0 -> NAT Gateway` (private route table) instead of `local + 0.0.0.0/0 -> IGW`
  (public route table)
- One-directional: a private-subnet resource can initiate a connection out through it; nothing
  on the internet can initiate one back in through it — the opposite of what an Internet Gateway
  allows

This is conceptual today — it's built and verified live in Module 8, deploying the mission's
backend, alongside a real ECS task placement error that shows exactly what happens when a
private-subnet task tries to reach ECR without one.

## Part 2c: An Alternative to the NAT Gateway — PrivateLink (5 min)

A NAT Gateway solves "reach ECR" by giving the private subnet a general-purpose path to the
*entire* internet — ECR happens to be reachable that way, but so is everything else out there.
That's more access than the actual problem needs, and every byte the task pulls from ECR travels
out over the public internet before coming back in, even though both the task and ECR are AWS
services in the same region.

**AWS PrivateLink**, via **VPC Interface Endpoints**, solves the same problem more narrowly:
a private connection directly to a specific AWS service, entirely over AWS's own network, with
no route to the public internet involved at all. For ECS pulling from ECR, that means:

- An interface endpoint for `com.amazonaws.<region>.ecr.api` and one for
  `com.amazonaws.<region>.ecr.dkr` (ECR's two API surfaces)
- A **gateway** endpoint for S3 (no hourly charge) — image layers are actually stored in S3
  under the hood, so an ECR pull needs this too
- Usually `com.amazonaws.<region>.logs` as well, if the task ships logs to CloudWatch

The genuine trade-off: a NAT Gateway is one resource that covers *any* outbound destination,
public internet included — simple, but broader than the problem requires, and it does route
through the internet path, even between two AWS services. PrivateLink is narrower and keeps
traffic entirely inside AWS's network (a real benefit for a regulated environment like
Fidelity's), but it only covers the specific services you provision an endpoint for — reaching
some unrelated third-party API from that same private subnet would still need a NAT Gateway (or
nothing, if no such need exists).

Which one costs less depends on the number of endpoints needed versus the data volume moved —
exactly the kind of trade-off Module 10 (Observability & Cost Awareness) covers properly. Cost
isn't a detail bolted on after an architecture is chosen; it's one of the real factors in
choosing between options like this one in the first place.

## Part 3: Security Groups — A Second, Independent Layer (12 min)

Everything so far — subnets, Internet Gateways, route tables — decides whether traffic *can*
reach a subnet at all. A **security group** is a second, entirely independent layer on top of
that: a stateful virtual firewall attached to a specific resource itself (an ECS task, a load
balancer, an RDS instance, an EC2 instance) — not to a subnet. It doesn't route traffic; it
decides whether traffic that has already reached that resource is *allowed through*, port by
port. A new security group denies *all* inbound traffic by default — allowing a port is always
an explicit, deliberate rule, never assumed. This is exactly why every later module that exposes
a port — ECS in Module 8, RDS in Module 9 — has its own security group rule to write, not an
afterthought.

Land the concept, then make it concrete with a situation many will recognise from deploying a
Spring Boot API in an earlier sprint: the route table is correct, an Internet Gateway is
attached, and the API is genuinely running — and it's still unreachable from anywhere but the
server itself.

```bash
# On the instance itself:
ssh ec2-user@<instance>
curl localhost:8080/api/health
# {"status":"UP"} - works, Spring Boot is listening on 8080

# From your own laptop, though:
curl http://<instance-public-ip>:8080/api/health
# curl: (28) Failed to connect - Connection timed out
```

Nothing is wrong with the app or its network route — this is deliberately the same "it works
when I curl it myself, but nobody else can reach it" moment most people hit the first time they
deploy an API to a real server, not a hypothetical. The missing piece is the security group rule
just explained a moment ago:

```bash
aws ec2 authorize-security-group-ingress --group-id <app-sg-id> \
  --protocol tcp --port 8080 --source-group <web-sg-id>

curl http://<instance-public-ip>:8080/api/health
# {"status":"UP"} - reachable now, same app, same code, same route -
# only the security group rule changed
```

Build two security groups, demonstrating a real least-privilege pattern, in an example VPC:

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
