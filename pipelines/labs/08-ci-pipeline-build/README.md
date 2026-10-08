# Module 08 Lab - Build a CI Pipeline from Scratch

## Recap: building on the Foundations week's Module 6, and this week's Modules 05 and 06

- **The Foundations week's Module 6**: PR workflow and branch protection, which can require a CI check to pass
- **Module 05**: pipeline stages conceptually, using a provided log you only had to read
- **Module 06**: a real multi-stage Dockerfile for the team skeleton

Today you write the Jenkinsfile from scratch, and wire up automatic triggering on a PR and on
merge to `main` using a **GitHub webhook**, the piece that makes the Foundations week's Module 6
branch protection meaningful in practice.

## Objectives

By the end of this lab you will have:

- Built a working Jenkins pipeline from scratch
- Triggered that pipeline automatically from GitHub, using a webhook, on a PR and on a merge to
  `main`
- Added a basic automated test step to the pipeline
- Committed the pipeline config to your team repository

## Setup

- The [`starter/`](starter) folder from this lab (this week's skeleton, with the multi-stage
  Dockerfile from Module 06 and a placeholder JUnit test, but **no Jenkinsfile**, you're
  writing that yourself)
- Your local Jenkins, running in Docker on `http://localhost:8080`, with rights to create a new
  job, and `Maven3` configured as a tool (exactly as in Module 02)
- A GitHub repository for this exercise, where you have **admin** rights (needed to add a
  webhook)
- Node.js (any current LTS version), which gives you the `npx` command used to run the webhook
  relay. Check with `node --version` and `npx --version`. If you can't install Node.js, see
  "Running the relay without Node.js" in the troubleshooting section.

### Why do we need a relay?

A **webhook** is GitHub calling Jenkins: the moment you push or open a PR, GitHub sends an HTTP
POST (the "payload") to a URL you give it. Your Jenkins runs on `localhost`, inside Docker on your
own laptop, so GitHub, out on the internet, has no way to reach it.

**smee.io** solves this. It gives you a public URL that GitHub can reach. A small program on your
laptop, `smee-client`, keeps a connection open to smee.io and forwards every payload it receives
on to your local Jenkins:

```text
GitHub  --POST-->  https://smee.io/<your-channel>  <--connection--  smee-client (your laptop)  --POST-->  http://localhost:8080/github-webhook/
```

smee.io is a development tool: fine for a lab, never for production. A production Jenkins is
normally reachable by GitHub directly (or through the organisation's own proxy), so no relay is
needed there.

## Task sheet

### Part A - Write the Jenkinsfile

1. Copy `starter/` into a repository and push it.
2. Write a `Jenkinsfile` at the repository root with three stages:
   - **Checkout**: `checkout scm`
   - **Build Image**: `docker build -t team-skeleton:${BUILD_NUMBER} .`
   - **Test**: `mvn -B test`, publishing results with the `junit` step (same pattern as
     Module 02, including the `tools { maven 'Maven3' }` block)

   Also add a `triggers` block containing `githubPush()`. This is the Jenkinsfile equivalent of
   ticking **GitHub hook trigger for GITScm polling** on a job's configuration page: it tells
   Jenkins to act on a push notification from GitHub, rather than waiting for someone to click
   **Build Now**.

   ```groovy
   triggers {
       githubPush()
   }
   ```

3. Commit and push the `Jenkinsfile` using the full PR workflow from the Foundations week's
   Module 6: branch, commit, push, open a PR, get it reviewed, merge.

**Check:** the `Jenkinsfile` is on `main` in GitHub, with three stages and a `triggers` block.

### Part B - Create the Multibranch Pipeline job

4. In Jenkins, check the plugins you need are installed: **Manage Jenkins > Plugins >
   Installed plugins**, search for **GitHub Branch Source** and **GitHub** (the second one
   provides the `/github-webhook/` endpoint and `githubPush()`). Install them from
   **Available plugins** if either is missing, then restart Jenkins.
5. Create a **Multibranch Pipeline** job pointing at your repository (not a plain Pipeline job,
   that only builds one branch): **New Item > Multibranch Pipeline**, then **Branch Sources >
   Add source > GitHub**, add credentials with read access to the repository, and paste the
   repository's HTTPS URL. Save.
6. Confirm Jenkins scans the repository, discovers `main`, and creates a sub-job for it.

**Check:** the job page lists `main` as a branch, and its first build has run (it doesn't matter
yet whether it's green).

### Part C - Set up the webhook relay with smee.io

7. Open <https://smee.io> in a browser and click **Start a new channel**. Copy the URL shown at
   the top of the page (it looks like `https://smee.io/AbC123xYz`). Keep this browser tab open,
   it shows every payload that arrives, which is very useful later.
8. In a terminal on the same machine as Jenkins, start the relay, replacing the URL with your
   own channel's URL:

   ```bash
   npx smee-client --url https://smee.io/AbC123xYz --target http://localhost:8080/github-webhook/
   ```

   The first time, `npx` asks to download `smee-client`, answer `y`. Leave this terminal
   running for the rest of the lab: if you close it, webhooks stop reaching Jenkins.

   **Check:** the terminal prints `Forwarding https://smee.io/AbC123xYz to
   http://localhost:8080/github-webhook/` and `Connected https://smee.io/AbC123xYz`.

9. In your GitHub repository: **Settings > Webhooks > Add webhook**, and fill in:
   - **Payload URL**: your smee.io channel URL (`https://smee.io/AbC123xYz`), **not**
     `localhost`
   - **Content type**: `application/json`
   - **Secret**: leave blank for this lab
   - **Which events would you like to trigger this webhook?**: choose **Let me select
     individual events**, and tick **Pushes** and **Pull requests**
   - **Active**: ticked

   Click **Add webhook**.

   **Check:** GitHub immediately sends a test `ping` event. Within a few seconds you should see
   it in three places: the smee.io browser tab, a `POST` line in the smee-client terminal, and
   a green tick next to the delivery under the webhook's **Recent Deliveries** tab in GitHub.

### Part D - Prove it triggers automatically

10. Create a new branch, make a small change, push it, and open a PR.
11. Confirm Jenkins automatically discovers the PR and builds it, without you clicking Build
    Now. With a webhook this should start within a few seconds, not minutes.

    **Check:** a new entry appears under the job's **Pull Requests** tab (for example `PR-1`)
    with a build running, and the PR page in GitHub shows the Jenkins status check.

12. Merge the PR to `main`.
13. Confirm Jenkins automatically triggers a separate build for `main` itself.

    **Check:** the `main` sub-job has a new build, and the smee-client terminal shows the
    `push` delivery that caused it.

### Part E - Close the loop with branch protection

14. If you have admin rights, configure branch protection on `main` to require this pipeline's
    check to pass before merging (as discussed conceptually in the Foundations week's Module 6).
15. If you don't have admin rights, write two or three sentences describing exactly what you'd
    configure, referencing the actual job name Jenkins is reporting as a status check.

### Part F - Tidy up

16. When you've finished, stop the smee-client terminal with **Ctrl+C**. Either delete the
    webhook in GitHub, or leave it in place and simply restart the same `npx smee-client`
    command (same channel URL) next time you want automatic builds. GitHub will show failed
    deliveries while the relay isn't running, which is harmless.

## Troubleshooting

Work through these in order: each one tells you how far the payload got.

| Symptom | Likely cause and fix |
|---|---|
| GitHub's **Recent Deliveries** shows a red warning icon | GitHub couldn't deliver to smee.io. Check the **Payload URL** is your smee.io channel URL, exactly as copied, starting `https://`. |
| Delivery is green in GitHub and appears in the smee.io tab, but nothing in the smee-client terminal | smee-client isn't running, or it's connected to a different channel. Check the `--url` matches the channel URL character for character, and that the terminal still says `Connected`. |
| smee-client shows the `POST` but with an error, such as `ECONNREFUSED` | Jenkins isn't reachable on the `--target` address. Check `http://localhost:8080` opens in your browser, and that the Jenkins container was started with `-p 8080:8080`. |
| smee-client shows a `404` from Jenkins | The target path is wrong, or the GitHub plugin isn't installed. The `--target` must end in `/github-webhook/`, including the trailing slash. |
| Jenkins receives the payload but ignores it | Check the webhook **Content type** is `application/json`, not `application/x-www-form-urlencoded`. Edit the webhook, change it, then use **Recent Deliveries > Redeliver** to send the last event again. |
| A PR builds, but merging to `main` doesn't | Check **Pushes** is ticked in the webhook's events, not just **Pull requests**. |
| Nothing at all in **Recent Deliveries** after a push | The webhook may be inactive, or you pushed to a different repository. Check **Active** is ticked. |

Useful habits:

- In GitHub, **Settings > Webhooks > (your webhook) > Recent Deliveries** shows every payload,
  the response code Jenkins (via smee) returned, and a **Redeliver** button, so you can retry
  without making another commit.
- In Jenkins, the Multibranch Pipeline job's **Scan Repository Log** shows what Jenkins did with
  each event it received.

### Running the relay without Node.js

If you can't install Node.js, run the same relay inside a container. From inside a container,
`localhost` means the container itself, so target Jenkins through `host.docker.internal`
instead:

```bash
docker run --rm -it node:22-alpine npx -y smee-client --url https://smee.io/AbC123xYz --target http://host.docker.internal:8080/github-webhook/
```

## Acceptance criteria

- A `Jenkinsfile` exists in your repository with Checkout, Build Image, and Test stages, and a
  `githubPush()` trigger.
- A Multibranch Pipeline job in Jenkins has discovered your repository's branches and PRs.
- A GitHub webhook, relayed through smee.io, shows successful deliveries under **Recent
  Deliveries**.
- You've demonstrated an automatic build triggered by opening a PR, and a separate automatic
  build triggered by a merge to `main`, without manually clicking Build Now for either.
- You can explain what branch protection rule would make this pipeline's result required before
  merging.

If you finish early, break the placeholder test deliberately (make it assert false), push, and
watch the PR's automatic build go red, this is the Foundations week's Module 6's "failing
pipeline protects main" made real, on a pipeline you wrote yourself.
