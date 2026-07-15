// Module 5 covered the basics of an interface: name a shape, tsc enforces
// it. This file covers what a real project actually needs beyond that.

// EXTENDING an interface - Attempt gets everything BaseRecord has, plus
// its own fields.
interface BaseRecord {
  readonly id: number;
  createdAt: string;
}

interface Attempt extends BaseRecord {
  username: string;
  outcome: string;
  notes?: string; // OPTIONAL - the ? means this key can be omitted entirely
}

const attempt: Attempt = {
  id: 1,
  createdAt: "2026-01-01T09:00:00Z",
  username: "alice",
  outcome: "success",
  // notes omitted - fine, it's optional
};
console.log(attempt);

// readonly enforced: uncomment to see a real compile error.
// attempt.id = 2; // error TS2540: Cannot assign to 'id' because it is a read-only property.

// A METHOD SIGNATURE inside an interface - not just data, but a shape
// that includes behaviour.
interface Verifier {
  verify(username: string): boolean;
}

const knownUsersVerifier: Verifier = {
  verify(username: string): boolean {
    return ["alice", "bob", "carol"].includes(username);
  },
};
console.log(knownUsersVerifier.verify("alice"));
console.log(knownUsersVerifier.verify("mallory"));
