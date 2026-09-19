# Lab 10 — Observability & Cost Awareness

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. This
module deliberately reuses metrics, logs, and cost data your account has already generated in
earlier modules — no new infrastructure needs to exist first.

## Task

### Part 1: What CloudWatch already knows

1. List the CloudWatch metrics ECS has already published for your cluster
   (`aws cloudwatch list-metrics --namespace AWS/ECS`). Note which metrics exist even though no
   task may be running right now.
2. Run a CloudWatch Logs Insights query against your mission-service log group, filtering for an
   event from an earlier module (a startup line, an error, or similar) over the last 7 days.

### Part 2: An alarm and dashboard

3. Create a CloudWatch alarm on your cluster's `CPUUtilization`, with `--treat-missing-data
   notBreaching`. Before you run it, work out which of the three alarm states (`OK`, `ALARM`,
   `INSUFFICIENT_DATA`) you expect it to show, and why — then check whether it matches.
4. Build a CloudWatch dashboard combining at least one metric widget and your Logs Insights
   query from Part 1 as a log widget.

### Part 3: Cost data

5. Query Cost Explorer for your account's actual spend by service over the last 14 days
   (`aws ce get-cost-and-usage`). Identify which service line corresponds to which earlier
   module's work.
6. These numbers will be small, because the billed resources were torn down shortly after each
   verification — not because they're actually cheap to run. For each billed service (NAT
   Gateway, ALB, ECS, VPC endpoints, RDS), look up AWS's published `us-east-1` hourly rate and
   calculate what running it continuously for 30 days (730 hours) would really cost. Compare that
   to simply scaling your 14-day figure by 30/14 — which number is more useful for planning a
   real budget, and why?
7. Create a monthly AWS Budget with an alert threshold (e.g. 80% of a $10 limit), notifying an
   email address.

## Verify

Compare your work against `solutions/10-.../model-answers.md`. Your dashboard should render
metric and log data, your alarm should show one of the three valid states depending on what's
currently running, and your Cost Explorer query should return actual numbers for your own
account.

## Cleanup

Dashboards, alarms, and budgets cost nothing to keep — AWS Budgets is free for the first two
budgets per account, and CloudWatch alarms/dashboards have no charge for a small number of them.
Leave all of this module's resources in place.

## A Question Worth Sitting With

Your Cost Explorer query should show an `Amazon Virtual Private Cloud` line from Module 8's
PrivateLink endpoints, and little or nothing under `EC2 - Other` (which is where NAT Gateway
hours would show up). If a teammate's account showed the opposite — an `EC2 - Other` charge and
no VPC endpoint charge — what would that tell you about which networking approach they used for
that same problem, without needing to ask them directly?
