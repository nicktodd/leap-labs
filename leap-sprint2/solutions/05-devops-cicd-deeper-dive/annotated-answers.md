# Module 05 Lab — Annotated Answers (Instructor Reference)

## 1. Stages and outcomes

| Stage | Outcome |
|---|---|
| Checkout | Passed |
| Build | Passed |
| Test | Passed (14/14 tests) |
| Acceptance Test | Passed (8/8 scenarios against staging) |
| Security Scan | **Failed** |
| Deploy | Never ran |

Worth drawing out: Test and Acceptance Test are checking different things. Test is unit-level
(does this method behave correctly in isolation). Acceptance Test deploys the build to staging
and checks the feature against its acceptance criteria (from Sprint 2 Modules 01-02), i.e. does
it satisfy what the Product Owner actually asked for. A pipeline can be green on one and not
the other.

## 2. The failure, quoted

```text
[WARN] jackson-databind:2.9.8 has 1 known vulnerability
[WARN] CVE-2019-12384: Polymorphic Typing issue, allows remote code execution
[WARN] Severity: CRITICAL (CVSS 8.1)
[ERROR] Build failed: 1 CRITICAL vulnerability found, threshold is 0 CRITICAL
```

Produced by `dependency-check`, a software composition analysis tool that scans a project's
dependencies against known vulnerability databases (the NVD, National Vulnerability Database).

## 4. Plain-English explanation (example)

"The pipeline found that one of the external libraries our code depends on
(`jackson-databind`) has a publicly known, serious security flaw that could let an attacker run
their own code on our server. Our pipeline is set up to stop automatically if it finds any
vulnerability this severe, so it stopped before deploying, rather than shipping the flaw to
production."

## 5. Connection to branch protection

If `main` requires this pipeline to pass and this PR had been merged anyway (say, because
branch protection wasn't configured, or someone had override permissions), the vulnerable
dependency would have shipped to production with no automated check having stopped it, exactly
the scenario branch protection combined with a security-scanning pipeline stage exists to
prevent.

## What to check as an instructor

- Delegates correctly identify Security Scan as the failed stage, not Test (a common
  misread, since Test's results are the most recently *unfamiliar looking* output right above
  it).
- The plain-English explanation avoids jargon a stakeholder wouldn't know (CVE, CVSS, NVD)
  without briefly defining it.
- Delegates actually looked up CVE-2019-12384 rather than accepting GenAI's explanation
  unverified, this is the whole point of the exercise, not an optional extra.
