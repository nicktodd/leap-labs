# Lab 9 - Managed Data & Secrets: RDS & Secrets Manager

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. Module 3's
VPC, Module 7's cluster and execution role, and Module 8's PrivateLink setup should already be in
place.

## Task

### Part 1: A private RDS instance

A production RDS instance belongs in a private subnet, never a public one - a database should
never be directly reachable from the internet, only through the application tier in front of it.

1. Create a DB subnet group from the two **private** subnets.
2. Create a security group for the database, allowing inbound `5432` only from your app
   security group - not from any CIDR block.
3. Create a `db.t3.micro` Postgres instance, `--no-publicly-accessible`, using
   `--manage-master-user-password` rather than supplying a password yourself.
4. Wait for the instance to reach `available`, and note its endpoint.

### Part 2: Find the secret AWS created for you

5. Run `describe-db-instances` and find the `MasterUserSecret.SecretArn` AWS generated
   automatically. Confirm the secret exists with `secretsmanager describe-secret` - without
   printing its actual value to your terminal.

### Part 3: Grant the execution role read access, scoped to this one secret

6. Attach a policy to your execution role granting `secretsmanager:GetSecretValue`, with
   `Resource` set to this one secret's ARN specifically - not `"*"`.
7. Register a new revision of your task definition adding a `secrets` entry for the database
   password (`valueFrom` the secret ARN) and `environment` entries for the host, port, database
   name, and username (none of these are secret - only the password is).

### Part 4: Verify real reachability

8. Create a small, dedicated task definition (reusing your mission-service image) with
   `entryPoint` set to `["sh", "-c"]` and `command` set to a real TCP check against your
   database's endpoint on port 5432 (BusyBox's `nc -zv -w 5 <host> <port>` needs no extra
   tooling in the image).
9. Run it in a **private** subnet with your app security group - confirm a genuine `open` /
   `REACHABLE` result in its CloudWatch logs.

## Verify

Compare your work against `solutions/09-.../model-answers.md`. Your RDS instance should be
`available` and not publicly accessible, a Secrets Manager secret should hold its password (never
typed or scripted by you directly), your execution role's policy should be scoped to that one
secret's ARN, and your reachability check should succeed.

## Cleanup

The RDS instance is billed for as long as it exists - delete it once you're done
(`--skip-final-snapshot` for this training account; a real production database would need a
snapshot policy). Deleting an RDS instance with a managed master password also deletes its
associated secret automatically. Remove the inline policy from your execution role. Leave the DB
subnet group and RDS security group in place - they cost nothing idle and Module 11's automation
can reuse them.

## A Question Worth Sitting With

`--manage-master-user-password` puts the *master* user's password in Secrets Manager
automatically. A real application, though, usually shouldn't connect as the master user at all -
why not, and what would you create instead?

## A Second Question Worth Sitting With

The task definition's `DB_HOST`, `DB_PORT`, and `DB_NAME` values are plain `environment` entries,
not secrets - but they could just as easily have come from AWS Systems Manager Parameter Store
instead of being hardcoded in the task definition itself. Parameter Store's standard tier is
free, unlike Secrets Manager. Given that, why did this module still use Secrets Manager for the
database *password* specifically, rather than Parameter Store?
