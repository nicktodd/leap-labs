# Demo: Module 11 — Docker Fundamentals

**Duration:** 12 minutes
**Prerequisite:** Docker Desktop 27.x running. IntelliJ with Copilot Chat open.
`unfamiliar-multistage-dockerfile.txt` open in the editor. A locally built
`sprint1-greeter-app-0.1.0.jar` from the `starter/` project (run `mvn clean package` first).

## Part 1: Containers vs VMs (2 min)

Narration, pointing at the diagram on the slides: a VM virtualises hardware, so each VM carries
a full guest operating system, that's slow to start and heavy on resources. A container
virtualises the operating system instead: every container on a host shares that host's OS
kernel, and only packages the application and its dependencies. That's why containers start in
milliseconds and a laptop can comfortably run dozens of them, where it might struggle with more
than two or three VMs.

## Part 2: Images vs containers (2 min)

```bash
docker images
docker ps -a
```

Narration: an **image** is a read-only template, built once from a Dockerfile. A **container**
is a running (or stopped) instance created from an image. The relationship is exactly like a
class and an object: one image, many containers can run from it at once, each isolated from the
others.

## Part 3: Explaining an unfamiliar Dockerfile with GenAI (4 min)

With `unfamiliar-multistage-dockerfile.txt` open, select the whole file and ask Copilot Chat:

```text
Explain what each instruction in this Dockerfile does, and why it uses two FROM lines.
```

Narration: read the explanation aloud. It should describe a **multi-stage build**: the first
stage compiles the Java project using a full Maven+JDK image, the second stage starts fresh
from a much smaller JRE-only image and copies in just the built jar. Critique it: does it
explain *why* this is smaller than shipping the Maven/JDK image itself? If not, prompt again or
fill the gap yourself, same habit as Module 05 and Module 10.

## Part 4: Writing your own minimal Dockerfile (3 min)

For the `starter/` project (already built locally, so no multi-stage build needed yet):

```dockerfile
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY target/sprint1-greeter-app-0.1.0.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

```bash
docker build -t sprint1-greeter-app .
docker run -d --name greeter sprint1-greeter-app
docker ps
docker logs greeter
docker exec -it greeter sh
```

Narration: `build` creates the image, `run` creates and starts a container from it, `-d` runs it
in the background. `ps` lists running containers, `logs` shows what it's printed,`exec -it ...
sh` gets you an interactive shell inside the running container, useful for poking around when
something isn't behaving as expected.

## Key message

Understand the image/container split before you touch Docker commands: build makes an image,
run makes a container from it. Use GenAI to fast-track understanding unfamiliar Dockerfile
syntax, same explain-then-verify habit as every other module this week.
