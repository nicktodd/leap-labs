# Module 12 Demo Guide — Containerising Spring Boot Services

Module 11's assembled service, unchanged. Today it just runs somewhere else.

## The Dockerfile, Two Stages

Open `Dockerfile`.

```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /build
COPY pom.xml .
RUN mvn -B dependency:go-offline
COPY src ./src
RUN mvn -B clean package -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /build/target/sprint6-m12-demo.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Two things worth stopping on:**

1. **`pom.xml` copied and dependencies fetched BEFORE `src/`.** Docker caches each instruction as
   a layer. As long as `pom.xml` doesn't change, `dependency:go-offline`'s layer is reused from
   cache on every rebuild — only source-code changes trigger a re-download. Getting this ordering
   wrong (copying everything at once) means every single code change re-downloads the entire
   dependency tree.
2. **`COPY --from=build`.** Only the built jar crosses from stage 1 into stage 2. The final image
   never contains Maven, the JDK compiler, or the source code — just a JRE and one jar file.
   Build the image and run `docker images` to see the size difference for yourself.

## Build It

```bash
docker build -t mission-service:m12 .
docker images | grep mission-service
```

## Networking: Container-to-Container, Not `localhost`

```bash
docker network create mission-net
docker network connect mission-net sprint6-postgres

docker run -d --name mission-service-m12 --network mission-net -p 8081:8080 \
  -e SPRING_DATASOURCE_URL="jdbc:postgresql://sprint6-postgres:5432/mission" \
  mission-service:m12
```

Point at `SPRING_DATASOURCE_URL`. Every module until now used `localhost:5433` — the **published**
port on the host. Inside a Docker network, containers reach each other by **container name** and
the **internal** port (`5432`, not `5433`). This is Spring Boot's standard environment-variable
override (`spring.datasource.url` → `SPRING_DATASOURCE_URL`) — no code change, no rebuild, just a
different value at `docker run` time. This is the same 12-factor idea from Sprint 1/2's CI/CD
modules, applied to a container instead of a Jenkins job.

## Prove the JWT Point From Module 9, Again

```bash
curl -si -X POST http://localhost:8081/accounts/1/orders -H "Content-Type: application/json" -d '{}'
# 401 - no network call to the auth stub happened at all
```

**Say this explicitly**: the auth stub is running on the *host*, not in this Docker network. The
container can't even reach it. And yet JWT validation still works correctly — because, exactly as
Module 9 taught, the mission service never calls the auth service at request time. It only needs
its own copy of the shared secret, baked into the image via `application.properties` (or, in a
real deployment, injected as an environment variable from a secrets manager).

Then get a real token from the auth stub running on the host, and submit a real order through the
containerised service:

```bash
TOKEN=$(curl -s -X POST http://localhost:4000/login -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}' | ...extract .token...)

curl -s -H "Authorization: Bearer $TOKEN" -X POST http://localhost:8081/accounts/1/orders \
  -H "Content-Type: application/json" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":5,"price":40.0,"side":"BUY"}'
```

Then confirm it actually landed in Postgres, from a completely different machine than the one
that wrote it:

```bash
docker exec -e PGPASSWORD=mission sprint6-postgres psql -U postgres -d mission -c \
  "SELECT h.account_id, i.ticker, h.quantity FROM holdings h JOIN instruments i ON h.instrument_id=i.instrument_id WHERE h.account_id=1 AND i.ticker='ULVR.L';"
```

## Transition to the Lab

Learners write the Dockerfile themselves, following the same two-stage pattern, and run it on the
same network against the same Postgres container.
