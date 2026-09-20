# Module 05 Lab - GitHub Essentials

## Objectives

By the end of this lab you will have:

- Connected a local repository to a remote on GitHub
- Pushed local commits to that remote
- Pulled a partner's changes from the same remote
- Navigated the GitHub UI to check what you pushed

## Setup

- GitHub account with access to the LEAP organisation
- Git 2.49
- The [`starter/`](starter) folder from this lab, copied to a working location of your choice
- Work in pairs. If you don't have a partner available, follow the **solo variant** at the
  bottom of this page instead.

## Task sheet (pair version)

One of you is **Partner A**, the other is **Partner B**. Decide now.

1. **Partner A: create the remote**
   - On github.com, create a new, empty repository named `foundations-<your-initials>-demo-app`
     (no README or `.gitignore` from GitHub, you're bringing your own).
   - Add Partner B as a collaborator (Settings > Collaborators).

2. **Partner A: connect and push**
   - Copy `starter/` to a working location, initialise it as a Git repository, and commit all
     the starter files.
   - Add the GitHub repository as a remote called `origin`.
   - Push your `main` branch, setting up tracking.
   - Refresh the repository page on github.com and confirm your commit is visible.

3. **Partner B: clone**
   - Clone Partner A's repository to your own machine.
   - Run `git log --oneline` and confirm you can see Partner A's commit.

4. **Partner A: push a change**
   - Make a small change to `src/Greeter.java` (e.g. add a comment).
   - Commit and push it.

5. **Partner B: pull the change**
   - Pull the latest changes into your clone.
   - Confirm the change is now present in your copy of `Greeter.java`.

6. **Swap roles**
   - Partner B makes a change and pushes it.
   - Partner A pulls it and confirms.

## Solo variant (no partner available)

Simulate two people using two local folders:

1. Create a GitHub repository as in step 1 (no collaborator needed).
2. Set up `starter/` as a repo in a folder called `foundations-demo-app`, connect it to the remote,
   and push.
3. Clone the same remote into a second folder, `foundations-demo-app-clone` - this stands in for
   "your partner's machine."
4. Make a change in `foundations-demo-app`, commit, and push.
5. In `foundations-demo-app-clone`, pull and confirm you received the change.
6. Reverse it: make a change in the clone folder, push, then pull it into the original folder.

## Acceptance criteria

- The GitHub repository shows at least two commits when viewed in a browser.
- Both partners (or both local folders, for the solo variant) have identical `git log` output
  after the final pull.
- You can explain, in one sentence each, what `git remote add`, `git push`, `git clone`, and
  `git pull` each do.

If you finish early, explore the **Branches** view on github.com and compare it with `git
branch -a` locally - do they show the same information?
