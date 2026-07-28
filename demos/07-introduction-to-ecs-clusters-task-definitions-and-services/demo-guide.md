# Module 7 Demo Guide — Introduction to ECS: Clusters, Task Definitions & Services

**Duration:** 50 minutes
**Prerequisite:** Module 3's `leap-mission-vpc` and Module 6's ECR images, both still in place.

## Part 0: The Three Concepts, Before Any Commands (8 min)

ECS (Elastic Container Service) has exactly three building blocks worth understanding before
touching the CLI:

- **Cluster**: a logical grouping of tasks and services — not physical servers, just a
  namespace. With Fargate (the launch type this sprint uses), AWS manages the actual compute;
  the cluster is purely an organisational boundary.
- **Task definition**: a blueprint — which container image, how much CPU/memory, which ports,
  which IAM role, where logs go. Registering one doesn't run anything; it's a template, versioned
  by revision number, the same way Module 6's ECR tags version an image.
- **Service**: keeps a specified number of task instances running continuously, restarting any
  that stop, and (Module 8) attaching a load balancer. Today builds and tests a task definition
  directly, with `run-task` — a one-off, no ongoing management — deliberately *before* wrapping
  it in a service, matching the lab's brief: build a task definition, verify it works, stop
  there.

**Fargate vs EC2 launch type**: EC2 launch type means the account manages real EC2 instances
that ECS schedules containers onto — full control, more to patch and manage. Fargate means AWS
manages the underlying compute entirely; the task definition specifies CPU/memory, AWS finds
somewhere to run it. This sprint uses Fargate throughout — no server to patch is the right
default for a training account.

## Part 1: The Cluster, the Execution Role, and the Task Definition (12 min)

```bash
aws ecs create-cluster --cluster-name leap-mission-cluster
```

A task definition needs an **execution role** — not the application's own permissions, but the
identity ECS itself uses to pull the image and write logs, before the application code runs at
all:

```bash
aws iam create-role --role-name leap-ecs-task-execution-role \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[
    {"Effect":"Allow","Principal":{"Service":"ecs-tasks.amazonaws.com"},
     "Action":"sts:AssumeRole"}]}'
aws iam attach-role-policy --role-name leap-ecs-task-execution-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

Register the task definition, referencing the real image pushed to ECR in Module 6:

```json
{
  "family": "leap-mission-service",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256", "memory": "512",
  "executionRoleArn": "arn:aws:iam::<account>:role/leap-ecs-task-execution-role",
  "containerDefinitions": [{
    "name": "mission-service",
    "image": "<account>.dkr.ecr.us-east-1.amazonaws.com/leap-mission-service:latest",
    "portMappings": [{"containerPort": 8080, "protocol": "tcp"}],
    "logConfiguration": {"logDriver": "awslogs", "options": {
      "awslogs-group": "/ecs/leap-mission-service",
      "awslogs-region": "us-east-1", "awslogs-stream-prefix": "ecs"}}
  }]
}
```

```bash
aws ecs register-task-definition --cli-input-json file://task-def.json
```

Real output: `revision 1`, `status: ACTIVE` — a template now exists, but nothing is running yet.

## Part 2: A Real Failure — Private Subnet, No Route to ECR (10 min)

Run the task definition once, in one of Module 3's *private* subnets, to test it:

```bash
aws ecs run-task --cluster leap-mission-cluster --task-definition leap-mission-service \
  --launch-type FARGATE --network-configuration \
  'awsvpcConfiguration={subnets=[<private-subnet-id>],securityGroups=[<app-sg-id>],assignPublicIp=DISABLED}'
```

Real, verified failure, after several minutes stuck `PENDING`:

```
ResourceInitializationError: unable to pull secrets or registry auth: The task cannot pull
registry auth from Amazon ECR: ... dial tcp 44.213.78.216:443: i/o timeout
```

This is Module 3's own lesson landing directly: a private subnet has no route to the internet
at all, and ECR's API is reached over the internet (or a VPC endpoint, neither of which exists
here yet). The task definition itself is correct — nothing about it was wrong — the network it
was placed in simply has no way to reach ECR. Module 8 addresses this properly for the real
deployment; today, re-run the same task definition unchanged in a *public* subnet with a public
IP, purely to isolate and confirm the task definition itself works:

```bash
aws ecs run-task ... --network-configuration \
  'awsvpcConfiguration={subnets=[<public-subnet-id>],securityGroups=[<app-sg-id>],assignPublicIp=ENABLED}'
```

## Part 3: A Second Real Failure — Platform Mismatch (8 min)

Real output this time, a different failure:

```
CannotPullContainerError: pull image manifest has been retried 7 time(s): image Manifest does
not contain descriptor matching platform 'linux/amd64'
```

`docker manifest inspect` on the pushed image confirms it: `architecture: arm64` — built on an
Apple Silicon Mac in Module 6, with no explicit platform flag, so Docker built for the machine
it ran on. Fargate defaults to expecting `linux/amd64`. The real fix, without rebuilding: tell
the task definition what architecture the image actually is —

```json
"runtimePlatform": {"cpuArchitecture": "ARM64", "operatingSystemFamily": "LINUX"}
```

Re-register (revision 2), re-run in the public subnet: `RUNNING` within seconds.

## Part 4: Verified — Real Logs, Real Reachability, and a Third Real Mismatch (10 min)

```bash
aws logs get-log-events --log-group-name /ecs/leap-mission-service \
  --log-stream-name ecs/mission-service/<task-id>
```

Real Spring Boot startup output, exactly as seen locally in Module 6.

Reaching the task from a browser fails at first — a third real, worth-naming mismatch:
`leap-app-sg` (Module 3) authorised port **8090**, but the container's real listening port,
confirmed by the Dockerfile's `EXPOSE 8080` and Spring Boot's own default, is **8080**. Port
8090 was a local development convention from earlier sprints, never the container's actual
port. Fix the security group to match the real artefact, not the earlier assumption:

```bash
aws ec2 revoke-security-group-ingress --group-id <app-sg-id> --protocol tcp --port 8090 \
  --source-group <web-sg-id>
aws ec2 authorize-security-group-ingress --group-id <app-sg-id> --protocol tcp --port 8080 \
  --source-group <web-sg-id>
```

With a temporary rule for the demo machine's own IP, a real request succeeds:

```bash
curl http://<task-public-ip>:8080/actuator/health
# HTTP 401 - identical to Module 6's local verification: Spring Security
# guarding the endpoint, not a broken deployment.
```

## Key Message

A task definition is a real, testable artefact on its own, before any service or load balancer
exists — and testing it directly, with `run-task`, surfaced three genuine, independent problems
(no network route, wrong CPU architecture, wrong port) that a rushed jump straight to a full
service-plus-ALB deployment in Module 8 would have made much harder to isolate and diagnose one
at a time.

## Transition to the Lab

Candidates build their own task definition for the mission-service image, test it the same way
— in a public subnet first, to isolate task-definition problems from Module 9's networking work
— and fix whatever real mismatches turn up along the way.
