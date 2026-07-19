// Two versions of the SAME log line - one leaks, one doesn't.

console.log("--- 1. The pitfall: logging the whole request body ---");
const loginAttempt = { username: "alice", password: "mission123" };
console.log("login attempt:", loginAttempt);

console.log("\n--- 2. The fix: log the event and username only ---");
function logAuthEvent(event, username) {
  console.log(`[auth] ${event} username=${username}`);
}
logAuthEvent("login_attempt", loginAttempt.username);

console.log("\n--- 3. The other half of 'weak secrets': a hardcoded fallback ---");
const JWT_SECRET = process.env.JWT_SECRET || "mission-control-shared-secret-key-32-bytes-minimum";
console.log("JWT_SECRET in use:               ", JWT_SECRET);
console.log("Was JWT_SECRET set via env var?  ", process.env.JWT_SECRET !== undefined);
