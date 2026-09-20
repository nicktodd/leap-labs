const rawAttempts = [
  "dave,success",
  "erin,fail",
  "dave,fail",
  "dave,fail",
  "frank,success",
  "erin,success",
];

function parseAttempt(rawLine) {
  const parts = rawLine.split(",");
  const username = parts[0];
  const outcome = parts[1];
  return { username: username, outcome: outcome };
}

const describeOutcome = function (outcome) {
  if (outcome === "success") {
    return "logged in successfully";
  } else {
    return "failed to log in";
  }
};

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
