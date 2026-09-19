import jwt from "jsonwebtoken";

const SECRET = "mission-control-shared-secret-key-32-bytes-minimum";

function issueToken(username, roles, expiresIn) {
  return jwt.sign({ sub: username, roles }, SECRET, {
    algorithm: "HS256",
    expiresIn,
  });
}

function validateToken(token) {
  return jwt.verify(token, SECRET);
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
