// KATA: this file has three TODOs. Each one is currently a function that
// throws — run it now, before changing anything, and see it fail loudly at
// the first TODO it reaches. That's the starting point, not a bug.

const rawAttempts = [
  "dave,success",
  "erin,fail",
  "dave,fail",
  "dave,fail",
  "frank,success",
  "erin,success",
];

// TODO 1: split rawLine on "," and return an object with `username` and
// `outcome` properties, matching the two parts of the string.
// Example: parseAttempt("dave,success") should behave like
//          { username: "dave", outcome: "success" }
function parseAttempt(rawLine) {
  throw new Error("TODO 1: implement parseAttempt");
}

// TODO 2: return "logged in successfully" if outcome === "success",
// otherwise return "failed to log in". Use if/else, not a shortcut.
const describeOutcome = function (outcome) {
  throw new Error("TODO 2: implement describeOutcome");
};

// TODO 3: using a `for` loop over rawAttempts (by index), call
// parseAttempt and describeOutcome for each entry, print a line for each
// (matching the demo's format: "<username> <description>"), and count
// successes into successCount and failures into failCount.
let successCount = 0;
let failCount = 0;

// (your for loop here)

console.log("");
console.log("Summary: " + successCount + " successful, " + failCount + " failed");

// Given, unchanged - the consecutive-failure lockout check from the demo,
// applied to this module's dataset. Notice what it reports once you've
// completed TODOs 1-3 and can run this section for real.
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
