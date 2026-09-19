# Module 10 Demo Guide — Observability & Cost Awareness

**Duration:** 55 minutes
**Prerequisite:** Modules 6-9's historical AWS activity — this module deliberately reuses the
data already generated rather than creating fresh resources first.

## Part 0: Two Questions Every Deployment Has to Answer (5 min)

Everything built so far answers "does it work?" Two questions remain, and neither is optional in
a production account: "is it actually healthy right now?" (observability) and "what is this
costing?" (cost awareness). Both get answered today using data this sprint's earlier modules
already generated — no new infrastructure needs to exist first.

## Part 1: CloudWatch Metrics — What ECS Already Tracks (10 min)

ECS publishes metrics automatically, with no configuration needed, for as long as a cluster has
ever run tasks:

```bash
aws cloudwatch list-metrics --namespace AWS/ECS \
  --query 'Metrics[?Dimensions[?Value==`leap-mission-cluster`]].MetricName'
```

Output: `CPUUtilization`, `MemoryUtilization`, `LiveTaskCount` — historical data points from
every task this sprint has run, going back to Module 7. A cluster with no tasks currently running
(true right now, since Module 9's verification tasks were one-off) still has this historical
metric data — CloudWatch doesn't delete it just because nothing is running this second.

## Part 2: What a CloudWatch Alarm Actually Is (8 min)

An alarm watches a single metric and compares it to a threshold over a configured number of
evaluation periods. It has exactly three possible states:

| State | What it means |
|---|---|
| `OK` | The metric is within the threshold |
| `ALARM` | The metric has breached the threshold for the configured number of evaluation periods |
| `INSUFFICIENT_DATA` | Not enough data points exist yet to evaluate the alarm — e.g. nothing has published a value recently |

An alarm can trigger an action in any of these states — most commonly, publishing a notification
(to an SNS topic, email, or a Lambda function) when it moves into `ALARM`.

```bash
aws cloudwatch put-metric-alarm --alarm-name leap-mission-high-cpu \
  --namespace AWS/ECS --metric-name CPUUtilization \
  --dimensions Name=ClusterName,Value=leap-mission-cluster \
  --statistic Average --period 300 --evaluation-periods 2 \
  --threshold 80 --comparison-operator GreaterThanThreshold \
  --treat-missing-data notBreaching
```

Output: state `INSUFFICIENT_DATA`. That's correct, not an error — no task is currently running to
report a CPU value at all. `treat-missing-data notBreaching` is a deliberate choice here —
without it, an alarm on a service that legitimately scales to zero between demos would move into
`ALARM` for a reason that has nothing to do with the service actually being unhealthy.

## Part 3: A Dashboard Combining Metrics and Logs (10 min)

A single dashboard can mix metric graphs with a **Logs Insights** query, run directly against the
log group every earlier module has been writing to:

```bash
aws logs start-query --log-group-name /ecs/leap-mission-service \
  --start-time <7-days-ago> --end-time <now> \
  --query-string 'fields @timestamp, @message
    | filter @message like /Started MissionServiceApplication/
    | sort @timestamp desc | limit 20'
```

Output: ten startup events, one per task run across Modules 7, 8, and 9 — actual timestamps,
actual startup durations, and the query's own statistics (`recordsScanned: 166`,
`bytesScanned: 22693`). This is the same log group used throughout this sprint; nothing new had
to be created to query it meaningfully.

```bash
aws cloudwatch put-dashboard --dashboard-name leap-mission-observability \
  --dashboard-body file://dashboard.json
```

The dashboard combines CPU/Memory time series, live task count, and that Logs Insights query as
a table — one place to check "is it healthy" without switching between the ECS console, the
CloudWatch console, and CloudWatch Logs separately.

## Part 4: Cost Data — the Actual Bill vs. What Continuous Running Would Cost (12 min)

Rather than estimate what this sprint's modules have cost, ask AWS directly:

```bash
aws ce get-cost-and-usage --time-period Start=<14-days-ago>,End=<today> \
  --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE
```

Output, sorted by cost, for this account's actual last two weeks:

| Service | Actual 14-day bill (USD) |
|---|---|
| NAT Gateway (EC2 - Other) | 0.0708 |
| Elastic Load Balancing | 0.0450 |
| Elastic Container Service | 0.0142 |
| Virtual Private Cloud (PrivateLink) | 0.0100 |
| RDS | 0.0069 |
| ECR | 0.0040 |
| S3 | 0.0025 |
| Secrets Manager | 0.0000 |

These numbers are small because every billed resource this sprint created was torn down again
straight after verification — a few hours of NAT Gateway, a few hours of RDS, not 14 days of
either. Naively scaling this sample up to a month (multiplying by 30/14) would still show
fractions of a cent, which understates the real cost of actually running these resources —
because most of the 14-day window, they simply didn't exist. A more honest monthly figure comes
from AWS's own published hourly rates for `us-east-1`, applied to what continuous, 24/7 operation
for 30 days (730 hours) would actually cost:

| Service | If run continuously for 30 days (USD) |
|---|---|
| NAT Gateway | 32.85 |
| Elastic Load Balancing | 16.43 |
| Elastic Container Service (2 tasks) | 14.42 |
| Virtual Private Cloud (3 PrivateLink endpoints) | 21.90 |
| RDS (db.t3.micro + 20GB storage) | 14.71 |
| ECR | 0.03 |
| S3 | 0.01 |
| Secrets Manager | 0.40 |

Two things worth being precise about: this right-hand column is *calculated* from AWS's published
rate card, not observed in Cost Explorer — none of these resources actually ran for 30 days, so
there's no real bill to point at for that figure. And NAT Gateway and the three PrivateLink
endpoints are shown as alternatives, not costs that add together — Module 8 never ran both at
once; they're the two competing answers to the same "how does a private subnet reach ECR"
question, and comparing their monthly figures side by side ($32.85 vs. $21.90, before NAT
Gateway's own data-processing charges) is a real part of the case for PrivateLink when a
workload's needs allow it.

## Part 5: What AWS Budgets Are, and How to Create One (8 min)

A budget tracks spend (or usage) against a limit you set, and notifies you when actual or
forecasted spend crosses a threshold — it doesn't stop spending on its own, only alerts. This is
exactly the kind of early warning that catches a forgotten NAT Gateway or an oversized RDS
instance before the monthly bill arrives, rather than after.

A budget is created with a limit, a time unit (monthly is typical for a cost budget), and one or
more notification thresholds, each with its own subscriber — an email address or an SNS topic:

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

A working budget: $10/month, alerting by email once actual spend crosses 80% of that. AWS Budgets
is free for the first two budgets on an account — there's no cost reason not to have one on every
account from day one.

## Key Message

Observability and cost awareness aren't separate concerns bolted on at the end — both are just
*asking AWS what actually happened*, the same discipline this sprint has used for every other
question ("is this subnet actually public," "is this port actually reachable"). CloudWatch
already has metrics and logs from every module so far; Cost Explorer already has the bill.
Today's work is querying data that already exists, not building a new observability system from
scratch.

## Transition to the Lab

Candidates query their own account's ECS metrics and cost history, build their own alarm and
dashboard, and set up their own budget with an alert threshold.
