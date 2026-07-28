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

### Part 2: Test the task definition directly

5. Run the task definition once with `run-task`, in one of Module 3's **public** subnets, with
   a public IP assigned — deliberately isolating "does this task definition work at all" from
   "does it work in a private subnet," which needs infrastructure this module doesn't build.
6. Confirm it reaches `RUNNING`, and pull its real logs from CloudWatch. Confirm the application
   inside actually started, not just that the task's status says `RUNNING`.
7. Find the task's public IP (via its ENI) and make a real HTTP request to it, from your own
   machine. If it fails, work through why systematically: is the security group actually
   allowing the port the container is really listening on (check the Dockerfile's `EXPOSE`
   line and the application's actual configuration, not an assumption)? Is your own IP allowed
   through?

### Part 3: What Module 3's security group actually assumed

8. Compare the port your security group allows against the port your container actually
   listens on. If they don't match, decide which one is wrong and fix it — don't just open the
   security group to more ports "to be safe."

## Verify

Compare your Part 3 finding against `solutions/07-.../model-answers.md`. Your task should
reach `RUNNING`, its logs should show a real application startup, and a real HTTP request from
your own machine should get a genuine HTTP response (even an error response, like a 401 or 403,
counts as genuine reachability — a connection timeout does not).

## Cleanup

Stop any running tasks (`aws ecs stop-task`) and revoke any temporary security group rules you
added for your own IP. Leave the cluster, task definition, execution role, and log group in
place — Module 8 builds directly on all four.

## A Question Worth Sitting With

This lab deliberately runs the task in a public subnet, with a public IP, even though the
mission's real backend (Module 8 onward) belongs in a private subnet behind a load balancer.
Why is testing in a public subnet first still a reasonable thing to do, given that it's not the
final architecture? What specifically would have been harder to diagnose if the first-ever test
of this task definition had happened inside a private subnet with a load balancer already in
front of it?
