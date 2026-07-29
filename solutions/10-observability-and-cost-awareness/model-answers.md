# Lab 10 Model Answers

## Verified Output

Run for real, against this account's actual accumulated activity from Modules 6-9:

- `aws cloudwatch list-metrics --namespace AWS/ECS`: real `CPUUtilization`, `MemoryUtilization`,
  `LiveTaskCount` for `leap-mission-cluster` — genuine historical data from every task run since
  Module 7, still present even with nothing currently running.
- A Logs Insights query for `Started MissionServiceApplication` returned 10 real startup events
  across Modules 7, 8, and 9, with real statistics (`recordsScanned: 166`, `bytesScanned: 22693`).
- `leap-mission-high-cpu` alarm created with `--treat-missing-data notBreaching`: real state
  `INSUFFICIENT_DATA` — honest and correct, since no task is currently running to report a value.
- `leap-mission-observability` dashboard combining CPU/Memory time series, live task count, and
  the Logs Insights query as a table widget — created with zero validation errors.
- `aws ce get-cost-and-usage` for the last 14 days, real per-service totals:

  ```
  0.0708  EC2 - Other                          (NAT Gateway hours, Module 8's first attempt)
  0.0450  Amazon Elastic Load Balancing         (ALB hours, Module 8)
  0.0142  Amazon Elastic Container Service      (Fargate task hours)
  0.0100  Amazon Virtual Private Cloud          (interface endpoints, Module 8's rebuild)
  0.0069  Amazon Relational Database Service    (Module 9's db.t3.micro)
  0.0040  Amazon EC2 Container Registry (ECR)
  0.0025  Amazon Simple Storage Service
  0.0000  AWS Secrets Manager
  ```

- `leap-mission-monthly-budget` created: $10/month, 80% actual-spend email alert — AWS Budgets'
  free tier covers this with no charge.

## The Reflection Question

An `EC2 - Other` charge (where NAT Gateway hourly and data-processing charges are billed) with no
corresponding `Amazon Virtual Private Cloud` line tells you that teammate's account is still
running a NAT Gateway for outbound access — meaning they either didn't switch Module 8 to
PrivateLink, or their workload genuinely needs the wider internet (an external API call
PrivateLink can't cover) and a NAT Gateway is the correct choice for their specific case.
Conversely, a real `Amazon Virtual Private Cloud` charge with no `EC2 - Other` line is exactly
this account's own pattern — PrivateLink interface endpoints, no NAT Gateway, no general internet
route from the private subnets at all.

The broader point: real Cost Explorer data doesn't just report what something costs — it's
verifiable, honest evidence of which architectural choice was actually made, the same way
checking a route table directly (Module 3) is more trustworthy than a subnet's name or tags. You
could infer the networking decision from the bill alone, without ever reading the teammate's
Terraform or CLI history.
