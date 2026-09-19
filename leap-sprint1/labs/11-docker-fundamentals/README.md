# Module 11 Lab — Docker Fundamentals

## Objectives

By the end of this lab you will have:

- Explained the difference between containers and VMs, and images and containers
- Used GenAI to explain an unfamiliar multi-stage Dockerfile
- Written your own minimal Dockerfile for a provided app
- Used core Docker commands: build, run, ps, logs, exec

## Setup

- Access to your Linux Docker host — connect in your preferred way (see Sprint 1 Module 3 if
  you need a refresher on SSH, or on setting up VS Code Remote Development)
- The [`starter/`](starter) folder from this lab, cloned or copied onto the Linux host
- GitHub Copilot Chat in IntelliJ
- The
  [`unfamiliar-multistage-dockerfile.txt`](../../demos/11-docker-fundamentals/unfamiliar-multistage-dockerfile.txt)
  from the demo

## Task sheet

### Part A — Explain before you write

1. Open `unfamiliar-multistage-dockerfile.txt` in IntelliJ.
2. Ask Copilot Chat to explain what each instruction does, and why it has two `FROM` lines.
3. Write down, in your own words, what a multi-stage build is and why it produces a smaller
   final image than building everything in one stage.

### Part B — Build the app

4. On your Linux Docker host, in `starter/`, run `mvn clean package`. Confirm a jar file appears
   under `target/`.

### Part C — Write your own Dockerfile

5. Create a file called `Dockerfile` in `starter/` (no file extension).
6. Base it on what you learned in Part A, but keep it to a **single stage**: start from
   `eclipse-temurin:21-jre-alpine`, set a working directory, copy in the jar you already built,
   and set the entrypoint to run it.
7. Build the image: `docker build -t sprint1-greeter-app .`
8. Confirm it appears in `docker images`.

### Part D — Run it and inspect it

9. Run a container from your image in detached mode, giving it a name.
10. Use `docker ps` to confirm it's running.
11. Use `docker logs` to see what the app printed.
12. Use `docker exec -it <name> sh` to get a shell inside the running container, and run `ls
    /app` to confirm the jar is there.
13. Stop and remove the container when you're done.

## Acceptance criteria

- You have a written explanation (in your own words) of containers vs VMs, and images vs
  containers.
- `docker images` shows your `sprint1-greeter-app` image.
- `docker ps` showed your container running, and `docker logs` showed the greeting message.
- You successfully opened a shell inside the running container with `docker exec`.

If you finish early, try changing the greeting in `Main.java`, rebuild the jar, rebuild the
image, and run a new container, notice the old image is now untagged (`<none>`) until you clean
it up with `docker image prune`.
