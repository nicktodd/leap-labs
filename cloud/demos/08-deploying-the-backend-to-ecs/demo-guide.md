# Module 8 Demo Guide - Deploying the Backend to ECS

**Duration:** 60 minutes
**Prerequisite:** Module 3's `leap-mission-vpc`, Module 6's ECR images, and Module 7's cluster,
execution role, and task definition, all still in place.

## Part 0: What's Missing From Module 7 (8 min)

Module 7 proved a single task definition works, tested directly with `run-task` in a public
subnet. Three real gaps stand between that and a genuine backend deployment:

- **No internet route from the private subnets.** Module 7 worked around this with a public
  subnet. The mission's real backend belongs in a *private* subnet - it needs a way to reach
  ECR to pull its image without being reachable directly from the internet.
- **No fixed entry point.** A task's IP address changes every time it restarts. Clients need a
  stable address that keeps working across restarts and deployments.
- **No ongoing management.** `run-task` starts one task and stops there - nothing restarts it if
  it crashes, and nothing coordinates replacing multiple tasks without downtime.

Three AWS pieces solve these, one each: **PrivateLink** (VPC Interface Endpoints) for reaching
ECR and CloudWatch Logs without an internet route at all, an **Application Load Balancer (ALB)**
for a stable entry point, and an **ECS service** for ongoing management.

## Part 1: PrivateLink - Reaching AWS Services With No Internet Route at All (12 min)

Module 3 covered two ways to solve "a private subnet needs to reach ECR": a NAT Gateway (general
internet access) or PrivateLink (a direct, private connection to specific AWS services, entirely
over AWS's own network). **This module uses PrivateLink, not a NAT Gateway** - and it's worth
being explicit about *why* that choice is safe here:

> **This container never needs to reach anything outside AWS.** It pulls its image from ECR and
> ships logs to CloudWatch - both AWS services - and nothing else. There is no external
> third-party API call anywhere in its code. That is precisely the condition under which
> PrivateLink alone is sufficient and a NAT Gateway isn't needed at all. A workload that *does*
> need to call out to the wider internet (a payment gateway, a third-party data feed) would still
> need a NAT Gateway, or PrivateLink for the AWS-service traffic plus a NAT Gateway for
> everything else.

Three interface endpoints cover this container's actual needs - the two ECR API surfaces and
CloudWatch Logs:

```bash
aws ec2 create-security-group --group-name leap-vpc-endpoints-sg --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <endpoints-sg-id> \
  --protocol tcp --port 443 --source-group <app-sg-id>

for SVC in ecr.api ecr.dkr logs; do
  aws ec2 create-vpc-endpoint --vpc-id <vpc-id> \
    --service-name com.amazonaws.us-east-1.$SVC --vpc-endpoint-type Interface \
    --subnet-ids <private-subnet-a> <private-subnet-b> \
    --security-group-ids <endpoints-sg-id> --private-dns-enabled
done
```

Plus a **gateway** endpoint for S3 - no hourly charge - since ECR image layers are actually
stored in S3 under the hood, associated with a private route table (local traffic only, still no
NAT route):

```bash
aws ec2 create-route-table --vpc-id <vpc-id>
aws ec2 associate-route-table --route-table-id <private-rtb-id> --subnet-id <private-subnet-a>
aws ec2 associate-route-table --route-table-id <private-rtb-id> --subnet-id <private-subnet-b>

aws ec2 create-vpc-endpoint --vpc-id <vpc-id> --service-name com.amazonaws.us-east-1.s3 \
  --vpc-endpoint-type Gateway --route-table-ids <private-rtb-id>
```

Real output: all three interface endpoints go `pending` → `available` within a couple of
minutes; the S3 gateway endpoint is `available` immediately.

## Part 2: The Application Load Balancer (15 min)

An ALB needs its own security group (public, port 80), a **target group** describing how to
route to the tasks, and a **listener** connecting the two:

```bash
aws ec2 create-security-group --group-name leap-alb-sg --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <alb-sg-id> --protocol tcp --port 80 --cidr 0.0.0.0/0

aws elbv2 create-target-group --name leap-mission-tg --protocol HTTP --port 8080 \
  --vpc-id <vpc-id> --target-type ip --health-check-path /actuator/health

aws elbv2 create-load-balancer --name leap-mission-alb --type application \
  --subnets <public-subnet-a> <public-subnet-b> --security-groups <alb-sg-id>

aws elbv2 create-listener --load-balancer-arn <alb-arn> --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn=<tg-arn>
```

`--target-type ip` matters here: Fargate tasks don't have a fixed EC2 instance to register, so
the target group tracks tasks by their (changing) IP addresses directly, updated automatically
as the ECS service starts and stops tasks.

A real, worth-naming finding: the default health check expects `HTTP 200`, but this
application's `/actuator/health` is guarded by Spring Security and genuinely returns `401` for
an unauthenticated request - the same response Module 6 and 7 saw. Rather than treat that as
broken, the health check's matcher was widened to accept both:

```bash
aws elbv2 modify-target-group --target-group-arn <tg-arn> --matcher '{"HttpCode":"200,401"}'
```

A real production setup would more likely expose an unauthenticated health endpoint
specifically for the load balancer - today's fix is the pragmatic one for the app as it exists.

Finally, the app security group needs to allow the ALB in, replacing the direct internet
reachability Module 7 used for testing:

```bash
aws ec2 authorize-security-group-ingress --group-id <app-sg-id> --protocol tcp --port 8080 \
  --source-group <alb-sg-id>
```

## Part 3: The ECS Service (12 min)

```bash
aws ecs create-service --cluster leap-mission-cluster --service-name leap-mission-service \
  --task-definition leap-mission-service:2 --desired-count 2 --launch-type FARGATE \
  --network-configuration 'awsvpcConfiguration={subnets=[<private-subnet-a>,<private-subnet-b>],securityGroups=[<app-sg-id>],assignPublicIp=DISABLED}' \
  --load-balancers targetGroupArn=<tg-arn>,containerName=mission-service,containerPort=8080
```

Real output, after both tasks reach `RUNNING` and pass the target group's health check:

```
runningCount: 2, desiredCount: 2
"has reached a steady state."
```

```bash
aws elbv2 describe-target-health --target-group-arn <tg-arn>
# both targets: "State": "healthy"
```

A real, worth-naming finding along the way: one of the two initial tasks was replaced -
`"Amazon ECS replaced 1 tasks due to an unhealthy status"` - a normal, self-healing event during
startup, not a PrivateLink problem; the service settled at `2/2 healthy` shortly after.

A real request to the ALB's own DNS name, from outside AWS entirely:

```bash
curl -i http://leap-mission-alb-63036275.us-east-1.elb.amazonaws.com/actuator/health
# HTTP/1.1 401 - genuine end-to-end reachability: public ALB, through a
# target group, to a task with no public IP of its own, in a private
# subnet, that never touched the public internet to get its image or
# ship this response's logs.
```

CloudWatch confirms the same thing from the other direction - real application logs, shipped
entirely over the `logs` interface endpoint:

```bash
aws logs get-log-events --log-group-name /ecs/leap-mission-service \
  --log-stream-name <stream-name>
# Started MissionServiceApplication in 38.9 seconds - a genuine Spring
# Boot startup, identical to Module 6 and 7's local/public-subnet runs.
```

## Part 4: A Real Rolling Deployment (8 min)

```bash
aws ecs update-service --cluster leap-mission-cluster --service leap-mission-service \
  --force-new-deployment
```

While this runs, repeated `curl` requests against the ALB's DNS name keep returning real `HTTP
401` responses throughout - no failed requests, no downtime. ECS's default rolling-update
behaviour (`minimumHealthyPercent: 100`, `maximumPercent: 200`) starts new tasks, waits for the
target group to mark them healthy, *then* deregisters and drains the old ones - the ALB never
routes traffic to a task that isn't ready.

## Key Message

Module 7 proved a task definition works in isolation. Today wires up the three pieces that turn
that into a real, continuously available backend: PrivateLink so private-subnet tasks can still
reach ECR and CloudWatch Logs with no internet route at all, an ALB and target group for a
stable entry point that tracks tasks by IP, and an ECS service that keeps the right number
running and rolls out changes without downtime. The choice of PrivateLink over a NAT Gateway is
itself worth remembering as a pattern, not just a fact about this one deployment: it's the right
default whenever a container's own outbound needs are limited to AWS services it can name in
advance - reach for a NAT Gateway only once something genuinely needs the wider internet.

## Transition to the Lab

Candidates deploy their own service the same way - PrivateLink endpoints, ALB, target group, and
ECS service - placing tasks in the private subnets behind the load balancer, and verify a real
HTTP response from outside AWS.
