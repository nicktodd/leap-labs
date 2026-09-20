# Module 7 Demo Guide - Introduction to ECS: Clusters, Task Definitions & Services

**Duration:** 50 minutes
**Prerequisite:** Module 3's `leap-mission-vpc` and Module 6's ECR images, both still in place.

## Part 0: The Three Concepts, Before Any Commands (8 min)

ECS (Elastic Container Service) has exactly three building blocks worth understanding before
touching the CLI:

- **Cluster**: a logical grouping of tasks and services - not physical servers, just a
  namespace. With Fargate (the launch type this week uses), AWS manages the actual compute;
  the cluster is purely an organisational boundary.
- **Task definition**: a blueprint - which container image, how much CPU/memory, which ports,
  which IAM role, where logs go. Registering one doesn't run anything; it's a template, versioned
  by revision number, the same way Module 6's ECR tags version an image.
- **Service**: keeps a specified number of task instances running continuously, restarting any
  that stop, and (Module 8) attaching a load balancer. Today builds and tests a task definition
  directly, with `run-task` - a one-off, no ongoing management - deliberately *before* wrapping
  it in a service, matching the lab's brief: build a task definition, verify it works, stop
  there.

**Fargate vs EC2 launch type**: EC2 launch type means the account manages real EC2 instances
that ECS schedules containers onto - full control, more to patch and manage. Fargate means AWS
manages the underlying compute entirely; the task definition specifies CPU/memory, AWS finds
somewhere to run it. This week uses Fargate throughout - no server to patch is the right
default for a training account.

## Part 1: The Cluster, the Execution Role, and the Task Definition (12 min)

```bash
aws ecs create-cluster --cluster-name leap-mission-cluster
```

A task definition needs an **execution role** - not the application's own permissions, but the
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

Real output: `revision 1`, `status: ACTIVE` - a template now exists, but nothing is running yet.

## Part 2: Which CPU Architecture? (8 min)

Fargate assumes `linux/amd64` unless told otherwise. Before running anything, check what a
pushed image actually is:

```bash
docker manifest inspect <account>.dkr.ecr.us-east-1.amazonaws.com/leap-mission-service:latest \
  | grep architecture
```

```
"architecture": "arm64"
```

Common when an image was built on an Apple Silicon machine with no `--platform` flag - Docker
builds for the machine it ran on, not necessarily the machine it will run *on later*. Rather
than rebuilding the image, declare the real architecture in the task definition:

```json
"runtimePlatform": {"cpuArchitecture": "ARM64", "operatingSystemFamily": "LINUX"}
```

Fargate supports both `ARM64` and `X86_64` - the task definition just needs to say which one the
image actually is.

## Part 3: Networking a Task - Ports and Security Groups (10 min)

`awsvpc` network mode gives every task its own elastic network interface (ENI) and IP address,
the same as an EC2 instance would. Two things a task definition needs before it's reachable:

- A subnet to launch into, and whether it gets a public IP
- A security group that allows the port the container actually listens on - confirmed by the
  Dockerfile's `EXPOSE` line, not assumed

For today, keep it simple: a public subnet, a public IP, and a security group open on the
container's real port:

```bash
aws ec2 create-security-group --group-name leap-ecs-public-sg \
  --description "Public ingress for ECS tasks tested directly with run-task" \
  --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <public-sg-id> \
  --protocol tcp --port 8080 --cidr 0.0.0.0/0
```

```bash
aws ecs run-task --cluster leap-mission-cluster --task-definition leap-mission-service \
  --launch-type FARGATE --network-configuration \
  'awsvpcConfiguration={subnets=[<public-subnet-id>],securityGroups=[<public-sg-id>],assignPublicIp=ENABLED}'
```

Module 8 moves this behind a load balancer in a private subnet - today's goal is just confirming
the task definition itself runs and is reachable.

## Part 4: Verified - Real Logs, Real Reachability (10 min)

```bash
aws logs get-log-events --log-group-name /ecs/leap-mission-service \
  --log-stream-name ecs/mission-service/<task-id>
```

Real Spring Boot startup output, exactly as seen locally in Module 6.

Find the task's public IP via its ENI and make a real request:

```bash
curl http://<task-public-ip>:8080/actuator/health
# HTTP 401 - Spring Security guarding the endpoint, the same response
# Module 6 saw locally: genuine reachability, not a broken deployment.
```

## Key Message

A task definition is a real, testable artefact on its own, before any service or load balancer
exists. Two things decide whether it actually runs and is reachable: matching the declared CPU
architecture to what the image was built for, and matching the security group's allowed port to
what the container actually listens on.

## Transition to the Lab

Candidates build their own task definition for the mission-service image, check its
architecture, run it with `run-task` in a public subnet behind a security group that allows its
real port, and confirm a genuine HTTP response.
