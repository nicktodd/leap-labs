# Module 12 Lab — Team Repo & Branching Strategy Setup

## Objectives

By the end of this lab your team will have:

- A team-owned GitHub repository, with every team member able to push to it
- A branching strategy the whole team has agreed on
- That strategy documented in the repository's README

## Setup

- Every team member has completed Modules 06-08 individually
- Access to GitHub, and (if your trainer has set one up) the team's GitHub organisation

## Task sheet

Work through this as a team, not individually. One person can drive the keyboard, but the
decisions in Part B belong to everyone.

### Part A — Create the repository

1. As a team, agree a repository name: `<team-name>-sprint1-project`.
2. One team member creates the repository on GitHub. Leave it empty, don't let GitHub generate
   a README, `.gitignore`, or licence.
3. Add every other team member as a collaborator (or confirm everyone already has access, if
   using a shared team organisation).
4. Every team member clones the repository locally and confirms they can see it (it will be
   empty, that's expected).

### Part B — Agree a branching strategy

5. As a team, revisit the trunk-based vs Gitflow-style comparison from Module 07.
6. Discuss your specific situation: team size, how often you expect to want to merge work, and
   how much process overhead feels right for a 10-week project.
7. Agree on one strategy. It's fine to choose a lighter version of either (for example,
   trunk-based with short-lived feature branches, reviewed before merging).

### Part C — Document and push

8. One team member creates a `README.md` at the root of the repository with:
   - A one-line project name/description (a placeholder is fine, the real project starts
     properly in a later sprint)
   - A `## Branching Strategy` section stating the chosen strategy and two or three sentences
     justifying it
   - A `## Team` section listing team members
9. Commit and push the README.
10. Every other team member pulls and confirms they can see it.

## Acceptance criteria

- The repository exists on GitHub with every team member able to push to it (confirm this by
  having someone other than the README's author make a trivial commit and push it).
- `README.md` contains a `## Branching Strategy` section with a named strategy and a reason.
- Every team member's local clone is up to date with the pushed README.

Your trainer will check each team's repository against this checklist before Module 13.
