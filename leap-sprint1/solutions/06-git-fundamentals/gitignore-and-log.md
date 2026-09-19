# Module 06 Lab — Reference Answers

Instructor reference only.

## Commands

```bash
cp -r starter sprint1-git-lab
cd sprint1-git-lab
git init
git status                       # README.md, src/, target/, .idea/ all untracked

git add README.md src/Greeter.java
git commit -m "Add initial README and Greeter class"

git status                       # target/ and .idea/ still show as untracked
```

## Expected .gitignore

```
target/
.idea/
```

```bash
git add .gitignore
git commit -m "Add .gitignore for build output and IDE files"
git status                       # clean, target/ and .idea/ no longer listed

# Edit Greeter.java to add a farewell() method
git diff                         # shows the added method, line by line
git add src/Greeter.java
git commit -m "Add farewell method to Greeter"

git log --oneline
```

## Expected `git log --oneline` (order and hashes will differ)

```
c3d4e5f Add farewell method to Greeter
b2c3d4e Add .gitignore for build output and IDE files
a1b2c3d Add initial README and Greeter class
```

## Answer key: untracked vs staged vs committed

- **Untracked**: Git sees the file exists but is not yet following its changes at all.
- **Staged**: the file's current content has been marked to go into the *next* commit, via
  `git add`.
- **Committed**: the staged content has been permanently recorded in the repository's history.
