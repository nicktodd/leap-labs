# Module 3 - Model Answers

`login-attempts.js` in this folder is the completed, verified implementation.

## Verified output

```
dave logged in successfully
erin failed to log in
dave failed to log in
dave failed to log in
frank logged in successfully
erin logged in successfully

Summary: 3 successful, 3 failed
dave had 2+ consecutive failures - would trigger a lockout in a real system
```

## TODO 1 - `parseAttempt`

```javascript
function parseAttempt(rawLine) {
  const parts = rawLine.split(",");
  const username = parts[0];
  const outcome = parts[1];
  return { username: username, outcome: outcome };
}
```

`"dave,success".split(",")` returns `["dave", "success"]` - an array of two strings, indexed
`[0]` and `[1]`.

## TODO 2 - `describeOutcome`

```javascript
const describeOutcome = function (outcome) {
  if (outcome === "success") {
    return "logged in successfully";
  } else {
    return "failed to log in";
  }
};
```

## TODO 3 - the `for` loop

```javascript
for (let i = 0; i < rawAttempts.length; i++) {
  const attempt = parseAttempt(rawAttempts[i]);
  console.log(attempt.username + " " + describeOutcome(attempt.outcome));

  if (attempt.outcome === "success") {
    successCount = successCount + 1;
  } else {
    failCount = failCount + 1;
  }
}
```

## The lockout question, answered

**`dave` gets named - but the sequence that triggered it was `erin`-fail (index 1) followed by
`dave`-fail (index 2).** The lockout check counts consecutive fails ACROSS THE WHOLE LIST,
without tracking which user each fail belongs to. Two different users failing back-to-back is
enough to trip it, and whichever user's attempt happened to be the second one gets blamed -
even though `dave` himself hadn't failed twice in a row at that point (his own second
consecutive fail came right after, at index 3, and by then the loop had already stopped).

**Is this a bug?** Genuinely defensible either way:
- **Bug**: a real account-lockout mechanism should almost certainly track failures PER USER, not
  globally - locking out `dave` based partly on `erin`'s failure is a real correctness problem in
  a security-relevant feature.
- **Deliberately simple first version**: as a rough "is something suspicious happening right
  now" signal (not a per-account lockout decision), a global consecutive-failure counter isn't
  unreasonable - some real systems do use exactly this kind of coarse global signal as a first
  line of detection, with per-account logic layered on top later.

Either answer is acceptable if argued specifically - the point of the question is noticing the
behaviour and reasoning about it, not landing on one "correct" verdict. This is deliberately left
unfixed through Module 4's refactor (which changes *how* the data is represented, not the
lockout logic itself) - a genuine example of a code smell being visible long before anyone
decides it's worth the cost to fix it.

## Talking points

- `parts[0]` / `parts[1]` is deliberately verbose - Module 4 introduces array destructuring
  (`const [username, outcome] = rawLine.split(",")`), which does the same thing more concisely.
  Seeing the manual-index version first makes the destructured version's benefit obvious rather
  than magic.
- `attempt.username` - dot notation to read an object property - is used here without being
  formally taught yet, exactly as the demo guide flagged. Learners don't need to understand
  object internals to use it correctly in this lab.
