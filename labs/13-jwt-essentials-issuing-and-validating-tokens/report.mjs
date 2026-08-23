// KATA: two TODOs. Run this now, before changing anything:
//   node report.mjs
// It throws at TODO 1. That's the starting point.

import jwt from "jsonwebtoken";

const SECRET = "mission-control-shared-secret-key-32-bytes-minimum";

// TODO 1: implement issueToken - sign a JWT with jwt.sign, payload
// { sub: username, roles }, using SECRET, algorithm "HS256", and the
// given expiresIn value.
function issueToken(username, roles, expiresIn) {
  throw new Error("TODO 1: implement issueToken");
}

// TODO 2: implement validateToken - call jwt.verify(token, SECRET) and
// return its result. Let any error jwt.verify throws propagate up
// unchanged (don't catch it here) - the caller below handles that.
function validateToken(token) {
  throw new Error("TODO 2: implement validateToken");
}

console.log("--- A normal token, issued and validated ---");
const token = issueToken("dave", ["MISSION_OPERATOR"], "1h");
console.log(validateToken(token));

console.log("\n--- An already-expired token ---");
const expiredToken = issueToken("dave", ["MISSION_OPERATOR"], "-1s");
try {
  validateToken(expiredToken);
  console.log("This should never print");
} catch (err) {
  console.log(`${err.name}: ${err.message}`);
}

console.log("\n--- A tampered token ---");
const [header, payload, signature] = token.split(".");
const tamperedPayload = Buffer.from(
  JSON.stringify({ sub: "dave", roles: ["MISSION_OPERATOR", "ADMIN"] }),
).toString("base64url");
const tamperedToken = `${header}.${tamperedPayload}.${signature}`;
try {
  validateToken(tamperedToken);
  console.log("This should never print");
} catch (err) {
  console.log(`${err.name}: ${err.message}`);
}
