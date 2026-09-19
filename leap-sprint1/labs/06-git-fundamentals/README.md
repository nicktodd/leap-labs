# Module 06 Lab — Git Fundamentals

## Objectives

By the end of this lab you will have:

- Initialised a Git repository and made a first series of commits
- Used staging, `git status`, and `git diff` as part of your normal workflow
- Written a `.gitignore` that excludes build output and IDE files

## Setup

- Git 2.49 installed, with `user.name` and `user.email` configured
- The [`starter/`](starter) folder from this lab, copied to a working location of your choice

## Task sheet

`starter/` contains a tiny placeholder Java project: a `README.md`, a `src/Greeter.java` file,
and two folders that stand in for files you should **never** commit — `target/` (a compiled
build artifact) and `.idea/` (IntelliJ's per-user workspace state).

1. **Initialise the repository**
   - Copy `starter/` to your working location and rename it `sprint1-git-lab`.
   - Initialise it as a Git repository.
   - Run `git status` and note what it reports before anything is staged.

2. **First commit**
   - Stage and commit just `README.md` and `src/Greeter.java`, with a clear commit message.
   - Confirm with `git log` that the commit exists.

3. **Add a .gitignore**
   - Run `git status` again — notice `target/` and `.idea/` show up as untracked.
   - Create a `.gitignore` file that excludes `target/` and `.idea/`.
   - Run `git status` once more to confirm they no longer appear.
   - Commit the `.gitignore` file on its own, with a message explaining what it's for.

4. **Second content commit, and diff**
   - Edit `src/Greeter.java` to add a second method of your choice (for example, a farewell
     message).
   - Run `git diff` before staging, and read what it shows you.
   - Stage and commit the change with a message describing what you added.

5. **Review your history**
   - Run `git log` and `git log --oneline`.
   - Compare the two outputs: what extra information does the full `git log` give you that
     `--oneline` doesn't?

## Acceptance criteria

- `git log --oneline` shows at least three commits: the initial README/Greeter commit, the
  `.gitignore` commit, and the second Greeter change.
- `git status` reports a clean working tree with `target/` and `.idea/` never tracked.
- You can explain, in one sentence each, the difference between "untracked", "staged", and
  "committed."

If you finish early, try `git log -p` to see the full diff for every commit in your history at
once.
