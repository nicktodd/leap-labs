// Module 5 covered basic inference: let username = "alice" infers string.
// This file covers the two inference behaviours that matter once
// generics are involved.

// RETURN TYPE INFERENCE: describeOutcome's return type is never written,
// but tsc infers it as string from the function body - hover over the
// function name in VS Code to see it.
function describeOutcome(outcome: string) {
  return outcome === "success" ? "logged in successfully" : "failed to log in";
}
// Proof it's really inferred as string, not any: this would be a real
// compile error if uncommented, because describeOutcome() returns string,
// not number.
// const wrong: number = describeOutcome("success");

console.log(describeOutcome("success"));

// GENERIC TYPE ARGUMENT INFERENCE: first<T> from generics-demo.ts never
// needs <string> written explicitly - tsc infers T from the ARGUMENT.
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const inferred = first(["alice", "bob"]); // T inferred as string - no <string> needed
const explicit = first<string>(["alice", "bob"]); // same result, spelled out
console.log(inferred, explicit);

// Sometimes tsc CAN'T infer anything USEFUL - an empty array gives it no
// element to look at, so T silently falls back to unknown. Not a compile
// error, just a much less useful type - explicit <string> here fixes it.
const empty = first<string>([]);
console.log(empty);
