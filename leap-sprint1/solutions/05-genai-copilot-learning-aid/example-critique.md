# Module 05 Lab — Example Critique (Instructor Reference)

A realistic example of what a completed critique looks like. Actual Copilot wording will vary
between sessions.

## Jenkinsfile snippet

**Copilot's explanation (paraphrased):** "This pipeline has three stages. Build runs a Maven
package. Test runs Maven tests and always publishes JUnit results, even if the tests fail.
Archive saves the built JAR as a Jenkins build artifact and records a fingerprint for it."

**Claim 1:** "`post { always { junit ... } }` publishes results even if the tests fail."
**Verdict:** Accurate. `post always` runs regardless of the stage outcome, which is exactly why
JUnit results should be published there rather than inside the `steps` block.

**Claim 2:** "`fingerprint: true` records a fingerprint for the artifact."
**Verdict:** Partially accurate. It's correct that it fingerprints the file, but Copilot didn't
mention *why*: fingerprinting lets Jenkins track that exact build artifact across other jobs
and pipelines that consume it, which matters once we have team pipelines depending on shared
artifacts (Sprint 3+). Worth adding that nuance rather than accepting the answer as complete.

## Dockerfile snippet

**Claim:** "Using `eclipse-temurin:21-jre-alpine` instead of a full JDK image keeps the final
image smaller because it only includes the Java Runtime Environment, not the full Development
Kit, and Alpine is a minimal Linux distribution."
**Verdict:** Accurate. Confirmed against the Eclipse Temurin image documentation: `-jre` tags
exclude compiler tooling not needed at runtime, and Alpine-based images are meaningfully
smaller than Debian-based equivalents.

## Reflection (example answer)

Good use case: explaining an unfamiliar Jenkinsfile stage before touching CI/CD pipelines in
Module 10, so I understand what I'm about to change rather than guessing.
Caution needed: anything involving specific numbers, versions, or security implications (like
whether an image has known CVEs) should always be verified against an official source, not
taken as given from a single explanation.
