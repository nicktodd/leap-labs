# Lab 10 Model Answers

## Verified Output

Run against this account's accumulated activity from Modules 6-9:

- `aws cloudwatch list-metrics --namespace AWS/ECS`: `CPUUtilization`, `MemoryUtilization`,
  `LiveTaskCount` for `leap-mission-cluster` — historical data from every task run since Module 7,
  still present even with nothing currently running.
- A Logs Insights query for `Started MissionServiceApplication` returned 10 startup events across
  Modules 7, 8, and 9, with query statistics (`recordsScanned: 166`, `bytesScanned: 22693`).
- `leap-mission-high-cpu` alarm created with `--treat-missing-data notBreaching`: state
  `INSUFFICIENT_DATA` — correct, since no task is currently running to report a value. Not `OK`
  (that would require actual data points within the threshold) and not `ALARM` (that would
  require actual data points breaching it) — `INSUFFICIENT_DATA` is the only one of the three
  states that fits "no data exists yet."
- `leap-mission-observability` dashboard combining CPU/Memory time series, live task count, and
  the Logs Insights query as a table widget — created with zero validation errors.
- `aws ce get-cost-and-usage` for the last 14 days, per-service totals extrapolated to a 30-day
  month:

  | Service | 14 days (USD) | Monthly (USD) |
  |---|---|---|
  | EC2 - Other (NAT Gateway hours, Module 8's first attempt) | 0.0708 | 0.15 |
  | Elastic Load Balancing (Module 8) | 0.0450 | 0.10 |
  | Elastic Container Service (Fargate task hours) | 0.0142 | 0.03 |
  | Virtual Private Cloud (interface endpoints, Module 8's rebuild) | 0.0100 | 0.02 |
  | RDS (Module 9's db.t3.micro) | 0.0069 | 0.01 |
  | ECR | 0.0040 | 0.01 |
  | S3 | 0.0025 | 0.01 |
  | Secrets Manager | 0.0000 | 0.40 * |

  \* Secrets Manager bills a flat monthly rate per secret rather than scaling with usage — Module
  9's secret existed for a few hours, not 14 days, so its 14-day figure of `0.0000` doesn't scale
  the way the other rows do.

- `leap-mission-monthly-budget` created: $10/month, 80% actual-spend email alert — covered by AWS
  Budgets' free tier for the first two budgets on an account.

## The Reflection Question

An `EC2 - Other` charge (where NAT Gateway hourly and data-processing charges are billed) with no
corresponding `Amazon Virtual Private Cloud` line tells you that teammate's account is still
running a NAT Gateway for outbound access — meaning they either didn't switch Module 8 to
PrivateLink, or their workload needs the wider internet (an external API call PrivateLink can't
cover) and a NAT Gateway is the correct choice for their specific case. Conversely, an `Amazon
Virtual Private Cloud` charge with no `EC2 - Other` line is exactly this account's own pattern —
PrivateLink interface endpoints, no NAT Gateway, no general internet route from the private
subnets at all.

The broader point: Cost Explorer data doesn't just report what something costs — it's verifiable
evidence of which architectural choice was actually made, the same way checking a route table
directly (Module 3) is more trustworthy than a subnet's name or tags. You could infer the
networking decision from the bill alone, without ever reading the teammate's Terraform or CLI
history.
