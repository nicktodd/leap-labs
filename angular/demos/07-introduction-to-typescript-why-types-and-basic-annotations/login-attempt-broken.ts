// Deliberately broken - run `npx tsc login-attempt-broken.ts --strict` and
// read the two real compiler errors. Neither of these would be caught by
// Node at all - Module 3's "Objects vs Java Records" comparison said a
// typo'd key just becomes undefined at runtime in plain JavaScript. This
// is what TypeScript adds: the same mistake, caught before the code ever
// runs.

interface Attempt {
  username: string;
  outcome: string;
}

function describeOutcome(outcome: string): string {
  return outcome === "success" ? "logged in successfully" : "failed to log in";
}

// Mistake 1: typo'd property name (outcom instead of outcome).
const attempt: Attempt = { username: "alice", outcom: "success" };

// Mistake 2: passing a number where describeOutcome expects a string.
console.log(describeOutcome(200));
