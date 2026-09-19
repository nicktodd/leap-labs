# Demo: Module 07 — Git Branching & Branching Strategies

**Duration:** 12 minutes
**Prerequisite:** A repo initialised with one commit (use the `starter/` project: `git init`,
`git add -A`, `git commit -m "Initial commit"`).

## Part 1: What a branch actually is (3 min)

```bash
git branch
git log --oneline --graph --all
```

Narration: a branch is just a movable label pointing at a commit. `main` is not special to Git
itself, it's just the conventional name for the default branch. `HEAD` is a pointer to whichever
branch (or commit) you currently have checked out. Draw this on the whiteboard: commits form a
line (or tree), branches are sticky notes on specific commits, and HEAD is the sticky note that
says "you are here."

```bash
git branch feature/formal-greeting
git branch
```

Narration: `git branch <name>` creates a new label pointing at the current commit. It does not
move you onto it, notice `git branch` still shows `*` next to `main`.

## Part 2: Switching and committing on a branch (3 min)

```bash
git switch feature/formal-greeting
```

Edit `src/Greeter.java`, change the greeting to `"Good day, " + name`.

```bash
git add src/Greeter.java
git commit -m "Use a more formal greeting"
git log --oneline --graph --all
```

Narration: commits made now only extend `feature/formal-greeting`. `main` still points at the
original commit. This isolation is the entire point of branching: you can experiment without
touching the code everyone else is using.

## Part 3: Merging back into main (2 min)

```bash
git switch main
git merge feature/formal-greeting
git log --oneline --graph --all
```

Narration: because no new commits were made on `main` since the branch was created, this is a
**fast-forward merge**, Git just moves the `main` label forward. No merge commit is created.

## Part 4: A merge conflict (3 min)

```bash
git switch -c feature/casual-greeting main~1
```

(Branches from the commit *before* the formal-greeting merge, so both branches touch the same
line independently.) Edit the same line in `Greeter.java` to `"Hey there, " + name`, commit it.

```bash
git switch main
git merge feature/casual-greeting
```

Show the conflict markers Git inserts (`<<<<<<<`, `=======`, `>>>>>>>`). Manually edit the file
to the agreed wording, then:

```bash
git add src/Greeter.java
git commit
git log --oneline --graph --all
```

Narration: a conflict just means Git found two changes to the same lines and can't guess which
one you want. You resolve it like any other edit, then commit. This is completely normal in
team development, not a sign something went wrong.

## Part 5: Branching strategies (1 min)

Narration: now that everyone has felt what a branch *is*, the strategy conversation makes sense
— it's really a question of "how long do branches like this live, and how often do they merge
back?" Cover trunk-based vs Gitflow-style on the slides.

## Key message

A branch is a label on a commit, not a copy of your code. Feature branches let you isolate
work; merging (and occasionally resolving a conflict) is how that work rejoins the team.
Branching *strategy* is just a team agreement about when and how that happens.
