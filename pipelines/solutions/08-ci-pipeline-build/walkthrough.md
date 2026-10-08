# Module 08 Lab - Walkthrough (Instructor Reference)

## Part A: the Jenkinsfile

See [`Jenkinsfile`](Jenkinsfile) in this folder. Delegates should follow the full Foundations
week's Module 6 PR workflow to get it into `main`: branch, commit, push, PR, review, merge, not a direct push.

## Part B: Multibranch Pipeline job

1. Check the **GitHub Branch Source** and **GitHub** plugins are installed (Manage Jenkins >
   Plugins). The GitHub plugin provides the `/github-webhook/` endpoint and `githubPush()`.
2. Jenkins: **New Item > Multibranch Pipeline**, name it after the repository.
3. **Branch Sources > Add > GitHub**, point it at the repository, provide credentials with
   read access.
4. Save, Jenkins scans the repository and creates a sub-job per branch it finds, starting with
   `main`.

## Part C: webhook relay through smee.io

Jenkins runs locally in Docker, so GitHub can't reach `localhost` directly. smee.io relays it.

5. <https://smee.io> > **Start a new channel**, copy the channel URL.
6. On the Jenkins host, run
   `npx smee-client --url https://smee.io/<channel> --target http://localhost:8080/github-webhook/`
   and leave it running. It should print `Connected`.
7. On GitHub: **Settings > Webhooks > Add webhook**, payload URL = the smee.io channel URL,
   content type `application/json`, events: **Pushes** and **Pull requests**.
8. The `ping` delivery should show green under **Recent Deliveries**, appear in the smee.io
   browser tab, and appear as a `POST` in the smee-client terminal.

## Part D: prove the triggers

9. Open a PR from a feature branch: Jenkins should trigger a build for that PR within seconds
   of the webhook firing, visible under the job's **Pull Requests** tab.
10. Merge to `main`: a separate build triggers for the `main` sub-job.

### Common problems seen in class

- Payload URL set to `http://localhost:8080/...` in GitHub: GitHub can't reach it, deliveries
  go red. It must be the smee.io URL; only the smee-client `--target` uses localhost.
- `--target` missing the trailing `/github-webhook/`: Jenkins returns 404.
- Content type left as `application/x-www-form-urlencoded`: deliveries succeed but Jenkins
  doesn't act on them. Fix it, then **Redeliver** from Recent Deliveries.
- smee-client terminal closed: nothing reaches Jenkins, although GitHub still shows green
  deliveries to smee.io. Check the terminal first.
- Running smee-client in a container: target `host.docker.internal:8080`, not `localhost`.

## Part E: branch protection

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
- Delegates used the Foundations week's Module 6 PR workflow to add the Jenkinsfile, not a
  direct push to `main`,
  the whole point of the Foundations week's Git modules is that this shouldn't be a manual override.
- The Multibranch Pipeline job, not a plain Pipeline job, was used, this is the actual answer to
  "how do you trigger on a PR and on merge to main" and is easy to skip past if delegates reach
  for the job type they already know from Module 02.
- Both trigger events (PR opened, merge to main) were demonstrated live, not just configured
  and assumed to work, with green deliveries under the webhook's Recent Deliveries.
- If a team attempted the "finish early" break-the-test extension, confirm they saw the PR
  build actually go red, and that they understood why that's the correct, intended behaviour.
