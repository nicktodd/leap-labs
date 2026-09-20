// Module 5's Attempt interface and functions, moved into their own file -
// a real project splits typed code across files exactly like Module 3
// split plain JavaScript across .mjs files.

export interface Attempt {
  username: string;
  outcome: string;
}

export function describeOutcome(outcome: string): string {
  return outcome === "success" ? "logged in successfully" : "failed to log in";
}

export function describeAttempt(attempt: Attempt): string {
  return `${attempt.username} ${describeOutcome(attempt.outcome)}`;
}
