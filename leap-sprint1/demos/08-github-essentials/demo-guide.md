# Demo: Module 08 — GitHub Essentials

**Duration:** 10 minutes
**Prerequisite:** GitHub account with access to the LEAP organisation, a local repo with at
least one commit (use the `starter/` project), Git 2.49.

## Part 1: Navigating the GitHub UI (2 min)

Open github.com and walk through, without creating anything yet:

- The **Code** tab: file browser for the current branch
- The **Commits** view: history, same information as `git log`, in a browser
- The **Branches** view: every branch that exists on the remote
- Repository **Settings > Collaborators**: who else has access

Narration: everything here is a web view onto the exact same data your local `.git` folder
has. GitHub doesn't store anything Git doesn't already understand.

## Part 2: Creating a remote and pushing (3 min)

On github.com: **New repository**, name it `sprint1-demo-app`, leave it empty (no README, no
`.gitignore` from GitHub, we already have our own).

```bash
git remote add origin https://github.com/<org>/sprint1-demo-app.git
git remote -v
git push -u origin main
```

Narration: `git remote add` just tells your local repo "there's another copy of this history
over there, and let's call it `origin`." `-u` on the first push sets up tracking, so future
`git push`/`git pull` know which remote branch to talk to without extra arguments. Refresh the
GitHub page: the commits are now visible in the browser.

## Part 3: Cloning as a second person (3 min)

In a *different* folder (simulating a teammate's machine):

```bash
git clone https://github.com/<org>/sprint1-demo-app.git sprint1-demo-app-clone
cd sprint1-demo-app-clone
git log --oneline
```

Narration: `clone` does three things in one command: creates a local folder, downloads the full
history, and automatically sets up `origin` for you. This is how every teammate gets started.

## Part 4: Push from one side, pull from the other (2 min)

Back in the original folder, make a change and push it:

```bash
echo "// TODO: add farewell method" >> src/Greeter.java
git add src/Greeter.java
git commit -m "Add TODO for farewell method"
git push
```

In the clone folder:

```bash
git pull
git log --oneline
```

Narration: `pull` is really `fetch` (download what's new) plus `merge` (bring it into your
current branch) in one step. This is exactly how you'll receive a partner's work in the lab.

## Key message

`origin` is just a name for "the GitHub copy." `push` sends your commits there, `pull` brings
theirs to you, `clone` does both for the first time in one step. Everything else about
collaborating through GitHub builds on these three commands — Pull Requests come in a later
sprint, but the underlying data flow is exactly this.
