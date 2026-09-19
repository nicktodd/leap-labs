# Demo: Module 06 — Git Fundamentals

**Duration:** 10 minutes
**Prerequisite:** Git 2.49 installed and configured (`git config --global user.name`/`user.email`
set from Module 02). A scratch folder to demo in.

## Part 1: Repositories and status (3 min)

```bash
mkdir demo-repo && cd demo-repo
git init
git status
echo "Hello sprint 1" > notes.txt
git status
```

Narration: `git init` creates a hidden `.git` folder, that's the entire repository. `git status`
is the single most useful Git command: run it constantly to see what's changed, staged, or
untracked.

## Part 2: Staging and committing (3 min)

```bash
git add notes.txt
git status
git commit -m "Add sprint 1 notes"
git log
```

Narration: staging (`git add`) is a deliberate middle step, it lets you build a commit from
exactly the changes you want, not just "everything that's different right now." Commit messages
should explain *why*, not just *what*.

## Part 3: Diff and a second commit (2 min)

```bash
echo "Day 2: version control" >> notes.txt
git diff
git add notes.txt
git commit -m "Add day 2 topic to notes"
git log --oneline
```

Narration: `git diff` shows exactly what changed, line by line, before you stage it. Get in the
habit of reading the diff before every commit.

## Part 4: .gitignore (2 min)

```bash
mkdir target && echo "compiled output" > target/app.class
git status
```

Show that `target/` now appears as untracked.

```bash
echo "target/" > .gitignore
echo ".idea/" >> .gitignore
git status
git add .gitignore
git commit -m "Add .gitignore for build output and IDE files"
```

Narration: `.gitignore` tells Git which files it should never track, typically build output,
IDE metadata, and secrets. Adding it early avoids ever accidentally committing junk.

## Key message

Git's core loop is: change something, check `git status`/`git diff`, stage what belongs
together, commit with a clear message. Everything else in Git builds on this loop.
