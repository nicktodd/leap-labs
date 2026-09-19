# Module 14 Lab — Sprint 1 Wrap-up & Assessment Prep

## Objectives

By the end of this lab you will have:

- Reviewed what Friday's environment-setup assessment will check
- Identified and closed any personal environment or skills gaps
- Peer-checked a partner's environment and repo setup against the checklist below

## Setup

- Everything from Modules 03-13, nothing new
- A partner (ideally not someone from your own team, so you're checking against the checklist
  fresh rather than confirming what you already agreed together)

## The assessment checklist

Work through this checklist with your partner. For each item, your partner should *show* you
the thing, not just tell you it works. Tick it off only once you've seen it yourself.

### Environment

- [ ] IntelliJ IDEA 2025.1 opens and can open a project
- [ ] Can connect to the Linux Docker host and confirm the daemon is reachable (e.g. `docker
      ps`)
- [ ] GitHub account is signed in and has access to the LEAP organisation
- [ ] GitHub Copilot Chat is available in IntelliJ

### Linux & PowerShell (Modules 03-04)

- [ ] Can SSH into the shared Linux host and navigate to a specific folder
- [ ] Can read the last N lines of a log file and find a specific error in it, in both bash and
      PowerShell
- [ ] Can explain the difference between a bash pipe and a PowerShell pipe, in one sentence

### GenAI (Module 05)

- [ ] Can explain, in their own words, this week's boundary: GenAI as a learning aid, not for
      code generation
- [ ] Can describe one time this week they used GenAI to explain something, and how they
      verified the explanation

### Git & GitHub (Modules 06-08)

- [ ] `git log --oneline` on a personal practice repo shows a real commit history
- [ ] Can explain what a merge conflict is and how they resolved one this week
- [ ] Can show a repository connected to a GitHub remote, and demonstrate `push` and `pull`

### CI/CD & Jenkins (Modules 09-10)

- [ ] Can explain, in one sentence each, the difference between Continuous Integration,
      Continuous Delivery, and Continuous Deployment
- [ ] Can navigate to a Jenkins job, open Console Output, and point at where a stage failed

### Docker (Module 11)

- [ ] Can explain the difference between an image and a container
- [ ] Has a working Dockerfile they wrote themselves, and can `docker build` and `docker run`
      it live

### Team Repo (Modules 12-13)

- [ ] Team repository exists, and this person has push access to it
- [ ] Can read out the Branching Strategy section of the team README and explain the reasoning
- [ ] Team's containerised skeleton builds and runs from a clean `git pull`
- [ ] Team's Jenkins job runs the `Jenkinsfile` from `main` and goes green

## Task sheet

1. Pair up with your partner.
2. Go through the checklist above together, partner by partner (so everyone gets checked).
3. For every unticked item, note it down specifically, not "Docker stuff", but "couldn't show a
   Dockerfile they wrote themselves."
4. Use any remaining lab time to close your own gaps: revisit the relevant module's lab README,
   ask your trainer, or ask a teammate who has it working.

## Acceptance criteria

- Every item on the checklist has been shown, not just claimed, to a partner.
- You have a specific, written list of any gaps you personally still have.
- For each gap, you've either closed it or know exactly what you'll do before Friday.

Friday: guest speaker, Weekly Knowledge Check (MCQ), Sprint 1 Assessment, and Group Retro.
