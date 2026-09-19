# Lab 9 Model Answers

## Verified Output

Run for real, building on Module 3's VPC and Module 7's cluster and execution role:

- `aws rds create-db-instance --manage-master-user-password`: real `DBInstanceStatus: creating`
  → `available` after several minutes, `--no-publicly-accessible`, no route to the internet.
- `describe-db-instances` showed a real `MasterUserSecret.SecretArn` — AWS generated and stored
  the password directly, with no password ever typed, scripted, or committed by hand.
- An inline execution-role policy granting `secretsmanager:GetSecretValue`, `Resource` scoped to
  that one secret's ARN specifically.
- A new task definition revision with a `secrets` entry (`DB_PASSWORD`, `valueFrom` the secret
  ARN) alongside plain `environment` entries for host, port, database name, and username.
- A dedicated task definition, `entryPoint` set to `["sh", "-c"]` and `command` running
  `nc -zv -w 5 <endpoint> 5432`, run in a **private** subnet with the app security group: real
  CloudWatch output — `... (10.42.12.68:5432) open` / `REACHABLE` — genuine TCP connectivity,
  confirming the security group and subnet routing both work, independent of whether the
  application itself can authenticate.

## The Reflection Question

Connecting as the master user for day-to-day application traffic means the application holds the
same permissions used to administer the database itself — create and drop other users, change
permissions, alter the schema in ways the application was never meant to. It also means every
application instance shares one identity, with no way to revoke a single compromised
application's access without also cutting off the master user's own administrative access.

The better pattern: create a dedicated application user, with only the specific privileges the
application actually needs (typically `SELECT`, `INSERT`, `UPDATE`, `DELETE` on its own tables,
nothing at the database-administration level), and store *that* user's credentials in their own
Secrets Manager secret — separate from the master user's. The master user's credentials
(AWS-managed here) stay reserved for genuine administrative tasks: creating the application user
in the first place, running migrations, or emergency access — not for the application's everyday
traffic.

## The Second Reflection Question

Cost isn't the only factor, and for a database password specifically it isn't even the deciding
one: Secrets Manager can **automatically rotate** a credential on a schedule, with a ready-made
Lambda rotation function for RDS specifically that changes the database password *and* updates
the secret together, with no application downtime. Parameter Store has no equivalent — a
`SecureString` parameter's value only changes when something explicitly updates it.

A database password is exactly the kind of value that benefits from rotating regularly without
manual intervention — the security value of automatic rotation is worth Secrets Manager's small
monthly cost. `DB_HOST`, `DB_PORT`, and `DB_NAME`, by contrast, rarely if ever change and don't
need rotation at all — Parameter Store's free standard tier is the better fit for values like
those, and using Secrets Manager for everything would just be paying for a capability those
particular values never use.
