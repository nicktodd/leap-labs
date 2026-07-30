# Lab 12 Model Answers

## Verified Output

Run for real, auditing the whole sprint's accumulated AWS activity at once:

- `ecs list-services --cluster leap-mission-cluster`: empty — no ECS service currently running.
- `rds describe-db-instances`: empty — Module 9's instance was deleted after verification.
- `describe-nat-gateways` (state `available`/`pending`): empty — Module 8's NAT Gateway attempt
  was deleted once PrivateLink replaced it.
- `describe-load-balancers`: empty — Module 8's ALB was deleted after verification.
- What remains, all free: the `leap-mission-cluster` cluster, the `leap-ecs-task-execution-role`
  and `leap-jenkins-deploy-role` roles, both ECR repositories (10 images total), the S3 gateway
  endpoint, the `leap-mission-observability` dashboard, the `leap-mission-high-cpu` alarm, and the
  `leap-mission-monthly-budget` budget.
- The alarm's state moved from `INSUFFICIENT_DATA` (Module 10, no data existed yet) to `OK`
  (now) — Module 11's task runs since then gave it real CPU data points to evaluate, all below
  the 80% threshold.

This is the expected clean state: every module's cleanup section worked as intended, and nothing
billed was left running by accident.

## Part 2 & 3

There's no single correct answer for a capstone-specific pipeline or a personal showcase
narrative — what a reviewer should check for:

- The pipeline genuinely builds and deploys the candidate's own capstone code, not just a copy of
  the baseline mission's Jenkinsfile with nothing changed.
- The Acceptance Tests stage includes a check specific to the capstone feature, not only Sprint
  9's original login flow.
- The Copilot/code-quality answer names a specific suggestion and a specific way it was verified
  or corrected — not a general statement like "Copilot helped me code faster."
- The DevOps automation answer names a specific risk the pipeline prevented or caught — not a
  general statement like "I automated my deployment."

## The Reflection Question

Answers will vary by capstone extension. A strong answer identifies something in the extension's
actual requirements that didn't map cleanly onto the baseline pattern — for example, a feature
needing its own database table (a schema migration step the baseline pipeline never needed), a
feature calling a genuine third-party API (requiring a NAT Gateway or an additional PrivateLink
endpoint the baseline never needed, exactly the trade-off Module 3 and Module 8 covered), or a
feature needing a different task sizing (more CPU/memory than the baseline's `256`/`512`). The
point of the question isn't to find a flaw in the mission brief's claim — it's to confirm the
deployment steps were understood well enough to recognise where they needed a real, deliberate
decision rather than being copied unchanged.
