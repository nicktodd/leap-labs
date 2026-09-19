# Module 08 Lab — GitHub Essentials

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
   - On github.com, create a new, empty repository named `sprint1-<your-initials>-demo-app`
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
2. Set up `starter/` as a repo in a folder called `sprint1-demo-app`, connect it to the remote,
   and push.
3. Clone the same remote into a second folder, `sprint1-demo-app-clone` — this stands in for
   "your partner's machine."
4. Make a change in `sprint1-demo-app`, commit, and push.
5. In `sprint1-demo-app-clone`, pull and confirm you received the change.
6. Reverse it: make a change in the clone folder, push, then pull it into the original folder.

## Acceptance criteria

- The GitHub repository shows at least two commits when viewed in a browser.
- Both partners (or both local folders, for the solo variant) have identical `git log` output
  after the final pull.
- You can explain, in one sentence each, what `git remote add`, `git push`, `git clone`, and
  `git pull` each do.

If you finish early, explore the **Branches** view on github.com and compare it with `git
branch -a` locally — do they show the same information?

## Setting up GitHub credentials on Amazon Linux

If you're also working from an Amazon Linux EC2 instance (e.g. the shared training host from
[Module 03](../03-linux-fundamentals)), you'll need to authenticate to GitHub from there
separately — credentials set up on your Windows machine don't carry over. The recommended
approach is an SSH key pair, since it doesn't expire and works well on a headless host.

### 1. Set your Git identity

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 2. Generate an SSH key on the Amazon Linux host

```bash
ssh-keygen -t ed25519 -C "you@example.com"
```

Press Enter to accept the default file location (`~/.ssh/id_ed25519`) and set a passphrase if
you want one. Then start the SSH agent and add the key:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 3. Add the public key to GitHub

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the output, then on github.com go to **Settings > SSH and GPG keys > New SSH key**, paste
it in, and save.

### 4. Test the connection

```bash
ssh -T git@github.com
```

You should see a message confirming you've authenticated as your GitHub username.

### 5. Use SSH remote URLs

When adding a remote or cloning on the Amazon Linux host, use the SSH form of the URL rather
than HTTPS:

```bash
git remote add origin git@github.com:your-org/your-repo.git
```

If you already added an `https://` remote, switch it with:

```bash
git remote set-url origin git@github.com:your-org/your-repo.git
```

### Alternative: HTTPS with a personal access token

If SSH traffic is blocked on your network, use HTTPS instead. Generate a token at
**github.com > Settings > Developer settings > Personal access tokens**, then run:

```bash
git config --global credential.helper store
```

The next time you `git push` or `git pull` over HTTPS, enter your GitHub username and the token
as the password. `credential.helper store` caches it in `~/.git-credentials` so you won't be
asked again on that host.

### Repeat on Windows if needed

The same steps work in Git Bash on Windows — the commands are identical. If you already
authenticated to GitHub on Windows via the GitHub CLI, GitHub Desktop, or Git Credential
Manager, you don't need to redo this section there; it's only required for hosts that don't
already have working credentials.
