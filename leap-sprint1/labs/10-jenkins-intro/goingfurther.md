# Going Further — Extending Your Jenkins Pipeline

Finished early? Here are some ways to extend the pipeline you just fixed. Pick whichever looks
most interesting — you don't need to do all of them. They build roughly in order of difficulty,
and most of them add directly onto your existing `Jenkinsfile` and `pom.xml`.

If you get stuck, [`solutions/Jenkinsfile_GoingFurther`](solutions/Jenkinsfile_GoingFurther) shows
one way of combining several of these together — but try it yourself first.

## 1. Add a code coverage stage

Report how much of the code your tests actually exercise.

**Hints:** the JaCoCo Maven plugin is the standard tool for this — it needs adding to the
`<plugins>` section of `pom.xml` and bound to run around the `test` phase. Once it's producing a
report under `target/site/jacoco`, add a new pipeline stage that runs it and archives the output
(`archiveArtifacts` works fine if you just want the HTML report saved; the HTML Publisher plugin
gives you a nicer in-Jenkins view if it's installed on your instance).

## 2. Add a static analysis stage

Catch style or quality issues automatically instead of relying on code review.

**Hints:** `maven-checkstyle-plugin` or `spotbugs-maven-plugin` are both straightforward to bolt
onto this project. Add the plugin to `pom.xml`, then add a stage that runs its `check` goal. Think
about whether you want the build to fail on violations or just report them — that changes what
Maven goal/config you reach for.

## 3. Run stages in parallel

Once you have a second stage alongside `Test` (coverage or static analysis), run them side by
side instead of one after another.

**Hints:** look at the `parallel` step — it takes a map of named branches, each with its own
`steps`. Both branches need the code already built, so this only makes sense *after* your `Build`
stage, not instead of it.

## 4. Add a manual approval gate

Pause the pipeline before `Archive` and require a human to click "proceed."

**Hints:** the `input` step is what you want. Think about where in the stage order it belongs, and
what happens if nobody responds — an unattended `input` step will hold a Jenkins executor open
indefinitely unless you wrap it in a `timeout`.

## 5. Parameterize the build

Let whoever triggers the build choose something — e.g. whether to skip tests, or which
environment a build is "for."

**Hints:** a `parameters {}` block at the top of the pipeline (try `booleanParam` or `choice`)
defines what shows up on the "Build with Parameters" screen. You can then read `params.X` in a
`when { expression { ... } }` block on a stage to make it conditional. One gotcha: Jenkins only
shows the parameters form *after* the pipeline has run once with the `parameters` block in place —
the first run after adding it won't prompt you.

## 6. Stretch: extract a Jenkins Shared Library

Move reusable pipeline logic (e.g. your test or notification steps) out into its own versioned
library that any Jenkinsfile can call into.

**Hints:** this needs a *second* git repository, with pipeline code under a `vars/` directory
following Jenkins' naming convention. You register it under **Manage Jenkins > System > Global
Pipeline Libraries**, then reference it from your Jenkinsfile with `@Library('your-lib-name') _`
at the top. This is the most involved option here — budget accordingly, and expect to need your
trainer's help wiring up the library in Jenkins.
