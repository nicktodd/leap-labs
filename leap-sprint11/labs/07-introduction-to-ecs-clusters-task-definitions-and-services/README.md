# Lab 7 — Introduction to ECS: Clusters, Task Definitions & Services

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. Module 3's
VPC and Module 6's ECR images already in place.

## Task

### Part 1: Cluster, execution role, task definition

1. Create an ECS cluster.
2. Create an ECS task execution role, trusting `ecs-tasks.amazonaws.com`, with the AWS-managed
   `AmazonECSTaskExecutionRolePolicy` attached.
3. Write and register a Fargate task definition referencing your own `leap-mission-service` (or
   `leap-auth-service`) image from Module 6, with a `logConfiguration` sending logs to a real
   CloudWatch log group.
4. Before running anything, check your image's actual CPU architecture with `docker manifest
   inspect <your-image>`. If it's `arm64` (common on Apple Silicon machines), add a
   `runtimePlatform` block to your task definition now, rather than discovering the mismatch the
   hard way.

### Part 2: Network it — public subnet, matching security group

5. Create a security group that allows inbound traffic on the port your container actually
   listens on (check the Dockerfile's `EXPOSE` line — don't assume). For today, keep it simple:
   allow that port from anywhere (`0.0.0.0/0`).
6. Run the task definition with `run-task`, in one of Module 3's **public** subnets, with a
   public IP assigned and your new security group attached.
7. Confirm it reaches `RUNNING`, and pull its real logs from CloudWatch. Confirm the application
   inside actually started, not just that the task's status says `RUNNING`.
8. Find the task's public IP (via its ENI) and make a real HTTP request to it, from your own
   machine. Even an error response (like a 401 or 403) counts as genuine reachability — a
   connection timeout means the security group or the architecture is still wrong.

## Verify

Compare your work against `solutions/07-.../model-answers.md`. Your task should reach
`RUNNING`, its logs should show a real application startup, and a real HTTP request from your
own machine should get a genuine HTTP response.

## Cleanup

Stop any running tasks (`aws ecs stop-task`). Leave the cluster, task definition, execution
role, log group, and security group in place — Module 8 builds directly on them.

## A Question Worth Sitting With

This lab deliberately runs the task in a public subnet with an open security group, even though
the mission's real backend (Module 8 onward) belongs in a private subnet behind a load balancer.
Why is testing in a simple, wide-open setup first still a reasonable thing to do, given that
it's not the final architecture?
