import { morningAttempts, afternoonAttempts } from "./attempts-data.mjs";

const allAttempts = [...morningAttempts, ...afternoonAttempts];

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

const isLockedOut = (attempts, username) => {
  let consecutiveFails = 0;
  for (const attempt of attempts) {
    if (attempt.username !== username) continue;
    consecutiveFails = attempt.outcome === "fail" ? consecutiveFails + 1 : 0;
    if (consecutiveFails >= 2) return true;
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
