// Module 2 Demo — plain JavaScript, nothing else. No frameworks, no npm
// packages, no objects/arrays-of-objects yet (that's Module 3). Just
// variables, functions, and control flow, applied to something real: a
// short log of login attempts against this sprint's mission.

// VARIABLES: `const` for values that never get reassigned, `let` for ones
// that do. Prefer `const` by default — reassignment is worth signalling
// explicitly, not the norm.
const rawAttempts = [
  "alice,success",
  "bob,fail",
  "alice,success",
  "carol,fail",
  "bob,fail",
  "alice,fail",
];

// A FUNCTION DECLARATION. Named, hoisted (usable before its own definition
// appears in the file — try moving the call above this and see it still
// works), and the standard way to define a reusable piece of behaviour.
function parseAttempt(rawLine) {
  // .split(",") is a String method - it returns an ARRAY. Arrays get their
  // own full module (Module 3); today, just enough to pull two values out
  // of one.
  const parts = rawLine.split(",");
  const username = parts[0];
  const outcome = parts[1];
  return { username: username, outcome: outcome };
  // (Yes, this returns an object - a preview of Module 3. Today's task
  // doesn't require understanding object internals, just that a function
  // can return more than one value bundled together.)
}

// A FUNCTION EXPRESSION: a function assigned to a variable, rather than
// declared with the `function name() {}` form above. Functionally similar
// for this simple case - the real difference (hoisting) matters more once
// functions start calling each other out of definition order.
const describeOutcome = function (outcome) {
  // CONTROL FLOW: if/else. Every branch returns a String.
  if (outcome === "success") {
    return "logged in successfully";
  } else {
    return "failed to log in";
  }
};

// CONTROL FLOW: a `for` loop with an index, and a running count using `let`
// (this one genuinely needs to be reassigned every iteration).
let successCount = 0;
let failCount = 0;

for (let i = 0; i < rawAttempts.length; i++) {
  const attempt = parseAttempt(rawAttempts[i]);
  console.log(attempt.username + " " + describeOutcome(attempt.outcome));

  if (attempt.outcome === "success") {
    successCount = successCount + 1;
  } else {
    failCount = failCount + 1;
  }
}

console.log("");
console.log("Summary: " + successCount + " successful, " + failCount + " failed");

// CONTROL FLOW: `while`, checking a real security-relevant condition - has
// any single user failed 3+ times in a row? A `for` loop works fine here
// too; `while` is shown because the loop's end condition ("found a repeat
// offender, or ran out of attempts") isn't naturally expressed as "count
// from 0 to N".
let index = 0;
let consecutiveFails = 0;
let lockedOutUser = null;

while (index < rawAttempts.length && lockedOutUser === null) {
  const attempt = parseAttempt(rawAttempts[index]);
  if (attempt.outcome === "fail") {
    consecutiveFails = consecutiveFails + 1;
  } else {
    consecutiveFails = 0;
  }
  if (consecutiveFails >= 2) {
    lockedOutUser = attempt.username;
  }
  index = index + 1;
}

if (lockedOutUser !== null) {
  console.log(lockedOutUser + " had 2+ consecutive failures - would trigger a lockout in a real system");
} else {
  console.log("No user hit the consecutive-failure threshold");
}
