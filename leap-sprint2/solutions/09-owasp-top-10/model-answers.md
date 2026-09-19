# Module 09 Lab — Model Answers (Instructor Reference)

Uses the **OWASP Top 10:2025** edition. Where relevant, the 2021-edition category name/number is
noted too, since a lot of existing material and delegates' prior exposure will still reference
the older edition.

## 01-account-lookup.java — A01:2025 Broken Access Control

**Risk:** Any authenticated customer can view *any other customer's* account and statement
simply by changing the `accountId` in the URL, there's no check that the requesting user owns
that account. This is a classic Insecure Direct Object Reference (IDOR).

**Fix:** Look up the authenticated user's own account IDs and verify `accountId` belongs to
them before returning data, e.g. `accountRepository.findByIdAndOwner(accountId,
currentUser())`, returning 403/404 if it doesn't match.

## 02-Dockerfile — A02:2025 Security Misconfiguration

**Risk:** Three separate misconfigurations in one file: a remote JDWP debug port left open in
production (lets anyone who can reach it attach a debugger and execute arbitrary code), a full
JDK image in production increasing attack surface unnecessarily, and a database password
stored in plain text as an environment variable, visible via `docker inspect`.

**Fix:** Remove the debug agent and port entirely from the production image, use a JRE-only
multi-stage build (Module 06), and inject secrets via a secrets manager or mounted secret, never
a plain `ENV` line.

*(This category jumped from #5 to #2 between the 2021 and 2025 editions.)*

## 03-pom-dependencies.xml — A03:2025 Software Supply Chain Failures

**Risk:** `jackson-databind:2.9.8` carries a known critical RCE vulnerability
(`CVE-2019-12384`), the same one from Module 05's pipeline log. `log4j:1.2.17` and
`spring-web:5.2.0` are also long past end-of-life with known CVEs. No dependency review in
three years, and no version-pinning or build-provenance strategy, compounds the risk.

**Fix:** Upgrade all three to current supported versions, and add a Security Scan pipeline
stage (Module 05) so this is caught automatically on every build. At the supply-chain level,
also consider dependency provenance/signing verification, not just version currency.

*(This was "A06:2021 Vulnerable and Outdated Components" in the older edition; the 2025 edition
broadens the category to the whole supply chain: dependencies, build systems, and distribution
infrastructure, not just outdated version numbers.)*

## 04-password-storage.java — A04:2025 Cryptographic Failures

**Risk:** MD5 is a fast, unsalted general-purpose hash, not a password hash. It's trivially
brute-forced with modern hardware and rainbow tables, meaning a database leak exposes most
users' real passwords quickly.

**Fix:** Use a purpose-built, slow, salted password hashing algorithm (bcrypt, scrypt, or
Argon2), never a general-purpose hash like MD5 or SHA-256 alone.

## 05-transaction-search.java — A05:2025 Injection

**Risk:** `merchantName` is concatenated directly into SQL. An attacker-supplied value like
`' OR '1'='1` changes the query's meaning entirely, potentially returning every transaction for
every customer.

**Fix:** Use a parameterised query / `PreparedStatement` with a bind parameter, never build SQL
via string concatenation with any user-supplied value.

*(This was #3 in the 2021 edition; still serious, but dropped two spots in the 2025 ranking.)*

## 06-password-reset-flow.md — A06:2025 Insecure Design

**Risk:** This is a design flaw, not an implementation bug, no amount of careful coding fixes
it. Emailing the actual current password (rather than a one-time reset link/token) means the
password now also lives in email, a less secure channel. A single, unchangeable security
question with no attempt limit is trivially guessable or brute-forceable.

**Fix:** Redesign the flow: a time-limited, single-use reset token sent by email, no plaintext
password ever transmitted, no reliance on a static security question, and rate-limiting on
attempts.

## 07-login-endpoint.java — A07:2025 Authentication Failures

**Risk:** No account lockout, rate limiting, or delay after failed attempts means an attacker
can brute-force passwords by trying large numbers of guesses in quick succession. Combined with
weak (MD5-based) password storage from example 04, this compounds badly.

**Fix:** Add rate limiting and account lockout (or exponential backoff) after repeated failed
attempts, and consider multi-factor authentication for a financial application.

*(Renamed from "A07:2021 Identification and Authentication Failures" to just "Authentication
Failures" for clarity; same position, #7, in both editions.)*

## 08-update-checker.java — A08:2025 Software or Data Integrity Failures

**Risk:** The app fetches a remote configuration bundle over plain HTTP and applies it directly,
with no signature or checksum verification. An attacker in a position to intercept or spoof
that traffic (or compromise the update server) could push malicious configuration straight into
the app.

**Fix:** Serve the update over HTTPS, and verify a cryptographic signature (or at minimum a
checksum from a trusted, separately-secured source) before applying any downloaded
configuration.

## 09-login-error-handling.java — A09:2025 Security Logging & Alerting Failures

**Risk:** Failed authentication attempts and access-denied events are silently swallowed, with
nothing written to any log, metric, or alert. A real attack (brute force, or someone probing for
IDOR access like example 01) would be invisible to the team until real damage was already done.

**Fix:** Log security-relevant events (failed logins, access-denied responses) with enough
context to investigate later (timestamp, account, source), and wire up **alerting** on unusual
patterns, e.g. many failed logins for one account in a short window, not just logging that goes
unread.

*(Renamed from "Security Logging and Monitoring Failures" specifically to foreground alerting,
a log nobody looks at doesn't protect anyone.)*

## 10-payment-transfer.java — A10:2025 Mishandling of Exceptional Conditions

**Risk:** When crediting the destination account fails partway through a transfer, the
`catch` block logs a warning and lets execution continue as if nothing went wrong, returning a
success result to the customer. The money has already left the source account but never
arrived at the destination, an inconsistent, incorrect state caused entirely by how the failure
path was (mis)handled, not by any single line of "wrong" business logic.

**Fix:** On failure partway through a multi-step operation, either roll back the steps already
completed (compensating the debit) or fail the whole operation and report the *actual* failure
to the caller, never swallow an exception from a critical step and report success anyway.

*(This category is entirely new in the 2025 edition, it didn't exist as a named category in
2021.)*

## 11-avatar-fetch-ssrf.java — A01:2025 Broken Access Control (SSRF)

**Risk:** The server fetches whatever URL a customer supplies, from inside the server's own
network. An attacker could point it at an internal-only address (e.g. a cloud metadata service
that returns credentials with no authentication) and have the server retrieve that data for
them, something the attacker's own browser could never reach directly.

**Fix:** Validate and restrict the target: only allow specific expected domains/schemes, resolve
and check the destination isn't a private/internal IP range before fetching, and ideally proxy
the fetch through a locked-down, dedicated outbound service rather than the main application.

*(This was its own category, "A10:2021 Server-Side Request Forgery (SSRF)"; the 2025 edition
folds it into Broken Access Control, since the underlying problem in both cases is a request
reaching a resource it shouldn't have access to.)*

## Which categories return in Sprint 8

**A01 (Broken Access Control), A05 (Injection), and A07 (Authentication Failures)** get a full
dedicated deep-dive in Sprint 8. Everything above is intentionally conceptual breadth for this
module, not the final depth these three will eventually get.
