# Lab 8 Model Answers

## Verified Output

Run for real, building directly on Module 7's cluster, execution role, and task definition:

- NAT Gateway created in a public subnet, `pending` → `available`; a new private route table,
  associated with both private subnets, routing `0.0.0.0/0` through it.
- The very first ECS task placement attempt, immediately after the NAT Gateway reported
  `available`, failed with a real `CannotPullContainerError: ... i/o timeout` — the data plane
  wasn't fully routing yet, even though the control plane said `available`. ECS retried on its
  own and the next attempt succeeded, with no manual intervention needed.
- Target group created with `--target-type ip` and a health check on `/actuator/health`. The
  default `200`-only matcher marked every target permanently unhealthy, because this
  application's actuator endpoint is guarded by Spring Security and genuinely returns `401` —
  fixed by widening the matcher to `"200,401"`.
- ALB, listener, and ECS service created; both tasks reached `RUNNING`, the target group reported
  both `healthy`, and the service reached a steady state.
- A real `curl` to the ALB's own DNS name, from outside AWS entirely, returned `HTTP 401` — a
  genuine end-to-end response through a public load balancer to a task with no public IP, in a
  private subnet.
- A forced rolling deployment: repeated `curl` requests against the ALB's DNS name throughout the
  rollout returned `HTTP 401` continuously — no failed requests, no downtime — while ECS started
  new tasks, waited for the target group to mark them healthy, and only then drained the old
  ones.

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
treating an authentication failure as "healthy" — which would also be true if the application's
security configuration were broken in some other way. A cleaner fix changes the application
itself: exposing `/actuator/health` without authentication (Spring Security's
`.requestMatchers("/actuator/health").permitAll()`, or Spring Boot Actuator's own management
security configuration) means the health check is verifying "is the application actually up,"
not "is the application up and does it happen to also return 401." The load balancer's
configuration should reflect what a healthy response really looks like, not be widened to
tolerate a response that happens to indicate the application is running but not necessarily
correctly configured.
