# Module 12 Lab — Containerising Spring Boot Services

## Objectives

By the end of this lab you will have:

- Written a multi-stage Dockerfile for the mission service (build stage separate from the
  runtime image)
- Run Postgres in a container for the first time this sprint (every earlier module used your
  local install), and run the containerised mission service alongside it on a Docker network,
  reaching Postgres by container name rather than `localhost`
- Confirmed that JWT validation needs no network connection to the auth service at all — a
  container that can't even reach `localhost:4000` still validates tokens correctly

## Setup

- Access to your Linux Docker host — connect in your preferred way (see Sprint 1 Module 3) —
  with Java 21 and Maven installed, and your work from Module 11 cloned or copied onto it
- A fresh Postgres 16 container, seeded with the Sprint 3 enterprise schema. Every earlier module
  used your local Postgres install directly; this is the first time Postgres itself runs in a
  container:

  ```bash
  docker run -d --name sprint6-postgres -e POSTGRES_PASSWORD=mission -e POSTGRES_DB=mission \
    -p 5433:5432 postgres:16-alpine
  docker cp ../../../leap-sprint3/shared/enterprise-schema.sql sprint6-postgres:/schema.sql
  docker exec -e PGPASSWORD=mission sprint6-postgres psql -U postgres -d mission -f /schema.sql
  ```

  (If you already created this container earlier, just make sure it's running:
  `docker start sprint6-postgres`.)
- The shared auth stub running on the **Linux host itself** (not containerised this module):
  `cd shared/auth-stub && npm start`
- Given, don't modify: everything under `src/` — this is Module 11's fully working, assembled
  service. Nothing about the application code changes this module.

## Task

### Part A — Write the Dockerfile

Write a multi-stage `Dockerfile` at the root of this lab folder:

- **Stage 1 (`build`)**: base it on `maven:3.9-eclipse-temurin-21`. Copy `pom.xml` first and run
  `mvn -B dependency:go-offline` as its own layer (so Docker can cache downloaded dependencies
  separately from your source code — see Module 11's demo-guide for why that ordering matters).
  Then copy `src/`, and run `mvn -B clean package -DskipTests`.
- **Stage 2 (runtime)**: base it on `eclipse-temurin:21-jre-alpine` — no Maven, no JDK compiler,
  just enough to run a jar. Copy **only** the built jar from stage 1 (`COPY --from=build ...`).
  Expose port `8080` and set the entrypoint to run it.

### Part B — Build and Network It

```bash
docker build -t mission-service:lab .

docker network create mission-net        # if it doesn't already exist
docker network connect mission-net sprint6-postgres   # no-op if already connected

docker run -d --name mission-service-lab --network mission-net -p 8081:8080 \
  -e SPRING_DATASOURCE_URL="jdbc:postgresql://sprint6-postgres:5432/mission" \
  mission-service:lab
```

Notice the datasource URL: inside the Docker network, Postgres is reachable at
`sprint6-postgres:5432` — the container's **name**, and its **internal, unpublished** port. That's
different from every earlier module, where the JDBC URL pointed straight at your local Postgres
install (`localhost:5432`). The container's port is separately published to the host at
`localhost:5433` (see the `-p 5433:5432` in Setup) purely so you can still reach it with
`psql`/pgAdmin from outside the network if you want to — the containerised service itself never
uses that published port; it reaches Postgres by container name instead.

### Part C — Verify

```bash
# No token: 401, before the container even touches Postgres
curl -si -X POST http://localhost:8081/accounts/1/orders \
  -H "Content-Type: application/json" -d '{}'

# A real order, with a real token from the (host-side, NOT containerised) auth stub
TOKEN=$(curl -s -X POST http://localhost:4000/login -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}' | ...extract .token...)

curl -s -H "Authorization: Bearer $TOKEN" -X POST http://localhost:8081/accounts/1/orders \
  -H "Content-Type: application/json" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":5,"price":40.0,"side":"BUY"}'
```

Then confirm the write actually landed:

```bash
docker exec -e PGPASSWORD=mission sprint6-postgres psql -U postgres -d mission -c \
  "SELECT h.account_id, i.ticker, h.quantity FROM holdings h JOIN instruments i ON h.instrument_id=i.instrument_id WHERE h.account_id=1 AND i.ticker='ULVR.L';"
```

## Deliverable

`Dockerfile`, at the root of this lab folder.

## Acceptance criteria

- `docker build` succeeds
- The container starts and stays up (`docker ps` shows it running, not restarting)
- A request with no token returns `401`
- A valid order, submitted with a real token from the host-side auth stub, returns `200` and the
  new holding quantity is genuinely persisted in Postgres — confirmed by querying the database
  directly, not just trusting the HTTP response
