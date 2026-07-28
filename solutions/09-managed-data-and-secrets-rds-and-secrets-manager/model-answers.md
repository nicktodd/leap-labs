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
- The first attempt at a reachability check — a `run-task` **override** of `command` — genuinely
  didn't work: the image's Dockerfile ends `ENTRYPOINT ["java", "-jar", "app.jar"]` (exec form),
  so the override became *extra arguments* appended to that entrypoint. Spring Boot just booted
  normally, ignoring them, and the task sat there `RUNNING` as a web server, never touching the
  database.
- The fix: a small, dedicated task definition with `entryPoint` set directly (there's no
  `run-task` override for `entryPoint` itself). That produced a second real, honest failure:
  `sh: can't create /dev/tcp/...amazonaws.com/5432: nonexistent directory` — `/dev/tcp` is a
  *Bash* built-in, and this image's `sh` is BusyBox `ash` (Alpine base), which doesn't have it.
- BusyBox's own `nc` applet does exist, though (`which nc` confirmed it). Using
  `nc -zv -w 5 <endpoint> 5432` produced a genuine result: `... (10.42.12.68:5432) open` /
  `REACHABLE` — real TCP connectivity, confirming the security group and subnet routing both
  work, independent of whether the application itself can authenticate.

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
