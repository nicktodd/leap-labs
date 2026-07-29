# Module 10 Demo Guide — Observability & Cost Awareness

**Duration:** 50 minutes
**Prerequisite:** Modules 6-9's real, historical AWS activity — this module deliberately reuses
the data already generated rather than creating fresh resources first.

## Part 0: Two Questions Every Real Deployment Has to Answer (5 min)

Everything built so far answers "does it work?" Two questions remain, and neither is optional in
a real account: "is it actually healthy right now?" (observability) and "what is this costing?"
(cost awareness). Both get real, live answers today, using data this sprint's earlier modules
already generated — no new infrastructure needs to exist first.

## Part 1: CloudWatch Metrics — What ECS Already Tracks (10 min)

ECS publishes metrics automatically, with no configuration needed, for as long as a cluster has
ever run tasks:

```bash
aws cloudwatch list-metrics --namespace AWS/ECS \
  --query 'Metrics[?Dimensions[?Value==`leap-mission-cluster`]].MetricName'
```

Real output: `CPUUtilization`, `MemoryUtilization`, `LiveTaskCount` — genuine historical data
points from every real task this sprint has run, going back to Module 7. A cluster with no tasks
currently running (true right now, since Module 9's verification tasks were one-off) still has
real historical metric data — CloudWatch doesn't delete it just because nothing is running this
second.

## Part 2: A Real CloudWatch Alarm (8 min)

```bash
aws cloudwatch put-metric-alarm --alarm-name leap-mission-high-cpu \
  --namespace AWS/ECS --metric-name CPUUtilization \
  --dimensions Name=ClusterName,Value=leap-mission-cluster \
  --statistic Average --period 300 --evaluation-periods 2 \
  --threshold 80 --comparison-operator GreaterThanThreshold \
  --treat-missing-data notBreaching
```

Real output: state `INSUFFICIENT_DATA` — an honest, correct state, not an error. It means exactly
what it says: no task is currently running to report a CPU value at all. `treat-missing-data
notBreaching` is a deliberate choice here — without it, an alarm on a service that legitimately
scales to zero between demos would flag as `ALARM` for a reason that has nothing to do with a
real problem.

## Part 3: A Dashboard Combining Metrics and Logs (10 min)

A single dashboard can mix metric graphs with a **Logs Insights** query, run directly against the
real log group every earlier module has been writing to:

```bash
aws logs start-query --log-group-name /ecs/leap-mission-service \
  --start-time <7-days-ago> --end-time <now> \
  --query-string 'fields @timestamp, @message
    | filter @message like /Started MissionServiceApplication/
    | sort @timestamp desc | limit 20'
```

Real output: ten genuine startup events, one per task run across Modules 7, 8, and 9 — real
timestamps, real startup durations, `recordsScanned: 166` against `bytesScanned: 22693` in the
query's own statistics. This is the same log group used throughout this sprint; nothing new had
to be created to query it meaningfully.

```bash
aws cloudwatch put-dashboard --dashboard-name leap-mission-observability \
  --dashboard-body file://dashboard.json
```

The dashboard combines CPU/Memory time series, live task count, and that Logs Insights query as
a table — one place to check "is it healthy" without switching between the ECS console, the
CloudWatch console, and CloudWatch Logs separately.

## Part 4: Real Cost Data — Cost Explorer (12 min)

Rather than estimate what this sprint's modules have cost, ask AWS directly:

```bash
aws ce get-cost-and-usage --time-period Start=<14-days-ago>,End=<today> \
  --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE
```

Real output, sorted by cost, for this account's actual last two weeks:

```
0.0708  EC2 - Other                              (NAT Gateway hours - Module 8)
0.0450  Amazon Elastic Load Balancing             (ALB hours - Module 8)
0.0142  Amazon Elastic Container Service          (Fargate task hours)
0.0100  Amazon Virtual Private Cloud               (interface endpoints - Module 8)
0.0069  Amazon Relational Database Service         (Module 9's db.t3.micro)
0.0040  Amazon EC2 Container Registry (ECR)
0.0025  Amazon Simple Storage Service
0.0000  AWS Secrets Manager
```

This is the real bill for exactly what this sprint built — and it directly confirms two earlier
decisions with actual numbers, not estimates: EC2 - Other (the NAT Gateway line) only appears for
Module 8's original attempt, and disappears entirely once Module 8 switched to PrivateLink;
Secrets Manager's real charge for the few hours Module 9's secret existed rounds to zero, but a
secret kept for a full month would show a real, non-zero monthly line the way Parameter Store
never would.

## Part 5: A Real Budget and Alert (5 min)

```bash
aws budgets create-budget --account-id <account-id> \
  --budget '{"BudgetName":"leap-mission-monthly-budget",
    "BudgetLimit":{"Amount":"10","Unit":"USD"},
    "BudgetType":"COST","TimeUnit":"MONTHLY"}' \
  --notifications-with-subscribers '[{"Notification":{
    "NotificationType":"ACTUAL","ComparisonOperator":"GREATER_THAN",
    "Threshold":80,"ThresholdType":"PERCENTAGE"},
    "Subscribers":[{"SubscriptionType":"EMAIL","Address":"<alert-email>"}]}]'
```

A real, working budget: $10/month, alerting by email once actual spend crosses 80% of that. AWS
Budgets is free for the first two budgets per account — there's no cost reason not to have one on
every real account from day one.

## Key Message

Observability and cost awareness aren't separate concerns bolted on at the end — they're both
just *asking AWS what actually happened*, the same discipline this sprint has used for every
other question ("is this subnet really public," "is this port really reachable"). CloudWatch
already has real metrics and logs from every module so far; Cost Explorer already has the real
bill. Today's work is querying data that already exists, not creating a new observability system
from scratch.

## Transition to the Lab

Candidates query their own account's real ECS metrics and cost history, build their own alarm
and dashboard, and set up their own budget with a real alert threshold.
