// Primitive type annotations - a colon after the name, then the type.
const username: string = "alice";
const attemptCount: number = 3;
const isLockedOut: boolean = false;

// Typing a function: each parameter gets a type, and the return type
// comes after the parameter list.
function describeOutcome(outcome: string): string {
  if (outcome === "success") {
    return "logged in successfully";
  } else {
    return "failed to log in";
  }
}
console.log(describeOutcome("success"));

// An interface names a shape - the same "attempt object" from Module 3,
// but now with its shape written down and enforced.
interface Attempt {
  username: string;
  outcome: string;
}

const attempt: Attempt = { username: "alice", outcome: "success" };
console.log(attempt);

function describeAttempt(attempt: Attempt): string {
  return `${attempt.username} ${describeOutcome(attempt.outcome)}`;
}
console.log(describeAttempt(attempt));
