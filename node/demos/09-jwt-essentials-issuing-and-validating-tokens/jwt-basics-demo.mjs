// The exact jwt.sign/jwt.verify calls Sprint 6's real auth-stub uses -
// same library, same algorithm, same secret variable name.

import jwt from "jsonwebtoken";

const SECRET = "mission-control-shared-secret-key-32-bytes-minimum";

console.log("--- 1. Issuing a token ---");
const token = jwt.sign(
  { sub: "alice", roles: ["MISSION_OPERATOR"] },
  SECRET,
  { algorithm: "HS256", expiresIn: "1h" },
);
console.log(token);

console.log("\n--- 2. A JWT has three dot-separated parts ---");
const [header, payload, signature] = token.split(".");
console.log("header (base64):", header);
console.log("decoded header:", Buffer.from(header, "base64url").toString());
console.log("payload (base64):", payload);
console.log("decoded payload:", Buffer.from(payload, "base64url").toString());
console.log("signature (base64):", signature);

console.log("\n--- 3. Verifying the token ---");
const decoded = jwt.verify(token, SECRET);
console.log(decoded);

console.log("\n--- 4. Tampering with the payload ---");
try {
  const tamperedPayload = Buffer.from(
    JSON.stringify({ sub: "alice", roles: ["MISSION_OPERATOR", "ADMIN"] }),
  ).toString("base64url");
  const tamperedToken = `${header}.${tamperedPayload}.${signature}`;
  jwt.verify(tamperedToken, SECRET);
  console.log("This should never print");
} catch (err) {
  console.log(`${err.name}: ${err.message}`);
}

console.log("\n--- 5. Verifying with the WRONG secret ---");
try {
  jwt.verify(token, "a-completely-different-secret");
  console.log("This should never print");
} catch (err) {
  console.log(`${err.name}: ${err.message}`);
}

console.log("\n--- 6. An already-expired token ---");
const expiredToken = jwt.sign({ sub: "alice" }, SECRET, {
  algorithm: "HS256",
  expiresIn: "-1s", // already expired the instant it's issued
});
try {
  jwt.verify(expiredToken, SECRET);
  console.log("This should never print");
} catch (err) {
  console.log(`${err.name}: ${err.message}`);
}
