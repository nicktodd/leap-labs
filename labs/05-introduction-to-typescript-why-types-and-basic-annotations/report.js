"use strict";
// KATA: three TODOs. Run this now, before changing anything:
//   npx tsc report.ts --strict --noEmit
// It fails with real compiler errors (TS7006, "implicitly has an 'any'
// type") at TODO 1 and TODO 3. That's the starting point - work through
// the TODOs in order, rerunning after each one, until tsc reports zero
// errors.
const username = "dave";
const attemptCount = 2;
const isLockedOut = false;
// TODO 1: add a type annotation to the outcome parameter (string) and
// the function's return type (string).
function describeOutcome(outcome) {
    return outcome === "success" ? "logged in successfully" : "failed to log in";
}
console.log(describeOutcome("success"));
const attempt = { username: "dave", outcome: "success" };
console.log(attempt);
// TODO 3: add a type annotation to the attempt parameter (Attempt) and
// the function's return type (string).
function describeAttempt(attempt) {
    return `${attempt.username} ${describeOutcome(attempt.outcome)}`;
}
console.log(describeAttempt(attempt));
