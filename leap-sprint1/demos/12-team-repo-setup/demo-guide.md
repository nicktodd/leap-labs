# Demo: Module 12 — Team Repo & Branching Strategy Setup

**Duration:** 8 minutes
**Prerequisite:** none new, this reuses everything from Modules 06-08. No new tooling.

## Part 1: Framing the task (2 min)

Narration: this module introduces no new commands. Everything you need, you already have from
Modules 06, 07, and 08: `git init`/commit basics, branching and merging, and connecting a local
repo to GitHub. What's new is doing it for real, as a team, for the project you'll build for
the rest of this programme.

## Part 2: Creating a team-owned repository (3 min)

On github.com, walk through creating a repository under the team's control (either a shared
GitHub organisation the trainer has set up, or one team member's account with the rest added as
collaborators):

```text
New repository -> name it <team-name>-sprint1-project -> do not initialise with a README
(the team will add its own, containing the branching strategy record)
```

Add every team member as a collaborator under Settings > Collaborators, exactly as practised
individually in Module 08.

## Part 3: Reaching a branching strategy decision as a team (2 min)

Narration: point back to Module 07's criteria: team size, release cadence, and how much
overhead the team can tolerate. Remind them this isn't a graded "correct answer" question, it's
a real decision they'll live with for the rest of the programme, and they can revisit it later
if it stops working for them.

## Part 4: Recording the decision (1 min)

Show a short "Branching Strategy" section being added to the repository's `README.md`, stating
the chosen strategy and the reason in two or three sentences, then committed and pushed by one
team member while the others `git pull` to confirm they received it.

## Key message

This module is where Modules 06-08 stop being lab exercises and become how your team actually
works for the next ten weeks. Getting the repo and the strategy right now, while the codebase is
still empty, is far cheaper than trying to change it later once real work is on top of it.
