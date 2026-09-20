// Companion script for the "Template Literals" and "map/filter" sections of the
// demo guide (Parts 4 and 5) - run separately from report.mjs since these aren't
// part of the main login-attempts refactor.

console.log("--- template literals ---");
const username = "alice";
const attemptCount = 3;
console.log(`${username} has made ${attemptCount} attempts`);

console.log("--- array .map (compare Java Stream.map) ---");
const attempts = [
  { username: "alice", outcome: "success" },
  { username: "bob", outcome: "fail" },
];
const usernames = attempts.map((a) => a.username);
console.log(usernames);

console.log("--- array .filter (compare Java Stream.filter) ---");
const failed = attempts.filter((a) => a.outcome === "fail");
console.log(failed);
