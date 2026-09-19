# Module 13 Lab — Containerising the Project Skeleton

## Objectives

By the end of this lab your team will have:

- A minimal Dockerfile for a "hello world" project skeleton
- That skeleton committed to your team repository using the branching strategy you agreed in
  Module 12
- A container every team member can independently build and run from a clean checkout
- A simple Jenkinsfile that builds and smoke-tests that container through your team's Jenkins job

## Setup

- Your team repository from Module 12, with its branching strategy documented
- Access to your Linux Docker host — connect in your preferred way (see Sprint 1 Module 3), and
  clone your team repository there before starting Part B
- The [`starter/`](starter) folder from this lab (a minimal "hello world" Java app)

## Task sheet

### Part A — Branch

1. As a team, create a branch for this work, following whatever branch naming your Module 12
   strategy calls for (or `feature/docker-skeleton` if it doesn't specify one).

### Part B — Add the skeleton and containerise it

2. Copy the [`starter/`](starter) files into your team repository, on that branch.
3. Edit `Main.java` to replace `<team-name>` with your actual team name.
4. Build it locally with Maven and confirm it runs and prints your message.
5. Write a minimal, single-stage Dockerfile for it, based on what you practised in Module 11.
6. Build the image and run a container from it with `docker run --rm <image-name>` — confirm
   your message is printed, then the container exits (there's no need for `-d` here, this isn't
   a long-running app).

### Part C — Commit and merge, using your team's strategy

7. Commit the skeleton app and the Dockerfile, and push the branch.
8. Merge it into `main` following whatever process your team agreed in Module 12 (a quick
   review first, or a direct merge, depending on your strategy).
9. Push the merged `main`.

### Part D — Confirm it's reproducible

10. Have a **different** team member than whoever did steps 2-9 pull the latest `main`, build
    the image themselves, and run it.
11. Confirm they see the same output, from a completely clean checkout.

### Part E — Add a simple Jenkinsfile

12. As a team, create a `Jenkinsfile` at the root of the repository with three stages:
    `Checkout`, `Build Image` (runs `docker build`), and `Smoke Test` (runs `docker run --rm`
    against the image you just built). Base this on the Jenkinsfile syntax from Modules 05, 09,
    and 10, you don't need anything more complex than that for a skeleton.
13. Create a Jenkins Pipeline job pointing at your team repository and this `Jenkinsfile`.
14. Following your team's branching strategy, commit and merge the `Jenkinsfile` into `main`
    exactly as you did with the skeleton itself in Part C.
15. Run the job and confirm it goes green: Checkout, Build Image, and Smoke Test should all
    succeed.

## Acceptance criteria

- `main` in your team repository contains the skeleton app and a working Dockerfile.
- `docker build` and `docker run --rm` succeed for at least two different team members, each
  starting from a fresh `git pull` of `main`.
- Your team can point to the exact commit (or merge) where the skeleton was integrated, and
  explain which branching strategy step they followed to get it there.
- Your team's Jenkins job runs the `Jenkinsfile` from `main` and completes with all three
  stages green.

This is the last hands-on lab of Sprint 1. Module 14 wraps up and prepares you for Friday's
assessment.
