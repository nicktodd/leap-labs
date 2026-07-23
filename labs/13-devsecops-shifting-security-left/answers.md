# Module 13 Lab — Answers

## Part A — Dependency Scanning

**Vulnerable dependency:** `commons-collections:commons-collections:3.2.1`

**CVE found:** CVE-2015-6420

**One-sentence summary:** commons-collections 3.2.1 allows remote code execution by an attacker
who can supply a malicious serialized Java object, because the library's `InvokerTransformer`
class can be chained to execute arbitrary code during Java deserialization.

**Fix applied:** Bumped to `3.2.2` in `pom.xml`, which adds a serialization filter that prevents
the vulnerable `InvokerTransformer` chain from executing during deserialization.

**Verification:** OSV query against `3.2.2` returns `{}` (no known vulnerabilities).

---

## Part B — Secret Detection (Throwaway Repo Exercise)

### Step 4 Written Answer

After committing the fix that moved the credentials to `System.getenv(...)`, the gitleaks full-
history scan (`detect -v`, not `--no-git`) still finds 2 leaks. This is because gitleaks scans
the entire git commit history, not just the current working tree — the secrets were present in
the initial commit and that commit still exists in the repository's object database.

The ONE action that actually neutralizes the exposure is **credential rotation**: the exposed
values (API keys, access tokens) must be invalidated and replaced with new ones in the
credential management system (e.g. AWS IAM, Stripe dashboard). Rewriting git history with
`git filter-branch` or `git filter-repo` removes the secret from future clones of the
repository, but it does not invalidate the secret itself — anyone who has already cloned the
repository (or accessed the git history through GitHub's API, a mirror, or a fork) still has
the original value. Only revoking the credential in the issuing system makes it useless.

### Step 5 Comparison

The working-tree-only scan (`--no-git`) finds 0 leaks after the fix, because the current
working-tree file now uses `System.getenv(...)` and contains no credential values. This
demonstrates the contrast: the code is clean, but the history is not. Fixing the code is
necessary (so new clones don't contain the secret) but not sufficient (the secret is still in
the history and must be rotated).
