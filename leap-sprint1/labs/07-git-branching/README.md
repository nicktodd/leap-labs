# Module 07 Lab — Git Branching Strategies

## Objectives

By the end of this lab you will have:

- Created feature branches and switched between them
- Merged a branch back into `main`, including a fast-forward merge
- Deliberately caused and resolved a merge conflict
- Compared branching strategies and reasoned about which suits a small team

## Setup

- Git 2.49
- The [`starter/`](starter) folder from this lab, copied to a working location of your choice

## Task sheet

### Part A — Branch, edit, merge

1. Copy `starter/` to a working location, rename it `sprint1-branching-lab`, and initialise it
   as a Git repository with one commit containing all the starter files.
2. Create a branch called `feature/formal-greeting` and switch to it.
3. On that branch, change `Greeter.java`'s greeting to something more formal (e.g.
   `"Good day, " + name`). Commit the change.
4. Switch back to `main` and merge `feature/formal-greeting` in. Check `git log --oneline
   --graph --all` — was this a fast-forward merge? How can you tell?

### Part B — Cause and resolve a conflict

5. Create a second branch called `feature/casual-greeting`, but branch it from the commit
   *before* the formal-greeting merge (`main~1` at the point you do this — ask your trainer if
   you're not sure how to check).
6. On `feature/casual-greeting`, change the same line to something casual (e.g. `"Hey there, "
   + name`). Commit the change.
7. Switch to `main` and merge `feature/casual-greeting`. You should get a conflict.
8. Open the conflicted file, look at the `<<<<<<<`, `=======`, `>>>>>>>` markers, and edit the
   file to the wording your pair agrees on. Remove the conflict markers.
9. Stage the resolved file and complete the merge commit.

### Part C — Branching strategies

10. With a partner, discuss the difference between **trunk-based development** (short-lived
    branches, frequent merges to `main`) and a **Gitflow-style** workflow (long-lived `main`,
    `develop`, feature, release, and hotfix branches).
11. For your Scrum team (roughly 6-8 people, one repo, releasing frequently), decide which
    approach you'd recommend and write two or three sentences justifying it. You'll use this
    reasoning again in Module 12 when your team sets up its real repository.

## Acceptance criteria

- `git log --oneline --graph --all` shows both feature branches merged into `main`, with a
  visible merge commit for the conflict resolution.
- The conflicted file contains no leftover `<<<<<<<`/`=======`/`>>>>>>>` markers.
- You can explain, in your own words, what a fast-forward merge is and why the second merge
  wasn't one.
- You have a short written recommendation (trunk-based vs Gitflow-style) with a reason.

If you finish early, try `git log --graph --oneline --all --decorate` for a fuller view of the
branch history, and identify exactly which commit is the common ancestor of both feature
branches.
