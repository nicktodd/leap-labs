# Module 10 Lab — Diagnosis Walkthrough (Instructor Reference)

## The break

`starter/Jenkinsfile`'s Test stage has:

```groovy
junit 'target/test-reports/*.xml'
```

Maven Surefire's default output directory is `target/surefire-reports/`, not
`target/test-reports/`. The glob matches nothing.

## Console Output symptom

```text
[Pipeline] junit
ERROR: No test report files were found. Configuration error?
```

The build is marked **UNSTABLE** or **FAILURE** depending on Jenkins configuration, even though
`mvn -B test` itself passed. This is a good teaching moment: the underlying tests were fine, the
*reporting* step was misconfigured. Delegates should notice the Build and Test shell commands
both report success in the console log, before the `junit` step itself fails.

## Expected GenAI explanation (paraphrased)

"This error means Jenkins's JUnit plugin couldn't find any XML report files matching the glob
pattern you gave it. The most common cause is a mismatch between where your test tool actually
writes reports and the path configured in the `junit` step. For a standard Maven project using
Surefire, reports are written to `target/surefire-reports/`, so if your pipeline is looking in
`target/test-reports/`, that would explain it."

This is a case where the GenAI explanation is very likely to be accurate and directly
actionable, a good example of the tool working well as a learning aid.

## The fix

```groovy
junit 'target/surefire-reports/*.xml'
```

## Confirming locally

```bash
mvn test
dir target\surefire-reports
```

Delegates should see `.xml` and `.txt` report files in that folder, confirming the GenAI
explanation before applying the fix, not just after.
