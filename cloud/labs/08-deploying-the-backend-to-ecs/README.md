# Lab 8 - Deploying the Backend to ECS

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. Module 3's
VPC, Module 6's ECR images, and Module 7's cluster, execution role, and task definition should
already be in place.

## Task

### Part 1: Give the private subnets a way to reach ECR - without a NAT Gateway

This container has no need to reach anything outside AWS: it pulls its image from ECR and ships
logs to CloudWatch, nothing else. That's exactly the condition under which PrivateLink alone is
enough - a NAT Gateway would give it (and anything else that later lands in these subnets)
general internet access it doesn't need.

1. Create a security group for VPC interface endpoints, allowing inbound `tcp/443` from your app
   security group only.
2. Create three interface endpoints (`com.amazonaws.<region>.ecr.api`,
   `com.amazonaws.<region>.ecr.dkr`, `com.amazonaws.<region>.logs`), in the private subnets, with
   that security group, private DNS enabled.
3. Create a new route table (local route only, no NAT - the private subnets still have no route
   to the internet), associate it with both **private** subnets, and create an S3 **gateway**
   endpoint (no hourly charge) associated with it - ECR image layers are stored in S3.

### Part 2: A stable entry point

4. Create a security group for a load balancer, allowing inbound `tcp/80` from `0.0.0.0/0`.
5. Create a target group with `--target-type ip`, pointing at your container's real port. Check
   what your health check path actually returns when unauthenticated - if it's not a `200`,
   decide whether to widen the health check's matcher or expose an unauthenticated health
   endpoint instead.
6. Create an Application Load Balancer in the public subnets, with a listener on port 80
   forwarding to your target group.
7. Update your app security group to allow the load balancer's security group in on your
   container's port.

### Part 3: A managed, continuously running service

8. Create an ECS service referencing your Module 7 task definition, running in the **private**
   subnets with no public IP, attached to your target group.
9. Confirm the service reaches a steady state with the desired number of tasks running, and that
   the target group reports them healthy.
10. From your own machine, make a real HTTP request to the load balancer's DNS name - not the
    task's IP address. Confirm you get a genuine response.

### Part 4: A rolling deployment

11. Force a new deployment (`aws ecs update-service ... --force-new-deployment`) and, while it
    runs, repeatedly request the load balancer's DNS name. Confirm you don't see any failed
    requests during the rollout.

## Verify

Compare your work against `solutions/08-.../model-answers.md`. Your service should reach a
steady state, its target group should report healthy targets, a real HTTP request to the load
balancer's DNS name should succeed, and a forced redeployment should complete with no failed
requests along the way.

## Cleanup

This module's resources cost real money while running: the three interface endpoints and the
Application Load Balancer are all billed hourly. Once you've verified your work:

- Delete the ECS service (scale to 0, then delete).
- Delete the listener, then the load balancer, then the target group and its security group.
- Delete the three interface endpoints.

Leave the cluster, task definition, execution role, log group, ECR images, the S3 gateway
endpoint (no hourly charge), and the private route table in place - none of them cost anything
idle, and later modules can reuse them.

## A Question Worth Sitting With

The health check for `/actuator/health` had to accept a `401` as "healthy," because this
application guards that endpoint with authentication. What would you change about the
application itself, rather than the load balancer's configuration, to make this cleaner in a
real deployment?

## A Second Question Worth Sitting With

This module used PrivateLink instead of a NAT Gateway because the container has no need to
reach anything outside AWS. If a later capstone extension needed to call an external, non-AWS
API from this same private subnet, would PrivateLink alone still be enough? What would you need
to add, and would it replace the interface endpoints or sit alongside them?
