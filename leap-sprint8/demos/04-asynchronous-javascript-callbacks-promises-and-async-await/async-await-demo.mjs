import { verifyCredentials } from "./verify-credentials.mjs";

async function checkLoginsSequentially() {
  console.log("--- the same three checks, as async/await ---");
  try {
    const alice = await verifyCredentials("alice");
    console.log("Verified:", alice.username);
    const bob = await verifyCredentials("bob");
    console.log("Verified:", bob.username);
    const dave = await verifyCredentials("dave");
    console.log("Verified:", dave.username);
  } catch (err) {
    console.log("Error:", err.message);
  }
}

async function checkLoginsConcurrently() {
  console.log("");
  console.log("--- await Promise.all: same three checks, concurrently ---");
  const results = await Promise.all([
    verifyCredentials("alice"),
    verifyCredentials("bob"),
    verifyCredentials("carol"),
  ]);
  console.log(results.map((r) => r.username));
}

await checkLoginsSequentially();
await checkLoginsConcurrently();
