# Lab 7 Model Answers

## Verified Output

Run for real, against a cluster, execution role, and task definition created during
preparation:

- `aws ecs create-cluster`: real `ACTIVE` cluster.
- `aws ecs register-task-definition`: `revision 1`, `status ACTIVE` — a template, nothing
  running.
- First `run-task`, in a **private** subnet: stuck `PENDING` for several real minutes, then
  `STOPPED` with `ResourceInitializationError: unable to pull secrets or registry auth ... dial
  tcp ...: i/o timeout` — a private subnet has no route to ECR's API at all.
- Second `run-task`, in a **public** subnet with a public IP: `STOPPED` immediately with
  `CannotPullContainerError: ... does not contain descriptor matching platform 'linux/amd64'` —
  the image was built `arm64` on an Apple Silicon machine in Module 6, with no platform declared.
- Third `run-task`, task definition revision 2 with `runtimePlatform: {cpuArchitecture: ARM64}`
  added: `RUNNING` within seconds. Real CloudWatch logs showed a genuine Spring Boot startup,
  identical to Module 6's local verification.
- A real HTTP request to the task's public IP on port 8080, after correcting the security group
  from port 8090 (a leftover local-development convention) to port 8080 (the container's actual
  `EXPOSE`d and listening port): `HTTP 401` — the same Spring-Security-guarded response Module
  6 saw testing the image locally, confirming genuine reachability, not a broken deployment.

## Part 3: The Port Mismatch

The container's real listening port is 8080, confirmed by the Dockerfile's `EXPOSE 8080` and by
Spring Boot's own default (no `server.port` override exists anywhere in the application's
configuration) — the same port a local `docker run -p <host>:8080` test in Module 6 mapped
against. Module 3's security group was built assuming port 8090, which turns out to have been a
local-development-only convention from an earlier point in the mission's history, never the
actual port the containerised application listens on. The security group was wrong, not the
container — fixed by revoking the 8090 rule and authorising 8080 instead, kept scoped to the
same `leap-web-sg` source it always was.

## The Reflection Question

Testing in a public subnet first is reasonable precisely because it removes every other variable
except "does this task definition, as written, actually work" — no NAT Gateway or VPC endpoint
decision to get right first, no load balancer target group health check to configure correctly,
no private-subnet routing to reason about. Each of this lab's three real failures (no network
route, wrong CPU architecture, wrong port) surfaced as its own distinct, unambiguous error
message, one at a time, precisely because nothing else in the path could also be the cause.

Had the very first test happened inside a private subnet behind an already-configured load
balancer, all three problems would have presented identically and unhelpfully: the load
balancer's target group would simply report every target as unhealthy, with no indication of
*why* — a wrong CPU architecture, a missing network route, and a wrong security group port all
produce the exact same symptom (the target never becomes healthy) from an ALB's point of view.
Isolating the task definition first, deliberately outside the final architecture, is what let
each of these three real, independent bugs get diagnosed from its own specific, real error
message instead of one generic "unhealthy target" alarm covering all three at once.
