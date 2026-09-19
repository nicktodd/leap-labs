# Demo: Module 06 — Containerisation Deeper Dive

**Duration:** 12 minutes
**Prerequisite:** Docker Desktop running. The `starter/` project from this lab. GitHub Copilot
Chat available.

## Part 1: Recap, quickly (2 min)

Narration: Sprint 1 Module 11 covered containers vs VMs and images vs containers, and had you
write a minimal single-stage Dockerfile, copying in a jar you'd already built locally with
Maven. Module 11 also showed (but didn't have you write) a multi-stage example, using GenAI
just to explain what it did. Module 13 then used that same single-stage pattern to containerise
your team's actual project skeleton. Today, you write the multi-stage version yourself, for
real, and go further: best practices, networking, and docker-compose.

## Part 2: Why multi-stage? (2 min)

```bash
docker images
```

Show the current single-stage image size. Narration: this image only contains a JRE and a jar,
because the jar was built locally, outside Docker, before `docker build` ever ran. That's fine
for a skeleton, but it means the *build* isn't reproducible from the Dockerfile alone, anyone
without Maven configured identically to yours could get a different jar. A multi-stage build
fixes that: the build step happens *inside* Docker too, using a full Maven+JDK image, and only
the final runtime stage (JRE + jar) ships.

## Part 3: Writing the multi-stage Dockerfile (4 min)

```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /src
COPY pom.xml .
COPY src ./src
RUN mvn -B clean package -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=build /src/target/team-skeleton-0.1.0.jar app.jar
USER appuser
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Narration, pointing out three best practices:
- **Layer caching**: `COPY pom.xml .` happens before `COPY src ./src`, so Docker only re-downloads
  dependencies when `pom.xml` changes, not on every source edit
- **Least-privilege user**: a non-root `appuser` runs the application, so a container escape
  doesn't hand an attacker root
- **Minimal base image**: the final stage never contains Maven or the JDK, only what's needed
  to run

```bash
docker build -t team-skeleton:multistage .
docker images
```

Compare the size against the original image.

## Part 4: docker-compose, up, and the network it creates (4 min)

```bash
docker compose up -d
docker compose ps
docker network ls
```

Narration: `docker compose up` does three things: creates a private **bridge network** scoped
to this project, creates a container for every service, and starts them all. `docker network
ls` shows the network it just created, named after the project folder by default.

```bash
docker network inspect <project-name>_default
```

Narration: this shows every container attached to the network and the private IP address each
one has been given. These IPs mean nothing outside Docker, containers use them (or, more
usually, the service name) to talk to each other, your host machine doesn't use them at all.

```bash
docker exec -it <app-container> sh -c "getent hosts db"
```

Narration: `db` resolves because `docker-compose` runs DNS for the containers it manages,
`app` never hardcodes an IP, it just uses the service name from `docker-compose.yml`. This is
**service discovery**, and it's the main reason people reach for compose over plain `docker
run` the moment more than one container needs to talk to another.

Contrast this with the `ports:` mapping: only `db` has one, so only `db` is reachable from the
host machine on `localhost:5432`. `app` has no `ports:` entry, so it's invisible from outside
Docker entirely, even though it's fully reachable from `db` inside the bridge network.

## Part 5: Tearing it down (2 min)

```bash
docker compose down
docker compose ps
docker network ls
```

Narration: `down` is the mirror image of `up`, it stops every container, removes them, and
removes the network `up` created. Point out that `docker compose ps` now shows nothing, and the
project's network is gone from `docker network ls` too, this is destruction, not pausing.

```bash
docker compose down -v
```

Narration: plain `down` leaves named volumes alone, so a database's data survives being brought
down and back up. `down -v` additionally removes those volumes, the next `up` starts from a
completely empty database. Worth doing deliberately once, so it's an informed choice later, not
a surprise the first time someone loses local data by habit.

## Key message

Sprint 1's Dockerfile got you a working container. Sprint 2's deeper dive gets you one that's
reproducible from source, smaller, safer to run, and able to talk to other containers, the
shape a real team's Dockerfile actually needs to take.
