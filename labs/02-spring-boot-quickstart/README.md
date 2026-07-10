# Module 2 Lab — Spring Boot Quickstart

## Objectives

By the end of this lab you will have:

- Bootstrapped a Spring Boot service from scratch and understood what each piece of the setup does
- Got a service running locally, responding to a real HTTP request, as fast as possible

## Setup

- Java 21 and Maven installed
- `pom.xml` is given — Spring Boot's dependency management makes this file more boilerplate
  than learning material, so it's provided rather than typed by hand. Everything else in this
  lab, you write yourself.

## Task

### Step 1 — The application entry point

Create `src/main/java/com/fidelity/leap/sprint6/MissionServiceApplication.java`:

- Annotate the class with `@SpringBootApplication`
- Give it a `public static void main(String[] args)` method that calls
  `SpringApplication.run(MissionServiceApplication.class, args)`

### Step 2 — A "hello" endpoint

Create `src/main/java/com/fidelity/leap/sprint6/HelloController.java`:

- Annotate the class with `@RestController`
- Add a method annotated `@GetMapping("/hello")` that returns a `String` greeting of your choice

### Step 3 — Configuration

Create `src/main/resources/application.properties`:

```properties
spring.application.name=mission-service
server.port=8080
```

### Step 4 — Run it

```bash
mvn spring-boot:run
```

In a second terminal:

```bash
curl http://localhost:8080/hello
```

You should see your greeting back.

## A note on what NOT to do

Don't reach for Spring Initializr (start.spring.io) or an IDE wizard for this lab — building the
three files above by hand, understanding what each annotation does, is the actual point. Once
you've done it once by hand, using a generator later will make more sense, not less.

## Deliverable

A running Spring Boot service, with `MissionServiceApplication.java`, `HelloController.java`,
and `application.properties` all present and correct.

## Acceptance criteria

- `mvn spring-boot:run` starts without errors
- `curl http://localhost:8080/hello` (or a browser at the same URL) returns your greeting with
  an HTTP 200
- You can explain, without looking it up, what each of the three parts of `@SpringBootApplication`
  does
