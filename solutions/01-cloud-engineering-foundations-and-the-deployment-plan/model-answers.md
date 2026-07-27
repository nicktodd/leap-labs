# Lab 1 Model Answers

## Part 1: The Map

| Piece | Moves or stays? | AWS home | Network note |
|---|---|---|---|
| `mission-ui` | Moves | S3 (static build) behind CloudFront | Public — this is the one thing anyone on the internet should be able to reach directly |
| `mission-service` | Moves | ECS Fargate task, behind an Application Load Balancer | ALB is public; the ECS task itself sits in a private subnet, reachable only via the ALB |
| `sprint8-auth-service` | Moves | ECS Fargate task, behind the same or a second ALB | Same pattern as `mission-service` — private subnet, fronted by a load balancer |
| Postgres | Moves | RDS | Private subnet only — never reachable from the internet, only from the ECS tasks that need it |
| Kafka | **Stays local** | N/A (Docker Compose) | Not part of this sprint's deployment |

Kafka is the odd one out, and deliberately so — see the demo's Part 3. AWS's managed Kafka
service (MSK) is expensive to run correctly (a real cluster needs multiple broker nodes at a
non-trivial minimum size) and is its own multi-day topic to configure well. Kafka is out of
scope for this sprint by deliberate decision, not an oversight.

## Part 2: The Request Trace

```
Loading the app:
  Browser → CloudFront (public internet, TLS terminates here) → S3 (serves mission-ui's
  static files — HTML/CSS/JS only)

Once loaded, a separate, independent path for every API call the app makes:
  Browser → Application Load Balancer (public internet) → ECS Fargate task running
  mission-service (private subnet) → RDS Postgres (private subnet, reachable only from
  inside the VPC)
```

These are two unconnected branches, not one continuous chain — S3 never calls the load
balancer, and the load balancer never calls S3.

Two hops cross the public internet: browser-to-CloudFront and browser-to-ALB. Everything after
the ALB — the ECS task talking to RDS — never leaves AWS's private network. This mirrors
exactly how the mission already works locally: the browser only ever talks to `mission-service`
directly, never to Postgres.

## Part 3: Where Secrets Live

Both the JWT signing secret and the database password belong in **Secrets Manager**, retrieved
by the ECS task at startup rather than baked into either the container image or a local file.

"Hardcoded in the container image" is wrong even though it technically works, for a reason
that has nothing to do with convenience: a container image pushed to ECR is not automatically
secret. Anyone with read access to that ECR repository — which, in a real organisation, is
often a wider group than the people who should know the production database password — can
pull the image and extract anything baked into it. A secret embedded in an image also can't be
rotated without rebuilding and redeploying the image, whereas Secrets Manager lets the
credential change without touching the running task's code at all.

## The Reflection Question

**Applying this to a Sprint 10 capstone extension**: most extensions add one more thing that
either serves static content (fits into the S3/CloudFront pattern, no new AWS service needed)
or runs as its own long-lived process (fits into the ECS pattern — another task definition,
possibly its own ECR repository, sharing the same cluster and VPC as `mission-service`). A
websocket-based extension is the one case worth flagging as different: ECS/Fargate
can run a long-lived WebSocket server without any special handling, but an Application Load
Balancer needs to be configured for WebSocket support specifically (it works, but it's a real
configuration detail, not automatic) — worth raising with an instructor rather than assuming
it "just works" the same way a REST endpoint does.
