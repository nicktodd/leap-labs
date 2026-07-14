// This is Module 2's login-attempts.js, redone with what Module 3 adds:
// objects/arrays as the actual data (not comma-strings), destructuring,
// arrow functions, spread, rest, and ES module import/export splitting
// the code across two files.

import { morningAttempts, afternoonAttempts } from "./attempts-data.mjs";

// ARROW FUNCTION + OBJECT DESTRUCTURING in the parameter list itself.
const describeOutcome = ({ username, outcome }) =>
  outcome === "success"
    ? `${username} logged in successfully`
    : `${username} failed to log in`;

// SPREAD: combine two arrays into one, without a loop.
const allAttempts = [...morningAttempts, ...afternoonAttempts];

for (const attempt of allAttempts) {
  console.log(describeOutcome(attempt));
}

const summarize = (attempts) => {
  let successCount = 0;
  let failCount = 0;
  for (const { outcome } of attempts) {
    // ARRAY-ELEMENT DESTRUCTURING isn't needed here (this is object
    // destructuring on each element) - array destructuring is shown
    // separately below.
    if (outcome === "success") {
      successCount++;
    } else {
      failCount++;
    }
  }
  return { successCount, failCount };
};

// OBJECT DESTRUCTURING on a function's return value.
const { successCount, failCount } = summarize(allAttempts);
console.log(`\nSummary: ${successCount} successful, ${failCount} failed`);

const isLockedOut = (attempts, username) => {
  let consecutiveFails = 0;
  for (const attempt of attempts) {
    if (attempt.username !== username) continue;
    consecutiveFails = attempt.outcome === "fail" ? consecutiveFails + 1 : 0;
    if (consecutiveFails >= 2) return true;
  }
  return false;
};

// REST PARAMETER: check any number of usernames without an array argument.
const checkLockouts = (attempts, ...usernames) =>
  usernames.filter((username) => isLockedOut(attempts, username));

const lockedOut = checkLockouts(allAttempts, "alice", "bob", "carol");
console.log(
  lockedOut.length > 0
    ? `${lockedOut.join(", ")} had 2+ consecutive failures - would trigger a lockout in a real system`
    : "No lockouts"
);

// ARRAY DESTRUCTURING, shown on its own since nothing above needed it.
const [firstAttempt, secondAttempt] = allAttempts;
console.log(
  `\nFirst attempt: ${firstAttempt.username}, second attempt: ${secondAttempt.username}`
);
