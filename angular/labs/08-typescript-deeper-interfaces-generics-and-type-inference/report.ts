// KATA: three TODOs. Run this now, before changing anything:
//   npx tsc report.ts --strict --noEmit
// It fails with real compiler errors at TODO 2 (TS2315, Result isn't
// generic yet) and TODO 3 (TS7006, implicit any). TODO 1 does NOT cause
// an error yet, even though it's incomplete - an EMPTY interface accepts
// any object at all, so it provides zero type safety without erroring.
// That's worth noticing on its own before you fix it.

// TODO 1: define BaseRecord with a readonly id (number) and a createdAt
// (string). Then define LoginAttempt extending BaseRecord, with username
// (string), outcome (string), and an OPTIONAL notes (string).
interface BaseRecord {
}

interface LoginAttempt {
}

const attempt: LoginAttempt = {
  id: 1,
  createdAt: "2026-01-01T09:00:00Z",
  username: "dave",
  outcome: "success",
};
console.log(attempt);

// TODO 2: define a generic interface Result<T> with a boolean success, an
// optional value of type T, and an optional string error - same shape as
// the demo's Result<T>.
interface Result {
}

function verifyCredentials(username: string): Result<{ username: string }> {
  const knownUsers = ["dave", "erin", "frank"];
  if (knownUsers.includes(username)) {
    return { success: true, value: { username } };
  }
  return { success: false, error: `Unknown user: ${username}` };
}

const outcome = verifyCredentials("dave");
if (outcome.success) {
  console.log("Verified:", outcome.value?.username);
} else {
  console.log("Error:", outcome.error);
}

const failedOutcome = verifyCredentials("mallory");
if (failedOutcome.success) {
  console.log("Verified:", failedOutcome.value?.username);
} else {
  console.log("Error:", failedOutcome.error);
}

// TODO 3: write describeByUsername as a generic function, constrained so
// T must have at least a username: string field. Return
// `Record for ${record.username}`.
function describeByUsername(record) {
  throw new Error("TODO 3: implement describeByUsername");
}

console.log(describeByUsername({ username: "dave", outcome: "success" }));
console.log(describeByUsername({ username: "erin", verified: true }));
