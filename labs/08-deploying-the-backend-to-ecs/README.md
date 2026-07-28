# Lab 8 — Deploying the Backend to ECS

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. Module 3's
VPC, Module 6's ECR images, and Module 7's cluster, execution role, and task definition should
already be in place.

## Task

### Part 1: Give the private subnets a way out

1. Allocate an Elastic IP and create a NAT Gateway in one of the **public** subnets.
2. Create a new route table, add a `0.0.0.0/0` route pointing at the NAT Gateway, and associate
   it with both **private** subnets.

### Part 2: A stable entry point

3. Create a security group for a load balancer, allowing inbound `tcp/80` from `0.0.0.0/0`.
4. Create a target group with `--target-type ip`, pointing at your container's real port. Check
   what your health check path actually returns when unauthenticated — if it's not a `200`,
   decide whether to widen the health check's matcher or expose an unauthenticated health
   endpoint instead.
5. Create an Application Load Balancer in the public subnets, with a listener on port 80
   forwarding to your target group.
6. Update your app security group to allow the load balancer's security group in on your
   container's port.

### Part 3: A managed, continuously running service

7. Create an ECS service referencing your Module 7 task definition, running in the **private**
   subnets with no public IP, attached to your target group.
8. Confirm the service reaches a steady state with the desired number of tasks running, and that
   the target group reports them healthy.
9. From your own machine, make a real HTTP request to the load balancer's DNS name — not the
   task's IP address. Confirm you get a genuine response.

### Part 4: A rolling deployment

10. Force a new deployment (`aws ecs update-service ... --force-new-deployment`) and, while it
    runs, repeatedly request the load balancer's DNS name. Confirm you don't see any failed
    requests during the rollout.

## Verify

Compare your work against `solutions/08-.../model-answers.md`. Your service should reach a
steady state, its target group should report healthy targets, a real HTTP request to the load
balancer's DNS name should succeed, and a forced redeployment should complete with no failed
requests along the way.

## Cleanup

This module's resources cost real money while running: the NAT Gateway, the Elastic IP, and the
Application Load Balancer are all billed hourly. Once you've verified your work:

- Delete the ECS service (scale to 0, then delete).
- Delete the listener, then the load balancer, then the target group.
- Delete the NAT Gateway, then release its Elastic IP once it shows `deleted`.
- Disassociate and delete the private route table (the private subnets simply have no internet
  route again afterwards, same as after Module 3).

Leave the cluster, task definition, execution role, log group, and ECR images in place.

## A Question Worth Sitting With

The health check for `/actuator/health` had to accept a `401` as "healthy," because this
application guards that endpoint with authentication. What would you change about the
application itself, rather than the load balancer's configuration, to make this cleaner in a
real deployment?
