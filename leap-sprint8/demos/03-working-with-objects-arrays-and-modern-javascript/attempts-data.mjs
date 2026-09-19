// Login attempts as OBJECTS from the start - no more comma-separated
// strings to manually split. Two small arrays, so the demo also has a
// real reason to use the spread operator later (combining them).

export const morningAttempts = [
  { username: "alice", outcome: "success" },
  { username: "bob", outcome: "fail" },
  { username: "alice", outcome: "success" },
];

export const afternoonAttempts = [
  { username: "carol", outcome: "fail" },
  { username: "bob", outcome: "fail" },
  { username: "alice", outcome: "fail" },
];
