# Module 03 Lab — Advanced Git: Pull Requests & Repo Hygiene

## Recap: where we left off in Sprint 1

- **Module 06 (Git Fundamentals)**: staging, committing, `.gitignore` basics
- **Module 07 (Git Branching Strategies)**: branching, merging, and resolving a conflict by hand
- **Module 08 (GitHub Essentials)**: connecting to a remote, `push` and `pull`, explicitly
  stopping short of Pull Requests

This lab picks up exactly where Module 08 left off.

## Objectives

By the end of this lab you will have:

- Completed a full PR workflow end-to-end: branch, commit, push, PR, review, merge
- Written an effective PR title and description
- Understood what branch protection rules do and why they matter
- Applied a commit message convention
- Deliberately induced and resolved a merge conflict through a PR, in pairs

## Setup

- The [`starter/`](starter) folder from this lab (a self-contained copy of the Sprint 1
  project skeleton, so this works even if your real team repo is mid-flight)
- A GitHub repository for this exercise (a personal practice repo, or one your trainer
  provisions per pair)
- Git 2.49, and a partner

## Task sheet

### Part A — Solo: branch, commit, push, open a PR

1. Copy `starter/` into a new repository and push it to GitHub with an initial commit on
   `main`.
2. Create a branch and make a small, clear change to `Main.java`.
3. Commit using a **Conventional Commit** message: `<type>: <description>`, where `type` is one
   of `feat`, `fix`, `chore`, `docs`, or `refactor`.
4. Push the branch and open a Pull Request. Write a title that mirrors your commit message, and
   a description covering what changed, why, and how to verify it.

### Part B — With your partner: review and merge

5. Add your partner as a reviewer on your PR (and review theirs, if they've opened one too).
6. Leave at least one comment on your partner's PR, then approve it (or request changes, if you
   spot something worth fixing, full review etiquette is covered properly in Module 04).
7. Merge the approved PR.

### Part C — Branch protection

8. If you have admin rights on the repository, configure branch protection on `main`: require
   a PR before merging, require at least one approval. If you don't have admin rights, discuss
   with your partner what you *would* configure and why.

### Part D — In pairs: induce and resolve a merge conflict via a PR

9. Both partners branch from the same commit on `main`.
10. Each of you changes the **same line** in `Main.java` to something different, commits, pushes,
    and opens a PR.
11. Merge the first PR. It should merge cleanly.
12. Try to merge the second PR. GitHub should report a conflict.
13. Resolve it: pull `main` into your branch locally, fix the conflict in the file, remove the
    conflict markers, commit, and push. Confirm the PR now shows as mergeable, then merge it.

## Acceptance criteria

- A merged PR exists with a Conventional Commit-style title and a description covering what,
  why, and how to verify.
- At least one review comment exists on a PR from this exercise.
- You can explain what branch protection rule you'd apply to `main` and why.
- The second PR's conflict was resolved and merged, and you can explain, in your own words, why
  it conflicted when the first one didn't.

If you finish early, look at your merged PR's commit history on GitHub, can you tell, just from
reading it, what happened and why, without asking your partner?
