# Module 11 Lab — Walkthrough (Instructor Reference)

## The five vulnerabilities

| # | File | OWASP 2025 Category | Risk |
|---|---|---|---|
| 1 | `AccountController.java` | A01: Broken Access Control | Any user can view any account by changing the URL (IDOR) |
| 2 | `UserRegistrationService.java` | A04: Cryptographic Failures | Passwords hashed with unsalted MD5 |
| 3 | `TransactionSearchDao.java` | A05: Injection | SQL built via string concatenation |
| 4 | `LoginController.java` (login method) | A07: Authentication Failures | No rate limiting or lockout on failed logins |
| 5 | `LoginController.java` (exception handler) | A09: Security Logging & Alerting Failures | Failed logins silently discarded, nothing logged |

See the fixed versions of each file in this folder.

## Common imperfect Copilot suggestions to watch for

These are realistic, plausible-sounding suggestions that don't fully solve the problem, worth
specifically checking delegates caught and corrected:

- **For #2 (password hashing)**: Copilot commonly suggests **SHA-256** as "more secure than
  MD5." This is true in a narrow sense (SHA-256 is a stronger general-purpose hash) but
  **wrong** as a fix, SHA-256 is still fast and unsalted by default, the same fundamental
  weakness. The correct fix is a purpose-built password hash (bcrypt/scrypt/Argon2).
- **For #3 (SQL injection)**: Copilot sometimes suggests **escaping single quotes** in the
  input rather than switching to a parameterised query. Escaping is fragile (there is often
  another edge case), a `PreparedStatement` with bind parameters removes the entire class of
  problem rather than patching one instance of it.
- **For #4/#5 (auth failures/logging)**: Copilot may suggest logging without addressing rate
  limiting, or vice versa, since the two vulnerabilities live in the same file but are
  conceptually distinct (A07 vs A09). Both need addressing; accepting a fix for one shouldn't
  be mistaken for having fixed the other.

## What to check as an instructor

- All five vulnerabilities were identified, with the category and risk written down, **before**
  fixes were applied (Part A of the task sheet), not identified retroactively after copying a
  fix.
- The fix for #2 is a proper password-hashing algorithm, not SHA-256 or another general-purpose
  hash.
- The fix for #3 uses `PreparedStatement`/bind parameters, not string escaping.
- The fix for #4 and #5 are both present and distinct: a lockout/rate-limit mechanism, and
  actual logging of failed attempts.
- Delegates can point to at least one place they corrected or rejected a Copilot suggestion,
  and explain why in their own words, this is the module's real objective, not just having five
  green checkmarks.
