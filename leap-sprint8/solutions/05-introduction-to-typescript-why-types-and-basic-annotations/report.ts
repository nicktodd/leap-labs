const username = "dave";
const attemptCount = 2;
const isLockedOut = false;

function describeOutcome(outcome: string): string {
  return outcome === "success" ? "logged in successfully" : "failed to log in";
}
console.log(describeOutcome("success"));

interface Attempt {
  username: string;
  outcome: string;
}

const attempt: Attempt = { username: "dave", outcome: "success" };
console.log(attempt);

function describeAttempt(attempt: Attempt): string {
  return `${attempt.username} ${describeOutcome(attempt.outcome)}`;
}
console.log(describeAttempt(attempt));
