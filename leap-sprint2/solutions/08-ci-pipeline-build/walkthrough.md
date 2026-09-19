# Module 08 Lab — Walkthrough (Instructor Reference)

## Part A: the Jenkinsfile

See [`Jenkinsfile`](Jenkinsfile) in this folder. Delegates should follow the full Module 03 PR
workflow to get it into `main`: branch, commit, push, PR, review, merge, not a direct push.

## Part B-C: Multibranch Pipeline and triggers

1. Jenkins: **New Item > Multibranch Pipeline**, name it after the repository.
2. **Branch Sources > Add > GitHub**, point it at the repository, provide credentials with
   read access.
3. Save, Jenkins scans the repository and creates a sub-job per branch it finds, starting with
   `main`.
4. On GitHub: **Settings > Webhooks > Add webhook**, payload URL
   `http://<jenkins-host>/github-webhook/`, content type `application/json`, events: at least
   "Pull requests" and "Pushes."
5. Open a PR from a feature branch: Jenkins should trigger a build for that PR within seconds
   of the webhook firing, visible as a new sub-job under the Multibranch Pipeline item.
6. Merge to `main`: a separate build triggers for the `main` sub-job.

## Part D: branch protection

```text
Settings > Branches > Add branch protection rule
Branch name pattern: main
[x] Require a pull request before merging
[x] Require status checks to pass before merging
    -> select the Jenkins check (reported name matches the Multibranch Pipeline job)
```

## What to check as an instructor

- The Jenkinsfile genuinely has three stages in the right order, and the Test stage publishes
  JUnit results rather than just running `mvn test` silently.
- Delegates used the Module 03 PR workflow to add the Jenkinsfile, not a direct push to `main`,
  the whole point of this sprint's Git modules is that this shouldn't be a manual override.
- The Multibranch Pipeline job, not a plain Pipeline job, was used, this is the actual answer to
  "how do you trigger on a PR and on merge to main" and is easy to skip past if delegates reach
  for the job type they already know from Sprint 1 Module 10.
- Both trigger events (PR opened, merge to main) were demonstrated live, not just configured
  and assumed to work.
- If a team attempted the "finish early" break-the-test extension, confirm they saw the PR
  build actually go red, and that they understood why that's the correct, intended behaviour.
