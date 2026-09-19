# Lab 7 Model Answers

## Verified Output

Run for real, against a cluster, execution role, and task definition created during
preparation:

- `aws ecs create-cluster`: real `ACTIVE` cluster.
- `aws ecs register-task-definition`: `revision 1`, `status ACTIVE` — a template, nothing
  running.
- `docker manifest inspect` on the pushed image showed `"architecture": "arm64"` (built on an
  Apple Silicon machine in Module 6, with no `--platform` flag) — added a `runtimePlatform`
  block (`cpuArchitecture: ARM64`) to the task definition and re-registered as revision 2, before
  running anything.
- A security group allowing inbound `tcp/8080` from `0.0.0.0/0` — 8080 confirmed as the
  container's real listening port by the Dockerfile's `EXPOSE 8080` and Spring Boot's own
  default (no `server.port` override exists anywhere in the application's configuration).
- `run-task`, revision 2, in a public subnet with a public IP and that security group: `RUNNING`
  within seconds. Real CloudWatch logs showed a genuine Spring Boot startup, identical to Module
  6's local verification.
- A real HTTP request to the task's public IP on port 8080: `HTTP 401` — the same
  Spring-Security-guarded response Module 6 saw testing the image locally, confirming genuine
  reachability.

## Part 1: Choosing the Architecture

Fargate assumes `linux/amd64` unless a task definition says otherwise. Checking the pushed
image's actual architecture with `docker manifest inspect` before running anything avoids a
`CannotPullContainerError` at run-time — the fix belongs in the task definition
(`runtimePlatform`), not in rebuilding the image, since the image itself is a correct artefact
for the architecture it was built on.

## Part 2: Matching the Security Group to the Real Port

The security group has to allow the port the container actually listens on, not a port assumed
or carried over from an earlier convention. The Dockerfile's `EXPOSE` line is the authoritative
source, backed up by checking the application's own configuration for any port override. For
today's isolated test, opening that port to `0.0.0.0/0` in a dedicated security group is the
simplest way to get a reachable task without any other networking decisions in the way.

## The Reflection Question

Testing in a public subnet with a wide-open security group first is reasonable precisely because
it removes every other variable except "does this task definition, as written, actually work" —
no load balancer target group health check to configure correctly, no narrower security-group
source to get right first. If the very first test had happened behind an already-configured load
balancer in a private subnet, a wrong architecture and a wrong security group port would both
present identically and unhelpfully: the target group would simply report the target as
unhealthy, with no indication of which of several possible causes was responsible. Isolating the
task definition first, deliberately outside the final architecture, is what lets each concern be
verified on its own before Module 8 wraps it in a service and a load balancer.
