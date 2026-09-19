# Module 07 Lab — Worked Example (Instructor Reference)

## Commands

```bash
cp -r starter sprint1-branching-lab
cd sprint1-branching-lab
git init
git add -A
git commit -m "Initial commit"

# Part A
git branch feature/formal-greeting
git switch feature/formal-greeting
# edit Greeter.java: return "Good day, " + name;
git add src/Greeter.java
git commit -m "Use a more formal greeting"

git switch main
git merge feature/formal-greeting
# fast-forward: main's pointer just moves, no merge commit is created
# because main had no new commits since the branch point

# Part B
git switch -c feature/casual-greeting main~1
# edit Greeter.java: return "Hey there, " + name;
git add src/Greeter.java
git commit -m "Use a casual greeting"

git switch main
git merge feature/casual-greeting
# CONFLICT (content): Merge conflict in src/Greeter.java
```

## Expected conflict markers

```java
public class Greeter {
    public String greet(String name) {
<<<<<<< HEAD
        return "Good day, " + name;
=======
        return "Hey there, " + name;
>>>>>>> feature/casual-greeting
    }
}
```

Resolve by picking one, combining, or asking the trainer to nominate a "team decision" (e.g.
keep the formal greeting since it merged first):

```java
public class Greeter {
    public String greet(String name) {
        return "Good day, " + name;
    }
}
```

```bash
git add src/Greeter.java
git commit
git log --oneline --graph --all
```

## Expected graph shape (hashes will differ)

```
*   e5f6a7b (HEAD -> main) Merge branch 'feature/casual-greeting'
|\
| * d4e5f6a (feature/casual-greeting) Use a casual greeting
* | c3d4e5f (feature/formal-greeting) Use a more formal greeting
|/
* b2c3d4e Initial commit
```

## Branching strategy answer key

**Trunk-based development**: everyone branches for a short time (hours to a couple of days),
merges back to `main` frequently, and `main` is always close to releasable. Suits small teams
with strong CI, frequent releases, and where long-lived divergence is a bigger risk than the
occasional conflict.

**Gitflow-style**: separate `develop`, `release`, and `hotfix` branches alongside `main`, with
longer-lived feature branches. Suits larger teams, scheduled/versioned releases, or products
that must support multiple released versions in parallel.

**Recommendation for a 6-8 person Scrum team releasing frequently**: trunk-based, or a very
light version of it (short feature branches merged via review, no separate `develop` branch).
The overhead of Gitflow's extra long-lived branches isn't justified at this team size and
release cadence, and it increases the chance of exactly the kind of conflict just practised,
just with much more code involved by the time you resolve it.
