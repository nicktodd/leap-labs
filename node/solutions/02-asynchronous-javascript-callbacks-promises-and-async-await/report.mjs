import { verifyCredentials } from "./verify-credentials.mjs";

const usernames = ["dave", "erin", "mallory"];

async function checkSequentially(usernames) {
  for (const username of usernames) {
    try {
      const result = await verifyCredentials(username);
      console.log(`Verified: ${result.username}`);
    } catch (err) {
      console.log(`Not verified: ${username} (${err.message})`);
    }
  }
}

async function checkConcurrently(usernames) {
  const outcomes = await Promise.allSettled(usernames.map((u) => verifyCredentials(u)));
  outcomes.forEach((outcome, i) => {
    if (outcome.status === "fulfilled") {
      console.log(`Verified: ${outcome.value.username}`);
    } else {
      console.log(`Not verified: ${usernames[i]} (${outcome.reason.message})`);
    }
  });
}

console.log("--- sequential ---");
await checkSequentially(usernames);
console.log("--- concurrent ---");
await checkConcurrently(usernames);
