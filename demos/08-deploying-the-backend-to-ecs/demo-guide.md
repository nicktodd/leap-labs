# Module 8 Demo Guide — Deploying the Backend to ECS

**Duration:** 60 minutes
**Prerequisite:** Module 3's `leap-mission-vpc`, Module 6's ECR images, and Module 7's cluster,
execution role, and task definition, all still in place.

## Part 0: What's Missing From Module 7 (8 min)

Module 7 proved a single task definition works, tested directly with `run-task` in a public
subnet. Three real gaps stand between that and a genuine backend deployment:

- **No internet route from the private subnets.** Module 7 worked around this with a public
  subnet. The mission's real backend belongs in a *private* subnet — it needs a way to reach
  ECR to pull its image without being reachable directly from the internet.
- **No fixed entry point.** A task's IP address changes every time it restarts. Clients need a
  stable address that keeps working across restarts and deployments.
- **No ongoing management.** `run-task` starts one task and stops there — nothing restarts it if
  it crashes, and nothing coordinates replacing multiple tasks without downtime.

Three AWS pieces solve these, one each: a **NAT Gateway** for outbound internet access from
private subnets, an **Application Load Balancer (ALB)** for a stable entry point, and an **ECS
service** for ongoing management.

## Part 1: NAT Gateway — Giving Private Subnets a Way Out (12 min)

A NAT Gateway lives in a *public* subnet, with its own Elastic IP, and lets resources in private
subnets initiate outbound connections to the internet — without the internet being able to
initiate connections back in. This is exactly what a private-subnet ECS task needs to reach
ECR's API.

```bash
aws ec2 allocate-address --domain vpc
aws ec2 create-nat-gateway --subnet-id <public-subnet-id> --allocation-id <eip-alloc-id>
```

Real output: `NatGatewayId: nat-09d80fa620c22385d`, state `pending` → `available` after a few
minutes.

A new route table, associated with *both* private subnets, sends their internet-bound traffic
through the NAT Gateway — the public route table (Module 3) still points at the Internet Gateway
directly, since NAT Gateways and Internet Gateways serve opposite directions of traffic:

```bash
aws ec2 create-route-table --vpc-id <vpc-id>
aws ec2 create-route --route-table-id <private-rtb-id> \
  --destination-cidr-block 0.0.0.0/0 --nat-gateway-id <nat-gateway-id>
aws ec2 associate-route-table --route-table-id <private-rtb-id> --subnet-id <private-subnet-a>
aws ec2 associate-route-table --route-table-id <private-rtb-id> --subnet-id <private-subnet-b>
```

A real, genuine finding: creating an ECS service immediately after the NAT Gateway reported
`available` still produced one real `CannotPullContainerError: ... i/o timeout` on the very
first task placement attempt — the control plane reports `available` slightly before the data
plane is fully routing traffic. ECS's own service scheduler retried automatically and the next
placement attempt succeeded; nothing needed fixing by hand.

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
an unauthenticated request — the same response Module 6 and 7 saw. Rather than treat that as
broken, the health check's matcher was widened to accept both:

```bash
aws elbv2 modify-target-group --target-group-arn <tg-arn> --matcher '{"HttpCode":"200,401"}'
```

A real production setup would more likely expose an unauthenticated health endpoint
specifically for the load balancer — today's fix is the pragmatic one for the app as it exists.

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

A real request to the ALB's own DNS name, from outside AWS entirely:

```bash
curl -i http://leap-mission-alb-1691128842.us-east-1.elb.amazonaws.com/actuator/health
# HTTP/1.1 401 - genuine end-to-end reachability: public ALB, through a
# target group, to a task with no public IP of its own, in a private subnet.
```

## Part 4: A Real Rolling Deployment (8 min)

```bash
aws ecs update-service --cluster leap-mission-cluster --service leap-mission-service \
  --force-new-deployment
```

While this runs, repeated `curl` requests against the ALB's DNS name keep returning real `HTTP
401` responses throughout — no failed requests, no downtime. ECS's default rolling-update
behaviour (`minimumHealthyPercent: 100`, `maximumPercent: 200`) starts new tasks, waits for the
target group to mark them healthy, *then* deregisters and drains the old ones — the ALB never
routes traffic to a task that isn't ready.

## Key Message

Module 7 proved a task definition works in isolation. Today wires up the three pieces that turn
that into a real, continuously available backend: a NAT Gateway so private-subnet tasks can
still reach ECR, an ALB and target group for a stable entry point that tracks tasks by IP, and
an ECS service that keeps the right number running and rolls out changes without downtime.

## Transition to the Lab

Candidates deploy their own service the same way — NAT Gateway, ALB, target group, and ECS
service — placing tasks in the private subnets behind the load balancer, and verify a real HTTP
response from outside AWS.
