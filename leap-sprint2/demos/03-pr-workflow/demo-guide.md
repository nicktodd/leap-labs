# Demo: Module 03 — Advanced Git: Pull Requests & Repo Hygiene

**Duration:** 12 minutes
**Prerequisite:** A GitHub repository (the demo can reuse the `starter/` skeleton from this
lab), Git 2.49, GitHub Copilot Chat available.

## Part 1: Recap, quickly (2 min)

Narration: Sprint 1 got you comfortable with the mechanics: Module 06 was commits and staging,
Module 07 was branching and merging (including resolving a conflict by hand), Module 08 was
connecting to a remote and using push and pull, deliberately stopping short of Pull Requests.
Today picks up exactly where Module 08 left off.

## Part 2: Branch, commit, and push (2 min)

```bash
git switch -c feature/add-farewell-message
```

Edit `Main.java` to print a second line, then:

```bash
git add src/main/java/com/neueda/leap/Main.java
git commit -m "feat: add farewell message to startup output"
git push -u origin feature/add-farewell-message
```

Narration: point out the commit message format, `feat:` followed by a concise, present-tense
description. This is a **Conventional Commit**, more on the convention shortly.

## Part 3: Opening a PR (3 min)

On github.com, open a Pull Request from `feature/add-farewell-message` into `main`. Fill in:

- **Title**: mirrors the commit message, `feat: add farewell message to startup output`
- **Description**: what changed, why, and how to verify it (e.g. "run `mvn package && java -jar
  target/team-skeleton-0.1.0.jar` and confirm both lines print")

Narration: a PR title and description are for the *reviewer*, not the author. If a reviewer has
to guess what changed or why, the description has failed its job.

## Part 4: Branch protection (2 min)

Show (or describe, if the trainer's org settings aren't editable live) **Settings > Branches >
Branch protection rules** for `main`:

- Require a pull request before merging
- Require at least one approving review
- Require status checks (the Jenkins build) to pass before merging

Narration: branch protection is what turns "we agreed to use PRs" into something Git actually
enforces. Without it, anyone can still push straight to `main` by habit or under pressure.

## Part 5: Review and merge (2 min)

Have a partner review the PR: at least one comment, then an approval. Merge it.

## Part 6: .gitignore, revisited (1 min)

Narration: Sprint 1 Module 06 covered the basics (`target/`, `.idea/`). Today's addition:
`.gitignore` is also a security boundary, secrets, credentials, and `.env` files belong there
too, never in a commit. Module 09 (OWASP) and Module 11 (Secure Coding) come back to exactly
why that matters.

## Key message

A PR isn't extra process for its own sake, it's the moment a change gets a second pair of eyes
and an automated safety net (Jenkins) *before* it reaches `main`, not after.
