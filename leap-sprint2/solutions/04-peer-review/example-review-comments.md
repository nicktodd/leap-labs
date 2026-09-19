# Module 04 Lab — Example Review Comments (Instructor Reference)

Realistic examples of what "good" looks like, for calibrating delegates' own comments.

## Example: naming issue

> In `Main.java`, the placeholder `<team-name>` text was left in the println. Small thing, but
> worth catching, could we replace it with the actual team name before this goes further? Easy
> fix, just flagging it so it doesn't slip through.

Why this is good: specific (names the exact line/issue), low-stakes tone, suggests the fix
without being prescriptive about *how*.

## Example: security-adjacent issue

> The Dockerfile copies `target/*.jar` rather than a pinned filename. If more than one jar ever
> ends up in `target/` (say, from a shaded/fat-jar plugin later), this glob could pick up the
> wrong one silently. Worth pinning to the exact jar name now, before that becomes a real
> problem?

Why this is good: explains the *consequence*, not just "this looks risky", and frames it as a
question rather than a demand.

## Example: missing test coverage

> I don't see a test for `Greeter.greet()` in this repo. It's a small method, but it's also the
> only thing this app actually does, feels worth a single JUnit test asserting the returned
> string, so a future change to this method doesn't silently break it.

Why this is good: ties the ask back to *why* it matters for this specific codebase, not a
generic "add tests" comment.

## Examples of comments to avoid, and why

| Comment | Problem |
|---|---|
| "This is bad." | Not specific, doesn't say what's wrong or why |
| "Why would you do it this way?" | Reads as accusatory rather than curious |
| "Fix this." | No explanation of what "this" is or what "fixed" looks like |
| (No comments, just an approval) | Misses the whole point of the exercise, and of review in general |

## What to check as an instructor

- Comments name a specific file/line/behaviour, not a vague impression.
- At least one comment goes beyond syntax (naming, security, or tests, per the checklist).
- The approve/change-request decision has a stated reason, not just a click.
- Responses to received comments are non-defensive, look for language like "I chose X because
  Y" rather than "that's fine, don't worry about it."
