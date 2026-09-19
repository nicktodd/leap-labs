# Module 09 Lab — Find the OWASP Top 10, in the Wild

> Uses the **OWASP Top 10:2025** edition (finalized January 2026). If you've seen the 2021
> edition before: Security Misconfiguration jumped from #5 to #2, "Vulnerable and Outdated
> Components" was broadened into "Software Supply Chain Failures," SSRF was folded into
> Broken Access Control, and "Mishandling of Exceptional Conditions" is a brand new category.

## Objectives

By the end of this lab you will have:

- Reviewed eleven short code/config/design examples, covering all ten OWASP Top 10 (2025)
  categories
- Identified the category, explained the real-world risk, and proposed a fix for each
- Discussed your reasoning with a partner before checking the model answers
- Understood which categories (A01, A05, A07) get a full deep-dive in Sprint 8

## Setup

- The [`vulnerable-examples/`](vulnerable-examples) folder in this lab, eleven files, each a
  short excerpt from the fictional PaySprint Mobile codebase
- GitHub Copilot Chat
- A partner

## Task sheet

Work through all eleven files. Four of them (`05`, `02`, `03`, `11`) were demoed live, the
remaining seven are new. For **every** file, write down:

1. **Which OWASP Top 10 (2025) category** it belongs to (A01-A10)
2. **What the real-world risk is**, in plain English, as if explaining to a non-technical
   stakeholder
3. **A proposed fix**, specific enough that a developer could act on it

Discuss each one with your partner before you both look at the model answers, comparing notes
is more valuable than reaching the same conclusion silently.

**The eleven files:**

- `01-account-lookup.java` — A01: Broken Access Control
- `02-Dockerfile` — A02: Security Misconfiguration
- `03-pom-dependencies.xml` — A03: Software Supply Chain Failures
- `04-password-storage.java` — A04: Cryptographic Failures
- `05-transaction-search.java` — A05: Injection
- `06-password-reset-flow.md` — A06: Insecure Design
- `07-login-endpoint.java` — A07: Authentication Failures
- `08-update-checker.java` — A08: Software or Data Integrity Failures
- `09-login-error-handling.java` — A09: Security Logging & Alerting Failures
- `10-payment-transfer.java` — A10: Mishandling of Exceptional Conditions
- `11-avatar-fetch-ssrf.java` — bonus: an SSRF example, which the 2021 edition ranked as its
  own category (A10:2021) but the 2025 edition folds into A01: Broken Access Control

## A note on using GenAI here

Feel free to ask Copilot Chat to help explain any file you're stuck on, this is still a
learning-aid use case. But identify the category and articulate the risk in your own words
before checking the model answer, the exercise is in the recognition, not in collecting an AI's
output.

## Acceptance criteria

- All eleven files have a named OWASP category, a plain-English risk explanation, and a
  proposed fix, written down (not just discussed verbally).
- You can explain, for at least three of the eleven, *why* it's that specific category and not
  a neighbouring one (for example, why `07-login-endpoint.java` is an authentication failure
  and not broken access control, or why `11-avatar-fetch-ssrf.java` now falls under A01 rather
  than being its own category).
- You've compared your answers against the model answers and noted anywhere you disagreed or
  were unsure.

If you finish early, pick one file and sketch the actual code fix, not just a description of
what should change.
