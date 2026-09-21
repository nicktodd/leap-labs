# LEAP Labs

Monorepo for the LEAP training programme: the group project guidance and all per-week technical
labs.

Some folders below were originally merged in with `git subtree`, preserving their original
commit history - check `git log --follow` on a given folder if you need that history.

## Structure

| # | Folder | Week |
|---|---|---|
| 1 | [`foundations/`](foundations) | Foundations - Git, ways of working & GenAI |
| 2 | [`pipelines/`](pipelines) | Pipelines - CI/CD, containers, infrastructure & security |
| 2 | [`data/`](data) | Data Systems - Postgres, SQL, modelling |
| 3 | [`java/`](java) | Java |
| 4 | [`spring/`](spring) | Spring Boot |
| 5 | [`angular/`](angular) | Angular |
| 6 | [`node/`](node) | Node.js / NestJS |
| 7 | [`python/`](python) | Python & data analytics |
| 8 | [`kafka/`](kafka) | Kafka & enterprise data engineering |
| 10 | [`cloud/`](cloud) | AWS cloud deployment |
| - | [`project/`](project) | The group project: kickoff spec and Friday-by-Friday instructor guidance, run alongside the weeks above |

Pipelines and Data run in the same week (2), split across two parallel tracks. Week 9 is
deliberately unscheduled as technical content - candidates spend it on the group project
instead.

Each subfolder has its own `README.md` describing that week's modules, labs, and demos in
detail, generally split into `demos/`, `labs/`, and `solutions/`.
