# Module 06 Lab — Refactor to a Multi-Stage Docker Build

## Recap: where we left off in Sprint 1

- **Module 11 (Docker Fundamentals)**: containers vs VMs, images vs containers, a minimal
  single-stage Dockerfile, and a multi-stage example GenAI explained but you didn't write
- **Module 13 (Containerising the Project Skeleton)**: used that single-stage pattern to
  containerise your actual team project, plus a Jenkinsfile to build and smoke-test it

This lab has you write the multi-stage version for real, then go further with best practices,
networking, and docker-compose.

## Objectives

By the end of this lab you will have:

- Refactored a single-stage Dockerfile into a multi-stage build
- Verified the resulting image is smaller
- Applied Dockerfile best practices: layer caching, a least-privilege user, a minimal base image
- Run a multi-container set-up with docker-compose, and checked basic networking

## Setup

- Access to your Linux Docker host — connect in your preferred way (see Sprint 1 Module 3)
- The [`starter/`](starter) folder from this lab, cloned or copied onto the Linux host — a copy
  of the Sprint 1 project skeleton with its original single-stage `Dockerfile`

## Task sheet

### Part A — Baseline

1. In `starter/`, build the jar locally (`mvn clean package`), then build the existing
   single-stage image: `docker build -t team-skeleton:baseline .`
2. Note its size from `docker images`.

### Part B — Refactor to multi-stage

3. Rewrite `Dockerfile` as a multi-stage build:
   - **Build stage**: starts `FROM maven:3.9-eclipse-temurin-21 AS build`, copies `pom.xml`
     first, then `src/`, and runs `mvn -B clean package -DskipTests`
   - **Runtime stage**: starts fresh `FROM eclipse-temurin:21-jre-alpine`, copies only the built
     jar from the build stage with `COPY --from=build`
4. Apply two further best practices in the runtime stage:
   - Create and switch to a non-root user (`addgroup`/`adduser`, then `USER <name>`)
   - Confirm the base image stays JRE-only, not JDK, in the final stage
5. Build the new image: `docker build -t team-skeleton:multistage .`
6. Compare `docker images` output for `team-skeleton:baseline` vs `team-skeleton:multistage`.
   Note the size difference and explain, in your own words, why the multi-stage version is
   smaller.

### Part C — docker-compose, networking, and the up/down lifecycle

7. Write a `docker-compose.yml` with two services: your app (`build: .`) and a `db` service
   using the official `postgres:16-alpine` image, with a password set via environment variable
   and port `5432` mapped to the host.

8. **Bring it up** with `docker compose up -d`, and confirm both containers are running with
   `docker compose ps`.

9. **Inspect the network docker-compose created for you:**
   ```bash
   docker network ls
   docker network inspect <project-name>_default
   ```
   Find both your `app` and `db` containers listed under that network's containers, note the
   private IP address each one has been given, these addresses are internal to Docker and
   don't mean anything on your host machine's network.

10. **Confirm DNS-based service discovery**: from inside the app container (`docker exec -it
    <container> sh`), confirm you can resolve the `db` service by hostname (e.g. `getent hosts
    db`). This is docker-compose's bridge network doing name resolution for you, `db` is not an
    IP address anyone hardcoded, it's the service name from `docker-compose.yml`.

11. **Confirm host port mapping**: from your Linux Docker host itself (outside any container —
    e.g. the same shell you ran `docker compose up` from), confirm you can connect to Postgres
    on the mapped port, for example with a Postgres client pointed at `localhost:5432`, or
    `docker exec` into the `db` container and connect to `localhost` from there instead, and
    compare. Note that only the `db` service is reachable from the host, because only it has a
    `ports:` mapping, the `app` service does not, and isn't reachable from outside Docker at all
    unless you add one.

12. **Bring it down**: run `docker compose down` and observe what happens.
    - Run `docker compose ps` again, both containers should be gone.
    - Run `docker network ls` again, the project's network should be gone too.
    - Note that `docker compose down` does **not** remove the Postgres data by default, run
      `docker compose down -v` instead and note that this additionally removes the named
      volume, meaning next time you run `up` the database starts completely empty.

13. **Bring it back up and confirm it's the same picture**: run `docker compose up -d` again,
    and repeat step 9's network inspection. You should see a freshly created network with new
    container IPs, `up` and `down` are not "pause" and "resume", they create and destroy things.

## Acceptance criteria

- `team-skeleton:multistage` builds successfully and is measurably smaller than
  `team-skeleton:baseline`.
- The Dockerfile shows evidence of layer caching (separate `COPY pom.xml` / `COPY src`), a
  non-root `USER`, and a JRE-only final base image.
- `docker compose up -d` brings up both services, and you've demonstrated both bridge-network
  name resolution and host port mapping.
- You can explain, in your own words, the difference between `docker compose down` and
  `docker compose down -v`, and why only `db` (not `app`) is reachable from the host.

If you finish early, try changing only a Java source file and rebuilding, does Docker skip the
Maven dependency download step? That's layer caching working as intended.
