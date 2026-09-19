# Code Review Checklist

Use this checklist when reviewing a partner's repository. Not every item applies to every
change, use judgement, but check all of them before deciding approve vs change request.

## Correctness and logic

- [ ] Does the code actually do what its name/description claims?
- [ ] Are edge cases handled (empty input, null, zero, very large values)?
- [ ] Is there any logic that looks copy-pasted with only a small, easy-to-miss difference?

## Naming and readability

- [ ] Do variable, method, and class names describe what they hold or do?
- [ ] Would someone unfamiliar with this code understand it without asking the author?
- [ ] Is there dead code, commented-out blocks, or leftover debug output?

## Security (preview of Module 09)

- [ ] Is any user input used without validation?
- [ ] Are there any hardcoded secrets, credentials, or API keys?
- [ ] If there's a database query, is it parameterised rather than string-concatenated?

## Tests

- [ ] Is there at least one test covering the main behaviour?
- [ ] Do the tests actually assert something meaningful, not just "it didn't throw"?

## Git hygiene (recap of Modules 06-08 and Module 03)

- [ ] Are commit messages clear and, ideally, follow a convention?
- [ ] Does `.gitignore` exclude build output and IDE files, with nothing that shouldn't be
      tracked actually committed?

## Leaving your review

- Leave at least **two written comments**, each specific enough that the author knows exactly
  what to change and why
- Finish with either an **Approve** or a **Request Changes**, not silence
