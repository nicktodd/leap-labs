// KATA: refactor Module 2's login-attempts.js into this module's style.
// Three TODOs. Run this now, before changing anything - it throws at
// TODO 1. That's the starting point.
//
// Reference Module 2's ORIGINAL, working script if you get stuck:
// labs/02-javascript-fundamentals-syntax-variables-functions-and-control-flow/login-attempts.js
// (do not copy its string-splitting approach - that's exactly what this
// refactor replaces)

import { morningAttempts, afternoonAttempts } from "./attempts-data.mjs";

// TODO 1: combine morningAttempts and afternoonAttempts into one array
// called allAttempts, using the spread operator (no loop, no .concat()).
const allAttempts = [...morningAttempts, ...afternoonAttempts];

// TODO 2: write describeOutcome as an ARROW FUNCTION that takes a single
// attempt object, destructures { username, outcome } in its parameter
// list, and returns "<username> logged in successfully" or
// "<username> failed to log in" using an if/else (not a ternary).
const describeOutcome = ({ username, outcome }) => {
  if (outcome === "success") {
    return `${username} logged in successfully`;
  } else {
    return `${username} failed to log in`;
  }
};

for (const attempt of allAttempts) {
  console.log(describeOutcome(attempt));
}

let successCount = 0;
let failCount = 0;
for (const { outcome } of allAttempts) {
  if (outcome === "success") {
    successCount++;
  } else {
    failCount++;
  }
}
console.log("");
console.log(`Summary: ${successCount} successful, ${failCount} failed`);

// TODO 3: write isLockedOut(attempts, username) - same consecutive-failure
// check as Module 2's while loop, but you can write it with whichever loop
// you prefer now that you understand what it needs to do. Then write
// checkLockouts(attempts, ...usernames) using a REST parameter, returning
// the array of usernames that are locked out, and call it below with
// "dave", "erin", and "frank".
const isLockedOut = (attempts, username) => {
  let consecutive = 0;
  for (const attempt of attempts) {
    if (attempt.username !== username) continue;
    if (attempt.outcome === "fail") {
      consecutive++;
      if (consecutive >= 2) return true;
    } else {
      consecutive = 0;
    }
  }
  return false;
};
const checkLockouts = (attempts, ...usernames) =>
  usernames.filter((username) => isLockedOut(attempts, username));

const lockedOut = checkLockouts(allAttempts, "dave", "erin", "frank");
console.log(
  lockedOut.length > 0
    ? `${lockedOut.join(", ")} had 2+ consecutive failures - would trigger a lockout in a real system`
    : "No lockouts"
);
