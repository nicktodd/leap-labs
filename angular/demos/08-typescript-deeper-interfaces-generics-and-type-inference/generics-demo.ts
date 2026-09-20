// A GENERIC is a type that's parameterised by another type, written in
// angle brackets - the same <T> shape Java has used since generics
// arrived in Java 5.

// A generic function: T stands in for "whatever type the caller
// actually passes an array of."
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const firstUsername = first(["alice", "bob", "carol"]); // T inferred as string
console.log(firstUsername);

const firstCount = first([3, 1, 4]); // T inferred as number
console.log(firstCount);

// A generic INTERFACE: Result<T> can wrap a success value of ANY type T,
// without writing a separate Result type for every kind of value.
interface Result<T> {
  success: boolean;
  value?: T;
  error?: string;
}

function verifyCredentials(username: string): Result<{ username: string }> {
  const knownUsers = ["alice", "bob", "carol"];
  if (knownUsers.includes(username)) {
    return { success: true, value: { username } };
  }
  return { success: false, error: `Unknown user: ${username}` };
}

const outcome = verifyCredentials("alice");
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

// A CONSTRAINED generic: T extends { username: string } means T can be
// ANY shape, as long as it has at least a username field.
function describeByUsername<T extends { username: string }>(record: T): string {
  return `Record for ${record.username}`;
}

console.log(describeByUsername({ username: "alice", outcome: "success" }));
console.log(describeByUsername({ username: "bob", verified: true }));
