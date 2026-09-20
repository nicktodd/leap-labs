# Lab 8 Model Answers

## Verified Output

Run for real, building directly on Module 7's cluster, execution role, and task definition:

- Three VPC interface endpoints (`ecr.api`, `ecr.dkr`, `logs`) created in the private subnets,
  `pending` → `available` within a couple of minutes; an S3 gateway endpoint (no hourly charge)
  associated with a new private route table (local route only - no NAT Gateway at all).
- ECS service created straight into the private subnets with no NAT Gateway present: both tasks
  pulled their image and reached `RUNNING` via the interface endpoints alone. One of the two
  initial tasks was replaced during startup (`"Amazon ECS replaced 1 tasks due to an unhealthy
  status"`) - a normal, self-healing startup event, not a PrivateLink problem - and the service
  settled at `2/2 healthy` shortly after.
- Target group created with `--target-type ip` and a health check on `/actuator/health`. The
  default `200`-only matcher marked every target permanently unhealthy, because this
  application's actuator endpoint is guarded by Spring Security and genuinely returns `401` -
  fixed by widening the matcher to `"200,401"`.
- ALB, listener, and ECS service created; both tasks reached `RUNNING`, the target group reported
  both `healthy`, and the service reached a steady state.
- A real `curl` to the ALB's own DNS name, from outside AWS entirely, returned `HTTP 401` - a
  genuine end-to-end response through a public load balancer to a task with no public IP, in a
  private subnet, that never had a route to the public internet at all.
- Real CloudWatch logs, confirming a genuine Spring Boot startup, shipped entirely over the
  `logs` interface endpoint - the same evidence Module 6 and 7 saw locally and in a public
  subnet, now produced with no internet route present anywhere in the path.
- A forced rolling deployment: repeated `curl` requests against the ALB's DNS name throughout the
  rollout returned `HTTP 401` continuously - no failed requests, no downtime - while ECS started
  new tasks, waited for the target group to mark them healthy, and only then drained the old
  ones.

## Part 1: PrivateLink Instead of a NAT Gateway

This container's own outbound needs are exactly ECR (image pulls) and CloudWatch Logs (log
shipping) - both AWS services, nothing external. That is precisely the condition under which
PrivateLink alone is sufficient: three interface endpoints for the specific API surfaces needed,
plus a free S3 gateway endpoint for the image layers ECR stores there. No NAT Gateway, no Elastic
IP, and no route to the public internet exists anywhere in the private subnets - genuinely
tighter than a NAT Gateway would have been, not just cheaper.

## Part 2: The Health Check Mismatch

`/actuator/health` genuinely requires authentication in this application, so an unauthenticated
health check request gets `401`, not `200`. Two real options exist: widen the target group's
matcher to accept `401` alongside `200` (the pragmatic fix used here, since it needs no
application change), or change the application to expose `/actuator/health` without
authentication specifically for infrastructure health checks, which is the more common pattern
in a real production Spring Boot service (`management.endpoint.health.show-details` and a
separate, unauthenticated management port or explicit security rule for the health path).

## The Reflection Question

Widening the load balancer's health check matcher works, but it means the load balancer is
treating an authentication failure as "healthy" - which would also be true if the application's
security configuration were broken in some other way. A cleaner fix changes the application
itself: exposing `/actuator/health` without authentication (Spring Security's
`.requestMatchers("/actuator/health").permitAll()`, or Spring Boot Actuator's own management
security configuration) means the health check is verifying "is the application actually up,"
not "is the application up and does it happen to also return 401." The load balancer's
configuration should reflect what a healthy response really looks like, not be widened to
tolerate a response that happens to indicate the application is running but not necessarily
correctly configured.

## The Second Reflection Question

PrivateLink alone would **not** be enough for a task that also needs to call an external,
non-AWS API - interface endpoints only cover the specific AWS services you provision one for,
and there is no PrivateLink endpoint for an arbitrary third-party service. That workload would
need a NAT Gateway added back for the external-API traffic. Critically, this wouldn't mean
removing the interface endpoints - the two approaches are complementary, not exclusive: PrivateLink
continues handling the AWS-service traffic (ECR, CloudWatch Logs) over AWS's own network, exactly
as it does today, while a NAT Gateway handles only the genuinely external traffic that has no
AWS-service equivalent. The route table would end up with `0.0.0.0/0 → NAT Gateway` for general
internet traffic, alongside the endpoint-specific routes PrivateLink manages automatically.
