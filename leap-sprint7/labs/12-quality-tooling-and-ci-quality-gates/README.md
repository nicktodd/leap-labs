# Module 12 Lab — Quality Tooling & CI Quality Gates

## Objectives

By the end of this lab you will have:

- Run a real SonarQube analysis against a real quality gate, and watched it genuinely fail
- Read the tool's actual findings — not guessed at them — and fixed each one
- Rerun the analysis to prove the gate now passes

## Setup

Reuse the demo's SonarQube container (`sonarqube-sprint7`) and the `Sprint7 Strict Gate` created
in the demo. If you don't have a token yet, generate one: **My Account → Security → Generate
Token**.

```bash
cd labs/12-quality-tooling-and-ci-quality-gates
mvn compile
```

## Task

### Part A — See It Fail

```bash
mvn sonar:sonar -Dsonar.token=<your-token> -Dsonar.qualitygate.wait=true
```

**Before fixing anything**, note that this fails. Open the SonarQube dashboard for
`sprint7-m12-lab` (or query `/api/issues/search?componentKeys=sprint7-m12-lab`) and read the
actual issues reported — do not guess what might be wrong from looking at the code alone. There
are 4: one BUG, three CODE_SMELLs.

### Part B — Fix Every Reported Issue

Fix `SettlementReporter.java` until none of the 4 original issues remain. Some hints, without
giving away exact fixes:

- The `BufferedReader` is opened but never explicitly closed — what construct guarantees a
  resource gets closed even if an exception is thrown partway through reading?
- One local variable is assigned a value that's never read before being overwritten — the tool
  will tell you exactly which line.
- Building a growing string with `+=` inside a loop has a named, more efficient alternative.
- `System.out.println` is flagged specifically — what's the standard alternative for a real
  application (not a quick demo script)?

### Part C — Rerun, and Read Carefully

Rerun the analysis. **If new issues appear that weren't there before, read what they say — a
fix for one problem can introduce a different one** (this genuinely happened while building this
lab's solution — the model answers explain exactly what and why). Keep fixing and rerunning until
the gate passes with zero open issues.

## Deliverable

A fixed `SettlementReporter.java` that passes the `Sprint7 Strict Gate` with `bugs: 0`,
`code_smells: 0`, `vulnerabilities: 0`.

## Acceptance criteria

- `mvn sonar:sonar -Dsonar.qualitygate.wait=true` exits with `BUILD SUCCESS` and
  `QUALITY GATE STATUS: PASSED`
- The SonarQube dashboard for this project shows 0 open bugs and 0 open code smells
- You can name, for each original issue, which specific change fixed it (not "I changed some
  things and it went green")
