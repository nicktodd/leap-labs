# Demo: Module 09 — OWASP Top 10

**Duration:** 25 minutes
**Prerequisite:** The [`vulnerable-examples/`](../../labs/09-owasp-top-10/vulnerable-examples)
folder from the lab. GitHub Copilot Chat available. This module is longer than most, OWASP is
ten categories deep and worth the time.

> Uses the **OWASP Top 10:2025** edition (finalized January 2026), not the older 2021 edition
> still floating around in a lot of existing training material and blog posts. If your own
> notes or memory say "A06: Vulnerable and Outdated Components" or "A10: SSRF", that's the 2021
> numbering, flag the difference explicitly so delegates aren't confused by other sources later.

## Part 1: What OWASP is, and why it matters here (3 min)

Narration: OWASP (Open Web Application Security Project) is a non-profit that publishes
freely-available security research, most famously the **OWASP Top 10**, a ranked list of the
most critical web application security risks, refreshed periodically as the threat landscape
shifts, the 2021 edition was replaced by the **2025 edition** (finalized January 2026), which
is what this module uses throughout. It's not a compliance checklist invented in-house, it's
an industry-standard reference point, which is exactly why it's worth learning properly rather
than treating as a box to tick. In financial services specifically: PaySprint handles money and
personal financial data, the categories in this list map directly onto real regulatory and
reputational risk, not just abstract "best practice."

Mention up front: **A01 (Broken Access Control), A05 (Injection), and A07 (Authentication
Failures)** get a full dedicated deep-dive in Sprint 8. Today is conceptual breadth across all
ten, not depth on those three specifically.

## Part 2: What actually changed from the 2021 edition (2 min)

Narration, briefly, using the slide: Security Misconfiguration jumped from #5 to #2, "Vulnerable
and Outdated Components" was broadened into **Software Supply Chain Failures** (not just old
version numbers now, the whole dependency and build pipeline), SSRF was folded into **Broken
Access Control** rather than standing alone, and **Mishandling of Exceptional Conditions** is a
brand new category about what happens when error handling itself is the vulnerability. Worth
saying out loud: security guidance changes, and checking you're working from the current
edition is itself a professional habit, not a one-off correction.

## Part 3: Walk the ten categories, briefly (5 min)

Talk through all ten at a glance, using the slide deck's summary slide. Don't linger, this is
priming before the worked examples: A01 Broken Access Control, A02 Security Misconfiguration,
A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure
Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security
Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions.

## Part 4: Four worked examples, in depth (13 min)

Live-demo these four from `vulnerable-examples/`, roughly 3 minutes each. For each: read the
code together, ask the room to name the category before you confirm it, then ask Copilot Chat
to explain the risk, and critique its explanation before accepting it.

### A05 Injection — `05-transaction-search.java`

The SQL query is built by string concatenation. Ask Copilot: *"What could go wrong if
merchantName contains a single quote?"* Narration: a merchant name of
`' OR '1'='1` turns the WHERE clause into something that matches every row. The fix is a
parameterised query (`PreparedStatement`), never string concatenation with user input, full
stop. Worth noting: this dropped from #3 to #5 in the 2025 ranking, still serious, just no
longer the single most common finding industry-wide.

### A02 Security Misconfiguration — `02-Dockerfile`

Point out three separate problems in one file: a remote debug port left open in production
(`5005`), a full JDK image where Module 06 taught a JRE-only runtime stage is enough, and a
database password sitting in plain text as an `ENV` line, visible to anyone who can run `docker
inspect` on the container. Tie back to Module 06: this is exactly the kind of thing a
least-privilege, minimal-base-image Dockerfile avoids by construction. This category jumped from
#5 to #2 in the 2025 edition, worth mentioning why: misconfiguration is showing up far more
often in real incident data than it used to.

### A03 Software Supply Chain Failures — `03-pom-dependencies.xml`

Recognise `jackson-databind:2.9.8`, this is the same CVE-2019-12384 from Module 05's pipeline
log. Narration: in the 2021 edition this was "Vulnerable and Outdated Components", just about
version numbers. The 2025 edition broadens it deliberately to the whole supply chain: where
dependencies come from, whether your build system can be tampered with, and whether you can
trust the distribution path an artifact took to reach you, not only whether the version number
itself is current.

### Bonus: SSRF, now under A01 — `11-avatar-fetch-ssrf.java`

The server fetches whatever URL the customer supplies. Ask Copilot to explain what an attacker
could do with this. Narration: a customer could supply a URL pointing at an internal-only
service (for example, a cloud provider's metadata endpoint, which often has no authentication
and can leak credentials), and the server, not the attacker's own browser, makes that request
from inside the network. In the 2021 edition this was its own category (A10: SSRF); the 2025
edition folds it into **A01: Broken Access Control**, the underlying idea in both cases is a
request reaching somewhere it shouldn't have access to.

## Part 5: Handing off to the lab (2 min)

Narration: you've seen four worked in depth. The lab has all eleven files (ten categories plus
the SSRF bonus), work through the remaining seven with a partner the same way, name the
category, explain the risk, propose a fix, before checking the model answers.

## Key message

Every one of these ten categories has a recognisable shape once you've seen it named once.
That's the actual goal of this module, not memorising OWASP's numbering (which visibly changes
between editions), but building the pattern recognition to say "that looks like an injection
risk" or "that looks like broken access control" on sight, in code you've never seen before.
