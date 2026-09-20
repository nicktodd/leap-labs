# Module 12 - Model Answers & Notes

## The Dockerfile

```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /build

COPY pom.xml .
RUN mvn -B dependency:go-offline

COPY src ./src
RUN mvn -B clean package -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

COPY --from=build /build/target/missionservice-m12-lab.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

(Substitute your own `<finalName>` from `pom.xml` in the `COPY --from=build` line - it must match
exactly, or the build fails with a "file not found" error at that step.)

## Why the Dependency Layer Matters

Without the `COPY pom.xml` / `dependency:go-offline` split, a single Dockerfile instruction like
`COPY . .` followed by `mvn package` means Docker's layer cache invalidates on **any** file
change - including a one-line change to a Java file that has nothing to do with dependencies.
Every rebuild then re-downloads the entire Maven dependency tree from scratch. Splitting `pom.xml`
out first means that layer only invalidates when `pom.xml` itself changes - which is rare compared
to source code changes.

## Why `SPRING_DATASOURCE_URL` "Just Works"

Spring Boot's relaxed binding automatically maps environment variables to properties:
`spring.datasource.url` becomes `SPRING_DATASOURCE_URL` (dots become underscores, everything
uppercased). Environment variables take precedence over `application.properties`, so passing
`-e SPRING_DATASOURCE_URL=...` at `docker run` time overrides the file's value with no code change
and no rebuild required. This is exactly the same mechanism the Foundations/Pipelines weeks' CI/CD modules used to
inject different config per environment - it isn't new to containers, containers are just where
you'll use it most.

## Why This Container Can Validate Tokens Without Reaching the Auth Stub

`mission-net` doesn't include the auth stub - it's deliberately still running on the host, outside
Docker entirely. If JWT validation required a live call back to the auth service, this setup would
fail immediately. It doesn't, because Module 9's `SecurityConfig` only ever needed the shared
secret to check a signature locally. This is worth calling out as the payoff of a design decision
made three modules ago, not a new feature - containerising the service didn't require touching
security at all.
