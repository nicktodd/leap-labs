# Module 03 Lab — Walkthrough (Instructor Reference)

## Part A-B: standard PR flow

```bash
git switch -c feature/add-farewell-message
# edit Main.java to add a second System.out.println line
git add src/main/java/com/neueda/leap/Main.java
git commit -m "feat: add farewell message to startup output"
git push -u origin feature/add-farewell-message
```

Open a PR on GitHub:
- **Title**: `feat: add farewell message to startup output`
- **Description example**:
  > Adds a second line to the skeleton's startup output as a small practice change for the PR
  > workflow lab. Verify by running `mvn package && java -jar target/team-skeleton-0.1.0.jar`
  > and confirming two lines print.

Partner reviews, leaves a comment, approves, PR is merged (ideally via "Squash and merge" or
"Merge commit", either is fine for this exercise, consistency matters more than the specific
choice).

## Part D: the induced conflict

Both partners branch from the same `main` commit:

```bash
# Partner A
git switch -c feature/greeting-a
# change the println text to "Hello from Partner A's change"
git add . && git commit -m "feat: update startup message (A)"
git push -u origin feature/greeting-a

# Partner B, from the same starting commit
git switch -c feature/greeting-b
# change the SAME line to "Hello from Partner B's change"
git add . && git commit -m "feat: update startup message (B)"
git push -u origin feature/greeting-b
```

Partner A's PR merges cleanly (`main` hadn't moved). Partner B's PR now shows "This branch has
conflicts that must be resolved" in the GitHub UI.

**Resolving it:**

```bash
git switch feature/greeting-b
git pull origin main
# conflict markers appear in Main.java, exactly like Module 07
# edit to the agreed final wording, remove <<<<<<<, =======, >>>>>>>
git add src/main/java/com/neueda/leap/Main.java
git commit
git push
```

The PR updates automatically and shows as mergeable once pushed.

## What to check as an instructor

- The commit message actually follows `type: description` format, not just a vague sentence.
- The PR description answers what/why/how-to-verify, not just repeating the title.
- Partners can articulate *why* the second PR conflicted and the first didn't (same underlying
  mechanic as Module 07: two branches diverged from the same commit and touched the same line).
- If a pair skips resolving the conflict locally and instead tries to resolve it entirely in
  GitHub's web editor, that's fine mechanically but worth pointing out it doesn't scale to real
  conflicts across multiple files.
