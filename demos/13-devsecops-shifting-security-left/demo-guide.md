# Module 13 Demo Guide — DevSecOps: Shifting Security Left

## Where the Name "Shift Left" Comes From

Draw a software delivery timeline, left to right: **Code → Commit → Build → Test → Staging →
Production**. "Left" on that diagram means EARLIER — closer to the moment code is written, not
closer to the moment it ships.

Traditionally, security review sits on the RIGHT of that timeline — a manual audit, done by a
specialist team, right before release (or worse, discovered only after an incident in
production). "Shifting left" means literally moving that same kind of check leftward: replacing
(or supplementing) a late manual audit with automated checks that run at commit or build time —
exactly what today's three tools do.

**Why bother moving it?** The same vulnerability costs wildly different amounts to fix depending
on where in that timeline it's caught:

| Found at... | Cost |
|---|---|
| Commit | Change one line, before anyone else even sees it |
| Code review | A comment, a small diff, still pre-merge |
| Staging | A new build, a redeploy, a delayed release |
| Production | An incident, a patch under pressure, possibly a breach disclosure |

Same finding, same eventual fix — but the cost (in time, risk, and often money) grows the further
right it travels before anyone catches it. This is the entire economic argument for "shifting
left," and it's the same argument Module 11 made for characterisation tests catching a regression
before release, applied specifically to security.

Today covers three real, distinct categories of automated check, each catching a different kind
of mistake — SonarQube's security rules (SAST), a dependency vulnerability scanner, and a secret
scanner — and wires all three into the same CI pipeline Module 12 already started building.

## 1. SAST: Static Application Security Testing

Module 12's SonarQube analysis already IS a SAST tool — its rules aren't only about
maintainability. Revisit the real findings from `shared/starter-codebase`:

```
java:S2095  TradeReportGenerator.java:18  BLOCKER (type: BUG)
  "Use try-with-resources or close this BufferedReader in a finally clause."
```

This is a genuine security-adjacent finding, not just a style one: an unclosed resource under
attacker-controlled load is a real denial-of-service vector (exhausting file handles). SonarQube
tags issues with a `type` (`BUG`, `VULNERABILITY`, `CODE_SMELL`) and, for genuine
`VULNERABILITY` findings, an OWASP/CWE category — worth filtering the dashboard by `type=VULNERABILITY`
to see security-specific findings distinct from general code quality.

**The point**: you likely already have a SAST tool running from Module 12. DevSecOps isn't
always about adding a new tool — it's often about USING the security-relevant output of a tool
you already have.

## 2. Dependency Scanning: Vulnerable Libraries

Your own code can be perfect and still ship a real vulnerability — through a dependency.

```bash
cd demos/13-devsecops-shifting-security-left/dependency-scan-demo
mvn dependency:tree
```

```
com.fidelity.leap:sprint7-m13-dependency-scan-demo:jar:0.1.0
\- org.apache.logging.log4j:log4j-core:jar:2.14.1:compile
   \- org.apache.logging.log4j:log4j-api:jar:2.14.1:compile
```

`log4j-core:2.14.1` is a real, deliberately-pinned vulnerable version. Query the OSV
(Open Source Vulnerabilities) database — a free, public vulnerability API used by real scanning
tools:

```bash
curl -s -X POST \
  -d '{"version":"2.14.1","package":{"name":"org.apache.logging.log4j:log4j-core","ecosystem":"Maven"}}' \
  "https://api.osv.dev/v1/query"
```

Verified real result: **7 known vulnerabilities**, including:

```
ID: GHSA-jfh8-c2jp-5v3q  (CVE-2021-44228)
Summary: Remote code injection in Log4j
Severity: CRITICAL
```

This is Log4Shell — one of the most severe remote-code-execution vulnerabilities ever found in a
widely-used library, entirely INSIDE a transitive dependency, with zero mistakes in your own
code. **Point at this directly**: Module 12's SonarQube analysis would find nothing wrong here —
SAST examines code you wrote, not libraries you pulled in. This is why dependency scanning is a
genuinely separate category of tool, not a subset of SAST.

Fix it — bump the version:

```xml
<version>2.25.4</version>
```

Reverify:

```bash
curl -s -X POST \
  -d '{"version":"2.25.4","package":{"name":"org.apache.logging.log4j:log4j-core","ecosystem":"Maven"}}' \
  "https://api.osv.dev/v1/query"
```

Verified real result: `{}` — zero known vulnerabilities for this version.

## 3. Secret Detection: Credentials Committed to Git

The third category catches something neither SAST nor dependency scanning does: a real
credential, accidentally committed.

```bash
docker run --rm -v "<repo-path>:/repo" -w /repo zricethezav/gitleaks:latest detect -v
```

Run against a small demo repository containing a Java class with hardcoded credentials, verified
real output:

```
Finding:     ...CK_WEBHOOK_TOKEN = "slack_bot_token_placeholder"
RuleID:      slack-bot-token
File:        src/main/java/.../NotificationService.java
Line:        11

Finding:     ...static final String AWS_ACCESS_KEY = "aws_access_key_placeholder"
RuleID:      generic-api-key
Line:        13

leaks found: 2
```

## The Uncomfortable Part: Fixing the Code Isn't Enough

Fix the class properly — move both values to environment variables:

```java
private static final String SLACK_WEBHOOK_TOKEN = System.getenv("SLACK_WEBHOOK_TOKEN");
private static final String AWS_ACCESS_KEY = System.getenv("AWS_ACCESS_KEY");
```

Commit the fix. Rerun gitleaks (full history mode, the default):

```
leaks found: 2
```

**Still 2.** The secret is gone from today's code — but it is still sitting in an EARLIER commit,
forever, unless that history is explicitly rewritten. Confirm this with a working-tree-only scan
(no git history) for contrast:

```bash
docker run --rm -v "<repo-path>:/repo" zricethezav/gitleaks:latest detect --source=/repo --no-git -v
```

```
no leaks found
```

**Point at both results side by side**: the code you'd read today is clean. The repository is
not. This is the single most important, most counter-intuitive lesson about a leaked secret:

1. **Fixing the latest commit does not remove the secret from history** — anyone with clone
   access can `git log -p` and find it.
2. **The only correct response is rotating the credential** (making the leaked value useless,
   at the source system — AWS, Slack, wherever it belongs) — deleting or rewriting the commit is
   good hygiene, but rotation is what actually neutralizes the exposure.
3. History CAN be rewritten (`git filter-repo`, BFG Repo-Cleaner) to remove a secret from every
   commit, but that's a disruptive, coordinated operation (rewrites every commit hash downstream)
   — not something to reach for casually, and never a substitute for rotation.

## A Real Baseline, From This Repo

Running gitleaks against the WHOLE `leap-sprint7` repo (not just the demo scratch repo)
flags 4 findings — every one of them the fake credentials THIS module's own demo guide and lab
README contain, as documentation text. This is a genuinely common real-world situation: teaching
material, sample `.env.example` files, and README snippets often contain realistic-looking fake
credentials, and a naive scanner can't always tell fake from real.

The fix isn't disabling the scanner — it's a maintained baseline (`.gitleaksignore` at the repo
root) listing each confirmed false positive by its exact fingerprint, with a comment explaining
WHY it's safe to ignore. See `.gitleaksignore` in this repo. Rerunning with the baseline in place:

```
no leaks found
```

**The discipline that matters**: every entry in a baseline file should be reviewed deliberately,
one at a time — a baseline that gets bulk-approved without checking each entry is a scanner that's
been silently turned off.

## Wiring All Three Into CI

```groovy
stage('Security Scans') {
    parallel {
        stage('Dependency Check') {
            steps {
                sh 'mvn dependency:tree'
                // In practice: a dedicated plugin (OWASP dependency-check-maven,
                // or a hosted scanner) fails the build on new CRITICAL findings.
            }
        }
        stage('Secret Scan') {
            steps {
                sh 'docker run --rm -v $(pwd):/repo -w /repo zricethezav/gitleaks:latest detect'
            }
        }
    }
}
```

Running dependency and secret scanning in `parallel` alongside the Module 12 `Quality Gate`
stage keeps the pipeline fast — these three checks don't depend on each other's results.

## The Concept, Named

- **Shift left**: catching a security problem at commit/build time is cheaper (and safer) than
  catching it in production — the same economic argument as Module 11's characterisation tests
  catching a regression before release, applied to security specifically.
- **SAST**: analyzes code YOU wrote. Won't find a vulnerable dependency.
- **Dependency scanning**: analyzes libraries you PULLED IN. Won't find a hardcoded secret.
- **Secret scanning**: analyzes what got COMMITTED, including history. Won't find a code-quality
  issue or a vulnerable library.
- Three genuinely different blind spots — a real DevSecOps pipeline runs all three, not one.

## Transition to the Lab

Learners get a small project with one deliberately vulnerable dependency and one deliberately
committed credential — find both using the real tools demonstrated here, fix both correctly
(including reasoning about git history for the secret), and verify with the same commands.
