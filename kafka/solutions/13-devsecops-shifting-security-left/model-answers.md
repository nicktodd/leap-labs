# Module 13 - Model Answers

## Part A - Dependency Scanning

**Vulnerable dependency found**: `commons-collections:commons-collections:3.2.1`

**CVE**: CVE-2015-6420 - Insecure Deserialization in Apache Commons Collections. Serialized-object
interfaces in Java applications using this library may allow a remote attacker to execute
arbitrary commands via a crafted serialized Java object. Severity: **HIGH**.

**Fix**: bumped to `3.2.2` in `pom.xml` (this folder). Verified via OSV:

```bash
curl -s -X POST \
  -d '{"version":"3.2.2","package":{"name":"commons-collections:commons-collections","ecosystem":"Maven"}}' \
  "https://api.osv.dev/v1/query"
```

Verified real result: `{}` - zero known vulnerabilities.

## Part B - Secret Detection

### Verified gitleaks output (before the fix, full-history scan)

```
Finding:     ...STRIPE_API_KEY = "stripe_key_placeholder..."
RuleID:      stripe-access-token

Finding:     ...AWS_SECRET_ACCESS_KEY = "aws_secret_placeholder..."
RuleID:      generic-api-key

leaks found: 2
```

### After fixing `PaymentGateway.java` (moving both values to `System.getenv(...)`) and
committing

```
leaks found: 2
```

**Still 2** - identical to before the fix, because gitleaks' default scan walks the FULL commit
history, and the original commit (with the real hardcoded values) still exists.

### After a working-tree-only scan (`--no-git`)

```
no leaks found
```

## Model answer to Part B, step 4

> The result tells you that fixing the code in the latest commit does NOT remove the secret from
> the repository - anyone who clones the repo, or runs `git log -p`, can still find the original
> hardcoded values in the earlier commit, forever, unless that history is explicitly rewritten.
> The one action that actually neutralizes the exposure is **rotating the credential at its
> source** - generating a new Stripe API key and new AWS secret access key, and revoking the old
> ones - because that makes the LEAKED VALUES useless regardless of who has seen them or how much
> of the repo's history they can access. Deleting the file, or even rewriting git history to
> remove the commit entirely, is good hygiene, but neither one un-leaks a value that may already
> have been cloned, cached, or scraped before the fix landed.

## Talking points

- This exercise deliberately used realistic-format FAKE values rather than vendor-published
  examples, because many scanners allowlist well-known documentation examples and would otherwise
  skip the exercise entirely.
- The contrast between "full history: 2 leaks" and "working tree only: 0 leaks" is the entire
  lesson of Part B in one pair of numbers - worth making sure both were actually run and compared
  side by side, not just the first one.
- CVE-2015-6420 is over a decade old - a genuinely realistic scenario for a project that pinned a
  dependency version years ago and never revisited it, exactly the kind of finding a CI-integrated
  dependency scan (rather than a one-off manual check) is designed to catch automatically, on
  every build, going forward.
