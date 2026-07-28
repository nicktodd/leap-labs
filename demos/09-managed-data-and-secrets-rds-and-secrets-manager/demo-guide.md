# Module 9 Demo Guide — Managed Data & Secrets: RDS & Secrets Manager

**Duration:** 55 minutes
**Prerequisite:** Module 3's `leap-mission-vpc`, Module 7's cluster and execution role, Module 8's
PrivateLink endpoints, all still in place.

## Part 0: What's Missing So Far (5 min)

Every module up to now has been stateless: the mission-service container itself holds no data
between requests. A real backend needs somewhere durable to keep data, and — just as
importantly — a way to give the application that database's credentials without ever writing
them into a Dockerfile, a task definition, or source control. Two AWS services solve this: **RDS**
(a managed relational database) and **Secrets Manager** (for the credentials that reach it).

## Part 0b: What RDS Actually Is (8 min)

RDS (Relational Database Service) runs a real database engine — the same engine you'd install
yourself — on infrastructure AWS manages for you. It supports several engines directly: MySQL,
PostgreSQL, MariaDB, Oracle, and SQL Server, plus Aurora, AWS's own MySQL- and
PostgreSQL-compatible engine built for higher throughput and faster failover. Whatever engine you
pick, you connect to it exactly the way you always have — the same driver, the same connection
string shape, the same SQL — nothing about the application's own database code needs to change to
use RDS instead of a self-hosted database.

What "managed" actually buys: automated backups and point-in-time restore, automated engine
patching on a schedule you control, optional Multi-AZ deployments that fail over to a standby
automatically if the primary instance has a problem, and CloudWatch metrics out of the box — all
work a team would otherwise do by hand on a self-hosted database. Underneath, an RDS instance is
still a real virtual machine running the engine, placed inside your own VPC like any other
resource, reachable over the network the same way EC2 or ECS is — which is exactly why it needs
a subnet group and a security group, just like everything else this sprint has provisioned.

## Part 1: A Private RDS Instance (15 min)

**A production RDS instance belongs in a private subnet, never a public one** — there is no
legitimate reason for a database to be reachable directly from the internet; every access path
should go through the application tier that already sits in front of it. RDS needs to know which
subnets it's allowed to place its instance in — a **DB subnet group**, built from the same
private subnets everything else in this sprint has used:

```bash
aws rds create-db-subnet-group --db-subnet-group-name leap-mission-db-subnets \
  --db-subnet-group-description "Private subnets for the mission database" \
  --subnet-ids <private-subnet-a> <private-subnet-b>
```

A dedicated security group, following exactly the least-privilege pattern from Module 3: allow
`5432` only from the app tier's security group, not from any CIDR block at all:

```bash
aws ec2 create-security-group --group-name leap-rds-sg --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <rds-sg-id> --protocol tcp \
  --port 5432 --source-group <app-sg-id>
```

Then the instance itself, using `--manage-master-user-password` rather than passing a password
on the command line at all:

```bash
aws rds create-db-instance --db-instance-identifier leap-mission-db \
  --db-instance-class db.t3.micro --engine postgres --engine-version 18.4 \
  --allocated-storage 20 --storage-type gp3 --master-username missionadmin \
  --manage-master-user-password \
  --db-subnet-group-name leap-mission-db-subnets \
  --vpc-security-group-ids <rds-sg-id> --no-publicly-accessible \
  --backup-retention-period 0 --no-multi-az
```

Real output: `DBInstanceStatus: creating`, moving to `available` after several minutes.
`--no-publicly-accessible` means this database has no public IP and no route to the internet at
all — reachable only from inside the VPC, and even then only from something carrying the app
security group.

## Part 2: What `--manage-master-user-password` Actually Did (10 min)

```bash
aws rds describe-db-instances --db-instance-identifier leap-mission-db \
  --query 'DBInstances[0].MasterUserSecret'
```

Real output: a `SecretArn` — AWS generated a real, random password and stored it directly in
Secrets Manager, without it ever appearing in a CLI command, a script, or this terminal's
history. Confirm the secret itself exists, without revealing its value on screen:

```bash
aws secretsmanager describe-secret --secret-id <secret-arn> \
  --query '{Name:Name,LastRotated:LastRotatedDate}'
```

This is the pattern worth landing: a password that's never typed by a human, never committed to
a repository, and never hardcoded into a container image — generated once by AWS, stored once by
AWS, and read only by the specific IAM identities explicitly granted permission to read it.

## Part 2b: Secrets Manager vs. Parameter Store (5 min)

Secrets Manager isn't the only place to keep this kind of value. **AWS Systems Manager Parameter
Store** can store the exact same kind of value (a `SecureString` parameter, encrypted with KMS)
and a task definition's `secrets` field can read from either service interchangeably.

The real difference is cost and rotation, and it's worth being explicit about both:

- **Cost**: Parameter Store's *standard* tier is free — no per-parameter monthly charge, no API
  charge for standard throughput. Secrets Manager charges per secret per month (roughly $0.40)
  plus a small charge per API call. For a large number of simple values, that adds up.
- **Rotation**: Secrets Manager can **automatically rotate** a credential on a schedule — for an
  RDS secret specifically, AWS provides a ready-made Lambda rotation function that changes the
  database password *and* updates the secret, with no application downtime. Parameter Store has
  **no built-in rotation at all** — a `SecureString` parameter's value only ever changes when
  something (a person, a script) explicitly updates it.

The practical guideline: Parameter Store is the right, free choice for configuration values that
rarely change and don't need automatic rotation — the `DB_HOST`/`DB_PORT`-style values in this
module's task definition are a reasonable candidate. A database credential that should rotate on
a schedule, like this module's master password, is exactly the case Secrets Manager's extra cost
is buying you protection against.

## Part 3: Getting the Secret Into the Task — the Execution Role, Again (12 min)

Module 7 drew a distinction between the execution role (ECS's own identity, pulling images and
writing logs) and the application's own permissions. Reading a secret to inject as an environment
variable is *also* the execution role's job — it happens before the application code starts, the
same way pulling the image does:

```bash
aws iam put-role-policy --role-name leap-ecs-task-execution-role \
  --policy-name leap-read-db-secret \
  --policy-document '{"Version":"2012-10-17","Statement":[{
    "Effect":"Allow","Action":"secretsmanager:GetSecretValue",
    "Resource":"<secret-arn>"}]}'
```

Scoped to this one secret's ARN specifically — not `"Resource": "*"` — following the same
least-privilege instinct as every security group rule so far this sprint.

The task definition's `secrets` field (distinct from `environment`) references it directly:

```json
"secrets": [
  {"name": "DB_PASSWORD", "valueFrom": "<secret-arn>"}
],
"environment": [
  {"name": "DB_HOST", "value": "<rds-endpoint>"},
  {"name": "DB_PORT", "value": "5432"},
  {"name": "DB_NAME", "value": "postgres"},
  {"name": "DB_USERNAME", "value": "missionadmin"}
]
```

ECS resolves `secrets` entries at task startup, using the execution role's permissions, and
injects the resolved value as a real environment variable inside the container — the application
code reads `DB_PASSWORD` like any other environment variable and never calls the Secrets Manager
API itself.

## Part 4: Verified — Real Network Reachability (10 min)

Rather than assume the security group and subnet placement are correct, test them directly, the
same discipline Module 7 used for the container's own port — a simple TCP check against the
database's endpoint and port, run as a one-off ECS task carrying the app tier's security group:

```bash
aws ecs register-task-definition --cli-input-json file://connectivity-check-taskdef.json
# entryPoint: ["sh","-c"], command: ["nc -zv -w 5 <rds-endpoint> 5432 && echo REACHABLE || echo UNREACHABLE"]

aws ecs run-task --cluster leap-mission-cluster \
  --task-definition leap-db-connectivity-check --launch-type FARGATE \
  --network-configuration 'awsvpcConfiguration={subnets=[<private-subnet>],securityGroups=[<app-sg-id>],assignPublicIp=DISABLED}'
```

Real output in CloudWatch Logs:

```
leap-mission-db...amazonaws.com (10.42.12.68:5432) open
REACHABLE
```

Genuine TCP connectivity from a task carrying the app security group to the database on port
5432 — confirming the security group rule and subnet routing are both correct, independent of
whether the application code itself ever authenticates successfully. This check runs in a
**private** subnet, the same one the real application tier uses — there's no need for the
checking task to be in a public subnet at all, since it only needs to reach another resource
inside the same VPC.

## Key Message

A managed database and a managed secret solve two different problems that are easy to conflate:
RDS handles the data's durability and availability; Secrets Manager handles never letting a
credential exist anywhere a human or a source-control system could see it. `--manage-master-user-
password` ties them together at creation time, and the execution role — already ECS's identity
for pulling images and writing logs — is the natural, least-surprising place for "read this one
secret" to live too. Secrets Manager's monthly cost buys something Parameter Store's free tier
doesn't: automatic rotation — worth paying for on a credential, not on every piece of
configuration.

## Transition to the Lab

Candidates provision their own RDS instance and secret, grant their own execution role read
access scoped to that one secret, update a task definition to use it, and verify real TCP
reachability the same way.
