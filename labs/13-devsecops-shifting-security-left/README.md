# Module 13 Lab — DevSecOps: Shifting Security Left

## Objectives

By the end of this lab you will have:

- Found a real, known vulnerability in a dependency using the OSV API, and fixed it
- Reproduced a secret-scanning finding yourself, fixed the code, and confirmed the secret still
  exists in git history — the exact "fixing the code isn't enough" lesson from the demo

## Part A — Dependency Scanning

### Task

```bash
cd labs/13-devsecops-shifting-security-left
mvn dependency:tree
```

One of the two dependencies has a real, known CVE. Query the OSV API for each dependency listed
(same pattern the demo used) and identify which one:

```bash
curl -s -X POST \
  -d '{"version":"<version>","package":{"name":"<groupId>:<artifactId>","ecosystem":"Maven"}}' \
  "https://api.osv.dev/v1/query"
```

Once you've found it, fix `pom.xml` by bumping to a version with zero known vulnerabilities.
Confirm with the same OSV query against the new version — expect `{}`.

### Acceptance criteria

- You can name the CVE ID and one-sentence summary of the vulnerability you found
- The OSV query against your fixed version returns `{}`

## Part B — Secret Detection (Do This in a Throwaway Local Repo)

**Do not do this inside the `leap-sprint7` labs repo.** Create a separate, throwaway
folder anywhere on your machine — this exercise deliberately commits a (fake) secret, and the
point of Part B is practicing the cleanup, not leaving a trace in a real shared repository.

### Setup

```bash
mkdir secrets-lab && cd secrets-lab
git init
mkdir -p src/main/java/com/neueda/leap/sprint7
```

Create `src/main/java/com/neueda/leap/sprint7/PaymentGateway.java` with this content (the
values are fake and non-functional, formatted to look realistic on purpose — that's what makes
this a fair test of the tool):

```java
package com.neueda.leap.sprint7;

public class PaymentGateway {
  private static final String STRIPE_API_KEY = "stripe_key_placeholder_for_training";
  private static final String AWS_SECRET_ACCESS_KEY = "aws_secret_placeholder_for_training";

    public void charge(double amount) {
        System.out.println("Charging " + amount);
    }
}
```

```bash
git add -A
git -c user.email="you@example.com" -c user.name="You" commit -m "Add PaymentGateway"
```

### Task

1. Run gitleaks against your throwaway repo:
   ```bash
   docker run --rm -v "<path-to-secrets-lab>:/repo" -w /repo zricethezav/gitleaks:latest detect -v
   ```
   Confirm it finds both secrets.
2. Fix `PaymentGateway.java` — move both values to `System.getenv(...)`, matching the demo's
   fix for `NotificationService`.
3. Commit the fix, then rerun the SAME gitleaks command from step 1.
4. Write down, in your own words: what does the result tell you, and what is the ONE action
   that actually neutralizes the exposure (not just tidies the code)?
5. Run a working-tree-only scan (`--source=/repo --no-git`, no volume path needed beyond the
   repo itself) and compare its result to step 3's.

### Acceptance criteria

- Step 1's gitleaks run finds 2 leaks
- Step 3's gitleaks run (after the code fix) STILL finds 2 leaks — if it finds 0, you've likely
  scanned with `--no-git` by mistake; rerun in full-history mode
- Your written answer for step 4 names credential rotation specifically, not just "delete the
  file" or "rewrite history"
- Step 5's working-tree-only scan finds 0 leaks, demonstrating the contrast directly

## Deliverable

- A fixed `pom.xml` (Part A) with the CVE ID you found written in a comment or commit message
- Your written answer to Part B, step 4
