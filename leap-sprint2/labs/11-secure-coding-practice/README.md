# Module 11 Lab — Find and Fix Five Vulnerabilities

## Objectives

By the end of this lab you will have:

- Identified and remediated five deliberate vulnerabilities in an existing codebase
- Used GitHub Copilot to suggest fixes, and critically reviewed each suggestion before accepting it
- Applied input validation, output encoding, and parameterised queries as core defences

## Setup

- The [`starter/`](starter) folder from this lab, a small fictional PaySprint Mobile backend
- GitHub Copilot Chat
- Your notes from Module 09 (OWASP categories) and Module 10 (which categories you found hardest)

## Task sheet

### Part A — Find all five, before fixing any

1. Read through every file in `starter/src/main/java/com/neueda/leap/paysprint/`.
2. For each of the five vulnerabilities you find, write down: the file, the OWASP Top 10 (2025)
   category, and the specific risk in plain English. Do this **before** asking Copilot for
   fixes, the identification is the skill being practised first.

### Part B — Fix each one, using Copilot critically

3. For each vulnerability, ask Copilot Chat to suggest a fix.
4. Before accepting any suggestion, check it against what you know:
   - Does it actually solve the underlying problem, or a symptom of it?
   - For anything involving hashing: is the suggested algorithm actually appropriate for the
     purpose (a password hash needs to be slow and salted, not just "secure-sounding")?
   - For anything involving a query: does it use proper parameter binding, not just escaping or
     string manipulation?
5. Apply the fix once you're confident it's correct, adjusting it yourself if Copilot's first
   suggestion wasn't quite right.

### Part C — Reflect

6. For each of the five fixes, write one sentence: did Copilot's first suggestion need
   correcting, and if so, what was wrong with it?

## Acceptance criteria

- All five vulnerabilities are identified, each with a named OWASP category and risk
  explanation, written down before any fix was applied.
- All five are fixed, with the fix actually addressing the root cause (not a partial or
  cosmetic change).
- You have a written note on at least one case where you corrected or rejected part of
  Copilot's suggestion, and why.

If you finish early, write a short JUnit test that would have caught one of the five
vulnerabilities before it ever reached production, what would that test need to assert?
