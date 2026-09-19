# Module 08 Lab — Worked Example (Instructor Reference)

## Partner A

```bash
cp -r starter sprint1-demo-app
cd sprint1-demo-app
git init
git add -A
git commit -m "Initial commit"

git remote add origin https://github.com/<org>/sprint1-ab-demo-app.git
git remote -v
git push -u origin main
```

## Partner B

```bash
git clone https://github.com/<org>/sprint1-ab-demo-app.git sprint1-demo-app-clone
cd sprint1-demo-app-clone
git log --oneline
```

## Partner A pushes a change

```bash
# edit src/Greeter.java, add a comment
git add src/Greeter.java
git commit -m "Add clarifying comment to greet method"
git push
```

## Partner B pulls it

```bash
git pull
git log --oneline
# Partner B's log should now show both commits
```

## Command reference answer key

- **`git remote add origin <url>`**: registers a remote repository under the local name
  `origin`, so future commands can refer to it by that name instead of the full URL.
- **`git push`**: uploads commits from your current local branch to the corresponding branch on
  the remote.
- **`git clone <url>`**: creates a new local folder, downloads the full history from the remote,
  and automatically configures `origin` and branch tracking.
- **`git pull`**: downloads new commits from the remote (`fetch`) and merges them into your
  current local branch, in one step.

## Common issue: push rejected

If Partner B pushes a change without pulling first, their `git push` will be rejected with
"Updates were rejected because the remote contains work that you do not have locally." The fix
is `git pull` first, then `git push` again. This is expected and worth demonstrating if a pair
hits it naturally, rather than trying to prevent it.
