# Demo: Module 05 — DevOps Fundamentals & CI/CD Deeper Dive

**Duration:** 10 minutes
**Prerequisite:** `sample-pipeline-log.txt` open or projected. GitHub Copilot Chat available.

## Part 1: Recap, quickly (2 min)

Narration: Sprint 1 Module 09 covered CI/CD as a discipline (build, test, package) and the
CI/Delivery/Deployment distinction. Module 10 opened Jenkins itself and diagnosed a broken Test
stage using GenAI as a first port of call. Today extends both: a longer pipeline with a
security gate, and a real branch-protected `main` (from this sprint's Module 03) actually
depending on it passing.

## Part 2: CI, CD, and DevOps culture (2 min)

Narration, pointing at the diagram: CI and CD are specific technical practices, tools and
pipelines. DevOps is the broader culture they sit inside, shared ownership between development
and operations, blameless learning from failures, and treating reliability as everyone's job,
not a separate team's. CI/CD without that culture is just automation; the culture is what makes
teams actually trust and act on what the automation tells them.

## Part 3: Walking the pipeline log (3 min)

Read through `sample-pipeline-log.txt` stage by stage: Checkout, Build, and Test (unit tests)
all pass, then **Acceptance Test** also passes, deploying the build to staging and running 8
scenarios against it to confirm the feature actually satisfies its acceptance criteria (from
Module 01/02's story-writing work), not just that it compiles and unit-tests cleanly. Then
**Security Scan** fails: a dependency scan tool found a critical vulnerability
(`CVE-2019-12384`) in a library the project depends on, and the pipeline is configured to fail
on any CRITICAL finding. **Deploy never runs.**

Narration: point out that Acceptance Test and Security Scan are checking two completely
different things. Acceptance Test asks "does this do what the Product Owner asked for?"
Security Scan asks "does this introduce a known risk?" A pipeline can pass one and fail the
other, and both matter.

## Part 4: Interpreting it with GenAI (2 min)

Select the Security Scan section of the log and ask Copilot Chat:

```text
This Jenkins pipeline failed at the Security Scan stage. Explain in plain English what this
log output means and why the build failed.
```

Narration: same habit as every prior module, read the explanation, then verify the specific
claim (in this case, look up CVE-2019-12384 yourself, or check the dependency-check
documentation) before repeating it to anyone else as fact.

## Part 5: How this protects main (1 min)

Narration: tie back to Module 03. If this repository's `main` branch requires this pipeline to
pass before a PR can merge, this vulnerable dependency **never reaches production**, full stop.
That's the practical meaning of "a failing pipeline protects main", not an abstract idea.

## Part 6: Jenkins vs GitHub Actions (2 min)

Point at the comparison diagram. Both do the same job, run pipelines on events. Jenkins:
self-hosted, highly configurable, strong fit for complex or regulated environments already
running their own infrastructure. GitHub Actions: cloud-native, tightly integrated with GitHub
itself, faster to stand up for simpler workflows. This programme uses Jenkins throughout,
mention GitHub Actions exists and why some teams choose it, but keep hands-on work in Jenkins.

## Key message

A pipeline stage failing isn't a nuisance, it's the system doing exactly its job: catching a
real problem before it reaches customers, the same way Module 03's PR review catches problems
before they reach main.
