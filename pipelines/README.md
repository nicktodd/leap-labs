# LEAP Program - This Week's Lab Exercises

This repository contains the hands-on lab exercises accompanying **This Week: Pipelines -
CI/CD, Containers, Infrastructure & Security**, taught as part of week 2 of the LEAP graduate
programme (alongside `data/`, which covers this same week's data systems content).

## Prerequisites

- Everything from the Foundations week: Git 2.49, Docker Desktop 27.x, Jenkins access,
  IntelliJ IDEA 2025.1, GitHub account with LEAP organisation access, GitHub Copilot
- Access to the Secure Code Warrior platform (Modules 10-11)
- A working team repository from the Foundations week (referenced conceptually in a few
  modules; this repo also includes a self-contained copy of that skeleton so the labs work
  standalone even if a team's real repo is in an inconsistent state)

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`:

- `demos/<module>/` - instructor-led demo assets and guides
- `labs/<module>/` - your starter files and the task README for that module
- `solutions/<module>/` - reference solutions (try the lab first!)

For conceptual/walkthrough modules, `labs/<module>/README.md` contains the full step-by-step
guide along with any sample configs or commands, and there may be no `solutions/` content.

## CI tooling

This week uses **Jenkins** for hands-on pipeline work, consistent with the Foundations week.
Module 8 also builds a CI pipeline lab; GitHub Actions is discussed conceptually as a point of
comparison where relevant, but the hands-on pipeline work is built in Jenkins.

## Modules

| # | Module | Lab |
|---|---|---|
| 1 | CI/CD Fundamentals | [labs/01-cicd-fundamentals/README.md](labs/01-cicd-fundamentals/README.md) |
| 2 | Introduction to Jenkins | [labs/02-jenkins-intro/README.md](labs/02-jenkins-intro/README.md) |
| 3 | Docker Fundamentals | [labs/03-docker-fundamentals/README.md](labs/03-docker-fundamentals/README.md) |
| 4 | Containerising the Project Skeleton | [labs/04-containerising-skeleton/README.md](labs/04-containerising-skeleton/README.md) |
| 5 | DevOps Fundamentals & CI/CD Deeper Dive | [labs/05-devops-cicd-deeper-dive/README.md](labs/05-devops-cicd-deeper-dive/README.md) |
| 6 | Containerisation Deeper Dive | [labs/06-docker-multistage/README.md](labs/06-docker-multistage/README.md) |
| 7 | Infrastructure as Code Concepts | [labs/07-iac-concepts/README.md](labs/07-iac-concepts/README.md) |
| 8 | CI Pipeline Build Lab | [labs/08-ci-pipeline-build/README.md](labs/08-ci-pipeline-build/README.md) |
| 9 | OWASP Top 10 | [labs/09-owasp-top-10/README.md](labs/09-owasp-top-10/README.md) |
| 10 | Secure Code Warrior Introduction | [labs/10-secure-code-warrior-intro/README.md](labs/10-secure-code-warrior-intro/README.md) |
| 11 | Secure Coding in Practice | [labs/11-secure-coding-practice/README.md](labs/11-secure-coding-practice/README.md) |
| 12 | Cyber Challenge - Mission Day | [labs/12-cyber-challenge-mission-day/README.md](labs/12-cyber-challenge-mission-day/README.md) |
| 13 | Week 2 Wrap-up & Assessment Prep (Pipelines) | [labs/13-wrapup/README.md](labs/13-wrapup/README.md) |

## Getting started

1. Clone this repository.
2. Confirm your Foundations-week tooling (Git, Docker, Jenkins, IntelliJ, Copilot) still works.
3. Work through the modules in order, starting with `labs/01-cicd-fundamentals/README.md`.

## Support

Ask your trainer or Scrum team lead during class, or raise a question in the cohort's usual
support channel.
