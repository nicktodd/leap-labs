# Module 12 Demo Guide — Quality Tooling & CI Quality Gates

Module 10 built a small, hand-written scanner. Today swaps it for the real thing — SonarQube —
run against the same `shared/starter-codebase`, and wired into a CI pipeline stage that can
actually block a build.

## Where SonarQube Actually Runs

Today's demo is one specific choice among several a real team makes:

- **Self-hosted (SonarQube Server)** — you run it yourself: Docker (today), a VM, or a cluster
  for larger teams. Your code never leaves your own infrastructure, but you own patching,
  backups, and uptime. **Community Edition** (what we're using) is free and self-hosted;
  **Developer** and **Enterprise** editions are paid, self-hosted, and add branch/pull-request
  analysis, more languages, and organization-wide security reporting.
- **Cloud-hosted (SonarCloud)** — SonarSource runs it; you connect a GitHub/GitLab/Bitbucket/
  Azure DevOps repository and it analyzes on every push or PR, with zero server to maintain.
  **Free** for public/open-source repositories; **paid** (Team/Enterprise tiers) for private
  ones, priced by lines of code or seats.

The trade-off is control vs operational effort: self-hosted means full control over your data
and infrastructure, at the cost of running it; SonarCloud means trusting a third party with your
source code, in exchange for never touching a server. Neither is "correct" — it depends on
whether the org already has infrastructure to run this on, and whether sending source code to a
third party is acceptable under its compliance policy.

**Today's Community Edition container is the free, self-hosted tier** — the same core analysis
engine every paid tier is built on top of. Everything demonstrated today (rules, quality gates,
the CI integration) works identically on every edition; paid tiers add MORE capability, not a
different core.

## Stand Up SonarQube

```bash
docker run -d --name sonarqube-sprint7 -p 9000:9000 sonarqube:community
```

Takes 1-2 minutes to fully start (it runs its own embedded database on first boot — fine for a
dev/training instance, never for production, exactly like Module 5's KRaft-mode Kafka broker was
fine for training but not how a real broker cluster is usually configured).

```bash
curl -s http://localhost:9000/api/system/status
```

Wait for `"status":"UP"`. Log in at `http://localhost:9000` with `admin` / `admin` (it will
prompt you to change the password — for this training instance, that's optional). Generate a
token: **My Account → Security → Generate Token**.

## Run the Real Analysis

```bash
cd shared/starter-codebase
mvn clean test
mvn sonar:sonar -Dsonar.token=<your-token> -Dsonar.qualitygate.wait=true
```

Verified real output (against the codebase as Module 11 left it):

```
QUALITY GATE STATUS: PASSED - View details on http://localhost:9000/dashboard?id=sprint7-starter-codebase
BUILD SUCCESS
```

**Before celebrating — look at what it actually found**, via the dashboard or the API:

```
bugs: 2
vulnerabilities: 0
code_smells: 8
duplicated_lines_density: 0.0
ncloc: 117
```

Two real, `BLOCKER`-severity BUGS, and the gate still says PASSED. This is the single most
important thing to understand about SonarQube before using it for real.

## The Gotcha: What "PASSED" Actually Means

SonarQube's default gate ("Sonar way") is built around **new code**, not the whole codebase —
its conditions are things like "no new bugs in code changed since a baseline date." On a fresh
analysis of an old codebase with no prior baseline, almost everything looks like "new," and the
gate can still pass even with real, serious issues sitting in the report, because the specific
CONDITIONS configured don't happen to be violated.

**Point at the two real bugs directly** — both are genuine reliability issues, not style
nitpicks:

```
java:S2095  TradeReportGenerator.java:18  BLOCKER
  "Use try-with-resources or close this BufferedReader in a finally clause."

java:S2095  TradeReportGenerator.java:50  BLOCKER
  "Use try-with-resources or close this FileWriter in a finally clause."
```

Neither `BufferedReader` nor `FileWriter` gets closed if an exception is thrown mid-loop — a real
resource leak, not a style preference. A quality GATE that ignores this is a gate that isn't
actually protecting anything.

**Also worth pointing at**: `java:S1643` on line 38 — `"Use a StringBuilder instead."` This is
the EXACT performance issue Module 10's lab asked learners to reason about manually (string
concatenation in a loop). A real tool independently found the exact same thing a human found by
inspection — worth confirming the manual analysis was right, not replacing it.

## Building a Gate That Actually Protects Something

Create a custom, stricter gate:

**Quality Gates → Create** → name it `Sprint7 Strict Gate`, add conditions:
- `Bugs` is greater than `0` (on Overall Code, not just New Code)
- `Reliability Rating` is worse than `A` (on Overall Code)

Assign it to the project: **Project Settings → Quality Gate → Sprint7 Strict Gate**.

Rerun the exact same analysis, no code changes:

```bash
mvn sonar:sonar -Dsonar.token=<your-token> -Dsonar.qualitygate.wait=true
```

Verified real output:

```
QUALITY GATE STATUS: FAILED - View details on http://localhost:9000/dashboard?id=sprint7-starter-codebase
BUILD FAILURE
[ERROR] Failed to execute goal ... QUALITY GATE STATUS: FAILED
```

**Same code. Same bugs, which were already there.** Only the gate's CONDITIONS changed — and
now Maven itself exits with a non-zero status. This is what "quality gate" is supposed to mean:
a build that fails, loudly, when the code doesn't meet a bar someone deliberately set.

## Wiring It Into CI

```groovy
stage('Quality Gate') {
    steps {
        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
            sh 'mvn -B sonar:sonar -Dsonar.token=$SONAR_TOKEN -Dsonar.qualitygate.wait=true'
        }
    }
}
```

See `shared/starter-codebase/Jenkinsfile`. `sonar.qualitygate.wait=true` is the critical setting
— without it, this stage reports success the instant the analysis is UPLOADED, before anyone
checks whether the gate passed. With it, the Maven process itself blocks and exits non-zero on
failure, which is what makes a Jenkins pipeline stage actually fail rather than silently
continuing past a red gate.

## The Concept, Named

- **Static analysis tool**: examines code without running it, flagging patterns that correlate
  with real bugs (like unclosed resources) as well as maintainability concerns (naming,
  duplication, complexity) — Module 10's scanner was a tiny version of exactly this.
- **Quality gate**: a named set of PASS/FAIL conditions, evaluated against an analysis. The
  default gate exists, has a name, and is not automatically strict — someone has to look at what
  it actually checks.
- **New code vs overall code**: most default gates focus on new/changed code, on the theory that
  fixing a decade of legacy issues at once isn't realistic — but that same design means a gate
  can PASS while real, severe, pre-existing issues sit untouched in the report. Know which one
  your gate is checking.
- **`sonar.qualitygate.wait=true`**: the setting that turns "analysis uploaded" into "build
  actually blocked" — the difference between a quality gate that exists and one that enforces
  anything.

## Transition to the Lab

Learners get a small, self-contained file that fails the strict gate for real, fix each issue the
tool reports, and rerun the analysis until it goes green — practicing the actual workflow: read
the tool's report, fix what it names, verify, repeat.
